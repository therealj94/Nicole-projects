# Kit de edición de video con ElevenLabs

Estado verificado el **2026-11-02** con la API key del entorno (`ELEVEN_API_KEY`).

## Cuenta

- Plan: **Enterprise**, activo. Uso: ~15M de 130,6M caracteres/créditos del ciclo.
- Clonación de voz instantánea y profesional habilitadas.
- 95 voces en la cuenta (ver [VOCES.md](VOCES.md)), casi todas profesionales y en español latino.
- Aviso: la cuenta muestra una **factura abierta** de USD 11.038,45 que requiere método de pago. Conviene revisarla para que no se corte el servicio.

## Servicios disponibles y probados

| Servicio | Comando | Modelos | Estado |
|---|---|---|---|
| Texto a voz | `el.py tts` | `eleven_v4`, `eleven_v4_turbo`, `eleven_v3` (por defecto, admite etiquetas como `[excited]`, `[whispers]`), `eleven_multilingual_v2`, `eleven_flash_v2_5` | ✅ |
| Efectos de sonido | `el.py sfx` | `eleven_text_to_sound_v3` | ✅ |
| Música | `el.py music` | `music_v2_5` (también v2 y v1) | ✅ |
| Música a partir del video | `el.py v2m` | `music_v2_5`, con SFX opcionales | disponible |
| Transcripción y subtítulos SRT | `el.py stt` | Scribe | ✅ |
| Limpieza de voz (quita ruido) | `el.py isolate` | Audio Isolation | disponible |
| Doblaje a otro idioma | `el.py dub` | Dubbing | disponible |
| Imagen (Eleven Creative) | `el.py image` | `gemini-3-pro-image` (por defecto), `gemini-3.1-flash-image`, `gpt-image-2`, `gpt-image-2.5-*`, `bytedance-seedream-5-*` | ✅ |
| Video (Eleven Creative) | `el.py video` | **`veo-3.1-generate-001`** (4/6/8 s, 9:16 o 16:9, hasta 4K, con audio) | ✅ |
| Avatar con lipsync | `el.py video --model creatify-aurora` | imagen + audio | disponible |

### Bloqueos (requieren aprobación de ElevenLabs o del administrador)

- `veo-3.1-fast-generate-001`: el modelo no está aprobado en el workspace.
- Modelos de video ByteDance (Seedance 2 / 2.5): requieren aprobación explícita de soporte.
- Studio API (proyectos largos o podcasts): la cuenta no está en la lista blanca. Hay que pedirlo a ventas.

## Editor (`edit.py`, ffmpeg)

`cut`, `vertical` (9:16, 1:1, 4:5 o 16:9; con recorte o fondo desenfocado), `concat`, `voice` (voz en off), `music` (música de fondo que baja cuando hay voz), `sfx`, `subs` (subtítulos quemados), `logo`, `text`, `speed`, `fade`, `loud` (normaliza a −14 LUFS, el nivel de las redes) y `export` (reels, youtube o square).

## Flujo típico de un reel de marca

```bash
python3 el.py tts "Guion..." -o voz.mp3 --voice WuNBPlzQuFUTrVyyG1G3
python3 el.py video "toma de producto..." -o clip.mp4 --start producto.png
python3 edit.py voice clip.mp4 voz.mp3 -o 1.mp4
python3 el.py stt voz.mp3 -o subs.srt --lang es
python3 edit.py subs 1.mp4 subs.srt -o 2.mp4
python3 el.py music "lujo, minimalista, cálido" -o m.mp3 --instrumental
python3 edit.py music 2.mp4 m.mp3 -o 3.mp4
python3 edit.py logo 3.mp4 logo.png -o 4.mp4
python3 edit.py export 4.mp4 -o FINAL.mp4 --preset reels
```

## Cómo pasarme el material

Por cada marca: logo en PNG transparente, colores en HEX, tipografía (.ttf/.otf), voz preferida y tono. Por cada video: los clips en bruto y el resultado que quieres (duración, formato, plataforma, guion o texto en pantalla, música). Guarda el material de cada marca en `marcas/<nombre>/`.


## Actualización 2026-11-04: herramientas disponibles

### Por API (lo que puedo usar directamente desde aquí)
| Área | Herramienta | Modelos / opciones | Estado en la cuenta |
|---|---|---|---|
| Voz | Texto a voz | `eleven_v4` (el más expresivo, 90+ idiomas), `eleven_v4_turbo`, `eleven_v3`, `eleven_multilingual_v2` | ✅ |
| Voz | **Diálogo** (`/v1/text-to-dialogue`) | varias voces en una sola toma, con efectos de audio | ✅ disponible |
| Voz | **Cambiador de voz** (`/v1/voice-changer`) | tu propia actuación grabada → voz de José, conservando la emoción | ✅ disponible |
| Voz | Efectos de voz (`/v1/audio-effects/catalog`) | radio, teléfono, robot, ambientes | ✅ |
| Efectos | Efectos de sonido | `eleven_text_to_sound_v3` (hasta ~30 s, en bucle) | ✅ |
| Música | Música | `music_v2_5`; plan de composición por secciones, letra, bucles, ambiente, **música a partir del video**, separación de pistas (stems), finetunes propios | ✅ |
| Video | Veo 3.1 | texto/imagen a video, cuadro inicial y final, 3 imágenes de referencia, 4/6/8 s, hasta 4K, con audio | ✅ |
| Video | Veo 3.1 Fast | igual, más barato | ❌ requiere aprobación del administrador |
| Video | Seedance 2 / 2.5 | hasta 30 imágenes y **10 videos de referencia**, sincronía labial con audio | ❌ ByteDance requiere aprobación de soporte |
| Video | Creatify Aurora | imagen + audio → personaje hablando | ❌ requiere aprobación |
| Imagen | GPT Image 2 / 2.5, Gemini 3 Pro / 3.1 Flash, Seedream 5 | edición con referencias, hasta 4K | ✅ (Seedream requiere aprobación) |

### Solo en la app web de ElevenLabs (no por API)
- **Kling 4.0**: texto e imagen a video de 3 a 30 s, 720p/1080p, 16:9 · 9:16 · 1:1 · 21:9, hasta 10 imágenes y 5 videos de referencia,
  cuadro inicial y final, y **edición de video** (cambiar personaje, quitar objetos, re-estilizar el fondo conservando el resto).
  No disponible para usuarios en Estados Unidos. Fuente: https://elevenlabs.io/video/kling-4
- También en la app: Sora 2 / 2 Pro, Runway Gen-4.5, Kling 3.0 / O3 Pro, Minimax H3, Seedance 2.5 Video Edit, **Topaz Upscale** (escalado).
