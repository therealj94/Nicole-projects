#!/usr/bin/env python3
"""Editor de video (ffmpeg) para piezas de marca.

  info      Ver datos del video          edit.py info in.mp4
  cut       Recortar tramo               edit.py cut in.mp4 -o out.mp4 --start 3 --end 18.5
  vertical  Reencuadrar a 9:16/1:1/16:9  edit.py vertical in.mp4 -o out.mp4 [--ar 9:16] [--mode crop|blur]
  concat    Unir clips                   edit.py concat a.mp4 b.mp4 c.mp4 -o out.mp4
  voice     Poner voz en off             edit.py voice in.mp4 voz.mp3 -o out.mp4 [--keep 0.15] [--at 0.5]
  music     Música de fondo con ducking  edit.py music in.mp4 musica.mp3 -o out.mp4 [--vol 0.25]
  sfx       Insertar efecto en segundo X edit.py sfx in.mp4 fx.mp3 -o out.mp4 --at 2.0 [--vol 1]
  subs      Quemar subtítulos (SRT)      edit.py subs in.mp4 subs.srt -o out.mp4 [--font Montserrat] [--size 16] [--color FFFFFF]
  logo      Marca de agua / logo         edit.py logo in.mp4 logo.png -o out.mp4 [--pos tr] [--scale 0.18] [--opacity 0.9]
  text      Texto en pantalla            edit.py text in.mp4 "OFERTA 20%" -o out.mp4 --start 1 --end 4 [--pos center]
  speed     Cambiar velocidad            edit.py speed in.mp4 -o out.mp4 --x 1.25
  fade      Fundido entrada/salida       edit.py fade in.mp4 -o out.mp4 [--d 0.6]
  loud      Normalizar audio (redes)     edit.py loud in.mp4 -o out.mp4
  export    Export final redes           edit.py export in.mp4 -o out.mp4 [--preset reels|youtube|square]
"""
import argparse, json, os, subprocess, sys, tempfile

ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
       "-movflags", "+faststart"]
AR = {"9:16": (1080, 1920), "1:1": (1080, 1080), "4:5": (1080, 1350), "16:9": (1920, 1080)}


def run(cmd):
    print(" ".join(cmd), file=sys.stderr)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + cmd, check=True)


def probe(f):
    j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", f]))
    return j


def has_audio(f):
    return any(s["codec_type"] == "audio" for s in probe(f)["streams"])


def dur(f):
    return float(probe(f)["format"]["duration"])


