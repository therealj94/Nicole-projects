E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, VERTICAL 9:16 portrait frame for a phone screen. Soft rounded shapes, expressive faces. NOT realistic. No text, letters or numbers anywhere except the macaw's hat patch. Keep the TOP 15% of the frame free of faces (sky, wall or background there)."
G="the young teenage cartoon macaw exactly as in the macaw references: oversized head, big round glossy eyes, red body, two FEATHERED WINGS with yellow and blue feathers (wings are wings: no hands, no fingers, no claws on the wings), exactly TWO feet at the bottom of the body, the SAME beige bucket hat with the rectangular 'HONDURAS Secreta' patch facing the camera"
K="Kevin exactly as in his reference (10-year-old Honduran boy, spiky black hair, gap-tooth smile, blue long-sleeve shirt, denim shorts, colorful sneakers)"
R="the living stone Maya king statue exactly as in his reference (greenish-gray carved stone with moss, tall round carved feathered headdress, jade ear spools, ceremonial bar, kind golden glowing eyes)"
S="the small living stone Maya scribe statue exactly as in his reference (seated cross-legged, gray stone with moss, headband, stone paintbrush and shell ink pot, big kind eyes)"
Q="the two living stone macaw heads exactly as in their reference (carved gray-green stone macaw heads with big beaks and round cartoon eyes) sitting on top of a carved stone wall"
CP="the Maya archaeological site of Copán Ruinas, Honduras: grassy plaza, carved stone stelae, stepped stone pyramids, big ceiba trees, green hills"
RG="ref/jose_ref.png"; RC="ref/jose_ref_close.png"
g(){ o=$1; p=$2; shift 2; [ -s p2/mb/$o.png ] && return; python3 $E image "$ST $p" -o p2/mb/$o.png --model gemini-3.1-flash-image --ar 9:16 --res 2K "$@" > p2/mb/$o.log 2>&1; }
m1(){
g 01 "Blue hour, the Hieroglyphic Stairway of $CP. $S sits on a step and touches the carved glyphs with his stone brush: the glyphs light up in flowing golden light climbing the stairs. In the lower part, $K and $G look up in awe, mouths closed." --ref ref/escriba.png --ref ref/kevin_c.png --ref $RG &
g 02 "Night, $CP. Close-up: $K looking up curious, golden glyph light reflecting on his face, asking a question. No other characters." --ref ref/kevin_c.png &
g 03 "Night, $CP. Close-up: $S smiling mysteriously with a finger of stone over his lips as if keeping a secret, soft golden glyph light around him. Starry sky at top." --ref ref/escriba.png &
g 04 "Night, $CP. $S paints in the air with his glowing brush: three floating golden Maya-style glyphs of light hang in the air between him and $K, who stares at them amazed with sparkling eyes. Starry sky at top." --ref ref/escriba.png --ref ref/kevin_c.png &
g 05 "Night, the Great Plaza of $CP. $R kneels and draws Maya numbers on the dirt with a stick: dots, bars and a little shell shape for zero, glowing faintly golden. $K kneels across from him, delighted, understanding. $G watches from a stela, wings folded." --ref ref/rey.png --ref ref/kevin_c.png --ref $RG &
wait; }
m2(){
g 06 "A narrow ancient stone tunnel inside a Maya pyramid, lit by warm golden light; at the end of the tunnel a hidden temple painted bright red, green and yellow with large carved masks (the Rosalila temple of Copán). $S leads the way holding up his glowing brush like a lantern; $K and $G follow, amazed." --ref ref/escriba.png --ref ref/kevin_c.png --ref $RG &
g 07 "Dawn, the Great Plaza of $CP. Pink-orange sky on the horizon. $R stands on his base and gently puts his stone hand on the shoulder of $K, both smiling with emotion; $G sits on Kevin's shoulder, wings folded. The king's feet are starting to turn back into still stone." --ref ref/rey.png --ref ref/kevin_c.png --ref $RG &
g 08 "Morning, a bright Honduran elementary school classroom. $K stands proudly next to a big poster full of colorful drawings of Maya glyphs, Maya numbers and stone macaws; the teacher exactly as in her reference (40, glasses, light-blue cardigan) smiles holding a red pen. Classmates at desks." --ref ref/kevin_c.png --ref ref/maestra.png &
g 09 "Morning sun, the Great Plaza of $CP, tourists far away. Close-up of the stone king stela, now completely still stone again, giving a subtle playful wink to the camera with one stone eye. A real scarlet macaw flying in the blue sky at top." --ref ref/rey.png &
wait; }
m1; m2
