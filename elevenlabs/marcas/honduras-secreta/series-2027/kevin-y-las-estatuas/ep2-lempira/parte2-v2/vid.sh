E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, vertical 9:16, smooth expressive animation, characters exactly as in the first frame. The macaw has two feathered wings (no hands, no fingers, no claws on the wings) and only two feet, and always keeps its beige bucket hat with the patch. Stone statues move magically with small dust particles. One continuous shot, no cuts, no text on screen. ONLY ONE character speaks in this shot (the one described as speaking); every other character keeps the mouth completely closed. Dialogue in Spanish with a Honduran accent; say ONLY the quoted words."
NEG="realistic, photorealistic, text, letters, subtitles, captions, watermark, distorted face, extra limbs, hands on the macaw, four legs, claws on wings, second speaker, lip movement on listeners, extra dialogue, gibberish, morphing, characters disappearing, duplicated characters, camera cuts, flicker"
v(){ o=$1; d=$2; p=$3; [ -s ep2/p2b/vid/$o.mp4 ] && return; python3 $E video "$ST $p" -o ep2/p2b/vid/$o.mp4 --ar 9:16 --dur $d --res 4K --start ep2/p2b/sf/${4:-$o}.png --neg "$NEG" > ep2/p2b/vid/$o.log 2>&1; }
ST="$ST The macaw's beak is a smooth bird beak with NO teeth. The bronze statue moves magically with golden glints."
NEG="$NEG, teeth in beak, human teeth, gums"
NB=" No birds, no parrots, no macaws appear at any moment in this shot."
NEGB="$NEG, birds, parrots, macaws, extra animals"
w(){ o=$1; d=$2; p=$3; s=${4:-$1}; [ -s ep2/p2b/vid/$o.mp4 ] && return; python3 $E video "$ST $p$NB" -o ep2/p2b/vid/$o.mp4 --ar 9:16 --dur $d --res 4K --start ep2/p2b/sf/$s.png --neg "$NEGB" > ep2/p2b/vid/$o.log 2>&1; }
mkdir -p ep2/p2b/vid
k1(){
w S1 8 "Night street. The bronze Lempira walks toward the camera, looks back over his shoulder with an amused smile and says, his bronze mouth moving: \"Esa voz es de Doña Cántara. Vengan... y prepárense, porque habla más que un radio.\"" &
w C1 8 "In the pottery workshop, the living clay pot on the table opens her little handle arms and says cheerfully, her painted mouth moving: \"¡Por fin visitas! Soy de La Campa, donde las mujeres lencas hacen cántaros como yo desde hace siglos.\" Sound: crickets." &
w K2 4 "Close-up of the boy in the workshop; he leans forward curious and asks, lips moving: \"¿Y cómo los hacen?\"" &
w C2 8 "The living clay pot on the table proudly gestures with her handle arms and explains, her painted mouth moving: \"Sacamos el barro de la tierra, lo moldeamos a mano y lo quemamos en el fuego. Así lo aprendieron las abuelas de sus abuelas.\"" C1 &
v G3 4 "Close-up of the Honduras Secreta macaw on the table, the only bird in the scene; it tilts its head and asks, beak moving gently (smooth beak, no teeth): \"¿Y esos dibujos tan bonitos, doña Cántara?\" keeping its wings folded." G2 &
w C3 8 "Close-up of the living clay pot showing her painted patterns; she says, painted mouth moving: \"Cada línea cuenta algo de nuestro pueblo.\" then pauses, winks and adds playfully: \"Y no es por presumir... pero estoy bien chula.\"" &
wait; }
k2(){
w L4 8 "Night, Lenca village square. The bronze Lempira says proudly, his mouth moving: \"Esto es el Guancasco. Desde hace siglos, los pueblos lencas se visitan con sus santos y sus máscaras para hacer la paz.\" Behind him a golden procession of people with carved wooden masks walks peacefully. Sound: soft festive flutes." &
w K5 4 "Close-up of the boy at night; he asks, curious, lips moving: \"¿Y por qué tienen que hacer la paz?\"" &
w L5 8 "Night, village square. The bronze Lempira looks at the camera and answers wisely, his mouth moving: \"Porque un pueblo dividido es débil. Juntos se cuida la tierra, la cosecha y la familia.\"" L4 &
w K6 4 "Close-up of the boy at night; he laughs happily and says, lips moving: \"¡Como cuando uno se contenta con su alero!\"" K5 &
w L6 8 "Dawn. The bronze Lempira, kneeling, says tenderly, his mouth moving: \"Mi nombre está en la moneda para que nunca olviden algo: el valor de un pueblo está en su gente.\" The golden glow slowly fades from his bronze." &
w K7 6 "Close-up of the boy at dawn, moved, hand on his chest; he says, lips moving: \"Gracias, Lempira. Le voy a contar a todo el mundo.\"" &
wait; }
k3(){
v G8 4 "Close-up of the Honduras Secreta macaw on a rock at dawn, the only bird in the scene; it puffs its chest proudly and says, beak moving gently (smooth beak, no teeth): \"¡Y yo le ayudo, cipote!\"" &
w K9 8 "Classroom. The boy at the front holds up the red banknote and explains proudly to the class, lips moving: \"El lempira se llama así por un líder lenca que unió a los pueblos de la sierra para defender su tierra.\" Classmates listen silently." &
w M8 6 "Classroom. The teacher at her desk looks up with a proud smile and says warmly, her lips moving: \"¡Excelente, Kevin! ¿Y vos cómo sabés tanto de Lempira?\"" &
w K10 4 "Close-up of the boy holding the red banknote; he smiles mischievously at the camera and says, lips moving: \"Digamos que... me lo contó él mismo.\" then winks." K10 &
w W10 6 "Morning. The bronze Lempira statue stands completely still; after a moment he gives a subtle playful wink with one bronze eye. Sound: soft breeze, a tiny magical chime." &
wait; }
