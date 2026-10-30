from pathlib import Path
import re, hashlib, json
P=Path(r'D:\jarvis\otto-choreographer.html'); h=P.read_text(encoding='utf-8')
BEFORE=h
def replace(old,new):
 global h
 if h.count(old)!=1:raise RuntimeError('补丁定位不唯一: '+old[:100])
 h=h.replace(old,new)
def section(start,end,new):
 global h
 a=h.index(start);b=h.index(end,a);h=h[:a]+new+'\n\n'+h[b:]
replace('<title>Otto 在线编舞台</title>', '''<title>Otto 在线编舞台</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect x='6' y='10' width='52' height='46' rx='8' fill='%23eff4f8'/%3E%3Cpath d='M6 18h52M18 10l-6-7M46 10l6-7' stroke='%23159fd3' stroke-width='6'/%3E%3Crect x='17' y='24' width='30' height='22' rx='3' fill='%23080b10'/%3E%3Ccircle cx='26' cy='35' r='5' fill='%239df8ff'/%3E%3Ccircle cx='38' cy='35' r='5' fill='%239df8ff'/%3E%3C/svg%3E">''')
css='''
  /* Review: retain workstation layout; provide a usable stacked narrow view. */
  :root { --dim: #94a9bd; }
  main { grid-template-columns: minmax(240px,300px) minmax(0,1fr) minmax(300px,380px); }
  .panel { min-width:0; }
  button:focus-visible, input:focus-visible, textarea:focus-visible, .frame:focus-visible, canvas:focus-visible { outline:2px solid var(--accent); outline-offset:3px; }
  button[aria-pressed="true"] { border-color:var(--accent);color:var(--accent); }
  .stage canvas { display:block;width:520px;height:auto;aspect-ratio:26/23;max-width:100%;flex:none; }
  .model-note { max-width:520px;font-size:11px;color:var(--dim);text-align:center; }
  .sequence-summary { display:flex;flex-wrap:wrap;gap:10px;align-items:center;font-size:12px;color:var(--dim);padding:8px 14px;border-top:1px solid var(--line); }
  .sequence-summary input { width:90px;background:var(--panel-2);color:var(--text);border:1px solid var(--line);padding:4px; }
  .sequence-summary .warning { width:100%;color:var(--warn); }
  .connection-status { font-size:11px;color:var(--dim);max-width:180px;overflow-wrap:anywhere; }
  .frame-actions button { min-height:26px;min-width:26px; }
  .frame-meta { color:var(--dim); }
  .servo-help { font-size:11px;color:var(--dim);margin-top:3px; }
  .preset-btn .p-desc { color:var(--dim); }
  .modal-bg .modal { width:min(700px,94vw); }
  .osc-grid { display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px; }
  .osc-servo { border:1px solid var(--line);border-radius:6px;padding:10px;min-width:0; }
  .osc-servo h4 { margin-bottom:8px;font-size:13px; }
  .osc-servo .form-row { margin-bottom:8px; }
  .osc-servo label { letter-spacing:0; }
  .modal-actions { position:sticky;bottom:-22px;padding:12px 0;background:var(--panel); }
  .stage-controls { gap:6px; }
  .toast { max-width:calc(100vw - 24px);overflow-wrap:anywhere; }
  @media(max-width:1100px) {
    body { height:auto;min-height:100%;overflow:auto; }
    main { flex:none;grid-template-columns:minmax(0,1fr);gap:12px;background:var(--bg);padding:12px; }
    .panel { overflow:visible;border:1px solid var(--line);border-radius:8px; }
    .stage { order:-1;padding:14px; }
    .stage canvas { width:min(520px,100%); }
    .panel-body { overflow:visible; }
    #timeline { max-height:400px !important;overflow:auto; }
    .json-box { min-height:240px;resize:vertical; }
    header { flex-wrap:wrap;gap:8px; }
    header h1 { white-space:nowrap; }
    .conn { flex-wrap:wrap; }
  }
  @media(max-width:600px) {
    header { padding:12px; }
    header .spacer { display:none; }
    .conn { width:100%; }
    .conn input { flex:1;min-width:120px;width:auto;font-size:16px; }
    .connection-status { max-width:none;width:100%; }
    main { padding:8px;gap:8px; }
    button { min-height:44px; }
    .frame-actions button { min-height:44px;min-width:40px; }
    .servo-name,.servo-val,.preset-btn .p-name,.panel-head,.hint,.form-row label,.sequence-summary { font-size:14px; }
    .servo-desc,.servo-help,.preset-btn .p-desc,.frame-angles,.frame-meta,.model-note,.frame-mode { font-size:12px; }
    input[type=range] { height:26px;background:#24303f; }
    input[type=range]::-webkit-slider-thumb { width:22px;height:22px; }
    input[type=range]::-moz-range-thumb { width:22px;height:22px; }
    .json-box,.form-row input,.form-row select { font-size:16px; }
    .osc-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
    .modal { padding:16px; }
    .frame-head { gap:4px; }
    .stage { gap:10px; }
  }
  @media(prefers-reduced-motion:reduce) { *,*::before,*::after { transition:none !important; } }
'''
replace('</style>',css+'\n</style>')
replace('<span class="dot" id="connDot"></span>', '<span class="dot" id="connDot" aria-hidden="true"></span><span class="connection-status" id="connStatus" role="status">未连接</span>')
replace('<input id="ipInput" placeholder="192.168.0.x" value="">','<input id="ipInput" aria-label="设备IP或主机名" placeholder="192.168.0.x" value="" autocomplete="off" spellcheck="false">')
replace('data-view="side">侧面</button>','data-view="side">右侧面</button><button type="button" data-view="leftSide">左侧面</button>')
replace('▶ 播放全部','播放全部');replace('■ 停止','停止预览')
replace('id="jsonOut" spellcheck="false"','id="jsonOut" aria-label="序列JSON（自动生成，修改请使用导入）" readonly spellcheck="false"')
replace('<div class="panel-body" id="timeline" style="flex:0 1 auto;max-height:44%;"></div>', '''<div class="panel-body" id="timeline" style="flex:0 1 auto;max-height:44%;"></div>
    <div class="sequence-summary"><span id="sequenceStats">0 帧</span><label>总延迟 <input id="sequenceDelay" aria-label="序列结束后延迟毫秒" type="number" min="0" max="600000" step="1" value="0"> ms</label><span id="sequenceWarnings" class="warning" role="status"></span></div>''')
