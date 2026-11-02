# Video 01: agradecimiento a clientas + reseña en Google (2026-10-28 19:43)
FIX = {"Luxor": "Luxury"}
SUBS = [(0, 2), (3, 6), (7, 10), (11, 14), (15, 17), (18, 19), (20, 23), (24, 26), (27, 29), (30, 33),
        (34, 36), (37, 38), (39, 40), (41, 44), (45, 47), (48, 51), (52, 54), (55, 57), (58, 59)]
KEY_ES = {"feliz", "reserva", "luxury", "bella", "spa", "visita,", "recomendación", "elegirnos.", "cuidado",
          "belleza.", "comunidad", "ti.", "experiencia", "opinión", "google"}
ZK = [(0, 1.00), (1.25, 1.03), (5.75, 1.06), (6.15, 1.13), (12.9, 1.15), (13.3, 1.04), (18.5, 1.07), (18.9, 1.14),
      (21.7, 1.16), (22.1, 1.05), (28.9, 1.09), (99, 1.09)]
ANCHOR, CAP_Y, INTRO_BIG = (0.5, 0.50), 0.37, True
HEADER_SHINE, LEAK = [1.4, 6.0], [(13.1, 18.4)]

gracias = colorize(text_mask("Gracias", f_script(230)), "gold", glow=True)
gracias_panel = glass_panel(760, 330)
cta_panel = glass_panel(860, 330)
cta_t1 = colorize(text_mask("TU OPINIÓN NOS IMPORTA", f_mont(30, 600), tracking=6), IVORY)
cta_t2 = colorize(text_mask("Déjanos tu reseña en Google", f_cormi(58, 600)), "gold")
comm_t = colorize(text_mask("comunidad", f_script(150)), "gold", glow=True)
END_LINES = [colorize(text_mask("Gracias por ser parte", f_cormi(66, 500)), IVORY),
             colorize(text_mask("de nuestra historia", f_cormi(66, 500)), IVORY)]
END_STARS = True
END_CTA = colorize(text_mask("CALIFÍCANOS EN GOOGLE", f_mont(28, 600), tracking=6), "gold")

def moments(cv, t, END0):
    g = window(t, 13.15, 18.45, .5, .45)
    if g > 0:
        y = H*0.20
        paste_c(cv, gracias_panel, W/2, y, g * .95, .96 + .04 * eout(ramp(t, 13.15, 13.8)))
        rev = eout(ramp(t, 13.2, 14.3))
        gi = gracias.crop((0, 0, max(1, int(gracias.width * rev)), gracias.height))
        canvas = Image.new("RGBA", gracias.size, (0, 0, 0, 0)); canvas.alpha_composite(gi)
        paste_c(cv, shine(canvas, ramp(t, 14.4, 15.4)), W/2, y - 10, g)
        paste_c(cv, dia, W/2, y + 120, g * eout(ramp(t, 14.0, 14.5)))
    draw_particles(cv, t, 18.6, 22.0)
    c = window(t, 19.2, 21.9, .5, .4)
    if c > 0:
        paste_c(cv, glass_panel(700, 250), W/2, H*0.20, c * .95)
        paste_c(cv, comm_t, W/2, H*0.20 - 8, c, .94 + .06 * eout(ramp(t, 19.2, 20)))
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
