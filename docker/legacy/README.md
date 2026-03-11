# Legacy Docker 配置

这个目录包含旧版本的复杂 Docker 配置文件，已被简化版本替代。

## 为什么移到这里？

旧版配置包含了以下复杂功能：
- 内置 HTTPS 支持
- Nginx + Supervisor 多进程管理
- 多种部署模式（前后端一体、独立端口等）
- 复杂的环境变量配置

这些功能增加了维护难度和使用复杂度。

## 新版本的改进

新版本采用前后端分离的简单架构：
- 前端：独立的 Nginx 容器
- 后端：独立的 Python/Gunicorn 容器
- HTTPS 由用户自行配置反向代理（Nginx/Caddy/Traefik）
- 配置更简单，更容易理解和维护

## 如果需要使用旧版本

旧版本的文件仍然保留在这里，可以参考使用：

- `Dockerfile` - 旧版一体化镜像
- `docker-compose.yml` - 默认配置
- `docker-compose.frontend-backend.yml` - 前后端一体模式
- `docker-compose.api-only.yml` - 仅后端 API 模式
- `docker-compose.dual-port.yml` - 双端口模式
- `docker-compose.backend-http.yml` - 后端 HTTP 模式
- `entrypoint.sh` - 复杂的启动脚本
- `nginx.conf.template` - Nginx 配置模板
- `supervisord.conf` - Supervisor 配置

## 推荐

建议使用新版本的简化配置（docker 目录下的文件），除非有特殊需求。
