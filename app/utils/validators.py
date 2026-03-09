# -*- coding: utf-8 -*-
"""数据校验工具"""
from datetime import datetime, timedelta
import re


class ItemValidator:
    """物品数据校验器"""
    
    # 有效的物品分类
    VALID_PLACES = ['冷冻', '冷藏', '常温', '未分类']
    
    # 有效的物品类型
    VALID_TYPES = ['肉类', '蔬菜', '水果', '饮料', '调料', '速食', '其他']
    
    # 有效的单位
    VALID_UNITS = ['个', '瓶', '盒', '袋', '罐', '包', '斤', '克', '千克', '升', '毫升', '片', '条', '根', '只', '份']
    
    @staticmethod
    def validate_item_data(data: dict) -> tuple[bool, str, dict]:
        """校验物品数据
        
        Args:
            data: 待校验的物品数据
            
        Returns:
            (是否有效, 错误信息, 清洗后的数据)
        """
        try:
            cleaned_data = {}
            
            # 1. 校验物品名称
            name = data.get('name', '').strip()
            if not name:
                return False, '物品名称不能为空', {}
            
            if len(name) > 50:
                return False, '物品名称过长（最多50字符）', {}
            
            # 过滤特殊字符
            name = re.sub(r'[<>\"\'\\]', '', name)
            cleaned_data['name'] = name
            
            # 2. 校验数量
            quantity = data.get('quantity', 1)
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    return False, '数量必须大于0', {}
                if quantity > 9999:
                    return False, '数量过大（最多9999）', {}
                cleaned_data['quantity'] = quantity
            except (ValueError, TypeError):
                return False, '数量必须是有效的整数', {}
            
            # 3. 校验单位
            unit = data.get('unit', '个').strip()
            if unit not in ItemValidator.VALID_UNITS:
                # 尝试映射常见单位
                unit_mapping = {
                    '瓶子': '瓶', '盒子': '盒', '袋子': '袋',
                    'kg': '千克', 'g': '克', 'ml': '毫升', 'l': '升',
                    '公斤': '千克', '毫克': '克'
                }
                unit = unit_mapping.get(unit, '个')
            cleaned_data['unit'] = unit
            
            # 4. 校验过期日期
            expire_date = data.get('expire_date', '')
            if expire_date:
                # 尝试解析日期
                parsed_date = ItemValidator._parse_date(expire_date)
                if not parsed_date:
                    return False, f'无效的日期格式: {expire_date}', {}
                
                # 检查日期是否合理（不能是过去太久或未来太远）
                today = datetime.now().date()
                min_date = today - timedelta(days=30)  # 最早30天前（允许添加刚过期的物品）
                max_date = today + timedelta(days=3650)  # 最晚10年后
                
                if parsed_date < min_date:
                    # 如果日期太早，可能是年份错误，尝试修正
                    # 例如：2024-12-31 可能应该是 2026-12-31
                    if parsed_date.year < today.year:
                        # 尝试使用当前年份
                        try:
                            corrected_date = parsed_date.replace(year=today.year)
                            if corrected_date >= min_date and corrected_date <= max_date:
                                parsed_date = corrected_date
                                print(f"[数据校验] 日期年份已自动修正: {expire_date} -> {parsed_date}")
                            else:
                                # 尝试下一年
                                corrected_date = parsed_date.replace(year=today.year + 1)
                                if corrected_date <= max_date:
                                    parsed_date = corrected_date
                                    print(f"[数据校验] 日期年份已自动修正: {expire_date} -> {parsed_date}")
                                else:
                                    return False, f'过期日期过早: {expire_date}', {}
                        except:
                            return False, f'过期日期过早: {expire_date}', {}
                    else:
                        return False, f'过期日期过早: {expire_date}', {}
                
                if parsed_date > max_date:
                    return False, '过期日期过远（不能晚于10年后）', {}
                
                cleaned_data['expire_date'] = parsed_date.strftime('%Y-%m-%d')
            else:
                # 如果没有过期日期，设置为30天后
                default_date = datetime.now().date() + timedelta(days=30)
                cleaned_data['expire_date'] = default_date.strftime('%Y-%m-%d')
            
            # 5. 校验分类
            place = data.get('place', '未分类').strip()
            if place not in ItemValidator.VALID_PLACES:
                # 尝试智能匹配
                place_mapping = {
                    '冷冻室': '冷冻', '冷冻层': '冷冻',
                    '冷藏室': '冷藏', '冷藏层': '冷藏',
                    '常温区': '常温', '室温': '常温'
                }
                place = place_mapping.get(place, '未分类')
            cleaned_data['place'] = place
            
            # 6. 校验类型
            item_type = data.get('type', '其他').strip()
            if item_type not in ItemValidator.VALID_TYPES:
                # 尝试智能匹配
                type_mapping = {
                    '肉': '肉类', '肉食': '肉类', '荤菜': '肉类',
                    '菜': '蔬菜', '青菜': '蔬菜',
                    '果': '水果', '水果类': '水果',
                    '饮品': '饮料', '饮': '饮料',
                    '调味': '调料', '调味品': '调料',
                    '方便面': '速食', '快餐': '速食'
                }
                item_type = type_mapping.get(item_type, '其他')
            cleaned_data['type'] = item_type
            
            # 7. 校验备注（可选）
            note = data.get('note', '').strip()
            if note:
                if len(note) > 200:
                    return False, '备注过长（最多200字符）', {}
                note = re.sub(r'[<>\"\'\\]', '', note)
                cleaned_data['note'] = note
            
            return True, '', cleaned_data
            
        except Exception as e:
            return False, f'数据校验失败: {str(e)}', {}
    
    @staticmethod
    def _parse_date(date_str: str) -> datetime.date:
        """解析日期字符串
        
        支持的格式：
        - 2024-12-31
        - 2024/12/31
        - 20241231
        - 2024.12.31
        - 2024年12月31日
        """
        if not date_str:
            return None
        
        date_str = str(date_str).strip()
        
        # 格式1: YYYY-MM-DD
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            pass
        
        # 格式2: YYYY/MM/DD
        try:
            return datetime.strptime(date_str, '%Y/%m/%d').date()
        except:
            pass
        
        # 格式3: YYYYMMDD
        try:
            return datetime.strptime(date_str, '%Y%m%d').date()
        except:
            pass
        
        # 格式4: YYYY.MM.DD
        try:
            return datetime.strptime(date_str, '%Y.%m.%d').date()
        except:
            pass
        
        # 格式5: YYYY年MM月DD日
        try:
            date_str = date_str.replace('年', '-').replace('月', '-').replace('日', '')
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            pass
        
        return None
    
    @staticmethod
    def validate_batch_items(items: list) -> tuple[list, list]:
        """批量校验物品数据
        
        Args:
            items: 物品数据列表
            
        Returns:
            (有效的物品列表, 错误信息列表)
        """
        valid_items = []
        errors = []
        
        for i, item in enumerate(items):
            is_valid, error_msg, cleaned_data = ItemValidator.validate_item_data(item)
            if is_valid:
                valid_items.append(cleaned_data)
            else:
                errors.append(f'第{i+1}个物品: {error_msg}')
        
        return valid_items, errors


