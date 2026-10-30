from pathlib import Path
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat');P=Path(r'D:\jarvis\otto-choreographer.html');h=P.read_text(encoding='utf-8')
# Exact source_offset values from Metadata/model_settings.config; ground z=-89.
replacements={
"// Real 3MF mesh, millimetres, no per-part scaling. Origin: body floor at48.4.":"// Real 3MF millimetres and CAD source_offset; CAD ground z=-89 becomes worldY=0.",
"nativeGeometry('body'),white,0,69.4,0":"nativeGeometry('body'),white,0,71,0",
"0,96.4192352,0,'原始蓝顶盖天线'":"0,92.58076477050781,0,'原始蓝顶盖天线'",
"// Cap insertion geometry is designed for the top lip; its original extrema align\n  // the antenna tips with source110mm total height at neutral pose.":"// The author source_offset_z=3.5807647705078125; its CAD antenna is not inflated to110.",
"0,69.0,34.8,'LCD屏幕'":"0,70.6,34.8,'LCD屏幕'",
"eye,-6.8,70.7,35.7":"eye,-6.8,72.3,35.7",
"eye,6.8,70.7,35.7":"eye,6.8,72.3,35.7",
"navy,18.1,74.4,34.7":"navy,18.1,76,34.7",
"hip.position.set(dir*25.5,48.4,0)":"hip.position.set(dir*25.5,49,3.25)",
"const legMesh=mesh(hip,nativeGeometry('leg'),blue,0,-21,0,'原始蓝腿');legMesh.rotation.y=Math.PI;":"mesh(hip,nativeGeometry('leg'),blue,0,-21,0,'原始蓝腿');",
"ankle.position.set(0,-30.9,0)":"ankle.position.set(0,-31.5,-3.25)",
"arm.position.set(dir*49.5,80.4,13)":"arm.position.set(dir*49.5,82,13)",
"const ag=nativeGeometry('leg');ag.rotateY(Math.PI);ag.translate(0,-21,0);":"const ag=nativeGeometry('leg');ag.translate(0,-21,0);",
"dir*49.5,80.4,25.5":"dir*49.5,82,25.5",
}
for a,b in replacements.items():
 if h.count(a)!=1:raise RuntimeError(a)
 h=h.replace(a,b,1)
P.write_text(h,encoding='utf-8',newline='');print('原始CAD位置已对齐')
