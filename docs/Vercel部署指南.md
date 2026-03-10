# Vercel 部署指南

本指南将帮助你将前端应用部署到 Vercel，包含详细的配置步骤和常见问题解决方案。

## 📋 快速参考

| 配置项 | 值 | 说明 |
|--------|-----|------|
| **Framework Preset** | ✅ **Vite** | 必须选择 Vite，不是 Vue.js |
| **Root Directory** | `frontend` | 前端代码所在目录 |
| **Build Command** | `npm run build` | 构建命令（自动检测） |
| **Output Directory** | `dist` | 构建输出目录（自动检测） |
| **Install Command** | `npm install` | 安装命令（自动检测） |
| **Node.js Version** | `18.x` | 推荐版本 |
| **环境变量** | `VITE_API_BASE_URL` | 后端 API 地址 |

> 💡 **重点**：必须选择 **Vite** 框架预设，因为项目使用 Vite 构建工具！

## 🚀 部署方式

### 方式一：一键部署（推荐新手）

点击下方按钮，一键部署到 Vercel：

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FAdsryen%2FfridgeManager&project-name=fridge-manager&repository-name=fridgeManager&root-directory=frontend&env=VITE_API_BASE_URL&envDescription=后端%20API%20地址)

**详细步骤：**

1. **点击部署按钮**
   - 点击上方按钮，跳转到 Vercel 部署页面

2. **登录 Vercel**
   - 如果没有账号，选择 GitHub 登录（推荐）
   - 授权 Vercel 访问你的 GitHub 账号

3. **配置项目**
   - **Project Name**: `fridge-manager`（可自定义）
   - **Repository Name**: `fridgeManager`（保持默认）
   - **Root Directory**: `frontend`（已预设）

4. **配置环境变量**
   - **Variable Name**: `VITE_API_BASE_URL`
   - **Value**: 你的后端 API 地址
     - 示例：`https://api.example.com`
     - 本地测试：`http://localhost:8080`
   - **Environment**: 选择 `Production`

5. **开始部署**
   - 点击 **Deploy** 按钮
   - 等待 1-2 分钟完成部署

6. **访问应用**
   - 部署成功后，Vercel 会提供一个域名
   - 点击域名访问你的应用

### 方式二：通过 Vercel Dashboard（推荐有经验用户）

