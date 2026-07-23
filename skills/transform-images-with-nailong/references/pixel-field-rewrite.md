# 像素场重写：从原物体到奶龙

当前固定模板算法的问题是：先绘制奶龙，再把局部纹理覆盖上去。正确方法应当把原物体区域视为一个像素场，逐像素映射到新的奶龙拓扑中。

## 变量

- `I(x,y)`：原图像素；
- `M(x,y)`：原物体 mask；
- `N(u,v)`：由奶龙拓扑生成的新 mask；
- `S_M`、`S_N`：原区域和新拓扑的骨架；
- `D_M`、`D_N`：距离变换；
- `G_M`：原区域局部笔触/梯度方向场。

## 1. 自动得到真实色块

不用固定坐标框。先在局部邻域计算颜色、梯度和纹理的联合距离：

```text
d(p,q) = wc * color_distance(p,q)
       + wg * gradient_distance(p,q)
       + wt * texture_distance(p,q)
```

从种子点向相似像素扩张，配合闭运算、开运算、孔洞填充和连通域筛选，得到 `M`。边界由局部对比度和曲率共同决定，避免把周围笔触误切进物体。

## 2. 从原区域学习形状坐标

对 `M` 和 `N` 分别计算骨架和距离场。每个像素转换为骨架坐标：

```text
phi(p) = (arc_length_to_skeleton, signed_normal_distance / local_width)
```

新 mask 的像素 `p_N` 通过相同的 `phi` 找到原区域采样点 `p_M`。这一步是“原物体像素随奶龙形状变形”，不是把一张奶龙图放到原图上。

## 3. 逐像素颜色与笔触变换

对采样像素分成低频和高频：

```text
base = GaussianBlur(I[p_M])
detail = I[p_M] - base
```

将 `base` 转换到黄奶龙的颜色轨道，但保留原区域的亮度和明暗关系；将 `detail` 按 `G_M` 的方向投影到新形状。输出像素为：

```text
Y(p_N) = yellow_palette(local_style) * luminance(base)
       + alpha(phi) * project(detail, G_M)
```

腹皮只修改颜色轨道和局部亮度，不覆盖原笔触；眼、鼻、嘴、四肢和尾巴是从拓扑锚点生成的局部像素场，颜色仍由周围原画统计决定。

## 4. 边界和整体性

目标区域内部完成像素重写后，只在 `N` 的窄边带做梯度域融合：边界梯度取原背景和新物体梯度的加权和，求解 Poisson 方程得到连续边缘。背景之外的像素不参与优化，确保原画构图和笔触不漂移。

## 5. 迭代优化

每次迭代同时更新奶龙拓扑参数和像素映射参数：

```text
E = mask_error
  + topology_error
  + style_field_error
  + boundary_gradient_error
  + background_change_penalty
```

如果边界或风格项没有改善，回滚该次更新；不允许通过增加奶龙数量掩盖像素融合失败。

这套流程才是“把原来的色块和像素改造成奶龙”，而不是“在原画上生成几个奶龙”。当前 `raster_nailong.py` 仍是旧的 P2 基线，不能宣称已经实现本规范。

