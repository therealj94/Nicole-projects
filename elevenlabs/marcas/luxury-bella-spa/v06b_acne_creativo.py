# Video 06 (versión creativa): granitos en el rostro + capas de la piel animadas + tratamiento
FIX = {}
SUBS = [(0, 2), (3, 7), (8, 10), (11, 13), (14, 15), (16, 19), (20, 23), (24, 27), (28, 29), (30, 33), (34, 37),
        (38, 41), (42, 45), (46, 48), (49, 51), (52, 53), (54, 57), (58, 62)]
KEY_ES = {"granitos", "cara", "rostro", "importante,", "jabón.", "acné", "causas.", "análisis", "piel", "identificar",
          "tratamientos", "piel.", "comenta", "facial"}
ZK = [(0, 1.00), (0.4, 1.03), (4.9, 1.05), (5.1, 1.10), (7.3, 1.11), (7.5, 1.04), (11.6, 1.06), (11.85, 1.06),
      (21.9, 1.06), (22.1, 1.11), (22.35, 1.05), (99, 1.08)]
ANCHOR, CAP_Y, INTRO_BIG = (0.5, 0.37), 0.325, False
HEADER_SHINE, LEAK = [0.3, 22.4], []
INSETS = [(11.85, 21.95)]
INSET_S, INSET_DX, REVEAL_C = 0.58, 270, (0.43, 0.47)       # el círculo nace en su mejilla
PY = H * 0.185
T_PIMPLE = [0.95, 1.05, 1.15, 1.25, 1.35, 1.45, 1.55, 1.65, 1.75, 1.85]
T_HEAL0, T_HEAL1 = 18.3, 21.0

def two(t1, t2, s2=140, w=780, f2=None):
    return (glass_panel(w, 290), colorize(text_mask(t1, f_mont(28, 600), tracking=7), IVORY),
            colorize(text_mask(t2, f2 or f_script(s2), tracking=14 if f2 else 0), "gold", glow=True))
pA = two("¿TE SALEN", "granitos?", 150)
pB = two("LIMPIAR TU ROSTRO", "es importante", 140)
pB2 = two("PERO NO TODO SE RESUELVE", "con jabón", 150, 820)
pC = two("EL ACNÉ PUEDE TENER", "distintas causas", 125)
pD = two("IDENTIFICA LO QUE TU PIEL NECESITA", "Análisis de piel", 125, 880)
pT = two("CUIDADOS Y TRATAMIENTOS", "para tu piel", 135, 800)
pE = two("COMENTA", "PIEL", 0, 760, f_cinzel(118, 700))
pE_t3 = colorize(text_mask("o escríbenos por mensaje", f_cormi(44, 600)), IVORY)
END_LINES = [colorize(text_mask("Tu piel merece", f_cormi(66, 500)), IVORY),
             colorize(text_mask("un análisis profesional", f_cormi(66, 500)), IVORY)]
END_STARS = False
END_CTA = colorize(text_mask("COMENTA «PIEL»", f_mont(32, 600), tracking=8), "gold")

def script_panel(cv, t, a, y, P, t_in, t2_in):
    panel, t1, t2 = P
    paste_c(cv, panel, W/2, y, a * .95, .96 + .04 * eout(ramp(t, t_in, t_in + .5)))
    paste_c(cv, t1, W/2, y - 85, a * eout(ramp(t, t_in + .15, t_in + .55)))
    rev = eout(ramp(t, t2_in, t2_in + .9))
    gi = t2.crop((0, 0, max(1, int(t2.width * rev)), t2.height))
    cnv = Image.new("RGBA", t2.size, (0, 0, 0, 0)); cnv.alpha_composite(gi)
    paste_c(cv, shine(cnv, ramp(t, t2_in + 1.0, t2_in + 2.0)), W/2, y + 25, a)

