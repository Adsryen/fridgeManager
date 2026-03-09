// 表单处理模块

// 打开添加方式选择抽屉
function openAddDrawer() {
    openDrawer('addMethodDrawer');
}

// 处理添加方式选择
function handleAddMethod(method) {
    const isLoggedIn = document.body.dataset.loggedIn === 'true';
    
    if (method === 'ocr') {
        if (!isLoggedIn) {
            showToast('请先登录后使用文字识别功能', 'warning', 2000);
            setTimeout(() => {
                window.location.href = '/auth/login';
            }, 2200);  // Toast显示2秒后跳转
            return;
        }
        closeDrawer('addMethodDrawer');
        openOCRDrawer();
    } else if (method === 'manual') {
        closeDrawer('addMethodDrawer');
        openManualAddDrawer();
    } else if (method === 'ai') {
        if (!isLoggedIn) {
            showToast('请先登录后使用AI对话功能', 'warning', 2000);
            setTimeout(() => {
                window.location.href = '/auth/login';
            }, 2200);  // Toast显示2秒后跳转
            return;
        }
        closeDrawer('addMethodDrawer');
        openAIChatDrawer();
    }
}

// 打开手动添加物品抽屉
function openManualAddDrawer() {
    // 重置表单
    $('#mAddItemForm')[0].reset();
    $('#mAddItemForm .category-item').removeClass('selected');
    $('#mSelectedTypes').val('');
    
    openDrawer('addItemDrawer');
}

