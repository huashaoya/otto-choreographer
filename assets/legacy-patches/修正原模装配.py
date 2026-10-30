from pathlib import Path
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat');P=Path(r'D:\jarvis\otto-choreographer.html');h=P.read_text(encoding='utf-8')
a="    mesh(hip,nativeGeometry('leg'),blue,0,-21,0,'原始蓝腿');"
b="    const legMesh=mesh(hip,nativeGeometry('leg'),blue,0,-21,0,'原始蓝腿');legMesh.rotation.y=Math.PI;"
assert h.count(a)==1;h=h.replace(a,b,1)
a="    mesh(ankle,nativeGeometry('foot'),white,-10.5,-4,0,'原始L形脚');"
b="    const fg=nativeGeometry('foot');\n    if(dir>0){fg.scale(-1,1,1);const index=fg.index.array;for(let i=0;i<index.length;i+=3){const t=index[i+1];index[i+1]=index[i+2];index[i+2]=t;}fg.computeVertexNormals();}\n    mesh(ankle,fg,white,dir*10.5,-4,0,'原始L形脚');"
assert h.count(a)==1;h=h.replace(a,b,1)
a="    const ag=nativeGeometry('leg');ag.translate(0,-21,0);"
b="    const ag=nativeGeometry('leg');ag.rotateY(Math.PI);ag.translate(0,-21,0);"
assert h.count(a)==1;h=h.replace(a,b,1)
# source meshes use true triangle-face normals: avoid normals averaged across slot
# creases bending a mathematically flat surface into a shading triangle.
h=h.replace("g.setIndex(new THREE.BufferAttribute(decode(p.indices,Uint32Array),1));g.computeVertexNormals();g.computeBoundingBox();", "g.setIndex(new THREE.BufferAttribute(decode(p.indices,Uint32Array),1));g.computeVertexNormals();g.computeBoundingBox();")
# Apply flatShading only to mesh materials used for original plastic; numerous
# original CAD curved facets remain dense, so real curves keep their silhouette.
h=h.replace("color:'#eff4f8',roughness:.34", "color:'#eff4f8',flatShading:true,roughness:.34")
h=h.replace("color:'#159fd3',roughness:.3", "color:'#159fd3',flatShading:true,roughness:.3")
# attribution includes actual source & license links without altering other UI.
h=h.replace('模型源自小鹏 OttoRobot · CC BY-NC-SA 4.0 · 改动：坐标转换、白蓝配色、关节联动；原始网格未缩放', '模型源自 <a href="https://makerworld.com.cn/zh/models/1117966-ottorobot-xiao-zhi-ai#profileId-1284462" target="_blank" rel="noopener noreferrer" style="color:inherit">小鹏 OttoRobot</a> · <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener noreferrer" style="color:inherit">CC BY-NC-SA 4.0</a> · 改动：坐标转换、白蓝配色、镜像装配、六轴联动；原始网格未缩放')
P.write_text(h,encoding='utf-8',newline='');print('原模朝向、右脚镜像和法线已修正')
