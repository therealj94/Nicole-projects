E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, VERTICAL 9:16 portrait frame for a phone screen. Soft rounded shapes, expressive faces. NOT realistic. No text, letters or numbers anywhere except the macaw's hat patch. Keep the TOP 15% of the frame free of faces (sky, wall or background there)."
G="the young teenage cartoon macaw exactly as in the macaw references: oversized head, big round glossy eyes, red body, two FEATHERED WINGS with yellow and blue feathers (wings are wings: no hands, no fingers, no claws on the wings), exactly TWO feet at the bottom of the body, the SAME beige bucket hat with the rectangular 'HONDURAS Secreta' patch facing the camera"
K="Kevin exactly as in his reference (10-year-old Honduran boy, spiky black hair, gap-tooth smile, blue long-sleeve shirt, denim shorts, colorful sneakers)"
R="the living stone Maya king statue exactly as in his reference (greenish-gray carved stone with moss, tall round carved feathered headdress, jade ear spools, ceremonial bar, kind golden glowing eyes)"
S="the small living stone Maya scribe statue exactly as in his reference (seated cross-legged, gray stone with moss, headband, stone paintbrush and shell ink pot, big kind eyes)"
Q="the two living stone macaw heads exactly as in their reference (carved gray-green stone macaw heads with big beaks and round cartoon eyes) sitting on top of a carved stone wall"
CP="the Maya archaeological site of Copán Ruinas, Honduras: grassy plaza, carved stone stelae, stepped stone pyramids, big ceiba trees, green hills"
RG="ref/jose_ref.png"; RC="ref/jose_ref_close.png"
g(){ o=$1; p=$2; shift 2; [ -s ep2/p2/sf/$o.png ] && return; python3 $E image "$ST $p" -o ep2/p2/sf/$o.png --model gemini-3.1-flash-image --ar 9:16 --res 2K "$@" > ep2/p2/sf/$o.log 2>&1; }
LE="the living bronze monument statue of Lempira exactly as in his reference (dark bronze with green patina, long hair, feathered headband, cotton tunic and cape, tall staff, kind wise eyes)"
CA="the living Lenca clay pot exactly as in her reference (reddish terracotta with white and black painted patterns, little clay handle arms, painted cartoon face, small straw ring on top)"
WS="a cozy rustic Lenca pottery workshop in La Campa, Honduras, at night, shelves full of traditional painted clay pots, warm lamplight"
g C1 "$WS. Medium shot: $CA stands on a wooden table, little handle arms open in welcome, mouth closed for now. No other characters." --ref ref/cantaro_c.png &
g G2 "$WS. Close-up: $G standing on the wooden table, wings folded, looking curiously at something off-screen with its head tilted, beak closed." --ref ref/jose_ref.png --ref ref/jose_ref_close.png &
g L4 "Night in a Lenca village square with candles and colorful paper flags; behind, softly blurred and glowing golden, a peaceful procession with carved wooden masks and banners. Medium shot: $LE standing in front, looking at the camera with a calm proud smile, mouth closed. No other characters in focus." --ref ref/lempira_c.png &
g K5 "Night in a Lenca village square with candles and colorful paper flags, a golden procession glowing softly behind. Close-up: $K laughing happily, mouth closed. No other characters in focus." --ref ref/kevin_c.png &
g L6 "Dawn over the pine mountains of Lempira, pink-orange sky. Close-up: $LE kneeling, looking at the camera tenderly, mouth closed, golden morning light on the bronze. No other characters." --ref ref/lempira_c.png &
g K7 "Dawn over the pine mountains of Lempira, pink-orange sky. Close-up: $K with emotional, slightly teary grateful eyes, mouth closed. No other characters." --ref ref/kevin_c.png &
g K9 "Morning, a bright Honduran school classroom. Close-up: $K standing proudly holding a red-orange Honduran one-lempira banknote (no readable text), smiling mischievously at the camera, mouth closed. No other characters in focus." --ref ref/kevin_c.png &
g W10 "Morning sun in a small colonial plaza of Gracias, Lempira, white church behind, blue sky. Close-up of the bronze Lempira statue standing still on his stone pedestal, about to wink. A real scarlet macaw flies in the sky." --ref ref/lempira_c.png &
wait
