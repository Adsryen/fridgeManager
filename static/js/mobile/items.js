// 物品管理模块

// 全局变量
let allItems = [];
let currentFilter = 'all';
let currentPlace = 'all';
let expiryWarningDays = 3;

// 加载所有物品
function loadAllItems() {
    $.ajax({
        type: 'POST',
        url: '/item/total',
        success: function(items) {
            allItems = items;
            updateStatistics();
            updatePlaceCounts();
            updateCategoryCounts();
            displayItems(items);
        },
        error: function() {
            showToast('加载失败', 'error');
        }
    });
}

// 更新统计信息
function updateStatistics() {
    const now = moment();
    let expiringSoon = 0, expired = 0;

    allItems.forEach(item => {
        const expireDate = moment(item.ExpireDate);
        const daysUntilExpire = expireDate.diff(now, 'days');

        if (daysUntilExpire < 0) {
            expired++;
        } else if (daysUntilExpire <= expiryWarningDays) {
            expiringSoon++;
        }
    });

    $('#mTotalCount').text(allItems.length);
    $('#mExpiringSoonCount').text(expiringSoon);
    $('#mExpiredCount').text(expired);
}

// 更新位置统计
function updatePlaceCounts() {
    const counts = { cold: 0, frozer: 0, room: 0 };
    
    allItems.forEach(item => {
        if (counts.hasOwnProperty(item.Place)) {
            counts[item.Place]++;
        }
    });
    
    // 只在数量不为0时显示气泡
    if (counts.cold > 0) {
        $('#mColdCount').text(counts.cold).show();
    } else {
        $('#mColdCount').hide();
    }
    
    if (counts.frozer > 0) {
        $('#mFrozerCount').text(counts.frozer).show();
    } else {
        $('#mFrozerCount').hide();
    }
    
    if (counts.room > 0) {
        $('#mRoomCount').text(counts.room).show();
    } else {
        $('#mRoomCount').hide();
    }
}

// 更新分类统计
function updateCategoryCounts() {
    const categories = ['vegetable', 'fruit', 'meat', 'seafood', 'diary', 'beverage', 'egg', 'bread', 'frozen', 'sauce', 'snack', 'other'];
    const counts = {};
    let totalCount = 0;
    
    // 初始化计数
    categories.forEach(cat => counts[cat] = 0);
    
    // 统计每个分类的数量
    allItems.forEach(item => {
        const types = Array.isArray(item.Type) ? item.Type : [item.Type];
        types.forEach(type => {
            if (counts.hasOwnProperty(type)) {
                counts[type]++;
            }
        });
        totalCount++;
    });
    
    // 更新分类卡片的计数（首页）
    categories.forEach(cat => {
        const countElement = $(`#cat${cat.charAt(0).toUpperCase() + cat.slice(1)}Count`);
        if (counts[cat] > 0) {
            countElement.text(counts[cat]).show();
        } else {
            countElement.hide();
        }
    });
    
    // 更新分类标签的计数（底部标签栏）
    if (totalCount > 0) {
        $('#tagAllCount').text(totalCount).show();
    } else {
        $('#tagAllCount').hide();
    }
    
    categories.forEach(cat => {
        const tagCountElement = $(`#tag${cat.charAt(0).toUpperCase() + cat.slice(1)}Count`);
        if (counts[cat] > 0) {
            tagCountElement.text(counts[cat]).show();
        } else {
            tagCountElement.hide();
        }
    });
}

