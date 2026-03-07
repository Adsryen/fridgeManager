// 管理后台移动端 - 仪表板页面逻辑

let pullStartY = 0;
let isPulling = false;
let pullDistance = 0;
const pullThreshold = 80;

document.addEventListener('DOMContentLoaded', function() {
    initDashboard();
    initPullRefresh();
});

function initDashboard() {
    // 绑定刷新按钮
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', handleRefresh);
    }
}

function initPullRefresh() {
    const content = document.getElementById('adminContent');
    const indicator = document.getElementById('pullRefreshIndicator');
    
    if (!content || !indicator) return;
    
    content.addEventListener('touchstart', (e) => {
        if (content.scrollTop === 0) {
            pullStartY = e.touches[0].pageY;
            isPulling = true;
        }
    }, { passive: true });
    
    content.addEventListener('touchmove', (e) => {
        if (!isPulling) return;
        
        const currentY = e.touches[0].pageY;
        pullDistance = currentY - pullStartY;
        
        if (pullDistance > 0 && content.scrollTop === 0) {
            // 显示刷新指示器
            if (pullDistance > 20) {
                indicator.classList.add('visible');
            }
            
            // 达到阈值时改变图标
            if (pullDistance > pullThreshold) {
                indicator.innerHTML = '<i class="fas fa-arrow-down"></i>';
            } else {
                indicator.innerHTML = '<i class="fas fa-sync"></i>';
            }
        }
    }, { passive: true });
    
    content.addEventListener('touchend', () => {
        if (!isPulling) return;
        
        if (pullDistance > pullThreshold) {
            // 触发刷新
            indicator.innerHTML = '<i class="fas fa-sync"></i>';
            handleRefresh();
        } else {
            // 隐藏指示器
            indicator.classList.remove('visible');
        }
        
        isPulling = false;
        pullDistance = 0;
    }, { passive: true });
}

async function handleRefresh() {
    const refreshBtn = document.getElementById('refreshBtn');
    const indicator = document.getElementById('pullRefreshIndicator');
    
    // 添加旋转动画
    if (refreshBtn) {
        refreshBtn.classList.add('rotating');
    }
    
    try {
        // 模拟刷新延迟,让用户看到动画
        await new Promise(resolve => setTimeout(resolve, 500));
        location.reload();
    } catch (error) {
        showAlert('刷新失败: ' + error.message, 'danger');
        if (refreshBtn) {
            refreshBtn.classList.remove('rotating');
        }
        if (indicator) {
            indicator.classList.remove('visible');
        }
    }
}

function navigateToUsers() {
    window.location.href = '/admin/users';
}

function navigateToSettings() {
    window.location.href = '/admin/settings';
}
