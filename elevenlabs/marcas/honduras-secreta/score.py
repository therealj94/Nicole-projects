import json, sys
norm = lambda s: s.lower().strip('¡!¿?,.').replace('hey', 'ey')
ORDER = ['ey', 'querés', 'conocer', 'secreto', 'honduras', 'bienvenidos', 'copán', 'ruinas']
def times(f, fix_ey=None):
    ws = [w for w in json.load(open(f))['words'] if w['type'] == 'word']; d = {}
    for w in ws:
        k = norm(w['text'])
        if k in ORDER and k not in d: d[k] = w['start']
    if 'ey' not in d and fix_ey is not None: d['ey'] = d['querés'] - fix_ey
    return d, ws[-1]['end']
def plan(jf, vf, vmax, ey_gap):
    j, jend = times(jf); v, _ = times(vf, ey_gap)
    ks = [k for k in ORDER if k in j and k in v]
    sp = [(v[b] - v[a]) / max(j[b] - j[a], 1e-3) for a, b in zip(ks, ks[1:])]
    # tramo final: después de "ruinas" el video avanza a velocidad 1 hasta que acabe la voz
    tail_v = v['ruinas'] + (jend - j['ruinas'])
    ok = tail_v <= vmax and v[ks[0]] - j[ks[0]] >= 0
    return ks, sp, ok, j, v, jend
if __name__ == '__main__':
    for i in range(1, 9):
        for name, vf, vmax, gap in [('H', 'veo_h.json', 7.9, .55), ('V', 'veo_v.json', 6.95, .46)]:
            try:
                ks, sp, ok, j, v, jend = plan(f'j{i}.json', vf, vmax, gap)
                print(f'j{i} {name} min={min(sp):.2f} max={max(sp):.2f} ok={ok} dur={jend:.2f}', [round(x, 2) for x in sp])
            except Exception as e: print(f'j{i} {name} ERR {e}')
