# -*- coding: utf-8 -*-
"""OCR识别服务"""
import os
import base64
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime


def log(message):
    """带时间戳的日志输出"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")


class OCRService:
    """OCR识别服务"""
    
    def __init__(self):
        self.ocr = None
        self._init_ocr()
    
    def _init_ocr(self):
        """初始化OCR引擎"""
        try:
            from paddleocr import PaddleOCR
            # 使用中英文模型，关闭日志
            self.ocr = PaddleOCR(
                use_angle_cls=True,  # 启用方向分类
                lang='ch',  # 中文
                use_gpu=False,  # 不使用GPU
                show_log=False  # 关闭日志
            )
            log("[OCR] PaddleOCR初始化成功")
        except ImportError:
            log("[OCR] PaddleOCR未安装，OCR功能将不可用")
            self.ocr = None
        except Exception as e:
            log(f"[OCR] 初始化失败: {e}")
            self.ocr = None
    
    def is_available(self) -> bool:
        """检查OCR是否可用"""
        return self.ocr is not None
    
    def recognize_from_file(self, image_path: str) -> str:
        """从文件识别文字
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            识别的文字内容
        """
        if not self.is_available():
            raise Exception("OCR引擎未初始化")
        
        try:
            result = self.ocr.ocr(image_path, cls=True)
            
            # 提取所有文字
            texts = []
            if result and len(result) > 0:
                for line in result[0]:
                    if line and len(line) > 1:
                        text = line[1][0]  # 获取识别的文字
                        confidence = line[1][1]  # 获取置信度
                        if confidence > 0.5:  # 只保留置信度>0.5的结果
                            texts.append(text)
            
            return '\n'.join(texts)
        except Exception as e:
            raise Exception(f"OCR识别失败: {str(e)}")
    
    def recognize_from_base64(self, base64_data: str) -> str:
        """从base64数据识别文字
        
        Args:
            base64_data: base64编码的图片数据
            
        Returns:
            识别的文字内容
        """
        if not self.is_available():
            raise Exception("OCR引擎未初始化")
        
        try:
            # 解码base64
            if ',' in base64_data:
                base64_data = base64_data.split(',')[1]
            
            image_data = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_data))
            
            # 转换为RGB（如果是RGBA）
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            
            # 保存到临时文件
            temp_path = 'data/temp_ocr.jpg'
            os.makedirs('data', exist_ok=True)
            image.save(temp_path)
            
            # 识别
            text = self.recognize_from_file(temp_path)
            
            # 删除临时文件
            try:
                os.remove(temp_path)
            except:
                pass
            
            return text
        except Exception as e:
            raise Exception(f"OCR识别失败: {str(e)}")


class AIService:
    """AI服务（对话和视觉）"""
    
    @staticmethod
    def chat_for_item_info(messages: list, api_base: str, api_key: str, model: str) -> dict:
        """AI对话提取物品信息
        
        Args:
            messages: 对话历史 [{"role": "user/assistant", "content": "..."}]
            api_base: API地址
            api_key: API密钥
            model: 模型名称
            
        Returns:
            {"reply": "AI回复", "items": [...], "need_more_info": True/False}
        """
        from app.utils.validators import OCRResultValidator
        
        try:
            # 构建系统提示词
            system_prompt = """你是一个智能冰箱管理助手。你的任务是通过对话帮助用户添加食品物品到冰箱。

对话流程：
1. 询问用户要添加什么物品
2. 收集必要信息：物品名称、数量、过期日期
3. 可选信息：存放位置（冷冻/冷藏/常温）、物品类型（肉类/蔬菜/水果/饮料/调料/速食/其他）
4. 信息收集完整后，返回JSON格式的物品数据

对话规则：
- 友好、简洁、高效
- 如果用户一次性提供了完整信息，直接返回JSON
- 如果信息不完整，询问缺失的信息
- 如果用户提到生产日期和保质期，帮助计算过期日期
- 如果用户没有提供过期日期，根据物品类型给出合理建议

当信息收集完整时，必须在回复的最后添加JSON数据块：
```json
{
  "items": [
    {
      "name": "物品名称",
      "quantity": 数量,
      "unit": "单位",
      "expire_date": "YYYY-MM-DD",
      "place": "存放位置",
      "type": "物品类型"
    }
  ]
}
```

