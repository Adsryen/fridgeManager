# Docker 部署指南

## 快速开始

### 使用 Docker Compose（推荐）

1. **构建并启动**
   ```bash
   cd docker
   docker-compose up -d
   ```

2. **查看日志**
   ```bash
   docker-compose logs -f
   ```

3. **停止服务**
   ```bash
   docker-compose down
   ```

4. **访问应用**
   
   打开浏览器访问 `http://localhost:8080`

### 使用 Docker

1. **构建镜像**
   ```bash
   docker build -f docker/Dockerfile -t fridge-manager .
   ```

2. **运行容器**
   ```bash
   docker run -d \
     -p 8080:8080 \
     -v fridge_data:/data \
     --name fridge-manager \
     fridge-manager
   ```

3. **查看日志**
   ```bash
   docker logs -f fridge-manager
   ```

4. **停止容器**
   ```bash
   docker stop fridge-manager
   docker rm fridge-manager
   ```

## 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| HOST | 0.0.0.0 | 监听地址 |
| PORT | 8080 | 监听端口 |
| DATABASE_DIR | /data | 数据库目录 |
| FLASK_ENV | production | 运行环境 |
| SECRET_KEY | 自动生成 | 会话密钥 |

## 数据持久化

数据存储在 Docker volume `fridge_data` 中，即使删除容器，数据也不会丢失。

### 备份数据

```bash
docker run --rm -v fridge_data:/data -v $(pwd):/backup alpine tar czf /backup/fridge_backup.tar.gz -C /data .
```

### 恢复数据

```bash
docker run --rm -v fridge_data:/data -v $(pwd):/backup alpine tar xzf /backup/fridge_backup.tar.gz -C /data
```

## 生产环境部署

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 使用 HTTPS

建议使用 Let's Encrypt 配置 HTTPS：

```bash
# 安装 certbot
apt-get install certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d your-domain.com
```

## 故障排查

### 查看容器状态
```bash
docker ps -a
```

### 查看容器日志
```bash
docker logs fridge-manager
```

### 进入容器
```bash
docker exec -it fridge-manager /bin/bash
```

### 检查数据库
```bash
docker exec -it fridge-manager ls -la /data
```
