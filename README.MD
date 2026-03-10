# 🧊 冰箱里面还有啥

> 智能冰箱库存管理系统，帮助你有效管理冰箱中的食材，减少浪费，提升生活品质！

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FAdsryen%2FfridgeManager&project-name=fridge-manager&repository-name=fridgeManager&root-directory=frontend&env=VITE_API_BASE_URL&envDescription=后端%20API%20地址)

[English](./docs/README_EN.md) | 中文 | [技术文档](./docs/技术文档.md) | [开发指南](./docs/开发指南.md)

---

## 📋 目录

- [项目介绍](#项目介绍)
- [功能特性](#功能特性)
- [在线体验](#在线体验)
- [快速部署](#快速部署)
- [使用指南](#使用指南)
- [常见问题](#常见问题)
- [支持与反馈](#支持与反馈)

## 项目介绍

**冰箱里面还有啥** 是一个智能冰箱库存管理系统，帮助家庭有效管理食材，减少浪费，提升生活品质。

### 🎯 解决的问题
- 🤔 忘记冰箱里有什么食材
- 📅 不知道食材什么时候过期
- 🗑️ 食材过期造成浪费
- 👨‍👩‍👧‍👦 家庭成员无法共享食材信息

### 🌟 项目亮点
- **多用户支持**：每个用户独立管理，数据完全隔离
- **家庭共享**：支持家庭成员共享冰箱管理
- **智能提醒**：自动识别过期和即将过期的食材
- **现代化界面**：Vue 3 + TypeScript 构建的响应式界面
- **轻量部署**：基于 SQLite，无需复杂数据库配置

> 本项目基于 [hill0106/fridgeManager](https://github.com/hill0106/fridgeManager) 进行二次开发，在原有功能基础上新增了多用户支持、现代化前端界面和家庭共享功能。

## ✨ 功能特性

### 👤 用户管理
- **账户系统**：注册、登录、密码重置
- **多用户支持**：每个用户独立的数据空间
- **家庭共享**：创建或加入家庭，共享冰箱管理

### 🧊 冰箱管理
- **多冰箱支持**：管理多个冰箱（家用、办公室等）
- **权限控制**：设置冰箱访问权限
- **智能分类**：12种食材分类（蔬菜、水果、肉类等）
- **位置管理**：冷藏、冷冻、常温三种存储位置

### 📦 物品管理
- **快速添加**：支持手动输入、语音输入、OCR识别
- **智能搜索**：按名称、类别、位置实时搜索
- **批量操作**：批量编辑、删除物品
- **过期提醒**：自动标识过期和即将过期物品

### 🤖 AI 功能
- **智能对话**：AI助手帮你管理冰箱
- **OCR识别**：拍照识别食材信息
- **语音输入**：语音添加物品信息
- **智能建议**：基于库存推荐菜谱

### 📱 用户体验
- **响应式设计**：完美适配手机、平板、电脑
- **暗黑模式**：支持明暗主题切换
- **离线支持**：部分功能支持离线使用
- **快速操作**：一键添加、快速筛选

## 🌐 在线体验

### 演示地址
- **前端演示**：[https://fridge-manager.vercel.app](https://fridge-manager.vercel.app)
- **API文档**：[查看接口文档](./docs/API接口文档.md)

### 测试账号
```
用户名：demo
密码：123456
```

> 💡 演示环境数据会定期重置，请勿存储重要信息

## 🚀 快速部署

### 方式一：Vercel 一键部署（推荐）

点击下方按钮，一键部署前端到 Vercel：

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FAdsryen%2FfridgeManager&project-name=fridge-manager&repository-name=fridgeManager&root-directory=frontend&env=VITE_API_BASE_URL&envDescription=后端%20API%20地址)

**部署步骤：**
1. 点击按钮，跳转到 Vercel
2. 登录 Vercel 账号（支持 GitHub 登录）
3. 配置项目：
   - **Framework Preset**：选择 `Vite`（重要！）
   - **Root Directory**：`frontend`
   - **Environment Variables**：
     - `VITE_API_BASE_URL`：你的后端 API 地址
4. 点击 **Deploy** 开始部署
5. 等待 1-2 分钟完成部署
6. 访问 Vercel 提供的域名

> 📖 详细部署教程：[Vercel 部署指南](./docs/Vercel部署指南.md)

### 方式二：Docker 部署

```bash
# 克隆项目
git clone https://github.com/Adsryen/fridgeManager.git
cd fridgeManager/docker

# 启动服务
docker-compose up -d

# 访问应用
# 前端：http://localhost:8080
# 后端：http://localhost:8080/api
```

### 方式三：本地开发

```bash
# 1. 克隆项目
git clone https://github.com/Adsryen/fridgeManager.git
cd fridgeManager

# 2. 后端设置
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. 前端设置
cd frontend
npm install

# 4. 启动开发服务器
# Windows PowerShell
.\start_dev.ps1

# 或分别启动
python run.py  # 后端：http://localhost:8080
npm run dev    # 前端：http://localhost:5173
```

> 🔧 详细开发指南：[开发指南](./docs/开发指南.md)

## 📖 使用指南

### 🔐 账户管理

#### 注册账户
1. 访问应用首页
2. 点击"立即注册"
3. 填写用户名、邮箱、密码（至少6位）
4. 点击"注册"完成账户创建

#### 登录系统
1. 在登录页面输入用户名和密码
2. 点击"登录"进入系统
3. 系统会记住登录状态，下次访问自动登录

### 🏠 家庭管理

#### 创建家庭
1. 进入"家庭"页面
2. 点击"创建家庭"
3. 输入家庭名称和描述
4. 点击"创建"完成

#### 加入家庭
1. 获取家庭邀请码（由家庭创建者提供）
2. 在"家庭"页面点击"加入家庭"
3. 输入邀请码
4. 点击"加入"

### 🧊 冰箱管理

#### 创建冰箱
1. 在"冰箱"页面点击"新建冰箱"
2. 输入冰箱名称（如"家用冰箱"、"办公室冰箱"）
3. 选择所属家庭（可选）
4. 点击"创建"

#### 切换冰箱
- 在顶部导航栏点击冰箱名称
- 从下拉菜单中选择要管理的冰箱

### 📦 物品管理

#### 添加物品
**方式一：手动添加**
1. 点击"添加物品"按钮
2. 填写物品信息：
   - **名称**：食材名称
   - **数量**：物品数量
   - **过期日期**：选择过期日期
   - **存储位置**：冷藏/冷冻/常温
   - **分类**：选择食材类别
3. 点击"保存"

**方式二：语音添加**
1. 点击"语音添加"按钮
2. 说出物品信息（如"苹果3个明天过期"）
3. 系统自动识别并填充表单
4. 确认信息后保存

**方式三：拍照识别**
1. 点击"拍照添加"按钮
2. 拍摄食材照片
3. 系统自动识别物品信息
4. 确认并保存

#### 查看物品
- **全部物品**：查看所有库存
- **即将过期**：查看3天内过期的物品
- **已过期**：查看已过期物品
- **按位置筛选**：冷藏/冷冻/常温
- **按分类筛选**：蔬菜、水果、肉类等

#### 编辑物品
1. 在物品列表中点击要编辑的物品
2. 修改相关信息
3. 点击"保存"

#### 删除物品
1. 在物品列表中找到要删除的物品
2. 点击删除按钮
3. 确认删除

### 🤖 AI 助手

#### 智能对话
1. 点击右下角的AI助手图标
2. 输入问题（如"今天有什么菜可以做？"）
3. AI会根据你的库存推荐菜谱

#### 语音交互
1. 在对话框中点击语音按钮
2. 说出你的问题
3. AI会语音回复

### ⚙️ 个人设置

#### 修改个人信息
1. 点击右上角头像
2. 选择"个人设置"
3. 修改用户名、邮箱等信息
4. 点击"保存"

#### 主题设置
1. 在个人设置中找到"主题设置"
2. 选择明亮/暗黑主题
3. 系统会自动保存设置

#### 通知设置
1. 在个人设置中配置通知偏好
2. 设置过期提醒时间（1天、3天、7天前）
3. 选择通知方式（邮件、站内消息）

## ❓ 常见问题

### 部署相关

**Q: Vercel 部署时选择什么框架？**
A: 选择 **Vite**，不是 Vue.js。因为项目使用 Vite 作为构建工具。

**Q: 部署后 API 请求失败怎么办？**
A: 检查环境变量 `VITE_API_BASE_URL` 是否正确配置，确保后端服务正常运行。

**Q: 如何配置自定义域名？**
A: 在 Vercel Dashboard 的项目设置中添加自定义域名，并按提示配置 DNS。

### 使用相关

**Q: 忘记密码怎么办？**
A: 在登录页面点击"忘记密码"，输入邮箱地址重置密码。

**Q: 如何邀请家庭成员？**
A: 在家庭页面点击"邀请成员"，分享邀请码给家庭成员。

**Q: 物品过期提醒在哪里设置？**
A: 在个人设置的"通知设置"中配置过期提醒时间。

**Q: 支持哪些浏览器？**
A: 支持 Chrome、Firefox、Safari、Edge 等现代浏览器。

### 技术相关

**Q: 数据存储在哪里？**
A: 数据存储在 SQLite 数据库中，支持本地部署和云端部署。

**Q: 是否支持数据导出？**
A: 支持导出物品清单为 Excel 或 CSV 格式。

**Q: 如何备份数据？**
A: 定期备份 `data/fridge.db` 文件即可。

## 🆘 支持与反馈

### 获取帮助
- 📖 [查看完整文档](./docs/)
- 🐛 [提交问题](https://github.com/Adsryen/fridgeManager/issues)
- 💬 [讨论交流](https://github.com/Adsryen/fridgeManager/discussions)

### 贡献代码
欢迎提交 Pull Request！请先阅读 [开发指南](./docs/开发指南.md)。

### 联系方式
- GitHub: [@Adsryen](https://github.com/Adsryen)
- Email: [your-email@example.com](mailto:your-email@example.com)

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

**致谢**：感谢 [hill0106](https://github.com/hill0106) 创建的原始项目 [fridgeManager](https://github.com/hill0106/fridgeManager)。

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！**

[🏠 项目主页](https://github.com/Adsryen/fridgeManager) | [📖 技术文档](./docs/技术文档.md) | [🚀 开发指南](./docs/开发指南.md) | [📋 更新日志](./CHANGELOG.md)

</div>
