# Otto 在线编舞台 — 交接文档

> **⚠️ 2026-10-31 仓库迁移注记**：本仓库已整仓迁至 `D:\jarvis\otto-choreographer\`，本文与正文中的 `D:\jarvis\otto-choreographer.*` 等路径一律按新位置解读（如 `D:\jarvis\otto-choreographer\otto-choreographer.html`）。固件/后端/`_backup` 仍在 `D:\jarvis\` 原处。本文其余内容为历史 2D 阶段记录，仅作背景。

> 写给接手的 AI：你没有本会话的任何上下文，本文档自包含。请先完整读完再动手。
> 用户协作规则：**先给方案，用户确认后再动手改代码。不要未经确认直接开工。**

---

## 1. 任务是什么

`D:\jarvis\otto-choreographer.html` 是一个**单文件、零依赖**的 Otto 机器人在线编舞台（浏览器直接打开）。功能已全部完成：

- 左栏：6 个舵机角度滑块 + 16 个预设动作按钮（姿态库）
- 中栏：Canvas 2D 机器人预览（6 舵机联动）+ 播放/停止
- 右栏：时间轴（姿态帧/振荡帧，可增删排序编辑）+ 序列 JSON 实时生成/导入
- 顶部：WebSocket 直连机器人下发（`ws://设备IP:8080/ws`）

**用户当前的不满只有一个：中栏 Canvas 里画出来的机器人"还是不像"实物（用户发过实物照片，见 §2）。用户已经迭代反馈了多轮，你要做的是把预览画得"百分百还原"实物，并保证舵机方向与真机一致。其他功能不要动。**

---

## 2. 实物照片要点（用户会发图给你，这里是文字备份）

实物 = 「OTTO机器人 款式二」（淘宝白色+蓝色款），正面照，带尺寸标注：

| 部位 | 实物特征 |
|---|---|
| 头/身体 | 一体方形白壳，截面 69×69mm，圆角；总高 110mm，总宽 115mm（含臂） |
| 顶盖 | 蓝色，**梯形斜面（上窄下宽）**，与身体之间有一条深色接缝 |
| 天线 | 两根蓝色短天线，从顶盖两侧**向外后方**斜出，呈 V 形 |
| 屏幕 | 黑色方形，占头宽约 55-60%，位置居中略偏下 |
| 眼睛 | 两个**大**青色圆（直径≈屏宽 35-40%），在屏幕内接近垂直居中，间距较近 |
| 肩 | 身体两侧上部各一个**白色圆形肩盖**（突出身体轮廓），肩后露出橙色线材 |
| 手臂 | 从肩盖自然垂下、微微外张（约 15-25°）；白色；末端是**圆爪**（像连指手套，末端有两瓣），不是尖爪 |
| 大腿 | **蓝色**，占腿长的大部分（从身体底延伸到接近地面），上有深蓝螺丝孔 |
| 踝/小腿 | 白色，很短 |
| 脚 | 白色 L 形，**脚尖朝前**（正面视角看到的是脚的正面窄面 + 底板边缘），脚面上有蓝色圆点 |
| 材质 | 光面塑料，白色部分有柔和反光 |

---

## 3. 固件真实角度定义（这是"方向对不对"的唯一标准）

来源：`D:\jarvis\xiaozhi-esp32\main\boards\otto-robot\otto_movements.cc`（我已逐行核对过，**以下数据可信**）。

### 3.1 关键宏
```cpp
#define HAND_HOME_POSITION 45   // otto_movements.cc L11
```

### 3.2 六个舵机的语义（servo_sequences 工具描述字符串 + 实现反推）

| 键 | 部位 | 0° | 45°/135° | 90° | 180° |
|---|---|---|---|---|---|
| `ll` | 左腿 | 完全外展 | — | 中立（垂直） | 完全内收 |
| `rl` | 右腿 | 完全内收 | — | 中立（垂直） | 完全外展 |
| `lf` | 左脚 | 完全翘起 | — | 平放 | 完全下压 |
| `rf` | 右脚 | 完全下压 | — | 平放 | 完全翘起 |
| `lh` | 左手 | 完全下勾 | **45°=自然垂下** | 侧平举 | 完全上举 |
| `rh` | 右手 | 完全上举 | **135°=自然垂下** | 侧平举 | 完全下勾 |

**注意 lh 与 rh 的角度定义是完全镜像相反的。**

### 3.3 真机动作的实测角度（写预设时照抄这些）

```
Home(hands_down=true) 站立 = {ll:90, rl:90, lf:90, rf:90, lh:45, rh:135}   ← 真机开机默认
HandsUp（双手举起）        = {lh:170, rh:10}
HandWave(LEFT) 挥手        = lh 振荡中心 160、振幅 20、周期 300ms、5 个周期
HandWave(RIGHT) 挥手       = rh 振荡中心 20、振幅 20
Greeting(LEFT) 打招呼      = 脚 {lf:150, rf:150}，然后 lh 振荡(中心160 A20)
Shy(LEFT) 害羞             = 脚 {lf:150, rf:150}，双手垂下位振荡(中心45/135 A20)
Jump 起跳瞬间              = {lf:150, rf:30}
bend1→bend2 弯腰           = {lf:62, rf:35} → {lf:62, rf:105}
腿部/脚部振荡安全规则       = 腿(ll/rl)振荡时必须有一只脚锁在 90°，否则损坏舵机
```

