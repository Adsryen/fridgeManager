// 冰箱管理功能
let currentFridgeId = 'public'; // 当前选中的冰箱ID
let userFridges = []; // 用户的冰箱列表

// 从body的data属性读取登录状态
window.isLoggedIn = document.body.dataset.loggedIn === 'true';

/**
 * 加载用户的冰箱列表
 */
async function loadUserFridges() {
    try {
        const response = await fetch('/fridge/list');
        const data = await response.json();
        
        if (data.success) {
            userFridges = data.fridges;
            renderFridgeTabs();
        }
    } catch (error) {
        console.error('加载冰箱列表失败:', error);
    }
}

/**
 * 渲染冰箱选择标签
 */
function renderFridgeTabs() {
    const container = document.querySelector('.fridge-selector-scroll');
    if (!container) return;
    
    // 清空现有内容
    container.innerHTML = '';
    
    // 添加公共冰箱
    const publicTab = document.createElement('div');
    publicTab.className = 'fridge-tab' + (currentFridgeId === 'public' ? ' active' : '');
    publicTab.dataset.fridge = 'public';
    publicTab.onclick = () => switchFridge('public');
    publicTab.innerHTML = `
        <i class="fas fa-users"></i>
        <span>公共冰箱</span>
    `;
    container.appendChild(publicTab);
    
    // 添加用户的私人冰箱
    userFridges.forEach(fridge => {
        const tab = document.createElement('div');
        tab.className = 'fridge-tab' + (currentFridgeId === fridge._id ? ' active' : '');
        tab.dataset.fridge = fridge._id;
        tab.onclick = () => switchFridge(fridge._id);
        tab.innerHTML = `
            <i class="fas fa-home"></i>
            <span>${escapeHtml(fridge.name)}</span>
        `;
        container.appendChild(tab);
    });
    
    // 添加"添加冰箱"按钮
    const addTab = document.createElement('div');
    addTab.className = 'fridge-tab add-fridge';
    addTab.onclick = openAddFridgeDrawer;
    addTab.innerHTML = `
        <i class="fas fa-plus-circle"></i>
        <span>添加冰箱</span>
    `;
    container.appendChild(addTab);
}

/**
 * 切换冰箱
 */
async function switchFridge(fridgeId) {
    try {
        // 调用API切换冰箱
        const response = await fetch('/fridge/switch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ fridge_id: fridgeId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentFridgeId = fridgeId;
            
            // 更新UI
            document.querySelectorAll('.fridge-tab').forEach(tab => {
                tab.classList.toggle('active', tab.dataset.fridge === fridgeId);
            });
            
            // 重新加载物品列表
            if (typeof loadAllItems === 'function') {
                loadAllItems();
            }
            
            showToast(data.message || '切换成功', 'success');
        } else {
            showToast(data.error || '切换失败', 'error');
        }
    } catch (error) {
        console.error('切换冰箱失败:', error);
        showToast('切换失败', 'error');
    }
}

/**
 * 打开添加冰箱抽屉
 */
