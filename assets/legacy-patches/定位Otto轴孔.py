from pathlib import Path
import zipfile,xml.etree.ElementTree as E,collections,math,json
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat');z=zipfile.ZipFile(R/'Otto原始模型.3mf');ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
for n,p,axis,plane,lims in [('foot','3D/Objects/object_2.model',1,-23.4,(5,16,-1,12)),('leg','3D/Objects/object_3.model',1,18.75,(-5,5,-19,-7))]:
 v=[tuple(float(v.attrib[k]) for k in ['x','y','z']) for v in E.fromstring(z.read(p)).findall('.//m:vertex',ns)]
 pts=[(x,zz) for x,y,zz in v if abs(y-plane)<.01 and lims[0]<x<lims[1] and lims[2]<zz<lims[3]]
 print(n,len(pts),pts[:120])
