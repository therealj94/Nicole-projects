#!/usr/bin/env python3
"""CLI ElevenLabs para producción de videos de marca.

Requiere la variable de entorno ELEVEN_API_KEY.

Comandos:
  tts      Texto -> voz            el.py tts "Hola" -o voz.mp3 [--voice ID] [--model eleven_v3]
  sfx      Efecto de sonido        el.py sfx "whoosh cinematográfico" -o fx.mp3 [--dur 3]
  music    Música                  el.py music "lo-fi elegante para marca de joyería" -o m.mp3 [--ms 30000] [--instrumental]
  v2m      Música desde video      el.py v2m video.mp4 -o m.mp3 [--desc "..."] [--sfx]
  stt      Transcribir / subtítulos el.py stt video.mp4 -o subs.srt [--lang es]
  isolate  Limpiar voz (quita ruido) el.py isolate audio.mp3 -o limpio.mp3
  dub      Doblaje a otro idioma   el.py dub video.mp4 --to en -o doblado.mp4
  image    Generar imagen          el.py image "prompt" -o img.png [--model gemini-3-pro-image] [--ar 9:16] [--ref foto.jpg]
  video    Generar video           el.py video "prompt" -o clip.mp4 [--model veo-3.1-generate-001] [--ar 9:16] [--dur 8] [--start img.png]
  avatar   Personaje hablando  el.py avatar cara.png voz.mp3 -o habla.mp4 [--res 720p]
  voices   Listar voces
"""
import argparse, base64, json, mimetypes, os, sys, time
import requests

B = "https://api.elevenlabs.io"
KEY = os.environ.get("ELEVEN_API_KEY") or os.environ.get("ELEVENLABS_API_KEY")
H = {"xi-api-key": KEY or ""}
DEFAULT_VOICE = "WuNBPlzQuFUTrVyyG1G3"  # Nelson | Warm Latin American Spanish Narrator


def die(r):
    sys.exit(f"Error {r.status_code}: {r.text[:800]}")


def save(r, out):
    if not r.ok:
        die(r)
    with open(out, "wb") as f:
        f.write(r.content)
    print(out)


