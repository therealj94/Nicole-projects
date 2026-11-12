import cv2, numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS = 1080, 1920, 24
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; FX = '/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'
FM = 'fonts/PermanentMarker.ttf'; FR = 'fonts/Fraunces.ttf'
LOGO = Image.open('/home/user/Nicole-projects/elevenlabs/marcas/honduras-secreta/logo_honduras_secreta_reconstruido.png').convert('RGBA')
cv = lambda: Image.new('RGBA', (W, H), (0, 0, 0, 0))
def sub(text, cy, size=60, font=FB, cx=540, fill=(255, 255, 255)):
    im = cv(); d = ImageDraw.Draw(im); lines = text.split('\n')
    while size > 30 and max(d.textlength(l, font=ImageFont.truetype(font, size)) for l in lines) > 960: size -= 2
    f = ImageFont.truetype(font, size); hs = size * 1.2; y = cy - hs * len(lines) / 2
    for ln in lines:
        w = d.textlength(ln, font=f); x = max(40, min(W - 40 - w, cx - w / 2))
        d.text((x, y), ln, font=f, fill=fill, stroke_width=7, stroke_fill=(0, 0, 0, 230)); y += hs
    return im
def place(text, cy):                               # rótulo de lugar estilo marcador sobre cinta de papel
    im = cv(); d = ImageDraw.Draw(im); f = ImageFont.truetype(FM, 62); w = d.textlength(text, font=f)
    x = (W - w) / 2; d.rounded_rectangle((x - 34, cy - 54, x + w + 34, cy + 50), 10, fill=(246, 236, 214, 235))
    d.text((x, cy - 46), text, font=f, fill=(150, 60, 25)); return im.rotate(-2.5, resample=Image.BICUBIC, center=(540, cy))
def title(cy):
    im = cv(); d = ImageDraw.Draw(im); f = ImageFont.truetype(FM, 120)
    d.text((540, cy), 'LA ENCOMIENDA', font=f, fill=(255, 244, 222), anchor='mm', stroke_width=9, stroke_fill=(90, 40, 15)); return im
def endtext(lines, cy, size=62):
    im = cv(); d = ImageDraw.Draw(im); f = ImageFont.truetype(FR, size); y = cy
    for ln in lines: d.text((540, y), ln, font=f, fill=(255, 246, 228), anchor='mm', stroke_width=5, stroke_fill=(20, 25, 50, 200)); y += size * 1.3
    return im
def endcard():
    im = Image.new('RGBA', (W, H), (10, 14, 30, 215)); lw = 860; lg = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)))
    im.alpha_composite(lg, ((W - lw) // 2, 470)); d = ImageDraw.Draw(im)
    d.text((540, 900), 'Merry Christmas, catrachos.', font=ImageFont.truetype(FR, 66), fill=(255, 238, 205), anchor='mm')
    d.text((540, 1060), 'Someone you love far away?', font=ImageFont.truetype(FX, 58), fill=(255, 255, 255), anchor='mm')
    d.text((540, 1135), 'Send them a message. We\'ll share it on the 24th.', font=ImageFont.truetype(FB, 42), fill=(230, 230, 230), anchor='mm')
    d.text((540, 1250), '#DesdeHondurasConAmor', font=ImageFont.truetype(FX, 56), fill=(46, 190, 186), anchor='mm'); return im
Y = lambda f: int(f * 1920)
def lyr(text, cy=Y(.83)): return sub(text, cy, 44, FR, fill=(255, 236, 200))
M0 = 74.3
marta = [(0.22, 4.4, 'Son… we are all doing well here,\nthanks to you.'), (4.88, 9.3, 'The house has a new roof,\nand your sister\nstarted university.'),
         (9.66, 11.5, 'We know how hard it is for you.'), (11.72, 14.5, 'This Christmas, don\'t worry\nabout us…'), (14.72, 15.9, 'take care of yourself.'),
         (16.1, 18.9, 'We\'ll be waiting for you here,\nno matter how long it takes.')]
S = [ # (inicio, fin, texto, altura)
 (7.2, 10.8, 'Doña Marta, this year the care\npackage goes the other way.', .37),
 (10.95, 14.7, 'Then take a little piece\nof home to my Carlos.', .37),
 (15.3, 20.7, 'Take him this coffee,\nso he remembers the little cups\nof coffee and bread\nhis grandma used to give him.', .14),
 (22.0, 24.9, 'With this smell, he\'ll feel\nlike he\'s in Marcala!', .14),
 (25.8, 28.2, 'Hey! Those are for Carlos…', .28), (28.25, 29.7, 'Oh, little macaw!', .28), (29.95, 32.3, '…but take one, for the trip.', .28),
 (32.75, 36.0, 'Tell him I got into university,\nand it\'s thanks to him!', .12), (36.05, 37.5, 'We love you, uncle!', .12), (37.8, 39.4, 'Say nacatamal!', .37),
 (40.1, 42.0, 'Take good care of it for me, okay?', .30), (45.0, 47.1, 'With my life, Doña Marta.', .60),
 (48.75, 51.9, 'Hang in there, nacatamal…\nwe\'re almost there.', .10),
 (54.75, 56.7, 'Anything to declare?', .35), (57.65, 59.8, 'Just love… and a nacatamal.', .35), (60.55, 61.6, 'Merry Christmas.', .35),
 (63.35, 63.8, 'What\'s this?…', .32), (63.85, 66.9, 'What\'s this?… From Honduras?', .32),
 (72.35, 73.95, 'It smells like my grandma\'s house…', .15),
 (93.6, 94.9, 'Thank you, Mom…', .36), (94.95, 96.8, 'Thank you, Mom… Merry Christmas.', .36)]
OV = [(0.4, 3.6, place('Far from home', 230)), (3.7, 7.0, title(820)),
      (0.4, 3.6, lyr('Even if you\'re far from your homeland,')), (4.3, 7.3, lyr('even if the cold makes you miss it,')),
      (15.2, 18.6, place('Marcala, La Paz', 1720)), (25.6, 29.0, place('Sabanagrande, Francisco Morazán', 1720))]
OV += [(a, b, sub(t, Y(y))) for a, b, t, y in S]
OV += [(M0 + a, M0 + b, sub(t, 1300, 54, FR, fill=(255, 246, 228))) for a, b, t in marta]
OV += [(97.3, 102.9, lyr('In every cup of coffee,\nHonduras comes to hug you.')), (103.7, 106.5, lyr('There\'s always a place at the table,')), (107.1, 109.7, lyr('always a plate for you.')),
       (99.6, 103.4, endtext(['To those who left', 'to chase a dream…'], 360)),
       (103.4, 106.9, endtext(['…and to hold up', 'their family\'s dreams:'], 360)),
       (106.9, 109.4, endtext(['Honduras never forgets you.'], 380, 64)),
       (109.4, 113.36, endcard())]
OV = [(a, b, np.array(im).astype(np.float32)) for a, b, im in OV]
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', 'v2/seg/base2.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-vf', 'eq=saturation=1.04,format=yuv420p', '-c:v', 'libx264', '-crf', '17', 'v2/video_ov.mp4'], stdin=subprocess.PIPE)
i = 0
while True:
    b = dec.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32); t = i / FPS
    for a0, a1, im in OV:
        if a0 <= t <= a1:
            k = min(1, (t - a0) / .2, (a1 - t) / .2); al = im[..., 3:] / 255 * k; f = f * (1 - al) + im[..., :3] * al
    enc.stdin.write(f.astype(np.uint8).tobytes()); i += 1
enc.stdin.close(); enc.wait(); print('frames', i)
