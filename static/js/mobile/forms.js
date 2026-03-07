// 表单处理模块

// 打开添加物品抽屉
function openAddDrawer() {
    // 重置表单
    $('#mAddItemForm')[0].reset();
    $('#mAddItemForm .category-item').removeClass('selected');
    $('#mSelectedTypes').val('');
    
    openDrawer('addItemDrawer');
}

// 日期快捷选择
function setDateShortcut(formType, days) {
    const targetDate = moment().add(days, 'days').format('YYYY-MM-DD');
    const inputId = formType === 'add' ? 'addItemDate' : 'editItemDate';
    const displayId = formType === 'add' ? 'addItemDateDisplay' : 'editItemDateDisplay';
    
    $(`#${inputId}`).val(targetDate);
    $(`#${displayId}`).text(moment(targetDate).format('YYYY年MM月DD日')).addClass('has-value');
}

// 初始化类别选择
function initCategorySelection() {
    // 添加物品表单的类别选择
    $('#mAddItemForm .category-item').click(function() {
        $(this).toggleClass('selected');
        updateSelectedTypes('#mAddItemForm', '#mSelectedTypes');
    });
    
    // 编辑物品表单的类别选择
    $('#editCategoryGrid .category-item').click(function() {
        $(this).toggleClass('selected');
        updateSelectedTypes('#editCategoryGrid', '#mEditSelectedTypes');
    });
}

// 更新选中的类别
function updateSelectedTypes(containerSelector, inputSelector) {
    const selected = [];
    $(`${containerSelector} .category-item.selected`).each(function() {
        selected.push($(this).data('type'));
    });
    $(inputSelector).val(selected.join(','));
}

// 提交添加物品表单
function submitAddItemForm(e) {
    e.preventDefault();
    
    const formData = {
        itemName: $('#mAddItemForm input[name="itemName"]').val(),
        itemDate: $('#mAddItemForm input[name="itemDate"]').val(),
        itemNum: parseInt($('#mAddItemForm input[name="itemNum"]').val()),
        itemPlace: $('#mAddItemForm input[name="itemPlace"]:checked').val(),
        itemType: $('#mSelectedTypes').val()
    };
    
    if (!formData.itemType) {
        showToast('请选择至少一个类别', 'warning');
        return;
    }
    
    $.ajax({
        url: '/item/add',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            if (response.success) {
                showToast('添加成功', 'success');
                closeDrawer('addItemDrawer');
                loadAllItems();
            } else {
                showToast(response.message || '添加失败', 'error');
            }
        },
        error: function() {
            showToast('网络错误，请重试', 'error');
        }
    });
}

// 提交编辑物品表单
function submitEditItemForm(e) {
    e.preventDefault();
    
    const formData = {
        itemId: $('#mEditItemForm input[name="itemId"]').val(),
        itemName: $('#mEditItemForm input[name="itemName"]').val(),
        itemDate: $('#mEditItemForm input[name="itemDate"]').val(),
        itemNum: parseInt($('#mEditItemForm input[name="itemNum"]').val()),
        itemPlace: $('#mEditItemForm input[name="itemPlace"]:checked').val(),
        itemType: $('#mEditSelectedTypes').val()
    };
    
    if (!formData.itemType) {
        showToast('请选择至少一个类别', 'warning');
        return;
    }
    
    $.ajax({
        url: '/item/update',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            if (response.success) {
                showToast('更新成功', 'success');
                closeDrawer('editItemDrawer');
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

// 初始化日期选择器显示
function initDatePickers() {
    // 添加物品日期选择
    $('#addItemDate').on('change', function() {
        const date = $(this).val();
        if (date) {
            $('#addItemDateDisplay').text(moment(date).format('YYYY年MM月DD日')).addClass('has-value');
        }
    });
    
    // 编辑物品日期选择
    $('#editItemDate').on('change', function() {
        const date = $(this).val();
        if (date) {
            $('#editItemDateDisplay').text(moment(date).format('YYYY年MM月DD日')).addClass('has-value');
        }
    });
}
