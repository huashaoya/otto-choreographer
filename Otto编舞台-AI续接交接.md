# Otto 编舞台：AI 续接交接文档

> 写给接手 AI：本文不要求你继承上一会话或相信历史“已完成”标签。先读取现版文件、检查版本，再按用户下一条需求继续。不要直接运行历史补丁。
>
> **当前结论：单文件 3D 编舞台及维护文档已交付，离线功能回归通过；商家实物完整侧面、圆润双瓣爪和真机运动一致性仍未验收。**

## 1. 一分钟接手摘要

- 唯一生产源码与运行入口：`D:\jarvis\otto-choreographer\otto-choreographer.html`。原生 JS、内联 CSS、内嵌 Three.js 与五类原始网格，可离线直接打开，无 npm 构建。
- 当前入口：`file:///D:/jarvis/otto-choreographer/otto-choreographer.html`。
- 用户已选“单文件项目维护”：不能擅自拆 JS/CSS、引入 npm 工程或运行时 CDN，也不能改固件、服务端和现有 Git 配置。
- 使用说明：`D:\jarvis\otto-choreographer\README.md`；变更记录：`D:\jarvis\otto-choreographer\CHANGELOG-otto.md`；测试入口：`D:\jarvis\otto-choreographer\otto-tests\run.py`。
- 旧 `D:\jarvis\otto-choreographer\otto-编舞台-交接文档.md` 是历史 2D 文档，已保留；它的旧公式、行号、零依赖、“实测/百分百”结论不能覆盖现版。
- 最新代码末次变化为腿脚深度对齐，后续项目维护没有修改 HTML。本次交接也只新增本文。
- 页面没有自动保存和撤销。**不要擅自刷新用户正在使用的页面，或清空、导入其未保存编舞。** 用独立测试浏览器检查。
- 历史未完成项是“重新校准 Otto 侧面装配”。仅有本地实现断言，不能标成实物 1:1 完成。
- 本次用户只要求交接，没有要求执行新改动。收到下一条明确需求再动手；若只说“继续”，先确认要继续哪项，不自动进行真机操作。

### 版本指纹（本次交接时已重新核验）

- 文件大小：4,072,268 bytes；1446 行。
- SHA256：`A528E7066253225A0063E24DAA25831BA409688F0056E5DC60622B99FE0163B6`。
- 这些是快照，不是永久版本号。接手时若不同，说明现场可能更新，先比较差异，不能用旧备份覆盖新工作。

```powershell
Get-FileHash -LiteralPath "D:\jarvis\otto-choreographer\otto-choreographer.html" -Algorithm SHA256
python "D:\jarvis\otto-choreographer\otto-tests\run.py" --static-only
```

## 2. 用户目标与协作约定

项目起点是 Canvas 2D 编舞台：用户要求修幽灵块，并根据实物照片、视频还原 Otto。随后用户要求存档 2D，改为可旋转、缩放的实体 3D，再反复指出脚转向、侧面、左右、相机、腿壳和脚架问题。用户对“方向正确”和真实外观非常敏感。

- 左右以**机器人自身**为准：正面看，自身左手/左腿/左脚在画面右侧。
- 改角度、选择帧和播放时，相机位置/朝向与整机基座必须固定；不能自动居中、拉远或贴地补偿。
- 初始/复位视角为正面俯视，最终 pitch=0.24 rad；不要恢复早期 0.12。
- 清空不弹确认；已移除的文案/提示/按钮不能无故恢复。
- 原预设、JSON键和下发协议保留；模型调整不等于允许改运动数据。
- 原始要求曾强调先方案后改，后续逐项明确命令授权了局部直接修改。**不要把旧文档理解为每个小改都重问，也不要把完全访问理解为任意扩范围。** 结构、协议、真机或大范围方案变化须先明确目标。
- 回复中文、简洁、开头先总结进度；主动检查，少问已确定的问题；交付真实成品和证据。
- 仅照片/视频不能证明未知背面的扫描精度。不得再次承诺未经测量的“百分百所有角度一致”。

## 3. 接手阅读顺序与权威来源

