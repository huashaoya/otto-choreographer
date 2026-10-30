from pathlib import Path
import json,re,hashlib
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat\Otto整体优化');current=Path(r'D:\jarvis\otto-choreographer.html').read_text(encoding='utf-8');old=Path(r'D:\jarvis\_backup\otto-choreographer-整体优化前.html').read_text(encoding='utf-8')
def mesh(h):
 a=re.search(r'const OTTO_MESH\s*=\s*',h).end();obj,end=json.JSONDecoder().raw_decode(h[a:]);return obj
def part(h,a,b):return h[h.index(a):h.index(b,h.index(a))]
checks={'original_mesh_payload_equal':mesh(current)==mesh(old),'embedded_library_equal':re.findall(r'<script>\s*([\s\S]*?)</script>',current)[0]==re.findall(r'<script>\s*([\s\S]*?)</script>',old)[0],'preset_definitions_equal':part(current,'const PRESETS =','function buildPresetPanel')==part(old,'const PRESETS =','function buildPresetPanel'),'hand_mapping_equal':part(current,'function handLift','function roundedShape')==part(old,'function handLift','function roundedShape'),'offline_no_external_scripts':not re.search(r'<script[^>]+src=',current),'offline_no_fetch_requests':not re.search(r'\bfetch\(',re.findall(r'<script>\s*([\s\S]*?)</script>',current)[1])}
if not all(checks.values()):raise RuntimeError(checks)
report={'passed':True,'checks':checks,'bytes_before':len(old.encode()),'bytes_after':len(current.encode()),'sha256':hashlib.sha256(current.encode()).hexdigest()};(R/'保真核对.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
