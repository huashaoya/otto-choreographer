from pathlib import Path
import zipfile,xml.etree.ElementTree as E,json,base64,array
from PIL import Image,ImageDraw
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat')
z=zipfile.ZipFile(R/'Otto原始模型.3mf')
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
parts={};summaries={}
for name,path in {'cap':'3D/Objects/object_4.model','body':'3D/Objects/object_1.model','leg':'3D/Objects/object_3.model','foot':'3D/Objects/object_2.model','claw':'3D/Objects/object_10.model'}.items():
    root=E.fromstring(z.read(path))
    vertices=[tuple(float(v.attrib[k]) for k in ['x','y','z']) for v in root.findall('.//m:vertex',ns)]
    tris=[tuple(int(t.attrib[k]) for k in ['v1','v2','v3']) for t in root.findall('.//m:triangle',ns)]
    lo=[min(v[i] for v in vertices) for i in range(3)];hi=[max(v[i] for v in vertices) for i in range(3)]
    parts[name]={'positions':base64.b64encode(array.array('f',[x for v in vertices for x in v]).tobytes()).decode(),'indices':base64.b64encode(array.array('I',[x for t in tris for x in t]).tobytes()).decode(),'lo':lo,'hi':hi,'vertices':len(vertices),'faces':len(tris)}
    summaries[name]={'lo':lo,'hi':hi,'size':[hi[i]-lo[i] for i in range(3)],'vertices':len(vertices),'faces':len(tris)}
    img=Image.new('RGB',(960,360),'#eff2f5');d=ImageDraw.Draw(img)
    for view,(axes,label) in enumerate([((0,2),'XZ'),((0,1),'XY'),((1,2),'YZ')]):
        a,b=axes;sc=min(270/max(.1,hi[a]-lo[a]),280/max(.1,hi[b]-lo[b]));cx=(lo[a]+hi[a])/2;cy=(lo[b]+hi[b])/2
        # All wire edges show actual holes/slots in orthographic projections.
        for t in tris:
            pts=[(view*320+160+(vertices[k][a]-cx)*sc,180-(vertices[k][b]-cy)*sc) for k in t]
            d.line(pts+[pts[0]],fill='#7491a1',width=1)
        d.text((view*320+15,10),name+' '+label,fill='black')
    img.save(R/(name+'-原始网格.png'))
(R/'Otto真实网格.json').write_text(json.dumps(parts,separators=(',',':')),encoding='utf-8')
(R/'Otto模型尺寸.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summaries,ensure_ascii=False,indent=2))
