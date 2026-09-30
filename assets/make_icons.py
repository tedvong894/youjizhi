#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「游记志」全套图标：512/192/apple-touch/favicon + maskable。
母题：手账本 + 地点定位钉（区别于「旅游情报」的蓝山+琥珀太阳）。
配色：暖米白纸底 + 墨绿线条 + 陶土砖红定位钉（低饱和、不刺眼）。"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PAPER  = (246, 243, 236, 255)   # 暖米白纸底
INK    = (62, 107, 90, 255)     # 墨绿（主线条）
SAGE   = (168, 205, 187, 255)   # 浅鼠尾草（内页横线）
BRICK  = (198, 104, 90, 255)    # 陶土砖红（定位钉，低饱和）

S = 1024

def rounded_bg(size, fill, radius_ratio=0.195):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * radius_ratio), fill=fill)
    return img, d

def draw_pin(d, cx, cy, r, color, hole):
    """定位钉：圆头 + 下方尖角 + 中心镂空。"""
    d.polygon([(cx - r * 0.70, cy + r * 0.45), (cx + r * 0.70, cy + r * 0.45), (cx, cy + r * 2.0)], fill=color)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    hr = r * 0.42
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=hole)

def draw_mark(d, scale=1.0, ox=0, oy=0):
    """手账本 + 定位钉。scale/ox/oy 便于给 maskable 做安全缩放。"""
    def T(x, y):
        return (ox + x * scale, oy + y * scale)
    W = max(10, int(26 * scale))

    # 本子外框（纵向圆角矩形）
    x0, y0, x1, y1 = T(300, 320)[0], T(300, 320)[1], T(724, 824)[0], T(724, 824)[1]
    d.rounded_rectangle([x0, y0, x1, y1], radius=int(46 * scale), outline=INK, width=W)

    # 装订脊线
    sx = T(392, 0)[0]
    d.line([(sx, T(0, 344)[1]), (sx, T(0, 800)[1])], fill=INK, width=max(8, int(24 * scale)))

    # 内页横线（3 条，长短错落）
    lw = max(6, int(20 * scale))
    for (xa, xb, yy) in [(452, 664, 470), (452, 664, 548), (452, 604, 626)]:
        d.line([T(xa, yy), T(xb, yy)], fill=SAGE, width=lw)

    # 定位钉（钉在本子右上角外沿）
    cx, cy = T(688, 300)
    draw_pin(d, cx, cy, 74 * scale, BRICK, PAPER)

def build():
    # 圆角底标准图标
    img, d = rounded_bg(S, PAPER)
    draw_mark(d, 1.0)
    out = {"icon-512.png": 512, "icon-192.png": 192, "apple-touch-icon.png": 180, "favicon.png": 64}
    for name, size in out.items():
        img.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, name))
        print("+", name, size)

    # maskable：满铺底 + 内容缩进安全区
    m = Image.new("RGBA", (S, S), PAPER)
    md = ImageDraw.Draw(m)
    s = 0.74
    draw_mark(md, s, (S - S * s) / 2, (S - S * s) / 2)
    m.save(os.path.join(ROOT, "icon-maskable.png"))
    print("+ icon-maskable.png 1024")

if __name__ == "__main__":
    build()
