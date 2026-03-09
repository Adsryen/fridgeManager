# 🧊 冰箱里面还有啥

> 智能冰箱库存管理系统，帮助你有效管理冰箱中的食材，减少浪费，提升生活品质！

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-green.svg)](https://www.sqlite.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0.0-purple.svg)](https://getbootstrap.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](./docs/README_EN.md) | 中文

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
- **JWT**：用户认证
- **APScheduler**：定时任务

### 前端
- **Vue 3**：渐进式 JavaScript 框架
- **TypeScript**：类型安全
- **Vite**：现代化构建工具
- **Pinia**：状态管理
- **Vue Router**：路由管理
- **Element Plus**：UI 组件库
- **Axios**：HTTP 客户端

### 开发工具
- **Virtual Environment**：Python 虚拟环境
- **ESLint + Prettier**：代码规范
- **Version Control**：Git

## 🚀 快速开始

### 前置要求
- Python 3.12 或更高版本
- Node.js 18+ 和 npm
- Git

### 开发环境部署

#### 1. 克隆仓库
```bash
git clone https://github.com/Adsryen/fridgeManager.git
cd fridgeManager
```

#### 2. 后端设置
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 前端设置
```bash
cd frontend
npm install
```

#### 4. 启动开发服务器

**方式一：使用启动脚本（推荐）**
```bash
# Windows PowerShell
.\start_dev.ps1

# 或者使用 npm
npm run dev:all
```

**方式二：分别启动**
```bash
# 终端 1 - 启动后端（端口 8080）
python run.py

# 终端 2 - 启动前端（端口 5173）
cd frontend
npm run dev
```

#### 5. 访问应用
- 前端：`http://localhost:5173`
- 后端 API：`http://localhost:8080`

### 生产环境部署

#### Docker 部署（推荐）

1. **克隆仓库**
   ```bash
   git clone https://github.com/Adsryen/fridgeManager.git
   cd fridgeManager/docker
   ```

2. **启动服务**
   ```bash
   docker-compose up -d
   ```

3. **访问应用**
   
   打开浏览器访问 `http://localhost:8080`

详细说明请查看 [Docker 部署指南](./docker/README.md)

#### Vercel 部署前端

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FAdsryen%2FfridgeManager&project-name=fridge-manager&repository-name=fridgeManager&root-directory=frontend&env=VITE_API_BASE_URL&envDescription=后端%20API%20地址&envLink=https%3A%2F%2Fgithub.com%2FAdsryen%2FfridgeManager%23vercel-部署)

**环境变量配置：**
- `VITE_API_BASE_URL`：后端 API 地址（例如：`https://your-backend.com`）

**部署步骤：**
1. 点击上方按钮，跳转到 Vercel
2. 登录 Vercel 账号
3. 配置环境变量 `VITE_API_BASE_URL`
4. 点击 Deploy 开始部署
5. 部署完成后，访问 Vercel 提供的域名

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
├── app/                      # 后端应用核心代码
│   ├── __init__.py           # Flask 应用工厂
│   ├── models/               # 数据模型
│   │   ├── user.py           # 用户模型
│   │   ├── item.py           # 物品模型
│   │   ├── fridge.py         # 冰箱模型
│   │   ├── family.py         # 家庭模型
│   │   └── ...
│   ├── routes/               # 路由蓝图
│   │   ├── auth.py           # 认证路由
│   │   ├── item.py           # 物品路由
│   │   ├── fridge.py         # 冰箱路由
│   │   ├── family.py         # 家庭路由
│   │   └── admin.py          # 管理员路由
│   ├── services/             # 业务逻辑
│   │   ├── user_service.py
│   │   ├── item_service.py
│   │   ├── fridge_service.py
│   │   └── family_service.py
│   ├── utils/                # 工具函数
│   │   ├── jwt_auth.py       # JWT 认证
│   │   ├── database.py       # 数据库工具
│   │   └── validators.py     # 数据验证
│   └── tasks/                # 定时任务
│       └── scheduler.py      # 任务调度器
├── frontend/                 # Vue3 前端应用
│   ├── src/
│   │   ├── api/              # API 接口
│   │   ├── assets/           # 静态资源
│   │   ├── components/       # Vue 组件
│   │   │   ├── common/       # 通用组件
│   │   │   ├── item/         # 物品组件
│   │   │   ├── fridge/       # 冰箱组件
│   │   │   ├── family/       # 家庭组件
│   │   │   └── ai/           # AI 功能组件
│   │   ├── composables/      # 组合式函数
│   │   ├── router/           # 路由配置
│   │   ├── stores/           # Pinia 状态管理
│   │   ├── styles/           # 全局样式
│   │   ├── types/            # TypeScript 类型
│   │   ├── utils/            # 工具函数
│   │   ├── views/            # 页面视图
│   │   ├── App.vue           # 根组件
│   │   └── main.ts           # 入口文件
│   ├── public/               # 公共资源
│   ├── .env.development      # 开发环境变量
│   ├── .env.production       # 生产环境变量
│   ├── package.json          # 前端依赖
│   ├── tsconfig.json         # TypeScript 配置
│   ├── vite.config.ts        # Vite 配置
│   └── vercel.json           # Vercel 部署配置
├── config/                   # 后端配置文件
│   └── settings.py           # 应用配置
├── docker/                   # Docker 部署
│   ├── Dockerfile            # Docker 镜像
│   ├── docker-compose.yml    # Docker Compose 配置
│   └── README.md             # Docker 部署指南
├── docs/                     # 文档
│   ├── README_EN.md          # 英文文档
│   ├── API接口文档.md        # API 文档
│   └── 快速开始.md           # 快速开始指南
├── scripts/                  # 脚本工具
│   └── migrate_*.py          # 数据迁移脚本
├── static/                   # Flask 静态资源（旧版）
├── templates/                # Flask 模板（旧版）
├── tests/                    # 测试套件
├── data/                     # 数据库目录（不提交到 Git）
├── start_dev.ps1             # 开发环境启动脚本
├── run.py                    # 后端启动入口
├── requirements.txt          # Python 依赖
└── README.md                 # 项目文档（中文）
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
