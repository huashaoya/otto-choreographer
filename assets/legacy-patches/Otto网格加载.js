// Mesh geometry extracted unscaled from 小鹏 OttoRobot 3MF.
// CC BY-NC-SA 4.0; coordinate conversion is rigid, no shape reconstruction.
const OTTO_MESH = __MESH_DATA__;
function nativeGeometry(name){
  const p=OTTO_MESH[name];
  const decode=(s,Type)=>{const b=atob(s),a=new Uint8Array(b.length);for(let i=0;i<b.length;i++)a[i]=b.charCodeAt(i);return new Type(a.buffer);};
  const g=new THREE.BufferGeometry();
  const src=decode(p.positions,Float32Array),v=new Float32Array(src.length);
  // CAD: x right, y back, z up. WebGL: x right, y up, z forward.
  for(let i=0;i<src.length;i+=3){v[i]=src[i];v[i+1]=src[i+2];v[i+2]=-src[i+1];}
  g.setAttribute('position',new THREE.BufferAttribute(v,3));
  g.setIndex(new THREE.BufferAttribute(decode(p.indices,Uint32Array),1));g.computeVertexNormals();g.computeBoundingBox();
  return g;
}
