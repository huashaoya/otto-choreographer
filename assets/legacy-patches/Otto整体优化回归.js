const checks=[];const assert=(name,ok,detail={})=>{checks.push({name,passed:!!ok,detail});if(!ok)throw new Error(name+':'+JSON.stringify(detail));};
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const fixture={a:[{s:{ll:120},v:100,d:0},{s:{lh:160},v:100,d:0},{osc:{a:{lf:20},o:{lf:100},ph:{lf:90},p:100,c:.1},d:0}],d:70};
parseSequence(fixture);assert('局部姿态导入不补写其他关节',equal(buildSequence(),fixture),buildSequence());
selectFrame(1);assert('选择局部帧继承之前姿态',state.pose.ll===120&&state.pose.lh===160,state.pose);
$('frameDuration').value='250';$('frameDelay').value='80';$('frameDuration').dispatchEvent(new Event('change'));assert('帧耗时与延迟编辑写入正确',state.frames[1].v===250&&state.frames[1].d===80);
$('frameDuration').value='-1';$('frameDuration').dispatchEvent(new Event('change'));assert('无效时序输入不破坏帧',state.frames[1].v===250&&$('frameDuration').value==='250');
state.pose.lh=150;syncPoseToActiveFrame();assert('修改单轴不污染稀疏JSON',equal(state.frames[1].s,{lh:150}),state.frames[1].s);
moveFrame(0,1);assert('交换保留原选中帧身份',state.activeFrame===0);deleteFrame(1);assert('删除后选中索引有效',state.activeFrame===0);
const good=buildSequence();
for(const bad of [null,{}, {a:[null]}, {a:[{s:{lh:'<img src=x onerror=alert(1)>'}}]}, {a:[{s:{lh:181}}]}, {a:[{s:{lh:20},v:-1}]}, {a:[{s:{evil:90}}]}, {a:[{osc:{a:{lh:4},p:100,c:1}}]}, {a:[{osc:{a:{lh:10},o:null,p:100,c:1}}]}, {a:[{s:{lh:20},osc:{a:{lh:20}}}]}]){
 let error=false;try{parseSequence(bad);}catch(e){error=true;}assert('非法输入原子拒绝 '+checks.length,error&&equal(buildSequence(),good));
}
parseSequence(fixture);openOscModal(state.frames[2]);const edited=buildOscFromForm();assert('振荡编辑保留脚幅度中心和相位',equal(edited,fixture.a[2].osc),edited);$('oscConfirm').click();assert('振荡编辑保存后无损',equal(buildSequence(),fixture));
openOscModal(state.frames[2]);$('oscA_lf').value='';$('oscConfirm').click();assert('空表单不覆盖原帧',$('oscModal').classList.contains('show')&&equal(buildSequence(),fixture));closeOscModal();
assert('振荡默认中心来自固件90而非Home',oscCenterPose({a:{lh:20},o:{lh:160}}).rh===90);
assert('相位90在0时刻有正确位移',oscPoseAt({a:{lf:20},o:{lf:100},ph:{lf:90},p:100,c:1},0).lf===120);
assert('腿振荡未锁脚有警告',sequenceWarnings({a:[{osc:{a:{ll:20,lf:20,rf:20},o:{lf:110,rf:110}}}],d:0}).length>0);
assert('固定90脚的腿振荡通过',sequenceWarnings({a:[{osc:{a:{ll:20},o:{lf:90}}}],d:0}).length===0);
assert('超范围振荡不允许下发',sequenceWarnings({a:[{osc:{a:{lh:20},o:{lh:170}}}],d:0}).length>0);
for(const p of PRESETS){validateSequence({a:p.build().map(f=>f.type==='pose'?{s:f.s,v:f.v,d:f.d}:{osc:f.osc,d:f.d}),d:0});}
assert('16项预设结构保留且有效',PRESETS.length===16);
// End-to-end UI core: import -> select/edit -> play -> stop -> immediate restart.
parseSequence({a:[{s:{ll:120},v:100,d:0},{s:{lh:160},v:100,d:0}],d:70});state.pose={...STAND_POSE};syncPoseSliders();drawRobot(state.pose);
const start=performance.now();await playAll();assert('播放继承稀疏关节且包含总延迟',state.pose.ll===120&&state.pose.lh===160&&!state.playing&&performance.now()-start>=260,state.pose);
parseSequence({a:[{osc:{a:{lh:20},o:{lh:150},p:100,c:.1},d:0}],d:0});await playAll();assert('振荡结束以中心角作为基准',state.pose.lh===150&&state.pose.rh===90,state.pose);
parseSequence({a:[{s:{lh:170},v:100,d:5000}],d:0});const first=playAll();await wait(160);stopAll();
parseSequence({a:[{s:{lh:45,rh:135},v:100,d:0}],d:0});const second=playAll();await Promise.all([first,second]);assert('停止长延迟并立刻重播不竞争',!state.playing&&state.pose.lh===45&&state.pose.rh===135&&playTimer===null&&playTimeout===null,state.pose);
parseSequence({a:[{s:{lh:170},v:500,d:0}],d:0});const sliderRun=playAll();await wait(50);$('rng-lh').value='75';$('rng-lh').dispatchEvent(new Event('input'));await sliderRun;assert('播放时拖动滑块保持新输入75',state.pose.lh===75&&!state.playing,state.pose);
assert('预览按钮不启动播放锁',($('previewBtn').click(),!state.playing));
// Connection isolated mocks only. No socket network is opened.
const RealSocket=window.WebSocket;const sockets=[];
class MockSocket{static CONNECTING=0;static OPEN=1;static CLOSED=3;constructor(url){this.url=url;this.readyState=0;this.sent=[];sockets.push(this);}close(){this.readyState=3;}send(s){if(this.readyState!==1)throw Error('not open');this.sent.push(JSON.parse(s));}}
try{
 window.WebSocket=MockSocket;
 assert('拒绝协议路径和非法IP',!validHost('http://10.0.0.1')&&!validHost('999.1.1.1')&&!validHost('10.0.0.1/path'));
 $('ipInput').value='192.168.0.2';connectWs();const old=sockets.at(-1),oldClose=old.onclose;
 $('ipInput').value='otto.local';connectWs();const current=sockets.at(-1);current.readyState=1;current.onopen();oldClose();
 assert('旧socket关闭事件不覆盖新连接',state.ws===current&&!$('sendBtn').disabled&&$('connStatus').textContent==='已连接');
 parseSequence({a:[{s:{...STAND_POSE},v:100,d:0}],d:0});sendSequence();const packet=current.sent[0];
 assert('JSON-RPC协议和字符串序列保持',packet.type==='mcp'&&packet.payload.method==='tools/call'&&packet.payload.params.name==='self.otto.servo_sequences'&&typeof packet.payload.params.arguments.sequence==='string');
 current.onmessage({data:JSON.stringify({type:'mcp',payload:{jsonrpc:'2.0',error:{message:'test error'}}})});assert('嵌套设备错误可显示',$('toast').textContent.includes('test error'));
 parseSequence({a:[{osc:{a:{ll:20,lf:20,rf:20},o:{lf:110,rf:110},p:100,c:1},d:0}],d:0});sendSequence();assert('不安全序列没有发出',current.sent.length===1);
 disconnectWs();assert('断开重置状态与下发禁用',state.ws===null&&$('sendBtn').disabled);
}finally{disconnectWs();window.WebSocket=RealSocket;$('ipInput').value='';$('connStatus').textContent='未连接';}
// Geometry dimensions unchanged; motion mapping and full-frame visibility checked separately from likeness.
for(const name of Object.keys(OTTO_MESH)){const g=nativeGeometry(name),size=g.boundingBox.getSize(new THREE.Vector3()),s=OTTO_MESH[name];assert('原网格尺寸保留 '+name,Math.abs(size.x-(s.hi[0]-s.lo[0]))<.0001&&Math.abs(size.y-(s.hi[2]-s.lo[2]))<.0001&&Math.abs(size.z-(s.hi[1]-s.lo[1]))<.0001);g.dispose();}
for(const key of SERVO_KEYS)for(const angle of [0,90,180]){drawRobot({...STAND_POSE,[key]:angle});assert('六轴有限矩阵 '+key+'='+angle,robot3d.joints[key].matrixWorld.elements.every(Number.isFinite));}
for(const view of ['front','side','leftSide','back','reset']){drawRobot(STAND_POSE);setRobotView(view);const b=robot3d.bounds;let clip=false;for(const x of [b.min.x,b.max.x])for(const y of [b.min.y,b.max.y])for(const z of [b.min.z,b.max.z]){const v=new THREE.Vector3(x,y,z).project(robot3d.camera);if(Math.abs(v.x)>.99||Math.abs(v.y)>.99)clip=true;}assert('视角完整不裁切 '+view,!clip);}
assert('canvas渲染比例匹配实际元素',Math.abs(robot3d.camera.aspect-canvas.clientWidth/canvas.clientHeight)<.02);
const beforeFrames=robot3d.frames;for(let i=0;i<20;i++)queueRender3D();await wait(60);assert('批量视角请求只渲染一帧',robot3d.frames-beforeFrames===1,{delta:robot3d.frames-beforeFrames});
const memory=robot3d.renderer.info.memory.geometries;for(let i=0;i<5;i++)drawRobot(STAND_POSE);assert('重复渲染不增加GPU几何',robot3d.renderer.info.memory.geometries===memory);
parseSequence({a:[{s:{...STAND_POSE},v:800,d:100},{s:{lh:160},v:450,d:100},{osc:{a:{lh:20},o:{lh:160},p:300,c:5},d:100},{s:{...STAND_POSE},v:700,d:0}],d:0});state.pose={...STAND_POSE};syncPoseSliders();drawRobot(state.pose);setRobotView('reset');$('toast').className='toast';
return {passed:checks.every(c=>c.passed),count:checks.length,checks,renderer:{geometries:memory,drawCalls:robot3d.renderer.info.render.calls,triangles:robot3d.renderer.info.render.triangles,pixelRatio:robot3d.pixelRatio},likeness:'not accepted by user; not a geometry test conclusion'};
