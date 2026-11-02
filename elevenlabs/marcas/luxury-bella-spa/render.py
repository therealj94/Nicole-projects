#!/usr/bin/env python3
"""Luxury Bella Spa: motion graphics para video talking-head vertical.

Uso: render.py VIDEO TRANSCRIPT.json FONTS_DIR OUT_VIDEO_SIN_AUDIO.mp4
Estilo: negro + dorado + marfil, tipografías Cinzel / Cormorant Garamond / Great Vibes / Montserrat.
"""
import json, math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC, TRANS, FD, OUT = sys.argv[1:5]
W, H, FPS = 1080, 1920, 30
HOLD = 1.75                      # segundos extra para la tarjeta final
BRAND = "LUXURY BELLA SPA"
GOLD = [(246, 228, 180), (214, 180, 110), (176, 136, 64), (226, 196, 128)]
IVORY = (250, 246, 238)

# ---------- utilidades ----------
def font(name, size, wght=None):
    f = ImageFont.truetype(f"{FD}/{name}", size)
    if wght:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f

def ease(t):  # easeInOutCubic
    t = min(max(t, 0), 1)
    return 4*t*t*t if t < .5 else 1 - (-2*t + 2)**3 / 2

def eout(t):
    t = min(max(t, 0), 1)
    return 1 - (1 - t)**3

def ramp(t, a, b):
    return min(max((t - a) / (b - a), 0), 1) if b > a else float(t >= a)

def window(t, a, b, fi=.35, fo=.35):
    return eout(ramp(t, a, a + fi)) * (1 - ease(ramp(t, b - fo, b)))

def gold_fill(w, h):
    y = np.linspace(0, 1, h)[:, None]
    stops = np.array(GOLD, float)
    pos = np.array([0, .45, .75, 1.0])
    g = np.stack([np.interp(y[:, 0], pos, stops[:, c]) for c in range(3)], 1)
    arr = np.repeat(g[:, None, :], w, 1)
    return Image.fromarray(arr.astype(np.uint8), "RGB")

def text_mask(txt, f, tracking=0):
    if tracking == 0:
        b = f.getbbox(txt)
        m = Image.new("L", (b[2] - b[0] + 8, b[3] - b[1] + 8))
        ImageDraw.Draw(m).text((4 - b[0], 4 - b[1]), txt, font=f, fill=255)
        return m
    ws = [f.getlength(c) for c in txt]
    tw = int(sum(ws) + tracking * (len(txt) - 1)) + 8
    asc, desc = f.getmetrics()
    m = Image.new("L", (tw, asc + desc + 8))
    d = ImageDraw.Draw(m); x = 4
    for c, cw in zip(txt, ws):
        d.text((x, 4), c, font=f, fill=255); x += cw + tracking
    return m.crop(m.getbbox()) if m.getbbox() else m

def colorize(mask, color="gold", shadow=True, glow=False):
    """Devuelve RGBA con relleno (dorado o color) + sombra suave."""
    pad = 30
    w, h = mask.size[0] + 2*pad, mask.size[1] + 2*pad
    m = Image.new("L", (w, h)); m.paste(mask, (pad, pad))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if shadow:
        s = m.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .55))
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 255)); sh.putalpha(s)
        out = Image.alpha_composite(out, sh.transform((w, h), Image.AFFINE, (1, 0, 0, 0, 1, -4)))
    if glow:
        g = m.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * .5))
        gl = Image.new("RGBA", (w, h), (240, 205, 130, 255)); gl.putalpha(g)
        out = Image.alpha_composite(out, gl)
    fill = gold_fill(w, h).convert("RGBA") if color == "gold" else Image.new("RGBA", (w, h), color + (255,))
    fill.putalpha(m)
    return Image.alpha_composite(out, fill)

def with_alpha(img, a):
    if a >= .999: return img
    im = img.copy(); im.putalpha(img.getchannel("A").point(lambda v: int(v * a))); return im

def paste_c(canvas, img, cx, cy, a=1.0, scale=1.0):
    if a <= 0.003: return
    if abs(scale - 1) > 1e-3:
        img = img.resize((max(1, int(img.width*scale)), max(1, int(img.height*scale))), Image.LANCZOS)
    img = with_alpha(img, a)
    canvas.alpha_composite(img, (int(cx - img.width/2), int(cy - img.height/2)))

