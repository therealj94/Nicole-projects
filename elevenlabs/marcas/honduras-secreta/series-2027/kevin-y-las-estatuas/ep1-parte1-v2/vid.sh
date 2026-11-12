E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, vertical 9:16, smooth expressive animation, characters exactly as in the first frame. The macaw has two feathered wings (no hands, no fingers, no claws on the wings) and only two feet, and always keeps its beige bucket hat with the patch. Stone statues move magically with small dust particles. One continuous shot, no cuts, no text on screen. ONLY ONE character speaks in this shot (the one described as speaking); every other character keeps the mouth completely closed. Dialogue in Spanish with a Honduran accent; say ONLY the quoted words."
NEG="realistic, photorealistic, text, letters, subtitles, captions, watermark, distorted face, extra limbs, hands on the macaw, four legs, claws on wings, second speaker, lip movement on listeners, extra dialogue, gibberish, morphing, characters disappearing, duplicated characters, camera cuts, flicker"
v(){ o=$1; d=$2; p=$3; [ -s p1b/vid/$o.mp4 ] && return; python3 $E video "$ST $p" -o p1b/vid/$o.mp4 --ar 9:16 --dur $d --res 4K --start p1b/sf/$o.png --neg "$NEG" > p1b/vid/$o.log 2>&1; }
mkdir -p p1b/vid
c1(){
v A1 6 "The bored boy on the bed stares at the ceiling and complains, lips moving: \"¿Y qué tiene de interesante un montón de piedras viejas?\" The macaw far in the window stays still, beak closed. Ambient: afternoon birds." &
v A2 6 "The macaw on the window sill grins and says, beak moving: \"¿Piedras? Agarrá la mochila, cipote... nos vamos a Copán.\" Then it opens its wings, ready to fly. Ambient: afternoon." &
v C1 4 "The bored boy looks up and says flatly, lips moving: \"Ajá... puras piedras.\" The macaw next to him keeps its beak closed and looks up too. Behind them a golden glow starts on the stela." &
v C2 8 "Golden cracks glow on the stone king, dust falls, he blinks, stretches his stone shoulders and, looking down at the camera with a grin, says majestically, his stone mouth moving: \"¿Piedras? ¡Soy Waxaklajuun Ub'aah K'awiil, decimotercer rey de Copán!\" He keeps exactly the same design. Sound: stone cracking, magical shimmer." &
v D1 4 "The boy peeking from behind the stone asks confused, lips moving: \"¿Waxa... qué?\" and tilts his head." &
wait; }
c2(){
v D2 6 "The macaw tries to pronounce a long name, beak moving, tongue-twisted: \"Wa... Waxa... Waxaklaju... ¡ay, se me trabó el pico!\" then shakes its head dizzy with its wings folded. Comedic." &
v E 6 "The stone king laughs warmly and says, his stone mouth moving: \"Me pueden decir Dieciocho Conejo. Vengan, les enseño mi reino.\" while gesturing with his open hand. The small macaw in the background keeps its beak closed. Sound: stone rumble." &
v F1 8 "The stone king points at the carved altar and explains proudly, his stone mouth moving: \"Aquí están los dieciséis reyes de Copán. El primero fundó la ciudad en el año cuatrocientos veintiséis.\" The tiny carved figures on the altar glow golden one by one." &
v F2 4 "The boy kneeling by the glowing altar says amazed, lips moving: \"¡Hace como mil seiscientos años!\" eyes sparkling." &
v G1 4 "The two stone macaw heads come alive, shake off dust and squawk happily together, beaks moving: \"¡Bienvenida, prima!\"" &
wait; }
c3(){
v G2 4 "The macaw looks up, moved, and asks softly, beak moving: \"¿Ustedes... son mis tatarabuelas?\" keeping its wings folded." &
v G3 6 "The stone king says warmly, his stone mouth moving: \"La guacamaya era sagrada para nosotros. Por eso cuidan la cancha.\" The macaw on the wall stays still with its beak closed." &
v H1 4 "The stone king cheers with both arms up and shouts encouragingly, his stone mouth moving: \"¡Con la cadera, no con las manos!\"" &
v H2 6 "The boy bumps the heavy rubber ball with his hip; the ball flies up and passes through the carved stone ring; he jumps celebrating and shouts, lips moving: \"¡Gooool... digo, punto!\" Sound: ball thud." &
v I 6 "Blue hour. The glyphs glow softly. The stone scribe slowly raises his brush and says in a mysterious whisper, his stone mouth moving: \"Y eso no es nada... ¿quieren ver un secreto?\" The boy and the macaw seen from behind stay still and look at each other, no mouths moving. The macaw stays in place the whole time. Sound: magical shimmer." &
wait; }
