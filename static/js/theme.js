// 主题和深色模式管理模块

// 根据时间自动判断是否应该使用深色模式
function shouldUseDarkMode() {
    const hour = new Date().getHours();
    return hour >= 18 || hour < 6;
}

// 获取用户选择的主题色（优先从服务器，其次localStorage）
function getUserTheme() {
    try {
        // 从body的class中读取服务器设置的主题
        var bodyClasses = document.documentElement.className;
        var themeMatch = bodyClasses.match(/theme-(\w+)/);
        if (themeMatch) {
            return themeMatch[1];
        }
        
        // 如果没有主题class，尝试从localStorage读取（游客用户）
        var localTheme = localStorage.getItem('userTheme');
        if (localTheme) {
            return localTheme;
        }
        
        // 默认粉色
        return 'pink';
    } catch (e) {
        return 'pink';
    }
}

// 选择主题色
function selectTheme(theme) {
    console.log('选择主题:', theme);
    
    // 保存到服务器
    saveThemeToServer(theme);
    
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

// 保存主题到服务器
function saveThemeToServer(theme) {
    fetch('/settings/update-theme', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            theme_color: theme
        })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.success && !data.saved_to_server) {
            // 游客用户，保存到localStorage
            try {
                localStorage.setItem('userTheme', theme);
            } catch (e) {
                console.warn('无法保存到localStorage:', e);
            }
        }
    })
    .catch(function(error) {
        console.warn('保存主题设置失败，使用localStorage备用:', error);
        // 保存到localStorage作为备用
        try {
            localStorage.setItem('userTheme', theme);
        } catch (e) {
            console.warn('无法保存到localStorage:', e);
        }
    });
}

// 应用主题
function applyTheme(theme) {
    // 移除所有主题类（从body和html）
    $('body').removeClass('theme-pink theme-blue theme-purple theme-green theme-orange theme-gray');
    document.documentElement.className = document.documentElement.className.replace(/theme-\w+/g, '').trim();
    
    // 添加新主题类（同时到body和html）
    if (theme && theme !== 'pink') {
        $('body').addClass('theme-' + theme);
        document.documentElement.classList.add('theme-' + theme);
    }
    
    // 保持深色模式状态
    if ($('body').hasClass('dark-mode')) {
        document.documentElement.classList.add('dark-mode');
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
    
    const darkMode = isChecked ? 'auto' : ($('body').hasClass('dark-mode') ? 'dark' : 'light');
    
    // 保存到服务器
    saveDarkModeToServer(darkMode);
    
    if (isChecked) {
        initDarkMode();
        showToast('已开启自动日夜切换', 'success');
    } else {
        showToast('已关闭自动日夜切换', 'info');
    }
}

// 保存深色模式到服务器
function saveDarkModeToServer(darkMode) {
    fetch('/settings/update-theme', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            dark_mode: darkMode
        })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.success && !data.saved_to_server) {
            // 游客用户，保存到localStorage
            try {
                localStorage.setItem('darkMode', darkMode);
            } catch (e) {
                console.warn('无法保存到localStorage:', e);
            }
        }
    })
    .catch(function(error) {
        console.warn('保存深色模式设置失败，使用localStorage备用:', error);
        // 保存到localStorage作为备用
        try {
            localStorage.setItem('darkMode', darkMode);
        } catch (e) {
            console.warn('无法保存到localStorage:', e);
        }
    });
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
    
    // 从HTML元素读取服务器设置的深色模式状态
    var isDark = document.documentElement.classList.contains('dark-mode');
    var isAuto = !document.body.dataset.darkModeManual;
    
    // 如果是游客用户，尝试从localStorage读取
    if (!document.body.dataset.loggedIn || document.body.dataset.loggedIn === 'false') {
        try {
            var localDarkMode = localStorage.getItem('darkMode');
            if (localDarkMode === 'dark') {
                isDark = true;
                isAuto = false;
            } else if (localDarkMode === 'light') {
                isDark = false;
                isAuto = false;
            } else if (localDarkMode === 'auto') {
                isAuto = true;
                var hour = new Date().getHours();
                isDark = hour >= 18 || hour < 6;
            }
        } catch (e) {
            console.warn('无法读取localStorage:', e);
        }
    }
    
    if (isDark) {
        $('body').addClass('dark-mode');
    } else {
        $('body').removeClass('dark-mode');
    }
    
    updateDarkModeButton(isDark);
    
    // 更新滑块状态
    $('#autoDarkModeToggle').prop('checked', isAuto);
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
        
        // 保存到服务器（手动模式）
        const darkMode = isDark ? 'dark' : 'light';
        saveDarkModeToServer(darkMode);
        
        // 关闭自动模式
        $('#autoDarkModeToggle').prop('checked', false);
        document.body.dataset.darkModeManual = 'true';
        
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