1. 本文，确定当前状态和边界。
2. `README.md`、`CHANGELOG-otto.md`，了解使用语义和已有修复。
3. **现版 HTML**：先定位函数名，再读取对应片段；内嵌库和网格是超长单行，不整行倾倒，不按旧 2D 行号操作。
4. `otto-tests/run.py`、受影响套件及对应报告；报告才是那次运行的权威状态。
5. 外观任务再实际打开用户实物照片/视频帧、网格三视图和现版截图，不靠本文文字臆造。

优先级：当前用户要求 + 现场文件 > 本文版本快照 > README/变更记录 > 原始模型与实物证据 > 历史总结。源码事实与外观验收是不同层次：源码中存在某个定位值不代表定位符合真机。

## 4. 已完成的实现与不能回退的修复

### 4.1 编舞数据、编辑和播放

- 修复稀疏姿态被当成完整姿态覆盖的异常；现在选择/播放继承前帧，导出不补写 Home。
- 原始 2D 幽灵块问题已随绘制修复及迁移结束，不应在现版盲目套 `ctx.save/restore` 补丁；历史某个异常变换假设没有被证明为唯一根因。若出现新幽灵块，按现版复现。
- 顶层延迟不丢失；姿态帧耗时/延迟可编辑；振荡编辑保留六轴振幅、中心和相位。
- 导入严格校验后原子替换，不接受数字字符串、未知字段或非法范围；避免不可信字符串进入 innerHTML。
- 移动/选择/删除保持索引有效和选中帧身份。
- 播放继承稀疏关节，振荡结束按中心姿态作为后续基准。
- `state.playToken` 与可取消等待修复停止后立即重播的竞争；播放中拖滑块停止旧播放并保留输入。
- 没有自动保存/撤销；导入替换时间轴；清空直接清空帧和顶层延迟，播放中先停止，不重置当前机器人姿态。

### 4.2 3D、相机、布局与 UI

- 内嵌原始网格和 Three.js，实体可旋转缩放；没有运行时网格 fetch/CDN。
- 中栏占满剩余区域；原生全屏可用，宿主拒绝时页面全屏回退，退出恢复布局且不丢数据。
- 修正机器人自身左右及世界旋转符号、左右侧面按钮；JSON字段、预设、协议不变。
- Home 包围盒/相机目标固定，基座高度初始化一次；更新姿态的 bounds 不用于自动追踪相机。
- 初始/视角复位 yaw=0、pitch=0.24、distance=244；“正面”按钮 pitch=0。
- 移除顶部快捷“站立”及绑定；姿态库“站立/归位”保留。
- 移除“拖动旋转·滚轮缩放”“点击追加”提示及舞台模型说明，占位行也移除；版权/来源移入并保留 HTML 注释。
- 四条肩部 tube 沿 Z 整体后移 21，形状不改，位于深度中部。
- 蓝腿撤销绕 Y 的 π 翻转，局部 Z 改为 +3.25；随后脚架轴由旧 -3.25 改为 +3.25，消除该处错位缝隙。没有用填充块、拉伸掩盖。
- 窄屏和编辑弹窗布局、网格解码缓存、批量重绘合并、GPU几何复用已有回归。

### 4.3 连接

- 固定 `ws://设备IP:8080/ws`，8秒连接超时、取消、旧连接事件隔离。
- 支持 IPv4/主机名输入，拒绝协议、路径、端口输入；没有直接 IPv6/WSS支持。
- 嵌套设备错误可显示；已发送、设备确认请求和动作执行完成不能混称。
- 风险振荡允许本地限幅预览，但阻止下发。保持预设原数据；“欢呼”可能触发超界检查。
- 未进行真机连接、下发、烧录、校准、急停或硬件安全测试；自动回归仅隔离 mock WebSocket。

## 5. 现版模型与坐标：修改前必须理解

### 5.1 网格来源与不确定性

五类网格为 `body / cap / leg / foot / claw`，来自小鹏 OttoRobot 原始 3MF。没有简化或单部件缩放；腿网格同时被手臂复用，**改 leg 不一定只影响腿**。