a=h.index('    <div class="form-grid">',h.index('id="oscModal"'));b=h.index('    <div class="modal-actions">',a)
h=h[:a]+'''    <div class="osc-grid" id="oscServoFields"></div>
    <div class="form-grid">
      <div class="form-row"><label for="oscP">周期 p（100–3000 ms）</label><input id="oscP" type="number" value="500" min="100" max="3000" step="1"></div>
      <div class="form-row"><label for="oscC">周期数 c（0.1–20）</label><input id="oscC" type="number" value="5" min="0.1" max="20" step="0.1"></div>
    </div>
    <div class="form-row"><label for="oscD">帧后延迟 d（ms）</label><input id="oscD" type="number" value="0" min="0" max="600000" step="1"></div>
'''+h[b:]
replace('<div class="modal-bg" id="oscModal">','<div class="modal-bg" id="oscModal" role="dialog" aria-modal="true" aria-labelledby="oscTitle">')
replace('<h3>添加振荡帧</h3>','<h3 id="oscTitle">添加振荡帧</h3>')
replace('腿脚振荡时，必须至少有一只脚保持在 90°，否则舵机互顶会损坏齿轮。','腿部振荡时须至少锁定一只脚为 90°。预览停止只影响本页面，不会停止真机；超出关节范围和固件限幅会在下发前提示。')
replace('<div class="toast" id="toast">','<div class="toast" id="toast" role="status" aria-live="polite">')
replace('  msgId: 0,','  msgId: 0,\n  sequenceDelay: 0,\n  playToken: 0,')
# Cache decoded native meshes. Caller clones so rotations never mutate other parts.
replace('function nativeGeometry(name){','const nativeGeometryCache=new Map();\nfunction nativeGeometry(name){\n  if(nativeGeometryCache.has(name))return nativeGeometryCache.get(name).clone();')
replace("  return g;\n}\n\nfunction buildRobot3D()", "  nativeGeometryCache.set(name,g);return g.clone();\n}\n\nfunction buildRobot3D()")
replace("  const edge=new THREE.MeshStandardMaterial({color:'#c3d0da',roughness:.58,metalness:0});\n",'')
replace("  const metal=new THREE.MeshStandardMaterial({color:'#7e8c99',roughness:.3,metalness:.9});\n",'')
replace('  // Real 3MF millimetres and CAD source_offset; CAD ground z=-89 becomes worldY=0.','  // Preserved assembly candidate; source_offset is not proof of full assembly.\n  // Merchant-version side profile and grip shape remain unverified.')
replace('  // Actual assembly axes verified from native mesh holes: hip=Y, ankle=Z, arm=Z.','  // Existing axis mapping retained; hardware trim and merchant assembly are not measured.')
replace('  window.addEventListener(\'resize\',render3D);', '''  window.addEventListener('resize',queueRender3D);
  if(typeof ResizeObserver!=='undefined'){robot3d.resizeObserver=new ResizeObserver(queueRender3D);robot3d.resizeObserver.observe(canvas);}''')