// 显示物品列表
function displayItems(items) {
    const container = $('#mItemsContainer');
    
    if (!items || items.length === 0) {
        showEmptyState(container);
        return;
    }
    
    let html = '';
    
    items.forEach(item => {
        const expireDate = moment(item.ExpireDate);
        const { statusClass, statusBadgeClass, statusText } = getExpiryStatus(item.ExpireDate);
        const emoji = getTypeEmoji(item.Type);
        const placeText = getPlaceText(item.Place);

        html += `
            <div class="mobile-item-card ${statusClass}">
                <div class="item-card-main">
                    <div class="item-card-header">
                        <div class="item-emoji">${emoji}</div>
                        <div class="item-name-info">
                            <h3>${item.Name}</h3>
                        </div>
                    </div>
                    <div class="item-card-body">
                        <div class="item-info-row-group">
                            <span class="item-info-inline">
                                <i class="fas fa-map-marker-alt"></i>
                                ${placeText}
                            </span>
                            <span class="item-info-inline">
                                <i class="fas fa-calendar-alt"></i>
                                ${expireDate.format('MM-DD')}
                            </span>
                            <span class="item-info-inline">
                                <i class="fas fa-boxes"></i>
                                ×${item.Num}
                            </span>
                        </div>
                        <div class="item-bottom-row">
                            <div class="item-expiry-status ${statusBadgeClass}">
                                <span>${statusText}</span>
                            </div>
                            <button class="item-action-btn take-out" onclick="takeOutItem('${item._id}', '${item.Name}', ${item.Num})" title="取出">
                                <i class="fas fa-hand-holding"></i>
                            </button>
                            <button class="item-action-btn edit" onclick="editItem('${item._id}')" title="编辑">
                                <i class="fas fa-edit"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="item-card-actions">
                    <button class="item-action-btn delete" onclick="deleteItem('${item._id}', '${item.Name}')" title="删除">
                        <i class="fas fa-trash"></i>
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
    
    // 按类别筛选
    if (currentFilter !== 'all') {
        filtered = filtered.filter(item => {
            if (Array.isArray(item.Type)) {
                return item.Type.includes(currentFilter);
            }
            return item.Type === currentFilter;
        });
    }
    
    // 按搜索文本筛选
    if (searchText) {
        filtered = filtered.filter(item => 
            item.Name.toLowerCase().includes(searchText.toLowerCase())
        );
    }
    
    displayItems(filtered);
}

// 按位置筛选
function filterByPlace(place) {
    currentPlace = place;
    
    $('.sidebar-item').removeClass('active');
    $(`.sidebar-item[data-place="${place}"]`).addClass('active');
    
    filterItems($('#mSearchInput').val());
}

// 按类别筛选
function filterByCategory(type) {
    currentFilter = type;
    
    $('.category-tag').removeClass('active');
    $(`.category-tag[data-type="${type}"]`).addClass('active');
    
    filterItems($('#mSearchInput').val());
}

// 显示所有物品
function showAllItems() {
    currentFilter = 'all';
    currentPlace = 'all';
    
    $('.sidebar-item').removeClass('active');
    $('.sidebar-item[data-place="all"]').addClass('active');
    $('.category-tag').removeClass('active');
    $('.category-tag[data-type="all"]').addClass('active');
    
    displayItems(allItems);
}

// 显示即将过期的物品
function showExpiringSoon() {
    const now = moment();
    const filtered = allItems.filter(item => {
        const expireDate = moment(item.ExpireDate);
        const daysUntilExpire = expireDate.diff(now, 'days');
        return daysUntilExpire >= 0 && daysUntilExpire <= expiryWarningDays;
    });
    
    displayItems(filtered);
}

// 显示已过期的物品
function showExpired() {
    const now = moment();
    const filtered = allItems.filter(item => {
        const expireDate = moment(item.ExpireDate);
        return expireDate.diff(now, 'days') < 0;
    });
    
    displayItems(filtered);
}

// 删除物品
function deleteItem(itemId, itemName) {
    if (!confirm(`确定要删除"${itemName}"吗？`)) {
        return;
    }
    
    $.ajax({
        url: '/item/delete',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ itemId: itemId }),
        success: function(response) {
            if (response.success) {
                showToast('删除成功', 'success');
                loadAllItems();
            } else {
                showToast(response.message || '删除失败', 'error');
            }
        },
        error: function() {
            showToast('网络错误，请重试', 'error');
        }
    });
}

// 编辑物品
function editItem(itemId) {
    const item = allItems.find(i => i._id === itemId);
    if (!item) {
        showToast('物品不存在', 'error');
        return;
    }
    
    // 填充表单
    $('#mEditItemForm input[name="itemId"]').val(item._id);
    $('#mEditItemForm input[name="itemName"]').val(item.Name);
    $('#mEditItemForm input[name="itemDate"]').val(moment(item.ExpireDate).format('YYYY-MM-DD'));
    $('#mEditItemForm input[name="itemNum"]').val(item.Num);
    $('#mEditItemForm input[name="itemPlace"][value="' + item.Place + '"]').prop('checked', true);
    
    // 处理类别选择
    $('#editCategoryGrid .category-item').removeClass('selected');
    const types = Array.isArray(item.Type) ? item.Type : [item.Type];
    types.forEach(type => {
        $(`#editCategoryGrid .category-item[data-type="${type}"]`).addClass('selected');
    });
    $('#mEditSelectedTypes').val(types.join(','));
    
    openDrawer('editItemDrawer');
}