- CAD `(x,y,z)` 转 WebGL `(x,z,-y)`；单位 mm；WebGL Y向上、Z向前。
- 商家实物是圆润双瓣爪，作者原模型为多边形开口爪；使用作者原网格不等于商家款完全一致。
- `source_offset` 本身不是完整装配证据。作者原模型、商家照片、推测硬件填充需分开。
- 身体内脚舵机壳、部分装配关系属于推测，不是实测尺寸。
- 来源信息：`https://makerworld.com.cn/zh/models/1117966-ottorobot-xiao-zhi-ai#profileId-1284462`；早期参考还有 `https://oshwhub.com/txp666/ottorobot`。
- 模型许可记录为 CC BY-NC-SA 4.0：`https://creativecommons.org/licenses/by-nc-sa/4.0/`；内嵌 Three.js 是 MIT。不能把整个 HTML 统一改标 MIT，不得删除作者署名/许可。

### 5.2 现版装配数值（实现快照，不是测量结论）

全部位置在对应父节点局部坐标：

- `body` 位于 root `(0,71,0)`。
- `cap` 位于 root `(0,92.58076477050781,0)`。
- 屏幕 root `(0,70.6,34.8)`，尺寸 29.1×30×1.5；眼圆半径5.4，中心 `(±6.8,72.3,35.7)`。
- 髋轴 root `(±25.5,49,0)`，+X为自身左侧。
- 蓝腿在 hip `(0,-21,3.25)`，不绕Y翻转。
- 踝轴在 hip `(0,-31.5,3.25)`。
- 脚网格在 ankle `(dir*10.5,-4,0)`；dir>0 的脚镜像X并反转三角绕序、重算 normals。
- 手臂轴 root `(±49.5,82,0)`；臂壳复用leg，几何绕Z π后平移 `(0,-10.5,0)`。
- 爪几何绕Y -π/2、绕Z π后平移 `(0,-48.5,-3.25)`，挂在arm下。
- 橙线控制点 `(dir*36,92,3)`、`(dir*42,93.2,1)`、`(dir*47,89.6,-1)`；棕线 `(dir*36,91.4,1)`、`(dir*41,92.2,-1)`、`(dir*47,89,-3)`。

不要为了修侧面整体缩放某部件、移动所有关节或改变相机来“看似对齐”。优先确认孔轴和刚性装配关系，局部修改。

### 5.3 六轴映射

Home：`{ll:90,rl:90,lf:90,rf:90,lh:45,rh:135}`，不是全90。

```js
const r = Math.PI / 180;
j.ll.rotation.set(0, (p.ll - 90) * r, 0);
j.rl.rotation.set(0, (p.rl - 90) * r, 0);
j.lf.rotation.set(0, 0, (90 - p.lf) * r);
j.rf.rotation.set(0, 0, (90 - p.rf) * r);
j.lh.rotation.z = handLift(p.lh) * r;
j.rh.rotation.z = -handLift(180 - p.rh) * r;

function handLift(x) {
  if (x <= 45) return x * .5;
  if (x <= 90) return 22.5 + (x - 45) * 1.5;
  return 90 + (x - 90) * .889;
}
```

髋是Y轴；踝是前后Z轴，不能按想象改成X俯仰。手安装映射不是线性舵机角直转，不要丢掉45/135 Home。此为当前预览实现，尚未完成真机转轴/trim标定。

### 5.4 相机不变量

`robot3d.baseHeight` 只初始化一次；`framingBounds / cameraTarget` 捕获Home。`render3D()`使用它们，不使用当前运动包围盒重新定位。有效距离由Home适配值和用户缩放决定，`views.distance=244`不代表实际camera距离固定为244mm。

- 正面：yaw0、pitch0、distance244。
- 自身右侧：yaw -π/2、pitch0、distance260，cameraX为负。
- 自身左侧：yaw +π/2、pitch0、distance260，cameraX为正。
- 背面：yaw π、pitch0、distance260。
- 初始/复位：yaw0、pitch0.24、distance244。
- 窗口/fullscreen尺寸变化允许更新投影；关节/播放不改变相机或root。
- 不模拟步行位移、重心、碰撞或自动贴地；大动作可能出固定取景，用户可缩小。

## 6. 序列与协议：不能静默改变

详情见README；这里列容易被接手时写错的点。

