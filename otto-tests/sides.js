const checks=[],assert=(name,ok,detail={})=>{checks.push({name,passed:!!ok,detail});if(!ok)throw Error(name+JSON.stringify(detail));};
setRobotView('front');drawRobot(STAND_POSE);
const projectJoint=k=>robot3d.joints[k].getWorldPosition(new THREE.Vector3()).project(robot3d.camera).x;
for(const [left,right] of [['ll','rl'],['lf','rf'],['lh','rh']]){
 assert('自身左右位置 '+left+'/'+right,projectJoint(left)>0&&projectJoint(right)<0,{left:projectJoint(left),right:projectJoint(right)});
}
for(const key of SERVO_KEYS){
 parseSequence({a:[{s:{...STAND_POSE},v:800,d:0}],d:0});selectFrame(0);
 const before=Object.fromEntries(SERVO_KEYS.map(k=>[k,robot3d.joints[k].rotation.toArray().slice(0,3)]));
 const value=STAND_POSE[key]+20,rng=$('rng-'+key);rng.value=String(value);rng.dispatchEvent(new Event('input'));
 const after=Object.fromEntries(SERVO_KEYS.map(k=>[k,robot3d.joints[k].rotation.toArray().slice(0,3)]));
 assert('滑块只改变对应关节 '+key,SERVO_KEYS.every(k=>(JSON.stringify(before[k])!==JSON.stringify(after[k]))===(k===key)));
 assert('JSON保持原字段和值 '+key,buildSequence().a[0].s[key]===value&&SERVO_KEYS.filter(k=>k!==key).every(k=>buildSequence().a[0].s[k]===STAND_POSE[k]));
}
setRobotView('side');assert('右侧视从机器人右侧看',robot3d.camera.position.x<0);
setRobotView('leftSide');assert('左侧视从机器人左侧看',robot3d.camera.position.x>0);
parseSequence({a:[{s:{...STAND_POSE,lh:170},v:800,d:0}],d:0});selectFrame(0);setRobotView('front');
const claw=k=>robot3d.joints[k].children.find(c=>c.name==='原始开口爪');
const center=k=>new THREE.Box3().setFromObject(claw(k)).getCenter(new THREE.Vector3());
assert('左手举起位于正面画面右侧',center('lh').x>0&&center('lh').y>center('rh').y,{left:center('lh').toArray(),right:center('rh').toArray()});
return {passed:checks.every(c=>c.passed),count:checks.length,checks,note:'robot-local side convention; hardware not tested'};