1. **登录 Vercel Dashboard**
   - 访问 [vercel.com](https://vercel.com) 并登录

2. **导入项目**
   - 点击 **Add New** → **Project**
   - 选择 **Import Git Repository**
   - 找到并选择你的 `fridgeManager` 仓库

3. **配置项目设置**
   
   **重要配置项：**
   
   - **Framework Preset**: 
     ```
     选择：Vite ✅
     不要选择：Vue.js ❌
     ```
     > 💡 虽然项目使用 Vue 3，但必须选择 Vite，因为项目使用 Vite 作为构建工具
   
   - **Root Directory**: 
     ```
     点击 Edit → 输入：frontend
     ```
     > ⚠️ 重要：必须设置为 `frontend`，因为前端代码在子目录中
   
   - **Build Command**: 
     ```
     npm run build
     ```
     （通常自动检测，无需修改）
   
   - **Output Directory**: 
     ```
     dist
     ```
     （通常自动检测，无需修改）
   
   - **Install Command**: 
     ```
     npm install
     ```
     （通常自动检测，无需修改）

4. **配置环境变量**
   
   在 **Environment Variables** 部分添加：
   
   | Name | Value | Environment |
   |------|-------|-------------|
   | `VITE_API_BASE_URL` | `https://your-api.com` | Production |
   
   > 📝 **环境变量说明**：
   > - 必须以 `VITE_` 开头才能在前端代码中访问
   > - 不要包含敏感信息（如密钥），这些会暴露在前端代码中
   > - 修改后需要重新部署才能生效

5. **部署项目**
   - 检查所有配置无误后，点击 **Deploy**
   - 等待构建完成（通常 1-2 分钟）

### 方式三：通过 Vercel CLI（推荐开发者）

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

4. **初始化部署**
   ```bash
   vercel
   ```
   
   按照提示配置：
   ```
   ? Set up and deploy "~/fridgeManager/frontend"? [Y/n] Y
   ? Which scope do you want to deploy to? [选择你的账号]
   ? Link to existing project? [Y/n] N
   ? What's your project's name? fridge-manager
   ? In which directory is your code located? ./
   ? Want to override the settings? [y/N] N
   ```

5. **配置环境变量**
   ```bash
   vercel env add VITE_API_BASE_URL production
   ```
   输入你的后端 API 地址

6. **生产部署**
   ```bash
   vercel --prod
   ```

## 🔧 详细配置说明

### 框架预设选择

**为什么选择 Vite 而不是 Vue.js？**

| 选项 | 说明 | 是否正确 |
|------|------|----------|
| **Vite** | 针对使用 Vite 构建工具的项目 | ✅ 正确 |
| **Vue.js** | 针对使用 Vue CLI 或 Nuxt.js 的项目 | ❌ 错误 |
| **Other** | 通用选项，但不如 Vite 预设优化 | ⚠️ 可用但不推荐 |

**选择 Vite 的好处：**
- Vercel 自动识别 Vite 项目结构
- 自动配置正确的构建命令和输出目录
- 优化的缓存策略和构建性能
- 支持 Vite 的所有特性（HMR、环境变量等）

### 构建配置详解

```json
{
  "framework": "vite",
  "rootDirectory": "frontend",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "nodeVersion": "18.x"
}
```

### 环境变量配置

#### 前端环境变量规则
- **命名规则**：必须以 `VITE_` 开头
- **访问方式**：在代码中使用 `import.meta.env.VITE_变量名`
- **安全性**：会暴露在前端代码中，不要存储敏感信息

#### 常用环境变量
```bash
# 必需的环境变量
VITE_API_BASE_URL=https://your-backend-api.com

# 可选的环境变量
VITE_APP_TITLE=冰箱里面还有啥
VITE_APP_VERSION=1.0.0
VITE_ENABLE_ANALYTICS=true
```

#### 在代码中使用
```typescript
// 获取 API 基础地址
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

// 获取应用标题
const appTitle = import.meta.env.VITE_APP_TITLE || '冰箱里面还有啥'
```

## 🌐 自定义域名

### 添加自定义域名

1. **在 Vercel Dashboard 中**
   - 打开你的项目
   - 进入 **Settings** → **Domains**

2. **添加域名**
   - 点击 **Add** 按钮
   - 输入你的域名（如 `fridge.example.com`）
   - 点击 **Add**

3. **配置 DNS**
   
   根据域名类型配置 DNS 记录：
   
   **子域名（推荐）：**
   ```
   类型: CNAME
   名称: fridge
   值: cname.vercel-dns.com
   ```
   
   **根域名：**
   ```
   类型: A
   名称: @
   值: 76.76.19.61
   ```

4. **等待生效**
   - DNS 生效通常需要几分钟到几小时
   - 可以使用 `nslookup` 命令检查 DNS 是否生效

### SSL 证书
Vercel 会自动为所有域名提供免费的 SSL 证书，无需额外配置。

## 🔄 更新部署

### 自动部署
- 每次推送到 GitHub 主分支，Vercel 会自动重新部署
- 可以在 **Deployments** 页面查看部署历史

### 手动部署
```bash
# 使用 CLI 手动部署
cd frontend
vercel --prod
```

### 回滚部署
1. 在 Vercel Dashboard 中打开项目
2. 进入 **Deployments** 页面
3. 找到要回滚的版本
4. 点击 **Promote to Production**

## ❗ 常见问题与解决方案

### 部署配置问题

**Q1: 选择了错误的框架类型怎么办？**

如果不小心选择了 Vue.js 而不是 Vite：

**解决方案 1：删除项目重新创建**
1. 在 Vercel Dashboard 中进入项目设置
2. 滚动到底部，点击 **Delete Project**
3. 重新导入项目，这次选择 Vite

**解决方案 2：修改项目设置**
1. 进入项目 **Settings** → **General**
2. 在 **Framework Preset** 中选择 **Vite**
3. 确认 **Root Directory** 为 `frontend`
4. 保存设置并重新部署

**Q2: Root Directory 设置错误**

**症状**：构建时提示找不到 `package.json`

**解决方案**：
1. 进入 Vercel 项目 **Settings** → **General**
2. 找到 **Root Directory** 设置
3. 点击 **Edit**，输入 `frontend`
4. 保存并重新部署

**Q3: 构建失败**

**常见原因和解决方案**：

- **Node.js 版本不兼容**
  ```
  解决：在项目设置中指定 Node.js 版本为 18.x
  ```

- **依赖安装失败**
  ```
  解决：检查 package.json 中的依赖版本，本地测试 npm install
  ```

- **TypeScript 类型错误**
  ```
  解决：本地运行 npm run build 检查类型错误
  ```

- **内存不足**
  ```
  解决：在 vercel.json 中增加内存限制
  {
    "functions": {
      "app/api/**/*.js": {
        "memory": 1024
      }
    }
  }
  ```

### 运行时问题

**Q4: API 请求失败（CORS 错误）**

**原因**：后端未配置 CORS 允许 Vercel 域名

**解决方案**：在后端 Flask 应用中添加 CORS 配置
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    'http://localhost:5173',           # 开发环境
    'https://your-app.vercel.app',     # Vercel 域名
    'https://your-custom-domain.com'   # 自定义域名
])
```

**Q5: 环境变量未生效**

**解决方案**：
1. 确保环境变量名以 `VITE_` 开头
2. 在 Vercel Dashboard 中检查环境变量配置
3. 重新部署项目（修改环境变量不会自动触发部署）
4. 在代码中正确使用 `import.meta.env.VITE_变量名`

**Q6: 路由 404 错误**

**原因**：SPA 路由未正确配置

**解决方案**：确保项目根目录有 `vercel.json` 文件：
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### 性能问题

**Q7: 首次加载慢**

**解决方案**：
1. 启用代码分割
2. 使用图片优化
3. 启用 Vercel Analytics 监控性能

**Q8: 静态资源加载失败**

**解决方案**：
1. 检查资源路径是否正确
2. 确保资源文件在 `public` 目录中
3. 使用相对路径而不是绝对路径

## 📊 监控与分析

### Vercel Analytics
1. 在项目设置中启用 Analytics
2. 查看页面访问量、性能指标等
3. 分析用户行为和页面性能

### 部署日志
1. 在 **Deployments** 页面查看构建日志
2. 点击具体部署查看详细日志
3. 根据错误信息排查问题

### 性能监控
```typescript
// 在代码中添加性能监控
if (typeof window !== 'undefined') {
  // 监控页面加载时间
  window.addEventListener('load', () => {
    const loadTime = performance.now()
    console.log(`页面加载时间: ${loadTime}ms`)
  })
}
```

## 💰 成本说明

### Hobby 计划（免费）
- **带宽**：100GB/月
- **构建时间**：100 小时/月
- **域名**：无限制
- **团队成员**：1 人
- **适用场景**：个人项目、学习项目

### Pro 计划（$20/月）
- **带宽**：1TB/月
- **构建时间**：400 小时/月
- **域名**：无限制
- **团队成员**：10 人
- **高级功能**：密码保护、分析等
- **适用场景**：商业项目、团队协作

详细定价请查看 [Vercel Pricing](https://vercel.com/pricing)

## 🔗 相关链接

- [Vercel 官方文档](https://vercel.com/docs)
- [Vite 部署指南](https://vitejs.dev/guide/static-deploy.html)
- [Vue 3 部署指南](https://vuejs.org/guide/best-practices/production-deployment.html)
- [项目 GitHub 仓库](https://github.com/Adsryen/fridgeManager)

---

如有问题，请提交 [Issue](https://github.com/Adsryen/fridgeManager/issues) 或查看 [讨论区](https://github.com/Adsryen/fridgeManager/discussions)。
