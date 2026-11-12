E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, VERTICAL 9:16 portrait frame for a phone screen. Soft rounded shapes, expressive faces. NOT realistic. No text, letters or numbers anywhere except the macaw's hat patch. Keep the TOP 15% of the frame free of faces (sky, wall or background there)."
G="the young teenage cartoon macaw exactly as in the macaw references: oversized head, big round glossy eyes, red body, two FEATHERED WINGS with yellow and blue feathers (wings are wings: no hands, no fingers, no claws on the wings), exactly TWO feet at the bottom of the body, the SAME beige bucket hat with the rectangular 'HONDURAS Secreta' patch facing the camera"
K="Kevin exactly as in his reference (10-year-old Honduran boy, spiky black hair, gap-tooth smile, blue long-sleeve shirt, denim shorts, colorful sneakers)"
R="the living stone Maya king statue exactly as in his reference (greenish-gray carved stone with moss, tall round carved feathered headdress, jade ear spools, ceremonial bar, kind golden glowing eyes)"
S="the small living stone Maya scribe statue exactly as in his reference (seated cross-legged, gray stone with moss, headband, stone paintbrush and shell ink pot, big kind eyes)"
Q="the two living stone macaw heads exactly as in their reference (carved gray-green stone macaw heads with big beaks and round cartoon eyes) sitting on top of a carved stone wall"
CP="the Maya archaeological site of Copán Ruinas, Honduras: grassy plaza, carved stone stelae, stepped stone pyramids, big ceiba trees, green hills"
RG="ref/jose_ref.png"; RC="ref/jose_ref_close.png"
g(){ o=$1; p=$2; shift 2; [ -s p1b/sf/$o.png ] && return; python3 $E image "$ST $p" -o p1b/sf/$o.png --model gemini-3.1-flash-image --ar 9:16 --res 2K "$@" > p1b/sf/$o.log 2>&1; }
b1(){
g A1 "Afternoon, a humble Honduran kid's bedroom. Medium close shot: $K lies on his back on his bed, bored, looking at the ceiling, an open blank notebook on a small table in front. Behind him, far in the background, an open window with the macaw sitting on the sill, small. The macaw's beak is closed." --ref ref/kevin_c.png --ref $RG &
g A2 "Afternoon. Close-up from inside the bedroom: $G sits on the open window sill, both wings folded at its sides, both feet gripping the sill, leaning forward with a mischievous grin. Colorful village street behind. Blue sky at the top." --ref $RG --ref $RC &
g C1 "Golden sunset, Great Plaza of $CP. Medium shot: $K stands with his hands in his pockets, bored, looking up at something off-screen. Next to him $G stands on the grass with wings folded, beak closed. Behind them, softly blurred, a tall carved stone stela." --ref ref/kevin_c.png --ref $RG &
g C2 "Golden sunset, Great Plaza of $CP. Low-angle shot from below: $R stands on his stone base, filling the frame, golden light cracks glowing on the stone, dust falling, eyes just opened, smiling down at the camera. Sky above his headdress. No other characters." --ref ref/rey.png &
wait; }
b2(){
g D1 "Sunset, $CP. Close-up: $K peeks out from behind a big stone, confused and a bit scared, one eyebrow raised. No other characters visible." --ref ref/kevin_c.png &
g D2 "Sunset, $CP. Close-up: $G standing on the grass, wings folded, looking up with a funny concentrated face, about to try to say a difficult word. Stelae behind, sky at top." --ref $RG --ref $RC &
g E "Sunset, $CP. Medium shot: $R bends down kindly toward the camera with one open stone hand inviting, warm smile. Behind him pyramids and sky. No other characters." --ref ref/rey.png &
g F2 "Dusk, $CP. Close-up: $K kneeling beside a carved stone altar, eyes wide in amazement, mouth closed, golden glow on his face from the altar. No other characters." --ref ref/kevin_c.png &
wait; }
b3(){
g G1 "Dusk, the Maya ball court of $CP. Close shot: $Q, smiling happily with closed beaks, little stone dust falling. Sky and trees at the top." --ref ref/guacas.png &
g G2 "Dusk, the ball court of $CP. Close-up: $G standing on the stone floor, wings folded, looking up with an amazed, moved face, beak closed. Sloped stone wall behind." --ref $RG --ref $RC &
g G3 "Dusk, the ball court of $CP. Medium close shot: $R stands beside the sloped stone wall, looking at the camera with a warm proud smile, mouth closed. No other characters." --ref ref/rey.png &
g H1 "Dusk, the ball court of $CP. Medium shot: $R raises both stone arms cheering, mouth closed for now. No other characters." --ref ref/rey.png &
wait; }
b4(){
g H2 "Dusk, the ball court of $CP. $K stands alone in the center of the stone court holding a big dark solid rubber ball, determined face, ready to hit it with his hip. A carved stone ring high on the sloped wall behind him. No other characters." --ref ref/kevin_c.png &
g I "Blue hour, the Hieroglyphic Stairway of $CP: steep stone staircase covered in softly glowing golden carved glyphs. In the center $S sits on a step and looks at the camera with a mysterious wise half smile, mouth closed. In the lower foreground, $K and $G stand side by side seen from the back three-quarters looking up at him; the macaw has its wings folded and its hat patch is NOT visible from behind. Both mouths closed." --ref ref/escriba.png --ref ref/kevin_c.png --ref $RG &
wait; }