// 打开OCR识别抽屉
function openOCRDrawer() {
    // 先移除可能存在的旧抽屉
    const oldDrawer = document.getElementById('ocrDrawer');
    if (oldDrawer) {
        oldDrawer.remove();
    }
    
    const html = `
        <div class="drawer-overlay" id="ocrDrawer">
            <div class="drawer-content full-height">
                <div class="drawer-header">
                    <h5><i class="fas fa-camera"></i> 文字识别录入</h5>
                    <button class="close-btn" onclick="closeDrawer('ocrDrawer')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="drawer-body" style="padding: 24px;">
                    <div style="text-align: center;">
                        <div class="ocr-upload-area" id="ocrUploadArea">
                            <input type="file" id="ocrImageInput" accept="image/*" capture="environment" style="display: none;">
                            <div class="ocr-upload-icon">
                                <i class="fas fa-camera" style="font-size: 48px; color: var(--primary-color);"></i>
                            </div>
                            <div style="margin-top: 16px; font-size: 16px; font-weight: 600; color: var(--text-primary);">
                                点击拍照或上传图片
                            </div>
                            <div style="margin-top: 8px; font-size: 13px; color: var(--text-secondary);">
                                支持JPG、PNG格式
                            </div>
                        </div>
                        <div id="ocrPreview" style="display: none; margin-top: 20px;">
                            <img id="ocrPreviewImage" style="max-width: 100%; border-radius: 12px; margin-bottom: 16px;">
                            <div style="display: flex; gap: 12px;">
                                <button class="btn-primary" onclick="processOCR(false)" style="flex: 1;">
                                    <i class="fas fa-magic"></i> OCR识别
                                </button>
                                <button class="btn-secondary" onclick="processOCR(true)" style="flex: 1;">
                                    <i class="fas fa-eye"></i> 视觉模型
                                </button>
                            </div>
                            <div style="margin-top: 8px; font-size: 11px; color: var(--text-secondary);">
                                OCR识别：快速、免费 | 视觉模型：智能、需消耗token
                            </div>
                        </div>
                        <div id="ocrResult" style="display: none; margin-top: 20px; text-align: left;">
                            <div id="ocrResultText" style="margin-bottom: 16px;"></div>
                            <div style="display: flex; gap: 12px;">
                                <button class="btn-secondary" onclick="document.getElementById('ocrResult').style.display='none'; document.getElementById('ocrPreview').style.display='block';" style="flex: 1;">
                                    <i class="fas fa-redo"></i> 重新识别
                                </button>
                                <button class="btn-primary" onclick="confirmOCRResult()" style="flex: 1;">
                                    <i class="fas fa-check"></i> 确认添加
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', html);
    
    // 绑定上传区域点击事件
    document.getElementById('ocrUploadArea').addEventListener('click', function() {
        document.getElementById('ocrImageInput').click();
    });
    
    // 绑定文件选择事件
    document.getElementById('ocrImageInput').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                document.getElementById('ocrPreviewImage').src = event.target.result;
                document.getElementById('ocrUploadArea').style.display = 'none';
                document.getElementById('ocrPreview').style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });
    
    setTimeout(() => {
        document.getElementById('ocrDrawer').classList.add('active');
    }, 10);
}

// 处理OCR识别
async function processOCR(useVision = false) {
    showToast(useVision ? '正在使用视觉模型识别...' : '正在识别中...', 'info');
    
    const fileInput = document.getElementById('ocrImageInput');
    const file = fileInput.files[0];
    
    if (!file) {
        showToast('请先选择图片', 'error');
        return;
    }
    
    try {
        // 将图片转换为base64
        const base64 = await fileToBase64(file);
        
        // 发送识别请求
        const response = await fetch('/item/ocr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: base64,
                use_vision: useVision
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('ocrPreview').style.display = 'none';
            document.getElementById('ocrResult').style.display = 'block';
            
            // 显示识别方法
            const methodText = result.method === 'vision' ? '视觉模型' : 
                              result.method === 'ocr_ai' ? 'OCR + AI解析' : 'OCR识别';
            
            let resultHtml = `<div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">
                识别方式：${methodText}
            </div>`;
            
            // 显示识别的文字（如果有）
            if (result.text) {
                resultHtml += `<div style="padding: 12px; background: var(--bg-secondary); border-radius: 8px; margin-bottom: 12px;">
                    <div style="font-weight: 600; margin-bottom: 4px; font-size: 13px;">识别文字：</div>
                    <div style="color: var(--text-secondary); line-height: 1.6; font-size: 12px; white-space: pre-wrap;">${result.text}</div>
                </div>`;
            }
            
            // 显示解析的物品
            if (result.items && result.items.length > 0) {
                resultHtml += `<div style="font-weight: 600; margin-bottom: 8px; font-size: 13px;">识别到 ${result.items.length} 个物品：</div>`;
                result.items.forEach((item, index) => {
                    resultHtml += `
                        <div style="padding: 12px; background: var(--bg-secondary); border-radius: 8px; margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <div style="font-weight: 600; font-size: 14px;">${item.name}</div>
                                    <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
                                        数量：${item.quantity} ${item.unit || '个'} | 过期：${item.expire_date || '未知'}
                                    </div>
                                </div>
                                <button class="btn-icon" onclick="editOCRItem(${index})" style="padding: 8px;">
                                    <i class="fas fa-edit"></i>
                                </button>
                            </div>
                        </div>
                    `;
                });
                
                // 保存识别结果
                window.ocrRecognizedItems = result.items;
            } else {
                resultHtml += `<div style="text-align: center; padding: 20px; color: var(--text-secondary);">
                    <i class="fas fa-info-circle"></i> 未识别到物品信息
                </div>`;
            }
            
            document.getElementById('ocrResultText').innerHTML = resultHtml;
            
            showToast('识别完成！', 'success');
        } else {
            showToast(result.error || '识别失败', 'error');
        }
    } catch (error) {
        console.error('OCR识别错误:', error);
        showToast('识别失败，请重试', 'error');
    }
}

// 文件转base64
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// 编辑OCR识别的物品
function editOCRItem(index) {
    const item = window.ocrRecognizedItems[index];
    if (!item) return;
    
    // 关闭OCR抽屉
    closeDrawer('ocrDrawer');
    
    // 打开手动添加抽屉并填充数据
    openManualAddDrawer();
    
    // 填充表单
    setTimeout(() => {
        document.getElementById('mItemName').value = item.name;
        document.getElementById('mItemNum').value = item.quantity || 1;
        if (item.expire_date) {
            document.getElementById('mItemDate').value = item.expire_date;
        }
    }, 300);
}

// 确认OCR结果
async function confirmOCRResult() {
    const items = window.ocrRecognizedItems;
    
    if (!items || items.length === 0) {
        showToast('没有可添加的物品', 'warning');
        return;
    }
    
    showToast('正在添加物品...', 'info');
    
    try {
        // 使用批量添加接口
        const response = await fetch('/item/batch-insert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                items: items
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            let message = `成功添加 ${result.added} 个物品`;
            
            if (result.failed > 0) {
                message += `，${result.failed} 个失败`;
            }
            
            if (result.validation_errors && result.validation_errors.length > 0) {
                message += `\n数据校验警告：${result.validation_errors.length} 个`;
                console.warn('数据校验警告:', result.validation_errors);
            }
            
            showToast(message, result.failed > 0 ? 'warning' : 'success');
            closeDrawer('ocrDrawer');
            
            // 刷新页面
            setTimeout(() => location.reload(), 1000);
        } else {
            let errorMsg = result.error || '添加失败';
            
            if (result.details && result.details.length > 0) {
                errorMsg += '\n详情：' + result.details.join('; ');
            }
            
            showToast(errorMsg, 'error');
        }
    } catch (error) {
        console.error('添加物品错误:', error);
        showToast('添加失败，请重试', 'error');
    }
}

// 打开AI对话抽屉
function openAIChatDrawer() {
    // 先移除可能存在的旧抽屉
    const oldDrawer = document.getElementById('aiChatDrawer');
    if (oldDrawer) {
        oldDrawer.remove();
    }
    
    const html = `
        <div class="drawer-overlay" id="aiChatDrawer">
            <div class="drawer-content full-height">
                <div class="drawer-header">
                    <h5><i class="fas fa-comments"></i> AI对话</h5>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <button class="btn-secondary" onclick="resetAIChat()" style="padding: 8px 12px; font-size: 12px;">
                            <i class="fas fa-plus"></i> 新会话
                        </button>
                        <button class="close-btn" onclick="closeDrawer('aiChatDrawer')">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                <div class="drawer-body" style="padding: 0; display: flex; flex-direction: column; height: 100%;">
                    <div id="aiChatMessages" style="flex: 1; overflow-y: auto; padding: 20px; background: var(--bg-secondary);">
                        <div class="ai-message" style="display: flex; gap: 12px; margin-bottom: 16px;">
                            <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--primary-color); display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0;">
                                <i class="fas fa-robot"></i>
                            </div>
                            <div style="background: white; padding: 12px 16px; border-radius: 12px; max-width: 80%; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                                你好！我可以帮你添加物品到冰箱。请告诉我物品的名称、数量和过期时间。
                            </div>
                        </div>
                    </div>
                    <div id="aiChatConfirm" style="display: none; padding: 16px; background: var(--bg-primary); border-top: 1px solid var(--divider-color);">
                        <div style="margin-bottom: 12px; font-weight: 600; font-size: 14px;">
                            <i class="fas fa-check-circle" style="color: var(--success-color);"></i> 信息已收集完整
                        </div>
                        <div id="aiChatItemsPreview" style="margin-bottom: 12px;"></div>
                        <div style="display: flex; gap: 12px;">
                            <button class="btn-secondary" onclick="continueAIChat()" style="flex: 1;">
                                <i class="fas fa-edit"></i> 继续修改
                            </button>
                            <button class="btn-primary" onclick="confirmAIChat()" style="flex: 1;">
                                <i class="fas fa-check"></i> 确认添加
                            </button>
                        </div>
                    </div>
                    <div id="aiChatInput" style="padding: 16px; border-top: 1px solid var(--divider-color); background: var(--bg-primary);">
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <div style="flex: 4; position: relative;">
                                <input type="text" id="aiChatInputField" class="mobile-input" placeholder="输入消息..." style="width: 100%; margin: 0; padding-right: 48px;">
                                <button class="btn-secondary" onclick="startVoiceInput(event)" style="position: absolute; right: 8px; top: 50%; transform: translateY(-50%); padding: 8px 12px; margin: 0; background: transparent; border: none; color: var(--text-secondary);">
                                    <i class="fas fa-microphone"></i>
                                </button>
                            </div>
                            <button class="btn-primary" onclick="sendAIMessage()" style="flex: 1; padding: 12px; margin: 0;">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', html);
    
    // 初始化对话历史
    window.aiChatHistory = [];
    window.aiChatItems = [];
    
    // 加载历史对话记录
    loadChatHistory();
    
    // 绑定回车发送
    document.getElementById('aiChatInputField').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendAIMessage();
        }
    });
    
    setTimeout(() => {
        document.getElementById('aiChatDrawer').classList.add('active');
        document.getElementById('aiChatInputField').focus();
    }, 10);
}

