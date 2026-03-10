# -*- coding: utf-8 -*-
"""物品路由 - RESTful API"""
from flask import Blueprint, request, jsonify, Response
from datetime import datetime
from app import db_client
from app.services.item_service import ItemService
from app.utils.jwt_auth import jwt_required, get_current_user, jwt_optional
import json

item_bp = Blueprint('item', __name__)


def log(message):
    """带时间戳的日志输出"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")


@item_bp.route('/total', methods=['GET'])
@jwt_optional
def total():
    """获取所有物品 API - 允许游客访问公共冰箱"""
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    # 从查询参数获取冰箱ID
    fridge_id = request.args.get('fridge_id', 'public')
    
    item_service = ItemService(db_client.fridge)
    
    # 如果是公共冰箱,只查询公共物品
    if fridge_id == 'public':
        items = item_service.get_user_items('public')
    else:
        # 游客只能访问公共冰箱
        if user_id == 'public':
            return jsonify({'success': False, 'error': '游客只能访问公共冰箱'}), 403
        # 查询指定冰箱的物品
        items = [item for item in item_service.get_user_items(user_id) 
                if item.get('fridge_id') == fridge_id]
    
    return jsonify({'success': True, 'data': list(items)}), 200


@item_bp.route('/insert', methods=['POST'])
@jwt_required
def insert():
    """添加物品 API"""
    from app.models.system_settings import SystemSettings
    
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    data = request.get_json() if request.is_json else request.form
    
    # 获取当前冰箱ID
    fridge_id = data.get('fridge_id', 'public')
    
    # 检查用户物品数量限制
    if user_id != 'public':
        system_settings = SystemSettings(db_client.fridge)
        settings = system_settings.get_all_settings()
        max_items = settings.get('max_items_per_user', 0)
        
        if max_items > 0:
            item_service = ItemService(db_client.fridge)
            current_items = item_service.get_user_items(user_id)
            if len(current_items) >= max_items:
                return jsonify({'success': False, 'error': f'已达到最大物品数量限制（{max_items}个）'}), 400
    
    try:
        item_name = data.get('itemName') or data.get('name')
        item_date = data.get('itemDate') or data.get('expire_date')
        item_place = data.get('itemPlace') or data.get('place')
        item_num = data.get('itemNum') or data.get('quantity', 1)
        item_type = data.get('itemType') or data.get('type', '其他')
        
        if not all([item_name, item_date, item_place]):
            return jsonify({'success': False, 'error': '缺少必要字段'}), 400
        
        # 解析日期
        date = item_date.replace('-', '')
        expire_date = datetime.strptime(date, "%Y%m%d")
        
        item_service = ItemService(db_client.fridge)
        item = item_service.create_item(
            user_id=user_id,
            name=item_name,
            expire_date=expire_date,
            place=item_place,
            num=int(item_num),
            item_type=item_type
        )
        
        # 设置fridge_id
        item_service.update_item(user_id, item._id, fridge_id=fridge_id)
        
        return jsonify({'success': True, 'message': '添加成功', 'data': {'id': item._id}}), 200
    except Exception as e:
        log(f'添加物品失败: {e}')
        return jsonify({'success': False, 'error': '添加失败'}), 500


@item_bp.route('/update', methods=['PUT'])
@jwt_required
def update():
    """更新物品 API"""
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    try:
        data = request.get_json()
        item_id = data.get('itemId') or data.get('id')
        
        if not item_id:
            return jsonify({'success': False, 'error': '缺少物品ID'}), 400
        
        # 准备更新数据
        update_data = {}
        
        if 'itemName' in data or 'name' in data:
            update_data['Name'] = data.get('itemName') or data.get('name')
        
        if 'itemDate' in data or 'expire_date' in data:
            date_str = (data.get('itemDate') or data.get('expire_date')).replace('-', '')
            update_data['ExpireDate'] = datetime.strptime(date_str, "%Y%m%d")
        
        if 'itemPlace' in data or 'place' in data:
            update_data['Place'] = data.get('itemPlace') or data.get('place')
        
        if 'itemNum' in data or 'quantity' in data:
            update_data['Num'] = int(data.get('itemNum') or data.get('quantity'))
        
        if 'itemType' in data or 'type' in data:
            update_data['Type'] = data.get('itemType') or data.get('type')
        
        # 执行更新
        item_service = ItemService(db_client.fridge)
        item_service.update_item(user_id=user_id, item_id=item_id, **update_data)
        
        return jsonify({'success': True, 'message': '更新成功'}), 200
    
    except Exception as e:
        print(f'更新物品失败: {e}')
        return jsonify({'success': False, 'error': '更新失败'}), 500


@item_bp.route('/delete', methods=['DELETE'])
@jwt_required
def delete_item():
    """删除物品 API"""
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    try:
        # 支持从 JSON body 或查询参数获取 ID
        item_id = request.get_json().get('itemId') if request.is_json else request.args.get('id')
        
        if not item_id:
            return jsonify({'success': False, 'error': '缺少物品ID'}), 400
        
        item_service = ItemService(db_client.fridge)
        item_service.delete_item(user_id, item_id)
        
        return jsonify({'success': True, 'message': '删除成功'}), 200
    
    except Exception as e:
        print(f'删除物品失败: {e}')
        return jsonify({'success': False, 'error': '删除失败'}), 500


@item_bp.route('/search', methods=['POST'])
@jwt_optional
def search():
    """搜索物品 API - 允许游客访问公共冰箱"""
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    data = request.get_json() if request.is_json else request.form
    searchbox = data.get('text') or data.get('keyword', '')
    fridge_id = data.get('fridge_id', 'public')
    
    item_service = ItemService(db_client.fridge)
    
    # 如果是公共冰箱,只搜索公共物品
    if fridge_id == 'public':
        items = item_service.search_items('public', searchbox)
    else:
        # 游客只能访问公共冰箱
        if user_id == 'public':
            return jsonify({'success': False, 'error': '游客只能访问公共冰箱'}), 403
        # 搜索指定冰箱的物品
        all_items = item_service.search_items(user_id, searchbox)
        items = [item for item in all_items if item.get('fridge_id') == fridge_id]
    
    return jsonify({'success': True, 'data': list(items)}), 200



@item_bp.route('/ocr', methods=['POST'])
@jwt_required
def ocr_recognize():
    """OCR文字识别 API - 混合方案：OCR识别+AI解析"""
    from app.models.system_settings import SystemSettings
    from app.services.ocr_service import ocr_service, AIService
    
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    # 检查AI功能是否启用
    system_settings = SystemSettings(db_client.fridge)
    settings = system_settings.get_all_settings()
    
    if not settings.get('enable_ai_features'):
        return jsonify({'success': False, 'error': 'AI功能未启用'}), 403
    
    try:
        # 获取图片数据
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': '未提供图片数据'}), 400
        
        image_data = data['image']
        use_vision = data.get('use_vision', False)
        
        log(f"[OCR] 开始识别，使用视觉模型: {use_vision}")
        
        # 方案选择
        if use_vision:
            # 方案2：直接使用视觉模型识别
            print("[OCR] 使用视觉模型直接识别")
            api_base = settings.get('openai_api_base', '').strip()
            api_key = settings.get('openai_api_key', '').strip()
            vision_model = settings.get('openai_vision_model', 'gpt-4-vision-preview')
            
            if not api_base or not api_key:
                return jsonify({'success': False, 'error': 'AI API未配置'}), 400
            
            result = AIService.recognize_image_with_vision(
                image_data, api_base, api_key, vision_model
            )
            
            return jsonify({
                'success': True,
                'method': 'vision',
                'items': result.get('items', [])
            }), 200
            
        else:
            # 方案1：OCR识别 + AI解析（推荐）
            print("[OCR] 使用混合方案：OCR识别 + AI解析")
            
            # 步骤1：OCR识别文字
            if not ocr_service.is_available():
                return jsonify({
                    'success': False, 
                    'error': 'OCR引擎未安装，请安装PaddleOCR或使用视觉模型'
                }), 500
            
            print("[OCR] 步骤1：OCR识别文字")
            ocr_text = ocr_service.recognize_from_base64(image_data)
            print(f"[OCR] 识别结果：{ocr_text[:100]}...")
            
            if not ocr_text or len(ocr_text.strip()) == 0:
                return jsonify({
                    'success': False,
                    'error': '未识别到文字，请确保图片清晰'
                }), 400
            
            # 步骤2：AI解析文字
            print("[OCR] 步骤2：AI解析文字")
            api_base = settings.get('openai_api_base', '').strip()
            api_key = settings.get('openai_api_key', '').strip()
            chat_model = settings.get('openai_chat_model', 'gpt-3.5-turbo')
            
            if not api_base or not api_key:
                # 如果没有配置AI，至少返回识别的文字
                return jsonify({
                    'success': True,
                    'method': 'ocr_only',
                    'text': ocr_text,
                    'items': []
                }), 200
            
            result = AIService.parse_ocr_text(
                ocr_text, api_base, api_key, chat_model
            )
            
            print(f"[OCR] 解析结果：{result}")
            
            return jsonify({
                'success': True,
                'method': 'ocr_ai',
                'text': ocr_text,
                'items': result.get('items', [])
            }), 200
        
    except Exception as e:
        print(f"[OCR] 识别失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'识别失败: {str(e)}'}), 500


@item_bp.route('/ai-chat', methods=['POST'])
@jwt_required
def ai_chat():
    """AI对话 API（流式输出 SSE）"""
    from app.models.system_settings import SystemSettings
    from app.models.chat_history import ChatHistory
    import requests
    
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    # 检查AI功能是否启用
    system_settings = SystemSettings(db_client.fridge)
    chat_history_model = ChatHistory(db_client.fridge.chat_history)
    settings = system_settings.get_all_settings()
    
    if not settings.get('enable_ai_features'):
        return jsonify({'success': False, 'error': 'AI功能未启用'}), 403
    
    try:
        # 获取请求数据
        data = request.get_json()
        messages = data.get('messages', [])
        
        if not messages or not isinstance(messages, list):
            return jsonify({'success': False, 'error': '消息格式错误'}), 400
        
        # 获取最后一条用户消息
        last_message = messages[-1] if messages else {}
        if not last_message.get('content'):
            return jsonify({'success': False, 'error': '消息不能为空'}), 400
        
        log(f"[AI对话] 收到消息，历史记录: {len(messages)} 条")
        
        # 获取AI配置
        api_base = settings.get('openai_api_base', '').strip()
        api_key = settings.get('openai_api_key', '').strip()
        chat_model = settings.get('openai_chat_model', 'gpt-3.5-turbo')
        
        if not api_base or not api_key:
            return jsonify({
                'success': False, 
                'error': 'AI服务未配置，请联系管理员'
            }), 500
        
        # 获取当前日期信息
        now = datetime.now()
        today_str = now.strftime('%Y年%m月%d日')
        today_date = now.strftime('%Y-%m-%d')
        weekday_names = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        weekday = weekday_names[now.weekday()]
        
        # 构建系统提示词
        system_prompt = f"""你是一个智能冰箱管理助手。你的任务是帮助用户添加物品到冰箱。

