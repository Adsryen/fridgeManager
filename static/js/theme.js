// 主题和深色模式管理模块

// 根据时间自动判断是否应该使用深色模式
function shouldUseDarkMode() {
    const hour = new Date().getHours();
    return hour >= 18 || hour < 6;
}

// 获取用户选择的主题色（默认粉色）
function getUserTheme() {
    try {
        return localStorage.getItem('userTheme') || 'pink';
    } catch (e) {
        return 'pink';
    }
}

// 选择主题色
function selectTheme(theme) {
    console.log('选择主题:', theme);
    
    // 保存用户选择的主题
    try {
        localStorage.setItem('userTheme', theme);
    } catch (e) {
        console.warn('无法保存主题设置:', e);
    }
    
    // 应用主题
    applyTheme(theme);
    
    const themeNames = {
        'pink': '粉色',
        'blue': '蓝色',
        'purple': '紫色',
        'green': '绿色',
        'orange': '橙色',
        'gray': '灰色'
    };
    
    showToast('已切换到' + themeNames[theme] + '主题', 'success');
}

// 应用主题
function applyTheme(theme) {
    // 移除所有主题类
    $('body').removeClass('theme-pink theme-blue theme-purple theme-green theme-orange theme-gray');
    
    // 添加新主题类
    if (theme && theme !== 'pink') {
        $('body').addClass('theme-' + theme);
    }
    
    // 更新主题选择器的激活状态
    updateThemeSelector(theme);
}

// 更新主题选择器的激活状态
function updateThemeSelector(theme) {
    $('.theme-option').removeClass('active');
    $(`.theme-option[data-theme="${theme}"]`).addClass('active');
}

// 初始化主题
function initTheme() {
    console.log('初始化主题');
    const theme = getUserTheme();
    console.log('用户主题:', theme);
    applyTheme(theme);
}

// 切换自动日夜模式
function toggleAutoDarkMode() {
    const isChecked = $('#autoDarkModeToggle').is(':checked');
    console.log('切换自动日夜模式:', isChecked);
    
    try {
        if (isChecked) {
            // 开启自动模式
            localStorage.setItem('darkModeAuto', 'true');
            localStorage.removeItem('darkMode');
            initDarkMode();
            showToast('已开启自动日夜切换', 'success');
        } else {
            // 关闭自动模式，保持当前状态
            localStorage.setItem('darkModeAuto', 'false');
            const currentDark = $('body').hasClass('dark-mode');
            localStorage.setItem('darkMode', currentDark ? 'true' : 'false');
            showToast('已关闭自动日夜切换', 'info');
        }
    } catch (e) {
        console.warn('无法保存设置:', e);
    }
}

// 显示日夜切换规则说明
function showDarkModeHelp(event) {
    event.stopPropagation();
    
    const helpText = `
        <div style="text-align: left; line-height: 1.6;">
            <h4 style="margin-bottom: 12px; color: var(--primary-color);">
                <i class="fas fa-info-circle"></i> 自动日夜切换规则
            </h4>
            <p style="margin-bottom: 8px;">
                <strong>开启时：</strong>
            </p>
            <ul style="margin-left: 20px; margin-bottom: 12px;">
                <li>🌞 白天（6:00 - 18:00）：浅色模式</li>
                <li>🌙 夜晚（18:00 - 6:00）：深色模式</li>
            </ul>
            <p style="margin-bottom: 8px;">
                <strong>关闭时：</strong>
            </p>
            <ul style="margin-left: 20px;">
                <li>保持当前的浅色/深色模式</li>
                <li>可通过顶部按钮手动切换</li>
            </ul>
        </div>
    `;
    
    // 创建自定义提示框
    const alertHtml = `
        <div class="custom-alert-overlay" onclick="closeCustomAlert()">
            <div class="custom-alert-box" onclick="event.stopPropagation()">
                <div class="custom-alert-content">
                    ${helpText}
                </div>
                <button class="custom-alert-btn" onclick="closeCustomAlert()">
                    知道了
                </button>
            </div>
        </div>
    `;
    
    $('body').append(alertHtml);
}

// 关闭自定义提示框
function closeCustomAlert() {
    $('.custom-alert-overlay').fadeOut(200, function() {
        $(this).remove();
    });
}

// 初始化深色模式
function initDarkMode() {
    console.log('初始化深色模式');
    let darkModeSetting = null;
    let isAutoMode = true;
    
    try {
        darkModeSetting = localStorage.getItem('darkMode');
        isAutoMode = localStorage.getItem('darkModeAuto') !== 'false';
    } catch (e) {
        console.warn('无法读取深色模式设置，使用自动模式', e);
    }
    
    let shouldBeDark = false;
    
    if (isAutoMode) {
        shouldBeDark = shouldUseDarkMode();
        console.log('深色模式（自动）:', shouldBeDark, '- 当前时间:', new Date().getHours() + '点');
    } else {
        shouldBeDark = darkModeSetting === 'true';
        console.log('深色模式（手动）:', shouldBeDark);
    }
    
    if (shouldBeDark) {
        $('body').addClass('dark-mode');
    } else {
        $('body').removeClass('dark-mode');
    }
    
    updateDarkModeButton(shouldBeDark);
    
    // 更新滑块状态
    $('#autoDarkModeToggle').prop('checked', isAutoMode);
}

// 更新深色模式按钮
function updateDarkModeButton(isDark) {
    const btn = $('#darkModeBtn');
    const icon = btn.find('i');
    
    if (isDark) {
        icon.removeClass('fa-moon').addClass('fa-sun');
        btn.attr('title', '切换到浅色模式');
    } else {
        icon.removeClass('fa-sun').addClass('fa-moon');
        btn.attr('title', '切换到深色模式');
    }
}

// 手动切换深色模式（用于顶部按钮）
function toggleDarkMode() {
    console.log('手动切换深色模式');
    
    // 添加旋转动画
    const btn = $('#darkModeBtn');
    btn.addClass('rotating');
    
    // 延迟切换，让动画更流畅
    setTimeout(() => {
        $('body').toggleClass('dark-mode');
        const isDark = $('body').hasClass('dark-mode');
        
        try {
            localStorage.setItem('darkMode', isDark ? 'true' : 'false');
            localStorage.setItem('darkModeAuto', 'false');
            $('#autoDarkModeToggle').prop('checked', false);
        } catch (e) {
            console.warn('无法保存深色模式设置:', e);
        }
        
        updateDarkModeButton(isDark);
        showToast(isDark ? '已切换到夜间模式 🌙' : '已切换到日间模式 ☀️', 'info');
        
        // 移除旋转动画类
        setTimeout(() => {
            btn.removeClass('rotating');
        }, 600);
    }, 100);
}

// 重置深色模式为自动模式
function resetDarkModeToAuto() {
    console.log('重置深色模式为自动模式');
    
    try {
        localStorage.setItem('darkModeAuto', 'true');
        localStorage.removeItem('darkMode');
    } catch (e) {
        console.warn('无法保存设置:', e);
    }
    
    initDarkMode();
    showToast('已重置为自动日夜切换', 'success');
}

// 统一的初始化函数（供其他页面调用）
function initializeTheme() {
    console.log('初始化主题系统');
    initTheme();
    initDarkMode();
}

// 页面加载时自动初始化
$(document).ready(function() {
    initializeTheme();
});
