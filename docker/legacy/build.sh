#!/bin/bash

# 冰箱管理系统 Docker 构建脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 镜像信息
IMAGE_NAME="fridgemanager/app"
VERSION=${1:-latest}
FULL_IMAGE_NAME="${IMAGE_NAME}:${VERSION}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}冰箱管理系统 Docker 镜像构建${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${YELLOW}镜像名称: ${FULL_IMAGE_NAME}${NC}"
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker 未安装或未在 PATH 中${NC}"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "Dockerfile" ]; then
    echo -e "${RED}错误: 请在 docker 目录中运行此脚本${NC}"
    exit 1
fi

# 构建镜像
echo -e "${YELLOW}开始构建镜像...${NC}"
docker build -t "${FULL_IMAGE_NAME}" -f Dockerfile ..

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 镜像构建成功！${NC}"
    echo -e "${GREEN}镜像名称: ${FULL_IMAGE_NAME}${NC}"
    
    # 显示镜像信息
    echo ""
    echo -e "${BLUE}镜像信息:${NC}"
    docker images "${IMAGE_NAME}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    
    echo ""
    echo -e "${BLUE}使用方法:${NC}"
    echo -e "${YELLOW}# 直接运行镜像${NC}"
    echo "docker run -d -p 3000:3000 --name fridge-manager ${FULL_IMAGE_NAME}"
    echo ""
    echo -e "${YELLOW}# 使用 docker-compose${NC}"
    echo "docker-compose up -d"
    echo ""
    echo -e "${YELLOW}# 推送到 Docker Hub（需要登录）${NC}"
    echo "docker push ${FULL_IMAGE_NAME}"
    
else
    echo -e "${RED}❌ 镜像构建失败！${NC}"
    exit 1
fi