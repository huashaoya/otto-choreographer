from pathlib import Path
import json,re,hashlib
R=Path(r'C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat')
P=Path(r'D:\jarvis\otto-choreographer.html');A=Path(r'D:\jarvis\_backup\otto-choreographer-2D实物版.html')
h=P.read_text(encoding='utf-8');old=A.read_text(encoding='utf-8')
rep=json.loads((R/'Otto-3D验收'/'回归'/'report.json').read_text(encoding='utf-8'))
ev=rep['shots']['desktop']['eval']['result'];assert ev['passed'] and ev['checks']==72
assert not rep['shots']['desktop']['consoleErrors']
pairs=[('预设','const PRESETS = [','function buildPresetPanel()'),('JSON','function buildSequence()','/* ============================================================\n   播放'),('播放','async function playAll()','/* ============================================================\n   WebSocket 下发'),('下发','function connectWs()','/* ============================================================\n   工具')]
checks={n:h[h.index(s):h.index(e,h.index(s))]==old[old.index(s):old.index(e,old.index(s))] for n,s,e in pairs};assert all(checks.values())
assert not re.search(r'<script[^>]+src=',h)
summary=f'''# Otto 3D升级与存档

## 使用与恢复
- 当前文件：D:\\jarvis\\otto-choreographer.html。双击Edge打开，已打开的页面需要刷新后才能加载新版。
- 2D实物版存档：D:\\jarvis\\_backup\\otto-choreographer-2D实物版.html。可直接双击查看；与升级前的原文件SHA256一致。
- 存档SHA256：{hashlib.sha256(A.read_bytes()).hexdigest()}。
- 当前SHA256：{hashlib.sha256(P.read_bytes()).hexdigest()}。

## 实现
实体WebGL模型，不是照片平面转动。白色圆角一体壳、蓝色斜顶盖、向外后仰天线、黑色屏幕圆眼、固定肩支架、橙色线材、活动臂、双瓣开口爪、蓝腿、圆顶踝板和L形脚底都有体积与遮挡。正面轮廓/配色来自用户图片；视频用于固定肩、活动臂和前伸脚掌结构对照。
Three.js固定版本渲染库已内嵌HTML，无CDN运行依赖、无外部模型加载。仍是单HTML离线打开，不依赖服务端或构建步骤，未添加账号功能。

## 操作
拖动机器人区域旋转、滚轮缩放；可点正面、侧面、背面、视角复位。画布可键盘聚焦，方向键旋转，+/-缩放。距离/俯仰有边界，姿态变化时自动保证模型不裁切。后台不渲染，无静态自转循环。WebGL失败时显示真实图片后备及明确说明，不冒称3D。

## 六轴与原功能
Home仍为ll90/rl90/lf90/rf90/lh45/rh135。手臂以肩轴绕Z旋转，腿髋绕Z旋转，脚以X轴真实翻转。已独立检查世界坐标下的左右外展、上举、脚尖翘起，而非只检查公式字符串。
预设、JSON生成与导入、播放、WebSocket下发代码逐块与2D存档一致：{json.dumps(checks,ensure_ascii=False)}。不连接、不下发真机，固件和校准未改。

## 验收
Node UTF8提取两段内嵌脚本并node --check通过。Edge实际file入口1440×900，首帧ready标记、72项页面检查全部通过；内容包括实体网格、六轴每轴0/45/90/135/180的有效矩阵和自动取景、方向、局部姿态、侧面/背面、滚轮/键盘、播放归位及停止。
模型56个mesh，约3.5万三角形；渲染信息以回归报告为准。看过首版、修订站立、侧视、举手截图，主体非空、厚度和连接可见。新增库封装问题已修复并重跑；固定版本UMD的弃用提示只针对封装选择，保留MIT许可证，无其他控制台报错。
既有8个符号检测告警和favicon缺失未改，不影响当前预览；移动端固定三栏布局未改版。没有以桌面验收推称移动端已通过。

## 保真边界
用户已接受基于图视频建模与未知背面合理补全。69×69为图片标明顶面尺寸，前壳高、部件厚度、背面和内部结构是视觉比例建模假设，不是STL/STEP扫描尺寸。本版没有物理动力学、碰撞与真实支撑求解，只用最低脚底高度接地；极端姿态可能在现实硬件中碰撞。单侧角度不得视为硬件安全保证。
因此交付是真实体3D六轴预览，不宣称机械几何和真机全动态100%相同。未做真机同步实测。
'''
(R/'Otto-3D升级验收.md').write_text(summary,encoding='utf-8')
(R/'3D升级记录.json').write_text(json.dumps({'archive':str(A),'archive_sha256':hashlib.sha256(A.read_bytes()).hexdigest(),'current':str(P),'current_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'passed':ev['passed'],'checks':ev['checks'],'unchanged':checks},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':ev['passed'],'checks':ev['checks'],'unchanged':checks,'summary':str(R/'Otto-3D升级验收.md')},ensure_ascii=False))
