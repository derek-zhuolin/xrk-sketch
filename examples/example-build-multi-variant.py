#!/usr/bin/env python3
"""Build 3 brand-marketing cover variants + 1 gallery HTML."""

import re
import subprocess
from pathlib import Path

base = Path.home() / "Desktop/好看的视觉海报"
demo = base / "xhs-cover-demo"
out = base / "品牌营销-gallery"
out.mkdir(exist_ok=True)

SUB_OLD = re.compile(r'与时俱进，让品牌跑赢 <tspan font-family="\'Architects Daughter\', cursive">AI</tspan>')
SUB_NEW = '停下来，先想清楚一件事'

CAPTION_OLD = re.compile(r'写给还在用 <tspan font-family="\'Architects Daughter\', cursive">1\.0</tspan> 套路做品牌的你')
CAPTION_NEW = '写给在工具里迷路的品牌人'

TITLE_OLD = re.compile(r'<tspan font-family="\'Architects Daughter\', cursive" font-weight="700">GPT 2\.0</tspan> 帮你做品牌')
TITLE_NEW = '品牌营销该怎么做'


def common(content):
    content = SUB_OLD.sub(SUB_NEW, content)
    content = CAPTION_OLD.sub(CAPTION_NEW, content)
    content = content.replace('>策略</text>', '>是什么</text>')
    content = content.replace('>内容</text>', '>给谁</text>')
    content = content.replace('>视觉</text>', '>怎么记</text>')
    content = content.replace('>破局</text>', '>本质</text>')
    return content


# v1: 关键词大字
src = (demo / "v2-纯版式.html").read_text(encoding="utf-8")
content = common(src)
content = TITLE_OLD.sub(TITLE_NEW, content)
(out / "v1-关键词.html").write_text(content, encoding="utf-8")

# v2: 标题打散
src = (demo / "v3-标题打散.html").read_text(encoding="utf-8")
content = common(src)
# Original split: "GPT 2.0" / "帮你做" / "品牌"
# New split: "品牌营销" / "该" / "怎么做"
content = content.replace('>GPT 2.0<', '>品牌营销<')
content = content.replace('>帮你做<', '>该<')
content = content.replace('>品牌<', '>怎么做<')
(out / "v2-标题打散.html").write_text(content, encoding="utf-8")

# v3: 卡片堆叠
src = (demo / "v4-卡片堆叠.html").read_text(encoding="utf-8")
content = common(src)
content = TITLE_OLD.sub(TITLE_NEW, content)
(out / "v3-卡片堆叠.html").write_text(content, encoding="utf-8")

print("Generated 3 variant files")

# Build gallery
variants = [
    (1, "v1-关键词.html", "关键词「本质」", "无 icon · 极简留白 · 大字驱动"),
    (2, "v2-标题打散.html", "标题打散错位", "字本身=主视觉"),
    (3, "v3-卡片堆叠.html", "卡片堆叠", "便签纸 · 设计师工作台"),
]


def extract_svg(text):
    m = re.search(r'<svg viewBox="0 0 1242 1660".*?</svg>', text, re.DOTALL)
    return m.group(0) if m else ""


svgs = {v: extract_svg((out / f).read_text(encoding="utf-8")) for v, f, _, _ in variants}

