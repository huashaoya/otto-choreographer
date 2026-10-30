# 小智自建后端 · 一键启动
# 用法：右键「使用 PowerShell 运行」，或在终端执行 .\start-xiaozhi.ps1

$ErrorActionPreference = "Stop"

# opus.dll 在这个目录，必须加进 PATH 否则 opuslib_next 加载失败
$env:PATH = "C:\Users\Administrator\.conda\envs\xiaozhi\Library\bin;" + $env:PATH
$env:PYTHONIOENCODING = "utf-8"

$serverDir = "D:\jarvis\xiaozhi-esp32-server\main\xiaozhi-server"
$python = "C:\Users\Administrator\.conda\envs\xiaozhi\python.exe"

Write-Host ""
Write-Host "  小智后端启动中..." -ForegroundColor Cyan
Write-Host "  OTA:       http://192.168.0.116:8003/xiaozhi/ota/" -ForegroundColor Green
Write-Host "  WebSocket: ws://192.168.0.116:8000/xiaozhi/v1/" -ForegroundColor Green
Write-Host "  按 Ctrl+C 停止" -ForegroundColor DarkGray
Write-Host ""

Set-Location $serverDir
& $python app.py