// 加载对话历史
async function loadChatHistory() {
    try {
        const response = await fetch('/item/chat-history');
        const result = await response.json();
        
        if (result.success && result.history && result.history.length > 0) {
            const messagesContainer = document.getElementById('aiChatMessages');
            
            // 清空欢迎消息
            messagesContainer.innerHTML = '';
            
            // 渲染历史消息
            result.history.forEach(msg => {
                if (msg.role === 'user') {
                    messagesContainer.insertAdjacentHTML('beforeend', `
                        <div class="user-message-wrapper" style="display: flex; flex-direction: column; align-items: flex-end; margin-bottom: 16px;">
                            <div style="display: flex; gap: 12px; justify-content: flex-end;">
                                <div class="user-message-bubble" data-message="${escapeHtml(msg.content)}" style="background: var(--primary-color); color: white; padding: 12px 16px; border-radius: 12px; max-width: 80%; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                                    ${escapeHtml(msg.content)}
                                </div>
                                <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--text-secondary); display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0;">
                                    <i class="fas fa-user"></i>
                                </div>
                            </div>
                            <div class="message-actions" style="display: flex; gap: 8px; margin-top: 6px; margin-right: 48px; opacity: 0; transition: opacity 0.2s;">
                                <button onclick="retryMessage(this)" class="message-action-btn" title="重试">
                                    <i class="fas fa-redo"></i>
                                </button>
                                <button onclick="copyMessage(this)" class="message-action-btn" title="复制">
                                    <i class="fas fa-copy"></i>
                                </button>
                                <button onclick="editMessage(this)" class="message-action-btn" title="编辑">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button onclick="deleteMessage(this)" class="message-action-btn" title="删除">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                    `);
                } else if (msg.role === 'assistant') {
                    messagesContainer.insertAdjacentHTML('beforeend', `
                        <div style="display: flex; gap: 12px; margin-bottom: 16px;">
                            <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--primary-color); display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0;">
                                <i class="fas fa-robot"></i>
                            </div>
                            <div style="background: white; padding: 12px 16px; border-radius: 12px; max-width: 80%; box-shadow: 0 1px 2px rgba(0,0,0,0.1); white-space: pre-wrap;">
                                ${escapeHtml(msg.content)}
                            </div>
                        </div>
                    `);
                }
                
                // 添加到对话历史数组
                window.aiChatHistory.push({
                    role: msg.role,
                    content: msg.content
                });
            });
            
            // 滚动到底部
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            showToast(`已加载 ${result.count} 条历史记录`, 'success', 2000);
        }
    } catch (error) {
        console.error('加载对话历史失败:', error);
        // 失败时显示默认欢迎消息
    }
}