- 顶层 `{a:[帧...],d:序列末延迟}`，最多1000帧。
- 姿态帧 `{s:{部分或全部六轴},v,d}`；缺省v1000ms、d0；预览继承，JSON不补Home。
- 振荡帧 `{osc:{a,o,ph,p,c},d}`，不得与同帧s/v混用。
- 未指定振荡中心为90，不是Home；相位默认0；导入p默认300ms/c默认8，新建弹窗初始500ms/5，不能混淆。
- 振荡结束以中心角作为后续基准；普通姿态线性插值。
- `s/o`：0–180整数；振幅0停用或10–90整数；ph0–360数值；v/p100–3000整数ms；c0.1–20；d0–600000整数ms。
- 未知字段、数字字符串、非法结构/范围整体拒绝，不能部分覆盖现有时间轴。
- 腿振荡未锁90脚、双腿/双脚同时大幅≥40、中心±振幅超0–180会触发风险提示/阻止下发；通过检查仍不是硬件安全保证。

```js
{
  type: 'mcp',
  payload: {
    jsonrpc: '2.0', id: N, method: 'tools/call',
    params: {
      name: 'self.otto.servo_sequences',
      arguments: { sequence: JSON.stringify(sequenceObject) }
    }
  }
}
```

`sequence`必须是字符串，不是对象。旧交接中COM口/板型状态只是历史记录，本次没有核实当前设备，不应据此操作任何串口或固件。

## 7. 源码定位与环境

当前快照函数行号仅辅助搜索；修改后会变，以函数名为准：

- `handLift` 488；`nativeGeometry` 604；`buildRobot3D` 617。
- `resize3D` 711；`render3D` 719；`setRobotView` 741；`drawRobot` 748。
- `validateOsc` 1126；`validateSequence` 1135。
- `playAll` 1234；`stopAll` 1259；`connectWs` 1279；`bindEvents` 1346；`init` 1419。
- 同时关注 `normalizePose / STAND_POSE / PRESETS / parseSequence / buildSequence / selectFrame / syncPoseToActiveFrame / moveFrame / deleteFrame / toggleStageFullscreen / sendSequence`。
- 顶部style负责布局，舞台为`#robotStage / .robot-viewport`；库与`OTTO_MESH`的巨型单行不要输出或重新格式化。

环境：Windows、PowerShell 7；Python 3.13.16；维护记录中Node为22，接手时自行确认。Edge常见路径为 `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`。Git本次查询不在PATH，未安装、未提交、未推送；存在`.git`不等于已建立独立仓库。

所有shell用PowerShell，不能用Bash。文件内容显式UTF-8，保留原文件编码/换行，不用默认编码重写HTML。路径用LiteralPath，保存/回退不能覆盖未知文件。

## 8. 自动回归与验收证据

### 8.1 可重复运行的入口

```powershell
# 任意工作目录均可执行；不连接设备、不修改生产HTML
python "D:\jarvis\otto-choreographer\otto-tests\run.py"
python "D:\jarvis\otto-choreographer\otto-tests\run.py" --static-only
python "D:\jarvis\otto-choreographer\otto-tests\run.py" --suite camera
python "D:\jarvis\otto-choreographer\otto-tests\run.py" --suite core --suite sides --suite ui
```

测试需Python3.10+、Node；完整浏览器验证另需Playwright和HTML自检`shot.py`，这些不是页面运行依赖。`run.py`以自身位置定位HTML，自动发现shot和浏览器，支持`--shot`、`--browser`、`--html`、`--outdir`。若迁移到没有shot的环境，不能冒充完整回归已运行；不要要求新增运行时依赖以绕开。

本机shot路径：
`C:\Users\Administrator\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.skills\html\scripts\shot.py`

- 浏览器检查只由shot驱动，带`--no-auto-fix`，不自动修生产HTML。
- `core/camera/sides/fullscreen/ui.js`是注入页面的async函数体，**不能直接node执行**。
- `static-check.cjs`用Node检查两段内嵌脚本语法，并VM执行当前校验逻辑fixtures。
- WebSocket仅core隔离mock，末尾恢复；没有实际设备请求。
- 每次结果写入新时间戳目录，包含summary、report和截图；显式outdir也不得覆盖已有结果。
- `otto-tests/.gitignore`只排除本测试目录results与Python缓存；不改根目录规则。
- `otto-tests.zip`只含8个测试维护文件，是交接副本，不含生产HTML、外部shot、截图或其他工程。修改测试源以后需要重新生成交接包，不能把旧zip称为最新。

