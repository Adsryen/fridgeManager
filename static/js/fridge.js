// 全局变量
let allItems = [];
let currentFilter = 'all';
let currentPlace = 'all';
let currentMode = {
    is_logged_in: false,
    is_admin: false,
    is_public: true,
    effective_user_id: 'public'
};
let expiryWarningDays = 3; // 默认值，将从服务器获取

// 页面加载完成后初始化
$(document).ready(function() {
    loadSystemSettings();
    initCurrentMode();
    initEventListeners();
});

// 加载系统设置
function loadSystemSettings() {
    $.ajax({
        type: 'GET',
        url: '/item/get-system-settings',
        success: function(settings) {
            expiryWarningDays = settings.default_expiry_warning_days || 3;
        },
        error: function() {
            expiryWarningDays = 3; // 使用默认值
        }
    });
}

// 初始化事件监听器
function initEventListeners() {
    // 搜索功能
    $('#searchInput').on('input', function() {
        const searchText = $(this).val().toLowerCase();
        filterItems(searchText);
    });

    // 添加物品表单提交
    $('#addItemForm').on('submit', function(e) {
        e.preventDefault();
        addItem();
    });

    // 编辑物品表单提交
    $('#editItemForm').on('submit', function(e) {
        e.preventDefault();
        updateItem();
    });

    // 类别标签点击事件 - 添加表单
    $('#addItemModal .category-tag').on('click', function() {
        $(this).toggleClass('selected');
        updateSelectedTypes('#selectedTypes', '#addItemModal');
    });

    // 类别标签点击事件 - 编辑表单
    $('#editItemModal .category-tag').on('click', function() {
        $(this).toggleClass('selected');
        updateSelectedTypes('#editSelectedTypes', '#editItemModal');
    });

    // 模态框关闭时重置表单
    $('#addItemModal').on('hidden.bs.modal', function() {
        $('#addItemForm')[0].reset();
        $('#addItemModal .category-tag').removeClass('selected');
        $('#selectedTypes').val('');
    });
}

// 更新选中的类别
function updateSelectedTypes(inputId, modalId) {
    const selectedTypes = [];
    $(`${modalId} .category-tag.selected`).each(function() {
        selectedTypes.push($(this).data('type'));
    });
    $(inputId).val(selectedTypes.join(','));
}

// 初始化当前模式
function initCurrentMode() {
    $.ajax({
        type: 'GET',
        url: '/item/get-current-mode',
        success: function(mode) {
            currentMode = mode;
            updateUIForMode();
            loadAllItems();
            
            // 如果是管理员，加载用户列表
            if (mode.is_admin) {
                loadUsersList();
            }
        },
        error: function() {
            // 默认为游客模式 - 显示公共冰箱
            currentMode = {
                is_logged_in: false,
                is_admin: false,
                is_public: true,
                effective_user_id: 'public'
            };
            updateUIForMode();
            loadAllItems();
        }
    });
}

// 更新UI以反映当前模式
function updateUIForMode() {
    // 先移除所有按钮的激活状态
    $('.view-btn').removeClass('active');
    
    // 更新标题和按钮状态
    if (currentMode.is_public) {
        $('#fridgeTitle').text('公共冰箱');
        $('.view-btn[data-mode="public"]').addClass('active');
    } else if (currentMode.view_user_id && currentMode.is_admin) {
        $('#fridgeTitle').text('用户冰箱');
    } else {
        $('#fridgeTitle').text(currentMode.is_logged_in ? '我的冰箱' : '公共冰箱');
        if (currentMode.is_logged_in) {
            $('.view-btn[data-mode="private"]').addClass('active');
        }
    }
    
    // 显示/隐藏视图切换器
    if (currentMode.is_logged_in) {
        $('#viewSwitcher').show();
    } else {
        $('#viewSwitcher').hide();
    }
    
    // 显示/隐藏管理员用户选择器
    if (currentMode.is_admin) {
        $('#adminUserSelector').show();
    } else {
        $('#adminUserSelector').hide();
    }
}

// 切换视图模式
function switchViewMode(mode) {
    $.ajax({
        type: 'POST',
        url: '/item/switch-mode',
        contentType: 'application/json',
        data: JSON.stringify({ mode: mode }),
        success: function() {
            // 清除管理员选择的用户
            $('#userSelect').val('');
            initCurrentMode();
        },
        error: function() {
            showError('切换失败，请重试');
        }
    });
}

