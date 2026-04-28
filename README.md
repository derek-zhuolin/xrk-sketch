# xrk-sketch

> 小红书封面 · 手绘笔记本风格 · Claude Code Skill
>
> 一句话生成 1242×1660 竖版手绘风封面 · 一次给 3 版排版对比 · 浏览器一键导出 PNG

---

## ✨ 效果

- **手绘笔记本风格**：建筑师速写本线条 + crosshatching 阴影 + 水彩低饱和色块 + 散落颗粒
- **3 版默认对比**：每次自动给 3 个结构本质不同的排版（关键词大字 / 标题打散 / 卡片堆叠），一页对比 + 独立下载
- **PNG 一键导出**：纯前端、零依赖、字体内联（绕过 SVG 渲染丢字体的坑）
- **反 AI slop**：内置反隐喻黑名单（避免印章、灯泡、章鱼、火箭这些被用滥的图标）

---

## 🚀 安装（一行命令）

```bash
git clone https://github.com/derek-zhuolin/xrk-sketch.git ~/.claude/skills/xrk-sketch
```

不用 git？用 curl：

```bash
mkdir -p ~/.claude/skills && curl -L https://github.com/derek-zhuolin/xrk-sketch/archive/refs/heads/main.tar.gz | tar -xz -C ~/.claude/skills/ && mv ~/.claude/skills/xrk-sketch-main ~/.claude/skills/xrk-sketch
```

装完**重启 Claude Code**，skill 自动加载。

---

## 🎯 怎么触发

直接对 Claude Code 说，任意一句即可：

- "做一个小红书封面"
- "做个手绘风封面"
- "/xrk-sketch + 主题"
- "这篇文章配个封面"

Claude 会问你三件事：
1. **主标题**（8-14 字，缩略图下也要看得清）
2. **副标题**（可选，16-24 字）
3. **核心关键词**（2-4 字，不与标题重复）—— 你不给它会主动提炼

然后默认产出 **3 版排版** 一起给你看，你点喜欢的那版下载就行。

---

## 📁 文件结构

```
xrk-sketch/
├── SKILL.md                              # skill 入口（含完整工作流和决策原则）
├── prompts/
│   └── master-prompt.md                  # SVG 生成的完整 prompt 模板
├── templates/
│   ├── cover.html                        # 单版封面 HTML 模板（含 PNG 导出按钮）
│   └── gallery-builder.py                # 多版 gallery 拼接脚本
├── examples/
│   └── example-build-multi-variant.py    # 端到端样本：从主题→3 版 gallery
└── README.md                             # 本文件
```

---

## 🛠 默认工作流（3 版 gallery）

| 版本 | 排版 | 适合场景 |
|---|---|---|
| v1 关键词大字 | 中央 2-4 字大字 + 引号衬托 | 抽象主题 |
| v2 标题打散 | 主标题三段错位（Saul Bass 风）| 标题本身够强 |
| v3 卡片堆叠 | 3 张错落便签卡片，中央承载关键词 | 多维度内容 |

如果主题有强物件锚点（如望远镜、皮箱），v1 自动换成实物 icon 版。

---

## 🎨 风格 DNA（必做项）

- **字体**：中文 Ma Shan Zheng + 英文 Architects Daughter（英文必须用 `<tspan>` 单独包）
- **手抖 filter**：`feTurbulence` + `feDisplacementMap`，所有形状都加 `filter="url(#rough)"`
- **Crosshatching**：45° + -45° 双层斜线，物体阴影必用，禁止纯色填充
- **色板**：纸色 `#F5F0E6` / 暖黑 `#2C2520` / 标签三色 / 颗粒六色（opacity 0.6-0.8）
- **物件精度**：工业设计草图级别，不画卡通简笔画

---

## 🚫 反隐喻黑名单（避坑指南）

| 主题词 | **不要用** | 原因 |
|---|---|---|
| 高级品牌 / 奢侈品 | 印章、章子 | 作坊/官僚感，与"高级"反义 |
| 创意 / 灵感 | 灯泡 | 被用滥的 cliché |
| 多任务 / 协作 | 章鱼、瑞士军刀 | 烂大街图标 |
| 思维 / 洞察 | 大脑切片、齿轮人头 | AI 伪深度典型 |
| 增长 | 火箭、向上箭头 | 创业 PPT slop |

**自检问题**："LV / Apple / Hermès 会用这个物件做封面吗？"

---

## 🔧 PNG 导出原理（纯前端）

1. fetch Google Fonts CSS，把每个 woff2 转 base64 data URI（绕过 SVG 渲染丢字体）
2. 把 inlined CSS 注入 SVG `<defs>`
3. `XMLSerializer` 序列化 SVG → Blob → Image → Canvas → `toBlob('image/png')`
4. 触发 `<a download>` 下载
5. 等 `document.fonts.ready` 后再导出，确保字体不缺失

---

## 🐛 常见失败

| 现象 | 修法 |
|---|---|
| 标题在 feed 缩略图看不清 | 字号 ≥ 96，单行尽量 120 |
| 物件像简笔画 | hatch1 + hatch2 双层叠加 |
| PNG 导出空白 / 字体丢失 | 检查网络（要拉 Google Fonts），或换镜像源 |
| SVG 显示乱码 | 检查 xmlns 是否齐全 |
| 颜色太艳 | opacity 控制在 0.6-0.8 |

---

## 📜 依赖前置

- **Claude Code** 已安装（必须）
- **Python 3**（系统自带，用于多版 gallery 拼接脚本）
- **网络**：要能访问 Google Fonts（PNG 导出时要拉字体）

---

## 🔗 相关

- 本 skill 的视觉 DNA 派生自 `sketchnote-style`（多页 PPT 风），但用途、画布、布局完全独立
- skill 由 [Claude Code](https://claude.com/claude-code) 自动加载，无需手动注册

---

## 📄 License

MIT — 自由使用、修改、分发。

---

## 💡 反馈

欢迎在 [GitHub Issues](https://github.com/derek-zhuolin/xrk-sketch/issues) 提需求或 bug。
