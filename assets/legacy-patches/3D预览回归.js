const results=[];
const assert=(name,ok,detail)=>{results.push({name,passed:!!ok,detail});if(!ok)throw new Error(name+': '+JSON.stringify(detail));};
assert('3D首帧与六关节已就绪',robot3d.ready&&robot3d.frames>0&&Object.keys(robot3d.joints).length===6,{frames:robot3d.frames,joints:Object.keys(robot3d.joints)});
const meshes=[];robot3d.root.traverse(o=>{if(o.isMesh)meshes.push(o);});
assert('实体网格具有体积',meshes.filter(o=>o.geometry.type==='ExtrudeGeometry').length>15,{meshes:meshes.length,triangles:robot3d.renderer.info.render.triangles});
const originalSeq=JSON.stringify(buildSequence());selectFrame(1);
assert('局部姿态完整且JSON不变',SERVO_KEYS.every(k=>Number.isFinite(state.pose[k]))&&JSON.stringify(buildSequence())===originalSeq,state.pose);
const stand={...STAND_POSE};
// Check in world-space positions, independently of angle formulas.
drawRobot({...stand,ll:0,rl:180});
const lOut=robot3d.joints.ll.localToWorld(new THREE.Vector3(0,-20,0)).x;
const rOut=robot3d.joints.rl.localToWorld(new THREE.Vector3(0,-20,0)).x;
assert('双腿外展方向正确',lOut<-25.2&&rOut>25.2,{lOut,rOut});
drawRobot({...stand,lh:170,rh:10});
const handL=robot3d.joints.lh.localToWorld(new THREE.Vector3(0,-45,0));
const handR=robot3d.joints.rh.localToWorld(new THREE.Vector3(0,-45,0));
assert('双臂上举方向正确',handL.y>82&&handR.y>82,{l:handL.y,r:handR.y});
drawRobot({...stand,lf:0,rf:180});
const toeL=robot3d.joints.lf.localToWorld(new THREE.Vector3(0,-20,25));
const axisL=robot3d.joints.lf.getWorldPosition(new THREE.Vector3());
const toeR=robot3d.joints.rf.localToWorld(new THREE.Vector3(0,-20,25));
const axisR=robot3d.joints.rf.getWorldPosition(new THREE.Vector3());
assert('脚尖翘起真实X轴旋转',toeL.y>axisL.y&&toeR.y>axisR.y,{left:toeL.y-axisL.y,right:toeR.y-axisR.y});
for(const key of SERVO_KEYS){for(const value of [0,45,90,135,180]){
  drawRobot({...stand,[key]:value});
  const matrices=SERVO_KEYS.map(k=>robot3d.joints[k].matrixWorld.elements).flat();
  assert('有效3D姿态 '+key+'='+value,matrices.every(Number.isFinite),{});
  const bounds=new THREE.Box3().setFromObject(robot3d.root);let clipped=false;
  for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){const p=new THREE.Vector3(x,y,z).project(robot3d.camera);if(Math.abs(p.x)>.99||Math.abs(p.y)>.99)clipped=true;}
  assert('自动取景无裁切 '+key+'='+value,!clipped,{distance:robot3d.effectiveDistance});
}}
state.pose={...stand};drawRobot(stand);
const cameraBefore=robot3d.camera.position.clone();document.querySelector('[data-view="side"]').click();
assert('侧面按钮改变镜头而非姿态',robot3d.camera.position.distanceTo(cameraBefore)>50&&JSON.stringify(state.pose)===JSON.stringify(stand),robot3d.views);
canvas.dispatchEvent(new WheelEvent('wheel',{deltaY:160,bubbles:true,cancelable:true}));
assert('滚轮缩放生效且有限位',robot3d.views.distance>260&&robot3d.views.distance<=440,robot3d.views);
canvas.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true,cancelable:true}));
assert('键盘旋转生效',robot3d.views.yaw<Math.PI/2,robot3d.views);
document.querySelector('[data-view="back"]').click();
assert('背面实体可渲染',robot3d.views.yaw===Math.PI&&robot3d.renderer.info.render.calls>0,robot3d.renderer.info.render);
document.querySelector('[data-view="reset"]').click();
state.frames=[poseFrame(stand,100,0),poseFrame({lh:160},100,0),oscFrame({a:{lh:20},o:{lh:160},p:100,c:1},0),poseFrame(stand,100,0)];await playAll();
assert('播放结束归位一致',!state.playing&&JSON.stringify(previewState.pose)===JSON.stringify(stand)&&JSON.stringify(state.pose)===JSON.stringify(stand),state.pose);
state.frames=[poseFrame({lh:170,rh:10},1000,0)];const playback=playAll();await new Promise(r=>setTimeout(r,100));stopAll();await Promise.race([playback,new Promise((_,reject)=>setTimeout(()=>reject(new Error('stop悬挂')),1500))]);
assert('停止后无悬挂且姿态一致',!state.playing&&JSON.stringify(previewState.pose)===JSON.stringify(state.pose),state.pose);
state.frames=[poseFrame({...stand},800,100),poseFrame({lh:160},450,100),oscFrame({a:{lh:20},o:{lh:160},p:300,c:5},100),poseFrame({...stand},700,0)];state.activeFrame=0;state.pose={...stand};syncPoseSliders();renderTimeline();updateJson();drawRobot(stand);setRobotView('reset');
return {passed:results.every(x=>x.passed),checks:results.length,results,render:robot3d.renderer.info.render,ready:robot3d.ready};
