import cv2, numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS = 1080, 1920, 24
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; FX = '/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'
FM = 'fonts/PermanentMarker.ttf'; FR = 'fonts/Fraunces.ttf'
LOGO = Image.open('/home/user/Nicole-projects/elevenlabs/marcas/honduras-secreta/logo_honduras_secreta_reconstruido.png').convert('RGBA')
cv = lambda: Image.new('RGBA', (W, H), (0, 0, 0, 0))
def sub(text, cy, size=60, font=FB, cx=540, fill=(255, 255, 255)):
    im = cv(); d = ImageDraw.Draw(im); f = ImageFont.truetype(font, size); lines = text.split('\n'); hs = size * 1.2; y = cy - hs * len(lines) / 2
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
    d.text((540, 900), 'Feliz Navidad, catrachos.', font=ImageFont.truetype(FR, 66), fill=(255, 238, 205), anchor='mm')
    d.text((540, 1060), '¿Tenés a alguien lejos?', font=ImageFont.truetype(FX, 58), fill=(255, 255, 255), anchor='mm')
    d.text((540, 1135), 'Mandale tu mensaje. Lo publicamos el 24.', font=ImageFont.truetype(FB, 42), fill=(230, 230, 230), anchor='mm')
    d.text((540, 1250), '#DesdeHondurasConAmor', font=ImageFont.truetype(FX, 56), fill=(46, 190, 186), anchor='mm'); return im
# subtítulos de la mamá (voz en off) por frases, a partir de los tiempos de la transcripción
M0 = 54.0
marta = [(0.22, 4.4, 'Mijo… aquí todos estamos bien,\ngracias a vos.'), (4.88, 9.3, 'La casa ya tiene techo nuevo,\ny tu hermana ya entró\na la universidad.'),
         (9.66, 11.5, 'Sabemos lo que te cuesta.'), (11.72, 14.5, 'Esta Navidad no te preocupés\npor nosotros…'), (14.72, 15.9, 'cuidate vos.'),
         (16.1, 18.9, 'Aquí te esperamos,\nel tiempo que sea.')]
OV = [(0.4, 3.6, place('Muy lejos de casa', 230)),
      (6.35, 9.0, sub('Este año, la encomienda va al revés.', 700)),
      (9.1, 12.3, title(720)),
      (13.0, 16.2, place('Marcala, La Paz', 230)),
      (18.0, 21.3, place('Sabanagrande, Francisco Morazán', 230)),
      (39.45, 40.75, sub('Anything to declare?\n(¿Algo que declarar?)', 640, 54)),
      (40.8, 43.7, sub('Solo amor… y un nacatamal.', 640))]
OV += [(M0 + a, M0 + b, sub(t, 1300, 54, FR, fill=(255, 246, 228))) for a, b, t in marta]
OV += [(72.99, 74.55, sub('Gracias, mamá.', 820)),
       (79.4, 82.6, endtext(['A los que se fueron', 'a buscar un sueño…'], 360)),
       (82.6, 85.4, endtext(['…y a sostener', 'los de su familia:'], 360)),
       (85.4, 86.9, endtext(['Honduras no los olvida.'], 380, 68)),
       (86.9, 91.17, endcard())]
OV = [(a, b, np.array(im).astype(np.float32)) for a, b, im in OV]
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', 'seg/base2.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-vf', 'eq=saturation=1.04,format=yuv420p', '-c:v', 'libx264', '-crf', '17', 'video_ov.mp4'], stdin=subprocess.PIPE)
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
