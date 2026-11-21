"""サンプル README（Tidepool、架空）用のヒーロー画像を自作レンダリングする。

左のログ行が多数の流れになって中央の「プール」に集まり、少数の太い流れとして右へ出ていく図。
使い方: uv run --with pillow python scripts/render-sample-hero.py [出力]
既定の出力: examples/sample-readme/images/hero.png（2400x1000）
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.getcwd()
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "examples", "sample-readme", "images", "hero.png")
W, H, S = 2400, 1000, 2  # S は縮小前の倍率（アンチエイリアス用）
random.seed(7)

MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BG = (7, 11, 16)
TEAL = (45, 212, 191)
CYAN = (56, 189, 248)
AMBER = (245, 158, 11)
CX, CY = W * 0.5, H * 0.56


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (
        u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
        u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],
    )


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def stream_pts(y0, y1, x0, x1, n=120):
    # 左の y0 から中央の y1 へ、S字に集まる
    p0, p3 = (x0, y0), (x1, y1)
    p1, p2 = (x0 + (x1 - x0) * 0.55, y0), (x0 + (x1 - x0) * 0.45, y1)
    return [bez(p0, p1, p2, p3, i / (n - 1)) for i in range(n)]


canvas = Image.new("RGBA", (W * S, H * S), BG + (255,))
sc = lambda pts: [(x * S, y * S) for x, y in pts]

# 1) 左側のログ行（読める程度に薄く）
log = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
d = ImageDraw.Draw(log)
f = ImageFont.truetype(MONO, 15 * S)
levels = [("INFO ", 0.62), ("INFO ", 0.62), ("INFO ", 0.62), ("DEBUG", 0.4), ("WARN ", 0.9), ("ERROR", 1.0)]
svc = ["ingest", "parse", "ship", "wal", "tail", "shard"]
rows = 60
for r in range(rows):
    y = 40 + r * (H - 80) / rows
    lv, a = random.choice(levels)
    s = (f"09:14:{random.randint(0, 59):02d}.{random.randint(0, 999):03d} {lv} "
         f"{random.choice(svc)}[{random.randint(1, 31)}] seq={random.randint(10**6, 9 * 10**6)} "
         f"len={random.choice([128, 256, 512, 1024, 4096])}")
    col = AMBER if lv == "ERROR" else (TEAL if lv != "DEBUG" else (120, 140, 150))
    # 右へ行くほど消える
    cut = random.randint(34, 56)
    for i, ch in enumerate(s[:cut]):
        k = max(0.0, 1 - i / cut) ** 1.4
        d.text((60 * S + i * 9.0 * S, y * S), ch, font=f, fill=col + (int(255 * a * k * 0.8),))
canvas = Image.alpha_composite(canvas, log)

# 2) 中央のさざ波（遠近つきの同心楕円）
rip = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
d = ImageDraw.Draw(rip)
for i in range(1, 15):
    rx = i * 70 + i * i * 4
    ry = rx * 0.19
    a = int(150 * (1 - i / 15) ** 1.3)
    d.ellipse([(CX - rx) * S, (CY + 60 - ry) * S, (CX + rx) * S, (CY + 60 + ry) * S],
              outline=TEAL + (a,), width=2 * S)
canvas = Image.alpha_composite(canvas, rip)

# 3) 集まる流れ（左→中央）と出ていく流れ（中央→右）
fl = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
d = ImageDraw.Draw(fl)
n_in = 54
for i in range(n_in):
    y0 = 40 + i * (H - 80) / (n_in - 1)
    y1 = CY + 60 + (i - n_in / 2) * 1.3
    pts = stream_pts(y0, y1, 380, CX)
    err = random.random() < 0.07
    base = AMBER if err else mix(TEAL, CYAN, random.random() * 0.6)
    for k in range(len(pts) - 1):
        t = k / len(pts)
        a = int(255 * (0.25 + 0.75 * t) * (0.75 if not err else 0.95))
        d.line(sc(pts[k:k + 2]), fill=base + (a,), width=int(1.6 * S))
    # 流れに乗るパケット
    for _ in range(random.randint(1, 3)):
        t = random.random() ** 0.7
        x, y = pts[int(t * (len(pts) - 1))]
        r = random.choice([2.4, 3.2, 4.0])
        d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=base + (255,))
n_out = 7
for i in range(n_out):
    y1 = 120 + i * (H - 240) / (n_out - 1)
    y0 = CY + 60 + (i - n_out / 2) * 6
    pts = stream_pts(y0, y1, CX, W - 150)
    for k in range(len(pts) - 1):
        t = k / len(pts)
        a = int(255 * (1 - t * 0.35))
        d.line(sc(pts[k:k + 2]), fill=mix(TEAL, CYAN, t) + (a,), width=int(4.5 * S))
    for j in range(4):
        x, y = pts[int((j + 0.5) / 4 * (len(pts) - 1))]
        r = 7
        d.rectangle([(x - r) * S, (y - r * 0.6) * S, (x + r) * S, (y + r * 0.6) * S], fill=(230, 245, 250, 255))
canvas = Image.alpha_composite(canvas, fl)

# 4) 右端のシンクの印（ラベルなしの小さな四角）
sk = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
d = ImageDraw.Draw(sk)
for i in range(n_out):
    y = 120 + i * (H - 240) / (n_out - 1)
    d.rounded_rectangle([(W - 150) * S, (y - 22) * S, (W - 70) * S, (y + 22) * S], 8 * S,
                        outline=CYAN + (170,), width=2 * S)
    d.line([(W - 135) * S, y * S, (W - 85) * S, y * S], fill=CYAN + (140,), width=2 * S)
canvas = Image.alpha_composite(canvas, sk)

# 5) 弱い光（流れの集まる所だけ）
glow = canvas.filter(ImageFilter.GaussianBlur(10 * S))
canvas = Image.blend(canvas, Image.alpha_composite(canvas, glow), 0.35)

img = canvas.resize((W, H), Image.LANCZOS).convert("RGB")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print(OUT, img.size)
