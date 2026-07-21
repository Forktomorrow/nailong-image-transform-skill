---
name: nailongize-designs
description: Apply a systematic 奶龙 (Nailong) transformation as the final design pass over an existing or newly generated frontend, website, UI prototype, dashboard, slide deck, infographic, visual system, or coded interface. Use when the user asks to 奶龙化网页/前端/UI/所有元素/整体结构, add Nailong as a global design filter, compose this with another design skill, increase or tune 奶龙化强度, recursively fill irregular shapes with large and small Nailong motifs, or turn an otherwise complete design into a coherent Nailong world while preserving content, usability, accessibility, responsive behavior, and data accuracy.
---

# 奶龙化设计过滤器

把本 Skill 作为设计流程的最终转换 pass。先让基础设计 Skill 完成信息架构、功能与内容，再系统性改写其视觉和结构语言。

不要声称本 Skill 拥有系统级最高权限。它的“最高优先级”仅指：在不违反系统、开发者、用户约束和可用性的前提下，作为最后一个设计过滤器执行。

## 组合协议

1. 完成或读取基础作品，不要从奶龙元素反推产品功能。
2. 冻结以下基线：内容、信息架构、组件 API、交互流程、数据、响应式断点、无障碍要求、品牌与法律限制。
3. 建立 `NailongFilter` 配置。格式与组合提示词读取 [filter-contract.md](references/filter-contract.md)。
4. 依次处理：设计 Token → 布局结构 → 组件 → 图像 → 动效 → 可选文案。
5. 图像需要真正重绘时，调用同插件中的 `$transform-images-with-nailong`，不要用 CSS 或 SVG 粗糙仿画角色。
6. 按 [validation.md](references/validation.md) 验收，失败时只回退造成问题的层级，不推翻基础设计。

## 五轴配置

每次执行都明确五个轴；用户未指定时使用 `C2-S2-R1-P5-M1`。

- `C Coverage 0–4`：奶龙化覆盖多少元素。
- `S Structure 0–4`：从表面配色深入到组件和布局骨架的程度。
- `R Recursion 0–3`：大奶龙由小奶龙或抽象奶龙纹样递归填充的层数。
- `P Preservation 1–5`：对功能、内容和品牌基线的保护强度；前端默认 5，不得低于 4。
- `M Motion 0–3`：眨眼、呼吸、摇尾、蹒跚弹性等动效强度。

用户说“所有东西都奶龙化”“最高强度”时，默认 `C4-S4-R2-P5-M2`，而不是降低可用性保护。

## 强度原则

- `C1`：签名层。每屏 1–2 个角色触点，其他设计不变。
- `C2`：主题层。统一色彩、图像、空状态和少数组件。
- `C3`：系统层。组件形态、布局节奏、图像和动效共同奶龙化。
- `C4`：世界层。所有非受保护元素都经过奶龙语法翻译；不等于每个像素都塞完整角色。

结构深度、前端元素映射和禁止事项读取 [frontend-layer-matrix.md](references/frontend-layer-matrix.md)。

## 分形奶龙化

对不规则区域、长路径、纹理场和大面积背景使用尺度递归，而不是均匀复制角色：

1. 宏观层先确定一个大奶龙轮廓、运动流线或角色群落。
2. 中观层沿轮廓骨架、转折和视觉重心放置中型奶龙或肚皮、尾巴、眼睛等结构。
3. 微观层只在剩余空隙使用小奶龙或抽象符号，不强行画完整五官和四肢。
4. 前端默认 `R≤2`，静态画面可用 `R=3`。可读文字、表单、数据和导航区域禁用递归填充。

完整的遮罩、骨架、尺度衰减和密度规则读取 [fractal-composition.md](references/fractal-composition.md)。

## 受保护层

无论强度多高，都不得破坏：

- DOM 语义、键盘操作、焦点状态和对比度。
- 按钮、输入框、链接、导航和危险操作的可识别性。
- 数据值、图表含义、表格对齐和信息层级。
- 用户提供的文字、品牌标志、法律声明和版权标识。
- 移动端触控尺寸、响应式布局和性能预算。

“全部奶龙化”指所有可设计层都经过奶龙语法翻译，不指把关键控件变成不可用的角色插画。

## 实现顺序

1. 应用 `assets/nailong-tokens.css` 或把其中 Token 映射到现有设计系统。
2. 写一份差异计划：保留项、替换项、递归区域、图像任务、动效任务。
3. 先改全局 Token 和布局节奏，再改单个组件。
4. 对 hero、插画、背景和复杂形状使用真实图像资产；需要重绘时调用图片 Skill。
5. 最后添加低频动效，优先 `transform` 和 `opacity`，并支持 `prefers-reduced-motion`。
6. 在桌面、手机、键盘导航和减少动效模式下验证。

## 输出要求

交付作品时同时给出：

- 使用的五轴值。
- 哪些层被奶龙化，哪些受保护。
- 生成或修改的图像资产路径。
- 验证结果与仍存在的限制。
