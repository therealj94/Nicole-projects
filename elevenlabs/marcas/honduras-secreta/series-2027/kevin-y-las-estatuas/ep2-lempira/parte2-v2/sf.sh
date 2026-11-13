E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, VERTICAL 9:16 portrait frame for a phone screen. Soft rounded shapes, expressive faces. NOT realistic. No text, letters or numbers anywhere except the macaw's hat patch. Keep the TOP 15% of the frame free of faces (sky, wall or background there)."
G="the young teenage cartoon macaw exactly as in the macaw references: oversized head, big round glossy eyes, red body, two FEATHERED WINGS with yellow and blue feathers (wings are wings: no hands, no fingers, no claws on the wings), exactly TWO feet at the bottom of the body, the SAME beige bucket hat with the rectangular 'HONDURAS Secreta' patch facing the camera"
K="Kevin exactly as in his reference (10-year-old Honduran boy, spiky black hair, gap-tooth smile, blue long-sleeve shirt, denim shorts, colorful sneakers)"
R="the living stone Maya king statue exactly as in his reference (greenish-gray carved stone with moss, tall round carved feathered headdress, jade ear spools, ceremonial bar, kind golden glowing eyes)"
S="the small living stone Maya scribe statue exactly as in his reference (seated cross-legged, gray stone with moss, headband, stone paintbrush and shell ink pot, big kind eyes)"
Q="the two living stone macaw heads exactly as in their reference (carved gray-green stone macaw heads with big beaks and round cartoon eyes) sitting on top of a carved stone wall"
CP="the Maya archaeological site of Copán Ruinas, Honduras: grassy plaza, carved stone stelae, stepped stone pyramids, big ceiba trees, green hills"
RG="ref/jose_ref.png"; RC="ref/jose_ref_close.png"
g(){ o=$1; p=$2; shift 2; [ -s ep2/p2b/sf/$o.png ] && return; python3 $E image "$ST $p" -o ep2/p2b/sf/$o.png --model gemini-3.1-flash-image --ar 9:16 --res 2K "$@" > ep2/p2b/sf/$o.log 2>&1; }
LE="the living bronze monument statue of Lempira exactly as in his reference (dark bronze with green patina, long hair, feathered headband, cotton tunic and cape, tall staff, kind wise eyes)"
NB="There are NO birds, NO parrots, NO macaws anywhere in the image."
g S1 "Night, a cobblestone street of a Lenca village in the mountains, warm light coming from the open door of a small pottery workshop behind. Medium shot: $LE walking toward the camera, looking back over his shoulder with an amused smile, mouth closed. No other characters. $NB" --ref ref/lempira_c.png &
g K2 "Night, a cozy rustic Lenca pottery workshop with shelves of painted clay pots, warm lamplight. Close-up: $K leaning forward curious, eyes wide, mouth closed. No other characters. $NB" --ref ref/kevin_c.png &
g K5 "Night in a Lenca village square with candles and colorful paper flags, a golden procession glowing softly far behind. Close-up: $K looking up, curious and a bit confused, mouth closed. No other characters in focus. $NB" --ref ref/kevin_c.png &
g G8 "Dawn over the pine mountains of Lempira, pink-orange sky. Close-up: $G standing on a rock, wings folded, proud happy face, beak closed, its patch facing the camera." --ref ref/jose_ref.png --ref ref/jose_ref_close.png &
g K9 "Morning, a bright Honduran school classroom. $K stands at the front of the class next to the blackboard holding up a red-orange Honduran one-lempira banknote (no readable text) and explaining with an open hand, mouth closed; classmates at desks seen from behind. No teacher in the frame. $NB" --ref ref/kevin_c.png &
g M8 "Morning, a bright Honduran school classroom. Medium close shot: the teacher exactly as in her reference (40, glasses, light-blue cardigan) sitting at her desk, looking up with a proud surprised smile, mouth closed. No other characters in focus. $NB" --ref ref/maestra.png &
g W10 "Morning sun in a small colonial plaza of Gracias, Lempira, white church behind, clear blue sky. Close-up of the bronze Lempira statue standing still on his stone pedestal. $NB" --ref ref/lempira_c.png &
wait