页面里的 `STAND_POSE` 常量（HTML L362）= `{ll:90, rl:90, lf:90, rf:90, lh:45, rh:135}`，全局引用它，**不要把站立写成全 90**（全 90 时真机手臂是侧平举）。

---

## 4. 当前代码结构（48.5 KB / 1510 行）

### 4.1 关键函数行号

```
L351  const SERVOS        6 个舵机的名称/描述/左右侧
L362  const STAND_POSE   真机 Home 站立姿态（全局基准）
L385  drawGrid           网格背景
L405  roundRect          圆角矩形 path 工具
L432  handLift           手臂舵机角→画布角的分段映射（见 §5.3）
L442  drawLeg            画一条腿（大腿+踝+脚）
L531  drawArm            画一条臂（弯臂+圆爪）
L594  drawRobot          ★ 主绘制函数（映射公式、身体、屏幕、顶盖、肩盖都在这）
L812  buildServoPanel    生成滑块
L851  const PRESETS      16 个预设动作（角度已按 §3.3 真机标定）
L1179 buildSequence      时间轴 → 下发 JSON
L1199 parseSequence      JSON → 时间轴
L1274 animateTo          播放时的姿态插值
L1289 animateOsc         振荡帧的画布演示
L1333 connectWs          WebSocket 连接
L1361 sendSequence       下发（JSON-RPC 包裹 servo_sequences）
L1511 init               入口（含内置示例序列）
```

### 4.2 下发协议（已按固件 websocket_control_server.cc 核实）

