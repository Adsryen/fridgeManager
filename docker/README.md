# 简化版 Docker 部署指南

前后端分离的简化部署方案，不包含 HTTPS 配置，用户自行配置反向代理。

## 镜像说明

- `fridge-manager-backend:latest` - 后端 API 服务（Python Flask + Gunicorn）
- `fridge-manager-frontend:latest` - 前端静态文件服务（Nginx）

## 快速开始

### 1. 构建镜像

**Linux/Mac:**
```bash
cd docker
./build-simple.sh
```

**Windows:**
```powershell
cd docker
.\build-simple.ps1
```

### 2. 启动服务

```bash
docker-compose -f docker/docker-compose.yml up -d
```

### 3. 访问服务

- 前端: http://localhost:3000
- 后端: http://localhost:8080

### 4. 查看日志

```bash
# 查看所有日志
docker-compose -f docker/docker-compose.yml logs -f

# 只看后端日志
docker-compose -f docker/docker-compose.yml logs -f backend

# 只看前端日志
docker-compose -f docker/docker-compose.yml logs -f frontend
```

### 5. 停止服务

```bash
docker-compose -f docker/docker-compose.yml down
```

## 生产环境部署

### 配置反向代理

推荐使用 Nginx、Caddy 或 Traefik 作为反向代理，配置 HTTPS。

**Nginx 配置示例:**

```nginx
# 前端
server {
    listen 443 ssl http2;
    server_name bx.prlrr.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# 后端
server {
    listen 443 ssl http2;
    server_name bx.gr.prlrr.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS 配置
        add_header 'Access-Control-Allow-Origin' 'https://bx.prlrr.com' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;
    }
}
```

### 环境变量配置

修改 `docker-compose.yml` 中的环境变量：

```yaml
backend:
  environment:
    # 修改为实际的前端域名
    CORS_ORIGINS: "https://bx.prlrr.com,https://your-domain.com"
    
    # 可选：配置 AI 功能
    OPENAI_API_KEY: "your-openai-key"
    OPENAI_API_BASE: "https://api.openai.com/v1"

frontend:
  build:
    args:
      # 修改为实际的后端域名
      VITE_API_BASE_URL: "https://bx.gr.prlrr.com"
```

## 数据持久化

后端数据存储在 Docker volume `backend_data` 中，包括：
- SQLite 数据库
- 用户上传的文件
- 会话数据

备份数据：
```bash
docker run --rm -v backend_data:/data -v $(pwd):/backup alpine tar czf /backup/backend-data-backup.tar.gz -C /data .
```

恢复数据：
```bash
docker run --rm -v backend_data:/data -v $(pwd):/backup alpine tar xzf /backup/backend-data-backup.tar.gz -C /data
```

## 代理配置

如果构建时需要使用代理，修改 `docker-compose.yml` 中的代理配置：

```yaml
build:
  args:
    - HTTP_PROXY=http://your-proxy:port
    - HTTPS_PROXY=http://your-proxy:port
```

## 故障排查

### 后端无法启动

```bash
# 查看后端日志
docker logs fridge-backend

# 进入容器检查
docker exec -it fridge-backend bash
```

### 前端无法访问后端

1. 检查 CORS 配置是否正确
2. 检查前端的 API 地址配置
3. 检查网络连接

### 数据库初始化失败

```bash
# 删除旧数据重新初始化
docker-compose -f docker/docker-compose.yml down -v
docker-compose -f docker/docker-compose.yml up -d
```

## 性能优化

### 后端

修改 Gunicorn workers 数量（在 Dockerfile.backend 中）：
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "8", ...]
```

推荐 workers 数量 = (CPU 核心数 × 2) + 1

### 前端

Nginx 已配置 Gzip 压缩和静态资源缓存，无需额外配置。

## 监控

### 健康检查

```bash
# 后端健康检查
curl http://localhost:8080/health

# 前端健康检查
curl http://localhost:3000/health
```

### 容器状态

```bash
docker-compose -f docker/docker-compose.yml ps
```
