# Vercel 部署指南

本指南将帮助你将前端应用部署到 Vercel。

## 📋 快速参考

| 配置项 | 值 |
|--------|-----|
| **Framework Preset** | ✅ Vite（不是 Vue.js） |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |
| **Node.js Version** | 18.x |
| **环境变量** | `VITE_API_BASE_URL` |

> 💡 **重点**：选择 **Vite** 而不是 Vue.js，因为项目使用 Vite 构建工具！

## 前置要求

1. 一个 [Vercel](https://vercel.com) 账号
2. 后端 API 已部署并可访问（例如：部署在自己的服务器或云平台）

## 快速部署

### 方式一：一键部署（推荐）

点击下方按钮，一键部署到 Vercel：

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FAdsryen%2FfridgeManager&project-name=fridge-manager&repository-name=fridgeManager&root-directory=frontend&env=VITE_API_BASE_URL&envDescription=后端%20API%20地址&envLink=https%3A%2F%2Fgithub.com%2FAdsryen%2FfridgeManager%23vercel-部署)

**步骤：**
1. 点击按钮，跳转到 Vercel
2. 登录你的 Vercel 账号
3. 配置环境变量：
   - `VITE_API_BASE_URL`：你的后端 API 地址（例如：`https://api.example.com`）
4. 点击 **Deploy** 开始部署
5. 等待部署完成（通常 1-2 分钟）
6. 访问 Vercel 提供的域名

### 方式二：通过 Vercel CLI

1. **安装 Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **登录 Vercel**
   ```bash
   vercel login
   ```

3. **进入前端目录**
   ```bash
   cd frontend
   ```

4. **部署**
   ```bash
   vercel
   ```

5. **按照提示配置项目**
   - Set up and deploy: Yes
   - Which scope: 选择你的账号
   - Link to existing project: No
   - Project name: fridge-manager（或自定义）
   - In which directory is your code located: ./
   - Want to override the settings: No

6. **配置环境变量**
   ```bash
   vercel env add VITE_API_BASE_URL
   ```
   输入你的后端 API 地址（例如：`https://api.example.com`）

7. **重新部署以应用环境变量**
   ```bash
   vercel --prod
   ```

### 方式三：通过 Vercel Dashboard

