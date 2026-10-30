/* ============================================================
   预览：实体3D（Three.js内嵌，离线单HTML）
   外形依据用户照片/视频；不可见的背面及深度为建模假设，不是扫描尺寸。
   ============================================================ */
const canvas = $('robot');
const previewState = { pose: { ...STAND_POSE }, geometry: null };
const robot3d = { ready:false, renderer:null, scene:null, camera:null, root:null, joints:{}, views:{yaw:.28,pitch:.12,distance:244}, frames:0 };
function normalizePose(pose, fallback = STAND_POSE) {
  const out={};
  SERVO_KEYS.forEach(k=>{const b=Number.isFinite(fallback?.[k])?fallback[k]:STAND_POSE[k];out[k]=Number.isFinite(pose?.[k])?Math.min(180,Math.max(0,pose[k])):b;});
  return out;
}
function handLift(x) {
  if(x<=45)return x*.5;
  if(x<=90)return 22.5+(x-45)*1.5;
  return 90+(x-90)*.889;
}
function roundedShape(w,h,r){
  const s=new THREE.Shape(),x=-w/2,y=-h/2;
  s.moveTo(x+r,y);s.lineTo(x+w-r,y);s.quadraticCurveTo(x+w,y,x+w,y+r);
  s.lineTo(x+w,y+h-r);s.quadraticCurveTo(x+w,y+h,x+w-r,y+h);
  s.lineTo(x+r,y+h);s.quadraticCurveTo(x,y+h,x,y+h-r);
  s.lineTo(x,y+r);s.quadraticCurveTo(x,y,x+r,y);return s;
}
function extrude(shape,depth,bevel=.7){
  const g=new THREE.ExtrudeGeometry(shape,{depth:Math.max(.05,depth-2*bevel),steps:1,bevelEnabled:bevel>0,bevelThickness:bevel,bevelSize:bevel,bevelSegments:3,curveSegments:20});
  g.translate(0,0,-depth/2+bevel);g.computeVertexNormals();return g;
}
function mesh(parent,geometry,material,x=0,y=0,z=0,name=''){
  const m=new THREE.Mesh(geometry,material);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;m.name=name;parent.add(m);return m;
}
function block(parent,w,h,d,r,material,x,y,z,name=''){
  return mesh(parent,extrude(roundedShape(w-1.2,h-1.2,Math.max(.3,r-.6)),d,.6),material,x,y,z,name);
}
function cylinder(parent,r,len,material,x,y,z,axis='z'){
  const m=mesh(parent,new THREE.CylinderGeometry(r,r,len,32),material,x,y,z);
  if(axis==='z')m.rotation.x=Math.PI/2;
  if(axis==='x')m.rotation.z=Math.PI/2;return m;
}
function tube(parent,points,r,material){
  const curve=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p)));
  return mesh(parent,new THREE.TubeGeometry(curve,16,r,8,false),material);
}
function buildRobot3D(){
  const scene=new THREE.Scene();scene.background=new THREE.Color('#0f151d');robot3d.scene=scene;
  const camera=new THREE.PerspectiveCamera(34,520/460,.5,1600);robot3d.camera=camera;
  const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:false,preserveDrawingBuffer:true});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));renderer.setSize(520,460,false);
  renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.12;
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;robot3d.renderer=renderer;
  scene.add(new THREE.HemisphereLight(0xe7f4ff,0x566272,2.0));
  const key=new THREE.DirectionalLight(0xffffff,3.1);key.position.set(-120,180,170);key.castShadow=true;
  key.shadow.mapSize.set(1024,1024);key.shadow.camera.left=-130;key.shadow.camera.right=130;key.shadow.camera.top=170;key.shadow.camera.bottom=-130;key.shadow.camera.far=600;key.shadow.bias=-.001;key.shadow.normalBias=.2;scene.add(key);
  const fill=new THREE.DirectionalLight(0xc7e3ff,1.3);fill.position.set(140,80,40);scene.add(fill);
  const rim=new THREE.DirectionalLight(0xffffff,1.8);rim.position.set(15,160,-140);scene.add(rim);
  // Neutral light-box environment, generated locally (no external HDR request).
  const envScene=new THREE.Scene();envScene.background=new THREE.Color(0x9ba4ad);
  const walls=new THREE.Mesh(new THREE.BoxGeometry(12,10,12),new THREE.MeshBasicMaterial({color:0x9ba4ad,side:THREE.BackSide}));envScene.add(walls);
  [[-4,3,0],[4,3,0],[0,4,-3]].forEach(([x,y,z])=>{const p=new THREE.Mesh(new THREE.BoxGeometry(1,3,4),new THREE.MeshBasicMaterial({color:0xffffff}));p.position.set(x,y,z);envScene.add(p);});
  const pmrem=new THREE.PMREMGenerator(renderer);const env=pmrem.fromScene(envScene,.04);scene.environment=env.texture;pmrem.dispose();envScene.traverse(o=>{if(o.isMesh){o.geometry.dispose();o.material.dispose();}});
  const white=new THREE.MeshPhysicalMaterial({color:'#eff4f8',roughness:.34,metalness:0,clearcoat:.25,clearcoatRoughness:.3,envMapIntensity:.55});
  const blue=new THREE.MeshPhysicalMaterial({color:'#159fd3',roughness:.3,metalness:0,clearcoat:.32,clearcoatRoughness:.25,envMapIntensity:.6});
  const edge=new THREE.MeshStandardMaterial({color:'#c3d0da',roughness:.58,metalness:0});
  const navy=new THREE.MeshStandardMaterial({color:'#126587',roughness:.5,metalness:0});
  const metal=new THREE.MeshStandardMaterial({color:'#7e8c99',roughness:.3,metalness:.9});
  const orange=new THREE.MeshStandardMaterial({color:'#e69a4d',roughness:.65});
  const brown=new THREE.MeshStandardMaterial({color:'#7c4937',roughness:.7});
  const screen=new THREE.MeshStandardMaterial({color:'#03060a',roughness:.16,metalness:0,envMapIntensity:.18});
  const eye=new THREE.MeshBasicMaterial({color:'#9df8ff',toneMapped:false});
  const floor=new THREE.Mesh(new THREE.PlaneGeometry(450,450),new THREE.MeshBasicMaterial({color:'#131d28'}));floor.rotation.x=-Math.PI/2;floor.position.y=-.16;scene.add(floor);
  const contact=new THREE.Mesh(new THREE.PlaneGeometry(450,450),new THREE.ShadowMaterial({opacity:.38}));contact.rotation.x=-Math.PI/2;contact.position.y=-.12;contact.receiveShadow=true;scene.add(contact);
  const grid=new THREE.GridHelper(280,14,0x355061,0x20303f);grid.position.y=.02;grid.material.transparent=true;grid.material.opacity=.4;scene.add(grid);
  const root=new THREE.Group();root.name='Otto实体模型';scene.add(root);robot3d.root=root;
  // Top footprint=69×69mm from photo. Visible front-shell height scaled from image.
  // Units approximate mm. Width annotation115 belongs to foot span, not claw span.
  block(root,69,43,69,3.1,white,0,71,0,'白色一体壳');
  block(root,68.9,1.15,68.7,.7,edge,0,92.6,0,'顶盖接缝');
  const cap=new THREE.Shape();cap.moveTo(-34.5,-2.6);cap.lineTo(34.5,-2.6);cap.lineTo(32.7,2.6);cap.lineTo(-32.7,2.6);cap.closePath();
  mesh(root,extrude(cap,68,.5),blue,0,95.3,0,'蓝色斜面顶盖');
  // Antennas lean outward/back; not vertical rabbit ears.
  tube(root,[[-9,98,-12],[-15,102,-19],[-25,107,-27]],1.15,blue);
  tube(root,[[9,98,-12],[15,102,-19],[25,107,-27]],1.15,blue);
  block(root,31.1,31.5,1.9,1.0,edge,0,71.1,34.7,'屏幕边框');
  block(root,30,30.5,1.5,.55,screen,0,71.1,35.45,'黑色屏幕');
  mesh(root,new THREE.CircleGeometry(5.5,64),eye,-7,72.3,36.3,'左圆眼');
  mesh(root,new THREE.CircleGeometry(5.5,64),eye,7,72.3,36.3,'右圆眼');
  cylinder(root,.45,.4,navy,18.1,77.3,34.65);
  // Four screen screw heads remain tiny, not luminous ornaments.
  [[-14.2,-14.5],[14.2,-14.5],[-14.2,14.5],[14.2,14.5]].forEach(([x,y])=>cylinder(root,.38,.3,metal,x,71.1+y,36.4));
  const pivots={};
  [-1,1].forEach(dir=>{
    const left=dir===-1,hand=left?'lh':'rh',leg=left?'ll':'rl',foot=left?'lf':'rf';
    const sx=dir*49.8,sy=82.3,sz=12;
    // Fixed triangular shoulder bracket and circular servo cover.
    const shoulder=new THREE.Shape();shoulder.moveTo(dir*34.2,90.2);shoulder.lineTo(dir*48,90.2);shoulder.quadraticCurveTo(dir*55,89.7,dir*55.2,84);shoulder.lineTo(dir*52.8,76.8);shoulder.lineTo(dir*34.2,61);shoulder.closePath();
    mesh(root,extrude(shoulder,5,.8),white,0,0,32,'固定肩支架');
    cylinder(root,2.3,.7,edge,sx,sy,35.2);cylinder(root,1.8,.8,white,sx,sy,35.8);
    tube(root,[[dir*36,92,22],[dir*42,93.5,22],[dir*46,90,19]],.7,orange);
    tube(root,[[dir*36,91.4,20],[dir*41,92.5,20],[dir*46,89.4,18]],.6,brown);
    const armPivot=new THREE.Group();armPivot.position.set(sx,sy,sz);root.add(armPivot);pivots[hand]=armPivot;
    block(armPivot,16.5,32,12,2,white,0,-13,0,'活动手臂壳');
    cylinder(armPivot,1.25,.7,metal,0,-20.4,6.7);cylinder(armPivot,.6,.85,navy,0,-20.4,7);
    block(armPivot,9.5,7.5,10,3,white,0,-31.2,0,'固定腕连接');
    // Actual claw is an open C-ring with two rounded lobes, not a closed mitten.
    const claw=new THREE.Shape();
    claw.moveTo(-.9,-21);claw.bezierCurveTo(-8,-21,-10,-16,-10,-11);claw.bezierCurveTo(-10,-5,-6,0,-1,0);claw.bezierCurveTo(6,0,10,-4,10,-10);claw.bezierCurveTo(10,-16,6,-21,.9,-21);
    claw.lineTo(1.5,-16.5);claw.bezierCurveTo(5,-15,5.1,-12,5,-9);claw.bezierCurveTo(4.7,-5.5,2.8,-4.3,0,-4.3);claw.bezierCurveTo(-3,-4.3,-4.8,-6,-5,-9.3);claw.bezierCurveTo(-5.2,-12.7,-4,-15,-1.5,-16.5);claw.closePath();
    const cm=mesh(armPivot,extrude(claw,9,.5),white,0,-34.4,0,'双瓣开口爪');cm.rotation.z=dir*.08;
    const hip=new THREE.Group();hip.position.set(dir*25.2,49.5,0);root.add(hip);pivots[leg]=hip;
    block(hip,17,27,17,1.8,blue,0,-12.8,0,'蓝色腿壳');
    cylinder(hip,1.7,.65,navy,0,-12,8.7);cylinder(hip,.6,.75,metal,-.35,-11.7,9);
    // Foot rotation is genuinely around X in 3D: positive Z is the forward toe.
    const ankle=new THREE.Group();ankle.position.set(0,-26,0);hip.add(ankle);pivots[foot]=ankle;
    block(ankle,18.8,24.5,7,6.0,white,0,-6,9.7,'白色脚踝侧板');
    block(ankle,18.8,24.5,7,6.0,white,0,-6,-9.7,'脚踝后板');
    cylinder(ankle,1.8,26,navy,0,0,0,'z');
    cylinder(ankle,2.3,.8,blue,0,0,13.75);
    cylinder(ankle,1.75,.9,blue,0,0,14.0);
    cylinder(ankle,.65,.7,blue,0,7,13.55);
    // Wide L-shaped sole extends forward, with a modest outer flare as in photo.
    block(ankle,42,5.7,38,3.6,white,dir*4.2,-20.7,10,'L形脚底板');
    block(ankle,19,8.2,19,2.0,white,0,-15.3,2,'脚踝底部筋');
  });
  robot3d.joints=pivots;
  robot3d.ready=true;document.documentElement.dataset.robot3d='ready';
  canvas.style.cursor='grab';canvas.style.touchAction='none';
  let drag=null;
  canvas.addEventListener('pointerdown',e=>{if(e.button!==0)return;drag={x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId);canvas.style.cursor='grabbing';});
  canvas.addEventListener('pointermove',e=>{if(!drag)return;robot3d.views.yaw-=(e.clientX-drag.x)*.009;robot3d.views.pitch=Math.min(.95,Math.max(-.22,robot3d.views.pitch+(e.clientY-drag.y)*.007));drag={x:e.clientX,y:e.clientY};render3D();});
  const endDrag=()=>{drag=null;canvas.style.cursor='grab';};canvas.addEventListener('pointerup',endDrag);canvas.addEventListener('pointercancel',endDrag);
  canvas.addEventListener('wheel',e=>{e.preventDefault();robot3d.views.distance=Math.min(440,Math.max(185,robot3d.views.distance*Math.exp(e.deltaY*.001)));render3D();},{passive:false});
  canvas.addEventListener('keydown',e=>{const step=.12;if(e.key==='ArrowLeft')robot3d.views.yaw-=step;else if(e.key==='ArrowRight')robot3d.views.yaw+=step;else if(e.key==='ArrowUp')robot3d.views.pitch=Math.min(.95,robot3d.views.pitch+step);else if(e.key==='ArrowDown')robot3d.views.pitch=Math.max(-.22,robot3d.views.pitch-step);else if(e.key==='+'||e.key==='=')robot3d.views.distance=Math.max(185,robot3d.views.distance-12);else if(e.key==='-')robot3d.views.distance=Math.min(440,robot3d.views.distance+12);else return;e.preventDefault();render3D();});
  window.addEventListener('resize',render3D);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)render3D();});
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();show3DFailure('3D绘图上下文丢失，请重新打开文件');});
  drawRobot(previewState.pose);
}
function render3D(){
  if(!robot3d.ready||document.hidden)return;
  const {yaw,pitch,distance}=robot3d.views;
  const bounds=new THREE.Box3().setFromObject(robot3d.root);
  const target=new THREE.Vector3(0,(bounds.min.y+bounds.max.y)/2,0);
  const direction=new THREE.Vector3(Math.sin(yaw)*Math.cos(pitch),Math.sin(pitch),Math.cos(yaw)*Math.cos(pitch));
  const right=new THREE.Vector3(Math.cos(yaw),0,-Math.sin(yaw));
  const up=new THREE.Vector3().crossVectors(direction,right).normalize();
  const tan=Math.tan(robot3d.camera.fov*Math.PI/360)*.88;
  let fit=160;
  for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){
    const v=new THREE.Vector3(x,y,z).sub(target),near=v.dot(direction);
    fit=Math.max(fit,near+Math.abs(v.dot(right))/(tan*robot3d.camera.aspect),near+Math.abs(v.dot(up))/tan);
  }
  robot3d.effectiveDistance=Math.max(distance,fit);
  robot3d.camera.position.copy(target).addScaledVector(direction,robot3d.effectiveDistance);
  robot3d.camera.lookAt(target);robot3d.renderer.render(robot3d.scene,robot3d.camera);robot3d.frames++;
}
function setRobotView(name){
  const views={front:{yaw:0,pitch:0,distance:244},side:{yaw:Math.PI/2,pitch:.1,distance:260},back:{yaw:Math.PI,pitch:.12,distance:260},reset:{yaw:.28,pitch:.12,distance:244}};
  if(!views[name])return;robot3d.views={...views[name]};render3D();
}
function drawRobot(pose){
  const p=normalizePose(pose);previewState.pose=p;
  if(!robot3d.ready)return;
  const r=Math.PI/180,j=robot3d.joints;
  // World Y up. Positive Z rotation takes a downward limb to the right.
  // Therefore the sign is opposite to the old Canvas Y-down rotation.
  j.ll.rotation.z=(p.ll-90)*r;j.rl.rotation.z=(p.rl-90)*r;
  j.lh.rotation.z=-handLift(p.lh)*r;j.rh.rotation.z=handLift(180-p.rh)*r;
  // In world coordinates X pitch negative lifts the forward (+Z) toe.
  j.lf.rotation.x=(p.lf-90)*r;j.rf.rotation.x=(90-p.rf)*r;
  // Height only: put the lowest sole on the stage. This is not a dynamics simulation.
  robot3d.root.position.y=0;robot3d.root.updateMatrixWorld(true);
  const feet=['lf','rf'].map(k=>new THREE.Box3().setFromObject(j[k]));
  robot3d.root.position.y=-Math.min(...feet.map(b=>b.min.y));
  robot3d.root.updateMatrixWorld(true);
  previewState.geometry={jointAngles:Object.fromEntries(SERVO_KEYS.map(k=>[k,{x:j[k].rotation.x,z:j[k].rotation.z}])),heightOffset:robot3d.root.position.y};
  render3D();
}
function show3DFailure(message){
  robot3d.ready=false;
  const stage=canvas.parentElement;let node=$('robot3dFailure');
  if(!node){node=document.createElement('div');node.id='robot3dFailure';node.style.cssText='position:absolute;top:42%;left:20px;right:20px;color:#ffb020;background:#151d28;padding:18px;text-align:center;border:1px solid #654c29;border-radius:8px;';stage.appendChild(node);}
  node.textContent=message+'。2D实物存档位于 D:/jarvis/_backup/otto-choreographer-2D实物版.html';
}
try{buildRobot3D();}catch(error){console.error(error);show3DFailure('当前环境无法初始化WebGL实体预览');}