class OCRResultValidator:
    """OCR识别结果校验器"""
    
    @staticmethod
    def validate_ocr_response(data: dict) -> tuple[bool, str, dict]:
        """校验OCR API响应数据
        
        Args:
            data: OCR API返回的数据
            
        Returns:
            (是否有效, 错误信息, 标准化的数据)
        """
        try:
            # 检查必需字段
            if 'items' not in data:
                return False, 'OCR响应缺少items字段', {}
            
            items = data.get('items', [])
            if not isinstance(items, list):
                return False, 'items字段必须是数组', {}
            
            # 校验每个物品
            valid_items, errors = ItemValidator.validate_batch_items(items)
            
            if not valid_items and items:
                # 所有物品都无效
                return False, f'所有物品数据无效: {"; ".join(errors)}', {}
            
            result = {
                'items': valid_items,
                'errors': errors,
                'total': len(items),
                'valid': len(valid_items),
                'invalid': len(errors)
            }
            
            return True, '', result
            
        except Exception as e:
            return False, f'OCR结果校验失败: {str(e)}', {}


class AIPromptBuilder:
    """AI提示词构建器"""
    
    @staticmethod
    def build_ocr_parse_prompt(ocr_text: str) -> str:
        """构建OCR文字解析提示词"""
        return f"""你是一个食品物品信息提取助手。请从以下OCR识别的文字中提取食品物品信息。

OCR识别的文字：
{ocr_text}

请严格按照以下JSON格式返回，不要添加任何其他文字或说明：

{{
  "items": [
    {{
      "name": "物品名称（必填，字符串，最多50字符）",
      "quantity": 数量（必填，正整数，默认1）,
      "unit": "单位（必填，字符串，如：个/瓶/盒/袋/斤/克等）",
      "expire_date": "过期日期（必填，格式：YYYY-MM-DD）",
      "place": "存放位置（选填，可选值：冷冻/冷藏/常温/未分类）",
      "type": "物品类型（选填，可选值：肉类/蔬菜/水果/饮料/调料/速食/其他）",
      "note": "备注（选填，字符串，最多200字符）"
    }}
  ]
}}

重要规则：
1. 如果文字中包含生产日期和保质期，请计算出过期日期
2. 如果没有明确的过期日期，请根据常识估算（如牛奶6个月，蔬菜7天等）
3. 数量必须是正整数，如果识别到"12盒"，quantity应为12，unit应为"盒"
4. 如果识别到多个物品，请在items数组中返回多个对象
5. 如果无法识别到有效的物品信息，返回空数组：{{"items": []}}
6. 只返回JSON，不要包含```json```标记或其他说明文字

示例输入：蒙牛纯牛奶 250ml*12 生产日期:2024-01-15 保质期:6个月
示例输出：{{"items": [{{"name": "蒙牛纯牛奶", "quantity": 12, "unit": "盒", "expire_date": "2024-07-15", "place": "冷藏", "type": "饮料"}}]}}"""
    
    @staticmethod
    def build_vision_parse_prompt() -> str:
        """构建视觉模型识别提示词"""
        return """你是一个食品物品信息识别助手。请识别图片中的食品物品信息。

请严格按照以下JSON格式返回，不要添加任何其他文字或说明：

{
  "items": [
    {
      "name": "物品名称（必填，字符串，最多50字符）",
      "quantity": 数量（必填，正整数，默认1）,
      "unit": "单位（必填，字符串，如：个/瓶/盒/袋/斤/克等）",
      "expire_date": "过期日期（必填，格式：YYYY-MM-DD）",
      "place": "存放位置（选填，可选值：冷冻/冷藏/常温/未分类）",
      "type": "物品类型（选填，可选值：肉类/蔬菜/水果/饮料/调料/速食/其他）",
      "note": "备注（选填，字符串，最多200字符）"
    }
  ]
}

重要规则：
1. 识别图片中的文字信息（品牌、名称、日期等）
2. 如果能看到生产日期和保质期，请计算出过期日期
3. 如果没有明确的过期日期，请根据物品类型和常识估算
4. 数量必须是正整数，根据图片中的数量或包装规格判断
5. 根据物品外观和包装判断存放位置（如：冷冻食品→冷冻，牛奶→冷藏，饼干→常温）
6. 如果识别到多个物品，请在items数组中返回多个对象
7. 如果无法识别到有效的物品信息，返回空数组：{"items": []}
8. 只返回JSON，不要包含```json```标记或其他说明文字

示例输出：{"items": [{"name": "蒙牛纯牛奶", "quantity": 12, "unit": "盒", "expire_date": "2024-07-15", "place": "冷藏", "type": "饮料"}]}"""
