// 主入口模块 - 页面初始化和事件绑定

// 页面加载完成后初始化
$(document).ready(function() {
    console.log('页面初始化开始');
    
    // 初始化主题和深色模式
    initTheme();
    initDarkMode();
    
    // 加载系统设置
    loadSystemSettings();
    
    // 根据URL锚点恢复视图
    restoreViewFromHash();
    
    // 加载物品列表
    loadAllItems();
    
    // 初始化事件监听器
    initEventListeners();
    
    // 初始化表单
    initForms();
    
    // 监听浏览器前进后退按钮
    window.addEventListener('popstate', function() {
        restoreViewFromHash();
    });
    
    console.log('页面初始化完成');
});

// 加载系统设置
function loadSystemSettings() {
    $.ajax({
        url: '/item/get-system-settings',
        method: 'GET',
        success: function(response) {
            if (response.expiryWarningDays) {
                expiryWarningDays = response.expiryWarningDays;
            }
        },
        error: function() {
            console.warn('无法加载系统设置，使用默认值');
        }
    });
}

// 初始化事件监听器
function initEventListeners() {
    // 搜索框
    $('#mSearchInput').on('input', function() {
        const searchText = $(this).val();
        filterItems(searchText);
        
        if (searchText) {
            $('#clearSearchBtn').show();
        } else {
            $('#clearSearchBtn').hide();
        }
    });
    
    // 清除搜索
    $('#clearSearchBtn').click(function() {
        $('#mSearchInput').val('');
        $('#clearSearchBtn').hide();
        filterItems('');
    });
    
    // 抽屉背景点击关闭
    $('.drawer-overlay').click(function(e) {
        if ($(e.target).hasClass('drawer-overlay')) {
            $(this).removeClass('active');
        }
    });
}

// 初始化表单
function initForms() {
    // 初始化类别选择
    initCategorySelection();
    
    // 初始化日期选择器
    initDatePickers();
    
    // 绑定表单提交
    $('#mAddItemForm').submit(submitAddItemForm);
    $('#mEditItemForm').submit(submitEditItemForm);
}

// 视图切换
function switchView(viewName) {
    console.log('切换视图:', viewName);
    
    // 更新URL锚点
    if (history.pushState) {
        history.pushState(null, null, '#' + viewName);
    } else {
        window.location.hash = viewName;
    }
    
    // 更新底部导航激活状态
    $('.nav-item').removeClass('active');
    $(`.nav-item[data-view="${viewName}"]`).addClass('active');
    
    // 隐藏所有页面视图
    $('.page-view').hide();
    $('.mobile-content').hide();
    
    // 显示对应视图
    if (viewName === 'home') {
        $('.mobile-content').show();
        // 显示分类标签
        $('.category-tags-container').show();
    } else if (viewName === 'category') {
        $('#categoryPage').show();
        $('.category-tags-container').hide();
    } else if (viewName === 'stats') {
        $('#statsPage').show();
        $('.category-tags-container').hide();
    } else if (viewName === 'settings') {
        $('#settingsPage').show();
        $('.category-tags-container').hide();
    }
}

// 根据URL锚点恢复视图
function restoreViewFromHash() {
    const hash = window.location.hash.substring(1); // 移除 # 号
    if (hash && (hash === 'home' || hash === 'settings' || hash === 'category' || hash === 'stats')) {
        switchView(hash);
    } else {
        // 默认显示冰箱页面
        switchView('home');
    }
}

// 导出数据
function exportData() {
    showToast('导出功能开发中...', 'info');
}

// 清理过期物品
function clearExpiredItems() {
    const now = moment();
    const expiredItems = allItems.filter(item => {
        const expireDate = moment(item.ExpireDate);
        return expireDate.diff(now, 'days') < 0;
    });
    
    if (expiredItems.length === 0) {
        showToast('没有过期物品', 'info');
        return;
    }
    
    if (!confirm(`确定要删除 ${expiredItems.length} 个过期物品吗？`)) {
        return;
    }
    
    let deleted = 0;
    const total = expiredItems.length;
    
    expiredItems.forEach(item => {
        $.ajax({
            url: '/item/delete',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ itemId: item._id }),
            success: function(response) {
                if (response.success) {
                    deleted++;
                    if (deleted === total) {
                        showToast(`已删除 ${deleted} 个过期物品`, 'success');
                        loadAllItems();
                    }
                }
            }
        });
    });
}
