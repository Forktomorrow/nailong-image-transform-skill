# 奶龙元素替换 Skill

把表情包、名画、照片或插画中的关键视觉元素替换成奶龙，同时尽量保留原构图、文字、光影和画风。

在线展示：[奶龙化元素实验室](https://forktomorrow.github.io/nailong-image-transform-skill/)

仓库包含两种用法：

- Codex：安装插件后调用 `$transform-images-with-nailong`，上传图片并说明要奶龙化。
- 其他生图模型：上传图片，复制 `skills/transform-images-with-nailong/references/universal-prompt.md` 中的通用编辑块。

## 目录

```text
.codex-plugin/plugin.json
skills/transform-images-with-nailong/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── character-spec.md
│   ├── examples.md
│   ├── transformation-patterns.md
│   └── universal-prompt.md
└── assets/examples/
    └── starry-night-nailong-example.jpg
```

## 使用示例

```text
使用 $transform-images-with-nailong，把这张表情包中决定笑点的人物和道具替换成奶龙，字幕、背景和构图保持不变。
```

模型如果不认识“奶龙”，请同时附上示例图，并保留 Skill 中的完整外观描述。

## 视觉测试

展示页包含星空原图滑动对比，《蒙娜丽莎》《创造亚当》《呐喊》等西方构图测试，以及富春山居、千里江山、水墨奔马和敦煌飞天等东方绘画实验。页面源码位于 `docs/`，由 GitHub Pages 发布。

## 安装

把本仓库作为 Codex 插件源安装，或复制 `skills/transform-images-with-nailong` 到本地 Skills 目录。安装后重新打开一个任务，让 Codex 重新发现 Skill。

## 说明

本项目是非官方的提示词与工作流工具，与奶龙角色权利方无隶属或授权关系。MIT 许可仅覆盖本仓库原创的文字、配置和代码，不覆盖奶龙角色形象、示例底图或其他第三方素材。使用生成结果时请遵守所用平台规则及当地版权、商标和肖像权要求。
