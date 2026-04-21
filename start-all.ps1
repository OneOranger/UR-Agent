# UR Agent 完整启动脚本（后端 + 前端）

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  UR Agent 完整启动脚本" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 启动后端
Write-Host "[1/2] 正在启动后端服务..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; & '$PSScriptRoot\.venv\Scripts\Activate.ps1'; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
Start-Sleep -Seconds 3
Write-Host "✓ 后端服务已启动: http://localhost:8000" -ForegroundColor Green
Write-Host ""

# 启动前端
Write-Host "[2/2] 正在启动前端服务..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; & '$PSScriptRoot\.venv\Scripts\Activate.ps1'; npm run dev"
Start-Sleep -Seconds 2
Write-Host "✓ 前端服务已启动: http://localhost:3000" -ForegroundColor Green
Write-Host ""

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  所有服务已启动！" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "前端访问地址: http://localhost:3000" -ForegroundColor Green
Write-Host "后端API文档: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "按任意键退出此窗口..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
