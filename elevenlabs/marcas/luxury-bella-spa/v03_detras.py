# Video 03: detrás de cada experiencia (2026-10-28 15:47) + tomas de apoyo
UP = "/root/.claude/uploads/dd5b2fc2-184e-5514-b789-f8432119b327/"
FIX = {}
SUBS = [(0, 1), (2, 4), (5, 7), (8, 11), (12, 15), (16, 17), (18, 21), (22, 24), (25, 27), (28, 30), (31, 34),
        (35, 37), (38, 38), (39, 41), (42, 45), (46, 49), (50, 52), (53, 54), (55, 59), (60, 61)]
KEY_ES = {"experiencia", "luxury", "bella", "spa?", "tratamiento", "preparación,", "detalles", "compromiso",
          "cuidado", "clientas.", "visita", "personalizada,", "llegas", "despides.", "gracias", "confiar", "esperamos"}
ZK = [(0, 1.00), (0.7, 1.03), (5.2, 1.06), (5.6, 1.10), (13.9, 1.10), (14.2, 1.04), (20.9, 1.06), (21.2, 1.12),
      (24.7, 1.13), (25.0, 1.05), (99, 1.07)]
ANCHOR, CAP_Y, INTRO_BIG = (0.5, 0.42), 0.355, False
HEADER_SHINE, LEAK = [0.3, 3.95], [(21.2, 24.8)]

# Tomas de apoyo: (archivo, segundo de inicio en la toma, desde, hasta) en el tiempo del video principal
BROLL = [(UP + "39098b7e-IMG_3482.mp4", 1.0, 5.7, 10.4),     # cejas/pestañas: preparación, detalles
         (UP + "f114b8d5-IMG_5394.mp4", 3.0, 10.4, 13.95),   # mascarilla: cuidado de clientas
         (UP + "71e13bcf-IMG_8216.mp4", 6.0, 16.6, 20.95),   # masaje: experiencia personalizada
         (UP + "f114b8d5-IMG_5394.mp4", 12.0, 24.85, 30.2)]  # te esperamos
INSETS = [(5.7, 13.95), (16.6, 20.95), (24.85, 30.3)]
INSET_S, INSET_DX = 0.80, 150

pA = glass_panel(760, 300)
pA_t1 = colorize(text_mask("DESCUBRE", f_mont(32, 600), tracking=12), IVORY)
pA_t2 = colorize(text_mask("detrás de escena", f_script(132)), "gold", glow=True)
pB = glass_panel(820, 390)
ITEMS = [(7.82, colorize(text_mask("Preparación", f_cormi(64, 600)), "gold")),
         (8.86, colorize(text_mask("Atención al detalle", f_cormi(64, 600)), "gold")),
         (10.92, colorize(text_mask("Compromiso", f_cormi(64, 600)), "gold"))]
pG = glass_panel(760, 300)
pG_t1 = colorize(text_mask("GRACIAS POR", f_mont(30, 600), tracking=10), IVORY)
pG_t2 = colorize(text_mask("tu confianza", f_script(140)), "gold", glow=True)
pC = glass_panel(800, 300)
pC_t1 = colorize(text_mask("TE ESPERAMOS", f_mont(30, 600), tracking=10), IVORY)
pC_t2 = colorize(text_mask("Agenda tu visita", f_script(130)), "gold", glow=True)
END_LINES = [colorize(text_mask("Cada visita,", f_cormi(66, 500)), IVORY),
             colorize(text_mask("una experiencia única", f_cormi(66, 500)), IVORY)]
END_STARS = False
END_CTA = colorize(text_mask("AGENDA TU CITA HOY", f_mont(30, 600), tracking=6), "gold")

def script_panel(cv, t, a, y, panel, t1, t2, t_in):
    paste_c(cv, panel, W/2, y, a * .95, .96 + .04 * eout(ramp(t, t_in, t_in + .5)))
    paste_c(cv, t1, W/2, y - 85, a * eout(ramp(t, t_in + .15, t_in + .55)))
    rev = eout(ramp(t, t_in + .25, t_in + 1.3))
    gi = t2.crop((0, 0, max(1, int(t2.width * rev)), t2.height))
    cnv = Image.new("RGBA", t2.size, (0, 0, 0, 0)); cnv.alpha_composite(gi)
    paste_c(cv, shine(cnv, ramp(t, t_in + 1.4, t_in + 2.4)), W/2, y + 25, a)

def moments(cv, t, END0):
    y = H*0.20
    a = window(t, 0.65, 5.3, .45, .4)
    if a > 0: script_panel(cv, t, a, y, pA, pA_t1, pA_t2, 0.65)
    b = window(t, 7.6, 13.95, .4, .4)
    if b > 0:
        paste_c(cv, pB, W/2, y, b * .95, .96 + .04 * eout(ramp(t, 7.6, 8.1)))
        for k, (st, im) in enumerate(ITEMS):
            p = eout(ramp(t, st - .05, st + .35)); yy_ = y - 100 + 100*k
            paste_c(cv, im, W/2 + (1-p)*-30, yy_, b * p)
            paste_c(cv, dia, W/2 - im.width/2 - 6, yy_ + 4, b * p)
    g = window(t, 22.5, 24.8, .45, .35)
    if g > 0: script_panel(cv, t, g, y, pG, pG_t1, pG_t2, 22.5)
    c = window(t, 25.0, END0 + .2, .45, .35)
    if c > 0: script_panel(cv, t, c, y + (1 - eout(ramp(t, 25.0, 25.5))) * 60, pC, pC_t1, pC_t2, 25.0)