def pos_xy(pos, m=40):
    return {"tl": (f"{m}", f"{m}"), "tr": (f"W-w-{m}", f"{m}"), "bl": (f"{m}", f"H-h-{m}"),
            "br": (f"W-w-{m}", f"H-h-{m}"), "center": ("(W-w)/2", "(H-h)/2")}[pos]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    a = s.add_parser("info"); a.add_argument("i")
    a = s.add_parser("cut"); a.add_argument("i"); a.add_argument("-o", required=True)
    a.add_argument("--start", type=float, default=0); a.add_argument("--end", type=float)
    a = s.add_parser("vertical"); a.add_argument("i"); a.add_argument("-o", required=True)
    a.add_argument("--ar", default="9:16"); a.add_argument("--mode", default="crop", choices=["crop", "blur"])
    a = s.add_parser("concat"); a.add_argument("i", nargs="+"); a.add_argument("-o", required=True)
    a = s.add_parser("voice"); a.add_argument("i"); a.add_argument("a"); a.add_argument("-o", required=True)
    a.add_argument("--keep", type=float, default=0.15, help="volumen del audio original"); a.add_argument("--at", type=float, default=0)
    a = s.add_parser("music"); a.add_argument("i"); a.add_argument("a"); a.add_argument("-o", required=True)
    a.add_argument("--vol", type=float, default=0.25)
    a = s.add_parser("sfx"); a.add_argument("i"); a.add_argument("a"); a.add_argument("-o", required=True)
    a.add_argument("--at", type=float, required=True); a.add_argument("--vol", type=float, default=1.0)
    a = s.add_parser("subs"); a.add_argument("i"); a.add_argument("srt"); a.add_argument("-o", required=True)
    a.add_argument("--font", default="DejaVu Sans"); a.add_argument("--size", type=int, default=16)
    a.add_argument("--color", default="FFFFFF"); a.add_argument("--margin", type=int, default=60)
    a = s.add_parser("logo"); a.add_argument("i"); a.add_argument("logo"); a.add_argument("-o", required=True)
    a.add_argument("--pos", default="tr"); a.add_argument("--scale", type=float, default=0.18); a.add_argument("--opacity", type=float, default=0.9)
    a = s.add_parser("text"); a.add_argument("i"); a.add_argument("t"); a.add_argument("-o", required=True)
    a.add_argument("--start", type=float, default=0); a.add_argument("--end", type=float, default=9999)
    a.add_argument("--pos", default="center"); a.add_argument("--size", type=int, default=64)
    a.add_argument("--color", default="white"); a.add_argument("--box", default="black@0.45"); a.add_argument("--fontfile")
    a = s.add_parser("speed"); a.add_argument("i"); a.add_argument("-o", required=True); a.add_argument("--x", type=float, required=True)
    a = s.add_parser("fade"); a.add_argument("i"); a.add_argument("-o", required=True); a.add_argument("--d", type=float, default=0.6)
    a = s.add_parser("loud"); a.add_argument("i"); a.add_argument("-o", required=True)
    a = s.add_parser("export"); a.add_argument("i"); a.add_argument("-o", required=True)
    a.add_argument("--preset", default="reels", choices=["reels", "youtube", "square"])
    x = p.parse_args()

    if x.cmd == "info":
        j = probe(x.i)
        for st in j["streams"]:
            if st["codec_type"] == "video":
                print(f"video {st['width']}x{st['height']} {st.get('r_frame_rate')} {st['codec_name']}")
            else:
                print(f"audio {st['codec_name']} {st.get('sample_rate')}Hz")
        print(f"duración {float(j['format']['duration']):.2f}s  tamaño {int(j['format']['size'])/1e6:.1f}MB")

    elif x.cmd == "cut":
        c = ["-ss", str(x.start)] + (["-to", str(x.end)] if x.end else [])
        run(["-i", x.i] + c + ENC + [x.o])

    elif x.cmd == "vertical":
        W, H = AR[x.ar]
        if x.mode == "crop":
            vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
            run(["-i", x.i, "-vf", vf] + ENC + [x.o])
        else:
            fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:5[bg];"
                  f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[v]")
            run(["-i", x.i, "-filter_complex", fc, "-map", "[v]", "-map", "0:a?"] + ENC + [x.o])

    elif x.cmd == "concat":
        W, H = (lambda v: (v["width"], v["height"]))(next(st for st in probe(x.i[0])["streams"] if st["codec_type"] == "video"))
        ins, fc = [], ""
        for k, f in enumerate(x.i):
            ins += ["-i", f]
            fc += f"[{k}:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v{k}];"
            if has_audio(f):
                fc += f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo[a{k}];"
            else:
                fc += f"anullsrc=r=48000:cl=stereo,atrim=0:{dur(f)}[a{k}];"
        fc += "".join(f"[v{k}][a{k}]" for k in range(len(x.i))) + f"concat=n={len(x.i)}:v=1:a=1[v][a]"
        run(ins + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]"] + ENC + [x.o])

    elif x.cmd == "voice":
        d = int(x.at * 1000)
        if has_audio(x.i):
            fc = f"[0:a]volume={x.keep}[o];[1:a]adelay={d}|{d}[v];[o][v]amix=inputs=2:duration=first:normalize=0[a]"
        else:
            fc = f"[1:a]adelay={d}|{d},apad[a]"
        run(["-i", x.i, "-i", x.a, "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-shortest"] + ENC + [x.o])

    elif x.cmd == "music":
        D = dur(x.i)
        mus = f"[1:a]aloop=loop=-1:size=2e9,atrim=0:{D},volume={x.vol},afade=t=out:st={max(D-1.5,0)}:d=1.5[m]"
        if has_audio(x.i):
            fc = (mus + ";[0:a]asplit=2[v1][v2];[m][v2]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];"
                  "[v1][md]amix=inputs=2:duration=first:normalize=0[a]")
        else:
            fc = mus.replace("[m]", "[a]")
        run(["-i", x.i, "-i", x.a, "-filter_complex", fc, "-map", "0:v", "-map", "[a]"] + ENC + [x.o])

    elif x.cmd == "sfx":
        d = int(x.at * 1000)
        fc = f"[1:a]volume={x.vol},adelay={d}|{d}[s];"
        fc += "[0:a][s]amix=inputs=2:duration=first:normalize=0[a]" if has_audio(x.i) else "[s]apad[a]"
        run(["-i", x.i, "-i", x.a, "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-shortest"] + ENC + [x.o])

    elif x.cmd == "subs":
        style = (f"FontName={x.font},FontSize={x.size},PrimaryColour=&H00{x.color[4:6]}{x.color[2:4]}{x.color[0:2]},"
                 f"OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,Bold=1,Alignment=2,MarginV={x.margin}")
        srt = x.srt.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        run(["-i", x.i, "-vf", f"subtitles='{srt}':force_style='{style}'"] + ENC + [x.o])

    elif x.cmd == "logo":
        px, py = pos_xy(x.pos)
        fc = (f"[1:v][0:v]scale2ref=w=main_w*{x.scale}:h=ow/mdar[l][b];[l]format=rgba,colorchannelmixer=aa={x.opacity}[lo];"
              f"[b][lo]overlay={px}:{py}[v]")
        run(["-i", x.i, "-i", x.logo, "-filter_complex", fc, "-map", "[v]", "-map", "0:a?"] + ENC + [x.o])

    elif x.cmd == "text":
        px, py = {"center": ("(w-text_w)/2", "(h-text_h)/2"), "top": ("(w-text_w)/2", "h*0.12"),
                  "bottom": ("(w-text_w)/2", "h*0.80")}[x.pos]
        t = x.t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’")
        ff = f"fontfile='{x.fontfile}':" if x.fontfile else ""
        vf = (f"drawtext={ff}text='{t}':fontsize={x.size}:fontcolor={x.color}:box=1:boxcolor={x.box}:boxborderw=24:"
              f"x={px}:y={py}:enable='between(t,{x.start},{x.end})'")
        run(["-i", x.i, "-vf", vf] + ENC + [x.o])

    elif x.cmd == "speed":
        at, r = [], x.x
        while r > 2: at.append("atempo=2"); r /= 2
        while r < 0.5: at.append("atempo=0.5"); r /= 0.5
        at.append(f"atempo={r}")
        args = ["-i", x.i, "-vf", f"setpts=PTS/{x.x}"]
        if has_audio(x.i): args += ["-af", ",".join(at)]
        run(args + ENC + [x.o])

    elif x.cmd == "fade":
        D = dur(x.i); st = max(D - x.d, 0)
        args = ["-i", x.i, "-vf", f"fade=t=in:d={x.d},fade=t=out:st={st}:d={x.d}"]
        if has_audio(x.i): args += ["-af", f"afade=t=in:d={x.d},afade=t=out:st={st}:d={x.d}"]
        run(args + ENC + [x.o])

    elif x.cmd == "loud":
        run(["-i", x.i, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", x.o])

    elif x.cmd == "export":
        W, H = {"reels": (1080, 1920), "youtube": (1920, 1080), "square": (1080, 1080)}[x.preset]
        vf = f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps=30,setsar=1"
        args = ["-i", x.i, "-vf", vf]
        if has_audio(x.i): args += ["-af", "loudnorm=I=-14:TP=-1.5:LRA=11"]
        run(args + ["-b:v", "12M", "-maxrate", "16M", "-bufsize", "24M"] + ENC + [x.o])


if __name__ == "__main__":
    main()
