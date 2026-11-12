# Sincroniza cada toma con sus voces: el VIDEO se ajusta a la voz natural (nunca se estira el audio).
import json, subprocess, numpy as np, sys
norm = lambda s: s.lower().strip('¡!¿?,.…[]').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
def words(js, t0=0, t1=1e9): return [w for w in json.load(open(js))['words'] if w['type'] == 'word' and t0 <= w['start'] < t1]
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
CFG = {
 '01': [('vo/e1', None, (0, 8))], '02': [('vo/k2', None, (0, 4))], '03': [('vo/e3', None, (0, 6))],
 '04': [('vo/e4', None, (0, 6))], 'K4': [('vo/k4', None, (0, 4))], 'K5a': [('vo/k5a', None, (0, 4))],
 '05': [('vo/r5', None, (0, 8))], 'K5b': [('vo/k5b', None, (0, 4))], '06': [('vo/e6', None, (0, 8))],
 'G6': [('vo/g6', None, (0, 4))], '07': [('vo/r7a', None, (0, 6))], 'K7': [('vo/k7', None, (0, 4))],
 'R7b': [('vo/r7b', None, (0, 8))], '08': [('vo/m8', None, (0, 5.5))], 'K8': [('vo/k8', None, (0, 4))],
}
for n in ([a for a in sys.argv[1:] if not a.startswith('--')] or CFG):
    vid = f'hd/{n}.mp4'; vj = f'tr/{n}.json'; D = dur(vid)
    anchors = [(0.0, 0.0)]; delta = 0.0; clips = []
    for item in CFG[n]:
        src, trim, (w0, w1) = item[:3]; vov = item[3] if len(item) > 3 else None
        vw = words(vj, w0, w1)
        if src == 'VEO':
            a, b = vw[0]['start'] - .05, vw[-1]['end'] + .05
            anchors += [(a + delta, a), (b + delta, b)]; clips.append(('tr/' + n + '.wav', a, b, a + delta)); continue
        t0, t1 = trim or (0, 1e9); tw = words(src + '.json', t0, t1)
        ts, te = tw[0]['start'], tw[-1]['end']; vs, ve = (vov if vov is not None else vw[0]['start']), vw[-1]['end']
        out0 = max(vs + delta, anchors[-1][0] + .05)            # inicio de la línea en la salida
        off = out0 - ts
        pairs = [(ts + off, vs)]
        k = 0
        for w in (tw[1:-1] if vov is None else []):                                       # palabras intermedias que coinciden
            for j in range(k + 1, len(vw) - 1):
                if norm(vw[j]['text']) == norm(w['text']): pairs.append((w['start'] + off, vw[j]['start'])); k = j; break
        pairs.append((te + off, ve)); anchors += pairs; delta = (te + off) - ve
        a0 = max(t0, ts - .25); a1 = min(t1, te + .35)
        clips.append((src + '.mp3', a0, a1, a0 + off))
    total = D + delta; anchors.append((total, D))
    O = np.array([a[0] for a in anchors]); S = np.array([a[1] for a in anchors])
    T = np.arange(0, total - 1 / 48, 1 / 24); src = np.interp(T, O, S)
    src = np.convolve(np.pad(src, 3, mode='edge'), np.ones(7) / 7, mode='valid')
    spd = np.diff(src) * 24
    if '--audio' in sys.argv: print(n, 'solo audio'); clips_only = True
    else: clips_only = False
    F = None if clips_only else np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',vid,'-f','rawvideo','-pix_fmt','rgb24','-'], stdout=subprocess.PIPE).stdout, np.uint8).reshape(-1, 1920, 1080, 3)
    nf = 0 if clips_only else len(F)
    enc = None if clips_only else subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','24','-i','-','-c:v','libx264','-crf','13','-pix_fmt','yuv420p',f'sync/{n}.mp4'], stdin=subprocess.PIPE)
    for s in ([] if clips_only else src):
        f = min(max(s * 24, 0), nf - 1.001); i = int(f); a = f - i
        enc.stdin.write(np.ascontiguousarray(F[i] if a < .02 else (F[i] * (1 - a) + F[i + 1] * a).astype(np.uint8)).tobytes())
    if enc: enc.stdin.close(); enc.wait()
    # pista de diálogo de la toma, armada muestra por muestra (48 kHz estéreo)
    SR = 48000; L = int(len(T) / 24 * SR); trk = np.zeros((L, 2), np.float32)
    for (f, a0, a1, at) in clips:
        pcm = np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ss',f'{a0:.3f}','-to',f'{a1:.3f}','-ac','2','-ar',str(SR),'-f','f32le','-'], stdout=subprocess.PIPE).stdout, np.float32).reshape(-1, 2).copy()
        fi, fo = int(.04 * SR), int(.08 * SR)
        pcm[:fi] *= np.linspace(0, 1, fi)[:, None]; pcm[-fo:] *= np.linspace(1, 0, fo)[:, None]
        p = int(round(at * SR))
        if p < 0: pcm = pcm[-p:]; p = 0
        e = min(L, p + len(pcm))
        if e > p: trk[p:e] += pcm[:e - p]
    subprocess.run(['ffmpeg','-loglevel','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-c:a','pcm_s16le',f'sync/{n}.wav'], input=np.clip(trk, -1, 1).tobytes(), check=True)
    print(n, f'{D:.2f}->{len(T)/24:.2f}s', 'vel', round(spd.min(), 2), round(spd.max(), 2))