// 加载用户列表（管理员）
function loadUsersList() {
    $.ajax({
        type: 'GET',
        url: '/item/get-users-list',
        success: function(users) {
            const select = $('#userSelect');
            select.empty();
            select.append('<option value="">选择用户...</option>');
            
            users.forEach(user => {
                const option = $('<option></option>')
                    .val(user._id)
                    .text(user.username + (user.email ? ` (${user.email})` : ''));
                select.append(option);
            });
            
            // 如果当前正在查看某个用户，选中它
            if (currentMode.view_user_id) {
                select.val(currentMode.view_user_id);
            }
        },
        error: function() {
            console.error('加载用户列表失败');
        }
    });
}

// 切换用户（管理员）
function switchUser() {
    const userId = $('#userSelect').val();
    
    if (!userId) {
        // 如果没有选择用户，回到自己的冰箱
        switchViewMode('private');
        return;
    }
    
    $.ajax({
        type: 'POST',
        url: '/item/switch-user',
        contentType: 'application/json',
        data: JSON.stringify({ user_id: userId }),
        success: function() {
            initCurrentMode();
        },
        error: function() {
            showError('切换失败，请重试');
        }
    });
}

// 加载所有物品
function loadAllItems() {
    $.ajax({
        type: 'POST',
        url: '/item/total',
        success: function(items) {
            allItems = items;
            updateStatistics();
            updateFridgeSections();
            displayItems(items);
            checkExpiring();
        },
        error: function() {
            showError('加载物品失败');
        }
    });
}

// 更新统计信息
function updateStatistics() {
    const now = moment();
    let fresh = 0, expiringSoon = 0, expired = 0;

    allItems.forEach(item => {
        const expireDate = moment(item.ExpireDate);
        const daysUntilExpire = expireDate.diff(now, 'days');

        if (daysUntilExpire < 0) {
            expired++;
        } else if (daysUntilExpire <= expiryWarningDays) {
            expiringSoon++;
        } else {
            fresh++;
        }
    });

    $('#totalCount').text(allItems.length);
    $('#freshCount').text(fresh);
    $('#expiringSoonCount').text(expiringSoon);
    $('#expiredCount').text(expired);
}

// 更新冰箱分区显示
function updateFridgeSections() {
    const sections = {
        cold: { count: 0, fresh: 0, warning: 0, danger: 0 },
        frozer: { count: 0, fresh: 0, warning: 0, danger: 0 },
        room: { count: 0, fresh: 0, warning: 0, danger: 0 }
    };

    const now = moment();

    allItems.forEach(item => {
        const place = item.Place;
        if (!sections[place]) return;

        sections[place].count++;

        const expireDate = moment(item.ExpireDate);
        const daysUntilExpire = expireDate.diff(now, 'days');

        if (daysUntilExpire < 0) {
            sections[place].danger++;
        } else if (daysUntilExpire <= expiryWarningDays) {
            sections[place].warning++;
        } else {
            sections[place].fresh++;
        }
    });

    // 更新每个分区
    Object.keys(sections).forEach(place => {
        const section = sections[place];
        $(`#${place}Count`).text(section.count);

        let statusHtml = '';
        if (section.fresh > 0) {
            statusHtml += `<span class="status-badge fresh"><i class="fas fa-check-circle"></i> ${section.fresh}</span>`;
        }
        if (section.warning > 0) {
            statusHtml += `<span class="status-badge warning"><i class="fas fa-exclamation-triangle"></i> ${section.warning}</span>`;
        }
        if (section.danger > 0) {
            statusHtml += `<span class="status-badge danger"><i class="fas fa-times-circle"></i> ${section.danger}</span>`;
        }

        $(`#${place}Status`).html(statusHtml);
    });
}

// 检查过期提醒
function checkExpiring() {
    const now = moment();
    const expiringSoon = [];
    const expired = [];

    allItems.forEach(item => {
        const expireDate = moment(item.ExpireDate);
        const daysUntilExpire = expireDate.diff(now, 'days');

        if (daysUntilExpire < 0) {
            expired.push(item);
        } else if (daysUntilExpire <= expiryWarningDays) {
            expiringSoon.push(item);
        }
    });

    // 显示通知栏
    if (expired.length > 0 || expiringSoon.length > 0) {
        let notificationHtml = '';

        if (expired.length > 0) {
            notificationHtml += `
                <div class="notification-bar danger">
                    <i class="fas fa-exclamation-circle"></i>
                    <strong>紧急提醒：</strong> 有 ${expired.length} 个物品已过期，请及时处理！
                    <button class="btn btn-sm btn-danger ms-3" onclick="showExpired()">查看</button>
                </div>
            `;
        }

        if (expiringSoon.length > 0) {
            notificationHtml += `
                <div class="notification-bar">
                    <i class="fas fa-exclamation-triangle"></i>
                    <strong>提醒：</strong> 有 ${expiringSoon.length} 个物品即将过期（${expiryWarningDays}天内）
                    <button class="btn btn-sm btn-warning ms-3" onclick="showExpiringSoon()">查看</button>
                </div>
            `;
        }

        $('#notificationBar').html(notificationHtml).show();
    }
}

