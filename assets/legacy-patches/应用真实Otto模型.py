from pathlib import Path
import re,json
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat');P=Path(r'D:\jarvis\otto-choreographer.html')
h=P.read_text(encoding='utf-8')
assert 'const OTTO_MESH' not in h
loader=(R/'Otto网格加载.js').read_text(encoding='utf-8').replace('__MESH_DATA__',(R/'Otto真实网格.json').read_text(encoding='utf-8'))
h=h.replace('function buildRobot3D(){',loader+'\nfunction buildRobot3D(){',1)
x=h.index('  // Top footprint=69×69mm');y=h.index('  robot3d.joints=pivots;',x)
h=h[:x]+(R/'Otto原始模型装配.js').read_text(encoding='utf-8')+h[y:]
a='  j.ll.rotation.z=(p.ll-90)*r;j.rl.rotation.z=(p.rl-90)*r;'
b='  j.ll.rotation.set(0,(90-p.ll)*r,0);j.rl.rotation.set(0,(90-p.rl)*r,0);'
assert h.count(a)==1;h=h.replace(a,b,1)
a='  // In world coordinates X pitch negative lifts the forward (+Z) toe.\n  j.lf.rotation.x=(p.lf-90)*r;j.rf.rotation.x=(90-p.rf)*r;'
b='  // Fore-aft Z horn axis. Small angle lifts left outer edge and lowers right outer edge.\n  // Mirror installation changes meaning at either foot; it does not change the world-axis sign.\n  j.lf.rotation.set(0,0,(p.lf-90)*r);j.rf.rotation.set(0,0,(p.rf-90)*r);'
assert h.count(a)==1;h=h.replace(a,b,1)
h=h.replace("{x:j[k].rotation.x,z:j[k].rotation.z}","{x:j[k].rotation.x,y:j[k].rotation.y,z:j[k].rotation.z}")
h=h.replace('  // World Y up. Positive Z rotation takes a downward limb to the right.\n  // Therefore the sign is opposite to the old Canvas Y-down rotation.', '  // Actual assembly axes verified from native mesh holes: hip=Y, ankle=Z, arm=Z.')
# License and source attribution required by the native mesh license.
anchor='<div class="stage-controls" id="view3dControls">'
h=h.replace(anchor,'<div style="font-size:10px;color:var(--dim);max-width:520px;text-align:center">模型源自小鹏 OttoRobot · CC BY-NC-SA 4.0 · 改动：坐标转换、白蓝配色、关节联动；原始网格未缩放</div>\n    '+anchor,1)
P.write_text(h,encoding='utf-8',newline='')
print(json.dumps({'target':str(P),'bytes':P.stat().st_size,'source':'小鹏原始3MF','axis':'hip Y; foot Z'}))
