#!/usr/bin/env python3
"""Honduras Secreta · "Así vivimos los catrachos" (falso documental, ~90 s).
Uso (dentro de la carpeta catr): edit_catrachos.py h|v FONTS_DIR [--subs] [segundos de vista previa...]
  h = 1920x1080 (YouTube) · v = 1080x1920 (Reels/TikTok). --subs quema subtítulos en inglés.
Escribe: timeline_<fmt>.json (cortes, frases y subtítulos) y video_<fmt>[_subs].mp4
"""
import subprocess, json, sys, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FMT = sys.argv[1]; FD = sys.argv[2].rstrip('/') + '/'
SUBS = '--subs' in sys.argv; ONLY = [float(a) for a in sys.argv[3:] if a[0].isdigit()]
W, H = (1920, 1080) if FMT == 'h' else (1080, 1920); FPS = 24

def dur(f): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))
def off(k): return json.load(open(f'sync/{k}_{FMT}.mov.json'))['off']
def S(k): return f'sync/{k}_{FMT}.mov'
def P(k): return f'prep/{k}_{FMT}.mp4'

# ---------- segmentos: (nombre, archivo, inicio, duración, audio) ----------
SEG = [('i0', S('i0'), 0, dur(S('i0')), 'clip'),
       ('i1', S('i1'), 0, dur(S('i1')), 'clip'),
       ('s1', S('s1'), 0, dur(S('s1')), 'clip'), ('s1b', P('s1'), 3.77, 2.2, 'clip'),
       ('i2', S('i2'), 0, dur(S('i2')), 'clip'),
       ('s2', P('s2'), 0, 5.4, 'clip'),
       ('i3', S('i3'), 0, dur(S('i3')), 'clip'),
       ('s3', P('s3'), 0, 6.2, 'clip'),
       ('i4', S('i4'), 0, dur(S('i4')), 'clip'),
       ('s4', P('s4'), 0, 6.0, 'clip'),
       ('i5', S('i5'), 0, dur(S('i5')), 'clip'),
       ('s5', P('s5'), 0, 6.0, 'clip'),
       ('i6', S('i6c'), 0, dur(S('i6c')), 'clip'),
       ('s6', P('s6'), 0, 8.0, 'punta'),
       ('i7', S('i7'), 0, dur(S('i7')), 'clip'),
       # montaje rápido
       ('m1', P('s1'), 4.4, .55, 'mute'), ('m2', P('s2'), 2.6, .55, 'mute'), ('m3', P('s3'), 4.9, .55, 'mute'),
       ('m4', P('s4'), 1.6, .55, 'mute'), ('m5', P('s5'), 1.2, .55, 'mute'), ('m6', P('s6'), 3.4, .55, 'mute'),
       ('m7', P('i7'), .6, .9, 'mute'), ('m8', P('s6'), 6.3, .7, 'mute'),
       ('i8', P('i8'), 0, 6.0, 'clip'),
       ('s7', S('s7'), 0, dur(S('s7')), 'clip'),
       ('end', S('s7'), dur(S('s7')) - 1 / 24, 6.0, 'mute')]   # cuadro final congelado bajo el cierre
START = {}; acc = 0.0
for nm, f, ss, d, a in SEG:
    START[nm] = acc; acc += round(d * FPS) / FPS
TOTAL = acc

# ---------- frases (español) y subtítulos en inglés ----------
def vo_words(k, vk):
    return [w for w in json.load(open(f'vo/{vk}.json'))['words'] if w['type'] == 'word']
LINES = []   # (t0, t1, español, inglés)
def jose(seg, k, vk, es, en):
    ws = vo_words(k, vk); o = START[seg] + off(k)
    LINES.append((o + ws[0]['start'] - .05, o + ws[-1]['end'] + .35, es, en))
