# -*- coding: utf-8 -*-
"""冰箱服务"""
from datetime import datetime
from app.models import Fridge


class FridgeService:
    """冰箱业务逻辑"""
    
    def __init__(self, db):
        self.db = db
    
    def create_fridge(self, user_id: str, name: str) -> Fridge:
        """创建冰箱"""
        fridge = Fridge(
            user_id=user_id,
            name=name
        )
        
        self.db.fridge.insert_one(fridge.to_dict())
        return fridge
    
    def get_user_fridges(self, user_id: str) -> list[dict]:
        """获取用户所有冰箱"""
        return self.db.fridge.find({'user_id': user_id})
    
    def get_fridge(self, fridge_id: str, user_id: str) -> dict | None:
        """获取单个冰箱"""
        return self.db.fridge.find_one({'_id': fridge_id, 'user_id': user_id})
    
    def update_fridge(self, fridge_id: str, user_id: str, name: str) -> bool:
        """更新冰箱名称"""
        result = self.db.fridge.update_one(
            {'_id': fridge_id, 'user_id': user_id},
            {'$set': {
                'name': name,
                'updated_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
            }}
        )
        return result.modified_count > 0
    
    def delete_fridge(self, fridge_id: str, user_id: str) -> bool:
        """删除冰箱"""
        result = self.db.fridge.delete_one({'_id': fridge_id, 'user_id': user_id})
        return result.deleted_count > 0
    
    def delete_fridge_items(self, fridge_id: str) -> int:
        """删除冰箱中的所有物品，返回删除的物品数量"""
        result = self.db.item.delete_many({'fridge_id': fridge_id})
        return result.deleted_count
    
    def get_fridge_item_count(self, fridge_id: str) -> int:
        """获取冰箱中的物品数量"""
        items = self.db.item.find({'fridge_id': fridge_id})
        return len(items)
    
    def can_access_fridge(self, fridge_id: str, user_id: str) -> bool:
        """检查用户是否可以访问冰箱"""
        try:
            # 公共冰箱所有人都可以访问
            if fridge_id == 'public':
                return True
            
            # 检查是否是冰箱所有者
            fridge = self.db.fridge.find_one({'_id': fridge_id, 'user_id': user_id})
            if fridge:
                return True
            
            # 检查是否是家庭共享冰箱
            from app.services.family_service import FamilyService
            family_service = FamilyService(self.db)
            
            # 获取用户所属的家庭
            families = family_service.get_user_families(user_id)
            for family in families:
                family_fridges = family_service.get_family_shared_fridges(family['_id'])
                for shared_fridge in family_fridges:
                    if shared_fridge['_id'] == fridge_id:
                        return True
            
            return False
        except Exception as e:
            print(f"[错误] 检查冰箱访问权限失败: {str(e)}")
            import traceback
            traceback.print_exc()
            # 出错时返回False，拒绝访问
            return False
    
    def can_edit_fridge(self, fridge_id: str, user_id: str) -> bool:
        """检查用户是否可以编辑冰箱（添加、删除物品）"""
        try:
            # 公共冰箱所有人都可以编辑
            if fridge_id == 'public':
                return True
            
            # 检查是否是冰箱所有者
            fridge = self.db.fridge.find_one({'_id': fridge_id, 'user_id': user_id})
            if fridge:
                return True
            
            # 检查是否是可编辑的家庭共享冰箱
            from app.services.family_service import FamilyService
            family_service = FamilyService(self.db)
            
            # 获取用户所属的家庭
            families = family_service.get_user_families(user_id)
            for family in families:
                family_fridges = family_service.get_family_shared_fridges(family['_id'])
                for shared_fridge in family_fridges:
                    if shared_fridge['_id'] == fridge_id:
                        # 检查是否允许家庭成员编辑
                        permission = shared_fridge.get('permission', {})
                        return permission.get('is_editable_by_family', False)
            
            return False
        except Exception as e:
            print(f"[错误] 检查冰箱编辑权限失败: {str(e)}")
            import traceback
            traceback.print_exc()
            # 出错时返回False，拒绝编辑
            return False
