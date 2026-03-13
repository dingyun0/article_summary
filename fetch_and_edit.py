#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import argparse
import os
import re

class ArticleFetcher:
    def __init__(self):
        # 模拟浏览器请求头，提高抓取成功率
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def fetch_article_content(self, url):
        """从指定URL获取文章内容"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 尝试获取标题
            title = "Untitled"
            # 常见的标题标签
            title_tags = ['h1', 'h2', 'title', 'header h1', 'div[class*="title"]', 'div[class*="headline"]']
            
            for tag in title_tags:
                elements = soup.select(tag)
                if elements:
                    title = elements[0].get_text(strip=True)
                    if title:
                        break
            
            # 尝试获取文章主体内容
            content = ""
            # 常见的文章内容容器标签
            content_tags = [
                'article', 'main', 
                'div[class*="content"]', 'div[class*="article"]',
                'div[class*="post-content"]', 'div[class*="article-content"]',
                'div[class*="rich_media_content"]',  # 微信公众号
                'div[class*="content_main"]', 'div[class*="article_body"]'
            ]
            
            for tag in content_tags:
                elements = soup.select(tag)
                if elements:
                    content = '\n'.join([element.get_text(separator='\n', strip=True) for element in elements])
                    if content:
                        break
            
            # 如果没有找到内容，使用整个页面的文本
            if not content:
                content = soup.get_text(separator='\n', strip=True)
            
            return title, content
        except Exception as e:
            print(f"获取文章内容失败: {e}")
            return None, None
    
    def save_to_local_file(self, title, content, url):
        """将文章内容保存到本地文件"""
        try:
            # 清理文件名，移除特殊字符
            safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
            # 限制文件名长度
            safe_title = safe_title[:100]
            
            # 创建输出目录
            output_dir = "articles"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 生成文件名
            filename = f"{output_dir}/{safe_title}.md"
            
            # 构建文件内容，包含原文链接
            file_content = f"# {title}\n\n"
            file_content += f"## 原文链接\n{url}\n\n"
            file_content += f"## 内容\n{content}\n"
            
            # 写入文件
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            print(f"文件保存成功: {filename}")
            return True
        except Exception as e:
            print(f"保存文件失败: {e}")
            return False
    
    def process_url(self, url):
        """处理单个URL"""
        title, content = self.fetch_article_content(url)
        if title and content:
            return self.save_to_local_file(title, content, url)
        return False

def main():
    parser = argparse.ArgumentParser(description="读取链接文章并保存到本地文件")
    parser.add_argument("url", help="文章链接")
    
    args = parser.parse_args()
    
    fetcher = ArticleFetcher()
    success = fetcher.process_url(args.url)
    
    if success:
        print("任务完成！")
    else:
        print("任务失败！")

if __name__ == "__main__":
    main()
