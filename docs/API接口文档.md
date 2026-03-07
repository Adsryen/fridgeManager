# 🔌 冰箱管理系统 - 后端接口文档

> 完整的 RESTful API 接口清单和使用说明

---

## � 接口总览

| 分类 | 接口数量 | 说明 |
|------|---------|------|
| 🔐 认证接口 | 10 | 用户注册、登录、密码管理等 |
| 📦 物品管理接口 | 11 | 物品增删改查、模式切换等 |
| 👑 管理员接口 | 12 | 用户管理、系统设置、数据维护等 |
| ⚙️ 用户设置接口 | 2 | 个人偏好设置 |
| **总计** | **35** | **完整的后端 API 体系** |

---

## 📋 目录

- [接口总览](#接口总览)
- [接口清单表](#接口清单表)
- [认证接口](#认证接口)
- [物品管理接口](#物品管理接口)
- [管理员接口](#管理员接口)
- [用户设置接口](#用户设置接口)
- [数据结构说明](#数据结构说明)
- [错误码说明](#错误码说明)

---

## 📑 接口清单表

### 🔐 认证接口 (10个)
```
POST   /register              - 用户注册
POST   /login                 - 用户登录
GET    /logout                - 用户登出
POST   /check-username        - 检查用户名是否可用
POST   /check-email           - 检查邮箱是否可用
POST   /change-password       - 修改密码
POST   /update-profile        - 更新个人资料
POST   /forgot-password       - 发送密码重置邮件
POST   /reset-password        - 重置密码
GET    /profile               - 个人资料页面
```

### 📦 物品管理接口 (11个)
```
POST   /insert                - 添加物品
POST   /search                - 搜索物品
POST   /total                 - 获取所有物品
POST   /getone/<_id>          - 获取单个物品详情
POST   /update                - 更新物品
POST   /delete                - 删除物品
POST   /switch-mode           - 切换公共/私人冰箱模式
POST   /switch-user           - 管理员切换查看用户
GET    /get-current-mode      - 获取当前查看模式
GET    /get-users-list        - 获取用户列表(管理员)
GET    /get-system-settings   - 获取系统设置
```

**说明**: 
- 物品筛选(按位置、类别、过期状态)统一使用 `/total` 获取所有数据后在前端筛选
- 这样可以减少API数量,提高前端灵活性

### 👑 管理员接口 (12个)
```
GET    /admin/dashboard                        - 管理员仪表板
GET    /admin/users                            - 用户管理页面
GET    /admin/user/<user_id>                   - 用户详情页面
POST   /admin/user/<user_id>/toggle-status    - 切换用户激活状态
POST   /admin/user/<user_id>/toggle-admin     - 切换管理员权限
POST   /admin/user/<user_id>/delete           - 删除用户
GET    /admin/stats                            - 获取统计数据
GET    /admin/settings                         - 系统设置页面
POST   /admin/settings/save                    - 保存系统设置
POST   /admin/maintenance/clean-expired        - 清理过期物品
GET    /admin/maintenance/backup               - 备份数据库
GET    /admin/maintenance/logs                 - 查看系统日志
```

### ⚙️ 用户设置接口 (2个)
```
GET    /settings/             - 用户设置页面
POST   /settings/update       - 更新用户设置
```

---

## 🔐 认证接口

### 1. 用户注册
**端点**: `POST /register`

**描述**: 创建新用户账号

**请求参数**:
```json
{
  "username": "string (3-20字符，字母/数字/下划线/中文)",
  "email": "string (有效邮箱格式)",
  "password": "string (最少6位，必须包含字母和数字)"
}
```

**响应**:
- 成功 (200):
```json
{
  "success": true,
  "message": "注册成功"
}
```
- 失败 (400/403):
```json
{
  "error": "错误信息"
}
```

**注意事项**:
- 系统可能禁用注册功能
- 注册成功后自动登录
- 用户名和邮箱不能重复

---

### 2. 用户登录
**端点**: `POST /login`

**描述**: 用户身份验证

**请求参数**:
```json
{
  "username": "string",
  "password": "string"
}
```

**响应**:
- 成功 (200):
```json
{
  "success": true,
  "message": "登录成功"
}
```
- 失败 (400/401/403/429):
```json
{
  "error": "错误信息"
}
```

**注意事项**:
- 30分钟内失败次数超过限制(默认5次)将被锁定
- 记录登录日志(IP、User-Agent)
- 检查账号是否被禁用

---

### 3. 用户登出
**端点**: `GET /logout`

**描述**: 清除用户会话

**响应**: 重定向到首页

---

### 4. 检查用户名可用性
**端点**: `POST /check-username`

**请求参数**:
```json
{
  "username": "string"
}
```

**响应**:
```json
{
  "available": true/false,
  "message": "提示信息"
}
```

---

### 5. 检查邮箱可用性
**端点**: `POST /check-email`

**请求参数**:
```json
{
  "email": "string"
}
```

**响应**:
```json
{
  "available": true/false,
  "message": "提示信息"
}
```

---

### 6. 修改密码
**端点**: `POST /change-password`

**权限**: 需要登录

**请求参数**:
```json
{
  "old_password": "string",
  "new_password": "string"
}
```

**响应**:
```json
{
  "success": true,
  "message": "密码修改成功"
}
```

---

### 7. 更新个人资料
**端点**: `POST /update-profile`

**权限**: 需要登录

**请求参数**:
```json
{
  "email": "string"
}
```

**响应**:
```json
{
  "success": true,
  "message": "资料更新成功"
}
```

---

### 8. 忘记密码
**端点**: `POST /forgot-password`

**请求参数**:
```json
{
  "email": "string"
}
```

**响应**:
```json
{
  "success": true,
  "message": "重置链接已发送到您的邮箱"
}
```

**注意事项**:
- 为安全考虑，即使邮箱不存在也返回成功
- 发送包含重置令牌的邮件

---

### 9. 重置密码
**端点**: `POST /reset-password`

**请求参数**:
```json
{
  "token": "string (重置令牌)",
  "password": "string (新密码)"
}
```

**响应**:
```json
{
  "success": true,
  "message": "密码重置成功，请使用新密码登录"
}
```

---

### 10. 个人资料页面
**端点**: `GET /profile`

**权限**: 需要登录

**响应**: 返回个人资料页面 HTML

---

## 📦 物品管理接口

### 1. 添加物品
**端点**: `POST /insert`

**请求参数**:
```json
{
  "itemName": "string (物品名称)",
  "itemDate": "string (YYYY-MM-DD)",
  "itemPlace": "string (cold/frozer/room)",
  "itemNum": "integer (数量)",
  "itemType": "string (类别)"
}
```

**物品类别**:
- `vegetable` - 蔬菜
- `fruit` - 水果
- `seafood` - 海鲜
- `meat` - 肉类
- `beverage` - 饮料
- `diary` - 乳制品
- `egg` - 蛋类
- `bread` - 面包
- `frozen` - 冷冻食品
- `sauce` - 调味料
- `snack` - 零食
- `other` - 其他

**响应**: 重定向到首页

**注意事项**:
- 检查用户物品数量限制
- 游客和登录用户数据隔离

---

### 2. 搜索物品
**端点**: `POST /search`

**请求参数**:
```json
{
  "text": "string (搜索关键词)"
}
```

**响应**:
```json
[
  {
    "_id": "string",
    "Name": "string",
    "ExpireDate": "ISO 8601 日期",
    "Place": "string",
    "Num": integer,
    "Type": "string"
  }
]
```

---

### 3. 获取所有物品
**端点**: `POST /total`

**描述**: 获取当前用户的所有物品,前端可根据需要进行筛选(按位置、类别、过期状态等)

**响应**:
```json
[
  {
    "_id": "string",
    "Name": "string",
    "ExpireDate": "ISO 8601 日期",
    "Place": "string (cold/frozer/room)",
    "Num": integer,
    "Type": "string"
  }
]
```

---

### 4. 获取单个物品
**端点**: `POST /getone/<_id>`

**参数**:
- `_id`: 物品ID

**响应**:
```json
[
  {
    "_id": "string",
    "Name": "string",
    "ExpireDate": "ISO 8601 日期",
    "Place": "string",
    "Num": integer,
    "Type": "string"
  }
]
```

---

### 5. 更新物品
**端点**: `POST /update`

**请求参数**:
```json
{
  "itemId": "string",
  "itemName": "string (可选)",
  "itemDate": "string (可选)",
  "itemPlace": "string (可选)",
  "itemNum": "integer (可选)",
  "itemType": "string (可选)"
}
```

**响应**:
```json
{
  "success": true,
  "message": "更新成功"
}
```

---

### 6. 删除物品
**端点**: `POST /delete`

**请求参数**:
```json
{
  "itemId": "string"
}
```

**响应**:
```json
{
  "success": true,
  "message": "删除成功"
}
```

---

### 7. 切换查看模式
**端点**: `POST /switch-mode`

**请求参数**:
```json
{
  "mode": "public/private"
}
```

**响应**:
```json
{
  "success": true,
  "mode": "string"
}
```

**注意事项**:
- `public`: 查看公共冰箱
- `private`: 查看私人冰箱

---

### 8. 切换查看用户 (管理员)
**端点**: `POST /switch-user`

**权限**: 管理员

**请求参数**:
```json
{
  "user_id": "string"
}
```

**响应**:
```json
{
  "success": true,
  "user_id": "string"
}
```

---

### 9. 获取当前模式
**端点**: `GET /get-current-mode`

**响应**:
```json
{
  "is_logged_in": boolean,
  "is_admin": boolean,
  "current_user_id": "string",
  "effective_user_id": "string",
  "is_public": boolean,
  "view_user_id": "string"
}
```

---

### 10. 获取用户列表 (管理员)
**端点**: `GET /get-users-list`

**权限**: 管理员

**响应**:
```json
[
  {
    "_id": "string",
    "username": "string",
    "email": "string"
  }
]
```

---

### 11. 获取系统设置
**端点**: `GET /get-system-settings`

**响应**:
```json
{
  "default_expiry_warning_days": integer,
  "max_items_per_user": integer
}
```

---

## 👑 管理员接口

### 1. 管理员仪表板
**端点**: `GET /admin/dashboard`

**权限**: 管理员

**响应**: 返回仪表板页面 HTML

---

### 2. 用户管理页面
**端点**: `GET /admin/users`

**权限**: 管理员

**响应**: 返回用户列表页面 HTML

---

### 3. 用户详情
**端点**: `GET /admin/user/<user_id>`

**权限**: 管理员

**响应**: 返回用户详情页面 HTML

---

### 4. 切换用户激活状态
**端点**: `POST /admin/user/<user_id>/toggle-status`

**权限**: 管理员

**响应**:
```json
{
  "success": true,
  "message": "状态已更新"
}
```

---

### 5. 切换管理员权限
**端点**: `POST /admin/user/<user_id>/toggle-admin`

**权限**: 管理员

**响应**:
```json
{
  "success": true,
  "message": "权限已更新"
}
```

---

### 6. 删除用户
**端点**: `POST /admin/user/<user_id>/delete`

**权限**: 管理员

**响应**:
```json
{
  "success": true,
  "message": "用户已删除"
}
```

---

### 7. 获取统计数据
**端点**: `GET /admin/stats`

**权限**: 管理员

**响应**:
```json
{
  "total_users": integer,
  "active_users": integer,
  "total_items": integer,
  "expired_items": integer,
  "expiring_soon": integer
}
```

---

### 8. 系统设置页面
**端点**: `GET /admin/settings`

**权限**: 管理员

**响应**: 返回系统设置页面 HTML

---

### 9. 保存系统设置
**端点**: `POST /admin/settings/save`

**权限**: 管理员

**请求参数**:
```json
{
  "category": "string",
  "settings": {
    "key": "value"
  }
}
```

**可配置项**:
- `system_name`: 系统名称
- `allow_registration`: 是否允许注册
- `min_password_length`: 最小密码长度
- `max_login_attempts`: 最大登录尝试次数
- `enable_login_log`: 是否启用登录日志
- `max_items_per_user`: 每用户最大物品数
- `default_expiry_warning_days`: 默认过期提醒天数

**响应**:
```json
{
  "success": true,
  "message": "设置已保存"
}
```

---

### 10. 清理过期物品
**端点**: `POST /admin/maintenance/clean-expired`

**权限**: 管理员

**响应**:
```json
{
  "success": true,
  "count": integer
}
```

---

### 11. 备份数据库
**端点**: `GET /admin/maintenance/backup`

**权限**: 管理员

**响应**: 下载数据库文件

---

### 12. 查看系统日志
**端点**: `GET /admin/maintenance/logs`

**权限**: 管理员

**响应**: 返回日志页面 HTML

---

## ⚙️ 用户设置接口

### 1. 用户设置页面
**端点**: `GET /settings/`

**权限**: 需要登录

**响应**: 返回用户设置页面 HTML

---

### 2. 更新用户设置
**端点**: `POST /settings/update`

**权限**: 需要登录

**请求参数**:
```json
{
  "notify_expiring": "on/off",
  "notify_days": integer,
  "items_per_page": integer,
  "default_view": "string",
  "profile_public": "on/off"
}
```

**响应**:
```json
{
  "success": true,
  "message": "设置已保存"
}
```

---

## 📊 数据结构说明

### 用户对象
```json
{
  "_id": "string (唯一标识)",
  "username": "string (用户名)",
  "email": "string (邮箱)",
  "password_hash": "string (密码哈希)",
  "is_admin": boolean,
  "is_active": boolean,
  "created_at": "ISO 8601 日期",
  "updated_at": "ISO 8601 日期"
}
```

### 物品对象
```json
{
  "_id": "string (唯一标识)",
  "user_id": "string (所属用户ID)",
  "Name": "string (物品名称)",
  "ExpireDate": "ISO 8601 日期",
  "Place": "string (cold/frozer/room)",
  "Num": integer (数量),
  "Type": "string (类别)"
}
```

### 登录日志对象
```json
{
  "_id": "string",
  "user_id": "string",
  "username": "string",
  "success": boolean,
  "ip_address": "string",
  "user_agent": "string",
  "error_message": "string",
  "created_at": "ISO 8601 日期"
}
```

---

## ❌ 错误码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未授权(未登录或认证失败) |
| 403 | 禁止访问(权限不足或账号被禁用) |
| 404 | 资源不存在 |
| 429 | 请求过于频繁(登录尝试次数过多) |
| 500 | 服务器内部错误 |

---

## 🔒 权限说明

### 公开接口
- 注册、登录、忘记密码、重置密码
- 检查用户名/邮箱可用性

### 需要登录
- 个人资料、修改密码、更新资料
- 物品管理(增删改查)
- 用户设置

### 需要管理员权限
- 所有 `/admin/*` 接口
- 切换查看用户
- 获取用户列表

---

## 📝 使用示例

### JavaScript (Fetch API)

```javascript
// 登录
fetch('/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    username: 'testuser',
    password: 'password123'
  })
})
.then(response => response.json())
.then(data => console.log(data));

// 添加物品
fetch('/insert', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    itemName: '苹果',
    itemDate: '2024-12-31',
    itemPlace: 'cold',
    itemNum: '5',
    itemType: 'fruit'
  })
});

// 获取所有物品
fetch('/total', {
  method: 'POST'
})
.then(response => response.json())
.then(items => console.log(items));
```

---

## 📌 注意事项

1. **会话管理**: 使用 Flask Session，需要配置 SECRET_KEY
2. **CSRF 保护**: 建议在生产环境启用 CSRF 保护
3. **速率限制**: 登录接口有失败次数限制
4. **数据隔离**: 用户只能访问自己的数据(管理员除外)
5. **日期格式**: 前端使用 `YYYY-MM-DD`，后端存储为 ISO 8601
6. **编码**: 所有文件使用 UTF-8 编码

---

**文档版本**: 1.0  
**最后更新**: 2024-12-31  
**维护者**: Adsryen