// 发送AI消息
async function sendAIMessage() {
    const input = document.getElementById('aiChatInputField');
    const message = input.value.trim();
    
    if (!message) {
        return;
    }
    
    // 添加用户消息到界面
    const messagesContainer = document.getElementById('aiChatMessages');
    const messageId = 'msg-' + Date.now();
    messagesContainer.insertAdjacentHTML('beforeend', `
        <div class="user-message-wrapper" style="display: flex; flex-direction: column; align-items: flex-end; margin-bottom: 16px;">
            <div style="display: flex; gap: 12px; justify-content: flex-end;">
                <div class="user-message-bubble" data-message="${escapeHtml(message)}" style="background: var(--primary-color); color: white; padding: 12px 16px; border-radius: 12px; max-width: 80%; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    ${escapeHtml(message)}
                </div>
                <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--text-secondary); display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0;">
                    <i class="fas fa-user"></i>
                </div>
            </div>
            <div class="message-actions" style="display: flex; gap: 8px; margin-top: 6px; margin-right: 48px; opacity: 0; transition: opacity 0.2s;">
                <button onclick="retryMessage(this)" class="message-action-btn" title="重试">
                    <i class="fas fa-redo"></i>
                </button>
                <button onclick="copyMessage(this)" class="message-action-btn" title="复制">
                    <i class="fas fa-copy"></i>
                </button>
                <button onclick="editMessage(this)" class="message-action-btn" title="编辑">
                    <i class="fas fa-edit"></i>
                </button>
                <button onclick="deleteMessage(this)" class="message-action-btn" title="删除">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `);
    
    input.value = '';
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // 添加到对话历史
    window.aiChatHistory.push({
        role: 'user',
        content: message
    });
    
    // 显示加载动画
    messagesContainer.insertAdjacentHTML('beforeend', `
        <div class="ai-message-loading" style="display: flex; gap: 12px; margin-bottom: 16px;">
            <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--primary-color); display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0;">
                <i class="fas fa-robot"></i>
            </div>
            <div style="background: white; padding: 12px 16px; border-radius: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                <i class="fas fa-spinner fa-spin"></i> 思考中...
            </div>
        </div>
    `);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    try {
        // 使用fetch接收流式响应
        const response = await fetch('/item/ai-chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: window.aiChatHistory
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        let aiReplyDiv = null;
        let fullReply = '';
        let lastUpdateTime = Date.now();
        let buffer = '';
        
        // 创建AI回复容器
        const createAIReplyDiv = () => {
            const div = document.createElement('div');
            div.style.cssText = 'display: flex; gap: 12px; margin-bottom: 16px;';
            div.innerHTML = `
                <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--primary-color); display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0;">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="ai-reply-content" style="background: white; padding: 12px 16px; border-radius: 12px; max-width: 80%; box-shadow: 0 1px 2px rgba(0,0,0,0.1); white-space: pre-wrap;"></div>
            `;
            return div;
        };
        
        // 读取流式数据
        while (true) {
            const {done, value} = await reader.read();
            
            if (done) {
                break;
            }
            
            lastUpdateTime = Date.now();
            buffer += decoder.decode(value, {stream: true});
            
            // 处理SSE格式的数据
            const lines = buffer.split('\n');
            buffer = lines.pop(); // 保留不完整的行
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.substring(6));
                        
                        if (data.error) {
                            // 处理错误
                            const loadingMsg = messagesContainer.querySelector('.ai-message-loading');
                            if (loadingMsg) loadingMsg.remove();
                            
                            const errorReply = `抱歉，处理您的请求时出现了问题：\n${data.error}\n\n请尝试重新发送，或使用"新开会话"功能。`;
                            messagesContainer.insertAdjacentHTML('beforeend', `
                                <div style="display: flex; gap: 12px; margin-bottom: 16px;">
                                    <div style="width: 36px; height: 36px; border-radius: 50%; background: #ffc107; display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0;">
                                        <i class="fas fa-exclamation-triangle"></i>
                                    </div>
                                    <div style="background: #fff3cd; padding: 12px 16px; border-radius: 12px; max-width: 80%; box-shadow: 0 1px 2px rgba(0,0,0,0.1); white-space: pre-wrap; border-left: 3px solid #ffc107;">
                                        ${escapeHtml(errorReply)}
                                    </div>
                                </div>
                            `);
                            messagesContainer.scrollTop = messagesContainer.scrollHeight;
                            return;
                        }
                        
                        if (data.done) {
                            // 流式输出完成
                            const loadingMsg = messagesContainer.querySelector('.ai-message-loading');
                            if (loadingMsg) loadingMsg.remove();
                            
                            // 添加到对话历史
                            window.aiChatHistory.push({
                                role: 'assistant',
                                content: fullReply
                            });
                            
                            // 检查是否包含JSON数据
                            if (fullReply.includes('```json')) {
                                try {
                                    const jsonPart = fullReply.split('```json')[1].split('```')[0].trim();
                                    const parsed = JSON.parse(jsonPart);
                                    
                                    if (parsed.items && parsed.items.length > 0) {
                                        window.aiChatItems = parsed.items;
                                        showAIChatConfirm(parsed.items);
                                    }
                                } catch (e) {
                                    console.error('解析JSON失败:', e);
                                }
                            }
                            
                            return;
                        }
                        
                        if (data.content) {
                            // 接收到内容片段
                            fullReply += data.content;
                            
                            // 移除加载动画（首次接收时）
                            if (!aiReplyDiv) {
                                const loadingMsg = messagesContainer.querySelector('.ai-message-loading');
                                if (loadingMsg) loadingMsg.remove();
                                
                                // 创建AI回复容器
                                aiReplyDiv = createAIReplyDiv();
                                messagesContainer.appendChild(aiReplyDiv);
                            }
                            
                            // 更新内容
                            const contentDiv = aiReplyDiv.querySelector('.ai-reply-content');
                            contentDiv.textContent = fullReply;
                            messagesContainer.scrollTop = messagesContainer.scrollHeight;
                        }
                        
                    } catch (e) {
                        console.error('解析SSE数据错误:', e, line);
                    }
                }
            }
        }
        
    } catch (error) {
        console.error('AI对话错误:', error);
        
        // 移除加载动画
        const loadingMsg = messagesContainer.querySelector('.ai-message-loading');
        if (loadingMsg) {
            loadingMsg.remove();
        }
        
        showToast('AI对话失败，请重试', 'error');
    }
}

