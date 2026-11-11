import cv2,numpy as np,sys
n=sys.argv[1];a=cv2.VideoCapture('vid/'+n+'.mp4');b=cv2.VideoCapture('vfix/'+n+'.mp4');i=0;out=[]
while True:
  ok,x=a.read();ok2,y=b.read()
  if not ok or not ok2: break
  if i%4==0:
    d=np.abs(cv2.resize(x,(540,960)).astype(int)-cv2.resize(y,(540,960)).astype(int)).sum(2)>30;ys,xs=np.nonzero(d)
    out.append(f'{i}:{int(xs.mean()*4)},{int(ys.mean()*4)}' if len(xs)>20 else f'{i}:-')
  i+=1
print(n,' '.join(out))
