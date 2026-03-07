// 管理后台移动端 - 工具函数

// API请求封装
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || '请求失败');
        }
        
        return result;
    } catch (error) {
        console.error('API请求错误:', error);
        throw error;
    }
}

// 显示提示框
function showAlert(message, type = 'success') {
    const alertBox = document.getElementById('alertBox');
    const alertMessage = document.getElementById('alertMessage');
    
    if (!alertBox || !alertMessage) {
        alert(message);
        return;
    }
    
    // 移除之前的类
    alertBox.className = 'alert';
    alertBox.classList.add(`alert-${type}`);
    
    // 设置图标
    const icon = type === 'success' ? 'check-circle' : 
                 type === 'danger' ? 'exclamation-circle' : 
                 type === 'warning' ? 'exclamation-triangle' : 'info-circle';
    
    alertBox.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <span id="alertMessage">${message}</span>
    `;
    
    alertBox.style.display = 'flex';
    
    // 添加进入动画
    alertBox.style.animation = 'slideInDown 0.3s ease-out';
    
    setTimeout(() => {
        alertBox.style.animation = 'slideOutUp 0.3s ease-out';
        setTimeout(() => {
            alertBox.style.display = 'none';
        }, 300);
    }, 3000);
}

// 显示确认对话框
function showConfirm(title, message, onConfirm) {
    // 创建遮罩层
    const overlay = document.createElement('div');
    overlay.className = 'confirm-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.2s ease-out;
    `;
    
    // 创建对话框
    const dialog = document.createElement('div');
    dialog.className = 'confirm-dialog';
    dialog.style.cssText = `
        background: white;
        border-radius: 12px;
        padding: 24px;
        margin: 0 20px;
        max-width: 400px;
        width: 100%;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        animation: scaleIn 0.2s ease-out;
    `;
    
    dialog.innerHTML = `
        <div style="font-size: 18px; font-weight: 600; margin-bottom: 12px; color: var(--text-primary);">
            ${title}
        </div>
        <div style="font-size: 14px; line-height: 1.6; color: var(--text-secondary); margin-bottom: 24px; white-space: pre-line;">
            ${message}
        </div>
        <div style="display: flex; gap: 12px;">
            <button class="btn btn-secondary" style="flex: 1;" onclick="this.closest('.confirm-overlay').remove()">
                取消
            </button>
            <button class="btn btn-primary" style="flex: 1;" id="confirmBtn">
                确定
            </button>
        </div>
    `;
    
    overlay.appendChild(dialog);
    document.body.appendChild(overlay);
    
    // 绑定确定按钮
    document.getElementById('confirmBtn').addEventListener('click', () => {
        overlay.remove();
        onConfirm();
    });
    
    // 点击遮罩层关闭
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            overlay.remove();
        }
    });
    
    // 添加动画样式
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes scaleIn {
            from { transform: scale(0.9); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        @keyframes slideInDown {
            from { transform: translateY(-100%); }
            to { transform: translateY(0); }
        }
        @keyframes slideOutUp {
            from { transform: translateY(0); }
            to { transform: translateY(-100%); }
        }
    `;
    if (!document.querySelector('style[data-confirm-style]')) {
        style.setAttribute('data-confirm-style', 'true');
        document.head.appendChild(style);
    }
}

// 显示加载状态
function showLoading(show = true) {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = show ? 'flex' : 'none';
    }
}

// 格式化日期
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN');
}

// 格式化日期时间
function formatDateTime(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// 导出函数
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        apiRequest,
        showAlert,
        showConfirm,
        showLoading,
        formatDate,
        formatDateTime,
        debounce,
        throttle
    };
}