1. **登录 Vercel Dashboard**
   访问 [vercel.com](https://vercel.com) 并登录

2. **导入项目**
   - 点击 **Add New** → **Project**
   - 选择 **Import Git Repository**
   - 授权并选择你的 GitHub 仓库

3. **配置项目**
   
   在项目配置页面，按以下方式填写：
   
   - **Framework Preset**: 选择 **Vite** 
     > 💡 虽然项目使用 Vue 3，但应该选择 Vite 而不是 Vue.js，因为项目使用 Vite 作为构建工具
   
   - **Root Directory**: 点击 **Edit**，输入 `frontend`
     > ⚠️ 重要：必须设置为 `frontend`，因为前端代码在 frontend 子目录中
   
   - **Build Command**: `npm run build` （通常自动检测，无需修改）
   
   - **Output Directory**: `dist` （通常自动检测，无需修改）
   
   - **Install Command**: `npm install` （通常自动检测，无需修改）

4. **配置环境变量**
   在 **Environment Variables** 部分添加：
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: 你的后端 API 地址（例如：`https://api.example.com`）
   - **Environment**: Production

5. **部署**
   点击 **Deploy** 开始部署

## 环境变量说明

| 变量名 | 说明 | 示例 | 必需 |
|--------|------|------|------|
| `VITE_API_BASE_URL` | 后端 API 地址 | `https://api.example.com` | 是 |

> ⚠️ **注意**：
> - 所有前端环境变量必须以 `VITE_` 开头才能在代码中访问
> - 修改环境变量后需要重新部署才能生效
> - 不要在环境变量中包含敏感信息（如密钥），这些会暴露在前端代码中

## 项目类型选择详解

### 为什么选择 Vite 而不是 Vue.js？

在 Vercel 创建项目时，你会看到多个框架选项：

- ❌ **Vue.js** - 这是针对使用 Vue CLI 或 Nuxt.js 的项目
- ✅ **Vite** - 这是正确的选择，因为本项目使用 Vite 作为构建工具
- ❌ **Other** - 通用选项，但不如 Vite 预设优化好

**选择 Vite 的好处：**
1. Vercel 会自动识别 Vite 项目结构
2. 自动配置正确的构建命令和输出目录
3. 优化的缓存策略和构建性能
4. 支持 Vite 的所有特性（如 HMR、环境变量等）

### 完整的项目配置示例

```
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
Install Command: npm install
Node.js Version: 18.x (推荐)
```

## 自定义域名

1. 在 Vercel Dashboard 中打开你的项目
2. 进入 **Settings** → **Domains**
3. 点击 **Add** 添加你的域名
4. 按照提示配置 DNS 记录
5. 等待 DNS 生效（通常几分钟到几小时）

## 更新部署

### 自动部署
- 每次推送到 GitHub 主分支，Vercel 会自动重新部署
- 可以在 Vercel Dashboard 中查看部署历史和日志

### 手动部署
```bash
cd frontend
vercel --prod
```

## 常见问题

### 1. 选择了错误的框架类型怎么办？

如果不小心选择了 Vue.js 而不是 Vite：

**方案 1：删除项目重新创建**
1. 在 Vercel Dashboard 中进入项目设置
2. 滚动到底部，点击 **Delete Project**
3. 重新导入项目，这次选择 Vite

**方案 2：手动修改构建配置**
1. 进入项目 **Settings** → **General**
2. 修改 **Framework Preset** 为 Vite
3. 确认 **Root Directory** 为 `frontend`
4. 保存并重新部署

### 2. API 请求失败（CORS 错误）

**原因**：后端未配置 CORS 允许 Vercel 域名

**解决方案**：在后端 Flask 应用中添加 Vercel 域名到 CORS 配置

```python
# app/__init__.py
from flask_cors import CORS

CORS(app, origins=[
    'http://localhost:5173',
    'https://your-app.vercel.app',  # 添加你的 Vercel 域名
    'https://your-custom-domain.com'  # 如果有自定义域名
])
```

### 3. 环境变量未生效

**解决方案**：
1. 确保环境变量名以 `VITE_` 开头
2. 在 Vercel Dashboard 中检查环境变量是否正确配置
3. 重新部署项目（修改环境变量不会自动触发部署）

### 4. 路由 404 错误

**原因**：SPA 路由未正确配置

**解决方案**：确保 `vercel.json` 文件存在且配置正确（已包含在项目中）

### 5. 构建失败

**常见原因**：
- Node.js 版本不兼容
- 依赖安装失败
- TypeScript 类型错误

**解决方案**：
1. 检查 Vercel 构建日志
2. 本地运行 `npm run build` 测试
3. 确保 `package.json` 中的依赖版本正确
4. 在 Vercel 项目设置中指定 Node.js 版本（推荐 18.x）

### 6. Root Directory 设置错误

**症状**：构建时提示找不到 `package.json`

**解决方案**：
1. 进入 Vercel 项目 **Settings** → **General**
2. 找到 **Root Directory**
3. 点击 **Edit**，输入 `frontend`
4. 保存并重新部署

## 性能优化

### 1. 启用 CDN 缓存
Vercel 自动为静态资源启用 CDN 缓存，无需额外配置。

### 2. 图片优化
使用 Vercel Image Optimization：
```vue
<img src="/api/image?url=/path/to/image.jpg&w=800&q=75" />
```

### 3. 代码分割
Vite 已自动配置代码分割，无需额外配置。

## 监控和分析

### Vercel Analytics
1. 在 Vercel Dashboard 中启用 Analytics
2. 查看页面访问量、性能指标等

### 日志查看
1. 在 Vercel Dashboard 中打开项目
2. 进入 **Deployments** 查看部署日志
3. 点击具体部署查看详细日志

## 回滚部署

如果新部署出现问题，可以快速回滚：

1. 在 Vercel Dashboard 中打开项目
2. 进入 **Deployments**
3. 找到之前的稳定版本
4. 点击 **Promote to Production**

## 成本说明

- **Hobby 计划**：免费，适合个人项目
  - 100GB 带宽/月
  - 无限部署
  - 自动 HTTPS
  - 全球 CDN

- **Pro 计划**：$20/月，适合专业项目
  - 1TB 带宽/月
  - 更多并发构建
  - 团队协作功能

详细定价请查看 [Vercel Pricing](https://vercel.com/pricing)

## 相关链接

- [Vercel 官方文档](https://vercel.com/docs)
- [Vite 部署指南](https://vitejs.dev/guide/static-deploy.html)
- [Vue 3 部署指南](https://vuejs.org/guide/best-practices/production-deployment.html)

---

如有问题，请提交 [Issue](https://github.com/Adsryen/fridgeManager/issues)。
