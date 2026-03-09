// 家庭管理 JavaScript

let currentFamilyId = null;

// 页面加载时获取家庭列表
$(document).ready(function() {
    // 初始化主题
    if (typeof initializeTheme === 'function') {
        initializeTheme();
    }
    
    loadFamilies();
});

// 加载家庭列表
function loadFamilies() {
    $.ajax({
        url: '/family/list',
        method: 'GET',
        success: function(response) {
            if (response.success) {
                displayFamilies(response.data);
            } else {
                showToast('加载失败: ' + response.message, 'danger');
            }
        },
        error: function() {
            showToast('加载家庭列表失败', 'danger');
        }
    });
}

// 显示家庭列表
function displayFamilies(families) {
    const container = $('#familyList');
    container.empty();

    if (families.length === 0) {
        container.html(`
            <div class="empty-state" style="grid-column: 1/-1;">
                <i class="fas fa-users"></i>
                <p>您还没有加入任何家庭</p>
                <p style="margin-top: 8px; font-size: 14px;">创建一个家庭或加入现有家庭开始使用</p>
            </div>
        `);
        return;
    }

    families.forEach(family => {
        const roleText = family.role === 'creator' ? '创建者' : family.role === 'admin' ? '管理员' : '成员';
        const roleClass = family.role === 'creator' ? 'creator' : family.role === 'admin' ? 'admin' : 'member';
        
        const card = `
            <div class="family-card" onclick="viewFamilyDetail('${family._id}', '${escapeHtml(family.name)}')">
                <div class="family-card-header">
                    <div>
                        <div class="family-name">${escapeHtml(family.name)}</div>
                        <div class="family-code">
                            <i class="fas fa-key"></i>
                            <span>${family.family_code}</span>
                        </div>
                    </div>
                    <span class="role-badge ${roleClass}">${roleText}</span>
                </div>
                <div class="family-info">
                    <div class="family-meta">
                        <i class="fas fa-calendar"></i>
                        加入时间: ${formatDate(family.joined_at)}
                    </div>
                </div>
                <div class="family-actions" onclick="event.stopPropagation()">
                    <button class="card-btn primary" onclick="viewFamilyDetail('${family._id}', '${escapeHtml(family.name)}')">
                        <i class="fas fa-cog"></i>
                        <span>管理</span>
                    </button>
                    ${family.role !== 'creator' ? `
                        <button class="card-btn danger" onclick="leaveFamily('${family._id}')">
                            <i class="fas fa-sign-out-alt"></i>
                            <span>离开</span>
                        </button>
                    ` : `
                        <button class="card-btn danger" onclick="deleteFamily('${family._id}')">
                            <i class="fas fa-trash"></i>
                            <span>删除</span>
                        </button>
                    `}
                </div>
            </div>
        `;
        container.append(card);
    });
}

// 创建家庭
function createFamily() {
    const name = $('#familyName').val().trim();
    
    if (!name) {
        showToast('请输入家庭名称', 'warning');
        return;
    }

    $.ajax({
        url: '/family/create',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ name: name }),
        success: function(response) {
            if (response.success) {
                showToast(`家庭创建成功！家庭编号: ${response.data.family_code}`, 'success');
                $('#createFamilyModal').modal('hide');
                $('#createFamilyForm')[0].reset();
                loadFamilies();
            } else {
                showToast('创建失败: ' + response.message, 'danger');
            }
        },
        error: function() {
            showToast('创建家庭失败', 'danger');
        }
    });
}

// 加入家庭
function joinFamily() {
    const code = $('#familyCode').val().trim().toUpperCase();
    
    if (!code) {
        showToast('请输入家庭编号', 'warning');
        return;
    }

    if (code.length !== 6) {
        showToast('家庭编号应为6位', 'warning');
        return;
    }

    $.ajax({
        url: '/family/join',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ family_code: code }),
        success: function(response) {
            if (response.success) {
                showToast('成功加入家庭！', 'success');
                $('#joinFamilyModal').modal('hide');
                $('#joinFamilyForm')[0].reset();
                loadFamilies();
            } else {
                showToast('加入失败: ' + response.message, 'danger');
            }
        },
        error: function() {
            showToast('加入家庭失败', 'danger');
        }
    });
}

