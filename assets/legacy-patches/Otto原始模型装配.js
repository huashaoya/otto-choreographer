  // Real 3MF mesh, millimetres, no per-part scaling. Origin: body floor at48.4.
  mesh(root,nativeGeometry('body'),white,0,69.4,0,'原始白壳与固定肩');
  // Cap insertion geometry is designed for the top lip; its original extrema align
  // the antenna tips with source110mm total height at neutral pose.
  mesh(root,nativeGeometry('cap'),blue,0,96.4192352,0,'原始蓝顶盖天线');
  block(root,29.1,30,1.5,.6,screen,0,69.0,34.8,'LCD屏幕');
  mesh(root,new THREE.CircleGeometry(5.4,64),eye,-6.8,70.7,35.7,'左圆眼');
  mesh(root,new THREE.CircleGeometry(5.4,64),eye,6.8,70.7,35.7,'右圆眼');
  cylinder(root,.45,.4,navy,18.1,74.4,34.7);
  const pivots={};
  // Hip rotates about vertical Y. Foot horn axis is fore-aft Z (not X pitch).
  [-1,1].forEach(dir=>{
    const hand=dir<0?'lh':'rh',leg=dir<0?'ll':'rl',foot=dir<0?'lf':'rf';
    const hip=new THREE.Group();hip.position.set(dir*25.5,48.4,0);root.add(hip);pivots[leg]=hip;
    mesh(hip,nativeGeometry('leg'),blue,0,-21,0,'原始蓝腿');
    // Mesh CAD hole centre: foot=(10.5,±23.4,4); z-up converts to Y.
    // Native foot mesh is translated so both hole centres stay on the ankle Z axis.
    const ankle=new THREE.Group();ankle.position.set(0,-30.9,0);hip.add(ankle);pivots[foot]=ankle;
    mesh(ankle,nativeGeometry('foot'),white,-10.5,-4,0,'原始L形脚');
    cylinder(ankle,2.5,.8,blue,0,0,25.9);
    cylinder(ankle,.68,.8,blue,0,6.1,25.9);
    // Micro-servo casing inside the native leg opening: inferred hardware fill.
    block(hip,12.2,22,22,1,navy,0,-27,0,'脚舵机壳');
    const arm=new THREE.Group();arm.position.set(dir*49.5,80.4,13);root.add(arm);pivots[hand]=arm;
    // The arm shell is the same printed leg housing in the source kit (4 copies).
    const ag=nativeGeometry('leg');ag.translate(0,-21,0);
    mesh(arm,ag,white,0,0,0,'原始活动臂');
    block(arm,9,6,9,2.2,white,0,-42,0,'腕连接');
    // Native claw plane is CAD YZ, normal X; rotate it rigidly into front-facing XY.
    const cg=nativeGeometry('claw');cg.rotateY(-Math.PI/2);cg.rotateZ(Math.PI);cg.translate(0,-57,0);
    mesh(arm,cg,white,0,0,0,'原始开口爪');
    tube(root,[[dir*36,92,24],[dir*42,93.2,22],[dir*47,89.6,20]],.7,orange);
    tube(root,[[dir*36,91.4,22],[dir*41,92.2,20],[dir*47,89,18]],.55,brown);
    cylinder(root,2,.8,white,dir*49.5,80.4,25.5);
  });