// 显示确认界面
function showAIChatConfirm(items) {
    const confirmDiv = document.getElementById('aiChatConfirm');
    const inputDiv = document.getElementById('aiChatInput');
    const previewDiv = document.getElementById('aiChatItemsPreview');
    
    // 生成物品预览（优化显示格式）
    let previewHtml = `<div style="font-size: 13px; color: var(--text-secondary); margin-bottom: 12px;">共 ${items.length} 个物品</div>`;
    
    items.forEach((item, index) => {
        previewHtml += `
            <div style="padding: 14px; background: white; border-radius: 8px; margin-bottom: 10px; border: 1px solid var(--divider-color);">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="width: 24px; height: 24px; border-radius: 50%; background: var(--primary-color); color: white; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600; margin-right: 10px;">
                        ${index + 1}
                    </div>
                    <div style="font-weight: 600; font-size: 15px; color: var(--text-primary);">
                        ${escapeHtml(item.name)} × ${item.quantity}${item.unit || '个'}
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px; color: var(--text-secondary); padding-left: 34px;">
                    <div>
                        <i class="fas fa-calendar" style="margin-right: 4px;"></i>
                        ${item.expire_date || '未知'}
                    </div>
                    <div>
                        <i class="fas fa-map-marker-alt" style="margin-right: 4px;"></i>
                        ${item.place || '未分类'}
                    </div>
                    ${item.type ? `
                    <div style="grid-column: 1 / -1;">
                        <i class="fas fa-tag" style="margin-right: 4px;"></i>
                        ${item.type}
                    </div>
                    ` : ''}
                </div>
            </div>
        `;
    });
    
    previewDiv.innerHTML = previewHtml;
    
    // 显示确认界面，隐藏输入框
    confirmDiv.style.display = 'block';
    inputDiv.style.display = 'none';
}

