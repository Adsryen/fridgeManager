# -*- coding: utf-8 -*-
"""家庭服务"""
from datetime import datetime
from app.models import Family, FamilyMember, FridgePermission


class FamilyService:
    """家庭业务逻辑"""
    
    def __init__(self, db):
        self.db = db
    
    def create_family(self, name: str, creator_id: str) -> Family:
        """创建家庭"""
        family = Family(
            name=name,
            creator_id=creator_id
        )
        
        self.db.family.insert_one(family.to_dict())
        
        # 自动添加创建者为家庭成员
        member = FamilyMember(
            family_id=family._id,
            user_id=creator_id,
            role='creator'
        )
        self.db.family_member.insert_one(member.to_dict())
        
        return family
    
    def get_family_by_code(self, family_code: str) -> dict | None:
        """通过家庭编号获取家庭"""
        return self.db.family.find_one({'family_code': family_code})
    
    def get_family(self, family_id: str) -> dict | None:
        """获取家庭信息"""
        return self.db.family.find_one({'_id': family_id})
    
    def join_family(self, family_code: str, user_id: str) -> bool:
        """加入家庭"""
        # 查找家庭
        family = self.get_family_by_code(family_code)
        if not family:
            raise ValueError('家庭编号不存在')
        
        # 检查是否已经是成员
        existing = self.db.family_member.find_one({
            'family_id': family['_id'],
            'user_id': user_id
        })
        if existing:
            raise ValueError('您已经是该家庭的成员')
        
        # 添加成员
        member = FamilyMember(
            family_id=family['_id'],
            user_id=user_id,
            role='member'
        )
        self.db.family_member.insert_one(member.to_dict())
        return True
    
    def leave_family(self, family_id: str, user_id: str) -> bool:
        """离开家庭"""
        # 检查是否是创建者
        family = self.get_family(family_id)
        if family and family['creator_id'] == user_id:
            raise ValueError('创建者不能离开家庭，请先转让家庭或删除家庭')
        
        result = self.db.family_member.delete_one({
            'family_id': family_id,
            'user_id': user_id
        })
        return result.deleted_count > 0
    
    def get_user_families(self, user_id: str) -> list[dict]:
        """获取用户所在的所有家庭"""
        try:
            print(f"[调试] 开始查询用户 {user_id} 的家庭")
            members = list(self.db.family_member.find({'user_id': user_id}))
            print(f"[调试] 查询到的成员记录数: {len(members)}")
            
            families = []
            for member in members:
                print(f"[调试] 处理成员记录: {member}")
                family = self.get_family(member['family_id'])
                if family:
                    print(f"[调试] 找到家庭: {family['name']}")
                    # 计算家庭成员数量 - 使用SQLite兼容的方法
                    family_members = self.db.family_member.find({'family_id': family['_id']})
                    member_count = len(family_members)
                    print(f"[调试] 家庭成员数量: {member_count}")
                    family['member_count'] = member_count
                    family['role'] = member['role']
                    family['joined_at'] = member['joined_at']
                    families.append(family)
                else:
                    print(f"[调试] 未找到家庭 ID: {member['family_id']}")
            
            print(f"[调试] 最终返回的家庭数量: {len(families)}")
            return families
        except Exception as e:
            print(f"[调试] get_user_families 出错: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def get_family_members(self, family_id: str) -> list[dict]:
        """获取家庭所有成员"""
        # 获取家庭信息以确定创建者
        family = self.get_family(family_id)
        if not family:
            return []
        
        members = self.db.family_member.find({'family_id': family_id})
        result = []
        for member in members:
            user = self.db.user.find_one({'_id': member['user_id']})
            if user:
                result.append({
                    '_id': member['_id'],
                    'user_id': user['_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': member['role'],
                    'joined_at': member['joined_at'],
                    'is_owner': user['_id'] == family['creator_id']  # 添加是否为创建者的标识
                })
        return result
    
    def is_family_member(self, family_id: str, user_id: str) -> bool:
        """检查用户是否是家庭成员"""
        member = self.db.family_member.find_one({
            'family_id': family_id,
            'user_id': user_id
        })
        return member is not None
    
    def update_family(self, family_id: str, user_id: str, name: str) -> bool:
        """更新家庭名称（仅创建者和管理员）"""
        print(f"[调试] 更新家庭请求 - family_id: {family_id}, user_id: {user_id}, name: {name}")
        
        family = self.get_family(family_id)
        if not family:
            print(f"[调试] 家庭不存在: {family_id}")
            raise ValueError('家庭不存在')
        
        print(f"[调试] 找到家庭: {family['name']}, creator_id: {family['creator_id']}")
        
        # 检查是否是家庭创建者
        if family['creator_id'] == user_id:
            print(f"[调试] 用户是家庭创建者，允许修改")
            # 创建者可以直接修改
            result = self.db.family.update_one(
                {'_id': family_id},
                {'$set': {
                    'name': name,
                    'updated_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
                }}
            )
            print(f"[调试] 更新结果: {result.modified_count}")
            return result.modified_count > 0
        
        print(f"[调试] 用户不是创建者，检查管理员权限")
        # 检查是否是管理员
        member = self.db.family_member.find_one({
            'family_id': family_id,
            'user_id': user_id
        })
        
        print(f"[调试] 成员记录: {member}")
        
        if not member or member['role'] not in ['creator', 'admin']:
            print(f"[调试] 权限不足 - member: {member}")
            raise ValueError('只有创建者和管理员可以修改家庭信息')
        
        result = self.db.family.update_one(
            {'_id': family_id},
            {'$set': {
                'name': name,
                'updated_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
            }}
        )
        return result.modified_count > 0
    
    def delete_family(self, family_id: str, user_id: str) -> bool:
        """删除家庭（仅创建者）"""
        family = self.get_family(family_id)
        if not family:
            raise ValueError('家庭不存在')
        
        if family['creator_id'] != user_id:
            raise ValueError('只有创建者可以删除家庭')
        
        # 删除所有成员
        self.db.family_member.delete_many({'family_id': family_id})
        
        # 删除家庭
        result = self.db.family.delete_one({'_id': family_id})
        return result.deleted_count > 0
    
    def remove_member(self, family_id: str, user_id: str, target_user_id: str) -> bool:
        """移除家庭成员（仅创建者和管理员）"""
        family = self.get_family(family_id)
        if not family:
            raise ValueError('家庭不存在')
        
        # 检查操作者权限
        operator = self.db.family_member.find_one({
            'family_id': family_id,
            'user_id': user_id
        })
        
        if not operator or operator['role'] not in ['creator', 'admin']:
            raise ValueError('只有创建者和管理员可以移除成员')
        
        # 不能移除创建者
        if family['creator_id'] == target_user_id:
            raise ValueError('不能移除家庭创建者')
        
        result = self.db.family_member.delete_one({
            'family_id': family_id,
            'user_id': target_user_id
        })
        return result.deleted_count > 0
    
    def set_fridge_permission(self, fridge_id: str, is_family_shared: bool, 
                             is_editable_by_family: bool) -> bool:
        """设置冰箱权限"""
        print(f"[FamilyService] 设置冰箱权限 - 冰箱ID: {fridge_id}")
        print(f"[FamilyService] 家庭共享: {is_family_shared}, 允许编辑: {is_editable_by_family}")
        
        # 检查权限是否已存在
        existing = self.db.fridge_permission.find_one({'fridge_id': fridge_id})
        print(f"[FamilyService] 现有权限记录: {existing}")
        
        if existing:
            print(f"[FamilyService] 更新现有权限记录")
            result = self.db.fridge_permission.update_one(
                {'fridge_id': fridge_id},
                {'$set': {
                    'is_family_shared': is_family_shared,
                    'is_editable_by_family': is_editable_by_family,
                    'updated_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
                }}
            )
            print(f"[FamilyService] 更新结果: modified_count={result.modified_count}")
            return result.modified_count > 0
        else:
            print(f"[FamilyService] 创建新权限记录")
            permission = FridgePermission(
                fridge_id=fridge_id,
                is_family_shared=is_family_shared,
                is_editable_by_family=is_editable_by_family
            )
            result = self.db.fridge_permission.insert_one(permission.to_dict())
            print(f"[FamilyService] 创建结果: inserted_id={result.inserted_id}")
            return True
    
    def get_fridge_permission(self, fridge_id: str) -> dict | None:
        """获取冰箱权限"""
        print(f"[FamilyService] 获取冰箱权限 - 冰箱ID: {fridge_id}")
        permission = self.db.fridge_permission.find_one({'fridge_id': fridge_id})
        print(f"[FamilyService] 查询到的权限记录: {permission}")
        
        if not permission:
            # 返回默认权限
            default_permission = {
                'fridge_id': fridge_id,
                'is_family_shared': False,
                'is_editable_by_family': False
            }
            print(f"[FamilyService] 返回默认权限: {default_permission}")
            return default_permission
        
        print(f"[FamilyService] 返回现有权限: {permission}")
        return permission
    
    def get_family_shared_fridges(self, family_id: str) -> list[dict]:
        """获取家庭共享的所有冰箱"""
        # 获取家庭所有成员
        members = self.db.family_member.find({'family_id': family_id})
        user_ids = [m['user_id'] for m in members]
        
        # 获取所有成员的冰箱
        all_fridges = []
        for user_id in user_ids:
            fridges = self.db.fridge.find({'user_id': user_id})
            for fridge in fridges:
                permission = self.get_fridge_permission(fridge['_id'])
                if permission['is_family_shared']:
                    fridge['permission'] = permission
                    # 获取所有者信息
                    owner = self.db.user.find_one({'_id': user_id})
                    if owner:
                        fridge['owner_username'] = owner['username']
                    all_fridges.append(fridge)
        
        return all_fridges
    
    def can_access_fridge(self, fridge_id: str, user_id: str) -> bool:
        """检查用户是否可以访问冰箱"""
        # 获取冰箱信息
        fridge = self.db.fridge.find_one({'_id': fridge_id})
        if not fridge:
            return False
        
        # 如果是冰箱所有者
        if fridge['user_id'] == user_id:
            return True
        
        # 检查冰箱权限
        permission = self.get_fridge_permission(fridge_id)
        if not permission['is_family_shared']:
            return False
        
        # 检查是否在同一家庭
        owner_families = self.get_user_families(fridge['user_id'])
        user_families = self.get_user_families(user_id)
        
        owner_family_ids = {f['_id'] for f in owner_families}
        user_family_ids = {f['_id'] for f in user_families}
        
        return bool(owner_family_ids & user_family_ids)
    
    def can_edit_fridge(self, fridge_id: str, user_id: str) -> bool:
        """检查用户是否可以编辑冰箱"""
        # 获取冰箱信息
        fridge = self.db.fridge.find_one({'_id': fridge_id})
        if not fridge:
            return False
        
        # 如果是冰箱所有者
        if fridge['user_id'] == user_id:
            return True
        
        # 检查冰箱权限
        permission = self.get_fridge_permission(fridge_id)
        if not permission['is_family_shared'] or not permission['is_editable_by_family']:
            return False
        
        # 检查是否在同一家庭
        return self.can_access_fridge(fridge_id, user_id)