// 查看家庭详情
function viewFamilyDetail(familyId, familyName) {
    currentFamilyId = familyId;
    $('#familyDetailTitle').text(familyName);
    
    // 加载成员列表
    loadFamilyMembers(familyId);
    
    // 重置标签页到成员页
    $('#members-tab').tab('show');
    
    // 显示模态框
    $('#familyDetailModal').modal('show');
}

// 加载家庭成员
function loadFamilyMembers(familyId) {
    $.ajax({
        url: `/family/${familyId}/members`,
        method: 'GET',
        success: function(response) {
            if (response.success) {
                displayMembers(response.data);
            } else {
                $('#membersList').html('<div class="alert alert-danger">加载失败</div>');
            }
        },
        error: function() {
            $('#membersList').html('<div class="alert alert-danger">加载成员列表失败</div>');
        }
    });
}

// 显示成员列表
function displayMembers(members) {
    const container = $('#membersList');
    container.empty();

    if (members.length === 0) {
        container.html('<div class="empty-state"><i class="fas fa-user-slash"></i><p>暂无成员</p></div>');
        return;
    }

    members.forEach(member => {
        const roleText = member.role === 'creator' ? '创建者' : member.role === 'admin' ? '管理员' : '成员';
        const roleClass = member.role === 'creator' ? 'creator' : member.role === 'admin' ? 'admin' : 'member';
        
        const item = `
            <div class="list-group-item member-item">
                <div class="member-info">
                    <h6><i class="fas fa-user"></i> ${escapeHtml(member.username)}</h6>
                    <small>${escapeHtml(member.email)}</small>
                </div>
                <span class="role-badge ${roleClass}">${roleText}</span>
            </div>
        `;
        container.append(item);
    });
}

// 加载家庭共享冰箱
function loadFamilyFridges(familyId) {
    $.ajax({
        url: `/family/${familyId}/fridges`,
        method: 'GET',
        success: function(response) {
            if (response.success) {
                displayFridges(response.data);
            } else {
                $('#fridgesList').html('<div class="alert alert-danger">加载失败</div>');
            }
        },
        error: function() {
            $('#fridgesList').html('<div class="alert alert-danger">加载冰箱列表失败</div>');
        }
    });
}

// 显示冰箱列表
function displayFridges(fridges) {
    const container = $('#fridgesList');
    container.empty();

    if (fridges.length === 0) {
        container.html(`
            <div class="empty-state">
                <i class="fas fa-snowflake"></i>
                <p>暂无共享冰箱</p>
                <p style="margin-top: 8px; font-size: 14px; color: var(--text-secondary);">
                    在主页的"管理冰箱"中,点击冰箱的权限设置按钮(盾牌图标),<br>
                    开启"家庭共享"即可让家庭成员看到您的冰箱
                </p>
            </div>
        `);
        return;
    }

    fridges.forEach(fridge => {
        const editable = fridge.permission.is_editable_by_family;
        const item = `
            <div class="list-group-item fridge-item">
                <div class="fridge-info">
                    <h6><i class="fas fa-snowflake"></i> ${escapeHtml(fridge.name)}</h6>
                    <small>所有者: ${escapeHtml(fridge.owner_username)}</small>
                </div>
                <span class="badge ${editable ? 'bg-success' : 'bg-info'}">
                    <i class="fas fa-${editable ? 'edit' : 'eye'}"></i>
                    ${editable ? '可编辑' : '只读'}
                </span>
            </div>
        `;
        container.append(item);
    });
}

// 离开家庭
function leaveFamily(familyId) {
    if (!confirm('确定要离开这个家庭吗？')) {
        return;
    }

    $.ajax({
        url: `/family/leave/${familyId}`,
        method: 'POST',
        success: function(response) {
            if (response.success) {
                showToast('已离开家庭', 'success');
                loadFamilies();
            } else {
                showToast('操作失败: ' + response.message, 'danger');
            }
        },
        error: function() {
            showToast('离开家庭失败', 'danger');
        }
    });
}

// 删除家庭
function deleteFamily(familyId) {
    if (!confirm('确定要删除这个家庭吗？此操作不可恢复！')) {
        return;
    }

    $.ajax({
        url: `/family/${familyId}`,
        method: 'DELETE',
        success: function(response) {
            if (response.success) {
                showToast('家庭已删除', 'success');
                loadFamilies();
            } else {
                showToast('删除失败: ' + response.message, 'danger');
            }
        },
        error: function() {
            showToast('删除家庭失败', 'danger');
        }
    });
}

// 格式化日期
function formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// 转义HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

