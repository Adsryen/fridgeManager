#!/bin/bash
set -e

echo "=========================================="
echo "冰箱管理系统 - 启动中..."
echo "=========================================="

# 设置默认值
SERVER_NAME=${SERVER_NAME:-localhost}
ENABLE_HTTPS=${ENABLE_HTTPS:-false}
ENABLE_FRONTEND=${ENABLE_FRONTEND:-true}
ENABLE_BACKEND_PORT=${ENABLE_BACKEND_PORT:-false}
SSL_CERT_PATH=${SSL_CERT_PATH:-/etc/nginx/ssl/cert.pem}
SSL_KEY_PATH=${SSL_KEY_PATH:-/etc/nginx/ssl/key.pem}
CORS_ORIGIN=${CORS_ORIGIN:-*}

# 根据模式设置端口
if [ "$ENABLE_FRONTEND" = "true" ]; then
    HTTP_PORT=3000
    HTTPS_PORT=3001
else
    HTTP_PORT=8080
    HTTPS_PORT=8081
fi

echo "服务器配置："
echo "  域名: $SERVER_NAME"
echo "  HTTPS: $ENABLE_HTTPS"
echo "  前端: $ENABLE_FRONTEND"
echo "  独立后端端口: $ENABLE_BACKEND_PORT"
echo "  CORS 源: $CORS_ORIGIN"
echo "  HTTP 端口: $HTTP_PORT"
if [ "$ENABLE_HTTPS" = "true" ]; then
    echo "  HTTPS 端口: $HTTPS_PORT"
fi

# 配置 HTTPS
if [ "$ENABLE_HTTPS" = "true" ]; then
    echo "  SSL 证书: $SSL_CERT_PATH"
    echo "  SSL 密钥: $SSL_KEY_PATH"
    
    # 检查证书文件是否存在
    if [ ! -f "$SSL_CERT_PATH" ] || [ ! -f "$SSL_KEY_PATH" ]; then
        echo "错误: SSL 证书或密钥文件不存在！"
        echo "请确保已挂载证书文件到容器中。"
        exit 1
    fi
    
    # 配置 HTTPS 重定向
    HTTPS_REDIRECT="return 301 https://\$server_name:$HTTPS_PORT\$request_uri;"
    
    # 生成 HTTPS 服务器块
    HTTPS_SERVER_BLOCK="server {
        listen $HTTPS_PORT ssl http2 default_server;
        listen [::]:$HTTPS_PORT ssl http2 default_server;
        server_name ${SERVER_NAME};

        # SSL 证书配置
        ssl_certificate ${SSL_CERT_PATH};
        ssl_certificate_key ${SSL_KEY_PATH};
        
        # SSL 优化配置
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;
        
        # 安全头
        add_header Strict-Transport-Security \"max-age=31536000; includeSubDomains\" always;
        add_header X-Frame-Options \"SAMEORIGIN\" always;
        add_header X-Content-Type-Options \"nosniff\" always;
        add_header X-XSS-Protection \"1; mode=block\" always;

        ${FRONTEND_CONFIG}

        # 后端 API 代理
        location /api/ {
            # CORS 预检请求
            if (\$request_method = 'OPTIONS') {
                add_header 'Access-Control-Allow-Origin' '${CORS_ORIGIN}' always;
                add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
                add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization, X-Requested-With' always;
                add_header 'Access-Control-Allow-Credentials' 'true' always;
                add_header 'Access-Control-Max-Age' 3600 always;
                add_header 'Content-Type' 'text/plain charset=UTF-8' always;
                add_header 'Content-Length' 0 always;
                return 204;
            }

            proxy_pass http://127.0.0.1:8080/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
            proxy_cache_bypass \$http_upgrade;
            proxy_read_timeout 300s;
            proxy_connect_timeout 75s;

            # CORS 响应头
            add_header 'Access-Control-Allow-Origin' '${CORS_ORIGIN}' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
            add_header 'Access-Control-Expose-Headers' 'Content-Length, Content-Range' always;
        }

        # 健康检查端点
        location /health {
            proxy_pass http://127.0.0.1:8080/health;
            access_log off;
        }
    }"
else
    echo "  HTTP 模式（未启用 HTTPS）"
    HTTPS_REDIRECT="# HTTPS 未启用"
    HTTPS_SERVER_BLOCK="# HTTPS 未启用"
fi

