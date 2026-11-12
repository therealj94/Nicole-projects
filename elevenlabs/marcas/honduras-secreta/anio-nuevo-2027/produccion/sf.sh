E=/home/user/Nicole-projects/elevenlabs/el.py
ST="Stylized 3D cartoon animation like a family animated feature film, VERTICAL 9:16 portrait frame composed for a phone screen, characters large, story elements stacked top to bottom, nothing important cut at the sides. Soft rounded shapes, expressive faces. NOT realistic. No text, letters, signs or numbers anywhere except the macaw's hat patch. Setting: a colorful humble Honduran neighborhood street (barrio) on December 31st: painted cinder-block houses, string lights, a corner pulpería, power lines, hills in the background."
G="the young teenage cartoon macaw exactly as in the macaw references: oversized head, big round glossy eyes, red body, yellow and blue wings used like hands, the SAME beige bucket hat with the rectangular 'HONDURAS Secreta' patch facing camera"
CH="Don Chepe exactly as in his reference (65, gray mustache, light-blue shirt, khaki pants, red cap)"
TE="Doña Tencha exactly as in her reference (50, pink hair rollers, floral blouse, yellow apron)"
KE="Kevin exactly as in his reference (10-year-old boy, spiky black hair, blue long-sleeve shirt)"
LA="Don Lalo exactly as in his reference (chubby bald taxi driver, tropical floral shirt, sunglasses on his head)"
AB="the grandmother exactly as in her reference (tiny, white bun, round glasses, shawl, straw broom)"
MU="the Año Viejo effigy exactly as in the prop reference (stuffed rag doll man, plaid shirt, patched jeans, cloth face with painted mustache, torn straw hat) sitting on a white plastic chair"
RM="ref/jose_ref.png"; RC="ref/jose_ref_close.png"
g(){ o=$1; p=$2; shift 2; python3 $E image "$ST $p" -o sf/$o.png --model gemini-3.1-flash-image --ar 9:16 --res 2K "$@" > sf/$o.log 2>&1; }
mkdir -p sf
b1(){
g 01 "Golden late-afternoon light. In the upper half, $G flies in over the street holding a bulging cloth bag of old clothes in its feet, about to land on a low painted wall in the center. Below, the empty street with string lights and kids far away with sparklers." --ref $RM --ref $RC &
g 02 "In the center, $CH sits on a stool in front of his house stuffing sawdust into $MU, smiling proudly. A bag of sawdust beside him. The macaw is NOT in this shot." --ref ref/chepe_c.png --ref ref/muneco_c.png --ref ref/style_humans.png &
g 03 "Evening, string lights on. $TE stands next to $MU in the center, pushing a paper electricity bill into the doll's shirt pocket with a mischievous grin. $CH watches on the left, laughing. Warm light from house windows." --ref ref/tencha_c.png --ref ref/chepe_c.png --ref ref/muneco_c.png &
g 04 "Evening, string lights. In the center $MU on its chair. On the left $KE stuffs a scribbled school notebook into the doll, shouting happily. On the right $LA holds a small toy taxi car ready to put in. Both laughing." --ref ref/kevin_c.png --ref ref/lalo_c.png --ref ref/muneco_c.png &
wait; }
b2(){
g 05 "Evening, string lights. Close medium shot: $G stands on the arm of the white plastic chair next to $MU, holding open an empty brown wallet with one wing, a tiny moth flying out of it, the macaw with a funny relieved face. Neighbors laughing softly blurred in the background." --ref $RM --ref $RC --ref ref/muneco_c.png &
g 06 "Night, string lights. $TE runs happily down the street pulling a rolling suitcase, laughing. Above her in the upper part of the frame, $G flies alongside following her, curious." --ref ref/tencha_c.png --ref $RM --ref $RC &
g 07 "Night, string lights. In the front yard of a small house, $AB sweeps the dust out of the front door toward the street with determination. In the upper part, a clothesline with yellow shirts and yellow towels drying. $G sits on the clothesline looking at them, amused." --ref ref/abuela_c.png --ref $RM --ref $RC &
g 08 "Night, string lights. $CH stands in the center handing small clear bags of green grapes to $KE and two other neighborhood kids holding unlit sparklers, wagging one finger warning them kindly. $G sits on his shoulder." --ref ref/chepe_c.png --ref ref/kevin_c.png --ref $RM &
wait; }
b3(){
g 09 "Night just before midnight. The neighbors stand in a semicircle around $MU: $CH, $TE, $KE, $LA and $AB, each holding grapes, faces lit by string lights, excited. In the front center, $G holds a bunch of grapes, cheeks puffed full of grapes, eyes wide." --ref ref/chepe_c.png --ref ref/tencha_c.png --ref $RM --ref ref/muneco_c.png &
g 10 "Midnight. Wide shot: the Año Viejo effigy on its chair in the middle of the street burns with a big warm cheerful bonfire flame and rising sparks; the neighbors stand at a safe distance clapping and cheering; colorful fireworks burst in the night sky above the houses. $G flies happily above the crowd." --ref ref/muneco_c.png --ref $RM --ref ref/style_humans.png &
g 11 "Midnight, warm firelight and fireworks glow. Medium shot: $CH kneels down and hugs $G warmly; the macaw hugs him back with both wings. In the background blurred neighbors hug each other." --ref ref/chepe_c.png --ref $RM --ref $RC &
g 12 "Night, on a tin rooftop. $G sits alone on the edge of the roof seen from behind three-quarters, then looking up, holding one last grape. In front of it, the city lights of Tegucigalpa in the valley and colorful fireworks bursting over the hills. Lots of open sky in the upper part. Peaceful, emotional." --ref $RM --ref $RC &
wait; }