### 8.2 已通过的基线，不是本次新跑

权威完整报告：`otto-tests\results\<时间戳>\summary.json`（results 不入库，历史报告已按 2026-10-31 清理决定移除）。迁移后基线 `20261031-043341-924473` 全 PASS：

- 静态27项通过。
- core68、camera22、sides18、fullscreen14、ui14，各在1440×900桌面及390×844手机重复执行通过。
- console errors/warnings均为空，报告passed=true、production_unchanged=true。
- 套件有重叠，宽窄屏重复执行；不能累计成“数百个独立测试”。
- 桌面core和手机ui截图在维护轮实际读取过。本次交接回读报告并重新核对HTML哈希，**没有再次执行全套回归，也没有新增外观/真机验收**。
- 静态独跑记录：`20261031-024705-668128`。
- 错误HTML输入（README）预期失败记录：`20261031-025545-506838`，真实exit1。它不是产品故障，也不能因为时间较晚就当成完整基线。

成功不能只看进程exit0：须读summary和各视口`eval.executed / eval.result.passed`。没有浏览器、脚本抛异常/超时时可能只打印失败并返回1而不生成最终summary，缺报告也不是通过。

### 8.3 层级边界与反例

1. 语法/fixture：代码可执行、JSON规则成立。
2. 功能回归：编辑、播放、mock连接、相机、UI实现成立。
3. 图像检查：主体非黑屏、布局/裁切/可见缝隙是否合理。
4. 实物相似度：与商家照片/视频对应视角、比例、形状对照；未完整通过。
5. 真机一致性与安全：硬件轴、trim、动作、碰撞、急停；未执行。

不能用1/2替代4/5；某项断言若本来固化了错误装配，不能保留错误只为了让测试通过。修改装配时应依据新证据更新受影响断言，说明旧假设为何失效，而不是删测掩盖问题。

全屏回归特别注意：首次native申请与强制页面回退是两个不同分支。自动点击第二次原生申请可能因用户激活已消耗而拒绝，不据此宣称首次原生没成功；也不能把页面回退成功称为原生成功。读报告里的`nativeFullscreenVerified`。

## 9. 实物、网格和截图材料位置

以下素材在本次交接中已检查存在。共同根目录：
`C:\Users\Administrator\Doubao\chats\2026-10-28\new-chat`

相对于此根目录：

- `Otto原始模型.3mf`：原始模型备份。
- `Otto真实网格.json`：提取网格；`Otto模型尺寸.json`：网格尺寸资料。
- `otto-核查\实物部件核查.jpg`：实物参考提取图。
- `otto-核查\视频-00秒.jpg`、`视频-24秒.jpg`、`视频-48秒.jpg`：实物视频抽帧；不要把这些静态帧说成完整运动验证。
- `leg-原始网格.png`、`foot-原始网格.png`：网格三视图。
- `Otto腿脚对齐\侧面检查\otto-choreographer_desktop.png`：最近腿脚对齐的右侧截图。
- `Otto腿脚对齐\左侧复核\otto-choreographer_desktop.png`：对应左侧截图。

