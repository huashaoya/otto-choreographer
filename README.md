# Otto 在线编舞台

可离线打开的单文件六轴机器人编舞工具。**唯一源码与运行入口是 [`otto-choreographer.html`](otto-choreographer.html)**；不需要 npm、构建或本地服务。项目维护采用“单文件 HTML + 文档 + 离线回归套件”，不包含固件或服务端工程化。

> 当前 3D 是作者原始网格的装配候选，不是实物扫描结果。商家款侧面、圆润双瓣爪及真机运动同步仍未完整验收；测试通过不等于实物 1:1 或可以安全执行。

## 快速开始

1. 用支持 WebGL 的 Edge / Chrome 打开 `otto-choreographer.html`，当前入口为 `D:\jarvis\otto-choreographer\otto-choreographer.html`。
2. 页面默认载入一段打招呼示例，**不会自动播放或连接设备**。不要把示例当成已保存的个人编舞。
3. 左栏拖动六轴滑块；点击姿态库预设会将动作追加到时间轴。
4. 右栏选择帧、编辑时序、添加姿态帧或六轴振荡帧；可以上下移动、编辑或删除。
5. 点击“播放全部”仅运行本地预览；“停止预览”不会向设备发送停止命令。
6. JSON 区为只读自动生成内容。用“复制”保存文本，用“导入”粘贴序列；导入会替换当前时间轴。

**没有自动保存、撤销或持久化。刷新、重新打开、导入或清空前，先复制需要保留的 JSON。清空不弹确认，立即清空时间轴及序列延迟；不会重置当前机器人姿态。**

## 功能与界面规则

- 六轴：`ll / rl / lf / rf / lh / rh`，包含左右腿、脚、手。
- 16 项姿态库预设；顶部快捷“站立”按钮已移除，姿态库“站立”和“归位”保留。
- 真实实体 3D：拖动旋转、滚轮或 `+ / -` 缩放，画布聚焦后方向键改变视角。
- 初始及“视角复位”为正面俯视：`yaw=0`、`pitch=0.24 rad`；“正面”按钮是无俯角的正视。
- 左右均以**机器人自身**为准：正面看，左手、左腿、左脚在画面右侧；左侧面/右侧面按钮也使用此口径。
- 关节角度变化及播放不自动改变相机位置/朝向或整机基座；手动视角操作、窗口尺寸变化和全屏切换仍会更新取景。
- 基座仅在初始化时按 Home 定位；脚运动时不自动贴地，不模拟重心、步行位移、碰撞或动力学。大姿态可能超出当前固定取景范围，需手动缩小。
- 全屏使用浏览器 Fullscreen API；宿主拒绝时回退到页面全屏。点击“退出全屏”或按 Esc 返回。
- 中窄屏堆叠布局；宽屏保留左右编舞面板。
- 删除的舞台来源文案、拖动缩放提示和“点击追加”提示不再显示；模型署名及许可仍保留在 HTML 注释。

### Home 姿态与预览映射

Home 为 `{ll:90, rl:90, lf:90, rf:90, lh:45, rh:135}`，不是全 90。当前页面使用以下世界轴映射；这是实现约定，未替代真机标定。

- 髋轴：Y，`ll / rl` 的旋转为 `(angle-90) × π/180`。
- 踝轴：Z，`lf / rf` 的旋转为 `(90-angle) × π/180`。
- 手轴：Z，左手 `+handLift(lh)`，右手 `-handLift(180-rh)`。
- `handLift`：0→0、45→22.5、90→90、180→约170（度）。安装角并非精确测量。
- 蓝色腿壳使用原网格朝向，位于髋局部 `(0,-21,3.25)`；脚架轴为 `(0,-31.5,3.25)`。肩部线缆位于前后深度中部。

## 序列 JSON

可粘贴导入的示例：

