E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, vertical 9:16, smooth expressive animation, characters exactly as in the first frame. The macaw has two feathered wings (no hands, no fingers, no claws on the wings) and only two feet, and always keeps its beige bucket hat with the patch. Stone statues move magically with small dust particles. One continuous shot, no cuts, no text on screen. ONLY ONE character speaks in this shot (the one described as speaking); every other character keeps the mouth completely closed. Dialogue in Spanish with a Honduran accent; say ONLY the quoted words."
NEG="realistic, photorealistic, text, letters, subtitles, captions, watermark, distorted face, extra limbs, hands on the macaw, four legs, claws on wings, second speaker, lip movement on listeners, extra dialogue, gibberish, morphing, characters disappearing, duplicated characters, camera cuts, flicker"
v(){ o=$1; d=$2; p=$3; [ -s p2/vid/$o.mp4 ] && return; python3 $E video "$ST $p" -o p2/vid/$o.mp4 --ar 9:16 --dur $d --res 4K --start p2/sf/${4:-$o}.png --neg "$NEG" > p2/vid/$o.log 2>&1; }
mkdir -p p2/vid
d1(){
v 01 8 "Blue hour. The stone scribe touches the carved glyphs with his brush and golden light flows up the stairway; he turns to the camera and says wisely, his stone mouth moving: \"Esta escalinata es el texto maya más largo que existe: más de dos mil glifos cuentan la historia de nuestros reyes.\" The boy and the macaw below keep their mouths closed, amazed." &
v 02 4 "Close-up of the boy, golden light on his face; he asks curiously, lips moving: \"¿Y vos lo sabés leer todo?\"" &
v 03 6 "Close-up of the stone scribe; he smiles mysteriously, puts a stone finger to his lips, then says softly, his stone mouth moving: \"Casi todo... algunos todavía son un secreto.\"" &
v 04 6 "The stone scribe paints floating glyphs of golden light in the air with his brush and says tenderly, his stone mouth moving: \"Así se escribiría tu nombre, Kevin.\" The boy watches with mouth closed, amazed." &
v K4 4 "Close-up of the boy laughing with delight at something glowing in front of him, then saying, lips moving: \"¡Está más bonito que mi firma!\"" 02 &
wait; }
d2(){
v K5a 4 "Close-up of the boy kneeling, embarrassed, scratching his head, saying, lips moving: \"Es que yo soy malo pa' la matemática...\"" K5 &
v 05 8 "The stone king draws dots, bars and a shell on the dirt with a stick, the marks glow golden; he explains patiently, his stone mouth moving: \"Un punto es uno, una barra es cinco... y esta concha es el cero.\" The boy and the macaw listen with mouths closed." &
v K5b 4 "Close-up of the boy kneeling; his face lights up with understanding and he says happily, lips moving: \"¡Ah, así sí entiendo!\"" K5 &
v 06 8 "In the golden tunnel, the stone scribe holds his glowing brush like a lantern and whispers proudly, his stone mouth moving: \"Este es Rosalila, un templo escondido dentro de la pirámide. Lo descubrió un arqueólogo hondureño en mil novecientos ochenta y nueve.\" The boy and the macaw walk behind him, mouths closed, amazed by the colorful temple." &
v G6 4 "Close-up of the macaw in the tunnel; it grins proudly and says, beak moving: \"¡Un catracho descubriendo secretos... como nosotros!\" keeping its wings folded." &
wait; }
d3(){
v 07 6 "Dawn. The stone king, with his hand on the boy's shoulder, says calmly and a bit sad, his stone mouth moving: \"Ya viene el sol. Tenemos que volver a ser piedra.\" The boy and the macaw listen with mouths closed." &
v K7 4 "Close-up of the boy at dawn, sad and moved; he asks softly, lips moving: \"¿Los voy a volver a ver?\"" &
v R7b 8 "Close-up of the stone king at dawn, looking down tenderly, saying wisely, his stone mouth moving: \"Cada vez que alguien nos visite y nos cuide, vamos a estar vivos. Copán es de todos, Kevin.\" As he finishes, golden light fades and he slowly turns back into still stone." &
v 08 6 "Classroom. The teacher holding a red pen looks at the boy's poster and says warmly and proudly, her lips moving: \"¡Excelente, Kevin! ¿Cómo aprendiste todo esto?\" The boy smiles with mouth closed; classmates applaud silently." &
v K8 4 "Close-up of the boy next to his poster; he smiles mischievously at the camera and says, lips moving: \"Digamos que... me lo contaron en persona.\" then winks." &
v 09 6 "Morning, the stone king stela is completely still stone; after a moment it gives a subtle playful wink with one stone eye; a real scarlet macaw flies across the blue sky. No dialogue. Sound: birds, a tiny magical chime." &
wait; }
