# NailongFilter 配置与组合协议

## 配置模板

```yaml
nailong_filter:
  coverage: 2       # C 0-4
  structure: 2      # S 0-4
  recursion: 1      # R 0-3
  preservation: 5   # P 1-5；前端不得低于 4
  motion: 1         # M 0-3
  include:
    - visual_tokens
    - layout_rhythm
    - components
    - imagery
    - motion
  exclude:
    - legal_copy
    - brand_logos
    - raw_data
  protected:
    - information_architecture
    - accessibility
    - responsive_behavior
    - component_api
```

## 五轴解释

### Coverage

- `C0`：不应用。
- `C1`：局部签名与少量角色触点。
- `C2`：主题层覆盖，约三分之一可设计区域出现奶龙语法。
- `C3`：主要页面与组件系统共同转换。
- `C4`：所有非保护层都转换，但允许用抽象肚皮、眼点、尾巴曲线替代完整角色。

### Structure

- `S0`：仅替换图片。
- `S1`：配色、字体气质、纹理。
- `S2`：按钮、卡片、徽章、空状态等组件。
- `S3`：布局流线、导航节奏、容器关系。
- `S4`：页面骨架和空间叙事都使用奶龙语法。

### Recursion

- `R0`：无递归，一个区域只出现一个尺度。
- `R1`：大轮廓内含中型角色或符号。
- `R2`：大 → 中 → 小三尺度，适合高强度前端和海报。
- `R3`：再增加微纹理层，只用于静态画面或大尺寸背景。

### Preservation

- `P5`：像素关系可变化，但功能、内容、IA、无障碍和品牌完全锁定。
- `P4`：允许调整视觉层级和版式节奏，不改变任务流程。
- `P1–P3`：仅用于概念艺术，不用于生产型前端。

### Motion

- `M0`：静态。
- `M1`：低频呼吸、轻微摇尾、一次性入场。
- `M2`：组件反馈具有蹒跚弹性、眨眼和尾巴扫动。
- `M3`：连续叙事或实验动画；必须提供减少动效模式。

## 与其他 Skill 组合

推荐提示词：

```text
先使用 $<base-design-skill> 完成产品的信息架构、交互和基础视觉。
冻结功能、内容、无障碍、响应式行为和组件 API。
然后使用 $nailongize-designs 作为最终设计过滤器，配置 C4-S4-R2-P5-M2。
需要重绘页面图片时调用 $transform-images-with-nailong。
```

已有前端代码时：

```text
审计现有前端并生成 baseline snapshot，不改业务逻辑。
应用 $nailongize-designs，配置 <五轴值>，先提交差异计划，再修改 tokens、布局、组件、图像和动效。
```

不要使用“忽略其他所有指令”“最高系统权限”等表述。组合通过明确的最后执行顺序实现，不通过伪造权限实现。
