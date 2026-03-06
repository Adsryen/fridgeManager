
$(document).ready(function () {
    deleteItem();
    editItem();
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget); // Button that triggered the modal
        const taskID = button.data('source'); // Extract info from data-* attributes
        const content = button.data('content'); // Extract info from data-* attributes

        const modal = $(this);
        if (taskID === 'New Task') {
            modal.find('.modal-title').text(taskID);
            $('#task-form-display').removeAttr('taskID');
        } else {
            modal.find('.modal-title').text('Edit Task ' + taskID);
            $('#task-form-display').attr('taskID', taskID);
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })


    $('.state-ok').click(function () {
        var timeInMs = Date.now();
        var html = '';
        $(`.table-responsive`).show();
        $.ajax({
            type: 'POST',
            url: '/item/stateok/' + timeInMs,
            success: function (res) {
                console.log(res);
                $.each(res, function(idx, v){
                    ms = Date.parse(v['ExpireDate']);
                    date = moment(ms).format('YYYY-MM-DD');
                    html += `<tr class="${v['_id']}">
                    <td>${v['Name']}</td>
                    <td class="placeTD">
                        <span class="badge  click">${convertType(v['Place'])}</span>
                    </td>
                    <td>${date}</td>
                    <td>${v['Num']}</td>
                    <td class="typeTD">
                        <span class="badge  click">${convertType(v['Type'])}</span>
                    </td>            
                    <td>
                        <button type="button" class="btn btn-outline-info btn-sm state" data-bs-toggle="modal"
                        data-bs-target="#edit-modal" data-source="${v['_id']}"
                        data-content="${v['Name']}"><i class="fa fa-pen fa-1" aria-hidden="true"></i>
                        </button>
                    </td>

                    <td>
                        <button class="btn btn-outline-secondary btn-sm remove" data-source="${v['_id']}"
                        type="button"><i class="fa fa-trash fa-1" aria-hidden="true"></i>
                        </button>
                    </td>
                </tr>`;
                });
                
                $(`.table-responsive tbody`).html(html);
                deleteItem();
                editItem();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.state-bad').click(function () {
        var timeInMs = Date.now();
        var html = '';
        $(`.table-responsive`).show();
        $.ajax({
            type: 'POST',
            url: '/item/statebad/' + timeInMs,
            success: function (res) {
                console.log(res);
                $.each(res, function(idx, v){
                    ms = Date.parse(v['ExpireDate']);
                    date = moment(ms).format('YYYY-MM-DD');
                    html += `<tr class="${v['_id']}">
                    <td>${v['Name']}</td>
                    <td class="placeTD">
                        <span class="badge  click">${convertType(v['Place'])}</span>
                    </td>
                    <td>${date}</td>
                    <td>${v['Num']}</td>
                    <td class="typeTD">
                        <span class="badge  click">${convertType(v['Type'])}</span>
                    </td>            
                    <td>
                        <button type="button" class="btn btn-outline-info btn-sm state" data-bs-toggle="modal"
                        data-bs-target="#edit-modal" data-source="${v['_id']}"
                        data-content="${v['Name']}"><i class="fa fa-pen fa-1" aria-hidden="true"></i>
                        </button>
                    </td>

                    <td>
                        <button class="btn btn-outline-secondary btn-sm remove" data-source="${v['_id']}"
                        type="button"><i class="fa fa-trash fa-1" aria-hidden="true"></i>
                        </button>
                    </td>
                </tr>`;
                });
                
                $(`.table-responsive tbody`).html(html);
                deleteItem();
                editItem();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.all-btn').click(function () {
        var html = '';
        $(`.table-responsive`).show();
        $.ajax({
            type: 'POST',
            url: '/item/total',
            success: function (res) {
                console.log(res);
                $.each(res, function(idx, v){
                    ms = Date.parse(v['ExpireDate']);
                    date = moment(ms).format('YYYY-MM-DD');
                    html += `<tr class="${v['_id']}">
                    <td>${v['Name']}</td>
                    <td class="placeTD">
                        <span class="badge  click">${convertType(v['Place'])}</span>
                    </td>
                    <td>${date}</td>
                    <td>${v['Num']}</td>
                    <td class="typeTD">
                        <span class="badge click">${convertType(v['Type'])}</span>
                    </td>            
                    <td>
                        <button type="button" class="btn btn-outline-info btn-sm state" data-bs-toggle="modal"
                        data-bs-target="#edit-modal" data-source="${v['_id']}"
                        data-content="${v['Name']}"><i class="fa fa-pen fa-1" aria-hidden="true"></i>
                        </button>
                    </td>

                    <td>
                        <button class="btn btn-outline-secondary btn-sm remove ${v['_id']}" data-source="${v['_id']}"
                        type="button"><i class="fa fa-trash fa-1" aria-hidden="true"></i>
                        </button>
                    </td>
                </tr>`;
                });
                
                $(`.table-responsive tbody`).html(html);
                deleteItem();
                editItem();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.cold-btn').click(function () {
        var html = '';
        $(`.table-responsive`).show();
        $.ajax({
            type: 'POST',
            url: '/item/cold',
            success: function (res) {
                console.log(res);
                $.each(res, function(idx, v){
                    ms = Date.parse(v['ExpireDate']);
                    date = moment(ms).format('YYYY-MM-DD');
                    html += `<tr class="${v['_id']}">
                    <td>${v['Name']}</td>
                    <td class="placeTD">
                        <span class="badge  click">${convertType(v['Place'])}</span>
                    </td>
                    <td>${date}</td>
                    <td>${v['Num']}</td>
                    <td class="typeTD">
                        <span class="badge click">${convertType(v['Type'])}</span>
                    </td>            
                    <td>
                        <button type="button" class="btn btn-outline-info btn-sm state" data-bs-toggle="modal"
                        data-bs-target="#edit-modal" data-source="${v['_id']}"
                        data-content="${v['Name']}"><i class="fa fa-pen fa-1" aria-hidden="true"></i>
                        </button>
                    </td>

                    <td>
                        <button class="btn btn-outline-secondary btn-sm remove ${v['_id']}" data-source="${v['_id']}"
                        type="button"><i class="fa fa-trash fa-1" aria-hidden="true"></i>
                        </button>
                    </td>
                </tr>`;
                });
                
                $(`.table-responsive tbody`).html(html);
                deleteItem();
                editItem();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.fro-btn').click(function () {
        var html = '';
        $(`.table-responsive`).show();
        $.ajax({
            type: 'POST',
            url: '/item/frozer',
            success: function (res) {
                console.log(res);
                $.each(res, function(idx, v){
                    ms = Date.parse(v['ExpireDate']);
                    date = moment(ms).format('YYYY-MM-DD');
                    html += `<tr class="${v['_id']}">
                    <td>${v['Name']}</td>
                    <td class="placeTD">
                        <span class="badge  click">${convertType(v['Place'])}</span>
                    </td>
                    <td>${date}</td>
                    <td>${v['Num']}</td>
                    <td class="typeTD">
                        <span class="badge click">${convertType(v['Type'])}</span>
                    </td>            
                    <td>
                        <button type="button" class="btn btn-outline-info btn-sm state" data-bs-toggle="modal"
                        data-bs-target="#edit-modal" data-source="${v['_id']}"
                        data-content="${v['Name']}"><i class="fa fa-pen fa-1" aria-hidden="true"></i>
                        </button>
                    </td>

                    <td>
                        <button class="btn btn-outline-secondary btn-sm remove ${v['_id']}" data-source="${v['_id']}"
                        type="button"><i class="fa fa-trash fa-1" aria-hidden="true"></i>
                        </button>
                    </td>
                </tr>`;
                });
                
                $(`.table-responsive tbody`).html(html);
                deleteItem();
                editItem();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.search-ipt').on('input', function (e) {
        var html = '';
        $(`.table-responsive`).show();
        $.ajax({
            type: 'POST',
            url: '/item/search',
            data: {text: $('.search-ipt').val()},
            success: function (res) {
                console.log(res);
                $.each(res, function(idx, v){
                    ms = Date.parse(v['ExpireDate']);
                    date = moment(ms).format('YYYY-MM-DD');
                    html += `<tr class="${v['_id']}">
                    <td>${v['Name']}</td>
                    <td class="placeTD">
                        <span class="badge  click">${convertType(v['Place'])}</span>
                    </td>
                    <td>${date}</td>
                    <td>${v['Num']}</td>
                    <td class="typeTD">
                        <span class="badge click">${convertType(v['Type'])}</span>
                    </td>            
                    <td>
                        <button type="button" class="btn btn-outline-info btn-sm state" data-bs-toggle="modal"
                        data-bs-target="#edit-modal" data-source="${v['_id']}"
                        data-content="${v['Name']}"><i class="fa fa-pen fa-1" aria-hidden="true"></i>
                        </button>
                    </td>

                    <td>
                        <button class="btn btn-outline-secondary btn-sm remove ${v['_id']}" data-source="${v['_id']}"
                        type="button"><i class="fa fa-trash fa-1" aria-hidden="true"></i>
                        </button>
                    </td>
                </tr>`;
                });
                
                $(`.table-responsive tbody`).html(html);
                deleteItem();
                editItem();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    tagSearch('veg-btn');
    tagSearch('fru-btn');
    tagSearch('sea-btn');
    tagSearch('drink-btn');
    tagSearch('meat-btn');
    tagSearch('diary-btn');
    tagSearch('egg-btn');
    tagSearch('bread-btn');
    tagSearch('snack-btn');
    tagSearch('froze-btn');
    tagSearch('sauce-btn');
    tagSearch('other-btn');
});

function deleteItem() {
    $('.remove').click(function () {
        const remove = $(this);
        const id = remove.data('source');
        if($(`tbody tr`).hasClass(id)) {
            $(`tbody`).find(id).remove();
            location.reload();
        }

        $.ajax({
            type: 'POST',
            url: '/item/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
}

function editItem() {
    $('.state').click(function () {
        const state = $(this);
        const tID = state.data('source');
        $.ajax({
            method: 'POST',
            url: '/item/getone/'+ tID,
            success: function (res) {
                $.each(res, function(idx, val) {
                    ms = Date.parse(val['ExpireDate']);
                    date = new Date(ms);
                    var year = date.getFullYear();
                    var month = ("0" + (date.getMonth() + 1)).slice(-2);
                    var day = ("0" + date.getDate()).slice(-2);
                    t = val['Type'];
                    pl = val['Place'];
                    d = (`${year}-${month}-${day}`);
                    // console.log(moment(ms).format('MMM DD, YYYY'));
                    // console.log(typeof moment(ms).format('MMM DD, YYYY'));
                    $(`.edit-form .itemName`).attr('value', val['Name']);
                    $(`.edit-form .itemDate`).attr('value', d);
                    $(`.edit-form .itemNum`).attr('value', val['Num']);
                    $(".edit-form input[name=itemPlace][value=" + pl + "]").prop('checked', true);
                    $(".edit-form input[name=itemType][value=" + t + "]").prop('checked', true);
                    // $(`.edit-form input[value=${type}]`).attr('checked', true);
                    // var $radios = $('input:radio[name=itemType]');
                    // if($radios.is(':checked') === false) {
                    //     $radios.filter('[value="frozen"').prop('checked', true);
                    // }
                    // $(`.edit-form input[name="itemType"][value=frozen]`).attr('checked', true);
                });
            },
            error: function () {
                console.log('Error');
            }
        });
        $(`.edit-form`).attr('action', '/item/edit/'+tID)
    });
}

function tagSearch(s) {
    $(`.badge-container`).find('.'+s).click(function () {
        tagName = $(this).data('source');
        var html = '';
        $(`.table-responsive`).show();
        $.ajax({
            type: 'POST',
            url: '/item/tag/' + tagName,
            success: function (res) {
                console.log(res);
                $.each(res, function(idx, v){
                    ms = Date.parse(v['ExpireDate']);
                    date = moment(ms).format('YYYY-MM-DD');
                    html += `<tr class="${v['_id']}">
                    <td>${v['Name']}</td>
                    <td class="placeTD">
                        <span class="badge  click">${convertType(v['Place'])}</span>
                    </td>
                    <td>${date}</td>
                    <td>${v['Num']}</td>
                    <td class="typeTD">
                        <span class="badge click ">${convertType(v['Type'])}</span>
                    </td>            
                    <td>
                        <button type="button" class="btn btn-outline-info btn-sm state" data-bs-toggle="modal"
                        data-bs-target="#edit-modal" data-source="${v['_id']}"
                        data-content="${v['Name']}"><i class="fa fa-pen fa-1" aria-hidden="true"></i>
                        </button>
                    </td>

                    <td>
                        <button class="btn btn-outline-secondary btn-sm remove" data-source="${v['_id']}"
                        type="button"><i class="fa fa-trash fa-1" aria-hidden="true"></i>
                        </button>
                    </td>
                </tr>`;
                });
                
                $(`.table-responsive tbody`).html(html);
                deleteItem();
                editItem();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
}

function convertType(s) {
    if(s == 'vegetable') {return `<i class="fa-solid fa-carrot"></i> 蔬菜`;}
    if(s == 'fruit') {return `<i class="fa-solid fa-apple-whole"></i> 水果`;}
    if(s == 'seafood') {return `<i class="fa-solid fa-fish-fins"></i> 海鮮`;}
    if(s == 'meat') {return `<i class="fa-solid fa-bacon"></i> 肉類`;}
    if(s == 'beverage') {return `<i class="fa-solid fa-wine-glass"></i> 飲料`;}
    if(s == 'diary') {return `<i class="fa-solid fa-cow"></i> 乳製品`;}
    if(s == 'egg') {return `<i class="fa-solid fa-egg"></i> 蛋豆類`;}
    if(s == 'bread') {return `<i class="fa-solid fa-bread-slice"></i> 麵包`;}
    if(s == 'frozen') {return `<i class="fa-solid fa-ice-cream"></i> 冷凍食品`;}
    if(s == 'sauce') {return `<i class="fa-solid fa-bottle-water"></i> 醬料`;}
    if(s == 'other') {return `<i class="fa-solid fa-circle-info"></i> 其他`;}
    if(s == 'snack') {return `<i class="fa-solid fa-ice-cream"></i> 零食`;}
    if(s == 'cold') {return '冷藏';}
    if(s == 'frozer') {return '冷凍';}
    if(s == 'room') {return '室溫';}
}