```json
{
  "a": [
    {"s":{"ll":90,"rl":90,"lf":90,"rf":90,"lh":45,"rh":135},"v":800,"d":100},
    {"s":{"lh":160},"v":450,"d":100},
    {"osc":{"a":{"lh":20},"o":{"lh":160},"p":300,"c":5},"d":100},
    {"s":{"lh":45,"rh":135},"v":700,"d":0}
  ],
  "d":0
}
```

- 顶层 `a` 是动作数组，最多 1000 帧；顶层 `d` 是序列全部结束后的延迟，缺省 0。
- 姿态帧 `s` 可只写变化关节。预览从前帧继承未指定关节，但 JSON 不补写 Home。
- 姿态帧的 `v` 是移动耗时，缺省 1000 ms；帧 `d` 是帧后延迟，缺省 0。
- 振荡帧与姿态帧互斥；不能同一帧混用 `osc` 与 `s / v`。
- `osc.a` 是振幅，至少一个轴启用；`o` 是中心角，未指定轴中心默认为 90，而不是 Home；`ph` 是可选相位差，未指定默认为 0。
- 导入振荡帧的周期 `p` 缺省 300 ms、周期数 `c` 缺省 8；新增编辑弹窗的初始值是 500 ms、5 周期，二者不能混淆。
- 振荡结束以后按中心角作为后续姿态基准，普通移动采用线性插值。
- 只接受数值，不接受数字字符串；未知字段、非法范围或错误对象会在整体校验后原子拒绝，不覆盖现有编舞。

范围约束：

- `s / o`：0–180 整数。
- `osc.a`：0 停用，启用为 10–90 整数。
- `osc.ph`：0–360 数值。
- `v / osc.p`：100–3000 整数 ms。
- `osc.c`：0.1–20 数值。
- 顶层/帧 `d`：0–600000 整数 ms。

风险检查允许本地预览但阻止下发：腿振荡无任一脚锁定 90°、双腿或双脚同时振幅 ≥40、中心±振幅超出 0–180°。原预设保留不静默修改，其中“欢呼”会触发超界检查。预览限幅或通过校验不是设备安全保证。

## WebSocket 协议与边界

只有用户主动点击“连接”才会发起网络请求。主机输入支持 IPv4 或主机名，不输入协议、路径或端口；固定连接为 `ws://设备IP:8080/ws`，不支持直接输入 IPv6 / WSS。

JSON-RPC 外层封装如下：

```js
{
  type: "mcp",
  payload: {
    jsonrpc: "2.0",
    id: 1,
    method: "tools/call",
    params: {
      name: "self.otto.servo_sequences",
      arguments: { sequence: JSON.stringify(sequenceObject) }
    }
  }
}
```

`arguments.sequence` 必须为字符串化 JSON，不是对象。连接超时为 8 秒，可取消，旧连接事件不会覆盖新连接状态。“已发送”不等于已确认，“设备已确认请求”也不等于动作已完成。

本项目维护和自动测试**不连接真机、不下发、不烧录、不修改固件或服务端**。测试 WebSocket 仅使用 mock，不访问设备；设备执行、急停、角度 trim、碰撞安全和完整同步需另行验收。

## 目录与维护边界

```text
D:\jarvis\otto-choreographer\    # git 仓库根 = 项目根（2026-10-31 整仓迁入；固件/后端等在仓库外 D:\jarvis\）
├─ otto-choreographer.html       # 唯一生产源码/运行入口
├─ README.md                     # 当前使用与维护说明
├─ CHANGELOG-otto.md              # 编舞台变更记录
├─ assets\                       # 模型与素材（已入库）：原始3MF、网格JSON、三视图、Three.js原件、验收文档、历史补丁
├─ patches\                      # 固件/后端本地改动存档（已入库）：firmware-local\、server-local\，各含README
├─ otto-tests\                   # 独立离线测试；不属于运行依赖
│  ├─ run.py                     # 统一测试入口，检查失败返回非零
│  ├─ static-check.cjs            # 两段内嵌脚本语法/规则fixture
│  ├─ core.js                    # JSON、编辑、播放、mock协议回归
│  ├─ camera.js                  # 固定相机/基座
│  ├─ sides.js                   # 自身左右与单轴映射
│  ├─ fullscreen.js              # 全屏/退出/布局恢复
│  ├─ ui.js                      # 最近UI与腿脚对齐检查
│  └─ results\                   # 按次生成报告/截图/提取脚本（.gitignore，不入库）
├─ otto-编舞台-交接文档.md         # 历史2D交接，只作背景（路径按迁移注记解读）
└─ Otto编舞台-AI续接交接.md        # 3D 交接（快照口径）
```

