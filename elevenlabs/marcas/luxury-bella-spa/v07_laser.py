# Video 07: depilación láser + teléfono + planes de pago (2026-10-28 14:46) — versión creativa
FIX = {"Luxour": "Luxury"}
SUBS = [(0, 3), (4, 8), (9, 10), (11, 14), (15, 17), (18, 22), (23, 26), (27, 29), (30, 32), (33, 35), (36, 38),
        (39, 40), (50, 53), (54, 55), (56, 59), (60, 62)]          # los dígitos del teléfono van en el panel grande
KEY_ES = {"cansada", "depilarte", "constantemente?", "reducir", "vello", "simplificar", "depilación", "láser",
          "excelente", "luxury", "bella", "spa", "evaluamos", "piel", "tratamiento", "adecuado", "llama", "cita",
          "planes", "pago"}
ZK = [(0, 1.00), (0.4, 1.03), (3.2, 1.04), (10.9, 1.04), (11.3, 1.10), (13.9, 1.11), (14.1, 1.04), (18.2, 1.06),
      (18.4, 1.11), (22.2, 1.12), (22.4, 1.05), (99, 1.07)]
ANCHOR, CAP_Y, INTRO_BIG = (0.5, 0.38), 0.33, False
HEADER_SHINE, LEAK = [0.3, 11.4], []
INSETS = [(3.45, 10.95)]
INSET_S, INSET_DX, REVEAL_C = 0.58, 270, (0.5, 0.62)
PY = H * 0.185

def two(t1, t2, s2=140, w=780):
    return (glass_panel(w, 290), colorize(text_mask(t1, f_mont(28, 600), tracking=7), IVORY),
            colorize(text_mask(t2, f_script(s2)), "gold", glow=True))
def script_panel(cv, t, a, y, P, t_in, t2_in, dx2=0):
    panel, t1, t2 = P
    paste_c(cv, panel, W/2, y, a * .95, .96 + .04 * eout(ramp(t, t_in, t_in + .5)))
    paste_c(cv, t1, W/2, y - 85, a * eout(ramp(t, t_in + .15, t_in + .55)))
    rev = eout(ramp(t, t2_in, t2_in + .9))
    gi = t2.crop((0, 0, max(1, int(t2.width * rev)), t2.height))
    cnv = Image.new("RGBA", t2.size, (0, 0, 0, 0)); cnv.alpha_composite(gi)
    paste_c(cv, shine(cnv, ramp(t, t2_in + 1.0, t2_in + 2.0)), W/2 + dx2, y + 25, a)
