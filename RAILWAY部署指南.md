# Railway 部署指南

## 🚂 什么是 Railway？

Railway 是一个现代化的云平台，让你可以轻松部署和托管应用程序。

### Railway 的优势

✅ **无执行时间限制** - 不像 Vercel 有 10 秒限制，适合 AI 总结这种耗时操作  
✅ **简单易用** - 自动检测项目类型，无需复杂配置  
✅ **免费额度** - 每月 $5 免费额度，足够个人使用  
✅ **支持 Python** - 完美支持 Flask 应用  
✅ **自动部署** - 推送代码到 GitHub 自动重新部署  
✅ **实时日志** - 可以查看应用运行日志  
✅ **环境变量** - 方便管理敏感信息  

### Railway vs Vercel

| 特性 | Railway | Vercel |
|------|---------|--------|
| 执行时间限制 | 无限制 | 10秒（Hobby）|
| 适合场景 | 后端应用、API | 前端、静态网站 |
| Python 支持 | 原生支持 | 有限支持 |
| 免费额度 | $5/月 | 100GB 带宽 |
| 长时间任务 | ✅ 支持 | ❌ 不支持 |

**结论**: 对于你的 AI 文章总结应用，Railway 是更好的选择！

---

## 📋 前置准备

### 1. 注册 Railway 账号

