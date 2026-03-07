// UI交互模块 - Toast、抽屉、加载状态等

// 显示Toast提示
function showToast(message, type = 'info') {
    const toastContainer = $('.toast-container');
    if (toastContainer.length === 0) {
        $('body').append('<div class="toast-container"></div>');
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
    
    $('.toast-container').append(toast);
    
    setTimeout(() => {
        toast.fadeOut(300, function() {
            $(this).remove();
        });
    }, 3000);
}

// 打开抽屉
function openDrawer(drawerId) {
    $(`#${drawerId}`).addClass('active');
}

// 关闭抽屉
function closeDrawer(drawerId) {
    $(`#${drawerId}`).removeClass('active');
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
