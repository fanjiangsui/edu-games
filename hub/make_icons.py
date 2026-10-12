#!/usr/bin/env python3
"""產生圖示（紅底白色遊戲手把，對應首頁的 🎮）→ hub/icons/。不需要任何套件。
換成自己的圖：直接用同名 PNG 覆蓋 hub/icons/ 裡的檔案，再跑 python3 build_all.py。
  icon-192.png、icon-512.png（Android／電腦安裝用）、apple-touch-icon.png（iPhone 主畫面用，180x180）"""
import struct, zlib
from pathlib import Path

BG, FG = (192, 57, 43), (255, 255, 255)

def render(n, ss=3):
    def circ(x, y, cx, cy, r): return (x - cx) ** 2 + (y - cy) ** 2 <= r * r
    def box(x, y, cx, cy, hw, hh): return abs(x - cx) <= hw and abs(y - cy) <= hh
    def body(x, y):  # 遊戲手把：橫向膠囊 + 兩個握把
        cap = box(x, y, 0.5, 0.49, 0.22, 0.15) or circ(x, y, 0.28, 0.49, 0.15) or circ(x, y, 0.72, 0.49, 0.15)
        return cap or circ(x, y, 0.29, 0.60, 0.115) or circ(x, y, 0.71, 0.60, 0.115)
    def hole(x, y):  # 十字鍵與兩顆按鈕（鏤空成底色）
        return (box(x, y, 0.33, 0.49, 0.065, 0.02) or box(x, y, 0.33, 0.49, 0.02, 0.065)
                or circ(x, y, 0.63, 0.53, 0.032) or circ(x, y, 0.70, 0.45, 0.032))
    rows = []
    for j in range(n):
        row = bytearray([0])
        for i in range(n):
            hit = 0
            for a in range(ss):
                for b in range(ss):
                    x, y = (i + (a + .5) / ss) / n, (j + (b + .5) / ss) / n
                    hit += body(x, y) and not hole(x, y)
            hit /= ss ** 2
            row += bytes(round(BG[k] + (FG[k] - BG[k]) * hit) for k in range(3))
        rows.append(bytes(row))
    return b"".join(rows)

def png(n):
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(render(n), 9)) + chunk(b"IEND", b""))

out = Path(__file__).parent / "icons"; out.mkdir(exist_ok=True)
for name, n in (("icon-192.png", 192), ("icon-512.png", 512), ("apple-touch-icon.png", 180)):
    (out / name).write_bytes(png(n)); print("寫入", out / name)
