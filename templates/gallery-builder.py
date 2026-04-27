#!/usr/bin/env python3
"""Build a gallery HTML with multiple SVG cover variants for side-by-side comparison."""

import re
from pathlib import Path

base = Path.home() / "Desktop/好看的视觉海报/xhs-cover-demo"

# Pick 3 most distinct variants
variants = [
    (1, "v1-旅行箱无字.html", "旅行箱无字", "实物 icon · LV 风皮箱 · 物件路径"),
    (2, "v2-纯版式.html", "纯版式 · 破局", "大字关键词 · 极简留白"),
    (4, "v4-卡片堆叠.html", "卡片堆叠", "便签纸错落 · 工作台风"),
]


def extract_svg(content: str) -> str:
    m = re.search(r'<svg viewBox="0 0 1242 1660".*?</svg>', content, re.DOTALL)
    if not m:
        raise ValueError("SVG not found")
    return m.group(0)


svgs = {}
for v, fname, _, _ in variants:
    content = (base / fname).read_text(encoding="utf-8")
    svgs[v] = extract_svg(content)

# Build gallery HTML
head = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>小红书封面 · 3 版对比</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Architects+Daughter&display=swap');
  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0;
    background: #E8E2D5;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif;
  }
  body { padding: 40px 30px 80px; }
  header { max-width: 1400px; margin: 0 auto 40px; text-align: center; }
  header h1 { font-size: 28px; color: #2C2520; margin: 0 0 8px; font-weight: 600; }
  header p { color: #6B5D4F; font-size: 14px; margin: 0; }
  .grid {
    max-width: 1400px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 36px;
  }
  .card { display: flex; flex-direction: column; gap: 16px; }
  .stage {
    aspect-ratio: 3 / 4;
    background: #fff;
    box-shadow: 0 12px 36px rgba(44, 37, 32, 0.18);
    border-radius: 10px;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .stage:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(44, 37, 32, 0.28);
  }
  .stage svg { width: 100%; height: 100%; display: block; }
  .meta { text-align: center; }
  .meta h3 { margin: 0 0 4px; font-size: 18px; color: #2C2520; font-weight: 600; }
  .meta .desc { color: #6B5D4F; font-size: 13px; margin: 0 0 14px; }
  .btn-row { display: flex; gap: 10px; justify-content: center; }
  .btn {
    padding: 9px 18px;
    border: 1.5px solid #2C2520;
    background: #F5F0E6;
    color: #2C2520;
    font-size: 13px;
    font-weight: 600;
    border-radius: 999px;
    cursor: pointer;
    box-shadow: 0 1px 4px rgba(44, 37, 32, 0.08);
    transition: all 0.15s ease;
    font-family: inherit;
  }
  .btn:hover { transform: translateY(-1px); box-shadow: 0 3px 10px rgba(44, 37, 32, 0.16); }
  .btn[disabled] { opacity: 0.5; cursor: wait; }
  .btn.primary { background: #2C2520; color: #F5F0E6; }
  .toast {
    position: fixed; bottom: 30px; left: 50%;
    transform: translateX(-50%) translateY(20px);
    background: #2C2520; color: #F5F0E6;
    padding: 12px 22px; border-radius: 999px;
    font-size: 14px; opacity: 0; pointer-events: none;
    transition: opacity 0.25s ease, transform 0.25s ease;
    z-index: 200;
  }
  .toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
</style>
</head>
<body>
<header>
  <h1>小红书封面 · 3 版排版对比</h1>
  <p>主题：GPT 2.0 帮你做品牌 · 1242×1660 · 每张下方可独立下载 PNG</p>
</header>
<div class="grid">
"""

cards = []
for v, _, name, desc in variants:
    cards.append(f"""
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
  </div>""")

tail = """
</div>
<div class="toast" id="toast"></div>
<script>
const SVG_WIDTH = 1242;
const SVG_HEIGHT = 1660;
const FONT_CSS_URL = 'https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Architects+Daughter&display=swap';
let cachedFontsCSS = null;
const toast = document.getElementById('toast');

function showToast(msg, ms = 1800) {
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => toast.classList.remove('show'), ms);
}

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
  if (!defs) {
    defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    clone.insertBefore(defs, clone.firstChild);
  }
  const styleEl = document.createElementNS('http://www.w3.org/2000/svg', 'style');
  styleEl.textContent = inlinedCSS;
  defs.insertBefore(styleEl, defs.firstChild);
  const svgString = new XMLSerializer().serializeToString(clone);
  const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
  const url = URL.createObjectURL(svgBlob);
  try {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    await new Promise((resolve, reject) => {
      img.onload = resolve;
      img.onerror = () => reject(new Error('SVG image load failed'));
      img.src = url;
    });
    const canvas = document.createElement('canvas');
    canvas.width = SVG_WIDTH * scale;
    canvas.height = SVG_HEIGHT * scale;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#F5F0E6';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    return await new Promise((resolve) => canvas.toBlob(resolve, 'image/png', 1));
  } finally {
    URL.revokeObjectURL(url);
  }
}

const versionNames = { 1: '旅行箱无字', 2: '纯版式破局', 4: '卡片堆叠' };

async function downloadPng(version) {
  const card = document.querySelector(`[data-v="${version}"]`).parentElement;
  const btn = card.querySelector('.btn.primary');
  const svgEl = card.querySelector('svg');
  btn.disabled = true;
  btn.textContent = '生成中…';
  try {
    await document.fonts.ready;
    const blob = await svgToPngBlob(svgEl, 1);
    const a = document.createElement('a');
    a.download = `xhs-cover-v${version}-${versionNames[version]}.png`;
    a.href = URL.createObjectURL(blob);
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    showToast(`v${version} PNG 已下载`);
  } catch (e) {
    console.error(e);
    showToast('导出失败：' + e.message, 3000);
  } finally {
    btn.disabled = false;
    btn.textContent = '下载 PNG';
  }
}

async function copyPng(version) {
  const card = document.querySelector(`[data-v="${version}"]`).parentElement;
  const btn = card.querySelectorAll('.btn')[1];
  const svgEl = card.querySelector('svg');
  btn.disabled = true;
  btn.textContent = '复制中…';
  try {
    await document.fonts.ready;
    const blob = await svgToPngBlob(svgEl, 1);
    if (!navigator.clipboard || !window.ClipboardItem) throw new Error('当前浏览器不支持图片剪贴板');
    await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]);
    showToast(`v${version} 已复制`);
  } catch (e) {
    console.error(e);
    showToast(e.message, 3000);
  } finally {
    btn.disabled = false;
    btn.textContent = '复制';
  }
}
</script>
</body>
</html>
"""

output = head + "".join(cards) + tail
out_path = base / "gallery.html"
out_path.write_text(output, encoding="utf-8")
print(f"Built: {out_path}")
print(f"Size: {len(output):,} bytes")
