const wait=ms=>new Promise(r=>setTimeout(r,ms)),checks=[];
const check=(name,ok,detail)=>{checks.push({name,passed:!!ok,detail});if(!ok)throw Error(name+JSON.stringify(detail));};
const rect=el=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height};};
const stage=document.getElementById('robotStage'),vp=document.getElementById('robotViewport'),btn=document.getElementById('stageFullscreen');
const sequence=JSON.stringify(buildSequence()),pose=JSON.stringify(state.pose),normal=rect(vp);
check('普通画布铺满视口',Math.abs(canvas.clientWidth-vp.clientWidth)<=1&&Math.abs(canvas.clientHeight-vp.clientHeight)<=1,{canvas:rect(canvas),viewport:normal});
check('普通中栏无固定520上限',innerWidth<1101||vp.clientWidth>520,{width:vp.clientWidth});
btn.click();await wait(180);const native=document.fullscreenElement===stage;
check('全屏入口可用',native||stage.classList.contains('stage-expanded'),{native});
check('全屏铺满窗口',Math.abs(stage.clientWidth-innerWidth)<3&&Math.abs(stage.clientHeight-innerHeight)<3,{stage:rect(stage),window:{w:innerWidth,h:innerHeight}});
check('全屏画布与相机无拉伸',Math.abs(robot3d.camera.aspect-canvas.clientWidth/canvas.clientHeight)<.01,{aspect:robot3d.camera.aspect,canvas:rect(canvas)});
await toggleStageFullscreen();await wait(180);
check('退出恢复布局',!document.fullscreenElement&&!stage.classList.contains('stage-expanded')&&Math.abs(rect(vp).w-normal.w)<2&&Math.abs(rect(vp).h-normal.h)<2,{normal,after:rect(vp)});
check('切换不丢编舞和姿态',sequence===JSON.stringify(buildSequence())&&pose===JSON.stringify(state.pose));
// Force host-not-supported branch to verify reversible fallback.
const request=stage.requestFullscreen;stage.requestFullscreen=undefined;
try{
 await toggleStageFullscreen();await wait(100);check('受限环境降级为页面全屏',stage.classList.contains('stage-expanded'));
 document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));await wait(100);check('Esc退出页面全屏',!stage.classList.contains('stage-expanded')&&!document.body.classList.contains('stage-expanded-open'));
 await toggleStageFullscreen();await wait(100);
 for(const view of ['front','side','back','reset']){setRobotView(view);const b=robot3d.bounds;let clipped=false;for(const x of [b.min.x,b.max.x])for(const y of [b.min.y,b.max.y])for(const z of [b.min.z,b.max.z]){const p=new THREE.Vector3(x,y,z).project(robot3d.camera);if(Math.abs(p.x)>.99||Math.abs(p.y)>.99)clipped=true;}check('全屏取景完整 '+view,!clipped);}
}finally{stage.requestFullscreen=request;}
check('页面全屏退出按钮可见',stage.classList.contains('stage-expanded')&&rect(btn).y>=0&&rect(btn).y+rect(btn).h<=innerHeight,{button:rect(btn)});
return {passed:checks.every(c=>c.passed),count:checks.length,nativeFullscreenVerified:native,checks};
