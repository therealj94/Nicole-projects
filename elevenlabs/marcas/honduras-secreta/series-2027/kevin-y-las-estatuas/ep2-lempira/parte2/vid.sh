E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, vertical 9:16, smooth expressive animation, characters exactly as in the first frame. The macaw has two feathered wings (no hands, no fingers, no claws on the wings) and only two feet, and always keeps its beige bucket hat with the patch. Stone statues move magically with small dust particles. One continuous shot, no cuts, no text on screen. ONLY ONE character speaks in this shot (the one described as speaking); every other character keeps the mouth completely closed. Dialogue in Spanish with a Honduran accent; say ONLY the quoted words."
NEG="realistic, photorealistic, text, letters, subtitles, captions, watermark, distorted face, extra limbs, hands on the macaw, four legs, claws on wings, second speaker, lip movement on listeners, extra dialogue, gibberish, morphing, characters disappearing, duplicated characters, camera cuts, flicker"
v(){ o=$1; d=$2; p=$3; [ -s ep2/p2/vid/$o.mp4 ] && return; python3 $E video "$ST $p" -o ep2/p2/vid/$o.mp4 --ar 9:16 --dur $d --res 4K --start ep2/p2/sf/${4:-$o}.png --neg "$NEG" > ep2/p2/vid/$o.log 2>&1; }
ST="$ST The macaw's beak is a smooth bird beak with NO teeth. The bronze statue moves magically with golden glints."
NEG="$NEG, teeth in beak, human teeth, gums"
mkdir -p ep2/p2/vid
j1(){
v C1 8 "In the pottery workshop, the living clay pot on the table opens her little handle arms and says cheerfully, her painted mouth moving: \"¡Por fin visitas! Soy de La Campa, donde las mujeres lencas hacen cántaros como yo desde hace siglos.\" Sound: night crickets." &
v G2 4 "Close-up of the macaw on the table; it tilts its head curiously and asks, beak moving gently (smooth beak, no teeth): \"¿Y esos dibujos?\"" &
v C3 8 "Close-up of the living clay pot proudly showing her painted patterns, she says, painted mouth moving: \"Cada línea cuenta algo de nuestro pueblo.\" then pauses, winks and adds playfully: \"Y no es por presumir... pero estoy bien chula.\"" &
v L4 6 "Night, Lenca village square. The bronze Lempira says proudly and calmly, his mouth moving: \"Esto es el Guancasco: dos pueblos se visitan para hacer la paz y celebrar juntos.\" Behind him the golden procession walks peacefully. Sound: soft festive music far away." &
v K5 4 "Close-up of the boy laughing happily, he says, lips moving: \"¡Como cuando uno se contenta con su alero!\"" &
wait; }
j2(){
v L6 8 "Dawn. The bronze Lempira, kneeling, says tenderly, his mouth moving: \"Mi nombre está en la moneda para que nunca olviden algo: el valor de un pueblo está en su gente.\" As he finishes, the golden glow fades and he becomes still bronze again." &
v K7 4 "Close-up of the boy at dawn, moved, hand on his chest; he says softly, lips moving: \"Gracias, Lempira.\"" &
v M8 6 "Classroom. The teacher sitting at her desk looks at the boy and asks warmly and surprised, her lips moving: \"¿Y vos cómo sabés tanto de Lempira?\" The boy holding the banknote smiles with his mouth closed; classmates are silent and curious." &
v K9 4 "Close-up of the boy holding the red banknote; he smiles mischievously at the camera and says, lips moving: \"Digamos que... me lo contó él mismo.\" then winks." &
v W10 5 "Morning. The bronze Lempira statue is completely still; after a moment he gives a subtle playful wink with one bronze eye; a real scarlet macaw flies across the blue sky. No dialogue. Sound: birds, a tiny magical chime." &
wait; }
