const checks=[],check=(name,ok,detail={})=>{checks.push({name,passed:!!ok,detail});if(!ok)throw Error(name+JSON.stringify(detail));};
check('3D初始化完成',robot3d.ready&&robot3d.frames>0);
check('移除的顶部站立按钮未恢复',!$('resetPose'));
check('移除的两处提示未恢复',!document.body.innerText.includes('点击追加')&&!$('view3dControls').innerText.includes('拖动旋转'));
check('舞台说明未恢复',!$('robotStage').querySelector('.model-note'));
check('姿态库仍有16项含站立',PRESETS.length===16&&PRESETS.some(p=>p.name==='站立'));
for(const key of ['ll','rl']){
 const hip=robot3d.joints[key],shell=hip.children.find(o=>o.name==='原始蓝腿'),foot=robot3d.joints[key==='ll'?'lf':'rf'];
 check('腿壳与脚架同深度 '+key,shell.position.z===3.25&&foot.position.z===shell.position.z);
 const horn=new THREE.Vector3(0,21,-3.25).applyMatrix4(shell.matrix);
 check('腿壳顶部髋孔对齐 '+key,horn.length()<1e-8);
}
const cables=robot3d.root.children.filter(o=>o.isMesh&&o.geometry.type==='TubeGeometry');
check('两侧线缆保留',cables.length===4);
check('线缆后移到中部',cables.every(o=>{o.geometry.computeBoundingBox();return o.geometry.boundingBox.min.z>-4&&o.geometry.boundingBox.max.z<4;}));
check('初始正面俯角和复位一致',robot3d.views.yaw===0&&robot3d.views.pitch===.24);
const sequenceBefore=JSON.stringify(buildSequence()),rootBefore=robot3d.root.position.toArray();
let dialogs=0;const realConfirm=window.confirm;window.confirm=()=>{dialogs++;throw Error('不应确认');};
try{$('clearAll').click();}finally{window.confirm=realConfirm;}
check('清空不弹确认且JSON为空',dialogs===0&&state.frames.length===0&&state.activeFrame===-1&&state.playIndex===-1&&state.sequenceDelay===0&&JSON.stringify(buildSequence())==='{"a":[],"d":0}');
check('清空不移动机器人基座',JSON.stringify(rootBefore)===JSON.stringify(robot3d.root.position.toArray()));
parseSequence(JSON.parse(sequenceBefore));drawRobot(STAND_POSE);setRobotView('reset');
return {passed:checks.every(c=>c.passed),count:checks.length,checks,scope:'UI and assembly implementation checks; not physical fitting or likeness acceptance'};
