E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, VERTICAL 9:16 portrait frame for a phone screen. Soft rounded shapes, expressive faces. NOT realistic. No text, letters or numbers anywhere except the macaw's hat patch. Keep the TOP 15% of the frame free of faces (sky, wall or background there)."
G="the young teenage cartoon macaw exactly as in the macaw references: oversized head, big round glossy eyes, red body, two FEATHERED WINGS with yellow and blue feathers (wings are wings: no hands, no fingers, no claws on the wings), exactly TWO feet at the bottom of the body, the SAME beige bucket hat with the rectangular 'HONDURAS Secreta' patch facing the camera"
K="Kevin exactly as in his reference (10-year-old Honduran boy, spiky black hair, gap-tooth smile, blue long-sleeve shirt, denim shorts, colorful sneakers)"
R="the living stone Maya king statue exactly as in his reference (greenish-gray carved stone with moss, tall round carved feathered headdress, jade ear spools, ceremonial bar, kind golden glowing eyes)"
S="the small living stone Maya scribe statue exactly as in his reference (seated cross-legged, gray stone with moss, headband, stone paintbrush and shell ink pot, big kind eyes)"
Q="the two living stone macaw heads exactly as in their reference (carved gray-green stone macaw heads with big beaks and round cartoon eyes) sitting on top of a carved stone wall"
CP="the Maya archaeological site of Copán Ruinas, Honduras: grassy plaza, carved stone stelae, stepped stone pyramids, big ceiba trees, green hills"
RG="ref/jose_ref.png"; RC="ref/jose_ref_close.png"
g(){ o=$1; p=$2; shift 2; [ -s ep2/mb/$o.png ] && return; python3 $E image "$ST $p" -o ep2/mb/$o.png --model gemini-3.1-flash-image --ar 9:16 --res 2K "$@" > ep2/mb/$o.log 2>&1; }
LE="the living bronze monument statue of Lempira exactly as in his reference (dark bronze with green patina, long hair, feathered headband, cotton tunic and cape, tall staff, kind wise eyes)"
CA="the living Lenca clay pot exactly as in her reference (reddish terracotta with white and black painted patterns, little clay handle arms, painted cartoon face, small straw ring on top)"
GR="the colonial town of Gracias, Lempira, Honduras: white adobe houses with red clay tile roofs, cobblestone streets, a white colonial church, green pine mountains behind"
e1(){
g 01 "Afternoon, Kevin's bedroom. Close-up: $K holds up a Honduran one-lempira banknote (no readable text) close to his face, puzzled, one eyebrow raised. The macaw small on the window sill behind him, beak closed." --ref ref/kevin_c.png --ref ref/jose_ref.png &
g 02 "Golden afternoon in $GR. $K walks down a cobblestone street with his backpack, looking around amazed; $G flies above him. A colonial white fort with cannons on a hill in the distance." --ref ref/kevin_c.png --ref ref/jose_ref.png &
g 03 "Sunset in the central park of $GR. $LE stands on his stone pedestal, golden light cracks glowing on the bronze, eyes just opening, a kind smile. In the lower part $K and $G look up amazed, mouths closed." --ref ref/lempira_c.png --ref ref/kevin_c.png --ref ref/jose_ref.png &
g 04 "Sunset. Close-up: $LE looking down kindly at the camera with a proud warm smile, golden sky behind. No other characters." --ref ref/lempira_c.png &
g 05 "Night on top of a high rocky mountain fortress (the Peñol de Cerquín, Lempira, Honduras) under a starry sky; below, many small villages with warm fires glowing across the pine mountains. $LE stands pointing to the villages; $K sits on a rock listening amazed; $G sits beside him, wings folded." --ref ref/lempira_c.png --ref ref/kevin_c.png --ref ref/jose_ref.png &
wait; }
e2(){
g 06 "Night, a cozy rustic Lenca pottery workshop in La Campa, Honduras, with shelves of traditional painted clay pots, warm lamplight. In the center $CA has just come alive on a wooden table, smiling chatty with her little handle arms open; $K and $G look at her surprised." --ref ref/cantaro_c.png --ref ref/kevin_c.png --ref ref/jose_ref.png &
g 07 "Night, the same pottery workshop. Close-up: $CA proudly showing her painted patterns, winking. No other characters." --ref ref/cantaro_c.png &
g 08 "Night in a Lenca village square with colorful paper flags and candles: a magical ghostly-golden procession of the Guancasco tradition, people with carved wooden masks and banners walking peacefully from one village to meet another, embracing. $K and $G watch amazed next to $LE." --ref ref/lempira_c.png --ref ref/kevin_c.png --ref ref/jose_ref.png &
g 09 "Dawn over the pine mountains of Lempira, pink-orange sky. $LE kneels and puts a bronze hand on $K's shoulder, both smiling with emotion; $G sits on Kevin's other shoulder. The statue's feet are turning back to still bronze." --ref ref/lempira_c.png --ref ref/kevin_c.png --ref ref/jose_ref.png &
g 10 "Morning, Honduran school classroom. $K stands in front of the class proudly holding up a one-lempira banknote and pointing at it, explaining; the teacher exactly as in her reference smiles; classmates raise their hands curious." --ref ref/kevin_c.png --ref ref/maestra.png &
wait; }
e1; e2