// 显示物品列表
function displayItems(items) {
    const container = $('#itemsContainer');

    if (items.length === 0) {
        container.html(`
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <h4>暂无物品</h4>
                <p>点击"添加物品"按钮开始管理你的冰箱</p>
            </div>
        `);
        return;
    }

    const now = moment();
    let html = '';

    items.forEach(item => {
        const expireDate = moment(item.ExpireDate);
        const daysUntilExpire = expireDate.diff(now, 'days');

        let statusClass = '';
        let statusText = '';
        let statusColor = '';

        if (daysUntilExpire < 0) {
            statusClass = 'expired';
            statusText = `已过期 ${Math.abs(daysUntilExpire)} 天`;
            statusColor = 'text-danger';
        } else if (daysUntilExpire === 0) {
            statusClass = 'expiring-soon';
            statusText = '今天过期';
            statusColor = 'text-danger';
        } else if (daysUntilExpire <= expiryWarningDays) {
            statusClass = 'expiring-soon';
            statusText = `还剩 ${daysUntilExpire} 天`;
            statusColor = 'text-warning';
        } else if (daysUntilExpire <= 7) {
            statusText = `还剩 ${daysUntilExpire} 天`;
            statusColor = 'text-info';
        } else {
            statusText = `还剩 ${daysUntilExpire} 天`;
            statusColor = 'text-success';
        }

        const icon = getTypeIcon(item.Type);
        const placeText = getPlaceText(item.Place);
        const typeText = getTypeText(item.Type);
        const typeIcons = getTypeIcons(item.Type);

        html += `
            <div class="item-card ${statusClass}">
                <div class="item-header">
                    <div class="item-name">${item.Name}</div>
                    <div class="item-icon">${typeIcons}</div>
                </div>
                <div class="item-details">
                    <div class="item-detail">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>${placeText}</span>
                    </div>
                    <div class="item-detail">
                        <i class="fas fa-tag"></i>
                        <span>${typeText}</span>
                    </div>
                    <div class="item-detail">
                        <i class="fas fa-calendar-alt"></i>
                        <span>${expireDate.format('YYYY-MM-DD')}</span>
                    </div>
                    <div class="item-detail">
                        <i class="fas fa-clock ${statusColor}"></i>
                        <strong class="${statusColor}">${statusText}</strong>
                    </div>
                    <div class="item-detail">
                        <i class="fas fa-boxes"></i>
                        <span>数量：${item.Num}</span>
                    </div>
                </div>
                <div class="item-actions">
                    <button class="item-action-btn edit" onclick="editItem('${item._id}')">
                        <i class="fas fa-edit"></i> 编辑
                    </button>
                    <button class="item-action-btn delete" onclick="deleteItem('${item._id}', '${item.Name}')">
                        <i class="fas fa-trash"></i> 删除
                    </button>
                </div>
            </div>
        `;
    });

    container.html(html);
}

// 筛选物品
function filterItems(searchText = '') {
    let filtered = allItems;

    // 按位置筛选
    if (currentPlace !== 'all') {
        filtered = filtered.filter(item => item.Place === currentPlace);
    }

    // 按状态筛选
    const now = moment();
    if (currentFilter === 'expiring') {
        filtered = filtered.filter(item => {
            const days = moment(item.ExpireDate).diff(now, 'days');
            return days >= 0 && days <= expiryWarningDays;
        });
    } else if (currentFilter === 'expired') {
        filtered = filtered.filter(item => {
            return moment(item.ExpireDate).diff(now, 'days') < 0;
        });
    }

    // 按搜索文本筛选
    if (searchText) {
        filtered = filtered.filter(item => 
            item.Name.toLowerCase().includes(searchText)
        );
    }

    displayItems(filtered);
}

// 按位置筛选
function filterByPlace(place) {
    currentPlace = place;
    currentFilter = 'all';

    // 更新UI
    $('.fridge-section').removeClass('active');
    $(`.fridge-section[data-place="${place}"]`).addClass('active');

    filterItems($('#searchInput').val().toLowerCase());
}

// 显示全部物品
function showAllItems() {
    currentFilter = 'all';
    currentPlace = 'all';
    $('.fridge-section').removeClass('active');
    $('#searchInput').val('');
    displayItems(allItems);
}

// 显示即将过期
function showExpiringSoon() {
    currentFilter = 'expiring';
    currentPlace = 'all';
    $('.fridge-section').removeClass('active');
    $('#searchInput').val('');
    filterItems();
}