仓库外（`D:\jarvis\`，不属本仓库，勿顺手改动）：`xiaozhi-esp32\`（固件生产目录）、`xiaozhi-esp32-server\`（后端生产目录）、两个 `*-mirror\` 上游镜像、`_backup\`、`audio-work\`、历史日志。固件/后端本地改动的权威存档在本仓库 `patches\`。Git 2.38.1 可用；未配置远程、未推送。

### 源码定位

不要依赖旧行号，用函数名定位；Three.js 压缩库和网格 base64 是大单行，不整行输出。

- 样式及响应式：顶部 `<style>`，最终舞台选择器 `#robotStage / .robot-viewport`。
- 六轴定义及 Home：`SERVOS / SERVO_KEYS / STAND_POSE`。
- 原始模型：`OTTO_MESH / nativeGeometry`；mm，CAD `(x,y,z)` 转 WebGL `(x,z,-y)`，网格不缩放。
- 装配：`buildRobot3D`；只在此调整具体零件定位，避免误改复用腿网格的手臂。
- 相机/固定基座：`resize3D / render3D / setRobotView / drawRobot`。
- 时间轴：`renderTimeline / selectFrame / syncPoseToActiveFrame / moveFrame / deleteFrame`。
- JSON 与校验：`validateSequence / validateOsc / parseSequence / buildSequence`。
- 播放：`playAll / runAnimation / stopAll / state.playToken`。
- 连接：`connectWs / disconnectWs / sendSequence`。
- 初始化与事件：`bindEvents / init`。

`otto-编舞台-交接文档.md` 的 2D 绘图公式、行号、库依赖及“已完成/实测”表述不能覆盖当前源码或真实验收状态。其他目录中的历史补丁/导出 JS 也不是生产权威，不直接重跑覆盖 HTML。

## 测试

运行页面只需浏览器。维护测试需要 Python 3.10+、Node.js；完整浏览器验证还需 Playwright 和 HTML 自检脚本 `shot.py`。本机已验证环境为 Python 3.13、Node.js 22。这些是开发依赖，不内嵌到页面，不改变单文件离线交付。

`core.js / camera.js / sides.js / fullscreen.js / ui.js` 是由 `shot.py --eval-file` 注入页面的 async 函数体，不是可直接用 Node 运行的应用模块。使用统一 `run.py` 入口；仅 `static-check.cjs` 可独立用 Node 执行。

下面的相对路径命令在 `D:\jarvis\otto-choreographer` 目录下执行。在其他目录可运行 `python "D:\jarvis\otto-choreographer\otto-tests\run.py"`；入口会自行定位项目，不依赖调用者的当前目录。

静态与逻辑 fixture（没有浏览器结论）：

```powershell
python .\otto-tests\run.py --static-only
```

完整回归：

```powershell
python .\otto-tests\run.py
```

只重查某一功能：

```powershell
python .\otto-tests\run.py --suite camera
python .\otto-tests\run.py --suite core --suite ui
```

脚本自动发现当前用户下的 HTML skill `scripts/shot.py` 和常见 Edge / Chrome 路径；外部维护环境可以显式传入路径：

```powershell
python .\otto-tests\run.py --shot "实际路径\html\scripts\shot.py" --browser "实际路径\msedge.exe"
```

没有 `shot.py` 时完整测试明确失败，不将缺失浏览器或依赖当成通过。`--static-only` 可独立执行，但输出会标记浏览器未运行。测试返回非零或 `summary.json` 中 `passed=false` 就不能交付为通过；即使截图工具退出码为 0，也必须检查 `eval.executed / eval.result.passed`。

