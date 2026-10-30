from pathlib import Path
import zipfile,xml.etree.ElementTree as E,math,random,json,collections
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat');z=zipfile.ZipFile(R/'Otto原始模型.3mf');ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
def verts(path):return [tuple(float(a.attrib[k]) for k in ['x','y','z']) for a in E.fromstring(z.read(path)).findall('.//m:vertex',ns)]
def circles(pts):
 rng=random.Random(11);out=[]
 if len(pts)<3:return out
 for _ in range(1400):
  p,q,r=rng.sample(pts,3);d=2*(p[0]*(q[1]-r[1])+q[0]*(r[1]-p[1])+r[0]*(p[1]-q[1]))
  if abs(d)<1e-6:continue
  s=lambda a:a[0]**2+a[1]**2
  cx=(s(p)*(q[1]-r[1])+s(q)*(r[1]-p[1])+s(r)*(p[1]-q[1]))/d
  cy=(s(p)*(r[0]-q[0])+s(q)*(p[0]-r[0])+s(r)*(q[0]-p[0]))/d
  rad=math.hypot(p[0]-cx,p[1]-cy)
  if not .5<rad<9:continue
  n=sum(abs(math.hypot(x-cx,y-cy)-rad)<.001 for x,y in pts)
  if n>20 and not any(math.hypot(cx-a[1],cy-a[2])+abs(rad-a[3])<.01 for a in out):out.append((n,cx,cy,rad))
 return sorted(out,reverse=True)
v=verts('3D/Objects/object_3.model')
for plane in [-20.75,-18.75,-14.25,-12.25,18.75,20.75]:
 pts=[(x,zz) for x,y,zz in v if abs(y-plane)<.0001]
 print('leg y',plane,'XZ circles',json.dumps(circles(pts)))
v=verts('3D/Objects/object_2.model')
for plane in [-25.9,-23.4,23.4,25.9]:
 pts=[(x,zz) for x,y,zz in v if abs(y-plane)<.0001]
 print('foot y',plane,'XZ circles',json.dumps(circles(pts)))
