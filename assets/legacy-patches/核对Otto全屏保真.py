from pathlib import Path
import re,json,hashlib,subprocess
root=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat\Otto全屏修复')
p=Path(r'D:\jarvis\otto-choreographer.html')
new=p.read_text(encoding='utf-8');old=Path(r'D:\jarvis\_backup\otto-choreographer-全屏修复前.html').read_text(encoding='utf-8')
def part(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
def mesh(s):return json.JSONDecoder().raw_decode(s[re.search(r'const OTTO_MESH\s*=\s*',s).end():])[0]
scripts=re.findall(r'<script>\s*([\s\S]*?)</script>',new)
old_scripts=re.findall(r'<script>\s*([\s\S]*?)</script>',old)
checks={
 'embedded_library_equal':scripts[0]==old_scripts[0],
 'original_mesh_equal':mesh(new)==mesh(old),
 'assembly_and_hand_mapping_equal':part(new,'function handLift','let queuedRender')==part(old,'function handLift','let queuedRender'),
 'six_axis_mapping_equal':part(new,'function drawRobot','function show3DFailure')==part(old,'function drawRobot','function show3DFailure'),
 'presets_data_playback_protocol_equal':part(new,'function buildServoPanel','   事件绑定')==part(old,'function buildServoPanel','   事件绑定'),
 'offline_no_external_scripts':not re.search(r'<script[^>]+src=',new),
 'offline_no_fetch':not re.search(r'\bfetch\(',scripts[1])
}
syntax=[]
for i,s in enumerate(scripts):
 f=root/f'内嵌语法{i}.js';f.write_text(s,encoding='utf-8',newline='')
 r=subprocess.run(['node','--check',str(f)],capture_output=True,text=True,encoding='utf-8')
 syntax.append({'script':i,'passed':r.returncode==0,'output':r.stdout+r.stderr})
runs=[]
for folder in ['验收宽窄屏','验收中屏横屏','原功能回归']:
 r=json.loads((root/folder/'report.json').read_text(encoding='utf-8'))
 for view,v in r['shots'].items():
  e=v.get('eval',{});res=e.get('result',{})
  ok=e.get('executed') and res.get('passed') and all(c['passed'] for c in res.get('checks',[]))
  runs.append({'run':folder,'view':view,'viewport':v['structure']['viewport'],'passed':bool(ok),'check_count':res.get('count'),'native_fullscreen':res.get('nativeFullscreenVerified'),'console_errors':len(v['consoleErrors']),'console_warnings':len(v['consoleWarnings'])})
report={'passed':all(checks.values()) and all(s['passed'] for s in syntax) and all(r['passed'] and not r['console_errors'] and not r['console_warnings'] for r in runs),'checks':checks,'syntax':syntax,'runs':runs,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'not_verified':'merchant side assembly likeness and physical robot execution; no network or firmware changes'}
(root/'保真与语法.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False));assert report['passed']
