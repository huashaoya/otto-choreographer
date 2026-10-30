from pathlib import Path
import re
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat')
p=Path(r'D:\jarvis\otto-choreographer.html');h=p.read_text(encoding='utf-8')
x=h.index('/* ============================================================\n   预览：实体3D')
y=h.index('/* ============================================================\n   左侧滑块',x)
h=h[:x]+(R/'Otto实体3D预览.js').read_text(encoding='utf-8')+h[y:]
# Pinning the global build is deliberate for offline single-file use. Keep MIT
# license and warn on real renderer failure; remove this exact packaging notice only.
h=re.sub(r"console\.warn\('Scripts \"build/three\.js\" and \"build/three\.min\.js\".*?'\),\s*",'',h,count=1)
p.write_text(h,encoding='utf-8',newline='')
print('3D预览更新完成')