# =================== 1) GRANITOS QUE SIGUEN EL ROSTRO ===================
def make_pimple(R=40):
    S = R * 7; yy_, xx_ = np.mgrid[0:S, 0:S] - S / 2
    d = np.sqrt(xx_**2 + yy_**2) / R
    halo = np.clip(1 - d / 3.0, 0, 1) ** 2 * .42                       # enrojecimiento difuso
    rgb = np.zeros((S, S, 3)); rgb[:] = (198, 82, 80); a = halo.copy()
    bump = np.clip((1.05 - d) * 2.2, 0, 1) ** 1.3                        # relieve suave
    shade = np.clip(.85 + .3 * (-(xx_ + yy_) / (R * 1.6)), .6, 1.1)[..., None]
    bcol = np.array((212, 122, 110)) * shade
    rgb = rgb * (1 - bump[..., None]) + bcol * bump[..., None]; a = np.maximum(a, bump * .62)
    wh = np.clip((.36 - np.sqrt(xx_**2 + (yy_ + .06*R)**2) / R) * 5, 0, 1) ** 1.2   # punto blanco
    rgb = rgb * (1 - wh[..., None]) + np.array((238, 222, 186)) * wh[..., None]; a = np.maximum(a, wh * .72)
    hl = np.clip((.18 - np.sqrt((xx_ + .34*R)**2 + (yy_ + .36*R)**2) / R) * 7, 0, 1) * .38
    rgb = rgb * (1 - hl[..., None]) + 255 * hl[..., None]; a = np.maximum(a, hl)
    im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a * 255]).astype(np.uint8), "RGBA")
    return im.filter(ImageFilter.GaussianBlur(R * .14))
PIMPLE = make_pimple()
# (landmark, desplazamiento vertical en anchos de cara, tamaño)
SPOTS = [(117, 0, 1.0), (280, 0, 1.05), (50, .01, .8), (427, 0, .75), (207, 0, .7), (346, 0, .85),
         (108, -.07, .8), (337, -.07, .7), (199, -.06, .85), (101, .02, .6)]
_fl, _lm = None, None
def landmarks(img):
    global _fl, _lm
    if _fl is None:
        import mediapipe as mp
        from mediapipe.tasks.python import vision, BaseOptions
        _fl = (mp, vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=os.environ.get("FACE_MODEL", "/tmp/x/face_landmarker.task")),
            num_faces=1)))
    mp, fl = _fl
    small = np.ascontiguousarray(np.array(img.resize((540, 960), Image.BILINEAR)))
    r = fl.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=small))
    if r.face_landmarks:
        p = np.array([(q.x * W, q.y * H) for q in r.face_landmarks[0]])
        _lm = p if _lm is None else .55 * p + .45 * _lm
    return _lm

def pimples(base, t):
    if t > T_HEAL1 + .6: return base
    L = landmarks(base)
    if L is None: return base
    fw = np.linalg.norm(L[234] - L[454])
    cv = base.convert("RGBA")
    for k, (i, dy, s) in enumerate(SPOTS):
        t0 = T_PIMPLE[k]
        pop = eout(ramp(t, t0, t0 + .28)) * (1 + .25 * math.sin(math.pi * ramp(t, t0, t0 + .28)))
        heal = 1 - ease(ramp(t, T_HEAL0 + k * .15, T_HEAL0 + 1.6 + k * .1))
        sz = fw * .034 * s * pop * (.35 + .65 * heal)
        if sz < 1 or heal <= 0.01: continue
        x, y = L[i][0], L[i][1] + dy * fw
        im = PIMPLE.resize((max(2, int(sz * 7)), max(2, int(sz * 7))), Image.BILINEAR)
        paste_c(cv, im, x, y, min(1, pop) * heal)
    return cv.convert("RGB")
PRE_FX = pimples

# =================== 2) CAPAS DE LA PIEL (infografía) ===================
DW, DH = 960, 540
SURF, EPI, DER, BOT = 140, 205, 390, 515
PX = 470
rng2 = np.random.default_rng(3)