// 重置AI对话（新开会话）
async function resetAIChat() {
    if (!confirm('确定要开始新会话吗？当前对话记录将被清空。')) {
        return;
    }
    
    try {
        // 调用后端清空历史记录
        const response = await fetch('/item/chat-history/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 清空对话历史
            window.aiChatHistory = [];
            window.aiChatItems = [];
            
            // 清空消息容器
            const messagesContainer = document.getElementById('aiChatMessages');
            messagesContainer.innerHTML = `
                <div class="ai-message" style="display: flex; gap: 12px; margin-bottom: 16px;">
                    <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--primary-color); display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0;">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div style="background: white; padding: 12px 16px; border-radius: 12px; max-width: 80%; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                        你好！我可以帮你添加物品到冰箱。请告诉我物品的名称、数量和过期时间。
                    </div>
                </div>
            `;
            
            // 隐藏确认界面，显示输入框
            document.getElementById('aiChatConfirm').style.display = 'none';
            document.getElementById('aiChatInput').style.display = 'block';
            
            // 聚焦输入框
            document.getElementById('aiChatInputField').focus();
            
            showToast(result.message || '已开始新会话', 'success');
        } else {
            showToast(result.error || '清空失败', 'error');
        }
    } catch (error) {
        console.error('清空对话历史失败:', error);
        showToast('清空失败，请重试', 'error');
    }
}

// 继续对话
function continueAIChat() {
    const confirmDiv = document.getElementById('aiChatConfirm');
    const inputDiv = document.getElementById('aiChatInput');
    
    confirmDiv.style.display = 'none';
    inputDiv.style.display = 'block';
    
    document.getElementById('aiChatInputField').focus();
}

