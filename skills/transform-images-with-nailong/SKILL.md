---
name: transform-images-with-nailong
description: Transform an uploaded meme, artwork, photo, poster, screenshot, or illustration by replacing its important visual elements with 奶龙 (Nailong) while preserving the source composition, visual hierarchy, captions, style, lighting, perspective, and joke logic. Use when the user asks for 奶龙化、奶龙替换、把主角/月亮/太阳/物体变成奶龙、制作奶龙表情包，或 wants a reusable prompt for an image-generation or image-editing model to perform that transformation.
---

# 奶龙元素替换

把输入图像视为需要精确编辑的底图，不要仅把整张图改成黄色，也不要无差别铺满奶龙。

## 工作流

1. 读取输入图像并判断任务类型：
   - 用户要求保留原图并替换元素时，执行图像编辑。
   - 用户只提供构图或画风参考时，按参考图重新生成。
2. 建立元素清单，按优先级排序：
   - 一级：主角、最大物体、梗的核心对象。
   - 二级：月亮、太阳、标志性道具、视线焦点。
   - 三级：重复图标、装饰物或背景中的次要对象。
3. 只选择支撑画面语义的关键元素。默认替换 1–8 个；密集图案可增加，但避免让奶龙覆盖所有纹理。
4. 先按几何与功能选择变形模式，再写替换映射：`原元素 -> 模式 -> 奶龙形态/动作 -> 必须继承的属性`。模式选择读取 [transformation-patterns.md](references/transformation-patterns.md)。
5. 生成编辑提示词，并明确：只改映射中的元素；其余像素级关系尽量保持不变。
6. 使用可编辑输入图像的生图工具执行。若当前环境没有图像编辑工具，输出可直接复制的完整提示词。
7. 检查结果；一次只修一个问题，并重复所有不变量。

需要选择推理方式时，读取 [model-backends.md](references/model-backends.md)。没有生图模型也要做预览或网页组件拟合时，读取 [algorithmic-pipeline.md](references/algorithmic-pipeline.md)，使用“视觉分析 + 多尺度奶龙资产拟合 + 遮罩合成”，不要把卷积/池化误写成生成器。仓库附带 `scripts/generate_nailong.py`：默认只生成编辑计划；检测到用户明确提供的 ComfyUI 与 workflow 后才提交本地任务。

若要求保留原画笔触、颗粒、光照和媒介风格，必须读取 [style-preserving-raster-replacement.md](references/style-preserving-raster-replacement.md)。此时禁止直接叠加现成奶龙 PNG；奶龙应作为矢量拓扑和 mask，原画纹理、梯度和局部统计负责填充其内部。

需要比较算法与高质量示例时，读取 [benchmark.md](references/benchmark.md)，运行 `scripts/benchmark_nailong.py` 记录五项分数；低于 70 分不得宣称可用。

需要提升无模型质量或判断场景上限时，读取 [no-model-optimization.md](references/no-model-optimization.md)。不要通过降低标准、增加奶龙数量或改变权重来伪造提分。

需要根据原物体选择姿态时，读取 [pose-grammar.md](references/pose-grammar.md)；需要覆盖名画和东方绘画案例时，读取 [benchmark-suite.md](references/benchmark-suite.md)。固定站立奶龙不得作为默认姿态。

需要实现跨场景自动适配时，读取 [adaptive-topology-generator.md](references/adaptive-topology-generator.md)。案例表只能作为评测集，不能写成场景硬编码；必须从 mask 的轮廓、骨架、宽度场、曲率和视觉重心自动检索并变形姿态。

需要准确描述奶龙外观时，必须同时读取 [character-spec.md](references/character-spec.md) 与 [character-topology-contract.md](references/character-topology-contract.md)，并查看 `assets/reference/nailong-reference-board.webp`。角色参考与拓扑合同优先于临时提示词；只做黄色椭圆或通用小龙判定为失败。需要选择对象变形方式或诊断失败结果时，读取 [transformation-patterns.md](references/transformation-patterns.md)。需要跨模型复制提示词时，读取 [universal-prompt.md](references/universal-prompt.md)。需要参考完整案例时，读取 [examples.md](references/examples.md)。

