# Video 04: cuidarte no es un lujo, mereces una pausa (2026-10-28 15:37)
FIX = {}
SUBS = [(0, 0), (1, 4), (5, 5), (6, 8), (9, 11), (12, 13), (14, 15), (16, 16), (17, 20), (21, 22), (23, 25),
        (26, 29), (30, 31), (32, 33), (34, 38), (39, 41), (42, 42), (43, 47), (48, 50), (51, 53), (54, 58)]
KEY_ES = {"cuidarte", "lujo", "tiempo.", "trabajo,", "familia", "responsabilidades,", "después.", "tú", "mereces",
          "pausa,", "cuidada", "momento", "ti.", "ti?", "comentarios"}
ZK = [(0, 1.00), (0.5, 1.03), (3.7, 1.05), (3.9, 1.11), (5.5, 1.12), (5.7, 1.03), (10.2, 1.06), (10.4, 1.12),
      (12.9, 1.13), (13.2, 1.04), (16.5, 1.07), (16.7, 1.13), (17.8, 1.14), (18.0, 1.05), (22.2, 1.07),
      (22.4, 1.13), (27.3, 1.14), (27.5, 1.06), (99, 1.07)]
ANCHOR, CAP_Y, INTRO_BIG = (0.5, 0.42), 0.355, False
HEADER_SHINE, LEAK = [0.3, 13.2], [(16.6, 22.2)]

pA = glass_panel(800, 300)
pA_t1 = colorize(text_mask("CUIDARTE NO ES UN LUJO", f_mont(30, 600), tracking=6), IVORY)
pA_t2 = colorize(text_mask("es dedicarte tiempo", f_script(118)), "gold", glow=True)
pB = glass_panel(820, 390)
ITEMS = [(6.20, colorize(text_mask("Trabajo", f_cormi(64, 600)), "gold")),
         (6.88, colorize(text_mask("Familia", f_cormi(64, 600)), "gold")),
         (8.56, colorize(text_mask("Responsabilidades", f_cormi(64, 600)), "gold"))]
pC = glass_panel(760, 300)
pC_t1 = colorize(text_mask("TÚ TAMBIÉN MERECES", f_mont(30, 600), tracking=8), IVORY)
pC_t2 = colorize(text_mask("una pausa", f_script(150)), "gold", glow=True)
pD = glass_panel(760, 300)
pD_t1 = colorize(text_mask("UN MOMENTO", f_mont(30, 600), tracking=10), IVORY)
pD_t2 = colorize(text_mask("solo para ti", f_script(145)), "gold", glow=True)
pE = glass_panel(820, 320)
pE_t1 = colorize(text_mask("¿CUÁNDO FUE LA ÚLTIMA VEZ?", f_mont(28, 600), tracking=5), IVORY)
pE_t2 = colorize(text_mask("Cuéntame", f_script(150)), "gold", glow=True)
DOT = colorize(Image.new("L", (1, 1)).resize((1, 1)), IVORY)
_d = Image.new("L", (26, 26)); ImageDraw.Draw(_d).ellipse((0, 0, 25, 25), fill=255); DOT = colorize(_d, "gold", shadow=False)
END_LINES = [colorize(text_mask("Tú también mereces", f_cormi(66, 500)), IVORY),
             colorize(text_mask("una pausa", f_cormi(66, 500)), IVORY)]
END_STARS = False
END_CTA = colorize(text_mask("TE LEO EN LOS COMENTARIOS", f_mont(28, 600), tracking=6), "gold")

def script_panel(cv, t, a, y, panel, t1, t2, t_in, t2_in=None):
    t2_in = t_in + .25 if t2_in is None else t2_in
    paste_c(cv, panel, W/2, y, a * .95, .96 + .04 * eout(ramp(t, t_in, t_in + .5)))
    paste_c(cv, t1, W/2, y - 85, a * eout(ramp(t, t_in + .15, t_in + .55)))
    rev = eout(ramp(t, t2_in, t2_in + 1.05))
    gi = t2.crop((0, 0, max(1, int(t2.width * rev)), t2.height))
    cnv = Image.new("RGBA", t2.size, (0, 0, 0, 0)); cnv.alpha_composite(gi)
    paste_c(cv, shine(cnv, ramp(t, t2_in + 1.15, t2_in + 2.15)), W/2, y + 25, a)

def moments(cv, t, END0):
    y = H*0.20
    a = window(t, 0.45, 5.45, .45, .4)
    if a > 0: script_panel(cv, t, a, y, pA, pA_t1, pA_t2, 0.45, 3.8)
    b = window(t, 5.9, 12.75, .4, .4)
    if b > 0:
        paste_c(cv, pB, W/2, y, b * .95, .96 + .04 * eout(ramp(t, 5.9, 6.4)))
        for k, (st, im) in enumerate(ITEMS):
            p = eout(ramp(t, st - .05, st + .35)); yy_ = y - 100 + 100*k
            fade = 1 - .55 * ease(ramp(t, 10.8, 11.6))         # "nos dejamos para después": se apagan
            paste_c(cv, im, W/2 + (1-p)*-30, yy_, b * p * fade)
            paste_c(cv, dia, W/2 - im.width/2 - 6, yy_ + 4, b * p * fade)
    c = window(t, 13.15, 18.1, .45, .35)
    if c > 0: script_panel(cv, t, c, y, pC, pC_t1, pC_t2, 13.15, 16.6)
    draw_particles(cv, t, 17.6, 22.3)
    d = window(t, 18.1, 22.25, .4, .35)
    if d > 0: script_panel(cv, t, d, y, pD, pD_t1, pD_t2, 18.1, 20.9)
    e = window(t, 22.3, END0 + .2, .45, .35)
    if e > 0:
        ye = y + (1 - eout(ramp(t, 22.3, 22.8))) * 60
        script_panel(cv, t, e, ye - 15, pE, pE_t1, pE_t2, 22.3, 22.4)
        for k in range(3):                                  # puntos de "escribiendo..."
            ph = (t - 23.5) * 2.4 - k * .35
            bob = max(0, math.sin(ph * math.pi)) if t > 23.5 else 0
            paste_c(cv, DOT, W/2 + (k - 1) * 44, ye + 112 - bob * 12, e * eout(ramp(t, 23.4, 23.8)) * (.55 + .45 * bob))
