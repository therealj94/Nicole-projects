from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import numpy as np, math, os, random
W,H=1080,1920
CREAM=(239,232,223); IVORY=(250,246,240); CHOC=(59,42,32); GOLD=(184,147,90); BURG=(110,20,35); INK=(40,30,26)
def F(name,size,wght=None):
    p={'pf':'PlayfairDisplay[wght].ttf','pfi':'PlayfairDisplay-Italic[wght].ttf','cg':'CormorantGaramond[wght].ttf','cgi':'CormorantGaramond-Italic[wght].ttf',
       'gv':'GreatVibes-Regular.ttf','ms':'Montserrat[wght].ttf','cz':'Cinzel[wght].ttf'}[name]
    f=ImageFont.truetype(p,size)
    if wght:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f
def paper(col=CREAM):
    rng=np.random.default_rng(3); n=rng.normal(0,4,(H,W,1))
    a=np.clip(np.array(col,np.float32)+n,0,255).astype(np.uint8); return Image.fromarray(np.repeat(a,1,2)[:,:,:3]).convert('RGBA')
def photo(k,fy=.5,dark=0,boost=1.05):
    im=Image.open(f'img/{k}.png').convert('RGB'); s=max(W/im.width,H/im.height); im=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS)
    y=int((im.height-H)*fy); x=(im.width-W)//2; im=im.crop((x,y,x+W,y+H)); im=ImageEnhance.Color(im).enhance(boost)
    im=im.convert('RGBA')
    if dark: im.alpha_composite(Image.new('RGBA',(W,H),(20,12,8,int(255*dark))))
    return im
def vgrad(im,top,h,a,col=(20,12,8)):
    g=Image.new('L',(1,256))
    for i in range(256): g.putpixel((0,i),int(a*(1-i/255)**1.3) if top else int(a*(i/255)**1.3))
    hh=int(H*h); ov=Image.new('RGBA',(W,hh),col+(0,)); ov.putalpha(g.resize((W,hh))); im.alpha_composite(ov,(0,0 if top else H-hh))
