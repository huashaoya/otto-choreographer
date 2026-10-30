# xiaozhi-esp32 固件本地改动存档

> 生成时间：2026-10-31。生成方式：快照（`D:\jarvis\xiaozhi-esp32`，v2.5.3，文件时间 10/24-10/28）与上游 `78/xiaozhi-esp32` main 历史逐文件 git-blob 哈希比对，排除行尾符（CRLF/LF）与编译产物后得出。
> **生产目录是快照原样，未做任何修改。** 本目录只是改动的备份与说明。

## 目录结构

- `D:\jarvis\xiaozhi-esp32\` — **生产固件目录（快照原样，含本地改动，可直接 build/flash）**
- `D:\jarvis\xiaozhi-esp32-upstream-mirror\` — 上游 main 镜像（addb1ed @ 2026-10-30，干净浅克隆，仅供 diff/参考，**不要在里面 build**）
- `patches\firmware-local\` — 本目录：本地改动文件的完整副本（文件级存档，比 git patch 抗基线漂移）

## 本地改动清单（12 个源文件 + 4 个构建相关产物）

| 文件 | 已知背景 |
|---|---|
| `main/mcp_server.cc` | 10/28 加 4 个屏幕 MCP 工具（show_text/set_emotion/clear/show_qrcode，先渲染后 SetManualMode） |
| `main/display/display.h` / `display.cc` | manual_mode_ 原子标志 + SetManualMode/IsManualMode + SetStatus 守卫 |
| `main/display/lcd_display.cc` / `lcd_display.h` | SetChatMessage 双分支守卫；ShowQrCode 用 qrcodegen 手绘到 lv_canvas |
| `main/CMakeLists.txt` | qrcodegen INCLUDE_DIRS（复用 esp_emote_gfx 内的 qrcodegen，避免重复符号） |
| `main/boards/bread-compact-wifi-lcd/config.json` | `CONFIG_LCD_ST7789_240X240=y` |
| `main/boards/bread-compact-wifi-lcd/compact_wifi_board_lcd.cc` | 配套屏幕改动（具体 diff 详见快照） |
| `main/assets/locales/zh-CN/language.json` | 10/26 三处提示文字（HELLO_MY_FRIEND→"你好，先生。系统已就绪。"、STANDBY→"待命 · 贾维斯"、LISTENING→"聆听中 · 请讲"） |
| `main/assets/lang_config.h` | 语言资源配置（ONLY_SNAPSHOT，上游无此文件） |
| `main/assets/locales/zh-CN/welcome.ogg` | 欢迎语音频被替换（`.bak` 为原版备份，同在快照） |
| `main/boards/lckfb/szpi-esp32s3/lichuang_dev_board.cc` | 立创板型相关改动（10/26 立创实战派轮次） |
| `main/Kconfig.projbuild` | 菜单项改动（与板型/屏幕配置相关，未在会话记录中，以快照为准） |
| `main/led/single_led.cc` / `single_led.h` | LED 行为改动（未在会话记录中，以快照为准） |
| `sdkconfig` / `sdkconfig.old` | 编译配置（bread-compact-wifi-lcd + zh-CN，构建产物） |

未在会话记录中的改动（Kconfig.projbuild、single_led、compact_wifi_board_lcd.cc）以快照文件内容为准——它们不在任何上游 commit 中，判定为本地改动。

## 快照基线

快照主体最接近上游 `03a7c65`（2026-10-25 11:27，指纹匹配 10/24 文件），上游 10/26-10/30 的演进（13 commits）**不在**生产目录中。精确基线 commit 因 shallow 历史损坏未能最终锚定；不影响上述判定（本地改动判定基于"不匹配任何已知上游 commit"）。

## 恢复 / 迁移方法

换机器或重建目录时：
1. `git clone --depth 1 https://github.com/78/xiaozhi-esp32.git`（或直接复制 upstream-mirror）
2. 用本目录的 16 个文件**覆盖**同名文件（`lang_config.h`、`sdkconfig` 是上游没有的，直接放入）
3. `sdkconfig` 已含板型/语言配置；如需重建：`build.py bread-compact-wifi-lcd --language zh-CN`
4. 欢迎语如需还原原版：`welcome.ogg.bak` 在快照 `main/assets/locales/zh-CN/` 内

## 注意

- 不要把 `xiaozhi-esp32-upstream-mirror` 当生产目录（无 sdkconfig、无本地改动）。
- 固件目录与镜像位于仓库外（`D:\jarvis\`），本 patches 目录**已入库**。
- 真机操作（烧录/串口/下发）不在自动流程内，需用户明确指示。
