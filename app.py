#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os
import re
import tempfile
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime._exceptions import ArkAPIError
from dotenv import load_dotenv

load_dotenv()



app = Flask(__name__)
CORS(app)

ARK_API_KEY = os.getenv("DOUBAO_API_KEY", "0892d12b-a090-4ce2-aeb4-4179b2e99ecb")
ARK_MODEL = "doubao-seed-2-0-lite-260215"
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

class ArticleFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.ark_client = Ark(
            base_url=ARK_BASE_URL,
            api_key=ARK_API_KEY
        )
    
    def fetch_article_content(self, url):
        """从指定URL获取文章内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = "Untitled"
            title_tags = ['h1', 'h2', 'title', 'header h1', 'div[class*="title"]', 'div[class*="headline"]']
            
            for tag in title_tags:
                elements = soup.select(tag)
                if elements:
                    title = elements[0].get_text(strip=True)
                    if title:
                        break
            
            content = ""
            content_tags = [
                'article', 'main', 
                'div[class*="content"]', 'div[class*="article"]',
                'div[class*="post-content"]', 'div[class*="article-content"]',
                'div[class*="rich_media_content"]',
                'div[class*="content_main"]', 'div[class*="article_body"]'
            ]
            
            for tag in content_tags:
                elements = soup.select(tag)
                if elements:
                    content = '\n'.join([element.get_text(separator='\n', strip=True) for element in elements])
                    if content:
                        break
            
            if not content:
                content = soup.get_text(separator='\n', strip=True)
            
            return {
                'success': True,
                'title': title,
                'content': content,
                'url': url
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def summarize_with_doubao(self, title, content):
        """进行文章总结"""
        try:
            prompt = f"""# 技术类内容精准全面总结Prompt
你是一名专业的技术内容总结专家，精通技术文章、产品技术测评、新技术科普类内容的核心逻辑，具备极强的技术信息抓取、精准还原、完整梳理能力。

## 核心任务
基于我提供的原文，完成**全面、精准、无遗漏、不敷衍**的深度总结，让我无需通读原文，就能完整掌握全文的所有核心信息。

## 核心执行准则
1.  绝对忠于原文：所有内容100%来自原文，不添加任何原文以外的主观解读、拓展内容，不篡改技术本意、不歪曲作者观点、不编造信息。
2.  全面无遗漏：完整覆盖原文所有核心内容，包括但不限于核心技术原理、关键参数、实测数据、核心观点、优势短板、关键结论、适用场景，禁止只做头尾概括，禁止遗漏关键技术细节与核心信息。
3.  精准不笼统：严格杜绝空洞套话、泛泛而谈的敷衍式总结，技术术语、数据、结论必须和原文完全一致，不简化、不曲解技术内容，清晰讲透核心逻辑，明确区分客观事实与作者的主观判断。
4.  逻辑清晰：根据原文的行文逻辑，用清晰的层级和通顺的语言组织内容，重点信息可加粗突出，关键数据清晰呈现，无需受固定模板限制，适配原文内容选择最优的总结结构。
# title：{title}
# content：{content}
"""
            
            stream = self.ark_client.chat.completions.create(
                model=ARK_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的文章总结助手，擅长提取文章的核心内容并进行全面详细的总结。"},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )
            
            summary = ""
            for chunk in stream:
                if not chunk.choices:
                    continue
                if chunk.choices[0].delta.content:
                    summary += chunk.choices[0].delta.content
            
            return {
                'success': True,
                'summary': summary
            }
        except ArkAPIError as e:
            return {
                'success': False,
                'error': f'豆包API错误: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_download_file(self, title, url, summary):
        """创建临时下载文件，只包含AI总结和原文链接"""
        try:
            from datetime import datetime
            import locale
            
            try:
                locale.setlocale(locale.LC_TIME, 'zh_CN.UTF-8')
            except:
                pass
            
            now = datetime.now()
            weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
            date_str = now.strftime('%Y年%m月%d日')
            weekday_str = weekdays[now.weekday()]
            
            safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
            safe_title = safe_title[:100]
            
            filename = f"{safe_title}_AI总结.md"
            
            file_content = f"# {title}\n\n"
            file_content += f"**总结日期：** {date_str} {weekday_str}\n\n"
            file_content += f"## AI总结\n\n{summary}\n\n"
            file_content += f"---\n\n"
            file_content += f"**原文链接：** {url}\n"
            
            temp_file = tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.md', delete=False)
            temp_file.write(file_content)
            temp_file.close()
            
            return {
                'success': True,
                'filepath': temp_file.name,
                'filename': filename
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

fetcher = ArticleFetcher()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fetch', methods=['POST'])
def fetch_article():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'error': '请提供文章链接'})
    
    result = fetcher.fetch_article_content(url)
    return jsonify(result)

@app.route('/api/summarize', methods=['POST'])
def summarize_article():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    
    if not all([title, content]):
        return jsonify({'success': False, 'error': '缺少必要参数'})
    
    result = fetcher.summarize_with_doubao(title, content)
    return jsonify(result)

@app.route('/api/download', methods=['POST'])
def download_article():
    data = request.json
    title = data.get('title')
    url = data.get('url')
    summary = data.get('summary')
    
    if not all([title, url, summary]):
        return jsonify({'success': False, 'error': '缺少必要参数'})
    
    result = fetcher.create_download_file(title, url, summary)
    
    if result['success']:
        return send_file(
            result['filepath'],
            as_attachment=True,
            download_name=result['filename'],
            mimetype='text/markdown'
        )
    else:
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

app = app
