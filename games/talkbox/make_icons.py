# Generate PWA icons (popcorn box). Run: python3 make_icons.py
from PIL import Image, ImageDraw
import math

NAVY=(27,35,64); RED=(216,55,47); WHITE=(255,255,255)
BUTTER=(255,212,92); BUTTER_D=(232,176,48); BUTTER_L=(255,241,184)
SS=1024  # supersample canvas

def art(draw_img, s, cx=512, cy=512):
    A = SS*s
    ox, oy = cx-A/2, cy-A/2
    P = lambda x,y: (ox + x/100*A, oy + y/100*A)
    d = ImageDraw.Draw(draw_img)
    # popcorn puffs (behind the box)
    puffs = [(26,42,11),(40,30,12),(56,26,13),(72,34,12),(80,46,10),(48,40,12),(34,48,10),(64,42,11)]
    for (x,y,r) in puffs:
        # lumpy puff = 4 overlapping circles
        for dx,dy,k in [(-.5,.2,.7),(.5,.2,.7),(0,-.55,.75),(0,.25,.85)]:
            cxp,cyp = P(x+dx*r, y+dy*r); rr = r*k/100*A
            d.ellipse([cxp-rr,cyp-rr,cxp+rr,cyp+rr], fill=BUTTER, outline=BUTTER_D, width=max(2,int(A*0.008)))
        hx,hy = P(x-r*.25, y-r*.2); hr = r*.22/100*A
        d.ellipse([hx-hr,hy-hr,hx+hr,hy+hr], fill=BUTTER_L)
    # striped box (trapezoid mask)
    layer = Image.new('RGBA',(SS,SS),(0,0,0,0))
    ld = ImageDraw.Draw(layer)
    stripes = 8; x0,x1 = 8,92; w=(x1-x0)/stripes
    for i in range(stripes):
        col = RED if i%2==0 else WHITE
        ld.rectangle([*P(x0+i*w,40), *P(x0+(i+1)*w,100)], fill=col)
    mask = Image.new('L',(SS,SS),0)
    md = ImageDraw.Draw(mask)
    md.polygon([P(8,46),P(92,46),P(80,96),P(20,96)], fill=255)
    # rim
    layer.putalpha(mask)
    draw_img.alpha_composite(layer)
    d = ImageDraw.Draw(draw_img)
    d.polygon([P(8,46),P(92,46),P(80,96),P(20,96)], outline=NAVY if False else (255,255,255), width=max(3,int(A*0.012)))
    d.rounded_rectangle([*P(5,42), *P(95,50)], radius=A*0.02, fill=WHITE)
    d.rounded_rectangle([*P(5,42), *P(95,50)], radius=A*0.02, outline=RED, width=max(3,int(A*0.012)))

def make(size, scale, rounded, path):
    img = Image.new('RGBA',(SS,SS),(0,0,0,0))
    bg = Image.new('RGBA',(SS,SS),NAVY+(255,))
    if rounded:
        m = Image.new('L',(SS,SS),0)
        ImageDraw.Draw(m).rounded_rectangle([0,0,SS-1,SS-1], radius=int(SS*0.22), fill=255)
        img.paste(bg,(0,0),m)
    else:
        img = bg
    art(img, scale)
    out = img.resize((size,size), Image.LANCZOS)
    if not rounded: out = out.convert('RGB')
    out.save(path, optimize=True)

make(512, 0.74, True,  'icons/icon-512.png')
make(192, 0.74, True,  'icons/icon-192.png')
make(512, 0.58, False, 'icons/icon-maskable-512.png')   # art inside the 80% safe zone
make(180, 0.62, False, 'icons/apple-touch-icon.png')    # iOS applies its own mask
print('ok')
