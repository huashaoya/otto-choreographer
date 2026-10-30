const checks=[],check=(name,ok,detail={})=>{checks.push({name,passed:!!ok,detail});if(!ok)throw Error(name+JSON.stringify(detail));};
const snapshot=()=>({camera:robot3d.camera.position.toArray(),orientation:robot3d.camera.quaternion.toArray(),root:robot3d.root.position.toArray(),target:robot3d.cameraTarget.toArray(),body:robot3d.root.children.find(o=>o.name==='原始白壳与固定肩').getWorldPosition(new THREE.Vector3()).project(robot3d.camera).toArray()});
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
drawRobot(STAND_POSE);setRobotView('reset');const fixed=snapshot();
for(const k of SERVO_KEYS)for(const a of [0,90,180]){const p={...STAND_POSE,[k]:a};state.pose=p;syncPoseSliders();$('rng-'+k).dispatchEvent(new Event('input'));check('滑块相机和机身不移动 '+k+'='+a,equal(fixed,snapshot()),snapshot());}
setRobotView('side');const side=snapshot();drawRobot({...STAND_POSE,lf:20,rh:20});check('手动换视角后角度变化保持相机',equal(side,snapshot()));
canvas.dispatchEvent(new WheelEvent('wheel',{deltaY:200,bubbles:true,cancelable:true}));await new Promise(r=>setTimeout(r,90));check('手动缩放仍生效',!equal(side.camera,snapshot().camera));const zoomed=snapshot();drawRobot(STAND_POSE);check('缩放后姿态变化保持用户相机',equal(zoomed,snapshot()));
// Record each local playback render, including interpolated motion and oscillator.
parseSequence({a:[{s:{lf:40,lh:170},v:180,d:0},{osc:{a:{rh:20},o:{rh:70},p:100,c:1},d:0},{s:{...STAND_POSE},v:180,d:0}],d:0});
const expected=snapshot(),original=drawRobot;let renders=0,stable=true;
drawRobot=function(p){original(p);renders++;if(!equal(expected,snapshot()))stable=false;};
try{await playAll();}finally{drawRobot=original;}
check('播放插值与振荡不移动相机机身',stable&&renders>3,{renders,stable});
parseSequence({a:[{s:{...STAND_POSE},v:800,d:0}],d:0});selectFrame(0);setRobotView('reset');
return {passed:checks.every(c=>c.passed),count:checks.length,checks,baseHeight:robot3d.baseHeight,mode:'fixed Home base and framing; no pose-dependent translation/auto-fit'};
