import cv2, numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS = 1080, 1920, 30
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; FX = '/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'
LOGO = Image.open('/home/user/Nicole-projects/elevenlabs/marcas/honduras-secreta/logo_honduras_secreta_reconstruido.png').convert('RGBA')
def canvas(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def sub(text, cx, cy, size=62, fill=(255, 255, 255)):
    im = canvas(); d = ImageDraw.Draw(im); f = ImageFont.truetype(FB, size)
    lines = text.split('\n'); hs = size * 1.18; y = cy - hs * len(lines) / 2
    for ln in lines:
        w = d.textlength(ln, font=f); x = max(40, min(W - 40 - w, cx - w / 2))
        d.text((x, y), ln, font=f, fill=fill, stroke_width=7, stroke_fill=(0, 0, 0, 230)); y += hs
    return im
def tag(t1, t2, x, y):
    im = canvas(); d = ImageDraw.Draw(im)
    d.rounded_rectangle((x, y, x + 520, y + 120), 18, fill=(12, 11, 11, 225), outline=(232, 163, 61, 255), width=3)
    d.text((x + 28, y + 16), t1, font=ImageFont.truetype(FX, 48), fill=(232, 163, 61))
    d.text((x + 28, y + 72), t2, font=ImageFont.truetype(FB, 30), fill=(91, 190, 120)); return im
def bubble(name, msg, col):
    im = canvas(); d = ImageDraw.Draw(im); x, y = 140, 260
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x + 6, y + 10, x + 806, y + 200), 34, fill=(0, 0, 0, 120))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(10))); d = ImageDraw.Draw(im)
    d.rounded_rectangle((x, y, x + 800, y + 190), 34, fill=(250, 248, 244, 250))
    d.ellipse((x + 26, y + 30, x + 126, y + 130), fill=(232, 163, 61)); d.text((x + 76, y + 80), 'N', font=ImageFont.truetype(FX, 56), fill=(255, 255, 255), anchor='mm')
    d.text((x + 150, y + 26), name, font=ImageFont.truetype(FB, 36), fill=(110, 105, 98))
    d.text((x + 150, y + 74), msg, font=ImageFont.truetype(FX, 84), fill=col); return im
def big(text, cy, size=150, col=(232, 163, 61)):
    im = canvas(); d = ImageDraw.Draw(im); f = ImageFont.truetype(FX, size)
    d.text((W / 2, cy), text, font=f, fill=col, anchor='mm', stroke_width=8, stroke_fill=(0, 0, 0, 220)); return im
def credits():
    im = canvas(); d = ImageDraw.Draw(im); y = 250
    for a, b in [('Idea', 'Nicole'), ('Producción', 'Monark Brand Labs'), ('Estrella', 'la guara')]:
        d.text((W / 2, y), a.upper(), font=ImageFont.truetype(FB, 34), fill=(232, 163, 61), anchor='mm', stroke_width=5, stroke_fill=(0, 0, 0, 200))
        d.text((W / 2, y + 58), b, font=ImageFont.truetype(FX, 64), fill=(255, 255, 255), anchor='mm', stroke_width=7, stroke_fill=(0, 0, 0, 220)); y += 170
    return im
def endcard():
    im = Image.new('RGBA', (W, H), (8, 8, 8, 200)); lw = 860; lg = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)))
    im.alpha_composite(lg, ((W - lw) // 2, 520)); d = ImageDraw.Draw(im)
    d.text((W / 2, 1010), '¿Qué lugar de Honduras', font=ImageFont.truetype(FX, 70), fill=(255, 255, 255), anchor='mm')
    d.text((W / 2, 1095), 'grabamos después?', font=ImageFont.truetype(FX, 70), fill=(255, 255, 255), anchor='mm')
    d.text((W / 2, 1210), 'Comentalo', font=ImageFont.truetype(FB, 54), fill=(232, 163, 61), anchor='mm')
    d.text((W / 2, 1380), 'MONARK BRAND LABS  ×  HONDURAS SECRETA', font=ImageFont.truetype(FB, 32), fill=(91, 190, 120), anchor='mm'); return im
OV = [  # (inicio, fin, capa)
 (1.2, 4.4, sub('Cada video de Honduras Secreta\ncomienza con una idea loca.', 540, 400)),
 (15.0, 17.6, tag('CLAUDIO', 'Monark Brand Labs', 500, 760)),
 (16.75, 18.0, sub('Vos soñalo.', 790, 980)),
 (19.35, 20.8, sub('Yo lo produzco.', 790, 980)),
 (21.65, 22.75, big('EL TALLER', 300, 120)),
 (30.3, 32.6, tag('LA GUARA', 'Estrella de Honduras Secreta', 470, 1500)),
 (34.4, 37.0, sub('¿Ya? Yo nací listo.', 780, 560)),
 (38.25, 39.6, sub('¡Acción!', 540, 330, 80)),
 (44.75, 47.1, bubble('Nicole · Monark', '0/10', (200, 40, 30))),
 (47.15, 48.1, big('VERSIÓN 7', 960, 150)),
 (48.15, 51.6, bubble('Nicole · Monark', '10/10  ♥', (40, 150, 70))),
 (51.85, 54.4, credits()),
 (54.3, 57.92, endcard()),
]
OV = [(a, b, np.array(im).astype(np.float32)) for a, b, im in OV]
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', 'base.mov', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', 'video_ov.mp4'], stdin=subprocess.PIPE)
i = 0
while True:
    b = dec.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32); t = i / FPS
    for a0, a1, im in OV:
        if a0 <= t <= a1:
            k = min(1, (t - a0) / .15, (a1 - t) / .15); al = im[..., 3:] / 255 * k
            f = f * (1 - al) + im[..., :3] * al
    enc.stdin.write(f.astype(np.uint8).tobytes()); i += 1
enc.stdin.close(); enc.wait(); print('frames', i)
