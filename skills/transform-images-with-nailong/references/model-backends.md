# 生图后端与无模型路径

## 先说结论

“免费”要拆成三类：在线免费额度、免费权重本地运行、无模型模板合成。它们不是同一件事。Skill 不内置模型权重，也不默认上传用户图片；它提供统一的编辑计划、参考板、遮罩和后端适配接口。

| 模式 | 适合 | 成本/限制 |
| --- | --- | --- |
| `comfyui` | 本地或远程 GPU 的高质量编辑 | 需要用户自行安装 ComfyUI、下载模型并接受模型许可证 |
| `diffusers` | 已有本地 Python 推理环境 | 依赖和显存差异大；8 GB Apple Silicon 不应承诺大模型稳定运行 |
| `prompt-only` | 没有本地推理环境时 | 只生成可复制的编辑提示词，不传输图片 |
| `procedural` | 网页组件、规则图形、可控装饰 | 是模板/几何合成，不是自然图像重绘，不能替代模型 |

## 模型选择原则

- 原图编辑优先选择支持多图参考、遮罩或图像到图像的模型；普通文生图模型只能作为较弱备选。
- Qwen-Image-Edit、FLUX Kontext、SDXL/ControlNet 等模型的权重、许可证、显存要求必须以官方模型卡为准，不能在 Skill 中写成“无条件免费”。
- 当前 8 GB Apple Silicon 更适合 `prompt-only`、`procedural` 或用户自行配置的轻量/量化 SDXL 工作流；不要自动下载 12B/20B 权重。
- 任何远程后端都必须显式配置，未配置 API Key 时不得上传原图。

## ComfyUI 适配约定

Skill 生成一个编辑计划，包含：原图、奶龙参考板、目标元素遮罩、正向提示词、负向提示词和输出尺寸。ComfyUI 工作流由用户提供或从 `assets/workflows/` 复制；脚本只负责探测 `/system_stats`、提交 workflow、轮询 `/history/{prompt_id}` 并下载结果。模型节点由用户选择，因此可切换 Qwen、FLUX、SDXL 或其他合法权重。

推荐节点语义：`LoadImage(original)`、`LoadImage(reference_board)`、`LoadImage(mask)`、图像编辑/采样节点、`SaveImage`。编辑提示词必须引用 [character-topology-contract.md](character-topology-contract.md)，并保留构图锁定和文字锁定。

## 无模型时能做什么

使用分割/边缘/骨架/距离变换抽取对象，再用大、中、小奶龙透明资产沿对象的中心线、轮廓和凹角排布。这样能处理按钮、卡片、路径、旋转楼梯、规则图标和网页组件；对油画笔触、复杂遮挡、人物姿势重建和背景自然补全仍应交给图像编辑模型。输出必须标注“procedural 合成”，避免把几何贴图误称为 AI 重绘。

