# 简化版构建脚本 - 前后端分离 (PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "冰箱管理系统 - 构建镜像" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 进入项目根目录
Set-Location (Split-Path -Parent $PSScriptRoot)

# 构建后端镜像
Write-Host ""
Write-Host "构建后端镜像..." -ForegroundColor Yellow
docker build -f docker/Dockerfile.backend -t fridge-manager-backend:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "后端镜像构建失败！" -ForegroundColor Red
    exit 1
}

# 构建前端镜像
Write-Host ""
Write-Host "构建前端镜像..." -ForegroundColor Yellow
docker build -f docker/Dockerfile.frontend -t fridge-manager-frontend:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "前端镜像构建失败！" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "构建完成！" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "镜像列表：" -ForegroundColor Cyan
docker images | Select-String "fridge-manager"
Write-Host ""
Write-Host "启动服务：" -ForegroundColor Cyan
Write-Host "  docker-compose -f docker\docker-compose.yml up -d" -ForegroundColor White
Write-Host ""
Write-Host "查看日志：" -ForegroundColor Cyan
Write-Host "  docker-compose -f docker\docker-compose.yml logs -f" -ForegroundColor White
Write-Host ""
