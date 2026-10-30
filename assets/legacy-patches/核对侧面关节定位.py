from pathlib import Path
import zipfile,xml.etree.ElementTree as E,json,math
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat');z=zipfile.ZipFile(R/'Otto原始模型.3mf');ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
v=[tuple(float(a.attrib[k]) for k in ['x','y','z']) for a in E.fromstring(z.read('3D/Objects/object_3.model')).findall('.//m:vertex',ns)]
pts=[(x,y) for x,y,zz in v if abs(zz-21)<.0001 and abs(x)<8.1 and -15<y<15]
# Fit separate circular contours; do not mix the horn hole and fastening screw.
import random
rng=random.Random(7);candidates=[]
for _ in range(500):
    p,q,r=rng.sample(pts,3)
    d=2*(p[0]*(q[1]-r[1])+q[0]*(r[1]-p[1])+r[0]*(p[1]-q[1]))
    if abs(d)<1e-5:continue
    s=lambda a:a[0]**2+a[1]**2
    cx=(s(p)*(q[1]-r[1])+s(q)*(r[1]-p[1])+s(r)*(p[1]-q[1]))/d
    cy=(s(p)*(r[0]-q[0])+s(q)*(p[0]-r[0])+s(r)*(q[0]-p[0]))/d
    rad=math.hypot(p[0]-cx,p[1]-cy)
    if not 1<rad<9:continue
    count=sum(abs(math.hypot(x-cx,y-cy)-rad)<.0005 for x,y in pts)
    if count>30 and not any(math.hypot(cx-a[1],cy-a[2])+abs(rad-a[3])<.01 for a in candidates):candidates.append((count,cx,cy,rad))
print(json.dumps({'separate_endplate_circles':sorted(candidates,reverse=True)},ensure_ascii=False))

# Other pole: solid pin at CAD y=-20.75 and z=-10.5.
print('leg CAD cap z21 faces forward when used as arm. Wrist CAD y=-20.75,z=-10.5.')
