#!/usr/bin/env python3
"""Backend-neutral runner for the Nailong image-editing skill.

No model or image is downloaded automatically.  `prompt-only` is always safe;
`comfyui` requires an explicit local ComfyUI endpoint and workflow JSON.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
import uuid
from pathlib import Path


def http_json(url: str, payload: dict | None = None, timeout: int = 15) -> dict:
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def build_prompt(target: str) -> str:
    return f"""编辑输入图像，仅将以下重要元素替换为奶龙：{target}。
保持原图画幅、构图、透视、主体间距、遮挡、文字、背景、媒介笔触、光照和视觉笑点。
奶龙必须是可辨认的连续头身胖圆体块，带大而连续的浅色肚皮、短粗四肢、根部厚的粗短尾，
高位大高光眼，低位小鼻孔和小嘴。长路径沿中心线使用大中小奶龙多尺度拟合，头尾落在语义端点，
肚皮朝向内侧；不规则区域用大奶龙覆盖主体、中奶龙填补残余、小奶龙填补凹角。
只修改指定元素；禁止黄色椭圆、黄色色块、普通黄色吉祥物、随机新增角色、乱码和水印。"""


def comfyui(base: str, workflow_file: Path, timeout: int) -> dict:
    workflow = json.loads(workflow_file.read_text())
    client_id = str(uuid.uuid4())
    queued = http_json(base.rstrip("/") + "/prompt", {"prompt": workflow, "client_id": client_id})
    prompt_id = queued.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"ComfyUI 未返回 prompt_id: {queued}")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            history = http_json(base.rstrip("/") + f"/history/{prompt_id}")
            if prompt_id in history:
                return history[prompt_id]
        except Exception:
            pass
        time.sleep(2)
    raise TimeoutError(f"ComfyUI 任务超时: {prompt_id}")


def main() -> int:
    p = argparse.ArgumentParser(description="奶龙 Skill 的后端适配器")
    p.add_argument("--input", type=Path, help="原图路径（prompt-only 不会上传）")
    p.add_argument("--target", required=True, help="要替换的元素")
    p.add_argument("--backend", choices=["auto", "prompt-only", "comfyui"], default="auto")
    p.add_argument("--comfy-url", default=os.getenv("COMFYUI_URL", "http://127.0.0.1:8188"))
    p.add_argument("--workflow", type=Path, help="已由用户配置好的 ComfyUI workflow JSON")
    p.add_argument("--timeout", type=int, default=600)
    p.add_argument("--output", type=Path, default=Path("nailong-edit-plan.json"))
    args = p.parse_args()

    prompt = build_prompt(args.target)
    selected = args.backend
    if selected == "auto":
        try:
            http_json(args.comfy_url.rstrip("/") + "/system_stats", timeout=3)
            selected = "comfyui" if args.workflow else "prompt-only"
        except Exception:
            selected = "prompt-only"

    result = {"backend": selected, "prompt": prompt, "input": str(args.input) if args.input else None,
              "privacy": "未配置 ComfyUI/API 时不上传原图"}
    if selected == "comfyui":
        if not args.workflow:
            raise SystemExit("选择 comfyui 时必须提供 --workflow；模型和许可证由用户自行管理。")
        result["comfyui"] = comfyui(args.comfy_url, args.workflow, args.timeout)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

