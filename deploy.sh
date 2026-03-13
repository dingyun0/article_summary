#!/bin/bash

echo "🚀 开始部署到 Railway..."
echo ""

# 检查是否在正确的目录
if [ ! -f "app.py" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

# 检查 Git 是否已初始化
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    echo "✅ Git 仓库初始化完成"
    echo ""
fi

# 添加所有文件
echo "📝 添加文件到 Git..."
git add .

# 提交
echo "💾 提交更改..."
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 检查是否已关联远程仓库
if ! git remote | grep -q "origin"; then
    echo "⚠️  尚未关联 GitHub 仓库"
    echo ""
    echo "请按照以下步骤操作："
    echo "1. 在 GitHub 创建新仓库"
    echo "2. 运行以下命令关联仓库："
    echo ""
    echo "   git remote add origin https://github.com/你的用户名/仓库名.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "3. 然后访问 https://railway.app 部署项目"
    exit 0
fi

# 推送到 GitHub
echo "🚢 推送到 GitHub..."
git push

echo ""
echo "✅ 代码已推送到 GitHub！"
echo ""
echo "📋 下一步："
echo "1. 访问 https://railway.app"
echo "2. 登录并创建新项目"
echo "3. 选择 'Deploy from GitHub repo'"
echo "4. 选择你的仓库"
echo "5. 等待部署完成"
echo ""
echo "🎉 完成后你就可以访问你的应用了！"
