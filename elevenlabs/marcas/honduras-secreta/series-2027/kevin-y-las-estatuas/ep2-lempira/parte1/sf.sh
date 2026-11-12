E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, VERTICAL 9:16 portrait frame for a phone screen. Soft rounded shapes, expressive faces. NOT realistic. No text, letters or numbers anywhere except the macaw's hat patch. Keep the TOP 15% of the frame free of faces (sky, wall or background there)."
G="the young teenage cartoon macaw exactly as in the macaw references: oversized head, big round glossy eyes, red body, two FEATHERED WINGS with yellow and blue feathers (wings are wings: no hands, no fingers, no claws on the wings), exactly TWO feet at the bottom of the body, the SAME beige bucket hat with the rectangular 'HONDURAS Secreta' patch facing the camera"
K="Kevin exactly as in his reference (10-year-old Honduran boy, spiky black hair, gap-tooth smile, blue long-sleeve shirt, denim shorts, colorful sneakers)"
R="the living stone Maya king statue exactly as in his reference (greenish-gray carved stone with moss, tall round carved feathered headdress, jade ear spools, ceremonial bar, kind golden glowing eyes)"
S="the small living stone Maya scribe statue exactly as in his reference (seated cross-legged, gray stone with moss, headband, stone paintbrush and shell ink pot, big kind eyes)"
Q="the two living stone macaw heads exactly as in their reference (carved gray-green stone macaw heads with big beaks and round cartoon eyes) sitting on top of a carved stone wall"
CP="the Maya archaeological site of Copán Ruinas, Honduras: grassy plaza, carved stone stelae, stepped stone pyramids, big ceiba trees, green hills"
RG="ref/jose_ref.png"; RC="ref/jose_ref_close.png"
g(){ o=$1; p=$2; shift 2; [ -s ep2/p1/sf/$o.png ] && return; python3 $E image "$ST $p" -o ep2/p1/sf/$o.png --model gemini-3.1-flash-image --ar 9:16 --res 2K "$@" > ep2/p1/sf/$o.log 2>&1; }
LE="the living bronze monument statue of Lempira exactly as in his reference (dark bronze with green patina, long hair, feathered headband, cotton tunic and cape, tall wooden-looking bronze staff, kind wise eyes)"
GR="the colonial town of Gracias, Lempira, Honduras: white adobe houses with red clay tile roofs, cobblestone streets, a white colonial church, green pine mountains"
PE="the top of a huge rocky mountain fortress in the pine-covered mountains of Lempira, Honduras, at night under a starry sky, small village fires glowing far below"
f1(){
g A1 "Afternoon, a humble Honduran kid's bedroom. Close-up: $K holds up a RED-ORANGE Honduran one-lempira banknote (no readable text, red tones, not green, not a dollar) near his face, puzzled, one eyebrow raised. No other characters." --ref ref/kevin_c.png &
g A2 "Afternoon. Close-up from inside the bedroom: $G sits on the open window sill, wings folded at its sides, both feet gripping the sill, mischievous grin with beak closed. Colorful village street behind, blue sky at the top." --ref ref/jose_ref.png --ref ref/jose_ref_close.png &
g B "Golden afternoon in $GR. Wide shot: $G flies happily over a cobblestone street, wings open; below, small, $K walks with his backpack looking around amazed. A white colonial fort on a hill in the background." --ref ref/jose_ref.png --ref ref/kevin_c.png &
g C1 "Sunset in a small colonial plaza of $GR. Close-up: $K with his jaw dropped and eyes wide, pointing up at something off-screen, golden light on his face. No other characters." --ref ref/kevin_c.png &
g C2 "Sunset in a small colonial plaza of $GR, white church behind. Low-angle: $LE stands on his stone pedestal, golden light cracks glowing on the bronze, eyes just opened, a calm kind smile, mouth closed. Sky at top. No other characters." --ref ref/lempira_c.png &
wait; }
f2(){
g D "Sunset. Close-up: $LE looking at the camera with a proud warm smile, mouth closed, one hand inviting, golden sky behind. No other characters." --ref ref/lempira_c.png &
g E1 "$PE. Medium shot: $LE stands on the edge of the rock pointing at the glowing villages below, mouth closed. No other characters in front." --ref ref/lempira_c.png &
g E2 "$PE. Close-up: $K sitting on a rock, hugging his knees, looking up a bit worried and curious, mouth closed. No other characters." --ref ref/kevin_c.png &
g E3 "$PE. Close-up: $LE kneeling down to eye level, looking at the camera with a gentle reassuring smile, mouth closed, stars behind. No other characters." --ref ref/lempira_c.png &
g F "$PE, darker. Medium shot: $K and $G stand side by side on the rock, both turning their heads toward the dark trees on the right with surprised wide eyes, mouths closed; the macaw has its wings folded. Something small glows faintly between the trees." --ref ref/kevin_c.png --ref ref/jose_ref.png &
wait; }
f1; f2
