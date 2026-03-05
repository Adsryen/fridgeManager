# -*- coding: utf-8 -*-
"""主页路由"""
from flask import Blueprint, render_template
from app.utils.auth import login_required, get_current_username

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    """主页"""
    return render_template('template.html', username=get_current_username())
