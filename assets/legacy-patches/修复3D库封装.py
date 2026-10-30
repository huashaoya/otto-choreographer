from pathlib import Path
import re
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat')
p=Path(r'D:\jarvis\otto-choreographer.html');h=p.read_text(encoding='utf-8')
lib=(R/'three-0.158.0.min.js').read_text(encoding='utf-8')
# Keep comma-expression wrapper valid: replacing only warn call by void 0.
lib=re.sub(r"console\.warn\('Scripts \"build/three\.js\" and \"build/three\.min\.js\"[^\n]*?'\)", 'void 0',lib,count=1)
lib=re.sub(r'</script',r'<\\/script',lib,flags=re.I)
x=h.index('<script>');y=h.index('</script>',x)
h=h[:x]+'<script>\n'+lib+'\n'+h[y:]
p.write_text(h,encoding='utf-8',newline='')
print('库封装完整恢复，保留离线固定版本和许可证')
