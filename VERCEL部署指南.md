# Vercel 部署指南

## 📋 前置准备

1. **注册 Vercel 账号**
   - 访问 [vercel.com](https://vercel.com)
   - 使用 GitHub、GitLab 或 Bitbucket 账号登录

2. **安装 Git**（如果还没有）
   - Mac: `brew install git`
   - 或从 [git-scm.com](https://git-scm.com) 下载

3. **创建 GitHub 仓库**（推荐）
   - 登录 [github.com](https://github.com)
   - 点击右上角 "+" → "New repository"
   - 填写仓库名称，例如：`yuque-article-fetcher`
   - 选择 Public 或 Private
   - 点击 "Create repository"

## 🚀 部署步骤

### 方法一：通过 GitHub 部署（推荐）

#### 1. 初始化 Git 仓库并推送到 GitHub

在项目目录下执行：

```bash
cd /Users/donson/Documents/projects/yuque_article_fetcher

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 关联远程仓库（替换成你的 GitHub 仓库地址）
git remote add origin https://github.com/你的用户名/yuque-article-fetcher.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

#### 2. 在 Vercel 上导入项目

1. 登录 [vercel.com](https://vercel.com)
2. 点击 "Add New..." → "Project"
3. 选择 "Import Git Repository"
4. 找到你的 `yuque-article-fetcher` 仓库，点击 "Import"
5. 配置项目：
   - **Framework Preset**: 选择 "Other"
   - **Root Directory**: 保持默认 `./`
   - **Build Command**: 留空
   - **Output Directory**: 留空
6. 点击 "Deploy"

#### 3. 等待部署完成

- Vercel 会自动检测 Python 项目
- 部署过程大约需要 1-3 分钟
- 部署成功后会显示项目 URL

### 方法二：使用 Vercel CLI 部署

#### 1. 安装 Vercel CLI

```bash
npm install -g vercel
```

#### 2. 登录 Vercel

```bash
vercel login
```

#### 3. 部署项目

```bash
cd /Users/donson/Documents/projects/yuque_article_fetcher
vercel
```

按照提示操作：
- 选择 "Set up and deploy"
- 选择你的 Vercel 账号
- 确认项目名称
- 确认项目路径
- 等待部署完成

## ⚙️ 环境变量配置（可选）

如果你想将 API Key 设置为环境变量：

1. 在 Vercel 项目页面，点击 "Settings"
2. 选择 "Environment Variables"
3. 添加以下变量：
   - `ARK_API_KEY`: `0892d12b-a090-4ce2-aeb4-4179b2e99ecb`
4. 点击 "Save"
5. 重新部署项目

然后修改 `app.py`：

```python
import os
ARK_API_KEY = os.getenv('ARK_API_KEY', '0892d12b-a090-4ce2-aeb4-4179b2e99ecb')
```

## 📝 注意事项

### 1. **Vercel 的限制**

- **执行时间限制**: 
  - Hobby 计划：10秒
  - Pro 计划：60秒
  - 如果 AI 总结时间过长可能会超时

- **文件系统**:
  - Vercel 是无服务器环境，文件系统是只读的
  - 临时文件会在请求结束后被清理

### 2. **可能遇到的问题**

#### 问题1：AI 总结超时
**解决方案**：
- 升级到 Vercel Pro 计划
- 或者优化总结逻辑，减少处理时间
- 或者使用其他支持长时间运行的平台（如 Railway、Render）

#### 问题2：依赖安装失败
**解决方案**：
- 确保 `requirements.txt` 中的包都是兼容的
- 检查 Python 版本是否正确

#### 问题3：静态文件无法加载
**解决方案**：
- 确保 `static/` 和 `templates/` 文件夹都已提交到 Git
- 检查 `vercel.json` 配置是否正确

## 🔄 更新部署

### 通过 GitHub 自动部署

每次推送代码到 GitHub，Vercel 会自动重新部署：

```bash
git add .
git commit -m "更新说明"
git push
```

### 通过 CLI 手动部署

```bash
vercel --prod
```

## 🌐 自定义域名（可选）

1. 在 Vercel 项目页面，点击 "Settings"
2. 选择 "Domains"
3. 输入你的域名
4. 按照提示配置 DNS 记录
5. 等待 DNS 生效（通常需要几分钟到几小时）

## 📊 监控和日志

- 在 Vercel 项目页面可以查看：
  - 部署历史
  - 运行日志
  - 性能指标
  - 错误报告

## 🎉 完成！

部署成功后，你会得到一个类似这样的 URL：
- `https://yuque-article-fetcher.vercel.app`

你可以直接访问这个 URL 使用你的应用！

## 💡 替代方案

如果 Vercel 的限制不适合你的需求，可以考虑：

1. **Railway** - 支持长时间运行，更适合 Flask 应用
2. **Render** - 免费计划支持 Web 服务
3. **Heroku** - 经典的 PaaS 平台
4. **PythonAnywhere** - 专门为 Python 应用设计
5. **自己的服务器** - 使用 Nginx + Gunicorn 部署

需要帮助部署到其他平台吗？
