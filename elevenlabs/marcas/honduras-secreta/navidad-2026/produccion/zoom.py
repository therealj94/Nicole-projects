import cv2,numpy as np,sys
# uso: zoom.py salida.jpg clip:cuadro,cuadro clip:cuadro ...
rows=[]
for spec in sys.argv[2:]:
  n,ts=spec.split(':');ts=[int(t) for t in ts.split(',')]
  a=cv2.VideoCapture('vid/'+n+'.mp4');b=cv2.VideoCapture('vfix/'+n+'.mp4');i=0;row=[]
  while ts and i<=max(ts):
    ok,x=a.read();ok2,y=b.read()
    if not ok: break
    if i in ts:
      d=np.abs(cv2.resize(x,(540,960)).astype(int)-cv2.resize(y,(540,960)).astype(int)).sum(2)>30;ys,xs=np.nonzero(d)
      if len(xs)>20: cx,cy=int(xs.mean()*4),int(ys.mean()*4);x0,y0=min(max(0,cx-450),1260),max(0,cy-280);c=y[y0:y0+560,x0:x0+900];lab='FIX'
      else: c=cv2.resize(y,(315,560));lab='--'
      row.append(cv2.putText(cv2.resize(c,(450,280)),f'{n} {i} {lab}',(5,25),0,.7,(0,255,255),2))
    i+=1
  rows.append(np.hstack(row))
W=max(r.shape[1] for r in rows);rows=[np.pad(r,((0,0),(0,W-r.shape[1]),(0,0))) for r in rows]
cv2.imwrite(sys.argv[1],np.vstack(rows))
