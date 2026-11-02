# Video 02: cuidado de la piel para hombres (2026-10-28 19:18)
FIX = {}
SUBS = [(0, 0), (1, 5), (6, 9), (10, 12), (13, 14), (15, 15), (16, 16), (17, 19), (20, 21), (22, 24), (25, 27), (28, 30)]
KEY_ES = {"hombres,", "cuidado", "piel", "masculina", "limpieza,", "hidratación", "personalizados.", "rostro", "bien"}
ZK = [(0, 1.00), (0.6, 1.02), (4.3, 1.05), (4.6, 1.10), (9.7, 1.12), (10.0, 1.03), (14.6, 1.07), (99, 1.07)]
ANCHOR, CAP_Y, INTRO_BIG = (0.5, 0.42), 0.355, False
HEADER_SHINE, LEAK = [0.3, 10.1], [(0.6, 4.3)]

pA = glass_panel(760, 300)
pA_t1 = colorize(text_mask("SKIN CARE", f_mont(32, 600), tracking=12), IVORY)
pA_t2 = colorize(text_mask("para hombres", f_script(150)), "gold", glow=True)
pB = glass_panel(820, 390)
ITEMS = [(6.40, colorize(text_mask("Limpieza", f_cormi(64, 600)), "gold")),
         (7.16, colorize(text_mask("Hidratación", f_cormi(64, 600)), "gold")),
         (8.18, colorize(text_mask("Cuidados personalizados", f_cormi(64, 600)), "gold"))]
pC = glass_panel(800, 300)
pC_t1 = colorize(text_mask("CUIDADO FACIAL MASCULINO", f_mont(28, 600), tracking=6), IVORY)
pC_t2 = colorize(text_mask("Agenda tu cita", f_script(140)), "gold", glow=True)
END_LINES = [colorize(text_mask("Cuida tu piel,", f_cormi(66, 500)), IVORY),
             colorize(text_mask("siéntete bien", f_cormi(66, 500)), IVORY)]
END_STARS = False
END_CTA = colorize(text_mask("AGENDA TU CITA HOY", f_mont(30, 600), tracking=6), "gold")

def moments(cv, t, END0):
    y = H*0.20
    a = window(t, 0.55, 4.35, .45, .4)
    if a > 0:
        paste_c(cv, pA, W/2, y, a * .95, .96 + .04 * eout(ramp(t, .55, 1.1)))
        paste_c(cv, pA_t1, W/2, y - 85, a * eout(ramp(t, .7, 1.1)))
        rev = eout(ramp(t, .8, 1.9))
        gi = pA_t2.crop((0, 0, max(1, int(pA_t2.width * rev)), pA_t2.height))
        cnv = Image.new("RGBA", pA_t2.size, (0, 0, 0, 0)); cnv.alpha_composite(gi)
        paste_c(cv, shine(cnv, ramp(t, 2.0, 3.0)), W/2, y + 25, a)
    b = window(t, 6.2, 9.75, .4, .4)
    if b > 0:
        paste_c(cv, pB, W/2, y, b * .95, .96 + .04 * eout(ramp(t, 6.2, 6.7)))
        for k, (st, im) in enumerate(ITEMS):
            p = eout(ramp(t, st - .05, st + .35)); yy_ = y - 100 + 100*k
            paste_c(cv, im, W/2 + (1-p)*-30, yy_, b * p)
            paste_c(cv, dia, W/2 - im.width/2 - 6, yy_ + 4, b * p)
    c = window(t, 9.95, END0 + .2, .45, .35)
    if c > 0:
        yc = y + (1 - eout(ramp(t, 9.95, 10.5))) * 60
        paste_c(cv, pC, W/2, yc, c * .97)
        paste_c(cv, pC_t1, W/2, yc - 85, c)
        paste_c(cv, shine(pC_t2, ramp(t, 11.0, 12.0)), W/2, yc + 25, c * eout(ramp(t, 10.2, 10.8)))
