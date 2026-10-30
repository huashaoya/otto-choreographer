# xiaozhi-esp32-server 后端本地改动存档

> 生成时间：2026-10-31。生成方式：快照（`D:\jarvis\xiaozhi-esp32-server`，2026-10-24 下载自 xinnan-tech 上游）与上游 main（1a095d5 + 深化历史 60 commits）逐文件 git-blob 哈希比对，排除行尾符与运行产物（`__pycache__`/`data`/`tmp`/`models`/`music`/`.pyc`，共 135 个）后得出。

## 目录结构

- `D:\jarvis\xiaozhi-esp32-server\` — **生产后端目录（快照原样，含本地改动，可直接运行）**
- `D:\jarvis\xiaozhi-esp32-server-mirror\` — 上游镜像（xinnan-tech main @ 1a095d5，仅供 diff/参考）
- `patches\server-local\` — 本目录：2 个本地改动文件的完整副本

## 本地改动清单（2 个文件）

| 文件 | 已知背景 |
|---|---|
| `main/xiaozhi-server/core/providers/asr/doubao_stream.py` | 方舟 ASR 流式接入改动（10/23-24 配置方舟 Key 轮次）；快照内有 `.bak` 原版备份 |
| `main/xiaozhi-server/core/providers/tts/huoshan_double_stream.py` | 方舟 TTS 双流式接入改动（同上）；快照内有 `.bak` 原版备份 |

其余 28 个差异文件全部匹配上游历史 commit（快照基线约在 2026-10-19 前后的 main），为上游演进，非本地改动。

## 运行产物（不入库存档，留在生产目录）

`data/.config.yaml`（运行时配置）、`tmp/server.log`、`__pycache__`、`models/SenseVoiceSmall`、`models/snakers4_silero-vad`、`music/*.mp3`。

## 注意

- 后端两把方舟 Key 仍未填（`config.yaml` 中为占位符），设备切换自建后端前需先填 Key（见 2026-10-23 会话记录）。
- 不要把 `xiaozhi-esp32-server-mirror` 当生产目录（无本地改动、无运行配置）。
- 主仓库 `.gitignore` 排除 `xiaozhi-esp32-server*/`，本 patches 目录已入库。
