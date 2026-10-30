'use strict';
// Dependency-free static checks and deterministic validation fixtures.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),cp=require('node:child_process'),crypto=require('node:crypto');
const htmlPath=path.resolve(process.argv[2]||path.join(__dirname,'..','otto-choreographer.html'));
const out=path.resolve(process.argv[3]||path.join(__dirname,'results','static-'+Date.now()));
fs.mkdirSync(out,{recursive:true});
const html=fs.readFileSync(htmlPath,'utf8'),checks=[];
function check(name,passed,detail={}){checks.push({name,passed:!!passed,detail});}
const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]);
check('exactly two inline scripts',scripts.length===2);
for(let i=0;i<scripts.length;i++){
 const p=path.join(out,'script-'+i+'.cjs');fs.writeFileSync(p,scripts[i],'utf8');
 const result=cp.spawnSync(process.execPath,['--check',p],{encoding:'utf8'});
 check('syntax script '+i,result.status===0,{stderr:result.stderr});
}
const app=scripts[1]||'';
check('no external script dependency',!/<script\b[^>]*\bsrc\s*=/i.test(html));
check('no application fetch or XHR dependency',!/(?:\bfetch\s*\(|new\s+XMLHttpRequest\b)/.test(app));
check('no restrictive viewport zoom',!/(maximum-scale\s*=\s*1|user-scalable\s*=\s*no)/i.test(html));
check('no clear confirmation',!app.includes("confirm('清空所有帧？')"));
check('robot own side mapping',app.includes("hand=dir>0?'lh':'rh',leg=dir>0?'ll':'rl',foot=dir>0?'lf':'rf'"));
check('initial and reset front-downward',([...app.matchAll(/yaw:0,pitch:\.24,distance:244/g)]).length===2);
check('fixed framing uses Home bounds',app.includes('const bounds=robot3d.framingBounds;')&&app.includes('const target=robot3d.cameraTarget;'));
check('base height computed once',app.includes('if(robot3d.baseHeight===undefined)'));
check('corrected housing and foot depth',app.includes("mesh(hip,legGeometry,blue,0,-21,3.25,'原始蓝腿')")&&app.includes('ankle.position.set(0,-31.5,3.25)'));
check('model license metadata retained',html.includes('https://creativecommons.org/licenses/by-nc-sa/4.0/')&&html.includes('小鹏 OttoRobot'));
const context=vm.createContext({});
try{
 const stand=app.match(/const STAND_POSE\s*=\s*([^;]+);/)[0];
 const start=app.indexOf('const isRecord='),end=app.indexOf('function oscCenterPose',start);
 vm.runInContext("const SERVO_KEYS=['ll','rl','lf','rf','lh','rh'];"+stand+app.slice(start,end),context,{timeout:1000});
 const validate=value=>vm.runInContext('validateSequence('+JSON.stringify(value)+')',context,{timeout:1000});
 const good={a:[{s:{lh:160},v:450,d:100},{osc:{a:{lf:20},o:{lf:100},ph:{lf:90},p:300,c:1},d:0}],d:70};
 check('sparse fixture retained',JSON.stringify(validate(good))===JSON.stringify(good));
 const defaults=validate({a:[{s:{lh:45}},{osc:{a:{lh:10}}}]});
 check('implementation defaults',defaults.a[0].v===1000&&defaults.a[1].osc.p===300&&defaults.a[1].osc.c===8&&defaults.d===0);
 for(const bad of [null,{}, {a:[{s:{lh:'160'}}]}, {a:[{s:{lh:181}}]}, {a:[{s:{unknown:90}}]}, {a:[{s:{lh:20},v:0}]}, {a:[{osc:{a:{lh:9}}}]}, {a:[{osc:{a:{lh:10},p:99}}]}, {a:[{osc:{a:{lh:10},c:0}}]}, {a:[{s:{lh:20},osc:{a:{lh:20}}}]}, {a:[],d:600001}, {a:[],extra:true}]){
  let rejected=false;try{validate(bad);}catch(e){rejected=true;}check('invalid fixture '+checks.length,rejected);
 }
}catch(e){check('validation fixture harness',false,{error:String(e)});}
const report={passed:checks.every(c=>c.passed),count:checks.length,checks,html:htmlPath,sha256:crypto.createHash('sha256').update(fs.readFileSync(htmlPath)).digest('hex'),scope:'syntax/static/validation only; no browser, WebSocket, firmware or likeness proof'};
fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2),'utf8');
console.log(JSON.stringify(report,null,2));process.exitCode=report.passed?0:1;