def inline(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return {"type": "inline_base64", "mime_type": mime,
            "content_base64": base64.b64encode(open(path, "rb").read()).decode()}


def poll(kind, gid, out, every=8, timeout=1800):
    t0 = time.time()
    while time.time() - t0 < timeout:
        r = requests.get(f"{B}/v1/flows/{kind}/{gid}", headers=H)
        if not r.ok:
            die(r)
        j = r.json()
        st = j.get("status")
        if st == "completed":
            save(requests.get(j["content_url"]), out)
            return
        if st == "failed":
            sys.exit(f"Falló: {json.dumps(j)[:800]}")
        print(f"  {st}… {int(time.time()-t0)}s", file=sys.stderr)
        time.sleep(every)
    sys.exit("Timeout")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)

    a = s.add_parser("tts"); a.add_argument("text"); a.add_argument("-o", required=True)
    a.add_argument("--voice", default=DEFAULT_VOICE); a.add_argument("--model", default="eleven_v3")
    a.add_argument("--stability", type=float); a.add_argument("--style", type=float)
    a.add_argument("--speed", type=float); a.add_argument("--lang")

    a = s.add_parser("sfx"); a.add_argument("text"); a.add_argument("-o", required=True)
    a.add_argument("--dur", type=float); a.add_argument("--loop", action="store_true")

    a = s.add_parser("music"); a.add_argument("prompt"); a.add_argument("-o", required=True)
    a.add_argument("--ms", type=int, default=30000); a.add_argument("--instrumental", action="store_true")
    a.add_argument("--model", default="music_v2_5")

    a = s.add_parser("v2m"); a.add_argument("video"); a.add_argument("-o", required=True)
    a.add_argument("--desc"); a.add_argument("--sfx", action="store_true"); a.add_argument("--model", default="music_v2_5")

    a = s.add_parser("stt"); a.add_argument("file"); a.add_argument("-o", required=True)
    a.add_argument("--lang")

    a = s.add_parser("isolate"); a.add_argument("file"); a.add_argument("-o", required=True)

    a = s.add_parser("dub"); a.add_argument("file"); a.add_argument("--to", required=True)
    a.add_argument("--src", default="auto"); a.add_argument("-o", required=True)

    a = s.add_parser("image"); a.add_argument("prompt"); a.add_argument("-o", required=True)
    a.add_argument("--model", default="gemini-3-pro-image"); a.add_argument("--ar", default="9:16")
    a.add_argument("--res", default="2K"); a.add_argument("--ref", action="append", default=[])

    a = s.add_parser("video"); a.add_argument("prompt"); a.add_argument("-o", required=True)
    a.add_argument("--model", default="veo-3.1-generate-001"); a.add_argument("--ar", default="9:16")
    a.add_argument("--dur", type=int, default=8); a.add_argument("--res", default="1080p")
    a.add_argument("--start"); a.add_argument("--end"); a.add_argument("--no-audio", action="store_true")
    a.add_argument("--ref", action="append", default=[], help="imagen de referencia (sujeto/producto)")
    a.add_argument("--neg", help="prompt negativo (lo que el video debe evitar)")

    a = s.add_parser("avatar", help="imagen + audio -> personaje hablando (Creatify Aurora)")
    a.add_argument("image"); a.add_argument("audio"); a.add_argument("-o", required=True)
    a.add_argument("--res", default="720p"); a.add_argument("--guidance", type=float); a.add_argument("--audio-guidance", type=float)

    s.add_parser("voices")
    x = p.parse_args()
    if not KEY:
        sys.exit("Falta ELEVEN_API_KEY")

    if x.cmd == "tts":
        vs = {k: v for k, v in {"stability": x.stability, "style": x.style, "speed": x.speed}.items() if v is not None}
        body = {"text": x.text, "model_id": x.model}
        if vs: body["voice_settings"] = vs
        if x.lang: body["language_code"] = x.lang
        save(requests.post(f"{B}/v1/text-to-speech/{x.voice}?output_format=mp3_44100_192", headers=H, json=body), x.o)

    elif x.cmd == "sfx":
        body = {"text": x.text, "loop": x.loop, "model_id": "eleven_text_to_sound_v3"}
        if x.dur: body["duration_seconds"] = x.dur
        save(requests.post(f"{B}/v1/sound-generation", headers=H, json=body), x.o)

    elif x.cmd == "music":
        body = {"prompt": x.prompt, "music_length_ms": x.ms, "model_id": x.model, "force_instrumental": x.instrumental}
        save(requests.post(f"{B}/v1/music", headers=H, json=body), x.o)

    elif x.cmd == "v2m":
        data = {"model_id": x.model, "add_sfx": str(x.sfx).lower()}
        if x.desc: data["description"] = x.desc
        save(requests.post(f"{B}/v1/music/video-to-music", headers=H, data=data,
                           files=[("videos", open(x.video, "rb"))]), x.o)

    elif x.cmd == "stt":
        fmt = os.path.splitext(x.o)[1].lstrip(".").lower()
        data = {"model_id": "scribe_v2", "timestamps_granularity": "word", "diarize": "true"}
        if x.lang: data["language_code"] = x.lang
        if fmt in ("srt", "txt"):
            data["additional_formats"] = json.dumps([{"format": fmt, "max_characters_per_line": 32,
                                                      "max_segment_duration_s": 2.5}] if fmt == "srt" else [{"format": fmt}])
        r = requests.post(f"{B}/v1/speech-to-text", headers=H, data=data, files={"file": open(x.file, "rb")})
        if not r.ok and "scribe_v2" in r.text:
            data["model_id"] = "scribe_v1"
            r = requests.post(f"{B}/v1/speech-to-text", headers=H, data=data, files={"file": open(x.file, "rb")})
        if not r.ok: die(r)
        j = r.json()
        if fmt in ("srt", "txt") and j.get("additional_formats"):
            open(x.o, "w").write(j["additional_formats"][0]["content"])
        else:
            json.dump(j, open(x.o, "w"), ensure_ascii=False, indent=1)
        print(x.o)

    elif x.cmd == "isolate":
        save(requests.post(f"{B}/v1/audio-isolation", headers=H, files={"audio": open(x.file, "rb")}), x.o)

    elif x.cmd == "dub":
        r = requests.post(f"{B}/v1/dubbing", headers=H, files={"file": open(x.file, "rb")},
                          data={"target_lang": x.to, "source_lang": x.src, "watermark": "false", "highest_resolution": "true"})
        if not r.ok: die(r)
        did = r.json()["dubbing_id"]
        print("dubbing_id", did, file=sys.stderr)
        while True:
            st = requests.get(f"{B}/v1/dubbing/{did}", headers=H).json().get("status")
            print(" ", st, file=sys.stderr)
            if st == "dubbed": break
            if st == "failed": sys.exit("Doblaje falló")
            time.sleep(10)
        save(requests.get(f"{B}/v1/dubbing/{did}/audio/{x.to}", headers=H), x.o)

    elif x.cmd == "image":
        body = {"model_id": x.model, "prompt": x.prompt, "aspect_ratio": x.ar}
        if x.res and not x.model.startswith(("gpt-image-1", "gemini-2.5")): body["resolution"] = x.res
        if x.ref: body["images"] = [inline(f) for f in x.ref]
        r = requests.post(f"{B}/v1/flows/image", headers=H, json=body)
        if not r.ok: die(r)
        poll("image", r.json()["id"], x.o, every=4)

    elif x.cmd == "video":
        body = {"model_id": x.model, "prompt": x.prompt, "aspect_ratio": x.ar,
                "duration_secs": x.dur, "resolution": x.res, "generate_audio": not x.no_audio}
        if x.neg: body["negative_prompt"] = x.neg
        if x.start: body["start_frame"] = inline(x.start)
        if x.end: body["end_frame"] = inline(x.end)
        if x.ref:
            body["images"] = ([{"image": inline(f), "role": "subject"} for f in x.ref]
                              if x.model.startswith("veo") else [inline(f) for f in x.ref])
        r = requests.post(f"{B}/v1/flows/video", headers=H, json=body)
        if not r.ok: die(r)
        print("generation_id", r.json()["id"], file=sys.stderr)
        poll("video", r.json()["id"], x.o)

    elif x.cmd == "avatar":
        au = {"type": "inline_base64", "mime_type": "audio/wav" if x.audio.endswith(".wav") else "audio/mpeg",
              "content_base64": base64.b64encode(open(x.audio, "rb").read()).decode()}
        body = {"model_id": "creatify-aurora", "image": inline(x.image), "audio": au, "resolution": x.res}
        if x.guidance is not None: body["guidance_scale"] = x.guidance
        if x.audio_guidance is not None: body["audio_guidance_scale"] = x.audio_guidance
        r = requests.post(f"{B}/v1/flows/video", headers=H, json=body)
        if not r.ok: die(r)
        print("generation_id", r.json()["id"], file=sys.stderr)
        poll("video", r.json()["id"], x.o)

    elif x.cmd == "voices":
        r = requests.get(f"{B}/v2/voices?page_size=100", headers=H)
        for v in r.json()["voices"]:
            print(f"{v['voice_id']}  {v['name']}")


if __name__ == "__main__":
    main()
