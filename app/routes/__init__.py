# -*- coding: utf-8 -*-
"""路由蓝图"""
from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.item import item_bp

__all__ = ['main_bp', 'auth_bp', 'item_bp']
