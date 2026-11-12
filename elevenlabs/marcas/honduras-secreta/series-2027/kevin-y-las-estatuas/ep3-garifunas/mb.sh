E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, VERTICAL 9:16 portrait frame for a phone screen. Soft rounded shapes, expressive faces. NOT realistic. No text, letters or numbers anywhere except the macaw's hat patch. Keep the TOP 15% of the frame free of faces (sky, wall or background there)."
G="the young teenage cartoon macaw exactly as in the macaw references: oversized head, big round glossy eyes, red body, two FEATHERED WINGS with yellow and blue feathers (wings are wings: no hands, no fingers, no claws on the wings), exactly TWO feet at the bottom of the body, the SAME beige bucket hat with the rectangular 'HONDURAS Secreta' patch facing the camera"
K="Kevin exactly as in his reference (10-year-old Honduran boy, spiky black hair, gap-tooth smile, blue long-sleeve shirt, denim shorts, colorful sneakers)"
R="the living stone Maya king statue exactly as in his reference (greenish-gray carved stone with moss, tall round carved feathered headdress, jade ear spools, ceremonial bar, kind golden glowing eyes)"
S="the small living stone Maya scribe statue exactly as in his reference (seated cross-legged, gray stone with moss, headband, stone paintbrush and shell ink pot, big kind eyes)"
Q="the two living stone macaw heads exactly as in their reference (carved gray-green stone macaw heads with big beaks and round cartoon eyes) sitting on top of a carved stone wall"
CP="the Maya archaeological site of Copán Ruinas, Honduras: grassy plaza, carved stone stelae, stepped stone pyramids, big ceiba trees, green hills"
RG="ref/jose_ref.png"; RC="ref/jose_ref_close.png"
g(){ o=$1; p=$2; shift 2; [ -s ep3/mb/$o.png ] && return; python3 $E image "$ST $p" -o ep3/mb/$o.png --model gemini-3.1-flash-image --ar 9:16 --res 2K "$@" > ep3/mb/$o.log 2>&1; }
AN="the living carved mahogany wooden statue of a Garifuna ancestor elder exactly as in his reference (warm dark wood grain, kind face, white carved beard, simple carved shirt, barefoot, holding a carved canoe paddle)"
TB="the living Garifuna drum exactly as in his reference (tall wooden hand drum with goatskin head tied with rope, yellow white and black painted stripes, cheerful carved face, two small wooden arms with open hands, NO drumsticks)"
PG="Punta Gorda, a Garifuna village on Roatán island, Honduras: turquoise Caribbean sea, white sand, colorful wooden houses on stilts, tall coconut palms, wooden dugout canoes (cayucos) on the beach"
x1(){
g 01 "Afternoon, Kevin's bedroom. $K sits at his desk with an open school notebook and a small map of Honduras, bored, chin on his hand. On the window sill behind him the macaw small, beak closed." --ref ref/kevin_c.png --ref ref/jose_ref.png &
g 02 "Bright afternoon in $PG. $G flies happily over the beach, wings open; below, $K walks barefoot on the sand amazed, sandals in hand." --ref ref/jose_ref.png --ref ref/kevin_c.png &
g 03 "Golden sunset on the beach of $PG. $AN stands on his driftwood base next to a palm tree, golden light cracks glowing in the wood grain, eyes just opened, a warm smile. Below, $K and $G look up amazed, mouths closed." --ref ref/ancestro_c.png --ref ref/kevin_c.png --ref ref/jose_ref.png &
g 04 "Sunset on the beach. Close-up: $AN looking at the camera with a warm grandfatherly smile, mouth closed, the sea glowing orange behind. No other characters." --ref ref/ancestro_c.png &
g 05 "Night on the beach of $PG under a huge starry sky: a magical glowing golden vision floating over the sea of several wooden canoes full of Garifuna families arriving at the shore, lanterns, hopeful faces. In the foreground, seen from behind, $AN, $K and $G watch the vision." --ref ref/ancestro_c.png --ref ref/kevin_c.png --ref ref/jose_ref.png &
wait; }
x2(){
g 06 "Night on the beach with a small bonfire. $TB has just come alive and plays itself with its little hands, huge grin; next to it $K tries to dance punta moving his hips clumsily and laughing; $G dances too with wings open. Joyful." --ref ref/tambor_c.png --ref ref/kevin_c.png --ref ref/jose_ref.png &
g 07 "Evening, a Garifuna village kitchen with a wood fire: a kind Garifuna grandmother in a colorful head wrap and dress offers $K a piece of warm round coconut bread (pan de coco) and thin crispy cassava bread (ereba) on a woven tray; $K takes a bite delighted. Coconuts and pots around." --ref ref/kevin_c.png --ref ref/style_humans.png &
g 08 "Night, a joyful Garifuna community celebration on the beach around a bonfire: people in colorful traditional clothes dancing punta, drummers playing tall hand drums with their hands, $TB among them, $K and $G dancing happily in the center. Yellow, white and black flags." --ref ref/tambor_c.png --ref ref/kevin_c.png --ref ref/jose_ref.png &
g 09 "Dawn on the beach of $PG, pink-orange sky over the sea. $AN kneels and puts his wooden hand on $K's shoulder, both smiling with emotion; $G sits on Kevin's other shoulder, wings folded. The statue's feet are turning back to still wood." --ref ref/ancestro_c.png --ref ref/kevin_c.png --ref ref/jose_ref.png &
g 10 "Morning, Honduran school classroom. $K stands in front of the class proudly presenting a drawing of canoes arriving at a beach and a small yellow, white and black Garifuna flag; the teacher exactly as in her reference smiles; classmates clap." --ref ref/kevin_c.png --ref ref/maestra.png &
wait; }
x1; x2
