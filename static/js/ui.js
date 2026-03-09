// UI交互模块 - Toast、抽屉、加载状态等

// 显示Toast提示
function showToast(message, type = 'info', duration = 2500) {
    // 确保全局只有一个toast容器
    let toastContainer = $('.toast-container');
    if (toastContainer.length === 0) {
        toastContainer = $('<div class="toast-container"></div>');
        $('body').append(toastContainer);
    } else if (toastContainer.length > 1) {
        // 如果有多个容器，删除多余的，只保留第一个
        toastContainer.slice(1).remove();
        toastContainer = toastContainer.first();
    }
    
    const iconMap = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };
    
    const icon = iconMap[type] || iconMap['info'];
    
    const toast = $(`
        <div class="toast ${type}">
            <i class="fas ${icon}"></i>
            <span class="toast-message">${message}</span>
        </div>
    `);
    
    toastContainer.append(toast);
    
    // 根据消息长度和类型调整显示时间
    let displayDuration = duration;
    
    // 警告和错误消息显示更久
    if (type === 'warning' || type === 'error') {
        displayDuration = Math.max(duration, 3000);
    }
    
    // 长消息显示更久
    if (message.length > 20) {
        displayDuration = Math.max(displayDuration, 3500);
    }
    
    setTimeout(() => {
        toast.fadeOut(300, function() {
            $(this).remove();
        });
    }, displayDuration);
}

// 打开抽屉
function openDrawer(drawerId) {
    $(`#${drawerId}`).addClass('active');
}

// 关闭抽屉
function closeDrawer(drawerId) {
    const drawer = document.getElementById(drawerId);
    if (drawer) {
        drawer.classList.remove('active');
        
        // 只删除动态创建的抽屉（有特定标记的）
        // 静态HTML中的抽屉（如addMethodDrawer、addItemDrawer等）不删除
        const staticDrawers = ['addMethodDrawer', 'addItemDrawer', 'editItemDrawer', 'userMenuDrawer'];
        
        if (!staticDrawers.includes(drawerId)) {
            // 等待动画结束后删除动态创建的元素
            setTimeout(() => {
                drawer.remove();
            }, 300);
        }
    }
}

// 显示加载状态
function showLoading(container) {
    const loadingHtml = `
        <div class="loading-state">
            <div class="spinner"></div>
            <p>加载中...</p>
        </div>
    `;
    $(container).html(loadingHtml);
}

// 显示空状态
function showEmptyState(container, message = '暂无数据') {
    const emptyHtml = `
        <div class="empty-state">
            <i class="fas fa-inbox"></i>
            <h4>${message}</h4>
            <p>点击下方 + 按钮添加物品</p>
        </div>
    `;
    $(container).html(emptyHtml);
}