replace("  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();show3DFailure('3D绘图上下文丢失，请重新打开文件');});", "  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();stopAll();show3DFailure('3D绘图上下文丢失，请重新打开文件');});\n  canvas.addEventListener('webglcontextrestored',()=>{location.reload();});")
# Only high-frequency view events use rAF coalescing. drawRobot retains synchronous first frame.
replace('drag={x:e.clientX,y:e.clientY};render3D();','drag={x:e.clientX,y:e.clientY};queueRender3D();')
replace('robot3d.views.distance*Math.exp(e.deltaY*.001)));render3D();','robot3d.views.distance*Math.exp(e.deltaY*.001)));queueRender3D();')
replace('function render3D(){', '''let queuedRender=0;
function queueRender3D(){if(queuedRender||document.hidden)return;queuedRender=requestAnimationFrame(()=>{queuedRender=0;render3D();});}
function resize3D(){
  const box=canvas.getBoundingClientRect(),w=Math.max(1,Math.round(box.width)),ht=Math.max(1,Math.round(box.height));
  const ratio=Math.min(window.devicePixelRatio||1,w<440?1.5:2);
  if(robot3d.width===w&&robot3d.height===ht&&robot3d.pixelRatio===ratio)return;
  robot3d.width=w;robot3d.height=ht;robot3d.pixelRatio=ratio;
  robot3d.renderer.setPixelRatio(ratio);robot3d.renderer.setSize(w,ht,false);
  robot3d.camera.aspect=w/ht;robot3d.camera.updateProjectionMatrix();
}
function render3D(){''')
replace('  const {yaw,pitch,distance}=robot3d.views;','  resize3D();\n  const {yaw,pitch,distance}=robot3d.views;')
replace('  if(!views[name])return;robot3d.views={...views[name]};render3D();', '''  if(!views[name])return;robot3d.views={...views[name]};
  document.querySelectorAll('#view3dControls [data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===name)));
  render3D();''')
# Improve label/accessibility and prevent playback edits.
replace('<span class="servo-name">${s.name}<span class="servo-desc">${s.key}</span></span>','<label class="servo-name" for="rng-${s.key}">${s.name}<span class="servo-desc">${s.key}</span></label>')
replace('<div style="font-size:10px;color:#4d5f73;margin-top:3px;">${s.desc}</div>','<div class="servo-help">${s.desc}</div>')
replace("    rng.addEventListener('input', () => {\n      state.pose", "    rng.addEventListener('input', () => {\n      if(state.playing)stopAll();\n      state.pose")
replace("      const p = PRESETS[+btn.dataset.idx];", "      if(state.playing)stopAll();\n      const p = PRESETS[+btn.dataset.idx];")
replace('    f.s = { ...state.pose };','    SERVO_KEYS.forEach(k=>{if(f.s[k]!==state.pose[k])f.s[k]=state.pose[k];});')
replace('function renderTimeline() {','function renderTimeline() {\n  updateSequenceSummary();')
replace("    div.className = 'frame'", "    div.tabIndex=0;div.setAttribute('aria-label',`第${i+1}帧${f.type==='osc'?'振荡':'姿态'}`);\n    div.addEventListener('keydown',e=>{if(e.target===div&&(e.key==='Enter'||e.key===' ')){e.preventDefault();selectFrame(i);}});\n    div.className = 'frame'")
replace('<button data-act="edit" title="编辑">✎</button>','<button data-act="edit" title="编辑">编辑</button>')
replace('<button data-act="del" title="删除">✕</button>','<button data-act="del" title="删除">删除</button>')
replace('function selectFrame(i) {\n  state.activeFrame = i;', '''function selectFrame(i) {
  if(!state.frames[i])return;if(state.playing)stopAll();
  state.activeFrame = i;''')
