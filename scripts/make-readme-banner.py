"""readme-creator 自身の README 用バナー docs/images/banner.png を作る。

examples/sample-readme の撮影画像（screenshot.png）を、角丸の枠に入れて暗い背景に置く。文字は足さない。
背景はサンプルのヒーロー画像（hero.png）を暗くぼかしたもの。
使い方: uv run --with pillow python scripts/make-readme-banner.py
出力: docs/images/banner.png（2400x1100）
"""
import os

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

ROOT = os.getcwd()
SAMPLE = os.path.join(ROOT, "examples", "sample-readme", "images")
OUT = os.path.join(ROOT, "docs", "images", "banner.png")
W, H, R, SHOT_W = 2400, 1100, 28, 1560

bg = Image.open(os.path.join(SAMPLE, "hero.png")).convert("RGB")
k = max(W / bg.width, H / bg.height)  # 画面を覆う倍率
bg = bg.resize((round(bg.width * k), round(bg.height * k)), Image.LANCZOS)
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
bg = bg.filter(ImageFilter.GaussianBlur(8))
bg = ImageEnhance.Brightness(bg).enhance(0.55).convert("RGBA")

shot = Image.open(os.path.join(SAMPLE, "screenshot.png")).convert("RGB")
shot = shot.resize((SHOT_W, round(shot.height * SHOT_W / shot.width)), Image.LANCZOS)
sw, sh = shot.size
x, y = (W - sw) // 2, (H - sh) // 2
SS = 4
mask = Image.new("L", (sw * SS, sh * SS), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw * SS - 1, sh * SS - 1], R * SS, fill=255)
mask = mask.resize((sw, sh), Image.LANCZOS)

# 影
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shadow.paste((0, 0, 0, 200), (x, y + 24), mask)
bg = Image.alpha_composite(bg, shadow.filter(ImageFilter.GaussianBlur(36)))

# 枠線（1px、枠より少し大きい角丸を下に敷く）
ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rm = Image.new("L", (sw + 2, sh + 2), 0)
ImageDraw.Draw(rm).rounded_rectangle([0, 0, sw + 1, sh + 1], R + 1, fill=255)
ring.paste((72, 82, 94, 255), (x - 1, y - 1), rm)
bg = Image.alpha_composite(bg, ring)
bg.paste(shot, (x, y), mask)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
bg.convert("RGB").save(OUT, optimize=True)
print(OUT, bg.size)