1. 访问 [railway.app](https://railway.app)
2. 点击右上角 "Login"
3. 选择 "Login with GitHub"（推荐）
4. 授权 Railway 访问你的 GitHub 账号

### 2. 创建 GitHub 仓库

1. 登录 [github.com](https://github.com)
2. 点击右上角 "+" → "New repository"
3. 填写仓库名称：`yuque-article-fetcher`
4. 选择 Public 或 Private（都可以）
5. 点击 "Create repository"

---

## 🚀 部署步骤

### 第一步：准备项目文件

Railway 需要一些配置文件来正确部署你的应用。

#### 1. 创建 Procfile

在项目根目录创建 `Procfile` 文件（已为你准备好）：

```
web: gunicorn app:app
```

#### 2. 更新 requirements.txt

确保包含 `gunicorn`（已为你准备好）。

#### 3. 创建 railway.json（可选）

用于配置构建和部署选项（已为你准备好）。

### 第二步：推送代码到 GitHub

在终端执行以下命令：

```bash
# 1. 进入项目目录
cd /Users/donson/Documents/projects/yuque_article_fetcher

# 2. 初始化 Git 仓库
git init

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Initial commit: 文章抓取和AI总结工具"

# 5. 关联 GitHub 仓库（替换成你的仓库地址）
git remote add origin https://github.com/你的用户名/yuque-article-fetcher.git

# 6. 推送到 GitHub
git branch -M main
git push -u origin main
```

### 第三步：在 Railway 上部署

#### 方式一：通过 Railway 网站（推荐）

1. **登录 Railway**
   - 访问 [railway.app](https://railway.app)
   - 用 GitHub 账号登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"

3. **选择仓库**
   - 找到 `yuque-article-fetcher` 仓库
   - 点击 "Deploy Now"

4. **等待部署**
   - Railway 会自动检测这是一个 Python 项目
   - 自动安装依赖（requirements.txt）
   - 自动启动应用
   - 部署过程大约 2-5 分钟

5. **获取访问地址**
   - 部署成功后，点击项目
   - 点击 "Settings" → "Domains"
   - 点击 "Generate Domain"
   - 你会得到一个类似 `your-app.up.railway.app` 的地址

#### 方式二：使用 Railway CLI

```bash
# 1. 安装 Railway CLI
npm install -g @railway/cli

# 或使用 Homebrew (Mac)
brew install railway

# 2. 登录
railway login

# 3. 初始化项目
cd /Users/donson/Documents/projects/yuque_article_fetcher
railway init

# 4. 关联 GitHub 仓库
railway link

# 5. 部署
railway up
```

---

## ⚙️ 配置环境变量（推荐）

为了安全，建议将 API Key 设置为环境变量。

### 在 Railway 上设置

1. 进入你的 Railway 项目
2. 点击 "Variables" 标签
3. 点击 "New Variable"
4. 添加以下变量：
   - **变量名**: `ARK_API_KEY`
   - **值**: `0892d12b-a090-4ce2-aeb4-4179b2e99ecb`
5. 点击 "Add"
6. Railway 会自动重新部署

### 修改代码使用环境变量

修改 `app.py`：

```python
import os

# 从环境变量读取 API Key，如果没有则使用默认值
ARK_API_KEY = os.getenv('ARK_API_KEY', '0892d12b-a090-4ce2-aeb4-4179b2e99ecb')
```

---

## 📊 监控和管理

### 查看日志

1. 进入 Railway 项目
2. 点击 "Deployments" 标签
3. 选择最新的部署
4. 点击 "View Logs"
5. 可以实时查看应用运行日志

### 查看指标

- **CPU 使用率**
- **内存使用**
- **网络流量**
- **请求数量**

### 重新部署

**自动部署**：
- 每次推送代码到 GitHub，Railway 会自动重新部署

**手动部署**：
1. 进入 Railway 项目
2. 点击 "Deployments"
3. 点击 "Deploy" 按钮

---

## 🔄 更新应用

每次修改代码后：

```bash
# 1. 提交更改
git add .
git commit -m "更新说明"

# 2. 推送到 GitHub
git push

# 3. Railway 会自动检测并重新部署
```

---

## 🌐 自定义域名（可选）

### 使用 Railway 提供的域名

Railway 会自动生成一个域名，格式：`your-app.up.railway.app`

### 使用自己的域名

1. 在 Railway 项目中，点击 "Settings" → "Domains"
2. 点击 "Custom Domain"
3. 输入你的域名，例如：`article.yourdomain.com`
4. Railway 会提供 CNAME 记录
5. 在你的域名服务商添加 CNAME 记录：
   - **类型**: CNAME
   - **名称**: article（或你想要的子域名）
   - **值**: Railway 提供的地址
6. 等待 DNS 生效（通常 5-30 分钟）

---

## 💰 费用说明

### 免费额度

Railway 提供：
- **$5 免费额度/月**
- 包含：
  - 500 小时运行时间
  - 100GB 出站流量
  - 8GB 内存
  - 8 vCPU

### 对于你的应用

假设：
- 每天使用 2 小时
- 每月约 60 小时
- 流量很少

**结论**: 免费额度完全够用！

### 如果超出免费额度

- 可以绑定信用卡，按使用量付费
- 大约 $0.000231/分钟
- 对于个人项目，通常每月不超过 $5-10

---

## 🐛 常见问题

### 1. 部署失败：找不到 gunicorn

**原因**: requirements.txt 中没有 gunicorn

**解决**:
```bash
echo "gunicorn" >> requirements.txt
git add requirements.txt
git commit -m "Add gunicorn"
git push
```

### 2. 应用启动失败

**检查日志**:
1. 进入 Railway 项目
2. 查看 "Logs"
3. 找到错误信息

**常见原因**:
- Python 版本不兼容
- 依赖安装失败
- 代码有语法错误

### 3. AI 总结超时

Railway 没有严格的超时限制，但如果总结时间过长：

**优化建议**:
- 限制文章内容长度（已在代码中限制为 8000 字符）
- 使用更快的 AI 模型
- 添加超时处理

### 4. 无法访问应用

**检查**:
1. 确认部署状态是 "Active"
2. 确认域名已生成
3. 检查防火墙设置
4. 查看日志是否有错误

---

## 🎯 部署检查清单

部署前确认：

- [ ] 代码已推送到 GitHub
- [ ] requirements.txt 包含所有依赖
- [ ] Procfile 文件存在
- [ ] Railway 账号已创建
- [ ] 项目已在 Railway 上创建
- [ ] 环境变量已设置（如果需要）

部署后确认：

- [ ] 部署状态显示 "Active"
- [ ] 可以访问生成的域名
- [ ] 可以正常抓取文章
- [ ] AI 总结功能正常
- [ ] 可以下载文件

---

## 🆚 其他部署选项对比

| 平台 | 优点 | 缺点 | 适合场景 |
|------|------|------|----------|
| **Railway** | 无时间限制、易用 | 免费额度有限 | ✅ 你的项目 |
| Vercel | 免费额度大、CDN快 | 10秒超时 | 前端项目 |
| Render | 免费计划、稳定 | 冷启动慢 | 小型项目 |
| Heroku | 成熟稳定 | 免费计划取消 | 企业项目 |
| PythonAnywhere | Python专用 | 配置复杂 | Python学习 |

---

## 🎉 完成！

部署成功后，你会得到一个类似这样的 URL：
```
https://yuque-article-fetcher.up.railway.app
```

你可以：
- ✅ 在任何地方访问你的应用
- ✅ 分享给朋友使用
- ✅ 随时更新代码，自动部署
- ✅ 查看实时日志和监控

---

## 📞 需要帮助？

- Railway 文档: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- GitHub Issues: 在你的仓库创建 Issue

---

## 🚀 下一步

1. **优化性能**: 添加缓存、优化数据库查询
2. **添加功能**: 批量处理、历史记录、用户系统
3. **监控告警**: 设置错误通知、性能监控
4. **备份数据**: 定期备份重要数据

需要帮助执行部署步骤吗？