【重要信息】
今天的日期是：{today_str}（{weekday}）
日期格式：{today_date}

【常见食品保质期参考】
- 新鲜蔬菜：3-7天（叶菜3天，根茎类7天）
- 新鲜水果：5-14天（浆果5天，苹果橙子14天）
- 鲜奶：7天
- 酸奶：14-21天
- 鸡蛋：30天
- 新鲜肉类（冷藏）：2-3天
- 新鲜肉类（冷冻）：90天
- 熟食：2-3天
- 面包：3-5天
- 调味品：根据包装标注

【物品分类和存放建议】
- 水果：冷藏（香蕉、芒果等热带水果可常温）
- 蔬菜：冷藏
- 肉类：冷藏（短期）或冷冻（长期）
- 饮料：冷藏
- 调味品：常温或冷藏
- 面包糕点：常温（短期）或冷冻（长期）
- 乳制品：冷藏

请通过对话收集以下信息：
1. 物品名称（必需）
2. 数量和单位（必需）
3. 过期日期（必需，格式：YYYY-MM-DD）
   - 主动根据物品类型给出保质期建议
4. 存放位置（必需：冷藏、冷冻、常温）
   - 主动根据物品类型给出存放建议
5. 物品类型（必需：蔬菜、水果、肉类、饮料、调味品、面包糕点、乳制品等）
   - 主动根据物品名称判断类型