// 取出物品
function takeOutItem(itemId, itemName, currentNum) {
    console.log('取出物品:', itemId, itemName, currentNum);
    showTakeOutDrawer(itemId, itemName, currentNum);
}

// 显示取出数量选择抽屉
function showTakeOutDrawer(itemId, itemName, currentNum) {
    const drawerHtml = `
        <div class="drawer-overlay active" id="takeOutDrawer">
            <div class="drawer-content">
                <div class="drawer-header">
                    <h5><i class="fas fa-hand-holding"></i> 取出物品</h5>
                    <button class="close-btn" onclick="closeDrawer('takeOutDrawer')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="drawer-body">
                    <div class="take-out-info">
                        <h4>${itemName}</h4>
                        <p>当前数量：${currentNum}</p>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-boxes"></i> 取出数量</label>
                        <div class="quantity-selector">
                            <button type="button" class="qty-btn minus" onclick="adjustTakeOutQty(-1)">
                                <i class="fas fa-minus"></i>
                            </button>
                            <input type="number" id="takeOutQty" class="qty-input" value="1" min="1" max="${currentNum}">
                            <button type="button" class="qty-btn plus" onclick="adjustTakeOutQty(1)">
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                        <div class="qty-shortcuts">
                            <button type="button" class="qty-shortcut-btn" onclick="setTakeOutQty(1)">1个</button>
                            ${currentNum >= 2 ? `<button type="button" class="qty-shortcut-btn" onclick="setTakeOutQty(${Math.floor(currentNum/2)})">${Math.floor(currentNum/2)}个</button>` : ''}
                            <button type="button" class="qty-shortcut-btn" onclick="setTakeOutQty(${currentNum})">全部</button>
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="button" class="btn-secondary" onclick="closeDrawer('takeOutDrawer')">取消</button>
                        <button type="button" class="btn-primary" onclick="confirmTakeOut('${itemId}', ${currentNum})">
                            <i class="fas fa-check"></i> 确认取出
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    $('#takeOutDrawer').remove();
    $('body').append(drawerHtml);
}

// 调整取出数量
function adjustTakeOutQty(delta) {
    const input = $('#takeOutQty');
    const currentVal = parseInt(input.val()) || 1;
    const min = parseInt(input.attr('min'));
    const max = parseInt(input.attr('max'));
    const newVal = Math.max(min, Math.min(max, currentVal + delta));
    input.val(newVal);
}

// 设置取出数量
function setTakeOutQty(qty) {
    $('#takeOutQty').val(qty);
}

// 确认取出
function confirmTakeOut(itemId, currentNum) {
    const takeOutQty = parseInt($('#takeOutQty').val());
    
    if (!takeOutQty || takeOutQty < 1) {
        showToast('请输入有效的数量', 'error');
        return;
    }
    
    if (takeOutQty > currentNum) {
        showToast('取出数量不能超过当前数量', 'error');
        return;
    }
    
    const remainingQty = currentNum - takeOutQty;
    
    closeDrawer('takeOutDrawer');
    
    if (remainingQty === 0) {
        if (confirm('取出后数量为0，是否删除该物品卡片？\n\n点击"确定"删除卡片\n点击"取消"保留卡片（数量为0）')) {
            deleteItemById(itemId);
        } else {
            updateItemQuantity(itemId, 0, takeOutQty);
        }
    } else {
        updateItemQuantity(itemId, remainingQty, takeOutQty);
    }
}

// 更新物品数量
function updateItemQuantity(itemId, newQty, takeOutQty) {
    $.ajax({
        url: '/item/update',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            itemId: itemId,
            itemNum: newQty
        }),
        success: function(response) {
            if (response.success) {
                if (newQty === 0) {
                    showToast(`已取出 ${takeOutQty} 个，卡片已保留`, 'success');
                } else {
                    showToast(`已取出 ${takeOutQty} 个，剩余 ${newQty} 个`, 'success');
                }
                loadAllItems();
            } else {
                showToast(response.message || '更新失败', 'error');
            }
        },
        error: function() {
            showToast('网络错误，请重试', 'error');
        }
    });
}

// 通过ID删除物品（不弹确认框）
function deleteItemById(itemId) {
    $.ajax({
        url: '/item/delete',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ itemId: itemId }),
        success: function(response) {
            if (response.success) {
                showToast('已取出并移除', 'success');
                loadAllItems();
            } else {
                showToast(response.message || '删除失败', 'error');
            }
        },
        error: function() {
            showToast('网络错误，请重试', 'error');
        }
    });
}
