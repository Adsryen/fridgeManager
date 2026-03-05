# -*- coding: utf-8 -*-
"""应用启动入口"""
import os
from app import create_app

# 获取配置环境
config_name = os.environ.get('FLASK_ENV', 'default')

# 创建应用
app = create_app(config_name)

if __name__ == "__main__":
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '8080'))
    debug = os.environ.get('DEBUG', '').lower() in ('1', 'true', 'yes', 'y')
    
    app.run(host=host, port=port, debug=debug)