gallery_head = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>品牌营销该怎么做 · 3 版对比</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Architects+Daughter&display=swap');
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: #E8E2D5; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif; }
  body { padding: 40px 30px 80px; }
  header { max-width: 1400px; margin: 0 auto 40px; text-align: center; }
  header h1 { font-size: 28px; color: #2C2520; margin: 0 0 8px; font-weight: 600; }
  header p { color: #6B5D4F; font-size: 14px; margin: 0; }
  .grid { max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 36px; }
  .card { display: flex; flex-direction: column; gap: 16px; }
  .stage { aspect-ratio: 3 / 4; background: #fff; box-shadow: 0 12px 36px rgba(44, 37, 32, 0.18); border-radius: 10px; overflow: hidden; transition: transform 0.2s ease, box-shadow 0.2s ease; }
  .stage:hover { transform: translateY(-4px); box-shadow: 0 16px 48px rgba(44, 37, 32, 0.28); }
  .stage svg { width: 100%; height: 100%; display: block; }
  .meta { text-align: center; }
  .meta h3 { margin: 0 0 4px; font-size: 18px; color: #2C2520; font-weight: 600; }
  .meta .desc { color: #6B5D4F; font-size: 13px; margin: 0 0 14px; }
  .btn-row { display: flex; gap: 10px; justify-content: center; }
  .btn { padding: 9px 18px; border: 1.5px solid #2C2520; background: #F5F0E6; color: #2C2520; font-size: 13px; font-weight: 600; border-radius: 999px; cursor: pointer; box-shadow: 0 1px 4px rgba(44, 37, 32, 0.08); transition: all 0.15s ease; font-family: inherit; }
  .btn:hover { transform: translateY(-1px); box-shadow: 0 3px 10px rgba(44, 37, 32, 0.16); }
  .btn[disabled] { opacity: 0.5; cursor: wait; }
  .btn.primary { background: #2C2520; color: #F5F0E6; }
  .toast { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(20px); background: #2C2520; color: #F5F0E6; padding: 12px 22px; border-radius: 999px; font-size: 14px; opacity: 0; pointer-events: none; transition: opacity 0.25s ease, transform 0.25s ease; z-index: 200; }
  .toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
</style>
</head>
<body>
<header>
  <h1>品牌营销该怎么做 · 3 版排版对比</h1>
  <p>1242×1660 · 手绘笔记本风格 · 每张下方可独立下载 PNG</p>
</header>
<div class="grid">
"""

cards = ""
for v, _, name, desc in variants:
    cards += f"""
  <div class="card">
    <div class="stage" data-v="{v}">
{svgs[v]}
    </div>
    <div class="meta">
      <h3>v{v} · {name}</h3>
      <p class="desc">{desc}</p>
      <div class="btn-row">
        <button class="btn primary" onclick="downloadPng({v})">下载 PNG</button>
        <button class="btn" onclick="copyPng({v})">复制</button>
      </div>
    </div>
  </div>"""

gallery_tail = """
</div>
<div class="toast" id="toast"></div>
<script>
const SVG_WIDTH = 1242;
const SVG_HEIGHT = 1660;
const FONT_CSS_URL = 'https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Architects+Daughter&display=swap';
let cachedFontsCSS = null;
const toast = document.getElementById('toast');
function showToast(msg, ms = 1800) { toast.textContent = msg; toast.classList.add('show'); clearTimeout(showToast._t); showToast._t = setTimeout(() => toast.classList.remove('show'), ms); }
async function fetchInlinedFontsCSS() {
  if (cachedFontsCSS) return cachedFontsCSS;
  const cssText = await fetch(FONT_CSS_URL).then(r => r.text());
  const fontUrls = [...cssText.matchAll(/url\\((https:[^)]+)\\)/g)].map(m => m[1]);
  const replacements = await Promise.all(fontUrls.map(async (url) => {
    try {
      const buf = await fetch(url).then(r => r.arrayBuffer());
      let bin = '';
      const bytes = new Uint8Array(buf);
      for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
      return [url, `data:font/woff2;base64,${btoa(bin)}`];
    } catch (e) { return [url, url]; }
  }));
  let inlined = cssText;
  for (const [orig, dataUri] of replacements) inlined = inlined.split(orig).join(dataUri);
  cachedFontsCSS = inlined;
  return inlined;
}
async function svgToPngBlob(svgEl, scale = 1) {
  const clone = svgEl.cloneNode(true);
  if (!clone.getAttribute('xmlns')) clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  clone.setAttribute('width', SVG_WIDTH);
  clone.setAttribute('height', SVG_HEIGHT);
  const inlinedCSS = await fetchInlinedFontsCSS();
  let defs = clone.querySelector('defs');
  if (!defs) { defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs'); clone.insertBefore(defs, clone.firstChild); }
  const styleEl = document.createElementNS('http://www.w3.org/2000/svg', 'style');
  styleEl.textContent = inlinedCSS;
  defs.insertBefore(styleEl, defs.firstChild);
  const svgString = new XMLSerializer().serializeToString(clone);
  const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
  const url = URL.createObjectURL(svgBlob);
  try {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    await new Promise((resolve, reject) => { img.onload = resolve; img.onerror = () => reject(new Error('SVG image load failed')); img.src = url; });
    const canvas = document.createElement('canvas');
    canvas.width = SVG_WIDTH * scale; canvas.height = SVG_HEIGHT * scale;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#F5F0E6'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    return await new Promise((resolve) => canvas.toBlob(resolve, 'image/png', 1));
  } finally { URL.revokeObjectURL(url); }
}
const versionNames = { 1: '关键词本质', 2: '标题打散', 3: '卡片堆叠' };
async function downloadPng(version) {
  const card = document.querySelector(`[data-v="${version}"]`).parentElement;
  const btn = card.querySelector('.btn.primary');
  const svgEl = card.querySelector('svg');
  btn.disabled = true; btn.textContent = '生成中…';
  try {
    await document.fonts.ready;
    const blob = await svgToPngBlob(svgEl, 1);
    const a = document.createElement('a');
    a.download = `xhs-品牌营销-v${version}-${versionNames[version]}.png`;
    a.href = URL.createObjectURL(blob);
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    showToast(`v${version} PNG 已下载`);
  } catch (e) { console.error(e); showToast('导出失败：' + e.message, 3000); }
  finally { btn.disabled = false; btn.textContent = '下载 PNG'; }
}
async function copyPng(version) {
  const card = document.querySelector(`[data-v="${version}"]`).parentElement;
  const btn = card.querySelectorAll('.btn')[1];
  const svgEl = card.querySelector('svg');
  btn.disabled = true; btn.textContent = '复制中…';
  try {
    await document.fonts.ready;
    const blob = await svgToPngBlob(svgEl, 1);
    if (!navigator.clipboard || !window.ClipboardItem) throw new Error('当前浏览器不支持图片剪贴板');
    await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]);
    showToast(`v${version} 已复制`);
  } catch (e) { console.error(e); showToast(e.message, 3000); }
  finally { btn.disabled = false; btn.textContent = '复制'; }
}
</script>
</body>
</html>
"""

gallery_path = out / "gallery.html"
gallery_path.write_text(gallery_head + cards + gallery_tail, encoding="utf-8")
print(f"Built gallery: {gallery_path}")

subprocess.run(["open", str(gallery_path)])
