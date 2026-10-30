const results=[];const test=(name,ok,detail)=>{results.push({name,passed:!!ok,detail});if(!ok)throw new Error(name+': '+JSON.stringify(detail));};
test('原始实体网格及六轴就绪',robot3d.ready&&Object.keys(robot3d.joints).length===6,Object.keys(robot3d.joints));
for(const name of Object.keys(OTTO_MESH)){
 const g=nativeGeometry(name),s=g.boundingBox.getSize(new THREE.Vector3()),o=OTTO_MESH[name];
 test('原模不缩放 '+name,Math.abs(s.x-(o.hi[0]-o.lo[0]))<.0001&&Math.abs(s.y-(o.hi[2]-o.lo[2]))<.0001&&Math.abs(s.z-(o.hi[1]-o.lo[1]))<.0001,{size:s,faces:g.index.count/3});
 g.dispose();
}
const stand={...STAND_POSE};
// Independent point check: true ankle axis Z, fore-aft coordinate invariant.
for(const key of ['lf','rf']){
 for(const angle of [30,90,150]){
  drawRobot({...stand,[key]:angle});const j=robot3d.joints[key];
  const centre=j.getWorldPosition(new THREE.Vector3());
  const outer=j.localToWorld(new THREE.Vector3(key==='lf'?-20:20,-17.5,25));
  test('脚轴不再前后俯仰 '+key+'='+angle,Math.abs(j.rotation.x)<1e-10&&Math.abs(outer.z-centre.z-25)<1e-6,{axisX:j.rotation.x,axisZ:j.rotation.z,outerRelativeY:outer.y-centre.y});
  const baseline=-17.5;const delta=outer.y-centre.y-baseline;
  const expectUp=key==='lf'?angle<90:angle>90;
  if(angle!==90)test('脚外缘方向 '+key+'='+angle,expectUp?delta>0:delta<0,{delta,expectUp});
 }
}
// True hip-Y axis: yaw moves depth but does not tip blue leg sideways.
drawRobot({...stand,ll:60,rl:120});
for(const key of ['ll','rl']){const j=robot3d.joints[key];const a=j.getWorldPosition(new THREE.Vector3()),b=j.localToWorld(new THREE.Vector3(0,-20,12));test('髋竖直舵机轴 '+key,Math.abs(j.rotation.z)<1e-10&&Math.abs((b.y-a.y)+20)<1e-6,{rotation:j.rotation.toArray()});}
for(const key of SERVO_KEYS){for(const angle of [0,45,90,135,180]){
 drawRobot({...stand,[key]:angle});test('六轴有效姿态 '+key+'='+angle,robot3d.joints[key].matrixWorld.elements.every(Number.isFinite),{});
 const box=new THREE.Box3().setFromObject(robot3d.root);let clipped=false;
 for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z]){const p=new THREE.Vector3(x,y,z).project(robot3d.camera);if(Math.abs(p.x)>.99||Math.abs(p.y)>.99)clipped=true;}
 test('无裁切 '+key+'='+angle,!clipped,{});
}}
const before=JSON.stringify(buildSequence());selectFrame(1);test('部分姿态JSON不变',JSON.stringify(buildSequence())===before&&SERVO_KEYS.every(k=>Number.isFinite(state.pose[k])),state.pose);
state.pose={...stand};drawRobot(stand);state.frames=[poseFrame(stand,100,0),poseFrame({lh:160},100,0),oscFrame({a:{lh:20},o:{lh:160},p:100,c:1},0),poseFrame(stand,100,0)];await playAll();test('播放归位',JSON.stringify(state.pose)===JSON.stringify(stand)&&!state.playing,state.pose);
state.frames=[poseFrame({lf:60},1000,0)];const running=playAll();await new Promise(r=>setTimeout(r,80));stopAll();await Promise.race([running,new Promise((_,reject)=>setTimeout(()=>reject(new Error('停止悬挂')),1200))]);test('停止同步',!state.playing&&JSON.stringify(state.pose)===JSON.stringify(previewState.pose),state.pose);
state.frames=[poseFrame(stand,800,100),poseFrame({lh:160},450,100),oscFrame({a:{lh:20},o:{lh:160},p:300,c:5},100),poseFrame(stand,700,0)];state.activeFrame=0;state.pose={...stand};syncPoseSliders();renderTimeline();updateJson();drawRobot(stand);setRobotView('reset');
return {passed:results.every(r=>r.passed),checks:results.length,results,geometry:previewState.geometry};
