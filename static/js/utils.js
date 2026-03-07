// 工具函数模块

// 获取类别对应的emoji
function getTypeEmoji(type) {
    const emojiMap = {
        'vegetable': '🥬',
        'fruit': '🍎',
        'meat': '🥩',
        'seafood': '🐟',
        'diary': '🥛',
        'beverage': '🥤',
        'egg': '🥚',
        'bread': '🍞',
        'frozen': '🍦',
        'sauce': '🍯',
        'snack': '🍿',
        'other': '📦'
    };
    return emojiMap[type] || '📦';
}

// 获取类别文本
function getTypeText(type) {
    const typeMap = {
        'vegetable': '蔬菜',
        'fruit': '水果',
        'meat': '肉类',
        'seafood': '海鲜',
        'diary': '乳制品',
        'beverage': '饮料',
        'egg': '蛋豆类',
        'bread': '面包',
        'frozen': '冷冻食品',
        'sauce': '酱料',
        'snack': '零食',
        'other': '其他'
    };
    return typeMap[type] || '其他';
}

// 获取位置文本
function getPlaceText(place) {
    const placeMap = {
        'cold': '冷藏室',
        'frozer': '冷冻室',
        'room': '室温区'
    };
    return placeMap[place] || '未知';
}

// 计算过期状态
function getExpiryStatus(expireDate) {
    const now = moment();
    const expire = moment(expireDate);
    const daysUntilExpire = expire.diff(now, 'days');
    
    let statusClass = '';
    let statusBadgeClass = '';
    let statusText = '';
    
    if (daysUntilExpire < 0) {
        statusClass = 'expired';
        statusBadgeClass = 'danger';
        statusText = `已过期 ${Math.abs(daysUntilExpire)} 天`;
    } else if (daysUntilExpire === 0) {
        statusClass = 'expiring-soon';
        statusBadgeClass = 'warning';
        statusText = '今天过期';
    } else if (daysUntilExpire <= 3) {
        statusClass = 'expiring-soon';
        statusBadgeClass = 'warning';
        statusText = `还剩 ${daysUntilExpire} 天`;
    } else {
        statusClass = '';
        statusBadgeClass = 'fresh';
        statusText = `还剩 ${daysUntilExpire} 天`;
    }
    
    return { statusClass, statusBadgeClass, statusText, daysUntilExpire };
}

// HTML转义函数,防止XSS攻击
function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.toString().replace(/[&<>"']/g, function(m) { return map[m]; });
}