## 替换规则

- 保留原元素的中心位置、占画比例、朝向、动作方向、透视、遮挡和视觉权重。
- 用奶龙的全身、半身、头部或轮廓适配原元素，不强行使用同一种姿势。
- 原元素承担功能时，让奶龙继续承担该功能。例如月亮改为发光的蜷缩奶龙，人物改为做同一动作的奶龙，道具改为轮廓匹配的奶龙形态。
- 紧凑圆形对象（月亮、太阳、气泡）用一只肥圆奶龙紧凑蜷缩；不要把它处理成长条。
- 长路径对象（旋转楼梯、河流、丝带、道路）用一只长条奶龙沿对象中心线连续盘绕。头和尾分别落在路径两端，浅色肚皮形成连续内侧带，短肢贴在转折处；身体宽度继承原路径宽度。它可以很长，但不能退化成没有头尾和肚皮的管道。
- 山体、云团等大块地形采用“双重识别”：远看仍是山势或云势，近看才能辨认奶龙的头、背、肚皮与尾巴。允许树木、皴法和岩石纹理延续到奶龙身体表面。
- 动态主体优先继承速度、重心、动作方向和受力关系，不要机械复制原物种的外轮廓。
- 飘带、烟雾、笔触等附属轨迹用于延续动作，不要把它们误当成可随意删除的装饰。
- 重复元素分别生成姿态或表情略有差别的奶龙，但保持节奏和数量关系。
- 奶龙必须仍然可辨认：头身连续的黄色胖圆体块、大而连续的浅色肚皮、短粗四肢、根部厚的粗短尾、大而高位的高光眼，以及低位小鼻孔和小嘴。
- 让奶龙继承原图媒介。油画保留笔触，像素图保留像素网格，黑白漫画保留网点与线条，照片匹配光照和景深。
- 表情包默认保留所有文字、字号、位置、排版和拼写。只有用户明确要求时才改字。
- 不添加输入图中不存在的新道具、文字、水印、边框或额外角色。

## 提示词结构

按以下顺序组织最终提示词：

```text
任务：编辑输入图像，把指定重要元素替换成奶龙。
替换映射：
- <原元素 1> -> <奶龙姿态/形态>；继承 <位置、大小、方向、功能>
- <原元素 2> -> <奶龙姿态/形态>；继承 <位置、大小、方向、功能>

奶龙识别特征：<按 character-spec.md 写成一行>
风格匹配：严格继承原图的 <媒介、笔触/材质、色彩、光照、噪点或像素特征>。
构图锁定：保持画幅、镜头、透视、主体间距、留白、遮挡和层次不变。
文字锁定：原图文字逐字保留，不新增文字。
只修改：上述替换对象。
必须保留：<背景与未替换元素>。
避免：随机增加奶龙、黄色涂抹、构图漂移、错误肢体、不同角色、文字乱码、水印。
```

不要把过程分析塞进生图提示词。先内部完成元素清单，再给模型简洁、可执行的编辑指令。

## 结果检查

按顺序核对：

1. 梗或原图主题是否仍然一眼可读。
2. 所有选定关键元素是否真的变成奶龙，而不只是变黄。
3. 选择的变形模式是否匹配原对象：圆团、长路径、地形、动态主体或重复阵列。
4. 奶龙数量、位置、尺度、朝向、头尾关系和遮挡是否对应原元素。
5. 原构图、背景、画风、光影和文字是否保持。
6. 是否出现额外角色、随机装饰、乱码、水印、畸形肢体或无结构的黄色管道。

若不合格，使用局部修订语句：`仅修正 <具体问题>；继续保持 <全部不变量> 不变。`

## 边界

- 不声称不同平台会自动读取 Codex Skill。平台不支持 Skill 时，使用 `references/universal-prompt.md` 中的通用块。
- 当前任务是网页、UI、幻灯片或完整设计系统时，先使用 `$nailongize-designs` 建立跨层过滤计划；本 Skill 只负责其中需要重绘的位图资产。
- 不把示例图当作唯一造型模板；它用于说明替换逻辑和画风继承。
- 不移除原作者签名或来源标记。遇到水印时保留，除非用户拥有图像并明确要求合法清理。