# 配置前端
if [ "$ENABLE_FRONTEND" = "true" ]; then
    echo "  前端模式: 启用（提供静态文件）"
    FRONTEND_CONFIG="# 前端静态文件
        location / {
            root /usr/share/nginx/html;
            try_files \$uri \$uri/ /index.html;
            
            # 缓存策略
            location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)\$ {
                expires 1y;
                add_header Cache-Control \"public, immutable\";
            }
        }"
else
    echo "  前端模式: 禁用（仅 API）"
    FRONTEND_CONFIG="# 前端已禁用，所有请求转发到后端
        location / {
            # CORS 预检请求
            if (\$request_method = 'OPTIONS') {
                add_header 'Access-Control-Allow-Origin' '${CORS_ORIGIN}' always;
                add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
                add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization, X-Requested-With' always;
                add_header 'Access-Control-Allow-Credentials' 'true' always;
                add_header 'Access-Control-Max-Age' 3600 always;
                add_header 'Content-Type' 'text/plain charset=UTF-8' always;
                add_header 'Content-Length' 0 always;
                return 204;
            }

            proxy_pass http://127.0.0.1:8080;
            proxy_http_version 1.1;
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
            proxy_cache_bypass \$http_upgrade;

            # CORS 响应头
            add_header 'Access-Control-Allow-Origin' '${CORS_ORIGIN}' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
        }"
fi

# 配置独立的后端端口
if [ "$ENABLE_BACKEND_PORT" = "true" ]; then
    echo "  独立后端端口: 8080（启用）"
    BACKEND_PORT_CONFIG="# 独立的后端 API 端口
    server {
        listen 8080;
        listen [::]:8080;
        server_name ${SERVER_NAME};

        location / {
            # CORS 预检请求
            if (\$request_method = 'OPTIONS') {
                add_header 'Access-Control-Allow-Origin' '${CORS_ORIGIN}' always;
                add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
                add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization, X-Requested-With' always;
                add_header 'Access-Control-Allow-Credentials' 'true' always;
                add_header 'Access-Control-Max-Age' 3600 always;
                add_header 'Content-Type' 'text/plain charset=UTF-8' always;
                add_header 'Content-Length' 0 always;
                return 204;
            }

            proxy_pass http://127.0.0.1:8080;
            proxy_http_version 1.1;
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
            proxy_cache_bypass \$http_upgrade;

            # CORS 响应头
            add_header 'Access-Control-Allow-Origin' '${CORS_ORIGIN}' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
        }
    }"
else
    BACKEND_PORT_CONFIG="# 独立后端端口未启用"
fi

# 替换 Nginx 配置模板中的变量
export SERVER_NAME HTTPS_REDIRECT HTTPS_SERVER_BLOCK FRONTEND_CONFIG BACKEND_PORT_CONFIG CORS_ORIGIN HTTP_PORT HTTPS_PORT
envsubst '${SERVER_NAME} ${HTTPS_REDIRECT} ${HTTPS_SERVER_BLOCK} ${FRONTEND_CONFIG} ${BACKEND_PORT_CONFIG} ${CORS_ORIGIN} ${HTTP_PORT} ${HTTPS_PORT}' \
    < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

echo "Nginx 配置已生成"

# 测试 Nginx 配置
nginx -t

# 创建数据目录
mkdir -p ${DATABASE_DIR}

# 初始化数据库（如果需要）
if [ ! -f "${DATABASE_DIR}/fridge.db" ]; then
    echo "初始化数据库..."
    python -c "from app import create_app; app = create_app(); app.app_context().push(); from app.utils.database import init_db; init_db()"
fi

echo "=========================================="
echo "启动完成！"
if [ "$ENABLE_FRONTEND" = "true" ]; then
    echo "前端 HTTP 端口: $HTTP_PORT"
    if [ "$ENABLE_HTTPS" = "true" ]; then
        echo "前端 HTTPS 端口: $HTTPS_PORT"
    fi
else
    echo "后端 HTTP 端口: $HTTP_PORT"
    if [ "$ENABLE_HTTPS" = "true" ]; then
        echo "后端 HTTPS 端口: $HTTPS_PORT"
    fi
fi
if [ "$ENABLE_BACKEND_PORT" = "true" ]; then
    echo "独立后端 API 端口: 8080"
fi
echo "=========================================="

# 执行传入的命令
exec "$@"