def glass_panel(w, h, r=36, border=True):
    p = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.rounded_rectangle((0, 0, w-1, h-1), r, fill=(14, 12, 10, 170))
    if border:
        gm = Image.new("L", (w, h)); ImageDraw.Draw(gm).rounded_rectangle((6, 6, w-7, h-7), r-6, outline=255, width=2)
        gf = gold_fill(w, h).convert("RGBA"); gf.putalpha(gm.point(lambda v: int(v*.9)))
        p = Image.alpha_composite(p, gf)
    return p

def star(size):
    m = Image.new("L", (size*4, size*4)); c = size*2; R, r = size*1.9, size*.8
    pts = [(c + (R if i % 2 == 0 else r) * math.sin(i*math.pi/5), c - (R if i % 2 == 0 else r) * math.cos(i*math.pi/5)) for i in range(10)]
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return colorize(m.resize((size, size), Image.LANCZOS), "gold", shadow=True, glow=True)

def diamond(s=18):
    m = Image.new("L", (s, s)); ImageDraw.Draw(m).polygon([(s/2, 0), (s, s/2), (s/2, s), (0, s/2)], fill=255)
    return m

def gold_line(length, thick=2):
    m = Image.new("L", (length, thick+2)); ImageDraw.Draw(m).rectangle((0, 1, length, thick), fill=255)
    # desvanecido en los extremos
    a = np.array(m, float); x = np.linspace(0, 1, length)
    a *= np.clip(np.minimum(x, 1-x) * 6, 0, 1)[None, :]
    return colorize(Image.fromarray(a.astype(np.uint8)), "gold", shadow=False)

# ---------- assets ----------
f_cinzel = lambda s, w=600: font("Cinzel[wght].ttf", s, w)
f_corm = lambda s, w=600: font("CormorantGaramond[wght].ttf", s, w)
f_cormi = lambda s, w=600: font("CormorantGaramond-Italic[wght].ttf", s, w)
f_script = lambda s: font("GreatVibes-Regular.ttf", s)
f_mont = lambda s, w=500: font("Montserrat[wght].ttf", s, w)

brand_big = colorize(text_mask(BRAND, f_cinzel(78, 600), tracking=10), "gold", glow=True)
brand_small_mask = text_mask(BRAND, f_cinzel(34, 600), tracking=9)
brand_small = colorize(brand_small_mask, "gold")
line_long, line_short = gold_line(520), gold_line(150)
dia = colorize(diamond(16), "gold", shadow=False)
sub_intro = colorize(text_mask("spa · belleza · bienestar", f_cormi(46, 500)), IVORY)

STAR = star(78); STAR_S = star(46)
words = [w for w in json.load(open(TRANS))["words"] if w["type"] == "word"]

# ---------- configuración del video (textos, tiempos, momentos) ----------
import os
CFG = os.environ.get("CFG") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "v01_gracias.py")
INTRO_BIG, ANCHOR, CAP_Y, HEADER_SHINE, LEAK = True, (0.5, 0.5), 0.37, [], []
BROLL, INSETS, INSET_S, INSET_DX, REVEAL_C = [], [], 0.80, 150, (0.5, 0.68)
PRE_FX, BG_FX = None, None   # efectos sobre la persona / fondo generado
exec(open(CFG).read())
for w in words: w["text"] = FIX.get(w["text"], w["text"])
chunks = [[dict(w, key=w["text"].lower() in KEY_ES) for w in words[r[-2]:r[-1] + 1]] for r in SUBS]
F_CAP, F_CAPI = f_corm(84, 600), f_cormi(88, 600)
CAP_ASC = max(F_CAP.getmetrics()[0], F_CAPI.getmetrics()[0]); CAP_H = CAP_ASC + max(F_CAP.getmetrics()[1], F_CAPI.getmetrics()[1]) + 8
def cap_mask(txt, f):
    b = f.getbbox(txt)
    m = Image.new("L", (b[2] - b[0] + 8, CAP_H))
    ImageDraw.Draw(m).text((4 - b[0], 4 + CAP_ASC - f.getmetrics()[0]), txt, font=f, fill=255)
    return m