// 确认添加物品
async function confirmAIChat() {
    const items = window.aiChatItems;
    
    if (!items || items.length === 0) {
        showToast('没有可添加的物品', 'warning');
        return;
    }
    
    showToast('正在添加物品...', 'info');
    
    try {
        // 使用批量添加接口
        const response = await fetch('/item/batch-insert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                items: items
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            let message = `成功添加 ${result.added} 个物品`;
            
            if (result.failed > 0) {
                message += `，${result.failed} 个失败`;
            }
            
            showToast(message, result.failed > 0 ? 'warning' : 'success');
            
            // 清空当前物品列表
            window.aiChatItems = [];
            
            // 隐藏确认界面，显示输入框，让用户可以继续添加
            const confirmDiv = document.getElementById('aiChatConfirm');
            const inputDiv = document.getElementById('aiChatInput');
            confirmDiv.style.display = 'none';
            inputDiv.style.display = 'block';
            
            // 在对话中添加成功提示
            const messagesContainer = document.getElementById('aiChatMessages');
            messagesContainer.insertAdjacentHTML('beforeend', `
                <div style="display: flex; gap: 12px; margin-bottom: 16px;">
                    <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--success-color); display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0;">
                        <i class="fas fa-check"></i>
                    </div>
                    <div style="background: #e8f5e9; padding: 12px 16px; border-radius: 12px; max-width: 80%; box-shadow: 0 1px 2px rgba(0,0,0,0.1); border-left: 3px solid var(--success-color);">
                        ${message}！还需要添加其他物品吗？
                    </div>
                </div>
            `);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            // 聚焦输入框
            document.getElementById('aiChatInputField').focus();
            
            // 刷新物品列表（不刷新整个页面）
            if (typeof loadAllItems === 'function') {
                loadAllItems();
            }
        } else {
            showToast(result.error || '添加失败', 'error');
        }
    } catch (error) {
        console.error('添加物品错误:', error);
        showToast('添加失败，请重试', 'error');
    }
}

// HTML转义函数
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 重试消息
function retryMessage(btn) {
    const wrapper = btn.closest('.user-message-wrapper');
    const bubble = wrapper.querySelector('.user-message-bubble');
    const message = bubble.dataset.message;
    
    if (message) {
        // 填充到输入框
        document.getElementById('aiChatInputField').value = message;
        // 自动发送
        sendAIMessage();
    }
}

// 复制消息
function copyMessage(btn) {
    const wrapper = btn.closest('.user-message-wrapper');
    const bubble = wrapper.querySelector('.user-message-bubble');
    const message = bubble.dataset.message;
    
    if (message) {
        navigator.clipboard.writeText(message).then(() => {
            showToast('已复制到剪贴板', 'success', 1500);
        }).catch(() => {
            showToast('复制失败', 'error');
        });
    }
}

// 编辑消息
function editMessage(btn) {
    const wrapper = btn.closest('.user-message-wrapper');
    const bubble = wrapper.querySelector('.user-message-bubble');
    const message = bubble.dataset.message;
    
    if (message) {
        // 填充到输入框
        document.getElementById('aiChatInputField').value = message;
        document.getElementById('aiChatInputField').focus();
        showToast('消息已填入输入框，可以编辑后重新发送', 'info', 2000);
    }
}

// 删除消息
function deleteMessage(btn) {
    const wrapper = btn.closest('.user-message-wrapper');
    
    if (confirm('确定要删除这条消息吗？')) {
        wrapper.remove();
        showToast('消息已删除', 'success', 1500);
    }
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
    
    const formData = new FormData();
    formData.append('itemName', $('#mAddItemForm input[name="itemName"]').val());
    formData.append('itemDate', $('#mAddItemForm input[name="itemDate"]').val().replace(/-/g, ''));
    formData.append('itemNum', $('#mAddItemForm input[name="itemNum"]').val());
    formData.append('itemPlace', $('#mAddItemForm input[name="itemPlace"]:checked').val());
    formData.append('itemType', $('#mSelectedTypes').val());
    
    if (!$('#mSelectedTypes').val()) {
        showToast('请选择至少一个类别', 'warning');
        return;
    }
    
    $.ajax({
        url: '/item/insert',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.success) {
                showToast('添加成功', 'success');
                closeDrawer('addItemDrawer');
                loadAllItems();
            } else {
                showToast(response.error || '添加失败', 'error');
            }
        },
        error: function(xhr) {
            const response = xhr.responseJSON;
            showToast(response?.error || '网络错误，请重试', 'error');
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


// 语音输入相关
let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;
let recordingButton = null;

// 开始语音输入
async function startVoiceInput(event) {
    const btn = event ? event.target.closest('button') : recordingButton;
    recordingButton = btn;
    
    if (isRecording) {
        stopVoiceInput();
        return;
    }
    
    try {
        // 请求麦克风权限
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // 创建录音器 - 尝试使用wav格式
        const options = { mimeType: 'audio/webm' };
        mediaRecorder = new MediaRecorder(stream, options);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };
        
        mediaRecorder.onstop = async () => {
            // 停止所有音轨
            stream.getTracks().forEach(track => track.stop());
            
            // 创建音频blob
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            
            // 转换为WAV格式并发送
            await convertAndProcessVoice(audioBlob);
        };
        
        // 开始录音
        mediaRecorder.start();
        isRecording = true;
        
        // 更新按钮状态
        btn.innerHTML = '<i class="fas fa-stop"></i>';
        btn.style.background = '#f44336';
        btn.style.color = 'white';
        
        showToast('正在录音，再次点击停止...', 'info', 2000);
        
    } catch (error) {
        console.error('无法访问麦克风:', error);
        showToast('无法访问麦克风，请检查权限设置', 'error');
    }
}

// 停止语音输入
function stopVoiceInput() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        
        // 恢复按钮状态
        if (recordingButton) {
            recordingButton.innerHTML = '<i class="fas fa-microphone"></i>';
            recordingButton.style.background = '';
            recordingButton.style.color = '';
        }
        
        showToast('录音结束，正在识别...', 'info', 1500);
    }
}