示例对话：
用户：我买了一箱牛奶
助手：好的！请问是什么品牌的牛奶？一箱有多少瓶？过期日期是什么时候？

用户：蒙牛纯牛奶，12盒，2026年12月31日过期
助手：明白了！我帮你添加：蒙牛纯牛奶 12盒，过期日期2026-12-31，建议放在冷藏。确认添加吗？
```json
{"items": [{"name": "蒙牛纯牛奶", "quantity": 12, "unit": "盒", "expire_date": "2026-12-31", "place": "冷藏", "type": "饮料"}]}
```"""

            # 构建完整的消息列表
            full_messages = [{"role": "system", "content": system_prompt}] + messages
            
            # 调用API
            url = f"{api_base.rstrip('/')}/chat/completions"
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': model,
                'messages': full_messages,
                'temperature': 0.7,  # 对话模式使用稍高的温度
                'max_tokens': 1000,
                'stream': True  # 启用流式输出
            }
            
            log(f"[AI对话] 调用API: {url}")
            log(f"[AI对话] 模型: {model}")
            log(f"[AI对话] 消息数: {len(messages)}")
            
            # 使用流式请求
            response = requests.post(url, headers=headers, json=data, timeout=120, stream=True)
            
            if response.status_code == 200:
                # 流式处理响应
                content = ""
                import json as json_module
                
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            line = line[6:]  # 移除 'data: ' 前缀
                            
                            if line == '[DONE]':
                                break
                            
                            try:
                                chunk = json_module.loads(line)
                                if 'choices' in chunk and len(chunk['choices']) > 0:
                                    delta = chunk['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        content += delta['content']
                            except:
                                continue
                
                log(f"[AI对话] 完整响应: {content[:200]}...")
                
                # 检查是否包含JSON数据
                items = []
                need_more_info = True
                reply = content
                
                if '```json' in content:
                    # 提取JSON部分
                    try:
                        json_part = content.split('```json')[1].split('```')[0].strip()
                        import json
                        parsed = json.loads(json_part)
                        
                        # 校验数据
                        is_valid, error_msg, validated_data = OCRResultValidator.validate_ocr_response(parsed)
                        
                        if is_valid and validated_data['valid'] > 0:
                            items = validated_data['items']
                            need_more_info = False
                            log(f"[AI对话] 提取到 {len(items)} 个有效物品")
                        else:
                            log(f"[AI对话] 数据校验失败: {error_msg}")
                        
                        # 移除JSON部分，只保留文字回复
                        reply = content.split('```json')[0].strip()
                        
                    except Exception as e:
                        log(f"[AI对话] JSON解析失败: {e}")
                
                return {
                    'reply': reply,
                    'items': items,
                    'need_more_info': need_more_info,
                    'raw_response': content
                }
            else:
                # 解析错误信息
                error_msg = response.text
                try:
                    error_json = response.json()
                    if 'error' in error_json:
                        error_detail = error_json['error']
                        if isinstance(error_detail, dict):
                            error_msg = error_detail.get('message', error_msg)
                            error_type = error_detail.get('type', '')
                            
                            # 提供更友好的错误提示
                            if error_type == 'bad_response_status_code':
                                error_msg = '后端模型服务不可用，请检查API配置或稍后重试'
                            elif 'rate_limit' in error_msg.lower():
                                error_msg = 'API调用频率超限，请稍后重试'
                            elif 'invalid_api_key' in error_msg.lower():
                                error_msg = 'API密钥无效，请检查配置'
                        else:
                            error_msg = str(error_detail)
                except:
                    pass
                
                raise Exception(f"API调用失败 ({response.status_code}): {error_msg}")
                
        except Exception as e:
            log(f"[AI对话] 错误: {e}")
            raise Exception(f"AI对话失败: {str(e)}")
    
    @staticmethod
    def parse_ocr_text(text: str, api_base: str, api_key: str, model: str) -> dict:
        """使用AI解析OCR识别的文字
        
        Args:
            text: OCR识别的文字
            api_base: API地址
            api_key: API密钥
            model: 模型名称
            
        Returns:
            解析结果 {"items": [...], "raw_response": "..."}
        """
        from app.utils.validators import AIPromptBuilder, OCRResultValidator
        
        try:
            # 构建提示词
            prompt = AIPromptBuilder.build_ocr_parse_prompt(text)

            # 调用API
            url = f"{api_base.rstrip('/')}/chat/completions"
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': model,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.1,  # 降低温度，提高准确性和一致性
                'max_tokens': 2000
            }
            
            log(f"[AI解析] 调用API: {url}")
            log(f"[AI解析] 模型: {model}")
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                log(f"[AI解析] 原始响应: {content[:200]}...")
                
                # 提取JSON部分
                import json
                json_str = content.strip()
                
                # 移除可能的markdown代码块标记
                if '```json' in json_str:
                    json_str = json_str.split('```json')[1].split('```')[0].strip()
                elif '```' in json_str:
                    json_str = json_str.split('```')[1].split('```')[0].strip()
                
                # 解析JSON
                try:
                    parsed = json.loads(json_str)
                except json.JSONDecodeError as e:
                    log(f"[AI解析] JSON解析失败: {e}")
                    log(f"[AI解析] 尝试解析的内容: {json_str}")
                    raise Exception(f'AI返回的不是有效的JSON格式: {str(e)}')
                
                # 校验数据
                is_valid, error_msg, validated_data = OCRResultValidator.validate_ocr_response(parsed)
                
                if not is_valid:
                    raise Exception(f'AI返回的数据格式不正确: {error_msg}')
                
                log(f"[AI解析] 校验通过，有效物品: {validated_data['valid']}/{validated_data['total']}")
                
                return {
                    'items': validated_data['items'],
                    'errors': validated_data.get('errors', []),
                    'raw_response': content
                }
            else:
                raise Exception(f"API调用失败: {response.status_code} - {response.text}")
                
        except Exception as e:
            log(f"[AI解析] 错误: {e}")
            raise Exception(f"AI解析失败: {str(e)}")
    
    @staticmethod
    def recognize_image_with_vision(base64_data: str, api_base: str, api_key: str, model: str) -> dict:
        """使用视觉模型直接识别图片
        
        Args:
            base64_data: base64编码的图片数据
            api_base: API地址
            api_key: API密钥
            model: 视觉模型名称
            
        Returns:
            识别结果 {"items": [...], "raw_response": "..."}
        """
        from app.utils.validators import AIPromptBuilder, OCRResultValidator
        
        try:
            # 确保base64数据格式正确
            if not base64_data.startswith('data:image'):
                base64_data = f'data:image/jpeg;base64,{base64_data}'
            
            # 构建提示词
            prompt = AIPromptBuilder.build_vision_parse_prompt()

            # 调用API
            url = f"{api_base.rstrip('/')}/chat/completions"
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': model,
                'messages': [
                    {
                        'role': 'user',
                        'content': [
                            {'type': 'text', 'text': prompt},
                            {'type': 'image_url', 'image_url': {'url': base64_data}}
                        ]
                    }
                ],
                'temperature': 0.1,  # 降低温度，提高准确性
                'max_tokens': 2000
            }
            
            log(f"[视觉识别] 调用API: {url}")
            log(f"[视觉识别] 模型: {model}")
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                log(f"[视觉识别] 原始响应: {content[:200]}...")
                
                # 提取JSON部分
                import json
                json_str = content.strip()
                
                if '```json' in json_str:
                    json_str = json_str.split('```json')[1].split('```')[0].strip()
                elif '```' in json_str:
                    json_str = json_str.split('```')[1].split('```')[0].strip()
                
                # 解析JSON
                try:
                    parsed = json.loads(json_str)
                except json.JSONDecodeError as e:
                    log(f"[视觉识别] JSON解析失败: {e}")
                    log(f"[视觉识别] 尝试解析的内容: {json_str}")
                    raise Exception(f'AI返回的不是有效的JSON格式: {str(e)}')
                
                # 校验数据
                is_valid, error_msg, validated_data = OCRResultValidator.validate_ocr_response(parsed)
                
                if not is_valid:
                    raise Exception(f'AI返回的数据格式不正确: {error_msg}')
                
                log(f"[视觉识别] 校验通过，有效物品: {validated_data['valid']}/{validated_data['total']}")
                
                return {
                    'items': validated_data['items'],
                    'errors': validated_data.get('errors', []),
                    'raw_response': content
                }
            else:
                raise Exception(f"API调用失败: {response.status_code} - {response.text}")
                
        except Exception as e:
            log(f"[视觉识别] 错误: {e}")
            raise Exception(f"视觉识别失败: {str(e)}")


# 全局OCR服务实例
ocr_service = OCRService()