cap = []
for k, ch in enumerate(chunks):
    imgs = []
    for w in ch:
        key = w["key"]
        im = colorize(cap_mask(w["text"], F_CAPI if key else F_CAP), "gold" if key else IVORY)
        imgs.append((w["start"], im))
    a = ch[0]["start"] - .08
    nxt = chunks[k+1][0]["start"] - .08 if k + 1 < len(chunks) else 99
    b = min(nxt, ch[-1]["end"] + .55)
    cap.append((a, b, imgs))
SPEECH_END = words[-1]["end"]

def draw_captions(cv, t):
    for a, b, imgs in cap:
        if not (a <= t < b): continue
        fade = 1 - ease(ramp(t, b - .14, b)) if b < 98 else 1
        gap = -68 + 20
        total = sum(im.width for _, im in imgs) + gap * (len(imgs) - 1)
        sc = min(1.0, 940 / total)                     # frases largas: se reducen para no salirse
        x = W/2 - total*sc/2; y = int(H*CAP_Y)
        for st, im in imgs:
            p = eout(ramp(t, st - .06, st + .22))
            if p > 0:
                paste_c(cv, im, x + im.width*sc/2, y + (1-p)*18, p*fade, sc)
            x += (im.width + gap) * sc

# ---------- capa de luz (light leak) ----------
yy, xx = np.mgrid[0:H//4, 0:W//4]
def light_leak(t, strength):
    if strength <= 0: return None
    cx = W//4 * (0.15 + 0.7 * (0.5 + 0.5*math.sin(t*.6))); cy = H//4 * (0.1 + 0.15*math.cos(t*.4))
    d = np.sqrt((xx-cx)**2 + (yy-cy)**2) / (W//4)
    a = np.clip(1 - d/0.9, 0, 1)**2 * strength
    rgb = np.zeros((H//4, W//4, 3)); rgb[..., 0], rgb[..., 1], rgb[..., 2] = 255, 196, 120
    im = Image.fromarray(np.dstack([rgb, a*255]).astype(np.uint8), "RGBA").resize((W, H), Image.BILINEAR)
    return im

# ---------- zoom por bloques ----------
def zoom_at(t):
    for (t0, z0), (t1, z1) in zip(ZK, ZK[1:]):
        if t0 <= t < t1:
            dur = t1 - t0
            return z0 + (z1 - z0) * (ease((t - t0) / dur) if dur < .6 else (t - t0) / dur)
    return ZK[-1][1]

# ---------- partículas doradas ----------
rng = np.random.default_rng(7)
PART = [(rng.uniform(80, W-80), rng.uniform(H*0.35, H*1.05), rng.uniform(4, 11), rng.uniform(40, 110), rng.uniform(0, 6.28)) for _ in range(46)]
def bokeh(r):
    m = Image.new("L", (int(r*6), int(r*6))); ImageDraw.Draw(m).ellipse((r*2, r*2, r*4, r*4), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(r*.7))
    im = Image.new("RGBA", m.size, (250, 218, 150, 255)); im.putalpha(m); return im
BOK = {int(r): bokeh(int(r)) for r in range(4, 12)}

def draw_particles(cv, t, a0, a1):
    s = window(t, a0, a1, .6, .8)
    if s <= 0: return
    for (x, y, r, sp, ph) in PART:
        yy_ = y - (t - a0) * sp
        xx_ = x + 18 * math.sin(t*1.3 + ph)
        tw = 0.55 + 0.45 * math.sin(t*3 + ph)
        paste_c(cv, BOK[int(r)], xx_, yy_, s * tw * .8)


# ---------- tomas de apoyo (B-roll) con la persona recortada al frente ----------
GRADE_BR = ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,"
            "eq=contrast=1.04:brightness=0.05:gamma=1.10:saturation=1.08,"
            "colorbalance=rs=0.015:gs=0.005:bs=-0.02:rh=0.025:gh=0.01:bh=-0.03,unsharp=5:5:0.4")
XF = 0.4   # duración de transiciones

class BRollReader:
    def __init__(self, path, src, t0, t1):
        self.path, self.src, self.t0, self.t1 = path, src, t0 - XF, t1 + XF
        self.p, self.idx, self.frame = None, -1, None
    def get(self, t):
        if not (self.t0 <= t <= self.t1): return None
        if self.p is None:
            self.p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", str(self.src), "-i", self.path, "-an",
                                       "-vf", GRADE_BR, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        want = int(round((t - self.t0) * FPS))
        while self.idx < want:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3: break
            self.frame = Image.frombytes("RGB", (W, H), buf); self.idx += 1
        if self.frame is None: return None
        z = 1.04 + 0.06 * ramp(t, self.t0, self.t1)          # empuje lento
        cw, ch = W / z, H / z
        return self.frame.resize((W, H), Image.BICUBIC, box=((W-cw)/2, (H-ch)/2, (W+cw)/2, (H+ch)/2))

_seg, _mprev = None, None
def person_mask(img):
    global _seg, _mprev
    if _seg is None:
        import mediapipe as mp
        from mediapipe.tasks.python import vision, BaseOptions
        _seg = (mp, vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
            base_options=BaseOptions(model_asset_path=os.environ.get("SEG_MODEL", "/tmp/x/selfie_multiclass.tflite")),
            output_confidence_masks=True)))
    mp, sg = _seg
    small = np.ascontiguousarray(np.array(img.resize((540, 960), Image.BILINEAR)))
    bg = sg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=small)).confidence_masks[0].numpy_view()
    m = np.clip(((1 - bg.reshape(960, 540)) - .3) / .4, 0, 1)
    if _mprev is not None: m = .65 * m + .35 * _mprev
    _mprev = m
    return Image.fromarray((m * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(2))

def inset_amount(t):
    return max([window(t, a, b, .5, .5) for a, b in INSETS] + [0])

ryy, rxx = np.mgrid[0:H//4, 0:W//4]
RD = np.sqrt((rxx - W//4 * REVEAL_C[0])**2 + (ryy - H//4 * REVEAL_C[1])**2) / (H//4)
def reveal_mask(p):
    a = np.clip((p * 1.25 - RD) / .12, 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)

READERS = [BRollReader(*b) for b in BROLL]
def broll_layer(t):
    if BG_FX: return BG_FX(t)
    out = None
    for r in READERS:
        f = r.get(t)
        if f is None: continue
        a = ease(ramp(t, r.t0, r.t0 + XF))       # fundido de entrada (sobre la toma anterior)
        out = f if out is None or a >= 1 else Image.blend(out, f, a)
    return out

def apply_broll(base, t):
    k = inset_amount(t)
    if k <= 0: return base
    bl = broll_layer(t)
    if bl is None: return base
    mask = person_mask(base)
    bg = Image.composite(bl, base, reveal_mask(k))
    s = 1 - (1 - INSET_S) * ease(k); dx = INSET_DX * ease(k)
    nw, nh = int(W * s), int(H * s)
    spk = base.resize((nw, nh), Image.BICUBIC); mk = mask.resize((nw, nh), Image.BILINEAR)
    ox, oy = int((W - nw) / 2 + dx), H - nh
    sh = Image.new("L", (W, H)); sh.paste(mk.point(lambda v: int(v * .55 * k)), (ox - 18, oy + 10))
    bg = Image.composite(Image.new("RGB", (W, H), (10, 8, 6)), bg, sh.filter(ImageFilter.GaussianBlur(26)))
    bg.paste(spk, (ox, oy), mk)
    return bg

# ---------- composición por cuadro ----------
def shine(img, p):
    """Barrido de brillo diagonal sobre un RGBA (p de 0 a 1)."""
    if p <= 0 or p >= 1: return img
    w, h = img.size
    x = np.arange(w)[None, :] + np.arange(h)[:, None] * .5
    c = -h + p * (w + 2*h)
    band = np.clip(1 - np.abs(x - c) / 60, 0, 1)
    a = np.array(img.getchannel("A"), float) / 255 * band * .9
    hl = Image.fromarray(np.dstack([np.full((h, w, 3), 255), a*255]).astype(np.uint8), "RGBA")
    return Image.alpha_composite(img, hl)

grad_bot = Image.fromarray(np.dstack([np.zeros((H, W, 3)), (np.exp(-((np.linspace(0, 1, H) - CAP_Y) / .055)**2) * 120)[:, None].repeat(W, 1)]).astype(np.uint8), "RGBA")
grad_top = Image.fromarray(np.dstack([np.zeros((H, W, 3)), (np.clip((.16 - np.linspace(0, 1, H)) / .16, 0, 1)**1.5 * 85)[:, None].repeat(W, 1)]).astype(np.uint8), "RGBA")
frame_m = Image.new("L", (W, H)); ImageDraw.Draw(frame_m).rounded_rectangle((34, 34, W-35, H-35), 28, outline=255, width=2)
frame_gold = gold_fill(W, H).convert("RGBA"); frame_gold.putalpha(frame_m)

def frame_reveal(p):
    """Marco dorado que se dibuja desde el centro superior e inferior."""
    if p >= 1: return frame_gold
    m = np.zeros((H, W)); half = p
    xs = np.abs(np.arange(W) - W/2) / (W/2); ys = np.arange(H) / H
    # progreso a lo largo del perímetro aproximado: horizontal primero, luego vertical
    hx = (xs <= min(half*2, 1))[None, :].repeat(H, 0)
    vy = np.abs(ys - .5)[:, None].repeat(W, 1) >= (.5 - max(half*2 - 1, 0) * .5)
    m = np.where((hx & (np.abs(ys - .5)[:, None] > .45)) | vy, 1, 0)
    fg = frame_gold.copy(); fg.putalpha(Image.fromarray((np.array(frame_m) * m).astype(np.uint8)))
    return fg

def compose(base, t, last_frame):
    END0 = SPEECH_END + .1
    # zoom
    z = zoom_at(t)
    if z > 1.001:
        cw, ch = W / z, H / z
        x0 = (W - cw) * ANCHOR[0]; y0 = (H - ch) * ANCHOR[1]
        base = base.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))
    if PRE_FX: base = PRE_FX(base, t)
    if INSETS: base = apply_broll(base, t)
    cv = base.convert("RGBA")

    # tarjeta final: desenfoque + oscurecido
    e = ease(ramp(t, END0, END0 + .7))
    if e > 0:
        bl = cv.filter(ImageFilter.GaussianBlur(22 * e))
        cv = Image.alpha_composite(bl, Image.new("RGBA", (W, H), (10, 8, 6, int(150 * e))))

    # intro oscurecida
    di = (1 - ease(ramp(t, 1.0, 1.8))) if INTRO_BIG else 0
    if di > 0: cv = Image.alpha_composite(cv, Image.new("RGBA", (W, H), (8, 6, 4, int(140 * di))))

    # degradados de lectura
    cv = Image.alpha_composite(cv, with_alpha(grad_bot, (1 - e) * eout(ramp(t, 1.0, 1.6))))
    cv = Image.alpha_composite(cv, with_alpha(grad_top, (1 - e) * eout(ramp(t, 1.2, 1.9))))

    # luz cálida
    lk = light_leak(t, .32 * (1 - ramp(t, 0, 2.2)) + .30 * ramp(t, END0, END0 + 1) + sum(.10 * window(t, x0, x1, .5, .6) for x0, x1 in LEAK))
    if lk is not None: cv = Image.alpha_composite(cv, lk)

    # marco dorado
    fr = eout(ramp(t, .15, 1.4))
    cv = Image.alpha_composite(cv, with_alpha(frame_reveal(fr), .75))

    # INTRO: marca grande al centro -> sube y se reduce a la cabecera
    if INTRO_BIG and t < 2.2:
        a = eout(ramp(t, .1, .7)) * (1 - ease(ramp(t, 1.15, 1.6)))
        sc = 1.06 - .06 * eout(ramp(t, .1, 1.2))
        paste_c(cv, shine(brand_big, ramp(t, .5, 1.3)), W/2, H*0.53, a, sc)
        lw = eout(ramp(t, .25, 1.0))
        paste_c(cv, line_long.resize((max(1, int(520*lw)), line_long.height)), W/2, H*0.53 - 80, a)
        paste_c(cv, line_long.resize((max(1, int(520*lw)), line_long.height)), W/2, H*0.53 + 70, a)
        paste_c(cv, sub_intro, W/2, H*0.53 + 135, a * eout(ramp(t, .45, .95)))
    # cabecera persistente
    hd = (eout(ramp(t, 1.35, 1.95)) if INTRO_BIG else eout(ramp(t, .15, .75))) * (1 - e)
    if hd > 0:
        yh = H*0.075 + (1 - hd) * 30
        p = next(((t - s0) / 1.1 for s0 in HEADER_SHINE if s0 <= t <= s0 + 1.1), -1)
        paste_c(cv, shine(brand_small, p), W/2, yh, hd)
        paste_c(cv, line_short, W/2 - brand_small.width/2 - 60, yh, hd * .9)
        paste_c(cv, line_short, W/2 + brand_small.width/2 + 60, yh, hd * .9)

    moments(cv, t, END0)

    # subtítulos
    if e < .5: draw_captions(cv, t)

    # TARJETA FINAL
    if e > 0:
        y0 = H*0.42
        a1 = eout(ramp(t, END0 + .2, END0 + .8))
        paste_c(cv, shine(brand_big, ramp(t, END0 + .7, END0 + 1.5)), W/2, y0, a1, .92 + .08 * a1)
        lw = eout(ramp(t, END0 + .35, END0 + 1.0))
        ll = line_long.resize((max(1, int(520*lw)), line_long.height))
        paste_c(cv, ll, W/2, y0 - 80, a1); paste_c(cv, ll, W/2, y0 + 70, a1)
        paste_c(cv, dia, W/2, y0 - 80, a1)
        a2 = eout(ramp(t, END0 + .6, END0 + 1.2))
        for k, im in enumerate(END_LINES):
            paste_c(cv, im, W/2, y0 + 165 + 75*k + (1-a2)*20, a2)
        yc = y0 + 165 + 75*len(END_LINES) + 45
        if END_STARS:
            for k in range(5):
                st = END0 + 1.0 + k * .1; p = eout(ramp(t, st, st + .25))
                paste_c(cv, STAR_S, W/2 + (k - 2) * 62, yc, a2 * p, max(.01, p))
            yc += 70
        paste_c(cv, END_CTA, W/2, yc, eout(ramp(t, END0 + 1.4, END0 + 1.9)))

    # fundido a negro final
    total = DUR
    fo = ease(ramp(t, total - .45, total))
    if fo > 0: cv = Image.alpha_composite(cv, Image.new("RGBA", (W, H), (0, 0, 0, int(255 * fo))))
    return cv.convert("RGB")

# ---------- pipeline ffmpeg ----------
src_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC]))
DUR = src_dur + HOLD
grade = ("fps=30,scale=1080:1920:flags=lanczos,eq=contrast=1.04:brightness=0.045:gamma=1.10:saturation=1.06,"
         "colorbalance=rs=0.015:gs=0.005:bs=-0.02:rh=0.025:gh=0.01:bh=-0.03,unsharp=5:5:0.4,"
         f"vignette=PI/9,tpad=stop_mode=clone:stop_duration={HOLD}")
dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", SRC, "-vf", grade, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", OUT],
                       stdin=subprocess.PIPE)
n, fs = 0, W * H * 3
only = float(sys.argv[5]) if len(sys.argv) > 5 else None   # modo vista previa: un solo instante
while True:
    buf = dec.stdout.read(fs)
    if len(buf) < fs: break
    t = n / FPS
    if only is not None and abs(t - only) > 1/(2*FPS):
        n += 1; continue
    img = Image.frombytes("RGB", (W, H), buf)
    out = compose(img, t, None)
    if only is not None:
        out.save(OUT.replace(".mp4", f"_{only:.1f}.png")); break
    enc.stdin.write(out.tobytes())
    n += 1
    if n % 90 == 0: print(f"{t:.1f}s", file=sys.stderr, flush=True)
dec.terminate(); enc.stdin.close(); enc.wait()