// 转换webm为wav格式
async function convertAndProcessVoice(webmBlob) {
    try {
        // 创建AudioContext
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        // 读取webm数据
        const arrayBuffer = await webmBlob.arrayBuffer();
        
        // 解码音频数据
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
        
        // 转换为WAV格式
        const wavBlob = audioBufferToWav(audioBuffer);
        
        // 发送到后端进行语音识别
        await processVoiceInput(wavBlob);
        
    } catch (error) {
        console.error('音频转换错误:', error);
        showToast('音频处理失败，请重试', 'error');
    }
}

// 将AudioBuffer转换为WAV格式
function audioBufferToWav(audioBuffer) {
    const numOfChan = audioBuffer.numberOfChannels;
    const length = audioBuffer.length * numOfChan * 2 + 44;
    const buffer = new ArrayBuffer(length);
    const view = new DataView(buffer);
    const channels = [];
    let offset = 0;
    let pos = 0;
    
    // 写入WAV文件头
    setUint32(0x46464952); // "RIFF"
    setUint32(length - 8); // file length - 8
    setUint32(0x45564157); // "WAVE"
    
    setUint32(0x20746d66); // "fmt " chunk
    setUint32(16); // length = 16
    setUint16(1); // PCM (uncompressed)
    setUint16(numOfChan);
    setUint32(audioBuffer.sampleRate);
    setUint32(audioBuffer.sampleRate * 2 * numOfChan); // avg. bytes/sec
    setUint16(numOfChan * 2); // block-align
    setUint16(16); // 16-bit
    
    setUint32(0x61746164); // "data" - chunk
    setUint32(length - pos - 4); // chunk length
    
    // 写入音频数据
    for (let i = 0; i < audioBuffer.numberOfChannels; i++) {
        channels.push(audioBuffer.getChannelData(i));
    }
    
    while (pos < length - 44) {
        for (let i = 0; i < numOfChan; i++) {
            let sample = Math.max(-1, Math.min(1, channels[i][offset]));
            sample = sample < 0 ? sample * 0x8000 : sample * 0x7FFF;
            view.setInt16(pos, sample, true);
            pos += 2;
        }
        offset++;
    }
    
    return new Blob([buffer], { type: 'audio/wav' });
    
    function setUint16(data) {
        view.setUint16(pos, data, true);
        pos += 2;
    }
    
    function setUint32(data) {
        view.setUint32(pos, data, true);
        pos += 4;
    }
}

// 处理语音输入
async function processVoiceInput(audioBlob) {
    try {
        // 将blob转换为base64
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        
        reader.onloadend = async () => {
            const base64Audio = reader.result;
            
            // 发送到后端进行语音识别
            const response = await fetch('/item/voice-to-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    audio: base64Audio
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // 将识别的文字填入输入框
                const input = document.getElementById('aiChatInputField');
                input.value = result.text;
                input.focus();
                
                showToast('识别成功！', 'success');
            } else {
                showToast(result.error || '语音识别失败', 'error');
            }
        };
    } catch (error) {
        console.error('语音识别错误:', error);
        showToast('语音识别失败，请重试', 'error');
    }
}