jose('i0', 'i0', 'i0_c', 'Ser hondureño es fácil… Te explico.', 'Being Honduran is easy… Let me explain.')
jose('i1', 'i1', 'i1_b', 'Aquí todos somos bien puntuales.', 'Here, we are all very punctual.')
jose('s1', 's1', 's1_c', '¡Ya voy saliendo!', "I'm already on my way!")
jose('i2', 'i2', 'i2_b', 'El transporte es cómodo y tranquilo.', 'Public transport is comfy and relaxed.')
LINES.append((START['s2'] + .05, START['s2'] + 3.3, '¡Hay campo, hay campo! ¡Súbase, hay campo!', "There's room, there's room! Hop on, there's room!"))
jose('i3', 'i3', 'i3_c', 'La luz… nunca se va.', 'The power… never goes out.')
LINES.append((START['s3'] + 3.3, START['s3'] + 4.6, '¡Noooo!', 'Nooooo!'))
jose('i4', 'i4', 'i4_b', 'Comemos ligero.', 'We eat light.')
LINES.append((START['s4'] + .4, START['s4'] + 2.3, '¿Y le pongo aguacate, mi amor?', 'Want some avocado on it, sweetie?'))
jose('i5', 'i5', 'i5_a', 'El clima es bien fresco.', 'The weather is nice and cool.')
jose('i6', 'i6c', 'i6_c', 'Y en las fiestas… nos medimos.', 'And at parties… we keep it chill.')
jose('i7', 'i7', 'i7_c', 'Todo bien normal.', 'Totally normal.')
qw = [w for w in json.load(open('vo/q.json'))['words'] if w['type'] == 'word']; Q0 = START['i8'] + .3
LINES.append((Q0 + qw[0]['start'] - .05, Q0 + qw[-1]['end'] + .5, 'Si todo es así… ¿por qué amás Honduras?', 'If it’s all like this… why do you love Honduras?'))
jose('s7', 's7', 's7_c', '¿Y dónde más iba a ser tan feliz?', 'Where else could I ever be this happy?')
T_END = START['end'] + .3
json.dump({'start': START, 'total': TOTAL, 'lines': LINES, 'q0': Q0}, open(f'timeline_{FMT}.json', 'w'), ensure_ascii=False, indent=1)

# ---------- lectura de cuadros ----------
CACHE = {}
def frames(nm):
    if nm in CACHE: return CACHE[nm]
    _, f, ss, d, _ = [s for s in SEG if s[0] == nm][0]
    b = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(ss), '-i', f, '-t', str(d + .2), '-vf', f'fps=24,scale={W}:{H}',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE).stdout
    fs = [b[i * W * H * 3:(i + 1) * W * H * 3] for i in range(len(b) // (W * H * 3))]
    if nm == 'end': fs = fs[:1]
    CACHE.clear(); CACHE[nm] = fs; return fs

# ---------- gráficos ----------
def font(f, s, w=None):
    ft = ImageFont.truetype(FD + f, s)
    if w:
        try: ft.set_variation_by_axes([w])
        except Exception: pass
    return ft
SC = W / 1920 if FMT == 'h' else 1080 / 1080 * .9
def ease(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def text_img(txt, ft, fill=(255, 255, 255), stroke=0, track=0):
    ws = [ft.getlength(c) for c in txt]; tw = int(sum(ws) + track * max(len(txt) - 1, 0)) + 40; asc, desc = ft.getmetrics()
    m = Image.new('L', (tw, asc + desc + 40)); d = ImageDraw.Draw(m); x = 20
    for c, w_ in zip(txt, ws): d.text((x, 20), c, font=ft, fill=255, stroke_width=stroke, stroke_fill=255); x += w_ + track
    return m
def paste_text(lay, m, cx, cy, a, fill=(255, 255, 255), shadow=.75):
    if a <= 0: return
    x, y = int(cx - m.width / 2), int(cy - m.height / 2)
    sh = Image.new('RGBA', m.size, (0, 0, 0, 255)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * shadow * a)))
    lay.alpha_composite(sh, (x + 2, y + 5))
    fl = Image.new('RGBA', m.size, fill + (255,)); fl.putalpha(m.point(lambda v: int(v * a))); lay.alpha_composite(fl, (x, y))

# subtítulos en inglés: caja suave, dos líneas máx.
F_SUB = font('Montserrat[wght].ttf', 46 if FMT == 'h' else 50, 700)
SUB_Y = H - 120 if FMT == 'h' else int(H * .70)
SUB_MAXW = W * .8 if FMT == 'h' else W * .86
def wrap(txt, ft, maxw):
    words, lines, cur = txt.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if ft.getlength(t) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur); return lines