```js
ws = new WebSocket(`ws://${ip}:8080/ws`);
ws.send(JSON.stringify({
  type: 'mcp',
  payload: {
    jsonrpc: '2.0', id: N, method: 'tools/call',
    params: { name: 'self.otto.servo_sequences',
              arguments: { sequence: JSON.stringify(序列对象) } }
  }
}));
```
注意：`arguments.sequence` 是**字符串化的 JSON**，不是对象。此功能只能在烧了 `otto-robot` 板型的真机上用（当前用户的 COM7 板子是 bread-compact-wifi-lcd，没有 Otto 工具）。

### 4.3 序列 JSON 格式（固件 self.otto.servo_sequences 的入参）

```json
{
  "a": [
    {"s": {"ll":90,"rl":90,"lf":90,"rf":90,"lh":45,"rh":135}, "v":800, "d":100},
    {"osc": {"a":{"lh":20}, "o":{"lh":160}, "p":300, "c":5.0}, "d":100}
  ],
  "d": 0
}
```
- `s`：舵机绝对角度（可只写变化关节）；`v`：移动耗时 ms(100-3000)；`d`：帧后延迟 ms
- `osc`：`a`=振幅(10-90)、`o`=中心绝对角、`ph`=相位差、`p`=周期 ms(100-3000)、`c`=周期数(0.1-20)

---

## 5. 已踩过的坑（重要！不要重蹈覆辙）

### 5.1 canvas rotate() 的方向
Canvas 坐标系 Y 轴向下，`ctx.rotate(正角度)` 让肢体**向左倒**，负角度向右倒。肢体从 (0,0) 画到 (0,L)（初始朝下）时：
- `rotate(90°)` → 末端到 (-L, 0)（向左）
- `rotate(-90°)` → 末端到 (L, 0)（向右）

我曾按"正角度=顺时针向右"推导，导致六个舵机方向全反。**当前映射公式（已验证方向正确）：**

```js
legDegL = 90 - pose.ll;        // ll=0 → +90(左外展)，ll=180 → -90(右内收)
legDegR = 90 - pose.rl;        // rl=0 → +90(左内收)，rl=180 → -90(右外展)
footTiltL = (90 - pose.lf) * 0.35;   // 脚只做微旋示意 + sin 投影缩放
footTiltR = (90 - pose.rf) * 0.35;
footScale = 0.55 + 0.45 * sin(舵机角 * π/180);  // lf/rf=90 → 1，翘/压 → 0.55
armDegL = handLift(pose.lh);           // 正角度=向左=左臂向外
armDegR = -handLift(180 - pose.rh);    // rh 镜像
```

### 5.2 handLift 分段映射（手臂）
真机站立（lh=45）时手臂只外张约 15-25°，不是 45°。舵机角≠手臂极坐标角（有安装角）。当前实现：

```js
function handLift(x) {          // x = lh（左臂）
  if (x <= 45) return x * 0.5;              // 0→0°, 45→22.5°（自然垂下）
  if (x <= 90) return 22.5 + (x - 45) * 1.5; // 90→90°（侧平举）
  return 90 + (x - 90) * 0.889;             // 180→170°（上举）
}
```

### 5.3 其他已修复的坑
1. **脚掌不能整只绕踝旋转**：90° 时会变成横置大方块。当前画法 = 蓝大腿（绕髋转）+ 白踝块（不转）+ 白脚（正面投影：脚面竖块 + 底部横板 + 微旋 + 高度缩放）。
2. **buildSequence 曾过滤 90 值**导致站立帧下发后手不归位 → 已改为保留全部显式值（含 45/135/90）。
3. **parseSequence / playAll / animateOsc 的缺省补全**必须用 `STAND_POSE` 而不是全 90（已改）。
4. **先画腿后画身体**：身体白块要盖住大腿根部，才有"腿从身体里长出来"的效果。
5. **PowerShell 提取 `<script>` 会 GBK 乱码**（中文注释被读坏导致 node --check 假报错）。提取必须用 node：
   ```powershell
   node -e "const fs=require('fs');const html=fs.readFileSync('D:/jarvis/otto-choreographer.html','utf8');const m=html.match(/<script>([\s\S]*?)<\/script>/);fs.writeFileSync('D:/jarvis/_tmp.js',m[1],'utf8');"
   node --check "D:\jarvis\_tmp.js"
   ```

---

## 6. ★ 当前未解决的问题（接手后从这里开始）

### 6.1 幽灵块（明确的 bug，先修这个）
最新渲染截图：`D:\jarvis\otto-choreographer-current.png`。
**现象**：默认站立姿态下，两腿中间、画布水平中心（x≈cx）、身体底缘下方（canvas y≈310-378）出现一个**带蓝点的白色圆角块 + 底部横板**——结构酷似一只"脚"，但那里不该有任何东西。左右两条腿本身画得正常。

**已排查（都不是）**：
- drawLeg 只调用两次（L638-639），参数个数与签名匹配（9 参）
- footTilt 在 lf=rf=90 时 = 0，无旋转位移
- 两条腿的 x = cx ± hipOff（±50px），中间块在 cx 处，不是任何一条腿
- 顶盖梯形/高光、缝隙线、肩盖、屏幕传感点的坐标都在别处
- 手臂末端（爪）位置在两侧 y≈222，不在中间

**下一步建议**：用二分法注释 drawRobot 的各个绘制段重新截图定位；或在 drawLeg 开头 `console.log(x, y)` 配合 headless console 输出；重点怀疑 **ctx.save/restore 不配对导致的变换残留**（drawLeg 内部 L446 的 save 与 L524 的 restore 之间有 translate/rotate，若某条路径提前 return 会漏 restore）。

### 6.2 还原度（用户的主诉，需对照 §2 逐项修）
当前版本与实物还有差距的点（我的判断，供参考）：
- **脚底板太宽**（42px 横条），看起来像"滑雪板"；实物脚底板只比脚面略宽
- 手臂弯臂的弯曲方向/幅度与实物爪的朝向需要再对照
- 天线角度（实物更向后仰）、肩盖大小可再调
- 整体质感（白色反光、蓝色的明暗）可再加一层渐变

**改外观时唯一不许破坏的**：§5.1 的映射公式和 §3 的角度语义。用户对"方向对不对"非常敏感，已两次因方向问题打回。

---

## 7. 验证工作流（每次修改后必做）

```powershell
# 1. JS 语法检查（必须用 node 提取，PowerShell 提取会乱码假报错）
node -e "const fs=require('fs');const html=fs.readFileSync('D:/jarvis/otto-choreographer.html','utf8');const m=html.match(/<script>([\s\S]*?)<\/script>/);fs.writeFileSync('D:/jarvis/_tmp.js',m[1],'utf8');"
node --check "D:\jarvis\_tmp.js"

# 2. headless Edge 截图（浏览器在 C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe）
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,900 --virtual-time-budget=4000 --screenshot="D:\jarvis\_check.png" "file:///D:/jarvis/otto-choreographer.html"

# 3. 用读图工具查看 _check.png，对照实物图逐项检查后清理临时文件
```

**验收标准（用户的原话是"百分百还原"）**：把 `_check.png` 与用户发的实物照片并排对比，头身比、屏幕/眼睛占比、顶盖形状、肩盖、垂下的手臂、蓝大腿+白脚的配色分段都要对得上；默认姿态（站立）应与实物照片的站姿一致（手臂垂下微外张、腿垂直、脚平放）。

---

## 8. 环境信息

- 文件：`D:\jarvis\otto-choreographer.html`（改这一个文件就够，无构建步骤）
- 截图存档：`D:\jarvis\otto-choreographer-current.png`（= 接手时的渲染状态）
- 固件源码（只读参考）：`D:\jarvis\xiaozhi-esp32\main\boards\otto-robot\`
  - 角度定义：`otto_controller.cc` L669-705（servo_sequences 工具描述）
  - 动作实测角度：`otto_movements.cc`（`HAND_HOME_POSITION` 在 L11）
- 用户环境：Windows，PowerShell，Edge 在 `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`，Node v24 可用
- 用户偏好：中文交流、简洁、成品交付、**先方案后动手**
