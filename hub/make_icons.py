#!/usr/bin/env python3
"""產生佔位圖示（紅底、白色 2x2 方格）→ hub/icons/。不需要任何套件。
換成自己的圖：直接用同名 PNG 覆蓋 hub/icons/ 裡的檔案，再跑 python3 build_all.py。
  icon-192.png、icon-512.png（Android／電腦安裝用）、apple-touch-icon.png（iPhone 主畫面用，180x180）"""
import struct, zlib
from pathlib import Path

BG, FG = (192, 57, 43), (255, 255, 255)

def render(n, ss=3):
    def inside(x, y):  # 回傳是否落在白色圓角方格內
        for cx in (0.34, 0.66):
            for cy in (0.34, 0.66):
                half, r = 0.13, 0.04
                dx, dy = abs(x - cx) - (half - r), abs(y - cy) - (half - r)
                if max(dx, 0) ** 2 + max(dy, 0) ** 2 <= r * r and abs(x - cx) <= half and abs(y - cy) <= half:
                    return True
        return False
    rows = []
    for j in range(n):
        row = bytearray([0])
        for i in range(n):
            hit = sum(inside((i + (a + .5) / ss) / n, (j + (b + .5) / ss) / n) for a in range(ss) for b in range(ss)) / ss ** 2
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