SUBCACHE = {}
def subtitle(lay, t):
    for t0, t1, es, en in LINES:
        if not (t0 <= t < t1): continue
        a = min(ease((t - t0) / .12), 1 - ease((t - (t1 - .12)) / .12))
        if en not in SUBCACHE: SUBCACHE[en] = [text_img(l, F_SUB) for l in wrap(en, F_SUB, SUB_MAXW)]
        ms = SUBCACHE[en]; lh = ms[0].height - 30; y0 = SUB_Y - (len(ms) - 1) * lh / 2
        bw = max(m.width for m in ms) - 10; bh = lh * len(ms) + 24
        box = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); ImageDraw.Draw(box).rounded_rectangle((0, 0, bw - 1, bh - 1), 18, fill=(0, 0, 0, int(150 * a)))
        lay.alpha_composite(box, (int(W / 2 - bw / 2), int(y0 - lh / 2 - 12)))
        for i, m in enumerate(ms): paste_text(lay, m, W / 2, y0 + i * lh, a, shadow=.4)

# rótulo de documental (al inicio, sobre la entrevista)
F_LT1 = font('Montserrat[wght].ttf', int(56 * (1 if FMT == 'h' else 1.05)), 800)
F_LT2 = font('Montserrat[wght].ttf', int(30 * (1 if FMT == 'h' else 1.05)), 500)
LT1, LT2 = text_img('JOSÉ', F_LT1, track=6), text_img('Hondureño · catracho de corazón', F_LT2, track=1)
F_TT = font('Montserrat[wght].ttf', 40 if FMT == 'h' else 44, 800); F_TT2 = font('CormorantGaramond-Italic[wght].ttf', 40 if FMT == 'h' else 44, 600)
TT1, TT2 = text_img('ASÍ VIVIMOS LOS CATRACHOS', F_TT, track=8), text_img('un documental de Honduras Secreta', F_TT2)
def lower_third(lay, t):
    a = ease((t - .5) / .4) * (1 - ease((t - (START['i1'] - .4)) / .4))
    if a <= 0: return
    if FMT == 'h': x0, y0 = 120, H - 300
    else: x0, y0 = 70, int(H * .58)
    bar = Image.new('RGBA', (8, 120), (255, 196, 40, int(255 * a))); lay.alpha_composite(bar, (x0, y0))
    for m, dy in ((LT1, 30), (LT2, 92)):
        m2 = m.crop((0, 0, max(1, int(m.width * ease((t - .6) / .6))), m.height))
        sh = Image.new('RGBA', m2.size, (0, 0, 0, 255)); sh.putalpha(m2.filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * .7 * a)))
        lay.alpha_composite(sh, (x0 + 12, y0 + dy - m2.height // 2 + 4))
        fl = Image.new('RGBA', m2.size, (255, 255, 255, 255)); fl.putalpha(m2.point(lambda v: int(v * a))); lay.alpha_composite(fl, (x0 + 10, y0 + dy - m2.height // 2))
def title_card(lay, t):
    a = ease((t - .2) / .5) * (1 - ease((t - (START['i1'] - .4)) / .4))
    if a <= 0: return
    y = 56 if FMT == 'h' else int(H * .05)
    paste_text(lay, TT1, W / 2, y, a); paste_text(lay, TT2, W / 2, y + 52, a, (255, 214, 140))

# cierre
LOGO = Image.open('../v5/logo_hs_fix.png').convert('RGBA'); LW = 760 if FMT == 'h' else 820
LOGO = LOGO.resize((LW, int(LOGO.height * LW / LOGO.width)), Image.LANCZOS)
F_E1 = font('Montserrat[wght].ttf', 58 if FMT == 'h' else 60, 800); F_E2 = font('CormorantGaramond-Italic[wght].ttf', 62 if FMT == 'h' else 66, 600)
F_E3 = font('Montserrat[wght].ttf', 30 if FMT == 'h' else 34, 500)
E1 = [text_img(l, F_E1, track=2) for l in (['Honduras no es lo que', 'dicen las noticias.'] if FMT == 'v' else ['Honduras no es lo que dicen las noticias.'])]
E2 = text_img('Es su gente.', F_E2)
E3 = [text_img(l, F_E3) for l in (["Honduras isn't what the news says.", "It's its people."])]
def endcard(lay, t):
    if t < T_END - .1: return
    a1 = ease((t - T_END) / .6); a2 = ease((t - (T_END + 1.1)) / .6); a3 = ease((t - (T_END + 2.2)) / .6)
    cy = H * .30 if FMT == 'h' else H * .30
    for i, m in enumerate(E1): paste_text(lay, m, W / 2, cy + i * 72, a1)
    paste_text(lay, E2, W / 2, cy + len(E1) * 72 + 30, a2, (255, 200, 90))
    if SUBS:
        for i, m in enumerate(E3): paste_text(lay, m, W / 2, cy + len(E1) * 72 + 110 + i * 42, a2 * .9, (230, 230, 230))
    lg = LOGO.copy(); lg.putalpha(lg.getchannel('A').point(lambda v: int(v * a3)))
    ly = int(H * .66 if FMT == 'h' else H * .62) - lg.height // 2
    sh = Image.new('RGBA', lg.size, (0, 0, 0, 255)); sh.putalpha(lg.getchannel('A').filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .6)))
    lay.alpha_composite(sh, (W // 2 - lg.width // 2 + 3, ly + 8)); lay.alpha_composite(lg, (W // 2 - lg.width // 2, ly))

# ---------- look común ----------
_x = np.arange(256) / 255.0; _S = np.clip(_x + .05 * np.sin(2 * np.pi * (_x - .5)) * (_x * (1 - _x)) * 4, 0, 1)
LUT = (np.clip(_S, 0, 1) * 255).astype(np.uint8)
_yy, _xx = np.mgrid[0:H, 0:W]; VIG = (1 - .16 * (((_xx - W / 2) / (W * .75)) ** 2 + ((_yy - H / 2) / (H * .75)) ** 2)).clip(.75, 1)[..., None].astype(np.float32)
def look(a): return np.clip(LUT[a].astype(np.float32) * VIG, 0, 255).astype(np.uint8)
def zoom(im, z, cy=.5):
    cw, ch = W / z, H / z; x0 = (W - cw) / 2; y0 = (H - ch) * cy
    return im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))

# ---------- render ----------
ORDER = [s[0] for s in SEG]; DUR = {s[0]: round(s[3] * FPS) for s in SEG}
out = f"video_{FMT}{'_subs' if SUBS else ''}.mp4"
enc = None if ONLY else subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
n = 0
for nm in ORDER:
    fs = frames(nm) if (not ONLY or any(START[nm] - .1 <= o < START[nm] + DUR[nm] / 24 + .1 for o in ONLY)) else None
    for k in range(DUR[nm]):
        t = n / FPS; n += 1
        if ONLY and not any(abs(t - o) < .5 / FPS for o in ONLY): continue
        raw = fs[min(k, len(fs) - 1)]
        im = Image.fromarray(look(np.frombuffer(raw, np.uint8).reshape(H, W, 3)))
        if nm.startswith('m'): im = zoom(im, 1.08 - .08 * k / max(DUR[nm] - 1, 1))      # montaje: pequeño empuje
        if nm == 'i8': im = zoom(im, 1 + .10 * ease(k / DUR[nm]), .42)                  # empuje lento mientras escucha
        if nm == 'end':
            p = ease(k / 18); im = Image.blend(im, im.filter(ImageFilter.GaussianBlur(16)), p)
            im = Image.blend(im, Image.new('RGB', (W, H), (12, 8, 4)), .35 * p)
        fo = ease((t - (TOTAL - .7)) / .7)
        if fo > 0: im = Image.blend(im, Image.new('RGB', (W, H)), fo)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        if t < START['i1']: title_card(lay, t); lower_third(lay, t)
        if SUBS and t < T_END: subtitle(lay, t)
        endcard(lay, t)
        im = im.convert('RGBA'); im.alpha_composite(lay); im = im.convert('RGB')
        if ONLY: im.save(f'pv_{FMT}_{t:.2f}.png')
        else: enc.stdin.write(im.tobytes())
if enc: enc.stdin.close(); enc.wait()
print('ok', out, round(TOTAL, 2))
