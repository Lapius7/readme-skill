"""examples/sample-readme/README.md を GitHub のダークテーマ風に描き、冒頭〜最初の Alert までを撮る。

外部サービスは使わない。バッジ（shields.io の badge/ URL）はローカルで flat-square の SVG にする。
使い方: uv run --with markdown-it-py --with playwright --with pillow python scripts/shoot-sample-readme.py [出力png]
既定の出力: examples/sample-readme/images/screenshot.png（幅 1200px の2倍）
環境変数 CHROME で Chromium の実行ファイルを指定できる（既定は Playwright の headless shell を探す）。
"""
import glob
import html
import os
import re
import sys
import urllib.parse

from markdown_it import MarkdownIt
from PIL import ImageFont
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(os.getcwd(), "examples", "sample-readme")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SAMPLE, "images", "screenshot.png")
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)

ICONS = {  # GitHub の octicons（16px）
    "note": "M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z",
    "important": "M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v9.5A1.75 1.75 0 0 1 14.25 13H8.06l-2.573 2.573A1.458 1.458 0 0 1 3 14.543V13H1.75A1.75 1.75 0 0 1 0 11.25Zm1.75-.25a.25.25 0 0 0-.25.25v9.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h6.5a.25.25 0 0 0 .25-.25v-9.5a.25.25 0 0 0-.25-.25Zm7 2.25v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 9a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z",
    "warning": "M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1.918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z",
}


def badge_svg(label, message, color):
    pad = 6
    lw = int(FONT.getlength(label)) + pad * 2
    mw = int(FONT.getlength(message)) + pad * 2
    w = lw + mw
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="20" role="img" aria-label="{html.escape(label)}: {html.escape(message)}">'
        f'<rect width="{lw}" height="20" fill="#555"/><rect x="{lw}" width="{mw}" height="20" fill="#{color}"/>'
        f'<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">'
        f'<text x="{lw / 2}" y="14">{html.escape(label)}</text><text x="{lw + mw / 2}" y="14">{html.escape(message)}</text></g></svg>'
    )


def local_badges(src):
    def sub(m):
        body = urllib.parse.unquote(m.group(1)).split("?")[0]
        parts = re.split(r"(?<!-)-(?!-)", body)
        label, message, color = [p.replace("--", "-").replace("_", " ") for p in parts]
        svg = badge_svg(label, message, color)
        return 'src="data:image/svg+xml;utf8,' + urllib.parse.quote(svg) + '"'
    return re.sub(r'src="https://img\.shields\.io/badge/([^"]+)"', sub, src)


def alerts(doc):
    def sub(m):
        kind = m.group(1).lower()
        title = kind.capitalize()
        return (f'<div class="markdown-alert markdown-alert-{kind}"><p class="markdown-alert-title">'
                f'<svg class="octicon" viewBox="0 0 16 16" width="16" height="16"><path d="{ICONS[kind]}"/></svg>{title}</p>'
                f'<p>{m.group(2)}</p></div>')
    return re.sub(r"<blockquote>\s*<p>\[!(NOTE|IMPORTANT|WARNING)\]\s*(.*?)</p>\s*</blockquote>", sub, doc, flags=re.S)


md = MarkdownIt("commonmark", {"html": True}).enable(["table", "strikethrough"])
text = open(os.path.join(SAMPLE, "README.md"), encoding="utf-8").read()
body = alerts(local_badges(md.render(text)))
body = body.replace('src="images/', 'src="file://' + SAMPLE + '/images/')
css = open(os.path.join(HERE, "vendor", "github-markdown-dark.css"), encoding="utf-8").read()
page = f"""<!doctype html><meta charset="utf-8"><style>{css}
body{{margin:0;background:#0d1117;padding:32px 0}}
.box{{width:1136px;margin:0 auto;border:1px solid #30363d;border-radius:6px;background:#0d1117}}
.head{{height:46px;border-bottom:1px solid #30363d;display:flex;align-items:center;padding:0 16px;color:#e6edf3;font:600 14px -apple-system,Segoe UI,Noto Sans,sans-serif}}
.markdown-body{{padding:32px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif}}
</style><div class="box"><div class="head">README</div><article class="markdown-body">{body}</article></div>"""
html_path = os.path.join(SAMPLE, "images", ".render.html")
open(html_path, "w", encoding="utf-8").write(page)

exe = os.environ.get("CHROME") or next(iter(sorted(glob.glob(os.path.expanduser(
    "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell")))[::-1]), None)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe)
    pg = b.new_page(viewport={"width": 1200, "height": 1000}, device_scale_factor=2)
    pg.goto("file://" + html_path)
    pg.wait_for_load_state("networkidle")
    box = pg.locator(".box").bounding_box()
    alert = pg.locator(".markdown-alert").first.bounding_box()
    clip = {"x": box["x"], "y": box["y"], "width": box["width"], "height": alert["y"] + alert["height"] + 12 - box["y"]}
    pg.screenshot(path=OUT, clip=clip)
    b.close()
os.remove(html_path)
print(OUT)
