#!/bin/bash

# 简化版构建脚本 - 前后端分离

set -e

echo "=========================================="
echo "冰箱管理系统 - 构建镜像"
echo "=========================================="

# 进入项目根目录
cd "$(dirname "$0")/.."

# 构建后端镜像
echo ""
echo "构建后端镜像..."
docker build -f docker/Dockerfile.backend -t fridge-manager-backend:latest .

# 构建前端镜像
echo ""
echo "构建前端镜像..."
docker build -f docker/Dockerfile.frontend -t fridge-manager-frontend:latest .

echo ""
echo "=========================================="
echo "构建完成！"
echo "=========================================="
echo ""
echo "镜像列表："
docker images | grep fridge-manager
echo ""
echo "启动服务："
echo "  docker-compose -f docker/docker-compose.yml up -d"
echo ""
echo "查看日志："
echo "  docker-compose -f docker/docker-compose.yml logs -f"
echo ""
