# -*- coding: utf-8 -*-
"""邮件发送工具"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app import db_client
from app.models.system_settings import SystemSettings


def get_email_config():
    """获取邮件配置"""
    try:
        settings = SystemSettings.get_settings(db_client)
        return {
            'smtp_server': settings.get('smtp_server', ''),
            'smtp_port': settings.get('smtp_port', 587),
            'smtp_username': settings.get('smtp_username', ''),
            'smtp_password': settings.get('smtp_password', ''),
            'from_email': settings.get('from_email', ''),
            'from_name': settings.get('from_name', '冰箱管理系统')
        }
    except Exception as e:
        print(f'获取邮件配置失败: {e}')
        return None


def send_email(to_email, subject, html_content):
    """
    发送邮件
    
    Args:
        to_email: 收件人邮箱
        subject: 邮件主题
        html_content: HTML格式的邮件内容
    
    Returns:
        bool: 发送是否成功
    """
    config = get_email_config()
    if not config or not config.get('smtp_server'):
        print('邮件配置不完整，无法发送邮件')
        return False
    
    try:
        # 创建邮件
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{config['from_name']} <{config['from_email']}>"
        msg['To'] = to_email
        
        # 添加HTML内容
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # 连接SMTP服务器并发送
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['smtp_username'], config['smtp_password'])
            server.send_message(msg)
        
        print(f'邮件发送成功: {to_email}')
        return True
    except Exception as e:
        print(f'邮件发送失败: {e}')
        return False


def send_password_reset_email(to_email, reset_token, username):
    """
    发送密码重置邮件
    
    Args:
        to_email: 收件人邮箱
        reset_token: 重置令牌
        username: 用户名
    
    Returns:
        bool: 发送是否成功
    """
    # 构建重置链接（需要根据实际域名调整）
    reset_link = f"http://localhost:5000/auth/reset-password?token={reset_token}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧊 密码重置</h1>
            </div>
            <div class="content">
                <p>你好，<strong>{username}</strong>！</p>
                <p>我们收到了你的密码重置请求。请点击下面的按钮重置你的密码：</p>
                <p style="text-align: center;">
                    <a href="{reset_link}" class="button">重置密码</a>
                </p>
                <p>或者复制以下链接到浏览器：</p>
                <p style="word-break: break-all; background: #fff; padding: 10px; border-radius: 5px;">{reset_link}</p>
                <p><strong>注意：</strong>此链接将在30分钟后失效。</p>
                <p>如果你没有请求重置密码，请忽略此邮件。</p>
            </div>
            <div class="footer">
                <p>此邮件由系统自动发送，请勿回复。</p>
                <p>© 2024 冰箱管理系统</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(to_email, '密码重置请求 - 冰箱管理系统', html_content)
