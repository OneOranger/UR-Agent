# UR Agent 前端平台启动脚本

Write-Host "正在启动 UR Agent 前端开发服务器..." -ForegroundColor Green
Write-Host ""

# 检查依赖
if (-Not (Test-Path "node_modules")) {
    Write-Host "首次运行，正在安装依赖..." -ForegroundColor Yellow
    npm install
    Write-Host ""
}

# 启动开发服务器
Write-Host "启动前端开发服务器..." -ForegroundColor Cyan
Write-Host "访问地址: http://localhost:3000" -ForegroundColor Green
Write-Host ""

npm run dev