def build_texture():
    tex = Image.new("RGBA", (DW, DH), (0, 0, 0, 0)); d = ImageDraw.Draw(tex)
    for y in range(SURF - 90, BOT):
        if y < EPI: c0, c1, f = (242, 208, 184), (230, 184, 162), (y - SURF + 90) / (EPI - SURF + 90)
        elif y < DER: c0, c1, f = (226, 156, 152), (204, 122, 128), (y - EPI) / (DER - EPI)
        else: c0, c1, f = (246, 224, 168), (236, 205, 140), (y - DER) / (BOT - DER)
        d.line((0, y, DW, y), fill=tuple(int(a + (b - a) * f) for a, b in zip(c0, c1)) + (255,))
    for _ in range(140):                                                   # células epidermis
        x, y = rng2.uniform(30, DW - 30), rng2.uniform(SURF - 10, EPI - 8)
        d.ellipse((x - 14, y - 5, x + 14, y + 5), outline=(205, 160, 140, 150), width=2)
    for _ in range(46):                                                    # colágeno dermis
        x0, y0 = rng2.uniform(0, DW), rng2.uniform(EPI + 15, DER - 15); ph = rng2.uniform(0, 6)
        pts = [(x0 + k * 9, y0 + 6 * math.sin(k * .45 + ph)) for k in range(14)]
        d.line(pts, fill=(244, 196, 192, 170), width=3)
    for _ in range(26):                                                    # lóbulos de grasa
        x, y, r = rng2.uniform(20, DW - 20), rng2.uniform(DER + 25, BOT - 15), rng2.uniform(18, 30)
        d.ellipse((x - r, y - r * .8, x + r, y + r * .8), fill=(250, 232, 180, 255), outline=(222, 186, 118, 255), width=3)
    for yb in (EPI, DER):                                                  # límites entre capas
        d.line([(x, yb + 5 * math.sin(x / 55)) for x in range(0, DW, 8)], fill=(150, 80, 80, 140), width=3)
    return tex
SKIN_TEX = build_texture()

def surf_y(x, bump):
    return SURF + 5 * math.sin(x / 70) - bump * 62 * math.exp(-((x - PX) / 58) ** 2)