replace('    state.pose = normalizePose(f.s);','    state.pose = resolveFramePose(i);')
replace('function moveFrame(i, dir) {\n  const j', 'function moveFrame(i, dir) {\n  if(state.playing)stopAll();\n  const j')
replace('  if (state.activeFrame === i) state.activeFrame = j;', '  if (state.activeFrame === i) state.activeFrame = j;\n  else if(state.activeFrame===j)state.activeFrame=i;')
replace('function deleteFrame(i) {\n  state.frames.splice(i, 1);', '''function deleteFrame(i) {
  if(state.playing)stopAll();if(!state.frames[i])return;
  state.frames.splice(i, 1);
  if(state.activeFrame>i)state.activeFrame--;''')
replace("  if (f.type === 'osc') {\n    openOscModal(f);", "  if (f.type === 'osc') {\n    openOscModal(f);")
replace('function addPoseFrame() {\n  const f', 'function addPoseFrame() {\n  if(state.playing)stopAll();\n  const f')
# Combined domain validation and lossless editor for all six servos.
section('let editingOscIndex = -1;','/* ============================================================\n   JSON 生成 / 导入', '''let editingOscIndex=-1,oscFocusReturn=null;
const isRecord=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
const cloneData=v=>JSON.parse(JSON.stringify(v));
function numeric(v,min,max,label,integer=false){
  if(typeof v!=='number'||!Number.isFinite(v)||v<min||v>max||(integer&&!Number.isInteger(v)))throw new Error(`${label}须为${min}–${max}${integer?'整数':'数值'}`);
  return v;
}
function allowedKeys(obj,keys,label){if(!isRecord(obj))throw new Error(label+'须为对象');for(const k of Object.keys(obj))if(!keys.includes(k))throw new Error(label+'包含未知字段 '+k);}
function servoMap(obj,label,min,max,integer=true){
  allowedKeys(obj,SERVO_KEYS,label);const out={};for(const k of SERVO_KEYS)if(Object.hasOwn(obj,k))out[k]=numeric(obj[k],min,max,label+'.'+k,integer);return out;
}
function validateOsc(raw){
  allowedKeys(raw,['a','o','ph','p','c'],'osc');
  const osc={a:servoMap(raw.a||{},'振幅',0,90),o:servoMap(raw.o||{},'中心角',0,180)};
  for(const [k,v] of Object.entries(osc.a))if(v!==0&&v<10)throw new Error(k+' 振幅应为0或10–90');
  if(!Object.values(osc.a).some(v=>v>0))throw new Error('至少一个关节的振幅须大于0');
  if(Object.hasOwn(raw,'ph'))osc.ph=servoMap(raw.ph,'相位',0,360,false);
  osc.p=numeric(raw.p??300,100,3000,'周期p',true);osc.c=numeric(raw.c??8,.1,20,'周期数c');
  return osc;
}
function validateSequence(seq){
  allowedKeys(seq,['a','d'],'序列');if(!Array.isArray(seq.a))throw new Error('缺少a动作数组');if(seq.a.length>1000)throw new Error('最多支持1000帧');
  const actions=seq.a.map((item,i)=>{
    allowedKeys(item,['s','v','d','osc'],`第${i+1}帧`);
    const delay=numeric(item.d??0,0,600000,'帧后延迟',true);
    if(Object.hasOwn(item,'osc')){if(Object.hasOwn(item,'s')||Object.hasOwn(item,'v'))throw new Error('振荡帧不能混入s/v');return {osc:validateOsc(item.osc),d:delay};}
    if(!Object.hasOwn(item,'s'))throw new Error(`第${i+1}帧缺少s或osc`);
    const s=servoMap(item.s,'姿态',0,180);return {s,v:numeric(item.v??1000,100,3000,'移动耗时',true),d:delay};
  });return {a:actions,d:numeric(seq.d??0,0,600000,'序列总延迟',true)};
}
function oscCenterPose(osc){return Object.fromEntries(SERVO_KEYS.map(k=>[k,osc.o?.[k]??90]));}
function oscPoseAt(osc,elapsed){
  const p=oscCenterPose(osc),phase=elapsed/(osc.p??300)*Math.PI*2;
  SERVO_KEYS.forEach(k=>{p[k]=Math.max(0,Math.min(180,p[k]+(osc.a?.[k]||0)*Math.sin(phase+(osc.ph?.[k]||0)*Math.PI/180)));});return p;
}
function resolveFramePose(index){
  let p={...STAND_POSE};for(let i=0;i<=index;i++){const f=state.frames[i];if(!f)break;p=f.type==='pose'?normalizePose(f.s,p):oscCenterPose(f.osc);}return p;
}
function openOscModal(existing){
  if(state.playing)stopAll();editingOscIndex=existing?state.frames.indexOf(existing):-1;oscFocusReturn=document.activeElement;
  const o=existing?.osc;
  $('oscServoFields').innerHTML=SERVOS.map(s=>`<section class="osc-servo"><h4>${s.name} ${s.key}</h4>
    <div class="form-row"><label for="oscA_${s.key}">振幅（0停用，10–90）</label><input id="oscA_${s.key}" type="number" min="0" max="90" step="1"></div>
    <div class="form-row"><label for="oscO_${s.key}">中心角（0–180）</label><input id="oscO_${s.key}" type="number" min="0" max="180" step="1"></div>
    <div class="form-row"><label for="oscPH_${s.key}">相位（0–360）</label><input id="oscPH_${s.key}" type="number" min="0" max="360" step="any"></div></section>`).join('');
  SERVO_KEYS.forEach(k=>{
    $(`oscA_${k}`).value=o?.a?.[k]??(existing?0:(['lh','rh'].includes(k)?30:0));
    $(`oscO_${k}`).value=o?.o?.[k]??90;$(`oscPH_${k}`).value=o?.ph?.[k]??0;
  });
  $('oscP').value=o?.p??500;$('oscC').value=o?.c??5;$('oscD').value=existing?.d??0;
  $('oscTitle').textContent=existing?'编辑振荡帧':'添加振荡帧';$('oscConfirm').textContent=existing?'保存':'添加';
  $('oscModal').classList.add('show');$('oscA_ll').focus();
}
function closeOscModal(){ $('oscModal').classList.remove('show');editingOscIndex=-1;oscFocusReturn?.focus(); }
function readFormNumber(id,min,max,label,integer=true){const raw=$(id).value.trim();if(raw==='')throw new Error(label+'不能为空');return numeric(Number(raw),min,max,label,integer);}
function buildOscFromForm(){
  const previous=editingOscIndex>=0?state.frames[editingOscIndex].osc:null;
  const a={},o={},ph={};
  for(const k of SERVO_KEYS){
    const amp=readFormNumber('oscA_'+k,0,90,k+'振幅'),center=readFormNumber('oscO_'+k,0,180,k+'中心角'),phase=readFormNumber('oscPH_'+k,0,360,k+'相位',false);
    if(amp>0||Object.hasOwn(previous?.a||{},k))a[k]=amp;
    if(amp>0||center!==90||Object.hasOwn(previous?.o||{},k))o[k]=center;
    if(phase!==0||Object.hasOwn(previous?.ph||{},k))ph[k]=phase;
  }
  // New leg oscillation starts with both feet locked; never silently rewrite an existing frame.
  if(!previous&&(a.ll||a.rl)){if(!a.lf)o.lf=90;if(!a.rf)o.rf=90;if(a.ll&&a.rl&&!ph.rl)ph.rl=180;}
  const out={a,o,p:readFormNumber('oscP',100,3000,'周期'),c:readFormNumber('oscC',.1,20,'周期数',false)};
  if(Object.keys(ph).length||Object.hasOwn(previous||{},'ph'))out.ph=ph;return validateOsc(out);
}
function sequenceWarnings(seq){
  const warnings=[];seq.a.forEach((f,i)=>{if(!f.osc)return;const o=f.osc,a=o.a||{},centers=oscCenterPose(o),prefix=`第${i+1}帧：`;
    if((a.ll||a.rl)&&!['lf','rf'].some(k=>!a[k]&&centers[k]===90))warnings.push(prefix+'腿部振荡未锁定90°脚，不允许下发');
    if((a.ll>=40&&a.rl>=40)||(a.lf>=40&&a.rf>=40))warnings.push(prefix+'双腿或双脚大幅振荡将被固件限幅，不允许下发');
    for(const k of SERVO_KEYS)if(a[k]&&(centers[k]-a[k]<0||centers[k]+a[k]>180))warnings.push(prefix+k+'振荡超出0–180°，预览限幅；不允许下发');
  });return warnings;
}
function updateSequenceSummary(){
  const seq=buildSequence();const ms=seq.a.reduce((n,f)=>n+(f.osc?f.osc.p*f.osc.c:f.v)+f.d,seq.d);
  $('sequenceStats').textContent=`${seq.a.length} 帧 · ${(ms/1000).toFixed(1)} 秒`;
  $('sequenceDelay').value=state.sequenceDelay;
  const warnings=sequenceWarnings(seq);$('sequenceWarnings').textContent=warnings.slice(0,3).join('；');
  if(warnings.length>3)$('sequenceWarnings').textContent+=`；另${warnings.length-3}项`;
}''')
section('function buildSequence() {','/* ============================================================\n   播放', '''function buildSequence(){
  return {a:state.frames.map(f=>f.type==='pose'?{s:{...f.s},v:f.v,d:f.d}:{osc:cloneData(f.osc),d:f.d}),d:state.sequenceDelay};
}
function updateJson(){ $('jsonOut').value=JSON.stringify(buildSequence(),null,2);updateSequenceSummary(); }
function parseSequence(seq){
  const checked=validateSequence(seq); // Atomic: validate everything before touching current work.
  if(state.playing)stopAll();
  state.frames=checked.a.map(f=>f.osc?oscFrame(f.osc,f.d):poseFrame(f.s,f.v,f.d));state.sequenceDelay=checked.d;
  state.activeFrame=state.frames.length?0:-1;state.playIndex=-1;
  if(state.frames.length){state.pose=resolveFramePose(0);syncPoseSliders();drawRobot(state.pose);}
  renderTimeline();updateJson();
}''')
# Token + cancel continuation prevents old run stealing a new run's state.
section('let playTimer = null;','/* ============================================================\n   WebSocket 下发', '''let playTimer=null,playTimeout=null,playCancel=null;
function lerpPose(a,b,t){return Object.fromEntries(SERVO_KEYS.map(k=>[k,a[k]+(b[k]-a[k])*t]));}
function cancelPlaybackWait(){
  if(playTimer!==null)cancelAnimationFrame(playTimer);if(playTimeout!==null)clearTimeout(playTimeout);
  playTimer=playTimeout=null;const done=playCancel;playCancel=null;done?.(false);
}
function playbackAlive(token){return state.playing&&token===state.playToken;}
function setPlaybackUI(){ $('playBtn').disabled=state.playing;$('previewBtn').disabled=state.playing;$('stopBtn').disabled=!state.playing; }
async function playAll(){
  if(state.playing||!state.frames.length)return;
  let seq;try{seq=validateSequence(buildSequence());}catch(e){toast(e.message,true);return;}
  const token=++state.playToken;state.playing=true;setPlaybackUI();let current=normalizePose(state.pose),completed=0;
  try{
    for(let i=0;i<seq.a.length&&playbackAlive(token);i++){
      state.playIndex=i;$('playhead').textContent=`${i+1} / ${seq.a.length}`;renderTimeline();const f=seq.a[i];
      if(f.osc){await animateOsc(f.osc,token);current=normalizePose(previewState.pose);}
      else {const target=normalizePose(f.s,current);await animateTo(current,target,f.v,token);current=target;}
      if(!playbackAlive(token))break;completed=i+1;if(f.d)await sleep(f.d,token);
    }
    if(playbackAlive(token)&&seq.d)await sleep(seq.d,token);
  }catch(e){if(token===state.playToken)toast('预览失败：'+e.message,true);}
  finally{if(token===state.playToken){state.playing=false;state.pose=normalizePose(previewState.pose);syncPoseSliders();state.playIndex=-1;setPlaybackUI();$('playhead').textContent=`${completed} / ${seq.a.length}`;renderTimeline();}}
}
function runAnimation(duration,render,token){
  return new Promise(resolve=>{
    const start=performance.now(),finish=ok=>{playTimer=null;if(playCancel===finish)playCancel=null;resolve(ok);};playCancel=finish;
    function tick(now){if(!playbackAlive(token)){finish(false);return;}const elapsed=Math.min(duration,now-start);render(elapsed,elapsed>=duration);if(elapsed<duration)playTimer=requestAnimationFrame(tick);else finish(true);}
    playTimer=requestAnimationFrame(tick);
  });
}
function animateTo(from,to,duration,token=state.playToken){return runAnimation(Math.max(100,duration),elapsed=>drawRobot(lerpPose(from,to,Math.min(1,elapsed/Math.max(100,duration)))),token);}
function animateOsc(osc,token=state.playToken){const total=osc.p*osc.c;return runAnimation(total,(elapsed,last)=>drawRobot(last?oscCenterPose(osc):oscPoseAt(osc,elapsed)),token);}
function sleep(ms,token=state.playToken){return new Promise(resolve=>{if(!playbackAlive(token)){resolve(false);return;}const finish=ok=>{playTimeout=null;if(playCancel===finish)playCancel=null;resolve(ok);};playCancel=finish;playTimeout=setTimeout(()=>finish(playbackAlive(token)),ms);});}
function stopAll(){
  const wasPlaying=state.playing;state.playing=false;++state.playToken;cancelPlaybackWait();
  state.pose=normalizePose(previewState.pose);syncPoseSliders();drawRobot(state.pose);state.playIndex=-1;setPlaybackUI();
  if(wasPlaying)$('playhead').textContent='已停止预览';renderTimeline();
}''')
section('function connectWs() {','/* ============================================================\n   工具', '''let wsTimeout=null;
function validHost(host){
  if(host.length>253||/[\s/:?#@\\\\]/.test(host))return false;
  if(/^\\d+\\.\\d+\\.\\d+\\.\\d+$/.test(host))return host.split('.').every(n=>Number(n)<=255);
  return host.split('.').every(p=>/^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/i.test(p));
}
function disconnectWs(){
  clearTimeout(wsTimeout);const old=state.ws;state.ws=null;
  if(old){old.onopen=old.onclose=old.onerror=old.onmessage=null;try{old.close();}catch(e){}}
  $('sendBtn').disabled=true;setDot('','已断开');
}
function connectWs(){
  const host=$('ipInput').value.trim();if(!validHost(host)){toast('请输入有效IPv4或主机名（不要带协议、路径或端口）',true);return;}
  disconnectWs();let ws;try{ws=new WebSocket(`ws://${host}:8080/ws`);}catch(e){setDot('err','连接失败');toast('无法建立连接：'+e.message,true);return;}
  state.ws=ws;setDot('','连接中…');$('connBtn').textContent='取消连接';$('sendBtn').disabled=true;
  wsTimeout=setTimeout(()=>{if(state.ws!==ws||ws.readyState!==WebSocket.CONNECTING)return;disconnectWs();setDot('err','连接超时');toast('连接超时，请检查设备和网络',true);},8000);
  ws.onopen=()=>{if(state.ws!==ws)return;clearTimeout(wsTimeout);setDot('on','已连接');$('sendBtn').disabled=false;};
  ws.onclose=()=>{if(state.ws!==ws)return;clearTimeout(wsTimeout);state.ws=null;$('sendBtn').disabled=true;setDot('','已断开');};
  ws.onerror=()=>{if(state.ws!==ws)return;$('sendBtn').disabled=true;setDot('err','连接失败');};
  ws.onmessage=ev=>{if(state.ws!==ws)return;try{const msg=JSON.parse(ev.data);const body=msg.payload||msg;if(body.error)toast('设备返回错误：'+(body.error.message||'未知错误'),true);else if(body.jsonrpc==='2.0'&&Object.hasOwn(body,'result'))toast('设备已确认请求（不代表动作已完成）');}catch(e){}};
}
function sendSequence(){
  if(!state.ws||state.ws.readyState!==WebSocket.OPEN){toast('还没连接设备',true);return;}
  if(!state.frames.length){toast('时间轴是空的',true);return;}
  let seq;try{seq=validateSequence(buildSequence());}catch(e){toast(e.message,true);return;}
  const warnings=sequenceWarnings(seq);if(warnings.length){toast('未下发：'+warnings[0],true);return;}
  const payload={type:'mcp',payload:{jsonrpc:'2.0',id:++state.msgId,method:'tools/call',params:{name:'self.otto.servo_sequences',arguments:{sequence:JSON.stringify(seq)}}}};
  try{state.ws.send(JSON.stringify(payload));toast(`已发送${seq.a.length}帧，等待设备确认`);}catch(e){toast('发送失败：'+e.message,true);}
}
function setDot(cls,text){const d=$('connDot');d.className='dot'+(cls?' '+cls:'');$('connStatus').textContent=text||'未连接';$('connBtn').textContent=state.ws?(state.ws.readyState===WebSocket.OPEN?'断开':'取消连接'):'连接';}''')
# Binding adjustments and transactional form.
a=h.index("  $('previewBtn').addEventListener('click', () => {");b=h.index("  $('addFrame')",a)
h=h[:a]+'''  $('previewBtn').addEventListener('click',()=>{if(state.playing)return;drawRobot(state.pose);toast('当前姿态已显示（仅本地预览）');});
  $('sequenceDelay').addEventListener('change',()=>{try{state.sequenceDelay=readFormNumber('sequenceDelay',0,600000,'序列总延迟');updateJson();}catch(e){$('sequenceDelay').value=state.sequenceDelay;toast(e.message,true);}});
'''+h[b:]
a=h.index("  $('oscConfirm').addEventListener('click', () => {");b=h.index("  $('oscModal').addEventListener",a)
h=h[:a]+'''  $('oscConfirm').addEventListener('click',()=>{
    try{const osc=buildOscFromForm(),d=readFormNumber('oscD',0,600000,'帧后延迟');
      if(editingOscIndex>=0)state.frames[editingOscIndex]=oscFrame(osc,d);else{state.frames.push(oscFrame(osc,d));state.activeFrame=state.frames.length-1;}
      closeOscModal();renderTimeline();updateJson();
    }catch(e){toast(e.message,true);}
  });
'''+h[b:]
replace("  $('clearAll').addEventListener('click', () => {\n    if (!confirm('清空所有帧？')) return;", "  $('clearAll').addEventListener('click', () => {\n    if (!confirm('清空所有帧？')) return;\n    if(state.playing)stopAll();state.sequenceDelay=0;")
replace("    if (state.ws && state.ws.readyState === WebSocket.OPEN) {\n      state.ws.close();", "    if (state.ws) {\n      disconnectWs();")
replace("    if (e.target.matches('input, textarea, select')) return;", '''    if($('oscModal').classList.contains('show')){
      if(e.key==='Escape'){e.preventDefault();closeOscModal();}
      if(e.key==='Tab'){const nodes=[...$('oscModal').querySelectorAll('input,button')],first=nodes[0],last=nodes.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}return;
    }
    if(e.target.closest('input,textarea,select,button,[contenteditable="true"]')||e.defaultPrevented)return;''')