结果默认保存到 `otto-tests/results/时间戳/summary.json`，按套件分别保存 desktop/mobile `report.json`、PNG 截图。输出会同时检查生产 HTML 的 SHA256 未改变；浏览器使用 `--no-auto-fix`，不会自动改生产源码。**实际打开截图检查黑屏、裁切、装配缝隙；报告不报错不能替代视觉验收。**

测试套件共同维护同一批断言，桌面/手机重复执行不算新的独立测试。完整回归验证实现和本地逻辑，不验证实物相似度、碰撞、设备网络或真实执行。

- 如果Git可用，`otto-tests/.gitignore`仅排除本测试目录的results/和Python缓存；不修改根目录或其他项目规则。

### 本轮验证基线

完整运行 `python .\otto-tests\run.py` 的报告按次生成于 `otto-tests/results/<时间戳>/summary.json`（results 不入库，历史报告已按 2026-10-31 清理决定移除）。迁移后基线为 `20261031-043341-924473`：27项静态检查，以及core 68、camera 22、sides 18、fullscreen 14、ui 14项断言，在1440×900与390×844视口通过，0运行错误/警告。套件之间有重叠，宽窄屏是重复执行，不计为新的独立测试。桌面与手机截图已实际读取；实物和真机验收仍不在覆盖范围。

HTML SHA256：`A528E7066253225A0063E24DAA25831BA409688F0056E5DC60622B99FE0163B6`。维护文件新增前后保持相同。以后修改HTML必须重跑相应测试，不将此基线作为动态最新结果。

## 修改、回退与发布

1. 回读当前源码，明确只改哪个对象；未知装配数据保持假设标记。
2. 改前复制当前 HTML 到 `_backup`，用语义化名称和时间戳，不覆盖已有存档。
3. 原地修改唯一 HTML，保留库、原始网格、JSON字段、预设和协议，除非需求明确要求改变。
4. 运行最小受影响测试，再按改动范围运行回归；检查真实截图，记录覆盖与缺口到 `CHANGELOG-otto.md`。
5. 通过以后交付最新 HTML；文档或测试修改也应同步维护，不凭历史“通过”覆盖本次结果。

回退前先复制个人 JSON，并确认所选备份版本；恢复到原 `otto-choreographer.html`，不要把 `_backup` 内多个版本当成当前入口。刷新无自动保存。

没有新增构建或发布流程；转发运行工具只需这一份 HTML。要交接源码维护则一并携带 README、变更记录和测试目录，不必携带测试输出及其他固件项目。不要未经授权公开发布作者模型或推送到额外仓库。

## 许可与来源

- 模型：小鹏 OttoRobot，来源 `https://makerworld.com.cn/zh/models/1117966-ottorobot-xiao-zhi-ai#profileId-1284462`，采用原始 3MF 网格。
- 模型许可：CC BY-NC-SA 4.0，`https://creativecommons.org/licenses/by-nc-sa/4.0/`。保留署名、来源、非商业及相同方式共享要求；公开分发修改模型前核对原许可。
- 内嵌 Three.js 采用 MIT，库内版权/许可文本保留。不删掉它们来减小文件。
- 本项目没有重新授予作者模型许可；自写页面代码未在本轮另行指定开源许可证，不能将整个 HTML 统一标成 MIT。

## 未完成与验收缺口

- 商家实物的侧面装配、双瓣圆爪、未知背面及深度仍未完整 1:1 验收。
- 未做真机连接/动作下发/固件烧录/舵机校准/动力学与碰撞验证。
- 未实现自动保存、撤销、拖拽时间轴或设备急停。
- 固定相机可能让大幅动作超出取景；这是保留固定视角的取舍，不自动改相机追随动作。
- 当前维护保留单文件结构，大库/网格单行会影响阅读；暂不拆源码，不引入运行时 CDN 或本地 fetch。
