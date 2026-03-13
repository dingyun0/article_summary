# 文章抓取工具

这个工具可以从指定的URL抓取文章内容（包括微信公众号文章），并将其保存到本地Markdown文件中，同时附上原文链接。

## 功能特点

- 自动从URL抓取文章标题和内容
- 支持抓取微信公众号文章
- 保存为Markdown格式，包含原文链接
- 自动创建输出目录并处理文件名
- 命令行参数支持，方便快速使用

## 环境要求

- Python 3.6+
- 依赖包：requests, beautifulsoup4, lxml

## 安装依赖

```bash
cd /Users/donson/Documents/projects/yuque_article_fetcher
pip install -r requirements.txt
```

## 使用方法

直接运行脚本，传入文章链接：

```bash
python fetch_and_edit.py https://example.com/article
```

### 支持的链接类型

- 普通网站文章
- 微信公众号文章
- 博客文章
- 新闻文章

## 输出结果

脚本会在当前目录创建一个 `articles` 文件夹，并在其中生成以文章标题命名的Markdown文件。文件内容包括：

- 文章标题
- 原文链接
- 文章内容

## 注意事项

- 该工具依赖于BeautifulSoup解析HTML，对于不同网站的结构可能需要调整解析逻辑
- 对于某些需要登录或有反爬措施的网站，可能无法正常抓取
- 微信公众号文章的抓取可能会受到限制，具体取决于公众号的设置

## 示例

```bash
# 示例1：抓取普通网站文章
python fetch_and_edit.py https://www.example.com/article

# 示例2：抓取微信公众号文章
python fetch_and_edit.py https://mp.weixin.qq.com/s/xxxxxxxx
```

## 故障排除

如果遇到抓取失败的情况：
1. 检查网络连接是否正常
2. 确认链接是否可以正常访问
3. 对于微信公众号文章，确保你可以在浏览器中直接访问
4. 如果仍然失败，可能是网站有反爬措施，尝试稍后再试
