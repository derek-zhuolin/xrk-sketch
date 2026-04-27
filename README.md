# xrk-sketch · 小红书封面 · 手绘笔记本风格

复用 `sketchnote-style` 的视觉 DNA，专为小红书封面设计。

## 与 sketchnote-style 的差异

|  | sketchnote-style | xrk-sketch |
|---|---|---|
| 用途 | 多页 PPT / 流程图 | 单张小红书封面 |
| 画布 | 1600 × 900 横版 | **1242 × 1660 竖版（3:4）** |
| 标题字号 | 56 | **96-120**（缩略图也得清楚）|
| 输出 | 多个 SVG | **HTML 含 PNG 导出按钮** |
| 布局 | 三栏分布 | 标题 + 主视觉 + 装饰单页 |

## 目录

```
xrk-sketch/
├── SKILL.md                  # Skill 入口（自动触发）
├── prompts/
│   └── master-prompt.md      # SVG 生成 prompt 模板
├── templates/
│   └── cover.html            # HTML 包装（含 PNG 导出按钮）
└── examples/                 # 历次成功的样本
```

## 使用流程

1. 用户说"做个小红书封面/xhs 封面"，Claude 自动加载这个 skill
2. Claude 问三件事：主标题（8-14 字）/ 副标题 / 主视觉物件
3. Claude 按 `prompts/master-prompt.md` 生成 SVG
4. Claude 把 SVG 注入 `templates/cover.html` 的 `<!-- SVG_HERE -->` 位置
5. 保存到 `~/Desktop/{项目}/xhs-cover-{主题}-{日期}.html`
6. 双击 HTML → 浏览器打开 → 右上角「下载 PNG」按钮 → 得到 1242×1660 PNG

## PNG 导出原理

纯前端，零依赖：
1. 先 fetch Google Fonts CSS，把每个 woff2 转 base64 data URI（绕过 SVG 渲染时外部资源加载问题）
2. 把 inlined CSS 注入 SVG `<defs>`
3. `XMLSerializer` 序列化 SVG → Blob → Image → Canvas → `toBlob('image/png')`
4. 触发 `<a download>` 下载
5. 等 `document.fonts.ready` 后再导出，确保字体不缺失

## 风格 DNA（与 sketchnote-style 共享，缺一不可）

- **字体**：中文 Ma Shan Zheng + 英文 Architects Daughter（用 tspan 单独包英文）
- **手抖 filter**：feTurbulence + feDisplacementMap，所有形状都加 `filter="url(#rough)"`
- **Crosshatching**：45° + -45° 双层斜线，物体阴影必用，禁止纯色填充
- **色板**：纸色 #F5F0E6 / 暖黑 #2C2520 / 三色标签 / 六色颗粒
- **物件精度**：工业设计草图级别，不画卡通简笔画

## 常见失败模式

| 现象 | 修法 |
|---|---|
| 标题在 feed 里看不清 | 字号必须 ≥ 96，单行尽量 120 |
| 物件像简笔画 | hatch1 + hatch2 双层叠加 |
| PNG 导出空白 / 字体丢失 | 检查 `fontsToDataURI()` 是否成功，注意网络 |
| SVG 显示乱码 | xmlns 是否齐全 |
| 颜色太艳 | opacity 0.6-0.8 区间 |

## 迭代记录

- v1（2026-04-27）：基于 sketchnote-style v1 派生，竖版布局 + HTML 包装 + PNG 导出
