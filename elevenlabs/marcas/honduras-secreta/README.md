# Honduras Secreta: integración de José (guacamayo) en tomas de dron

1. `track.py VIDEO T X Y`: seguimiento de cámara de un punto del suelo (KLT + similitud). Salida: `track.json`.
2. `track_people.py VIDEO`: sigue a dos personas (camisa amarilla por color y otra persona por KLT). Salida: `people.json`.
3. `key_color.py clip_veo.mp4 out/f`: recorta el fondo liso de los clips de Veo (por color y por cuadro); `key.py` para fondos claros.
4. `comp2.py VIDEO salida.mp4 [segundos para vista previa]`: coloca a José entre las dos personas, con oclusión de flores, sombra,
   gradación igualada y grano. Salta el tramo 3.05–4.15 s del clip de Veo (la "mano" que dibujó la IA).

Animaciones de José: Veo 3.1 (`el.py video ... --start`) a partir del paquete de imágenes. Voz: "Jose latam" (5rpOswWClIYBLr0xKelj).
