# Luxury Bella Spa: plantilla de edición

Estilo: negro, dorado y marfil. Tipografías Cinzel, Cormorant Garamond, Great Vibes y Montserrat (Google Fonts).
Subtítulos en español **sobre la cabeza** (fuera de la zona del pie de publicación de Instagram). Gradación luminosa y cálida.

## Uso
```bash
CFG=v07_laser.py python3 render.py VIDEO.mp4 transcripcion.json fonts/ salida_sin_audio.mp4 [segundo_para_vista_previa]
```
- `render.py`: motor común (marco dorado, cabecera, subtítulos palabra por palabra, zoom dinámico, paneles de vidrio,
  tarjeta final, tomas de apoyo con la persona recortada al frente y efectos sobre el rostro y el fondo).
- `vNN_*.py`: textos, tiempos, paneles y efectos de cada video.
- La transcripción sale de `el.py stt` y la voz limpia de `el.py isolate`. La mezcla de audio se hace con ffmpeg
  (música con ducking, efectos y -14 LUFS).
- Modelos de segmentación y rostro (MediaPipe): `/tmp/x/selfie_multiclass.tflite` y `/tmp/x/face_landmarker.task`
  (se configuran con `SEG_MODEL` y `FACE_MODEL`).

## Videos entregados (2026-11)
| # | Config | Tema |
|---|---|---|
| 01 | v01_gracias.py | Agradecimiento a clientas + reseña en Google |
| 02 | v02_hombres.py | Skin care para hombres |
| 03 | v03_detras.py | Detrás de cada experiencia (3 tomas de apoyo) |
| 04 | v04_pausa.py | Mereces una pausa (CTA comentarios) |
| 05 | v05_led.py | Relajación, mascarillas, luz LED |
| 06 | v06b_acne_creativo.py | Acné: granitos con seguimiento facial, capas de la piel, tratamiento |
| 07 | v07_laser.py | Depilación láser: folículos, láser, tonos de piel, teléfono (631) 365-6004 |
