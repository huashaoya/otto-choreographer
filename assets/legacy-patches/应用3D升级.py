from pathlib import Path
import re,json,hashlib
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat')
p=Path(r'D:\jarvis\otto-choreographer.html')
a=Path(r'D:\jarvis\_backup\otto-choreographer-2D实物版.html')
h=p.read_text(encoding='utf-8'); old=a.read_text(encoding='utf-8')
assert h==old,'目标已经发生未确认变化，停止覆盖'
lib=(R/'three-0.158.0.min.js').read_text(encoding='utf-8')
assert len(lib)>500000 and 'WebGLRenderer' in lib and 'ExtrudeGeometry' in lib
# Library marks legacy UMD as deprecated, but the offline single-file constraint
# requires the global build. Remove only this packaging warning, retain license.
warning='console.warn(\'Scripts "build/three.js" and "build/three.min.js" are deprecated with r150+, and will be removed with r160. Please use ES Modules or alternatives: https://threejs.org/docs/index.html#manual/en/introduction/Installation\');'
lib=lib.replace(warning,'')
# Ensure inline library cannot terminate HTML script prematurely.
lib=re.sub(r'</script',r'<\\/script',lib,flags=re.I)
render=(R/'Otto实体3D预览.js').read_text(encoding='utf-8')
x=h.index('/* ============================================================\n   画布：实物照片纹理')
y=h.index('/* ============================================================\n   左侧滑块',x)
h=h[:x]+render+h[y:]
# Library is entirely inline: no CDN, module imports, model fetch, or network at runtime.
h=h.replace("<script>\n'use strict';",'<script>\n'+lib+"\n</script>\n<script>\n'use strict';",1)
h=h.replace('<canvas id="robot" width="520" height="460"></canvas>', '<canvas id="robot" width="520" height="460" tabindex="0" aria-label="Otto实体3D预览，拖动旋转，滚轮缩放，方向键改变视角"></canvas>\n    <div class="stage-controls" id="view3dControls"><button type="button" data-view="front">正面</button><button type="button" data-view="side">侧面</button><button type="button" data-view="back">背面</button><button type="button" data-view="reset">视角复位</button><span style="font-size:11px;color:var(--dim)">拖动旋转 · 滚轮缩放</span></div>',1)
h=h.replace('function bindEvents() {','function bindEvents() {\n  document.querySelectorAll("#view3dControls [data-view]").forEach(btn => btn.addEventListener("click", () => setRobotView(btn.dataset.view)));',1)
p.write_text(h,encoding='utf-8',newline='')
# Discrete syntax fixtures extracted in UTF8 through Node in the next step.
(R/'3D升级记录.json').write_text(json.dumps({'archive':str(a),'archive_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),'target':str(p),'renderer':'WebGL实体网格','offline':True,'source':'用户白蓝照片和视频；背面和深度为合理补全'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'bytes':p.stat().st_size,'library_bytes':len(lib),'target':str(p)},ensure_ascii=False))
