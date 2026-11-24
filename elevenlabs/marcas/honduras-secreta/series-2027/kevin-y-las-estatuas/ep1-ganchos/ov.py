# Capas de texto del gancho: frase en español grande + subtítulo en inglés (estilo de la serie)
import sys
from PIL import Image,ImageDraw,ImageFont
W,H=1080,1920
FB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FM='/tmp/claude-0/-home-user-Nicole-projects/dd5b2fc2-184e-5514-b789-f8432119b327/scratchpad/hs/enc/fonts/PermanentMarker.ttf'
YEL=(255,214,64)
def layer(es,en,y,out):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    yy=y
    for i,l in enumerate(es.split('\n')):
        s=74
        while d.textlength(l,font=ImageFont.truetype(FM,s))>980: s-=2
        d.text((W/2,yy),l,font=ImageFont.truetype(FM,s),fill=YEL if i==len(es.split('\n'))-1 else (255,255,255),anchor='mm',stroke_width=10,stroke_fill=(30,15,50)); yy+=s*1.15
    if en: d.text((W/2,yy+8),en,font=ImageFont.truetype(FB,38),fill=(255,255,255),anchor='mm',stroke_width=5,stroke_fill=(0,0,0,235))
    im.save(out)
layer(*sys.argv[1:3],float(sys.argv[3]),sys.argv[4])
