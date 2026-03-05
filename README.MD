# 🧊 冰箱管理系统

> 智能冰箱库存管理系统，帮助你有效管理冰箱中的食材，减少浪费，提升生活品质！

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-green.svg)](https://www.sqlite.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0.0-purple.svg)](https://getbootstrap.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](./README_EN.md) | 中文

---

## 📋 目录

- [项目说明](#项目说明)
- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [API 文档](#api-文档)
- [项目结构](#项目结构)
- [测试](#测试)
- [许可证](#许可证)

## 项目说明

本项目基于 [hill0106/fridgeManager](https://github.com/hill0106/fridgeManager) 进行二次开发，在原有功能基础上新增了多用户支持和用户认证系统。

**原项目**：hill0106/fridgeManager - 冰箱管理大師

**主要改进**：
- ✅ 多用户支持 - 每个用户独立管理自己的冰箱
- ✅ 用户认证系统 - 注册、登录、密码加密
- ✅ 数据隔离 - 用户数据完全隔离
- ✅ 数据库优化 - 从 MongoDB 改为 SQLite，更轻量
- ✅ 性能提升 - 添加数据库索引
- ✅ 隐私保护 - 数据库文件不提交到 Git

## ✨ 功能特性

### 🎯 核心功能
- **👤 用户系统**：注册、登录、多用户数据隔离
- **📦 物品管理**：添加、编辑、删除冰箱物品
- **🔍 智能搜索**：按物品名称实时搜索
- **📅 过期追踪**：自动识别过期和即将过期的物品
- **🏷️ 分类管理**：12 种食材分类（蔬菜、水果、海鲜、肉类等）
- **📍 位置管理**：三种存储位置（冷藏、冷冻、常温）
- **📊 数据总览**：一目了然查看所有物品

### 🎨 用户体验
- **响应式设计**：适配各种屏幕尺寸
- **直观界面**：简洁美观的用户界面
- **实时反馈**：AJAX 驱动的无缝操作
- **图标支持**：Font Awesome 图标库

## 🛠 技术栈

### 后端
- **Python 3.12+**：主要编程语言
- **Flask 3.1.0**：Web 框架
- **SQLite 3**：轻量级数据库（无需额外安装）

### 前端
- **HTML5**：页面结构
- **CSS3**：样式设计
- **JavaScript (ES6)**：前端逻辑
- **jQuery 3.6.0**：DOM 操作
- **Bootstrap 5.0.0**：UI 框架
- **Font Awesome**：图标库
- **Moment.js**：日期处理

### 开发工具
- **Virtual Environment**：Python 虚拟环境
- **Version Control**：Git

## 🚀 快速开始

### 前置要求
- Python 3.12 或更高版本
- Git

### Windows 用户（推荐）

1. **克隆仓库**
   ```bash
   git clone https://github.com/Adsryen/fridgeManager.git
   cd fridgeManager
   ```

2. **一键配置**
   ```bash
   # 双击运行
   setup.bat
   ```

3. **启动应用**
   ```bash
   # 双击运行
   start.bat
   ```

4. **访问应用**
   
   打开浏览器访问 `http://127.0.0.1:8080`

### Linux/Mac 用户

1. **克隆仓库**
   ```bash
   git clone https://github.com/Adsryen/fridgeManager.git
   cd fridgeManager
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行应用**
   ```bash
   python app.py
   ```

5. **访问应用**
   
   打开浏览器访问 `http://127.0.0.1:8080`

## 📖 使用指南

### 首次使用
1. 访问 `http://127.0.0.1:8080`
2. 点击"立即注册"创建账号
3. 填写用户名、邮箱、密码（至少 6 位）
4. 注册成功后自动登录

### 添加物品
1. 点击"新增商品"按钮
2. 填写物品信息：
   - **名称**：物品名称
   - **过期日期**：选择过期日期
   - **数量**：物品数量
   - **位置**：冷藏/冷冻/常温
   - **类别**：选择合适的食材分类
3. 点击"添加"完成

### 查看物品
- **全部商品**：查看所有物品
- **尚在保存期限**：查看未过期物品
- **已过期**：查看过期物品
- **按位置筛选**：冷藏/冷冻
- **按类别筛选**：12 种食材分类
- **搜索功能**：按关键词实时搜索

### 编辑/删除物品
- 点击物品旁的编辑按钮进行修改
- 点击删除按钮移除物品

## 🔌 API 文档

### 端点列表

| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| GET | `/` | 主页 | - |
| GET/POST | `/register` | 用户注册 | username, email, password |
| GET/POST | `/login` | 用户登录 | username, password |
| GET | `/logout` | 用户登出 | - |
| POST | `/insert` | 添加物品 | itemName, itemDate, itemPlace, itemNum, itemType |
| POST | `/search` | 搜索物品 | text |
| POST | `/stateok/<time>` | 获取未过期物品 | time (时间戳) |
| POST | `/statebad/<time>` | 获取已过期物品 | time (时间戳) |
| POST | `/cold` | 获取冷藏物品 | - |
| POST | `/frozer` | 获取冷冻物品 | - |
| POST | `/tag/<tagName>` | 按类别获取物品 | tagName |
| POST | `/total` | 获取所有物品 | - |
| POST | `/delete/<_id>` | 删除物品 | _id |
| POST | `/getone/<_id>` | 获取单个物品 | _id |
| POST | `/edit/<_id>` | 编辑物品 | _id, itemName, itemDate, itemPlace, itemNum, itemType |

### 数据结构

```json
{
  "_id": "unique_id",
  "user_id": "user_id",
  "Name": "物品名称",
  "ExpireDate": "2024-12-31T00:00:00.000Z",
  "Place": "cold|frozer|room",
  "Num": 1,
  "Type": "vegetable|fruit|seafood|meat|beverage|diary|egg|bread|frozen|sauce|snack|other"
}
```

## 📁 项目结构

```
fridgeManager/
├── app.py                 # Flask 主应用
├── auth.py                # 用户认证模块
├── README.md              # 项目文档（中文）
├── README_EN.md           # 项目文档（英文）
├── 快速开始.md            # 快速开始指南
├── requirements.txt       # Python 依赖
├── setup.bat              # Windows 配置脚本
├── start.bat              # Windows 启动脚本
├── migrate_add_user_id.py # 数据迁移脚本
├── data/                  # 数据库目录（不提交到 Git）
├── templates/             # HTML 模板
│   ├── template.html      # 主页模板
│   ├── login.html         # 登录页面
│   └── register.html      # 注册页面
├── static/                # 静态资源
│   ├── index.js           # 前端 JavaScript
│   └── style/
│       └── index.css      # 样式表
└── tests/                 # 测试套件
    ├── conftest.py        # Pytest 配置
    ├── test_app.py        # 单元测试
    └── test_database.py   # 集成测试
```

## 🧪 测试

本项目包含完整的测试框架：

### 测试类型
- **单元测试**：Flask 路由和独立函数
- **集成测试**：数据库操作和 API 端点
- **Pytest 测试**：使用 fixtures 和 mocking 的现代测试

### 运行测试
```bash
# 运行所有测试
python run_tests.py

# 运行特定类型测试
python run_tests.py --type unittest
python run_tests.py --type pytest
python run_tests.py --type coverage
```

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

**教育用途**：本项目基于中央大学数据库系统期中项目进行二次开发，用于教育和研究目的。

**原项目致谢**：感谢 [hill0106](https://github.com/hill0106) 创建的原始项目。

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！**

原项目 / Original Project: [hill0106/fridgeManager](https://github.com/hill0106/fridgeManager)

二次开发 / Secondary Development: [Adsryen](https://github.com/Adsryen)

</div>