def pill(im, pad=14):
    p = Image.new("RGBA", (im.width - 40 + 2*pad, im.height - 40 + 2*pad), (0, 0, 0, 0))
    ImageDraw.Draw(p).rounded_rectangle((0, 0, p.width - 1, p.height - 1), p.height // 2, fill=(22, 16, 13, 215))
    out = Image.new("RGBA", (max(p.width, im.width), max(p.height, im.height)), (0, 0, 0, 0))
    out.alpha_composite(p, ((out.width - p.width) // 2, (out.height - p.height) // 2))
    out.alpha_composite(im, ((out.width - im.width) // 2, (out.height - im.height) // 2))
    return out
LBL = lambda s: pill(colorize(text_mask(s, f_mont(22, 600), tracking=5), IVORY))
CL = lambda s: pill(colorize(text_mask(s, f_cormi(38, 700)), "gold"), 18)

# ---------- 1) intro: rastrillo que no para ----------
pA = two("¿CANSADA DE", "depilarte?", 150)
def razor_icon():
    m = Image.new("L", (120, 220)); d = ImageDraw.Draw(m)
    d.rounded_rectangle((10, 0, 110, 44), 10, fill=255)                 # cabezal
    for k in range(3): d.line((22, 12 + k * 10, 98, 12 + k * 10), fill=0, width=3)
    d.rounded_rectangle((50, 40, 70, 210), 9, fill=255)                 # mango
    return colorize(m.rotate(-28, expand=True, resample=Image.BICUBIC), "gold", glow=True)
RAZOR = razor_icon()

# ---------- 2) infografía: folículos + láser ----------
DW, DH = 960, 520
SURF, EPI, DER, BOT = 200, 252, 420, 505
rng2 = np.random.default_rng(5)
def build_texture():
    tex = Image.new("RGBA", (DW, DH), (0, 0, 0, 0)); d = ImageDraw.Draw(tex)
    for y in range(SURF - 20, BOT):
        if y < EPI: c0, c1, f = (242, 208, 184), (230, 184, 162), (y - SURF + 20) / (EPI - SURF + 20)
        elif y < DER: c0, c1, f = (226, 156, 152), (204, 122, 128), (y - EPI) / (DER - EPI)
        else: c0, c1, f = (246, 224, 168), (236, 205, 140), (y - DER) / (BOT - DER)
        d.line((0, y, DW, y), fill=tuple(int(a + (b - a) * f) for a, b in zip(c0, c1)) + (255,))
    for _ in range(110):
        x, y = rng2.uniform(20, DW - 20), rng2.uniform(SURF + 6, EPI - 6)
        d.ellipse((x - 13, y - 4, x + 13, y + 4), outline=(205, 160, 140, 150), width=2)
    for _ in range(40):
        x0, y0 = rng2.uniform(0, DW), rng2.uniform(EPI + 15, DER - 15); ph = rng2.uniform(0, 6)
        d.line([(x0 + k * 9, y0 + 6 * math.sin(k * .45 + ph)) for k in range(14)], fill=(244, 196, 192, 170), width=3)
    for _ in range(20):
        x, y, r = rng2.uniform(20, DW - 20), rng2.uniform(DER + 22, BOT - 10), rng2.uniform(16, 26)
        d.ellipse((x - r, y - r * .8, x + r, y + r * .8), fill=(250, 232, 180, 255), outline=(222, 186, 118, 255), width=3)
    for yb in (EPI, DER):
        d.line([(x, yb + 5 * math.sin(x / 55)) for x in range(0, DW, 8)], fill=(150, 80, 80, 140), width=3)
    m = Image.new("L", (DW, DH)); ImageDraw.Draw(m).polygon([(0, BOT)] + [(x, SURF + 4 * math.sin(x / 70)) for x in range(0, DW + 1, 6)] + [(DW, BOT)], fill=255)
    tex.putalpha(Image.fromarray((np.array(tex.getchannel("A")).astype(float) * np.array(m) / 255).astype(np.uint8)))
    return tex, m
SKIN_TEX, SKIN_M = build_texture()
FOL = [120, 255, 390, 525, 660, 795]                       # x de cada folículo
GROW = [3.7 + k * .18 for k in range(6)]
LZ0, LZ1 = 7.45, 9.95                                     # barrido del láser
HIT = [LZ0 + (x - 60) / (DW - 120) * (LZ1 - LZ0) for x in FOL]
KEEP = 3                                                  # un vello queda fino (reducción, no eliminación)

def hair_state(k, t):
    g = eout(ramp(t, GROW[k], GROW[k] + 1.1))
    h = ease(ramp(t, HIT[k] + .15, HIT[k] + 1.0))
    length = 150 * g * (1 - h * (.55 if k == KEEP else .92))
    width = 11 - h * (5 if k == KEEP else 8)
    heat = math.exp(-((t - HIT[k] - .2) / .28) ** 2)
    return length, max(2, width), heat, h

LB_FOL, LB_LAS, LB_MENOS = CL("Folículo"), CL("Láser"), CL("Menos vello")
LAYER_LBL = [(LBL("EPIDERMIS"), (SURF + EPI) / 2 + 4), (LBL("DERMIS"), (EPI + DER) / 2), (LBL("HIPODERMIS"), (DER + BOT) / 2 + 4)]

def leader(d, x0, y0, x1, y1, a):
    d.line((x0, y0, x1, y1), fill=(226, 196, 128, int(230 * a)), width=2)
    d.ellipse((x1 - 5, y1 - 5, x1 + 5, y1 + 5), fill=(240, 214, 150, int(255 * a)))

def diagram(t):
    b = eout(ramp(t, 3.6, 4.5))
    img = Image.new("RGBA", (DW, DH), (0, 0, 0, 0))
    wipe = Image.new("L", (DW, DH)); ImageDraw.Draw(wipe).rectangle((0, BOT - (BOT - SURF + 40) * b, DW, DH), fill=255)
    sk = SKIN_TEX.copy(); sk.putalpha(Image.fromarray((np.array(SKIN_TEX.getchannel("A")).astype(float) * np.array(wipe) / 255).astype(np.uint8)))
    img.alpha_composite(sk)
    d = ImageDraw.Draw(img)
    ab = ramp(b, .4, 1)
    if ab > 0:
        for k, x in enumerate(FOL):
            L_, w_, heat, h = hair_state(k, t)
            sy = SURF + 4 * math.sin(x / 70)
            # vaina del folículo y bulbo
            d.polygon([(x - 12, sy), (x + 12, sy), (x + 9, 380), (x - 9, 380)], fill=(236, 190, 176, int(255 * ab)), outline=(170, 100, 96, int(200 * ab)))
            bc = tuple(int(c0 + (c1 - c0) * min(1, heat)) for c0, c1 in zip((150, 84, 80), (255, 170, 60)))
            d.ellipse((x - 18, 368, x + 18, 404), fill=bc + (int(255 * ab),))
            # tallo dentro y fuera de la piel
            col = (70, 46, 32, int(255 * ab * (1 - .6 * h if k != KEEP else 1)))
            d.line([(x, 386), (x, sy)], fill=col, width=int(w_))
            if L_ > 2:
                d.line([(x, sy), (x + L_ * .25, sy - L_ * .55), (x + L_ * .32, sy - L_)], fill=col, width=int(w_), joint="curve")
            if heat > .02:                                            # calor en el bulbo
                yy_, xx_ = np.mgrid[0:120, 0:120] - 60
                gl = np.exp(-(xx_**2 + yy_**2) / 900) * heat * .8
                glow = Image.fromarray(np.dstack([np.full((120, 120), 255), np.full((120, 120), 150), np.full((120, 120), 50), gl * 255]).astype(np.uint8), "RGBA")
                img.alpha_composite(glow, (int(x - 60), 326)); d = ImageDraw.Draw(img)
    # cabezal láser y haz
    la = window(t, LZ0 - .45, LZ1 + .45, .35, .35)
    if la > 0:
        p = ramp(t, LZ0, LZ1); lx = 60 + p * (DW - 120)
        beam = Image.new("RGBA", (DW, DH), (0, 0, 0, 0)); bd = ImageDraw.Draw(beam)
        bd.polygon([(lx - 10, 70), (lx + 10, 70), (lx + 26, 390), (lx - 26, 390)], fill=(255, 120, 150, int(150 * la)))
        bd.polygon([(lx - 3, 70), (lx + 3, 70), (lx + 6, 390), (lx - 6, 390)], fill=(255, 240, 245, int(230 * la)))
        img.alpha_composite(beam.filter(ImageFilter.GaussianBlur(5))); d = ImageDraw.Draw(img)
        d.rounded_rectangle((lx - 52, 22, lx + 52, 74), 16, fill=(244, 238, 230, int(255 * la)), outline=(214, 180, 110, int(255 * la)), width=4)
        d.rounded_rectangle((lx - 22, 64, lx + 22, 78), 6, fill=(255, 130, 160, int(255 * la)))
    # etiquetas
    for k, (im, y) in enumerate(LAYER_LBL):
        a = eout(ramp(t, 4.3 + k * .2, 4.7 + k * .2)) * (1 - ramp(t, 10.6, 10.95))
        if a > 0: paste_c(img, im, 20 + im.width / 2, y, a)
    a = window(t, 5.2, 7.4, .35, .3)
    if a > 0: leader(d, 470, 470, FOL[3] + 20, 388, a); paste_c(img, LB_FOL, 470 + LB_FOL.width / 2 - 20, 470, a)
    a = window(t, 7.5, 10.0, .3, .3)
    if a > 0:
        lx = 60 + ramp(t, LZ0, LZ1) * (DW - 120)
        paste_c(img, LB_LAS, min(DW - LB_LAS.width / 2, lx + 70 + LB_LAS.width / 2), 48, a)
    a = eout(ramp(t, 10.0, 10.35)) * (1 - ramp(t, 10.6, 10.95))
    if a > 0: paste_c(img, LB_MENOS, DW / 2, 120, a, .9 + .1 * a)
    return img

DFRAME = glass_panel(DW + 40, DH + 40, r=34)
_g = np.linspace(0, 1, H)[:, None, None]
BG_GRAD = Image.fromarray((np.array((22, 17, 14)) * (1 - _g) + np.array((52, 40, 33)) * _g).repeat(W, 1).astype(np.uint8), "RGB")
DCY = H * 0.49
def laser_background(t):
    bg = BG_GRAD.copy().convert("RGBA")
    draw_particles(bg, t, 3.2, 11.2)
    a = eout(ramp(t, 3.55, 4.05))
    paste_c(bg, DFRAME, W / 2, DCY, a)
    paste_c(bg, diagram(t), W / 2, DCY, a)
    return bg.convert("RGB")
BG_FX = laser_background
pB = two("REDUCE EL VELLO Y", "simplifica tu rutina", 112, 800)
pC = two("DEPILACIÓN", "láser", 170)

# ---------- 3) evaluación: tonos de piel + lista ----------
pE = glass_panel(860, 300)
pE_t1 = colorize(text_mask("EVALUAMOS TU PIEL", f_mont(28, 600), tracking=8), IVORY)
TONES = [(247, 224, 206), (236, 200, 170), (214, 170, 130), (186, 136, 96), (140, 96, 64), (92, 62, 44)]
def swatch(c):
    m = Image.new("L", (84, 84)); ImageDraw.Draw(m).ellipse((2, 2, 81, 81), fill=255)
    im = Image.new("RGBA", (84, 84), c + (255,)); im.putalpha(m); return im
SW = [swatch(c) for c in TONES]
_rm = Image.new("L", (112, 112)); ImageDraw.Draw(_rm).ellipse((3, 3, 108, 108), outline=255, width=5)
RING = colorize(_rm, "gold", shadow=False, glow=True)
pK = glass_panel(860, 380)
_ck = Image.new("L", (56, 56)); ImageDraw.Draw(_ck).ellipse((1, 1, 54, 54), outline=255, width=4)
CIRC = colorize(_ck, "gold", shadow=False)
CHECKS = [(14.05, colorize(text_mask("Evaluación de tu piel", f_cormi(54, 600)), IVORY)),
          (15.2, colorize(text_mask("Orientación personalizada", f_cormi(54, 600)), IVORY)),
          (16.7, colorize(text_mask("Tratamiento adecuado", f_cormi(54, 600)), IVORY))]
def check_mark(p):
    m = Image.new("L", (56, 56)); d = ImageDraw.Draw(m)
    p1 = min(1, p * 2); p2 = max(0, p * 2 - 1)
    a0, a1, a2 = (15, 29), (25, 39), (42, 18)
    d.line((a0, (a0[0] + (a1[0] - a0[0]) * p1, a0[1] + (a1[1] - a0[1]) * p1)), fill=255, width=6)
    if p2 > 0: d.line((a1, (a1[0] + (a2[0] - a1[0]) * p2, a1[1] + (a2[1] - a1[1]) * p2)), fill=255, width=6)
    return colorize(m, "gold", shadow=False)

# ---------- 4) teléfono dígito a dígito + planes de pago ----------
PHONE = "(631) 365-6004"
DIG_T = [19.08, 19.30, 19.62, 19.94, 20.16, 20.40, 20.74, 21.0, 21.40, 21.72]
F_PH = f_mont(86, 600)
PH_CH, k = [], 0
x = 0
for ch in PHONE:
    w = F_PH.getlength(ch)
    if ch.isdigit(): st = DIG_T[k]; k += 1
    else: st = DIG_T[max(0, k - 1)] if ch != "(" else DIG_T[0] - .05
    PH_CH.append((ch, x + w / 2, st, colorize(text_mask(ch, F_PH), "gold", glow=True) if ch.strip() else None))
    x += w
PH_W = x
pP = glass_panel(900, 400)
pP_t1 = colorize(text_mask("LLAMA Y AGENDA TU CITA", f_mont(28, 600), tracking=7), IVORY)
pP_t3 = colorize(text_mask("Planes de pago disponibles", f_cormi(52, 700)), "gold")
_phm = Image.new("L", (70, 70)); _d = ImageDraw.Draw(_phm)
_d.ellipse((2, 2, 67, 67), outline=255, width=4)
_d.rounded_rectangle((22, 15, 48, 55), 7, outline=255, width=4); _d.line((31, 49, 39, 49), fill=255, width=4)
PH_ICON = colorize(_phm, "gold", shadow=False, glow=True)

END_LINES = [colorize(text_mask("Agenda tu cita", f_cormi(66, 500)), IVORY),
             colorize(text_mask(PHONE, f_mont(60, 600)), "gold")]
END_STARS = False
END_CTA = colorize(text_mask("PLANES DE PAGO DISPONIBLES", f_mont(28, 600), tracking=6), "gold")

def moments(cv, t, END0):
    y = PY
    a = window(t, 0.3, 3.5, .4, .3)
    if a > 0:
        script_panel(cv, t, a, y, pA, 0.3, 1.1, dx2=-70)
        sw = math.sin((t - .5) * 7.5)                                     # vaivén del rastrillo
        paste_c(cv, RAZOR.rotate(sw * 14, resample=Image.BICUBIC, expand=True), W/2 + 250 + sw * 26, y + 20,
                a * eout(ramp(t, .8, 1.2)), .55)
    b = window(t, 3.5, 7.35, .35, .3)
    if b > 0: script_panel(cv, t, b, y, pB, 3.5, 5.05)
    c = window(t, 7.35, 10.95, .3, .35)
    if c > 0: script_panel(cv, t, c, y, pC, 7.35, 7.95)
    e = window(t, 11.25, 14.0, .4, .3)
    if e > 0:
        paste_c(cv, pE, W/2, y, e * .95, .96 + .04 * eout(ramp(t, 11.25, 11.75)))
        paste_c(cv, pE_t1, W/2, y - 95, e)
        sel = 2
        p = ease(ramp(t, 12.5, 13.6)); pos = p * 5 if p < .8 else 4 - (4 - sel) * ramp(p, .8, 1)
        pos = 5 * ease(ramp(t, 12.5, 13.3)) if t < 13.3 else 5 - (5 - sel) * ease(ramp(t, 13.3, 13.85))
        for k2, s_ in enumerate(SW):
            pk = eout(ramp(t, 11.6 + k2 * .1, 11.9 + k2 * .1))
            paste_c(cv, s_, W/2 + (k2 - 2.5) * 118, y + 30, e * pk, max(.01, pk) * (1.08 if abs(pos - k2) < .5 else 1))
        paste_c(cv, RING, W/2 + (min(5, pos) - 2.5) * 118, y + 30, e * eout(ramp(t, 12.4, 12.7)))
    kk = window(t, 14.0, 18.25, .35, .35)
    if kk > 0:
        yk = y + 20
        paste_c(cv, pK, W/2, yk, kk * .95, .96 + .04 * eout(ramp(t, 14.0, 14.5)))
        for i, (st, im) in enumerate(CHECKS):
            p = eout(ramp(t, st - .1, st + .3)); yy_ = yk - 110 + 110 * i
            x0 = W/2 - 330
            paste_c(cv, CIRC, x0, yy_, kk * p)
            paste_c(cv, check_mark(ramp(t, st + .1, st + .5)), x0, yy_, kk * p)
            paste_c(cv, im, x0 + 50 + im.width / 2 - 20, yy_, kk * p)
    q = window(t, 18.3, END0 + .2, .45, .35)
    if q > 0:
        yp = y + 40 + (1 - eout(ramp(t, 18.3, 18.8))) * 60
        paste_c(cv, pP, W/2, yp, q * .97)
        paste_c(cv, pP_t1, W/2, yp - 130, q * eout(ramp(t, 18.45, 18.85)))
        ring = math.sin(t * 22) * 9 * window(t, 18.6, 19.3, .1, .2)
        paste_c(cv, PH_ICON.rotate(ring, resample=Image.BICUBIC), W/2 - PH_W/2 - 40, yp - 25, q * eout(ramp(t, 18.5, 18.9)), .9)
        for ch, cx, st, im in PH_CH:
            if im is None: continue
            p = eout(ramp(t, st, st + .18))
            pop = 1 + .3 * math.sin(math.pi * ramp(t, st, st + .22))
            paste_c(cv, im, W/2 - PH_W/2 + 30 + cx, yp - 25, q * p, max(.01, p * pop))
        a3 = eout(ramp(t, 25.5, 26.0))
        paste_c(cv, pill(pP_t3, 22), W/2, yp + 105 + (1 - a3) * 20, q * a3)
