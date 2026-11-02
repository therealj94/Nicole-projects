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

gracias = colorize(text_mask("Gracias", f_script(230)), "gold", glow=True)
gracias_panel = glass_panel(760, 330)

STAR = star(78); STAR_S = star(46)
cta_panel = glass_panel(860, 330)
cta_t1 = colorize(text_mask("TU OPINIÓN NOS IMPORTA", f_mont(30, 600), tracking=6), IVORY)
cta_t2 = colorize(text_mask("Déjanos tu reseña en Google", f_cormi(58, 600)), "gold")

end_t1 = colorize(text_mask("Gracias por ser parte", f_cormi(66, 500)), IVORY)
end_t2 = colorize(text_mask("de nuestra historia", f_cormi(66, 500)), IVORY)
end_t3 = colorize(text_mask("CALIFÍCANOS EN GOOGLE", f_mont(28, 600), tracking=6), "gold")
comm_t = colorize(text_mask("comunidad", f_script(150)), "gold", glow=True)

# ---------- subtítulos ----------
words = [w for w in json.load(open(TRANS))["words"] if w["type"] == "word"]
FIX = {"Luxor": "Luxury"}
for w in words: w["text"] = FIX.get(w["text"], w["text"])
CHUNKS = [3, 4, 4, 4, 3, 2, 4, 3, 3, 4, 3, 3, 2, 4, 3, 4, 3, 3, 2]  # palabras por bloque
KEY = {"feliz", "reserva", "luxury", "bella", "spa", "visita", "recomendación", "elegirnos", "cuidado", "belleza",
       "comunidad", "ti", "experiencia", "opinión", "google", "vuelves"}
# Subtítulos en inglés: (texto, índice primera palabra ES, índice última palabra ES) para el tiempo
EN = [("A happy client", 0, 2), ("is so much more than", 3, 6), ("a booking to us.", 7, 10),
      ("At Luxury Bella Spa", 11, 14), ("we value every visit,", 15, 17), ("every referral", 18, 19),
      ("and every time", 20, 23), ("you choose us again.", 24, 26), ("Thank you for letting us", 27, 29),
      ("be part of your", 30, 33), ("moments of self-care", 34, 36), ("and beauty.", 37, 38),
      ("Our community", 39, 40), ("grows thanks to you.", 41, 44), ("If you've had", 45, 47),
      ("an experience with us,", 48, 51), ("we'd love for you", 52, 54), ("to share your review", 55, 57),
      ("on Google", 58, 59)]
KEY = {"happy", "booking", "luxury", "bella", "spa", "visit", "referral", "choose", "self-care", "beauty",
       "community", "experience", "review", "google"}
LANG = "es"   # "es" = palabras reales con su tiempo exacto; "en" = traducción EN
KEY_ES = {"feliz", "reserva", "luxury", "bella", "spa", "visita,", "recomendación", "elegirnos.", "cuidado",
          "belleza.", "comunidad", "ti.", "experiencia", "opinión", "google"}
chunks = []
for txt, i0, i1 in EN:
    if LANG == "es":
        chunks.append([dict(w, key=w["text"].lower() in KEY_ES) for w in words[i0:i1 + 1]])
        continue
    t0, t1 = words[i0]["start"], max(words[i1]["start"], words[i1]["end"] - .25)
    ws = txt.split()
    chunks.append([{"text": w, "start": t0 + (t1 - t0) * k / max(len(ws) - 1, 1), "end": words[i1]["end"]}
                   for k, w in enumerate(ws)])
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
        key = w.get("key", w["text"].strip(".,").lower() in KEY)
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
        x = W/2 - total/2; y = int(H*CAP_Y)
        for st, im in imgs:
            p = eout(ramp(t, st - .06, st + .22))
            if p > 0:
                paste_c(cv, im, x + im.width/2, y + (1-p)*18, p*fade)
            x += im.width + gap

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
ZK = [(0, 1.00), (1.25, 1.03), (5.75, 1.06), (6.15, 1.13), (12.9, 1.15), (13.3, 1.04), (18.5, 1.07), (18.9, 1.14),
      (21.7, 1.16), (22.1, 1.05), (28.9, 1.09), (99, 1.09)]
def zoom_at(t):
    for (t0, z0), (t1, z1) in zip(ZK, ZK[1:]):
        if t0 <= t < t1:
            dur = t1 - t0
            return z0 + (z1 - z0) * (ease((t - t0) / dur) if dur < .6 else (t - t0) / dur)
    return ZK[-1][1]
ANCHOR = (0.5, 0.50)

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