// 显示已过期
function showExpired() {
    currentFilter = 'expired';
    currentPlace = 'all';
    $('.fridge-section').removeClass('active');
    $('#searchInput').val('');
    filterItems();
}

// 添加物品
function addItem() {
    // 验证是否选择了类别
    const selectedTypes = $('#selectedTypes').val();
    if (!selectedTypes) {
        showError('请至少选择一个类别');
        return;
    }

    const formData = $('#addItemForm').serialize();

    $.ajax({
        type: 'POST',
        url: '/item/insert',
        data: formData,
        success: function() {
            $('#addItemModal').modal('hide');
            $('#addItemForm')[0].reset();
            $('#addItemModal .category-tag').removeClass('selected');
            $('#selectedTypes').val('');
            showSuccess('物品添加成功');
            loadAllItems();
        },
        error: function() {
            showError('添加失败，请重试');
        }
    });
}

// 编辑物品
function editItem(itemId) {
    $.ajax({
        type: 'POST',
        url: '/item/getone/' + itemId,
        success: function(items) {
            if (items.length > 0) {
                const item = items[0];
                const form = $('#editItemForm');

                form.find('[name="itemId"]').val(item._id);
                form.find('[name="itemName"]').val(item.Name);
                form.find('[name="itemDate"]').val(moment(item.ExpireDate).format('YYYY-MM-DD'));
                form.find('[name="itemNum"]').val(item.Num);
                form.find('[name="itemPlace"]').val(item.Place);

                // 处理类别标签选择
                $('#editItemModal .category-tag').removeClass('selected');
                const types = item.Type.split(',');
                types.forEach(type => {
                    $(`#editItemModal .category-tag[data-type="${type.trim()}"]`).addClass('selected');
                });
                $('#editSelectedTypes').val(item.Type);

                $('#editItemModal').modal('show');
            }
        },
        error: function() {
            showError('获取物品信息失败');
        }
    });
}

// 更新物品
function updateItem() {
    // 验证是否选择了类别
    const selectedTypes = $('#editSelectedTypes').val();
    if (!selectedTypes) {
        showError('请至少选择一个类别');
        return;
    }

    const itemId = $('#editItemForm').find('[name="itemId"]').val();
    const formData = $('#editItemForm').serialize();

    $.ajax({
        type: 'POST',
        url: '/item/edit/' + itemId,
        data: formData,
        success: function() {
            $('#editItemModal').modal('hide');
            showSuccess('物品更新成功');
            loadAllItems();
        },
        error: function() {
            showError('更新失败，请重试');
        }
    });
}

// 删除物品
function deleteItem(itemId, itemName) {
    if (!confirm(`确定要删除 "${itemName}" 吗？`)) {
        return;
    }

    $.ajax({
        type: 'POST',
        url: '/item/delete/' + itemId,
        success: function() {
            showSuccess('物品已删除');
            loadAllItems();
        },
        error: function() {
            showError('删除失败，请重试');
        }
    });
}

// 获取类型图标
function getTypeIcon(type) {
    const icons = {
        vegetable: '🥬',
        fruit: '🍎',
        seafood: '🐟',
        meat: '🥩',
        beverage: '🥤',
        diary: '🥛',
        egg: '🥚',
        bread: '🍞',
        frozen: '🍦',
        sauce: '🍯',
        snack: '🍿',
        other: '📦'
    };
    return icons[type] || '📦';
}

// 获取多个类型图标
function getTypeIcons(typeString) {
    const types = typeString.split(',');
    const icons = types.map(type => getTypeIcon(type.trim())).join(' ');
    return icons;
}

// 获取位置文本
function getPlaceText(place) {
    const places = {
        cold: '冷藏室',
        frozer: '冷冻室',
        room: '室温区'
    };
    return places[place] || place;
}

// 获取类型文本
function getTypeText(type) {
    const types = {
        vegetable: '蔬菜',
        fruit: '水果',
        seafood: '海鲜',
        meat: '肉类',
        beverage: '饮料',
        diary: '乳制品',
        egg: '蛋豆类',
        bread: '面包',
        frozen: '冷冻食品',
        sauce: '酱料',
        snack: '零食',
        other: '其他'
    };
    
    // 处理多个类别
    const typeArray = type.split(',');
    const typeTexts = typeArray.map(t => types[t.trim()] || t.trim());
    return typeTexts.join('、');
}

// 显示成功消息
function showSuccess(message) {
    // 可以使用 toast 或其他通知组件
    alert(message);
}

// 显示错误消息
function showError(message) {
    alert(message);
}
