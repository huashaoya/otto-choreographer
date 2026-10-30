from pathlib import Path
from PIL import Image
import base64,io,json,re,hashlib
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat')
P=Path(r'D:\jarvis\otto-choreographer.html')
h=P.read_text(encoding='utf-8')
assert 'id="robotFallback"' not in h
# User photo cutout is embedded as a real static fallback; it is not a 3D plane.
im=Image.open(R/'otto-核查'/'实物部件核查.jpg')
buf=io.BytesIO();im.save(buf,format='JPEG',quality=88)
src='data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode('ascii')
anchor='<canvas id="robot" width="520" height="460" tabindex="0" aria-label="Otto实体3D预览，拖动旋转，滚轮缩放，方向键改变视角"></canvas>'
assert h.count(anchor)==1
h=h.replace(anchor,anchor+'\n    <img id="robotFallback" hidden src="'+src+'" alt="WebGL不可用时显示的白蓝Otto实物参考，不是3D预览" style="width:520px;max-width:100%;height:460px;object-fit:contain;">',1)
a='  robot3d.ready=false;\n  const stage=canvas.parentElement;'
b='  robot3d.ready=false;\n  canvas.hidden=true;\n  const fallback=$(\'robotFallback\');if(fallback)fallback.hidden=false;\n  const stage=canvas.parentElement;'
assert h.count(a)==1;h=h.replace(a,b,1)
P.write_text(h,encoding='utf-8',newline='')
print(json.dumps({'bytes':P.stat().st_size,'fallback':'内嵌真实照片','archive':r'D:\jarvis\_backup\otto-choreographer-2D实物版.html'},ensure_ascii=False))
