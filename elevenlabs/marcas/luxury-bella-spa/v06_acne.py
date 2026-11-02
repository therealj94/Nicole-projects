# Video 06: granitos/acné y análisis de piel, CTA "comenta PIEL" (2026-10-28 15:02)
UP = "/root/.claude/uploads/dd5b2fc2-184e-5514-b789-f8432119b327/"
FIX = {}
SUBS = [(0, 2), (3, 7), (8, 10), (11, 13), (14, 15), (16, 19), (20, 23), (24, 27), (28, 29), (30, 33), (34, 37),
        (38, 41), (42, 45), (46, 48), (49, 51), (52, 53), (54, 57), (58, 62)]
KEY_ES = {"granitos", "cara", "rostro", "importante,", "jabón.", "acné", "causas.", "análisis", "piel", "identificar",
          "tratamientos", "piel.", "comenta", "facial"}
ZK = [(0, 1.00), (0.4, 1.03), (4.9, 1.05), (5.1, 1.10), (7.3, 1.11), (7.5, 1.04), (11.6, 1.06), (11.85, 1.12),
      (14.2, 1.12), (14.45, 1.04), (17.6, 1.05), (17.85, 1.10), (22.1, 1.11), (22.35, 1.05), (99, 1.08)]
ANCHOR, CAP_Y, INTRO_BIG = (0.5, 0.37), 0.325, False      # cabeza más alta en esta toma
HEADER_SHINE, LEAK = [0.3, 22.4], []
BROLL = [(UP + "f114b8d5-IMG_5394.mp4", 8.0, 17.85, 21.95)]   # tratamientos estéticos
INSETS = [(17.85, 21.95)]
PY = H * 0.185                                              # altura de los paneles

def two(t1, t2, s2=140, w=780, f2=None):
    return (glass_panel(w, 290), colorize(text_mask(t1, f_mont(28, 600), tracking=7), IVORY),
            colorize(text_mask(t2, f2 or f_script(s2), tracking=14 if f2 else 0), "gold", glow=True))
pA = two("¿TE SALEN", "granitos?", 150)
pB = two("LIMPIAR TU ROSTRO", "es importante", 140)
pB2 = two("PERO NO TODO SE RESUELVE", "con jabón", 150, 820)
pC = two("EL ACNÉ PUEDE TENER", "distintas causas", 125)
pD = two("IDENTIFICA LO QUE TU PIEL NECESITA", "Análisis de piel", 125, 880)
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

# escaneo de "análisis de piel": esquinas de enfoque + línea dorada que recorre el rostro
BX, BY, BW, BH = W/2, H*0.49, 440, 480
def corner(len_=70, th=4):
    m = Image.new("L", (len_, len_)); d = ImageDraw.Draw(m)
    d.rectangle((0, 0, len_, th), fill=255); d.rectangle((0, 0, th, len_), fill=255)
    return m
_c = corner()
CORN = [colorize(_c.transpose(op) if op is not None else _c, "gold", shadow=True)
        for op in (None, Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, Image.ROTATE_180)]
_sl = np.zeros((40, BW)); _sl[18:22] = 1; _sl = np.clip(_sl + np.exp(-((np.arange(40)[:, None] - 20) / 9) ** 2) * .35, 0, 1)
_sl *= np.clip(np.minimum(np.linspace(0, 1, BW), np.linspace(1, 0, BW)) * 5, 0, 1)[None, :]
SCAN = Image.fromarray(np.dstack([np.full((40, BW, 3), (246, 220, 160)), _sl * 255]).astype(np.uint8), "RGBA")
def scan(cv, t, a0, a1):
    s = window(t, a0, a1, .35, .4)
    if s <= 0: return
    g = eout(ramp(t, a0, a0 + .5)); off = (1 - g) * 40
    for k, (cx, cy) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        paste_c(cv, CORN[k], BX + cx * (BW/2 - 35 + off), BY + cy * (BH/2 - 35 + off), s)
    ph = ((t - a0 - .3) / 1.25) % 2; ph = ph if ph < 1 else 2 - ph
    paste_c(cv, SCAN, BX, BY - BH/2 + 30 + ph * (BH - 60), s * .9)

def moments(cv, t, END0):
    y = PY
    a = window(t, 0.35, 4.95, .4, .35)
    if a > 0: script_panel(cv, t, a, y, pA, 0.35, 1.0)
    b = window(t, 5.0, 7.45, .35, .3)
    if b > 0: script_panel(cv, t, b, y, pB, 5.0, 6.2)
    b2 = window(t, 7.45, 11.75, .3, .35)
    if b2 > 0: script_panel(cv, t, b2, y, pB2, 7.45, 10.9)
    c = window(t, 11.8, 14.35, .35, .3)
    if c > 0: script_panel(cv, t, c, y, pC, 11.8, 13.05)
    scan(cv, t, 14.9, 17.75)
    d = window(t, 14.4, 22.2, .35, .35)
    if d > 0: script_panel(cv, t, d, y, pD, 14.4, 14.55)
    e = window(t, 22.25, END0 + .2, .4, .35)
    if e > 0:
        ye = y + (1 - eout(ramp(t, 22.25, 22.75))) * 60
        pop = 1 + .18 * math.sin(math.pi * ramp(t, 22.85, 23.25))
        panel, t1, t2 = pE
        paste_c(cv, panel, W/2, ye, e * .95)
        paste_c(cv, t1, W/2, ye - 95, e * eout(ramp(t, 22.4, 22.8)))
        paste_c(cv, shine(t2, ramp(t, 23.4, 24.4)), W/2, ye + 5, e * eout(ramp(t, 22.85, 23.1)), pop)
        paste_c(cv, pE_t3, W/2, ye + 100, e * eout(ramp(t, 23.3, 23.8)))