function openAddFridgeDrawer() {
    // 先移除可能存在的旧抽屉
    const oldDrawer = document.getElementById('addFridgeDrawer');
    if (oldDrawer) {
        oldDrawer.remove();
    }
    
    const html = `
        <div class="drawer-overlay" id="addFridgeDrawer">
            <div class="drawer-content">
                <div class="drawer-header">
                    <h5><i class="fas fa-plus-circle"></i> 添加冰箱</h5>
                    <button class="close-btn" onclick="closeDrawer('addFridgeDrawer')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="drawer-body">
                    <form id="addFridgeForm">
                        <div class="form-group">
                            <label><i class="fas fa-tag"></i> 冰箱名称</label>
                            <input type="text" name="fridgeName" class="mobile-input" 
                                   placeholder="例如：家里的冰箱、办公室冰箱..." 
                                   maxlength="20" required autocomplete="off">
                            <small class="text-muted">最多20个字符</small>
                        </div>
                        <div class="form-actions">
                            <button type="button" class="btn-secondary" onclick="closeDrawer('addFridgeDrawer')">取消</button>
                            <button type="submit" class="btn-primary">
                                <i class="fas fa-check"></i> 创建
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', html);
    
    // 绑定表单提交事件
    document.getElementById('addFridgeForm').addEventListener('submit', handleAddFridge);
    
    // 显示抽屉
    setTimeout(() => {
        document.getElementById('addFridgeDrawer').classList.add('active');
        // 聚焦到输入框
        document.querySelector('#addFridgeForm input[name="fridgeName"]').focus();
    }, 10);
}

/**
 * 处理添加冰箱
 */
async function handleAddFridge(e) {
    e.preventDefault();
    
    const form = e.target;
    const name = form.fridgeName.value.trim();
    
    if (!name) {
        showToast('请输入冰箱名称', 'error');
        return;
    }
    
    try {
        const response = await fetch('/fridge/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('创建成功', 'success');
            closeDrawer('addFridgeDrawer');
            
            // 重新加载冰箱列表
            await loadUserFridges();
            
            // 自动切换到新创建的冰箱
            await switchFridge(data.fridge._id);
        } else {
            showToast(data.error || '创建失败', 'error');
        }
    } catch (error) {
        console.error('创建冰箱失败:', error);
        showToast('创建失败', 'error');
    }
}

/**
 * 打开管理冰箱抽屉
 */
function openManageFridgeDrawer() {
    // 先移除可能存在的旧抽屉
    const oldDrawer = document.getElementById('manageFridgeDrawer');
    if (oldDrawer) {
        oldDrawer.remove();
    }
    
    const fridgeListHtml = userFridges.map(fridge => `
        <div class="fridge-manage-item" data-fridge-id="${fridge._id}">
            <div class="fridge-info">
                <i class="fas fa-home"></i>
                <div class="fridge-details">
                    <div class="fridge-name">${escapeHtml(fridge.name)}</div>
                    <div class="fridge-count">${fridge.item_count || 0} 件物品</div>
                </div>
            </div>
            <div class="fridge-actions">
                <button class="icon-btn" onclick="renameFridge('${fridge._id}', '${escapeHtml(fridge.name)}')" title="重命名">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="icon-btn danger" onclick="deleteFridge('${fridge._id}', '${escapeHtml(fridge.name)}', ${fridge.item_count || 0})" title="删除">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    const html = `
        <div class="drawer-overlay" id="manageFridgeDrawer">
            <div class="drawer-content full-height">
                <div class="drawer-header">
                    <h5><i class="fas fa-snowflake"></i> 管理冰箱</h5>
                    <button class="close-btn" onclick="closeDrawer('manageFridgeDrawer')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="drawer-body">
                    <div class="fridge-manage-list">
                        ${fridgeListHtml || '<div class="empty-state">还没有创建冰箱</div>'}
                    </div>
                    <div class="form-actions" style="margin-top: 20px;">
                        <button type="button" class="btn-primary" onclick="closeDrawer('manageFridgeDrawer'); openAddFridgeDrawer();">
                            <i class="fas fa-plus"></i> 添加新冰箱
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', html);
    
    setTimeout(() => {
        document.getElementById('manageFridgeDrawer').classList.add('active');
    }, 10);
}

/**
 * 重命名冰箱
 */
function renameFridge(fridgeId, currentName) {
    // 先移除可能存在的旧抽屉
    const oldDrawer = document.getElementById('renameFridgeDrawer');
    if (oldDrawer) {
        oldDrawer.remove();
    }
    
    const html = `
        <div class="drawer-overlay" id="renameFridgeDrawer">
            <div class="drawer-content">
                <div class="drawer-header">
                    <h5><i class="fas fa-edit"></i> 重命名冰箱</h5>
                    <button class="close-btn" onclick="closeDrawer('renameFridgeDrawer')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="drawer-body">
                    <form id="renameFridgeForm">
                        <input type="hidden" name="fridgeId" value="${fridgeId}">
                        <div class="form-group">
                            <label><i class="fas fa-tag"></i> 冰箱名称</label>
                            <input type="text" name="fridgeName" class="mobile-input" 
                                   value="${escapeHtml(currentName)}"
                                   placeholder="请输入新的冰箱名称" 
                                   maxlength="20" required autocomplete="off">
                            <small class="text-muted">最多20个字符</small>
                        </div>
                        <div class="form-actions">
                            <button type="button" class="btn-secondary" onclick="closeDrawer('renameFridgeDrawer')">取消</button>
                            <button type="submit" class="btn-primary">
                                <i class="fas fa-check"></i> 保存
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', html);
    
    // 绑定表单提交事件
    document.getElementById('renameFridgeForm').addEventListener('submit', handleRenameFridge);
    
    // 显示抽屉
    setTimeout(() => {
        document.getElementById('renameFridgeDrawer').classList.add('active');
        // 聚焦到输入框并选中文本
        const input = document.querySelector('#renameFridgeForm input[name="fridgeName"]');
        input.focus();
        input.select();
    }, 10);
}

/**
 * 处理重命名冰箱
 */
function handleRenameFridge(e) {
    e.preventDefault();
    
    const form = e.target;
    const fridgeId = form.fridgeId.value;
    const newName = form.fridgeName.value.trim();
    
    if (!newName) {
        showToast('请输入冰箱名称', 'error');
        return;
    }
    
    if (newName.length > 20) {
        showToast('冰箱名称不能超过20个字符', 'error');
        return;
    }
    
    fetch(`/fridge/${fridgeId}/rename`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: newName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('重命名成功', 'success');
            closeDrawer('renameFridgeDrawer');
            closeDrawer('manageFridgeDrawer');
            loadUserFridges();
        } else {
            showToast(data.error || '重命名失败', 'error');
        }
    })
    .catch(error => {
        console.error('重命名失败:', error);
        showToast('重命名失败', 'error');
    });
}

/**
 * 删除冰箱
 */
function deleteFridge(fridgeId, name, itemCount) {
    if (itemCount > 0) {
        showToast(`${name}中还有${itemCount}件物品,请先清空`, 'error');
        return;
    }
    
    if (!confirm(`确定要删除"${name}"吗?`)) {
        return;
    }
    
    fetch(`/fridge/${fridgeId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('删除成功', 'success');
            closeDrawer('manageFridgeDrawer');
            
            // 如果删除的是当前冰箱,切换到公共冰箱
            if (currentFridgeId === fridgeId) {
                switchFridge('public');
            }
            
            loadUserFridges();
        } else {
            showToast(data.error || '删除失败', 'error');
        }
    })
    .catch(error => {
        console.error('删除失败:', error);
        showToast('删除失败', 'error');
    });
}

/**
 * 获取当前冰箱ID
 */
function getCurrentFridgeId() {
    return currentFridgeId;
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    // 如果用户已登录,加载冰箱列表
    if (typeof isLoggedIn !== 'undefined' && isLoggedIn) {
        loadUserFridges();
    }
});