def shadow(im,box,r=28,blur=22,a=70,off=(0,14)):
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((box[0]+off[0],box[1]+off[1],box[2]+off[0],box[3]+off[1]),r,fill=(0,0,0,a)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
def text(im,xy,s,f,fill,anchor='mm',spacing=8,align='center',sh=None):
    d=ImageDraw.Draw(im)
    if sh: 
        L=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(L).multiline_text(xy,s,font=f,fill=sh,anchor=anchor,spacing=spacing,align=align); im.alpha_composite(L.filter(ImageFilter.GaussianBlur(8)))
    d.multiline_text(xy,s,font=f,fill=fill,anchor=anchor,spacing=spacing,align=align)
def brand(im,y=175,col=GOLD):
    f=F('cz',30,500); d=ImageDraw.Draw(im); t='L U X U R Y   B E L L A   S P A'; d.text((W/2,y),t,font=f,fill=col,anchor='mm')
    w=d.textlength(t,font=f); d.line([(W/2-w/2-70,y),(W/2-w/2-20,y)],fill=col,width=2); d.line([(W/2+w/2+20,y),(W/2+w/2+70,y)],fill=col,width=2)
def cta(im,y=1560,dark=False,t='Agenda tu cita  ·  (631) 365-6004'):
    f=F('ms',34,600); d=ImageDraw.Draw(im); w=d.textlength(t,font=f)+90
    box=(W/2-w/2,y-42,W/2+w/2,y+42); shadow(im,box,42,16,60,(0,8))
    d.rounded_rectangle(box,42,fill=CHOC if not dark else IVORY); d.text((W/2,y),t,font=f,fill=IVORY if not dark else CHOC,anchor='mm')
def sticker(im,k,h,xy,rot=0,sh=True):
    s=Image.open(f'img/{k}_cut.png'); s=s.resize((int(s.width*h/s.height),h),Image.LANCZOS).rotate(rot,expand=True,resample=Image.BICUBIC)
    if sh:
        S=Image.new('RGBA',s.size,(0,0,0,0)); S.putalpha(s.split()[3].point(lambda v:int(v*.35))); S=S.filter(ImageFilter.GaussianBlur(10)); im.alpha_composite(S,(xy[0]+8,xy[1]+14))
    im.alpha_composite(s,xy)
def card(im,box,r=36,fill=(255,255,255,255)):
    shadow(im,box,r); ImageDraw.Draw(im).rounded_rectangle(box,r,fill=fill)
def notif(im,y,title,body,when='ahora',x0=150,x1=930):
    box=(x0,y,x1,y+190); card(im,box,34,(255,255,255,245)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((x0+38,y+42,x0+88,y+92),12,fill=CHOC); d.text((x0+63,y+67),'LB',font=F('cz',22,700),fill=GOLD,anchor='mm')
    d.text((x0+110,y+67),title,font=F('ms',36,700),fill=INK,anchor='lm'); d.text((x1-40,y+67),when,font=F('ms',30,500),fill=(130,120,110),anchor='rm')
    d.text((x0+40,y+135),body,font=F('cgi',40,500),fill=INK,anchor='lm')
def polaroid(im,k,box_w,xy,rot,fy=.5,cap=None):
    p=Image.open(f'img/{k}.png').convert('RGB'); hh=int(box_w*1.15); s=max(box_w/p.width,hh/p.height); p=p.resize((int(p.width*s)+1,int(p.height*s)+1),Image.LANCZOS)
    y=int((p.height-hh)*fy); x=(p.width-box_w)//2; p=p.crop((x,y,x+box_w,y+hh))
    fr=Image.new('RGBA',(box_w+40,hh+150),(252,250,246,255)); fr.paste(p,(20,20))
    if cap: ImageDraw.Draw(fr).text((fr.width/2,hh+85),cap,font=F('gv',64),fill=CHOC,anchor='mm')
    fr=fr.rotate(rot,expand=True,resample=Image.BICUBIC)
    S=Image.new('RGBA',fr.size,(0,0,0,0)); S.putalpha(fr.split()[3].point(lambda v:int(v*.35))); S=S.filter(ImageFilter.GaussianBlur(14)); im.alpha_composite(S,(xy[0]+10,xy[1]+16)); im.alpha_composite(fr,xy)
def torn(im,box,fill=(252,250,246)):
    x0,y0,x1,y1=box; rng=np.random.default_rng(int(x0+y0)); pts=[]
    for x in np.linspace(x0,x1,40): pts.append((x,y0+rng.uniform(-8,8)))
    for y in np.linspace(y0,y1,40): pts.append((x1+rng.uniform(-8,8),y))
    for x in np.linspace(x1,x0,40): pts.append((x,y1+rng.uniform(-8,8)))
    for y in np.linspace(y1,y0,40): pts.append((x0+rng.uniform(-8,8),y))
    S=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(S).polygon([(x+6,y+12) for x,y in pts],fill=(0,0,0,60)); im.alpha_composite(S.filter(ImageFilter.GaussianBlur(12)))
    ImageDraw.Draw(im).polygon(pts,fill=fill)
def tag(im,cx,cy,t,f=None,bg=GOLD,fg=(255,255,255)):
    f=f or F('ms',30,600); d=ImageDraw.Draw(im); w=d.textlength(t,font=f)+60; d.rounded_rectangle((cx-w/2,cy-30,cx+w/2,cy+30),30,fill=bg); d.text((cx,cy),t,font=f,fill=fg,anchor='mm')
def giftcard(w,rot=0):
    h=int(w*0.62); c=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.rounded_rectangle((0,0,w,h),int(w*.05),fill=(22,18,16)); m=int(w*.04); d.rounded_rectangle((m,m,w-m,h-m),int(w*.03),outline=GOLD,width=max(2,w//160))
    d.text((w/2,h*.38),'LUXURY BELLA SPA',font=F('cz',int(w*.075),600),fill=GOLD,anchor='mm')
    d.text((w/2,h*.62),'Gift Card',font=F('gv',int(w*.13)),fill=(230,210,170),anchor='mm')
    return c.rotate(rot,expand=True,resample=Image.BICUBIC)
def paste_shadow(im,c,xy,a=.4,blur=16):
    S=Image.new('RGBA',c.size,(0,0,0,0)); S.putalpha(c.split()[3].point(lambda v:int(v*a))); S=S.filter(ImageFilter.GaussianBlur(blur)); im.alpha_composite(S,(xy[0]+10,xy[1]+18)); im.alpha_composite(c,xy)