def pill(im, pad=14):
    p = Image.new("RGBA", (im.width - 40 + 2*pad, im.height - 40 + 2*pad), (0, 0, 0, 0))
    ImageDraw.Draw(p).rounded_rectangle((0, 0, p.width - 1, p.height - 1), p.height // 2, fill=(22, 16, 13, 215))
    out = Image.new("RGBA", (max(p.width, im.width), max(p.height, im.height)), (0, 0, 0, 0))
    out.alpha_composite(p, ((out.width - p.width) // 2, (out.height - p.height) // 2))
    out.alpha_composite(im, ((out.width - im.width) // 2, (out.height - im.height) // 2))
    return out
LBL = lambda s: pill(colorize(text_mask(s, f_mont(22, 600), tracking=5), IVORY))
LAYER_LBL = [(LBL("EPIDERMIS"), (SURF + EPI) / 2 + 6), (LBL("DERMIS"), (EPI + DER) / 2), (LBL("HIPODERMIS"), (DER + BOT) / 2 + 6)]
CL = lambda s: pill(colorize(text_mask(s, f_cormi(38, 700)), "gold"), 18)
CAUSES = [(15.0, CL("Poro obstruido"), (PX + 26, SURF + 30), 112),
          (15.6, CL("Exceso de sebo"), (PX + 62, 272), 202),
          (16.2, CL("Bacterias"), (PX + 14, 330), 292),
          (16.8, CL("Inflamación"), (PX + 120, 300), 382)]
TREAT_LBL = CL("Tratamiento personalizado")
RESULT = [(20.6, CL("Poro más limpio"), (PX + 26, SURF + 30), 170), (21.0, CL("Menos inflamación"), (PX + 120, 300), 300)]
BACT = [(rng2.uniform(-14, 14), rng2.uniform(SURF + 30, 370), rng2.uniform(0, 6)) for _ in range(16)] + \
       [(rng2.uniform(-90, 90), rng2.uniform(230, 360), rng2.uniform(0, 6)) for _ in range(10)]

def leader(d, x0, y0, x1, y1, a):
    d.line((x0, y0, x1, y1), fill=(226, 196, 128, int(230 * a)), width=2)
    d.ellipse((x1 - 5, y1 - 5, x1 + 5, y1 + 5), fill=(240, 214, 150, int(255 * a)))

def diagram(t):
    b = eout(ramp(t, 12.0, 13.0))                 # construcción
    c = ease(ramp(t, 13.0, 14.3))                 # obstrucción
    r = ease(ramp(t, 18.2, 21.0))                 # tratamiento
    bump = c * (1 - r)
    img = Image.new("RGBA", (DW, DH), (0, 0, 0, 0))
    # forma de la piel (superficie con granito)
    poly = [(0, BOT)] + [(x, surf_y(x, bump)) for x in range(0, DW + 1, 6)] + [(DW, BOT)]
    m = Image.new("L", (DW, DH)); ImageDraw.Draw(m).polygon(poly, fill=255)
    wipe = Image.new("L", (DW, DH)); ImageDraw.Draw(wipe).rectangle((0, BOT - (BOT - SURF + 120) * b, DW, DH), fill=255)
    m = Image.fromarray((np.array(m).astype(float) * np.array(wipe) / 255).astype(np.uint8))
    sk = SKIN_TEX.copy(); sk.putalpha(m); img.alpha_composite(sk)
    d = ImageDraw.Draw(img)
    if b > .3:
        ab = ramp(b, .3, 1)
        # glándulas sebáceas
        for sx in (-1, 1):
            gx = PX + sx * 52
            d.ellipse((gx - 28, 238, gx + 28, 306), fill=(248, 210, 104, int(255 * ab)), outline=(214, 168, 70, int(255 * ab)), width=3)
            d.line((gx - sx * 28, 262, PX + sx * 12, 252), fill=(214, 168, 70, int(255 * ab)), width=6)
        # folículo / poro
        sy = surf_y(PX, bump)
        fol = [(PX - 22, sy + 2), (PX + 22, sy + 2), (PX + 13, 360), (PX - 13, 360)]
        d.polygon(fol, fill=(252, 238, 224, int(255 * ab)), outline=(170, 100, 96, int(255 * ab)))
        d.ellipse((PX - 22, 352, PX + 22, 394), fill=(186, 104, 110, int(255 * ab)))
        d.line([(PX, 372), (PX + 2, 300), (PX - 3, sy - 20), (PX + 14, sy - 75)], fill=(96, 64, 44, int(255 * ab)), width=5)
        # sebo acumulado
        lvl = c * (1 - .85 * r)
        if lvl > 0:
            top = 360 - lvl * (360 - (sy + 8))
            hw = lambda y: 13 + 9 * (360 - y) / (360 - sy)
            d.polygon([(PX - hw(top), top), (PX + hw(top), top), (PX + 13, 360), (PX - 13, 360)], fill=(244, 200, 80, 235))
            if bump > .5:
                d.ellipse((PX - 16, sy - 6, PX + 16, sy + 14), fill=(250, 238, 206, int(255 * ramp(bump, .5, 1))))
        # inflamación
        inf = c * (1 - r) * (.85 + .15 * math.sin(t * 5))
        if inf > 0:
            yy_, xx_ = np.mgrid[0:DH, 0:DW]
            g = np.exp(-(((xx_ - PX) / 150) ** 2 + ((yy_ - 280) / 115) ** 2)) * .6 * inf
            g *= np.array(m) / 255
            red = Image.fromarray(np.dstack([np.full((DH, DW), 225), np.full((DH, DW), 40), np.full((DH, DW), 50), g * 255]).astype(np.uint8), "RGBA")
            img.alpha_composite(red)
            d = ImageDraw.Draw(img)
        # bacterias
        for k, (bx, by, ph) in enumerate(BACT):
            vis = ramp(c, k / len(BACT) * .6, k / len(BACT) * .6 + .4) * (1 - ramp(r, k / len(BACT) * .5, k / len(BACT) * .5 + .4))
            if vis <= 0: continue
            x = PX + bx + 3 * math.sin(t * 3 + ph); y = by + 3 * math.cos(t * 2.6 + ph)
            d.rounded_rectangle((x - 9, y - 4, x + 9, y + 4), 4, fill=(132, 86, 168, int(235 * vis)), outline=(90, 50, 120, int(235 * vis)))
    # tratamiento: haces de luz y gotas
    tr = window(t, 18.0, 21.6, .5, .5)
    if tr > 0:
        beams = Image.new("RGBA", (DW, DH), (0, 0, 0, 0)); bd = ImageDraw.Draw(beams)
        for k in range(5):
            x = PX - 260 + k * 130 + 40 * math.sin(t * 1.5 + k)
            bd.polygon([(x - 18, -10), (x + 18, -10), (x + 70, 380), (x + 20, 380)],
                       fill=(255, 214, 150, int(70 * tr)))
        img.alpha_composite(beams.filter(ImageFilter.GaussianBlur(10)))
        d = ImageDraw.Draw(img)
        for k in range(7):
            ph = ((t - 18.0) * .9 + k / 7) % 1
            x = PX - 210 + k * 70; y = -10 + ph * (surf_y(x, bump) + 10)
            d.ellipse((x - 7, y - 10, x + 7, y + 8), fill=(250, 222, 150, int(230 * tr * (1 - ph * .4))))
    # análisis: barrido vertical
    sc = window(t, 14.55, 17.75, .3, .35)
    if sc > 0:
        ph = ((t - 14.55) / 1.6) % 2; ph = ph if ph < 1 else 2 - ph
        x = 30 + ph * (DW - 60)
        col = np.exp(-((np.arange(DW) - x) / 14) ** 2)[None, :].repeat(DH, 0) * np.array(m) / 255 * .65 * sc
        img.alpha_composite(Image.fromarray(np.dstack([np.full((DH, DW), 250), np.full((DH, DW), 225), np.full((DH, DW), 160), col * 255]).astype(np.uint8), "RGBA"))
        d = ImageDraw.Draw(img)
    # etiquetas de capas
    for k, (im, y) in enumerate(LAYER_LBL):
        a = eout(ramp(t, 12.4 + k * .2, 12.8 + k * .2)) * (1 - ramp(t, 21.6, 21.95))
        if a > 0: paste_c(img, im, 20 + im.width / 2, y, a)
    # causas / resultado
    for st, im, (ax, ay), ly in CAUSES:
        a = eout(ramp(t, st, st + .35)) * (1 - ease(ramp(t, 17.8, 18.2)))
        if a > 0:
            leader(d, DW - 300, ly, ax, ay, a); paste_c(img, im, min(DW - im.width / 2, DW - 300 + im.width / 2 - 20), ly, a)
    for st, im, (ax, ay), ly in RESULT:
        a = eout(ramp(t, st, st + .35)) * (1 - ramp(t, 21.6, 21.95))
        if a > 0:
            leader(d, DW - 300, ly, ax, ay, a); paste_c(img, im, min(DW - im.width / 2, DW - 300 + im.width / 2 - 20), ly, a)
    ta = window(t, 18.1, 21.95, .4, .35)
    if ta > 0: paste_c(img, TREAT_LBL, 32 + TREAT_LBL.width / 2, 45, ta)
    return img

DFRAME = glass_panel(DW + 40, DH + 40, r=34)
_g = np.linspace(0, 1, H)[:, None, None]
BG_GRAD = Image.fromarray((np.array((22, 17, 14)) * (1 - _g) + np.array((52, 40, 33)) * _g).repeat(W, 1).astype(np.uint8), "RGB")
DCY = H * 0.485
def skin_background(t):
    bg = BG_GRAD.copy().convert("RGBA")
    draw_particles(bg, t, 11.6, 22.2)
    a = eout(ramp(t, 11.95, 12.45))
    paste_c(bg, DFRAME, W / 2, DCY, a)
    paste_c(bg, diagram(t), W / 2, DCY, a)
    return bg.convert("RGB")
BG_FX = skin_background

# =================== momentos ===================
def moments(cv, t, END0):
    y = PY
    a = window(t, 0.35, 4.95, .4, .35)
    if a > 0: script_panel(cv, t, a, y, pA, 0.35, 1.0)
    b = window(t, 5.0, 7.45, .35, .3)
    if b > 0: script_panel(cv, t, b, y, pB, 5.0, 6.2)
    b2 = window(t, 7.45, 11.75, .3, .35)
    if b2 > 0: script_panel(cv, t, b2, y, pB2, 7.45, 10.9)
    c = window(t, 11.8, 14.4, .35, .3)
    if c > 0: script_panel(cv, t, c, y, pC, 11.8, 13.05)
    d = window(t, 14.4, 17.85, .3, .3)
    if d > 0: script_panel(cv, t, d, y, pD, 14.4, 14.55)
    tt = window(t, 17.85, 22.2, .3, .35)
    if tt > 0: script_panel(cv, t, tt, y, pT, 17.85, 18.6)
    e = window(t, 22.25, END0 + .2, .4, .35)
    if e > 0:
        ye = y + (1 - eout(ramp(t, 22.25, 22.75))) * 60
        pop = 1 + .18 * math.sin(math.pi * ramp(t, 22.85, 23.25))
        panel, t1, t2 = pE
        paste_c(cv, panel, W/2, ye, e * .95)
        paste_c(cv, t1, W/2, ye - 95, e * eout(ramp(t, 22.4, 22.8)))
        paste_c(cv, shine(t2, ramp(t, 23.4, 24.4)), W/2, ye + 5, e * eout(ramp(t, 22.85, 23.1)), pop)
        paste_c(cv, pE_t3, W/2, ye + 100, e * eout(ramp(t, 23.3, 23.8)))
