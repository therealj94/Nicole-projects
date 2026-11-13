# Panel horizontal 1920x1080 transparente con el logo oficial a la izquierda y el título a la derecha.
import sys
from PIL import Image,ImageDraw,ImageFont
out,serie=sys.argv[1],sys.argv[2]; lines=sys.argv[3:]
FM='/tmp/claude-0/-home-user-Nicole-projects/dd5b2fc2-184e-5514-b789-f8432119b327/scratchpad/hs/enc/fonts/PermanentMarker.ttf'
LOGO=Image.open('/home/user/Nicole-projects/elevenlabs/marcas/honduras-secreta/logo_honduras_secreta_oficial.png').convert('RGBA')
im=Image.new('RGBA',(1920,1080),(0,0,0,0)); d=ImageDraw.Draw(im)
lw=560; lg=LOGO.resize((lw,int(LOGO.height*lw/LOGO.width)),Image.LANCZOS)
sh=Image.new('RGBA',im.size,(0,0,0,0))
from PIL import ImageFilter
x,y=(660-lw)//2,540-lg.height//2-40
sh.paste((0,0,0,150),(x+4,y+5),lg.split()[3].filter(ImageFilter.GaussianBlur(8))); im.alpha_composite(sh); im.alpha_composite(lg,(x,y))
f=ImageFont.truetype(FM,58); w=d.textlength(serie,font=f); d.text((330-w/2,y+lg.height+30),serie,font=f,fill=(255,214,64),stroke_width=3,stroke_fill=(60,30,0))
n=len(lines); ys=[540-(n-1)*45+i*90 for i in range(n)]
for i,(t,yy) in enumerate(zip(lines,ys)):
    s=46 if t.startswith('Parte') else 64
    f=ImageFont.truetype(FM,s); w=d.textlength(t,font=f); d.text((1590-w/2,yy-35),t,font=f,fill=(255,214,64),stroke_width=3,stroke_fill=(60,30,0))
im.save(out)