现版完整回归报告按次生成于 `otto-tests\results\<时间戳>\`（results 不入库，历史报告已按 2026-10-31 清理决定移除；迁移后基线 `20261031-043341-924473` 全 PASS）。

原照片曾在微信临时E盘路径，后来不可访问；不要死守过期路径。上列本地素材可先使用，若关键视角/细节仍缺，向用户索取对应实物侧面或尺寸，不能猜造。视频语义理解曾在末尾出错，像素和真实帧优先于文字摘要；曾有浏览器MP4黑画面，通过抽帧取得可读图片，不把黑画面当成无素材。

历史2D截图 `otto-choreographer-current.png / -preview.png` 已按 2026-10-31 清理决定移出工作区（仅存 git 历史），本就不代表当前3D。旧过程脚本（legacy-patches，同日移出，仅存 git 历史）、旧验收MD和旧导出JS也不是当前源码。

## 10. 剩余问题与建议续接顺序

### 10.1 真正未完成

- 商家实物完整侧面、肩臂和爪朝向是否一致，仍未1:1验收；左右侧多次被用户否决。
- 作者多边形爪与商家双瓣圆爪差异未解决。
- 未知背部、深度、装配尺寸没有完整测量。
- 真机舵机转向、trim、运动结束状态、相位与安全未校准。
- 没有自动保存、撤销、拖拽时间轴或设备急停；这不是本轮授权新增项。

### 10.2 如果用户继续侧面校准

1. 保护用户编舞；读取现版模型函数和实际素材，取得Home正面、左右侧、背面新截图。
2. 统一对应视角/比例，列“可见证据/推测/缺失”而不是立刻凭目测整体翻转。
3. 分离壳体朝向、孔轴位置、爪变体和相机误差；优先刚性装配，避免改变外观掩盖转轴问题。
4. 对关键未知向用户只问必需信息；明确哪些可以合理补全、哪些不能声称实测。
5. 先备份，再局部修改；保持相机固定、自身左右、JSON和协议。
6. 运行受影响套件，实际读图，再按影响范围完整回归；给用户看匹配视角的对照，明确仍未验收的部分。

不要再以“18项左右测试通过”“网格尺寸保留”来证明商家实物完全一致。不要擅自连接设备来获得更多证据。

## 11. 备份与项目边界

备份目录：`D:\jarvis\_backup`。本次确认的关键备份包括：

- `otto-choreographer-2D实物版.html`
- `otto-choreographer-整体优化前.html`
- `otto-choreographer-全屏修复前.html`
- `otto-choreographer-自身左右修正前-20261031-012120.html`
- `otto-choreographer-固定相机基座前-20261031-012730.html`
- `otto-choreographer-肩线后移前-20261031-020720.html`
- `otto-choreographer-腿壳前后翻正前-20261031-021110.html`
- `otto-choreographer-腿脚对齐前-20261031-022722.html`

这些是变更前快照，不是另一个生产入口；不同版本可能没有后续修复。恢复前必须比较、保护用户JSON，并另外存当前版。禁止把旧补丁重新运行覆盖现版。

`D:\jarvis`内的`xiaozhi-esp32`、`xiaozhi-esp32-server`、`audio-work`、日志、其他文件和`.git`都不能作为“整理项目”顺手改动。固件可在用户明确需要时只读参考；旧文档所谓“已实测”的角度必须重新查证，不能执行烧录/串口/下发。

若换机器/云端AI：本地绝对路径不会自动可访问。用户需要随交接提供**唯一HTML、README、CHANGELOG、测试目录和必要实物/网格素材**；本文本身不含完整源代码、网格或图片。保持生产结构，不把文档当成足够重造项目的材料。没有附件时先索取，而不是凭本文复刻覆盖。

## 12. 给下一个 AI 的可粘贴开场指令

```text
请先完整读取 D:\jarvis\otto-choreographer\Otto编舞台-AI续接交接.md、README.md、CHANGELOG-otto.md，并检查当前 otto-choreographer.html 的SHA256。唯一生产入口保留单文件，不拆JS/CSS，不改固件、服务端或现有Git配置。

根据我接下来给出的具体需求继续。修改前读取当前函数与真实素材，不运行旧补丁、不刷新我未保存的编舞。左右按机器人自身；关节变化不移动相机和整机基座；初始俯角0.24；原预设、JSON和协议保留。

实物侧面和商家双瓣圆爪仍未1:1验收，真机未测试；不得用功能回归通过替代外观或硬件验收。改前备份、改后运行受影响回归并实际看截图，更新CHANGELOG，交付最新唯一HTML。先总结现场状态与准备处理的对象，再继续。
```

## 13. 本次交接编制依据

本次直接读取：现版README、CHANGELOG、旧2D交接、现版3D装配/映射/相机函数、统一测试入口及完整回归summary；核验生产文件指纹、素材存在性和备份清单。历史用户反馈依据同一对话，明确区分实现已完成与实物未验收。

本次仅新增本交接文档，没有重新修改HTML、测试或其他工程；无新增真机/外观结论。本文不取代现场读取和用户的新指令。