replace("  $('resetPose').addEventListener('click', () => {\n    state.pose", "  $('resetPose').addEventListener('click', () => {\n    if(state.playing)stopAll();\n    state.pose")
replace("    document.execCommand('copy');\n    document.body.removeChild(ta);\n    toast('已复制');", "    const ok=document.execCommand('copy');\n    document.body.removeChild(ta);\n    toast(ok?'已复制':'复制失败，请选中JSON手动复制',!ok);")
replace('init();\n</script>', '''init();
// Review: geometry/axis state is preserved, not claimed as hardware-calibrated.
document.addEventListener('visibilitychange',()=>{if(document.hidden&&state.playing)stopAll();});
window.addEventListener('pagehide',()=>{if(state.playing)stopAll();disconnectWs();});
</script>''')
# Keep author attribution while exposing honest calibration boundary.
replace('改动：坐标转换、白蓝配色、镜像装配、六轴联动；原始网格未缩放','改动：坐标转换、白蓝配色、镜像装配、六轴联动；原始网格未缩放。商家款侧面/爪型及真机同步尚未验收')
# Break the huge mesh JSON across per-property lines without altering values.
a=h.index('const OTTO_MESH =')
# Source literal ends at first newline; cache declaration now follows it.
line_end=h.index('\n',a);literal=h[a:line_end]
if literal.endswith(';'):
 raw=json.loads(literal.split('=',1)[1][:-1]);pretty=json.dumps(raw,ensure_ascii=False,indent=2,separators=(',',': '));h=h[:a]+'const OTTO_MESH='+pretty+';'+h[line_end:]
# Atomic write, no library/source mesh changes expected.
P.write_text(h,encoding='utf-8',newline='')
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat\Otto整体优化')
(R/'改动记录.json').write_text(json.dumps({'before_sha256':hashlib.sha256(BEFORE.encode()).hexdigest(),'after_sha256':hashlib.sha256(h.encode()).hexdigest(),'before_bytes':len(BEFORE.encode()),'after_bytes':len(h.encode()),'scope':'single HTML; no firmware/hardware actions'},ensure_ascii=False,indent=2),encoding='utf-8')
print('优化补丁已写入',len(h.encode()),'bytes')