CAP_Y = 0.37   # subtítulos sobre la cabeza (entre la cabecera/paneles y el pelo), fuera del pie de Instagram
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
    cv = base.convert("RGBA")

    # tarjeta final: desenfoque + oscurecido
    e = ease(ramp(t, END0, END0 + .7))
    if e > 0:
        bl = cv.filter(ImageFilter.GaussianBlur(22 * e))
        cv = Image.alpha_composite(bl, Image.new("RGBA", (W, H), (10, 8, 6, int(150 * e))))

    # intro oscurecida
    di = 1 - ease(ramp(t, 1.0, 1.8))
    if di > 0: cv = Image.alpha_composite(cv, Image.new("RGBA", (W, H), (8, 6, 4, int(140 * di))))

    # degradados de lectura
    cv = Image.alpha_composite(cv, with_alpha(grad_bot, (1 - e) * eout(ramp(t, 1.0, 1.6))))
    cv = Image.alpha_composite(cv, with_alpha(grad_top, (1 - e) * eout(ramp(t, 1.2, 1.9))))

    # luz cálida
    lk = light_leak(t, .32 * (1 - ramp(t, 0, 2.2)) + .30 * ramp(t, END0, END0 + 1) + .10 * window(t, 13.1, 18.4, .5, .6))
    if lk is not None: cv = Image.alpha_composite(cv, lk)

    # marco dorado
    fr = eout(ramp(t, .15, 1.4))
    cv = Image.alpha_composite(cv, with_alpha(frame_reveal(fr), .75))

    # INTRO: marca grande al centro -> sube y se reduce a la cabecera
    if t < 2.2:
        a = eout(ramp(t, .1, .7)) * (1 - ease(ramp(t, 1.15, 1.6)))
        sc = 1.06 - .06 * eout(ramp(t, .1, 1.2))
        paste_c(cv, shine(brand_big, ramp(t, .5, 1.3)), W/2, H*0.53, a, sc)
        lw = eout(ramp(t, .25, 1.0))
        paste_c(cv, line_long.resize((max(1, int(520*lw)), line_long.height)), W/2, H*0.53 - 80, a)
        paste_c(cv, line_long.resize((max(1, int(520*lw)), line_long.height)), W/2, H*0.53 + 70, a)
        paste_c(cv, sub_intro, W/2, H*0.53 + 135, a * eout(ramp(t, .45, .95)))
    # cabecera persistente
    hd = eout(ramp(t, 1.35, 1.95)) * (1 - e)
    if hd > 0:
        yh = H*0.075 + (1 - hd) * 30
        p = (t - 6.0) / 1.1 if 6.0 <= t <= 7.1 else (t - 1.4) / 1.0 if 1.4 <= t <= 2.4 else -1
        paste_c(cv, shine(brand_small, p), W/2, yh, hd)
        paste_c(cv, line_short, W/2 - brand_small.width/2 - 60, yh, hd * .9)
        paste_c(cv, line_short, W/2 + brand_small.width/2 + 60, yh, hd * .9)

    # "Gracias" en script
    g = window(t, 13.15, 18.45, .5, .45)
    if g > 0:
        y = H*0.20
        paste_c(cv, gracias_panel, W/2, y, g * .95, .96 + .04 * eout(ramp(t, 13.15, 13.8)))
        rev = eout(ramp(t, 13.2, 14.3))
        gi = gracias.crop((0, 0, max(1, int(gracias.width * rev)), gracias.height))
        canvas = Image.new("RGBA", gracias.size, (0, 0, 0, 0)); canvas.alpha_composite(gi)
        paste_c(cv, shine(canvas, ramp(t, 14.4, 15.4)), W/2, y - 10, g)
        paste_c(cv, dia, W/2, y + 120, g * eout(ramp(t, 14.0, 14.5)))

    # comunidad: partículas + palabra
    draw_particles(cv, t, 18.6, 22.0)
    c = window(t, 19.2, 21.9, .5, .4)
    if c > 0:
        paste_c(cv, glass_panel(700, 250), W/2, H*0.20, c * .95)
        paste_c(cv, comm_t, W/2, H*0.20 - 8, c, .94 + .06 * eout(ramp(t, 19.2, 20)))

    # CTA reseña en Google
    q = window(t, 25.25, END0 + .2, .5, .35)
    if q > 0:
        y = H*0.205 + (1 - eout(ramp(t, 25.25, 25.85))) * 60
        paste_c(cv, cta_panel, W/2, y, q * .97)
        paste_c(cv, cta_t1, W/2, y - 105, q)
        for k in range(5):
            st = 25.6 + k * .17; p = eout(ramp(t, st, st + .3))
            bounce = 1 + .25 * math.sin(math.pi * ramp(t, st, st + .3))
            paste_c(cv, STAR, W/2 + (k - 2) * 100, y - 15, q * p, max(.01, p * bounce))
        paste_c(cv, cta_t2, W/2, y + 92, q * eout(ramp(t, 26.3, 26.8)))

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
        paste_c(cv, end_t1, W/2, y0 + 165 + (1-a2)*20, a2)
        paste_c(cv, end_t2, W/2, y0 + 240 + (1-a2)*20, a2)
        for k in range(5):
            st = END0 + 1.0 + k * .1; p = eout(ramp(t, st, st + .25))
            paste_c(cv, STAR_S, W/2 + (k - 2) * 62, y0 + 360, a2 * p, max(.01, p))
        paste_c(cv, end_t3, W/2, y0 + 430, eout(ramp(t, END0 + 1.4, END0 + 1.9)))

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
