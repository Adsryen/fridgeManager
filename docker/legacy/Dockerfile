# 多阶段构建 - 前端构建阶段
FROM node:22-alpine AS frontend-builder

# 设置代理参数
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

# 配置npm代理
RUN if [ -n "$HTTP_PROXY" ]; then npm config set proxy $HTTP_PROXY; fi && \
    if [ -n "$HTTPS_PROXY" ]; then npm config set https-proxy $HTTPS_PROXY; fi

WORKDIR /frontend

# 复制前端依赖文件
COPY frontend/package*.json ./

# 安装依赖
RUN npm install

# 复制前端源码
COPY frontend/ ./

# 构建前端
RUN npm run build

# 生产环境镜像
FROM python:3.12-slim

# 设置代理参数
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

# 配置pip代理和超时
RUN if [ -n "$HTTP_PROXY" ]; then \
        pip config set global.proxy $HTTP_PROXY && \
        pip config set global.timeout 300; \
    else \
        pip config set global.timeout 300; \
    fi

# 安装 Nginx 和其他必要工具
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    curl \
    gettext-base \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    HOST=127.0.0.1 \
    PORT=8080 \
    DATABASE_DIR=/data \
    ENABLE_FRONTEND=true

# 复制 Python 依赖文件
COPY requirements.txt ./

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 复制后端代码
COPY app/ ./app/
COPY config/ ./config/
COPY scripts/ ./scripts/
COPY run.py ./

# 从前端构建阶段复制构建产物
COPY --from=frontend-builder /frontend/dist /usr/share/nginx/html

# 创建必要的目录
RUN mkdir -p /data /var/log/supervisor /etc/nginx/ssl

# 复制配置文件
COPY docker/nginx.conf.template /etc/nginx/nginx.conf.template
COPY docker/entrypoint.sh /entrypoint.sh
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 设置执行权限
RUN chmod +x /entrypoint.sh

# 暴露端口
# 3000: HTTP 前端端口
# 3001: HTTPS 前端端口  
# 8080: HTTP 后端端口（仅后端模式或独立后端端口）
# 8081: HTTPS 后端端口（仅后端模式）
EXPOSE 3000 3001 8080 8081

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# 使用 entrypoint 脚本启动
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
