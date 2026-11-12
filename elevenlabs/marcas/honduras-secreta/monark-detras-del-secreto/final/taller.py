# Montaje del taller de Claudio: 6 etapas reales del proceso, 1 s cada una, estilo Monark (negro, ámbar, verde).
import cv2, numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1080, 1920, 30
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; FM = '/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf'
import os
if not os.path.exists(FM): FM = FB
AMB = (61, 163, 232); GRN = (91, 154, 61); BG = (12, 11, 11)
def label(img, n, name):
    pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); d = ImageDraw.Draw(pil)
    d.text((80, 170), f'0{n} / 06', font=ImageFont.truetype(FM, 38), fill=(170, 170, 160))
    d.text((80, 220), name, font=ImageFont.truetype(FB, 150), fill=(232, 163, 61))
    d.text((80, 1760), 'MONARK BRAND LABS', font=ImageFont.truetype(FM, 34), fill=(61, 154, 91))
    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
def frame_media(media, t):                       # medio dentro de un marco ámbar con zoom lento
    img = np.full((H, W, 3), BG, np.uint8)
    box = (80, 470, 1000, 1660); bw, bh = box[2] - box[0], box[3] - box[1]
    z = 1.0 + 0.06 * t; mh, mw = media.shape[:2]; s = max(bw / mw, bh / mh) * z
    m = cv2.resize(media, (int(mw * s), int(mh * s)), interpolation=cv2.INTER_AREA)
    y0 = (m.shape[0] - bh) // 2; x0 = (m.shape[1] - bw) // 2; img[box[1]:box[3], box[0]:box[2]] = m[y0:y0 + bh, x0:x0 + bw]
    cv2.rectangle(img, (box[0] - 4, box[1] - 4), (box[2] + 4, box[3] + 4), AMB, 4)
    return img
def vid(p, start=0):
    c = cv2.VideoCapture(p); c.set(cv2.CAP_PROP_POS_MSEC, start * 1000); out = []
    for _ in range(40):
        ok, f = c.read()
        if not ok: break
        out.append(f)
    return out
def wave(path, t):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', '8000', '-f', 's16le', '-'], stdout=subprocess.PIPE).stdout, np.int16).astype(np.float32)
    img = np.full((1190, 920, 3), (20, 18, 16), np.uint8); n = 70; seg = len(a) // n
    for i in range(n):
        v = np.abs(a[i * seg:(i + 1) * seg]).mean() / 4000; h = int(min(1, v) * 520 * (0.6 + 0.4 * abs(np.sin(t * 9 + i * .4)))) + 6
        x = 20 + i * 12; col = AMB if i / n < t else (70, 80, 90)
        cv2.rectangle(img, (x, 595 - h), (x + 7, 595 + h), col, -1)
    return img
def eq(t):
    img = np.full((1190, 920, 3), (20, 18, 16), np.uint8); rng = np.random.default_rng(int(t * 30))
    for i in range(16):
        h = int(150 + 750 * abs(np.sin(t * 6 + i * .7)) * (0.7 + 0.3 * rng.random()))
        for k in range(0, h, 34): cv2.rectangle(img, (40 + i * 54, 1150 - k), (40 + i * 54 + 40, 1150 - k - 24), AMB if k < 600 else GRN, -1)
    return img
guion = cv2.imread('guion.png'); lv = vid('../g1/land.mp4', 0.3); cv_ = vid('../g3/claudio.mp4', 3.0)
raw = cv2.VideoCapture('../real/t1_1080.mov'); raw.set(1, 180); before = raw.read()[1]
comp = cv2.VideoCapture('../g1/Escena1_prueba_cel.mp4'); comp.set(1, 180); after = comp.read()[1]
audit = cv2.imread('../../hs/enc/aud_all1.jpg')
STEPS = [('GUION', lambda t: guion[int(t * 900):int(t * 900) + 1400]), ('VOZ', lambda t: wave('../voces/claudio_A_CLAUDIO.mp3', t)),
         ('MÚSICA', eq), ('VIDEO', lambda t: np.hstack([lv[min(int(t * 30), len(lv) - 1)][:1240], cv_[min(int(t * 30), len(cv_) - 1)][:1240]])),
         ('COLOR', None), ('REVISIÓN', None)]
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '15', '-pix_fmt', 'yuv420p', 'taller.mp4'], stdin=subprocess.PIPE)
for n, (name, fn) in enumerate(STEPS, 1):
    for k in range(FPS):
        t = k / FPS
        if name == 'COLOR':
            x = int(1080 * (0.15 + 0.7 * t)); m = after.copy(); m[:, :x] = before[:, :x]; cv2.line(m, (x, 0), (x, 1920), (255, 255, 255), 6); media = m
        elif name == 'REVISIÓN':
            media = audit.copy(); hh, ww = media.shape[:2]
            for j in range(4):
                if t > j * .2: cv2.putText(media, 'OK', (ww - 260, 120 + j * 240), cv2.FONT_HERSHEY_DUPLEX, 3, (91, 200, 91), 6)
        else: media = fn(t)
        img = label(frame_media(media, t), n, name)
        if k < 4: img = (img * (k / 4)).astype(np.uint8)
        enc.stdin.write(img.tobytes())
enc.stdin.close(); enc.wait(); print('ok')
