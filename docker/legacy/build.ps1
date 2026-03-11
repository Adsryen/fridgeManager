# 冰箱管理系统 Docker 构建脚本 (Windows PowerShell)

param(
    [string]$Version = "latest"
)

# 镜像信息
$ImageName = "fridgemanager/app"
$FullImageName = "${ImageName}:${Version}"

Write-Host "========================================" -ForegroundColor Blue
Write-Host "冰箱管理系统 Docker 镜像构建" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host "镜像名称: $FullImageName" -ForegroundColor Yellow
Write-Host ""

# 检查 Docker 是否安装
try {
    docker --version | Out-Null
} catch {
    Write-Host "错误: Docker 未安装或未在 PATH 中" -ForegroundColor Red
    exit 1
}

# 检查是否在正确的目录
if (-not (Test-Path "Dockerfile")) {
    Write-Host "错误: 请在 docker 目录中运行此脚本" -ForegroundColor Red
    exit 1
}

# 构建镜像
Write-Host "开始构建镜像..." -ForegroundColor Yellow
Write-Host "使用代理: http://127.0.0.1:17890" -ForegroundColor Cyan

# 设置代理环境变量
$env:HTTP_PROXY = "http://127.0.0.1:17890"
$env:HTTPS_PROXY = "http://127.0.0.1:17890"
$env:NO_PROXY = "localhost,127.0.0.1"

docker build -t $FullImageName -f Dockerfile `
    --build-arg HTTP_PROXY=$env:HTTP_PROXY `
    --build-arg HTTPS_PROXY=$env:HTTPS_PROXY `
    --build-arg NO_PROXY=$env:NO_PROXY `
    --network=host `
    ..

if ($LASTEXITCODE -eq 0) {
    Write-Host "镜像构建成功！" -ForegroundColor Green
    Write-Host "镜像名称: $FullImageName" -ForegroundColor Green
    
    # 显示镜像信息
    Write-Host ""
    Write-Host "镜像信息:" -ForegroundColor Blue
    docker images $ImageName --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    
    Write-Host ""
    Write-Host "使用方法:" -ForegroundColor Blue
    Write-Host "# 直接运行镜像" -ForegroundColor Yellow
    Write-Host "docker run -d -p 3000:3000 --name fridge-manager $FullImageName"
    Write-Host ""
    Write-Host "# 使用 docker-compose" -ForegroundColor Yellow
    Write-Host "docker-compose up -d"
    Write-Host ""
    Write-Host "# 推送到 Docker Hub（需要登录）" -ForegroundColor Yellow
    Write-Host "docker push $FullImageName"
    
} else {
    Write-Host "镜像构建失败！" -ForegroundColor Red
    exit 1
}