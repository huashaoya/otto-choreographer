# Otto 编舞台变更记录

仅记录 `otto-choreographer.html` 及本项目维护文件。下述历史项目状态依据当前源码与本地验收资料，不能解释为实物 1:1、设备安全或真机执行已完成。

## 2026-10-31 · 固件/后端接管（仓库外变更，影响 patches 与 README）

- **应确认执行"基于上游镜像覆盖本地内容"**：快照基线经 ZIP 打包 mtime（1773 文件同刻 10-24 05:45）定位为上游 `a0fb73c`（2026-10-24 04:38 +0800）；本地改动 13 源文件 + lang_config.h（mtime 铁证，`Kconfig.projbuild` 被排除——此前 blob 分类误判）。GitHub 直连间歇性阻断，最终经本机代理 `127.0.0.1:7897` 完成镜像 clone。
- 固件目录现为 git 仓库：上游 `addb1ed` + 合并 commit `9fe5a97`（11 文件直接覆盖 + CMakeLists/mcp_server 经 `git merge-file` 三方合并零冲突：本地 qrcodegen INCLUDE/4 屏幕工具与上游新板型/snapshot 工具并存）。**编译验证通过**（`build.py bread-compact-wifi-lcd --language zh-CN`，`Project build complete`；期间修复组件缓存损坏并离线复制 `managed_components` 737MB）。**重放固件未上真机**，烧录验证由用户执行。
- 后端目录现为 git 仓库：上游 `1a095d5` + 合并 commit `fd3ab1f`（2 文件，方舟 Agent Plan Key 支持），`py_compile` 通过；运行数据（`data\.config.yaml`、music、models）已迁移，models 覆盖事故已 amend 修正（tracked 文件回退被还原）。
- 旧快照 ×2（1.3GB）与上游镜像目录已删除；`welcome.ogg.bak` 原版已补存至 `patches\firmware-local\`。`patches\` 两个 README 同步新结构。生产 HTML 与编舞台文件本轮零改动。

## 2026-10-31 · 过程文件清理（当日第三次结构变更）

- **应确认执行"只要最终项目文件"**：
  - `D:\jarvis\` 根：删除 7 份 build/flash 日志与 `otto-tests.zip`（未跟踪，直接删）。
  - 仓库内 `git rm`：历史 2D 截图 `otto-choreographer-current.png`、`-preview.png`；`assets\legacy-patches\` 27 个历史轮次补丁/回归脚本（豆包缓存原件仍在，git 历史 ebb1613 可找回）。
  - 删除 `otto-tests\results\`（24.8MB、6 份报告，本就不入库；需要时 `run.py` 重跑即再生成）。
- **保留并说明理由**：`_backup\`（2D 版本的唯一存档——git 基线即 3D 版，且生产 HTML 运行时提示仍引用其中 2D 实物版）；`audio-work\`（独立项目，范围外）；两个上游镜像（核查/升级参考）；固件/后端生产目录原样未动。
- 活文档引用同步：README「本轮验证基线」、3D 交接 §8.2/§9 改为"报告按次生成、results 不入库"，迁移后基线 `20261031-043341-924473`；`CHANGELOG` 历史条目不改写。
- 删除前后生产 HTML SHA256 均为 `A528E706…63B6`；本轮无外观/功能/真机结论。

## 2026-10-31 · 整仓迁移（当日第二次结构变更）

- **应确认执行整仓搬家**：git 仓库根由 `D:\jarvis\` 迁至 `D:\jarvis\otto-choreographer\`，仓库根 = 项目根。全部 76 个跟踪文件与 `.git` 一起移动，历史提交（`ce5bdd5`、`ebb1613`）完整保留，移动后 `git status` 干净。
- 迁移后仓库外保留（`D:\jarvis\`，均未改动）：固件生产目录、后端生产目录、两个上游镜像、`_backup\`、`audio-work\`、历史 build/flash 日志、`otto-tests.zip`。
- `.gitignore` 精简为测试产物三项（`/otto-tests/results/`、`__pycache__/`、`*.pyc`）；固件/server 等已在仓库外，无需忽略规则。
- 路径引用更新：README（入口、目录树、测试命令）、`Otto编舞台-AI续接交接.md`（18 处；`_backup` 与固件两处按仓库外原样保留）、`otto-编舞台-交接文档.md` 顶部加迁移注记（正文历史不改写）、`patches\` 两个 README 的仓库边界表述。`otto-choreographer.html` 内容零改动（其运行时提示指向的 `_backup` 路径迁移后依然正确）。
- **迁移暴露并修复两个测试环境问题**：① `assets\grid-views\` 五张三视图成为 HTML 兄弟目录后触发 shot.py 发布链路 lint（`assets/` 下未被 HTML 引用的图片 → error×5），已移至 `docs\grid-views\`（仓库内无代码引用，纯人工对照图，语义归 docs）；测试口径与外部 shot.py 均未改动。② 回归首次运行全套 `False(None)`：`playwright` 缺失（greenlet 残留）令 shot.py 降级 CDP 模式、`--eval` 断言不执行；已 `pip install playwright` 恢复。pip 提示的 sqlalchemy/typing-extensions 版本冲突为环境既有问题，未处理。
- 迁移后全量回归 **PASS**（`20261031-043341-924473`）：core 68、camera 22、sides 18、fullscreen 14、ui 14，desktop/mobile 双视图全过，`production_unchanged=true`。
- 生产 HTML SHA256 迁移前后均为 `A528E7066253225A0063E24DAA25831BA409688F0056E5DC60622B99FE0163B6`；本轮无外观/功能/真机结论。

## 2026-10-31 · 仓库化与素材归位

- **素材从聊天缓存迁出**：`Otto原始模型.3mf`、`Otto真实网格.json`、五类网格三视图、`three-0.158.0.min.js`、模型尺寸 JSON 及 3 份验收文档，从豆包聊天缓存目录复制到 `assets\`（原件未动，SHA256 校验一致）；历史轮次补丁/回归脚本 25 个归入 `assets\legacy-patches\`。此前素材存放在 `C:\Users\Administrator\Doubao\chats\...`，有清缓存即丢失风险。
- **建立本地 git 仓库**（原地 init 于 `D:\jarvis`）：`.gitignore` 排除固件/后端/镜像/`_backup`/日志/测试产物；基线提交 `ce5bdd5` 含生产 HTML（SHA256 `A528E7066253225A0063E24DAA25831BA409688F0056E5DC60622B99FE0163B6` 未变）、文档、测试套件与素材，共 56 文件。全局身份 `huashaoya` 复用，未配置远程、未推送。
- **固件快照核查**（`xiaozhi-esp32`，PROJECT_VER 2.5.3）：与上游 78/xiaozhi-esp32 main（@addb1ed）逐文件 git-blob 比对（MD5 方案因 CRLF/LF 行尾污染弃用），识别本地改动 12 源文件 + 4 构建产物（屏幕工具/manual_mode/qrcodegen/欢迎语/提示文字等），全部不匹配任何上游 commit；快照主体指纹最接近 03a7c65 (10-25)。生产目录**原样未动**，改动文件级存档至 `patches\firmware-local\`（16 文件 + README）。
- **固件上游镜像**：`xiaozhi-esp32-upstream-mirror\`（addb1ed，1819 文件）。浅仓库经多次 `--shallow-since` 叠加后 fetch 报 `error in object: unshallow`，log 可读但再次深化前需重建；镜像仅作 diff 参考。
- **后端快照核查**（`xiaozhi-esp32-server`，xinnan-tech 上游）：本地改动恰好 2 文件（`asr/doubao_stream.py`、`tts/huoshan_double_stream.py`，10/23-24 方舟 Key 轮次，有 `.bak` 备份），其余 28 差异均匹配上游历史；存档至 `patches\server-local\`。镜像 `xiaozhi-esp32-server-mirror\`（@1a095d5）。
- 生产 HTML、固件目录、后端目录内容均未被修改；本轮无外观/功能/真机结论。

## 未发布 · 单文件项目维护

- 保留 `otto-choreographer.html` 为唯一源码和运行入口，HTML 未拆分，生产内容不修改。
- 新增根目录 `README.md`，包含快速使用、JSON、实现默认值、左右口径、固定相机、连接边界、源码定位、测试、备份/回退、许可及未验收项。
- 新增 `otto-tests/`：统一 Python 测试入口、Node静态/逻辑fixture、core/camera/sides/fullscreen/ui浏览器套件。
- 浏览器验证统一由 HTML 自检 `shot.py` 执行；WebSocket 用 mock，无设备连接。
- 保留历史 `otto-编舞台-交接文档.md`，明确它描述旧2D；不重写历史事实和已存档版本。
- 不修改 `.git`、固件、服务端或其他日志。当前 Git 不在 PATH，未提交/推送。
- 本轮完整验证命令：`python .\otto-tests\run.py`；报告 `otto-tests/results/20261031-024706-317600/summary.json`，27项静态检查通过，core 68、camera 22、sides 18、fullscreen 14、ui 14项在desktop/mobile各自重复执行并通过，0运行错误/警告。不同套件有重叠，不汇总为独立测试总数。
- 生产HTML SHA256保持 `A528E7066253225A0063E24DAA25831BA409688F0056E5DC60622B99FE0163B6`；本轮只新增维护文件，没有修改模型或页面。
- `--static-only`已实际通过；将README作为错误HTML输入时返回1，失败路径已验证。静态-only报告不是浏览器验收。
- 新增 `otto-tests/.gitignore`，只忽略本目录results/和Python缓存，不改根目录或其他项目规则。
- 桌面和手机截图已读取；测试不代表实物相似度、真机网络或设备安全验证。以每次调用的报告为准，不把较晚的负例/静态-only报告误认为完整验收。

## 当前 HTML 已包含的改动

### 编舞数据与播放

- 稀疏姿态 JSON 原样保留，仅预览继承前帧未指定的关节。
- 导入时整体严格校验后原子提交；拒绝数字字符串、未知字段和非法范围。
- 顶层序列延迟保留可编辑；姿态帧 `v/d` 可编辑；振荡六轴的振幅/中心/相位保存无损。
- 播放令牌和可取消等待避免停止后立刻重播竞争；振荡后续基准为中心角。
- 连接8秒超时、可取消、旧事件隔离、嵌套设备错误、发送与确认区分；风险序列阻止下发。

### 预览与界面

- 内嵌真实原网格和 Three.js，离线单HTML；不通过CDN或本地fetch加载。
- 3D中栏占满可用区域，全屏与页面全屏回退，退出后恢复布局。
- 左右采用机器人自身口径，左右关节和侧视按钮对应修正。
- 相机与整机基座固定于Home参考，关节或播放不自动居中、拉远或贴地补偿。
- 初始/复位为正面俯视，pitch=0.24 rad；手动旋转缩放保留。
- 清空确认弹窗移除；舞台说明、顶部快捷“站立”、拖动缩放提示、“点击追加”提示移除。
- 两侧肩线向后移到深度中部；蓝色腿壳前后翻正；脚架深度改为与腿壳3.25对齐。
- 商家款爪型、完整侧面、背部及真机同步仍未完整验收。

## 维护记录规则

每次修改补记：目的、涉及文件/函数、用户确认的范围、验证命令与报告位置、未覆盖项、备份位置。禁止只写“全部通过”而没有范围；禁止把实现断言当成相似度或真机安全结论。
