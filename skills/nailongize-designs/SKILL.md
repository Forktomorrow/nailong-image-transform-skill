---
name: nailongize-designs
description: Apply a systematic 奶龙 (Nailong) transformation as the final design pass over an existing or newly generated frontend, website, UI prototype, dashboard, slide deck, infographic, visual system, or coded interface. Use when the user asks to 奶龙化网页/前端/UI/所有元素/整体结构, add Nailong as a global design filter, compose this with another design skill, increase or tune 奶龙化强度, make buttons/cards/navigation visibly adopt Nailong poses, fit irregular shapes with coherent large-medium-small Nailong instances, or turn an otherwise complete design into a coherent Nailong world while preserving content, usability, accessibility, responsive behavior, and data accuracy.
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
- `R Resolution 0–3`：使用几级尺寸的奶龙共同拟合目标区域。它表示大、中、小实例的尺度层级，不表示把一张奶龙图片嵌进另一张图片。
- `P Preservation 1–5`：对功能、内容和品牌基线的保护强度；前端默认 5，不得低于 4。
- `M Motion 0–3`：眨眼、呼吸、摇尾、蹒跚弹性等动效强度。

用户说“所有东西都奶龙化”“最高强度”时，默认 `C4-S4-R2-P5-M2`，而不是降低可用性保护。

## 强度原则

- `C1`：签名层。每屏 1–2 个角色触点，其他设计不变。
- `C2`：主题层。统一色彩、图像、空状态和少数组件。
- `C3`：系统层。组件形态、布局节奏、图像和动效共同奶龙化。
- `C4`：世界层。所有非受保护元素都经过奶龙语法翻译；不等于每个像素都塞完整角色。

结构深度、前端元素映射和禁止事项读取 [frontend-layer-matrix.md](references/frontend-layer-matrix.md)。

## 分型拟合与多尺度奶龙化

对不规则区域、长路径、组件群和大面积背景使用多实例尺度拟合，而不是均匀复制角色或嵌套其他素材。开始前必须读取 `../transform-images-with-nailong/references/character-topology-contract.md` 并查看其角色参考板；任何组件都不能退化成黄色椭圆、色块或通用小龙：

1. 先把目标区域视为遮罩，提取外轮廓、中心骨架、凹角、窄端和视觉重心。
2. 用 1–3 个大奶龙承担主轮廓和语义，不强求一只角色覆盖全部边角。
3. 用中型奶龙沿凹角、转折和边界补形；用小奶龙补剩余窄缝，并让朝向、视线和动作形成群体关系。
4. 同一组角色必须共享画风、光线和材质。禁止把蒙娜丽莎、呐喊、水墨等异质奶龙素材缩小后塞进界面充当递归。
5. `R0` 到 `R3` 每一级都重新求解整张构图：重新分配实例数量、大小、姿态、位置、遮挡和负空间；禁止保留上一层构图后只追加更小副本。
6. 前端默认 `R≤2`，静态画面可用 `R=3`。文字、表单和数据区保留负空间，但控件外形可以直接变成躺卧、蜷缩、探头或伸展的奶龙。

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
2. 写一份差异计划：保留项、形态替换项、拟合遮罩、多尺度角色组、图像任务、动效任务。
3. 先改全局 Token 和布局节奏，再改单个组件。
4. 先让组件本身获得奶龙形态：按钮可成为横卧奶龙，侧栏可成为蜷曲奶龙，标签可成为探头小奶龙；不要只换成黄黑色块。
5. 对 hero、插画、背景和复杂角色群使用同画风图像资产；需要重绘时调用图片 Skill。
6. 最后添加低频动效，优先呼吸、眨眼、摇尾和按压回弹，并支持 `prefers-reduced-motion`。
7. 在桌面、手机、键盘导航和减少动效模式下验证。

## 输出要求

交付作品时同时给出：

- 使用的五轴值。
- 哪些层被奶龙化，哪些受保护。
- 生成或修改的图像资产路径。
- 验证结果与仍存在的限制。
