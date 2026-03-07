// 冰箱管理模块

// 当前选中的冰箱
let currentFridge = 'public';

// 切换冰箱
function switchFridge(fridgeId) {
    console.log('切换到冰箱:', fridgeId);
    currentFridge = fridgeId;
    
    // 更新UI
    $('.fridge-tab').removeClass('active');
    $(`.fridge-tab[data-fridge="${fridgeId}"]`).addClass('active');
    
    // 重新加载物品列表
    loadAllItems();
    
    // 显示提示
    const fridgeNames = {
        'public': '公共冰箱',
        'private-1': '我的冰箱'
    };
    showToast(fridgeNames[fridgeId] || '冰箱', 'info');
}

// 打开添加冰箱抽屉
function openAddFridgeDrawer() {
    showToast('添加冰箱功能开发中...', 'info');
    // TODO: 实现添加冰箱的抽屉界面
}

// 打开管理冰箱抽屉
function openManageFridgeDrawer() {
    showToast('管理冰箱功能开发中...', 'info');
    // TODO: 实现管理冰箱的抽屉界面
}