【对话风格】
- 主动提供所有建议（过期日期、存放位置、物品类型）
- 一次性给出完整建议，让用户确认即可
- 简洁明了，不要反复询问
- 给出具体的日期而不是天数
- 支持一次添加多个物品
- 支持连续添加：用户确认添加后，可以继续添加更多物品

【重要】当收集到完整信息后的回复格式：
1. 先用友好的文字总结物品信息（使用列表或表格）
2. 然后在代码块中提供JSON数据

示例格式：
好的！为您整理了以下物品：

1. 香水柠檬 × 2个
   - 过期日期：2026-03-23
   - 存放位置：冷藏
   - 分类：水果

确认添加吗？

```json
{{"items": [{{"name": "香水柠檬", "quantity": 2, "unit": "个", "expire_date": "2026-03-23", "place": "冷藏", "type": "水果"}}]}}
```"""
        
        # 构建完整的消息列表
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        
        # 保存用户消息到历史记录
        if messages and len(messages) > 0:
            last_user_message = messages[-1]
            if last_user_message.get('role') == 'user':
                chat_history_model.save_message(
                    user_id=user_id,
                    role='user',
                    content=last_user_message.get('content', '')
                )
        
        # 定义流式生成器
        def generate():
            full_reply = ''
            try:
                url = f"{api_base.rstrip('/')}/chat/completions"
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                }
                
                request_data = {
                    'model': chat_model,
                    'messages': full_messages,
                    'temperature': 0.7,
                    'max_tokens': 1000,
                    'stream': True
                }
                
                log(f"[AI对话流式] 调用API: {url}, 模型: {chat_model}")
                
                response = requests.post(url, headers=headers, json=request_data, timeout=120, stream=True)
                
                if response.status_code != 200:
                    error_data = {'error': f'API返回错误: {response.status_code}', 'done': True}
                    yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
                    return
                
                # 流式读取响应
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            line_data = line[6:]
                            
                            if line_data == '[DONE]':
                                # 保存完整的AI回复到历史记录
                                if full_reply:
                                    chat_history_model.save_message(
                                        user_id=user_id,
                                        role='assistant',
                                        content=full_reply
                                    )
                                
                                yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"
                                break
                            
                            try:
                                chunk = json.loads(line_data)
                                if 'choices' in chunk and len(chunk['choices']) > 0:
                                    delta = chunk['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        content = delta['content']
                                        full_reply += content
                                        yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"
                            except Exception as e:
                                log(f"[AI对话流式] 解析chunk错误: {e}")
                                continue
                
            except Exception as e:
                log(f"[AI对话流式] 错误: {e}")
                error_data = {'error': str(e), 'done': True}
                yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
        
        return Response(generate(), mimetype='text/event-stream', headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        })
        
    except Exception as e:
        log(f"[AI对话] 错误: {e}")
        import traceback
        traceback.print_exc()
        
        # 返回友好的错误消息
        error_message = str(e)
        if 'Read timed out' in error_message:
            error_reply = '抱歉，AI服务响应超时了。请稍后重试。'
        elif '503' in error_message or 'bad_response_status_code' in error_message:
            error_reply = '抱歉，AI服务暂时不可用。请检查API配置。'
        elif 'rate_limit' in error_message.lower():
            error_reply = '抱歉，API调用频率超限了。请稍等片刻再试。'
        elif 'invalid_api_key' in error_message.lower():
            error_reply = '抱歉，API密钥无效。请联系管理员检查配置。'
        else:
            error_reply = f'抱歉，处理您的请求时出现了问题：{error_message}'
        
        return jsonify({
            'success': False,
            'error': error_reply
        }), 500


@item_bp.route('/voice-to-text', methods=['POST'])
@jwt_required
def voice_to_text():
    """语音转文字 API"""
    from app.models.system_settings import SystemSettings
    import requests
    import base64
    import tempfile
    import os
    
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    # 检查AI功能是否启用
    system_settings = SystemSettings(db_client.fridge)
    settings = system_settings.get_all_settings()
    
    if not settings.get('enable_ai_features'):
        return jsonify({'success': False, 'error': 'AI功能未启用'}), 403
    
    try:
        # 获取音频数据
        data = request.get_json()
        audio_data = data.get('audio', '')
        
        if not audio_data:
            return jsonify({'success': False, 'error': '未提供音频数据'}), 400
        
        log(f"[语音识别] 收到音频数据")
        
        # 获取AI配置
        api_base = settings.get('openai_api_base', '').strip()
        api_key = settings.get('openai_api_key', '').strip()
        audio_model = settings.get('openai_audio_model', 'whisper-1')
        
        if not api_base or not api_key:
            return jsonify({
                'success': False, 
                'error': 'AI服务未配置，请联系管理员'
            }), 500
        
        # 解码base64音频数据
        if ',' in audio_data:
            audio_data = audio_data.split(',')[1]
        
        audio_bytes = base64.b64decode(audio_data)
        
        log(f"[语音识别] 音频数据大小: {len(audio_bytes)} 字节")
        
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name
        
        try:
            # 调用OpenAI Whisper API
            url = f"{api_base.rstrip('/')}/audio/transcriptions"
            
            log(f"[语音识别] 调用API: {url}, 模型: {audio_model}")
            
            with open(temp_path, 'rb') as audio_file:
                files = {
                    'file': ('audio.wav', audio_file, 'audio/wav')
                }
                data_payload = {
                    'model': audio_model
                }
                headers = {
                    'Authorization': f'Bearer {api_key}'
                }
                
                response = requests.post(url, headers=headers, files=files, data=data_payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text = result.get('text', '')
                
                log(f"[语音识别] 识别结果: {text}")
                
                return jsonify({
                    'success': True,
                    'text': text
                }), 200
            else:
                error_msg = response.text
                try:
                    error_json = response.json()
                    if 'error' in error_json:
                        error_detail = error_json['error']
                        if isinstance(error_detail, dict):
                            error_msg = error_detail.get('message', error_msg)
                        else:
                            error_msg = str(error_detail)
                except:
                    pass
                
                log(f"[语音识别] API错误: {response.status_code} - {error_msg}")
                return jsonify({
                    'success': False,
                    'error': f'语音识别失败: {error_msg}'
                }), 400
        
        finally:
            # 删除临时文件
            try:
                os.remove(temp_path)
            except:
                pass
        
    except Exception as e:
        log(f"[语音识别] 错误: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'语音识别失败: {str(e)}'}), 500


@item_bp.route('/batch-insert', methods=['POST'])
@jwt_required
def batch_insert():
    """批量添加物品 API"""
    from app.models.system_settings import SystemSettings
    from app.utils.validators import ItemValidator
    
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    # 获取当前冰箱ID
    data = request.get_json()
    fridge_id = data.get('fridge_id', 'public')
    
    try:
        items = data.get('items', [])
        
        if not items or not isinstance(items, list):
            return jsonify({'success': False, 'error': '请提供有效的物品列表'}), 400
        
        print(f"[批量添加] 收到 {len(items)} 个物品")
        
        # 批量校验物品数据
        valid_items, errors = ItemValidator.validate_batch_items(items)
        
        if not valid_items:
            return jsonify({
                'success': False,
                'error': '所有物品数据无效',
                'details': errors
            }), 400
        
        print(f"[批量添加] 校验通过 {len(valid_items)}/{len(items)} 个物品")
        
        # 检查用户物品数量限制
        if user_id != 'public':
            system_settings = SystemSettings(db_client.fridge)
            settings = system_settings.get_all_settings()
            max_items = settings.get('max_items_per_user', 0)
            
            if max_items > 0:
                item_service = ItemService(db_client.fridge)
                current_items = item_service.get_user_items(user_id)
                remaining = max_items - len(current_items)
                
                if remaining <= 0:
                    return jsonify({
                        'success': False,
                        'error': f'已达到最大物品数量限制（{max_items}个）'
                    }), 400
                
                if len(valid_items) > remaining:
                    return jsonify({
                        'success': False,
                        'error': f'超出物品数量限制，最多还能添加{remaining}个物品'
                    }), 400
        
        # 批量添加物品
        item_service = ItemService(db_client.fridge)
        added_items = []
        failed_items = []
        
        for item_data in valid_items:
            try:
                # 解析过期日期
                expire_date = datetime.strptime(item_data['expire_date'], "%Y-%m-%d")
                
                # 创建物品
                item = item_service.create_item(
                    user_id=user_id,
                    name=item_data['name'],
                    expire_date=expire_date,
                    place=item_data.get('place', '未分类'),
                    num=item_data.get('quantity', 1),
                    item_type=item_data.get('type', '其他')
                )
                
                # 设置fridge_id
                item_service.update_item(user_id, item._id, fridge_id=fridge_id)
                
                added_items.append({
                    'id': item._id,
                    'name': item_data['name'],
                    'quantity': item_data.get('quantity', 1)
                })
                
                print(f"[批量添加] 成功添加: {item_data['name']}")
                
            except Exception as e:
                print(f"[批量添加] 添加失败: {item_data['name']} - {e}")
                failed_items.append({
                    'name': item_data['name'],
                    'error': str(e)
                })
        
        # 返回结果
        result = {
            'success': True,
            'added': len(added_items),
            'failed': len(failed_items),
            'total': len(items),
            'items': added_items
        }
        
        if failed_items:
            result['failed_items'] = failed_items
        
        if errors:
            result['validation_errors'] = errors
        
        print(f"[批量添加] 完成: 成功{len(added_items)}, 失败{len(failed_items)}")
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"[批量添加] 错误: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'批量添加失败: {str(e)}'}), 500


@item_bp.route('/chat-history', methods=['GET'])
@jwt_optional
def get_chat_history():
    """获取用户的对话历史 API - 允许游客访问"""
    from app.models.chat_history import ChatHistory
    
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    try:
        # 游客返回空历史
        if user_id == 'public':
            return jsonify({
                'success': True,
                'data': [],
                'count': 0
            }), 200
        
        chat_history_model = ChatHistory(db_client.fridge.chat_history)
        history = chat_history_model.get_user_history(user_id, limit=30)
        
        return jsonify({
            'success': True,
            'data': history,
            'count': len(history)
        }), 200
        
    except Exception as e:
        log(f"[对话历史] 获取失败: {e}")
        return jsonify({'success': False, 'error': f'获取失败: {str(e)}'}), 500


@item_bp.route('/chat-history/clear', methods=['POST'])
@jwt_required
def clear_chat_history():
    """清空用户的对话历史 API"""
    from app.models.chat_history import ChatHistory
    
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    try:
        chat_history_model = ChatHistory(db_client.fridge.chat_history)
        deleted_count = chat_history_model.clear_user_history(user_id)
        
        log(f"[对话历史] 用户 {user_id} 清空了 {deleted_count} 条历史记录")
        
        return jsonify({
            'success': True,
            'message': f'已清空 {deleted_count} 条历史记录'
        }), 200
        
    except Exception as e:
        log(f"[对话历史] 清空失败: {e}")
        return jsonify({'success': False, 'error': f'清空失败: {str(e)}'}), 500
