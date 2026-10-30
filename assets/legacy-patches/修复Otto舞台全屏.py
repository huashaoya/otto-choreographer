from pathlib import Path
P=Path(r'D:\jarvis\otto-choreographer.html');h=P.read_text(encoding='utf-8')
def rep(a,b):
 global h
 if h.count(a)!=1:raise RuntimeError('补丁定位不唯一 '+a[:70])
 h=h.replace(a,b)
rep('<section class="panel stage">','<section class="panel stage" id="robotStage">\n    <div class="robot-viewport" id="robotViewport">')
# Keep the original embedded fallback untouched; close wrapper after its image line.
a=h.index('<img id="robotFallback"');b=h.index('\n',a);h=h[:b]+'\n    </div>'+h[b:]
rep('<div class="stage-controls" id="view3dControls">','<div class="stage-controls" id="view3dControls"><button type="button" id="stageFullscreen" aria-pressed="false">全屏</button>')
rep('<div style="font-size:10px;color:var(--dim);max-width:520px;text-align:center">模型源自','<div class="model-note">模型源自')
rep('</style>', '''
  /* Canvas dimensions belong to the viewport, not the old 520x460 bitmap. */
  #robotStage { display:grid;grid-template-rows:minmax(0,1fr) auto auto auto;align-items:stretch;justify-content:stretch;gap:10px;padding:12px;min-width:0;min-height:0; }
  .robot-viewport { position:relative;min-width:0;min-height:0;overflow:hidden;width:100%;height:100%;background:var(--panel); }
  #robotStage .robot-viewport canvas { position:absolute;inset:0;display:block;width:100%;height:100%;max-width:none;max-height:none;aspect-ratio:auto;filter:none; }
  #robotStage .robot-viewport canvas[hidden] { display:none; }
  #robotStage #robotFallback { position:absolute;inset:0;width:100% !important;height:100% !important;object-fit:contain; }
  #robotStage .model-note { max-width:none;padding:0 6px;line-height:1.4; }
  #robotStage:fullscreen, #robotStage.stage-expanded { width:100vw;height:100dvh;min-height:0;max-height:none;border:0;border-radius:0;background:var(--panel);padding:12px; }
  #robotStage.stage-expanded { position:fixed;inset:0;z-index:90; }
  body.stage-expanded-open { overflow:hidden !important; }
  @media(max-width:1100px) { #robotStage { grid-template-rows:minmax(300px,60vh) auto auto auto; } }
  @media(max-width:600px) { #robotStage { grid-template-rows:minmax(260px,52vh) auto auto auto;padding:8px;gap:8px; } }
  #robotStage:fullscreen, #robotStage.stage-expanded { grid-template-rows:minmax(0,1fr) auto auto auto; }
  @media(max-height:500px) { #robotStage:fullscreen .model-note,#robotStage.stage-expanded .model-note { display:none; } }
</style>''')
rep('robot3d.effectiveDistance=Math.max(distance,fit);','// Preserve zoom ratio while fitting the entire available viewport.\n  robot3d.effectiveDistance=Math.max(fit,fit*distance/244);')
# CSS wrapping does not change failure message ancestry function needs stage target.
rep('const stage=canvas.parentElement;let node=',"const stage=$('robotViewport');let node=")
rep('function bindEvents() {', '''// Fullscreen is user-triggered only. A reversible in-page fallback covers
// hosts that disable the native Fullscreen API. It never reloads the file.
let stagePreviousFocus=null,stagePreviousScroll=0;
function syncStageFullscreen(){
  const stage=$('robotStage'),full=document.fullscreenElement===stage||stage.classList.contains('stage-expanded');
  $('stageFullscreen').textContent=full?'退出全屏':'全屏';$('stageFullscreen').setAttribute('aria-pressed',String(full));
  document.body.classList.toggle('stage-expanded-open',full);queueRender3D();
}
async function toggleStageFullscreen(){
  const stage=$('robotStage');
  if(document.fullscreenElement===stage){try{await document.exitFullscreen();}catch(e){toast('退出全屏失败，请按Esc',true);}return;}
  if(stage.classList.contains('stage-expanded')){stage.classList.remove('stage-expanded');syncStageFullscreen();window.scrollTo(0,stagePreviousScroll);stagePreviousFocus?.focus({preventScroll:true});return;}
  stagePreviousFocus=document.activeElement;stagePreviousScroll=window.scrollY;
  if(stage.requestFullscreen){try{await stage.requestFullscreen();return;}catch(e){/* host disallows fullscreen: use the same viewport in-page */}}
  stage.classList.add('stage-expanded');syncStageFullscreen();$('stageFullscreen').focus({preventScroll:true});
}
function bindEvents() {
  $('stageFullscreen').addEventListener('click',toggleStageFullscreen);
  document.addEventListener('fullscreenchange',()=>{syncStageFullscreen();if(!document.fullscreenElement){stagePreviousFocus?.focus({preventScroll:true});}});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&$('robotStage').classList.contains('stage-expanded')){e.preventDefault();toggleStageFullscreen();}});''')
# Initial view dimensions updates via ResizeObserver already observes canvas.
P.write_text(h,encoding='utf-8',newline='')
print('3D铺满与全屏补丁已写入')
