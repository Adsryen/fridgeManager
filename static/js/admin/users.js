// 管理后台移动端 - 用户管理页面逻辑

let touchStartX = 0;
let touchStartY = 0;
let currentSwipeCard = null;

document.addEventListener('DOMContentLoaded', function() {
    initUsers();
    initSwipeGesture();
});

function initUsers() {
    // 搜索功能
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
        
        // 搜索框聚焦时滚动到顶部
        searchInput.addEventListener('focus', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
}

function initSwipeGesture() {
    const userCards = document.querySelectorAll('.user-card');
    
    userCards.forEach(card => {
        let startX = 0;
        let currentX = 0;
        let isDragging = false;
        
        card.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            isDragging = true;
            card.style.transition = 'none';
        });
        
        card.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            
            currentX = e.touches[0].clientX;
            const diff = startX - currentX;
            
            // 只允许向左滑动
            if (diff > 0 && diff < 100) {
                card.style.transform = `translateX(-${diff}px)`;
            }
        });
        
        card.addEventListener('touchend', () => {
            if (!isDragging) return;
            
            const diff = startX - currentX;
            card.style.transition = 'transform 0.3s';
            
            if (diff > 50) {
                // 显示删除按钮
                card.classList.add('swipe-left');
                if (currentSwipeCard && currentSwipeCard !== card) {
                    currentSwipeCard.classList.remove('swipe-left');
                }
                currentSwipeCard = card;
            } else {
                // 恢复原位
                card.style.transform = '';
                card.classList.remove('swipe-left');
            }
            
            isDragging = false;
        });
    });
    
    // 点击其他地方关闭滑动
    document.addEventListener('click', (e) => {
        if (currentSwipeCard && !e.target.closest('.user-card')) {
            currentSwipeCard.classList.remove('swipe-left');
            currentSwipeCard = null;
        }
    });
}

function handleSearch(e) {
    const keyword = e.target.value.toLowerCase().trim();
    const userCards = document.querySelectorAll('.user-card');
    let visibleCount = 0;
    
    userCards.forEach(card => {
        const username = card.dataset.username?.toLowerCase() || '';
        const email = card.dataset.email?.toLowerCase() || '';
        
        if (username.includes(keyword) || email.includes(keyword)) {
            card.style.display = 'block';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    // 显示搜索结果提示
    const existingTip = document.querySelector('.search-result-tip');
    if (existingTip) {
        existingTip.remove();
    }
    
    if (keyword && visibleCount === 0) {
        const tip = document.createElement('div');
        tip.className = 'empty-state search-result-tip';
        tip.innerHTML = `
            <i class="fas fa-search"></i>
            <p>未找到匹配的用户</p>
            <p style="font-size: var(--font-size-small); color: var(--text-secondary);">
                搜索关键词: "${keyword}"
            </p>
        `;
        document.querySelector('.admin-content').appendChild(tip);
    }
}

function viewUser(userId) {
    // 添加点击动画
    event.target.closest('.btn').style.transform = 'scale(0.95)';
    setTimeout(() => {
        window.location.href = `/admin/user/${userId}`;
    }, 100);
}

async function toggleStatus(userId) {
    showConfirm('确认操作', '确定要切换用户状态吗?', async () => {
        showLoading(true);
        
        try {
            const result = await apiRequest(`/admin/user/${userId}/toggle-status`, 'POST');
            showAlert(result.message || '状态已更新', 'success');
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            showAlert('操作失败: ' + error.message, 'danger');
        } finally {
            showLoading(false);
        }
    });
}

async function toggleAdmin(userId) {
    showConfirm('确认操作', '确定要切换管理员权限吗?', async () => {
        showLoading(true);
        
        try {
            const result = await apiRequest(`/admin/user/${userId}/toggle-admin`, 'POST');
            showAlert(result.message || '权限已更新', 'success');
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            showAlert('操作失败: ' + error.message, 'danger');
        } finally {
            showLoading(false);
        }
    });
}

async function deleteUser(userId, username) {
    showConfirm(
        '危险操作',
        `确定要删除用户 "${username}" 吗?\n\n此操作将删除该用户的所有数据,且无法恢复!`,
        async () => {
            showLoading(true);
            
            try {
                const result = await apiRequest(`/admin/user/${userId}/delete`, 'POST');
                showAlert(result.message || '用户已删除', 'success');
                setTimeout(() => location.reload(), 1000);
            } catch (error) {
                showAlert('删除失败: ' + error.message, 'danger');
            } finally {
                showLoading(false);
            }
        }
    );
}

async function resetPassword(userId, username) {
    // 创建密码输入对话框
    const overlay = document.createElement('div');
    overlay.className = 'confirm-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.2s ease-out;
    `;
    
    const dialog = document.createElement('div');
    dialog.className = 'confirm-dialog';
    dialog.style.cssText = `
        background: white;
        border-radius: 12px;
        padding: 24px;
        margin: 0 20px;
        max-width: 400px;
        width: 100%;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        animation: scaleIn 0.2s ease-out;
    `;
    
    dialog.innerHTML = `
        <div style="font-size: 18px; font-weight: 600; margin-bottom: 12px; color: var(--text-primary);">
            <i class="fas fa-key"></i> 重置密码
        </div>
        <div style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">
            为用户 <strong>${username}</strong> 设置新密码
        </div>
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-size: 14px; color: var(--text-primary);">
                新密码 (至少6位)
            </label>
            <input type="password" id="newPassword" class="form-control" 
                   placeholder="请输入新密码" style="width: 100%;" minlength="6">
            <div style="margin-top: 8px;">
                <label style="display: flex; align-items: center; font-size: 14px; cursor: pointer;">
                    <input type="checkbox" id="showPassword" style="margin-right: 8px;">
                    显示密码
                </label>
            </div>
        </div>
        <div style="display: flex; gap: 12px;">
            <button class="btn btn-secondary" style="flex: 1;" id="cancelBtn">
                取消
            </button>
            <button class="btn btn-primary" style="flex: 1;" id="confirmResetBtn">
                <i class="fas fa-check"></i> 确定重置
            </button>
        </div>
    `;
    
    overlay.appendChild(dialog);
    document.body.appendChild(overlay);
    
    const passwordInput = document.getElementById('newPassword');
    const showPasswordCheckbox = document.getElementById('showPassword');
    const cancelBtn = document.getElementById('cancelBtn');
    const confirmBtn = document.getElementById('confirmResetBtn');
    
    // 显示/隐藏密码
    showPasswordCheckbox.addEventListener('change', () => {
        passwordInput.type = showPasswordCheckbox.checked ? 'text' : 'password';
    });
    
    // 取消按钮
    cancelBtn.addEventListener('click', () => {
        overlay.remove();
    });
    
    // 确定按钮
    confirmBtn.addEventListener('click', async () => {
        const newPassword = passwordInput.value.trim();
        
        if (!newPassword) {
            showAlert('请输入新密码', 'warning');
            return;
        }
        
        if (newPassword.length < 6) {
            showAlert('密码长度至少6位', 'warning');
            return;
        }
        
        overlay.remove();
        showLoading(true);
        
        try {
            const result = await apiRequest(`/admin/user/${userId}/reset-password`, 'POST', {
                password: newPassword
            });
            showAlert(result.message || '密码已重置', 'success');
        } catch (error) {
            showAlert('重置失败: ' + error.message, 'danger');
        } finally {
            showLoading(false);
        }
    });
    
    // 点击遮罩层关闭
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            overlay.remove();
        }
    });
    
    // 自动聚焦到输入框
    setTimeout(() => passwordInput.focus(), 100);
}
