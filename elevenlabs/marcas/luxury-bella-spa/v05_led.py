# Video 05: relajación + cuidado de la piel, terapia de luz LED (2026-10-28 15:23)
UP = "/root/.claude/uploads/dd5b2fc2-184e-5514-b789-f8432119b327/"
FIX = {}
SUBS = [(0, 3), (4, 6), (7, 8), (9, 11), (12, 13), (14, 14), (15, 15), (16, 19), (20, 22), (23, 26), (27, 28),
        (29, 31), (32, 34), (35, 37), (38, 40), (41, 44)]
KEY_ES = {"relajación", "piel?", "tratamientos", "personalizados,", "mascarillas", "hidratación", "cuidado", "ti.",
          "piel,", "terapia", "led.", "consentirte."}
ZK = [(0, 1.00), (0.2, 1.02), (4.0, 1.04), (4.2, 1.10), (5.6, 1.11), (5.8, 1.03), (11.5, 1.06), (11.8, 1.12),
      (15.0, 1.13), (15.25, 1.04), (19.3, 1.07), (19.5, 1.13), (21.5, 1.14), (21.75, 1.05), (99, 1.08)]
ANCHOR, CAP_Y, INTRO_BIG = (0.5, 0.42), 0.355, False
HEADER_SHINE, LEAK = [0.3, 15.3], [(11.8, 15.1)]
BROLL = [(UP + "f114b8d5-IMG_5394.mp4", 3.0, 8.3, 11.75)]     # mascarilla
INSETS = [(8.3, 11.75)]

def two(t1, t2, s2=140, w=780):
    return (glass_panel(w, 300), colorize(text_mask(t1, f_mont(28, 600), tracking=7), IVORY),
            colorize(text_mask(t2, f_script(s2)), "gold", glow=True))
pA = two("TU MOMENTO DE RELAJACIÓN", "cuidar tu piel", 140, 800)
pB = glass_panel(860, 390)
ITEMS = [(6.38, colorize(text_mask("Tratamientos personalizados", f_cormi(60, 600)), "gold")),
         (8.44, colorize(text_mask("Mascarillas", f_cormi(60, 600)), "gold")),
         (10.30, colorize(text_mask("Hidratación", f_cormi(60, 600)), "gold"))]
pC = two("UN MOMENTO DE", "cuidado para ti", 130)
pD = two("SEGÚN LAS NECESIDADES DE TU PIEL", "Terapia de luz LED", 112, 860)
pE = two("ES MOMENTO DE", "consentirte", 150)
END_LINES = [colorize(text_mask("Es momento", f_cormi(66, 500)), IVORY),
             colorize(text_mask("de consentirte", f_cormi(66, 500)), IVORY)]
END_STARS = False
END_CTA = colorize(text_mask("AGENDA TU CITA HOY", f_mont(30, 600), tracking=6), "gold")

def script_panel(cv, t, a, y, P, t_in, t2_in):
    panel, t1, t2 = P
    paste_c(cv, panel, W/2, y, a * .95, .96 + .04 * eout(ramp(t, t_in, t_in + .5)))
    paste_c(cv, t1, W/2, y - 85, a * eout(ramp(t, t_in + .15, t_in + .55)))
    rev = eout(ramp(t, t2_in, t2_in + 1.05))
    gi = t2.crop((0, 0, max(1, int(t2.width * rev)), t2.height))
    cnv = Image.new("RGBA", t2.size, (0, 0, 0, 0)); cnv.alpha_composite(gi)
    paste_c(cv, shine(cnv, ramp(t, t2_in + 1.15, t2_in + 2.15)), W/2, y + 25, a)

# brillo LED: luz de color que respira desde los bordes (rojo -> violeta -> azul)
_ly, _lx = np.mgrid[0:H//8, 0:W//8]
_edge = np.minimum.reduce([_lx, W//8 - 1 - _lx, _ly, H//8 - 1 - _ly]) / (W//8 * .5)
_edge = np.clip(1 - _edge / .5, 0, 1) ** 1.8
LEDC = [(255, 60, 90), (190, 80, 255), (70, 140, 255)]
def led_glow(cv, t, s):
    if s <= 0: return
    ph = (t * .45) % 1 * len(LEDC); i = int(ph); f = ph - i
    c0, c1 = np.array(LEDC[i % 3]), np.array(LEDC[(i + 1) % 3]); col = c0 + (c1 - c0) * f
    breath = .75 + .25 * math.sin(t * 4)
    a = _edge * .34 * s * breath
    im = Image.fromarray(np.dstack([np.broadcast_to(col, a.shape + (3,)), a * 255]).astype(np.uint8), "RGBA")
    cv.alpha_composite(im.resize((W, H), Image.BILINEAR))

def moments(cv, t, END0):
    y = H*0.20
    led_glow(cv, t, window(t, 19.35, 21.65, .45, .5))
    a = window(t, 0.15, 5.6, .4, .4)
    if a > 0: script_panel(cv, t, a, y, pA, 0.15, 4.1)
    b = window(t, 6.0, 11.8, .4, .35)
    if b > 0:
        paste_c(cv, pB, W/2, y, b * .95, .96 + .04 * eout(ramp(t, 6.0, 6.5)))
        for k, (st, im) in enumerate(ITEMS):
            p = eout(ramp(t, st - .05, st + .35)); yy_ = y - 100 + 100*k
            paste_c(cv, im, W/2 + (1-p)*-30, yy_, b * p)
            paste_c(cv, dia, W/2 - im.width/2 - 6, yy_ + 4, b * p)
    c = window(t, 11.85, 15.1, .4, .35)
    if c > 0: script_panel(cv, t, c, y, pC, 11.85, 13.6)
    draw_particles(cv, t, 12.6, 15.2)
    d = window(t, 15.25, 21.65, .4, .35)
    if d > 0: script_panel(cv, t, d, y, pD, 15.25, 19.4)
    e = window(t, 21.7, END0 + .2, .4, .35)
    if e > 0: script_panel(cv, t, e, y + (1 - eout(ramp(t, 21.7, 22.2))) * 60, pE, 21.7, 23.1)
