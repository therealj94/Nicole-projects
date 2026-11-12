E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, vertical 9:16, smooth expressive animation, characters exactly as in the first frame. The macaw has two feathered wings (no hands, no fingers, no claws on the wings) and only two feet, and always keeps its beige bucket hat with the patch. Stone statues move magically with small dust particles. One continuous shot, no cuts, no text on screen. ONLY ONE character speaks in this shot (the one described as speaking); every other character keeps the mouth completely closed. Dialogue in Spanish with a Honduran accent; say ONLY the quoted words."
NEG="realistic, photorealistic, text, letters, subtitles, captions, watermark, distorted face, extra limbs, hands on the macaw, four legs, claws on wings, second speaker, lip movement on listeners, extra dialogue, gibberish, morphing, characters disappearing, duplicated characters, camera cuts, flicker"
v(){ o=$1; d=$2; p=$3; [ -s ep2/p1/vid/$o.mp4 ] && return; python3 $E video "$ST $p" -o ep2/p1/vid/$o.mp4 --ar 9:16 --dur $d --res 4K --start ep2/p1/sf/${4:-$o}.png --neg "$NEG" > ep2/p1/vid/$o.log 2>&1; }
ST="$ST The macaw's beak is a smooth bird beak with NO teeth. The bronze statue moves magically with golden glints."
NEG="$NEG, teeth in beak, human teeth, gums"
mkdir -p ep2/p1/vid
h1(){
v A1 4 "Close-up of the boy holding the red banknote; he looks at it puzzled and asks, lips moving: \"¿Y por qué el pisto se llama lempira?\"" &
v A2 6 "The macaw on the window sill grins and says, beak moving: \"¿No sabés? Agarrá la mochila... nos vamos a Gracias.\" then spreads its wings ready to fly." &
v B 6 "The macaw flies joyfully over the colonial street and says happily, beak moving: \"¡Bienvenido a Gracias, una de las ciudades más antiguas de Honduras!\" The boy below walks, mouth closed. Sound: wings flapping, town ambience." &
v C1 4 "Close-up of the boy, jaw dropped, pointing up, he shouts amazed, lips moving: \"¡Púchica! ¡Es el del billete!\"" &
v C2 8 "Golden cracks glow on the bronze statue, he blinks, stretches his shoulders, looks down at the camera with a calm smile and says proudly, his bronze mouth moving: \"Soy Lempira, señor de la sierra. Y sí... también el del billete.\" The small macaw on the church far behind stays still. Sound: metallic shimmer." &
wait; }
h2(){
v D 6 "The bronze Lempira looks at the camera warmly, gestures with his open hand inviting and says, his mouth moving: \"Vengan. Les voy a enseñar por qué mi gente nunca se rindió.\"" &
v E1 6 "Night on the mountain fortress. Lempira points at the glowing villages below and says solemnly, his bronze mouth moving: \"Desde aquí uní a muchos pueblos de la sierra para defender nuestra tierra.\" Sound: night wind, crickets." &
v E2 4 "Close-up of the boy hugging his knees on the rock, he asks softly and a bit worried, lips moving: \"¿Y no les daba miedo?\"" &
v E3 6 "Lempira, kneeling, smiles gently and says tenderly, his bronze mouth moving: \"Claro que sí. Pero juntos... el miedo se hace pequeño.\"" &
v F 6 "Night. The boy and the macaw stand still on the rock; suddenly they both turn their heads toward the dark trees on the right with wide surprised eyes; a small warm glow appears between the trees. Nobody on screen speaks, both mouths stay closed. Sound: crickets, a magical twinkle." &
wait; }
