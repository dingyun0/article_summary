let currentArticle = null;
let currentSummary = null;

document.getElementById('fetch-btn').addEventListener('click', fetchAndSummarize);
document.getElementById('download-btn').addEventListener('click', downloadArticle);
document.getElementById('reset-btn').addEventListener('click', resetForm);

const urlInput = document.getElementById('url-input');

urlInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        fetchAndSummarize();
    }
});

urlInput.addEventListener('keydown', function(e) {
    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    const cmdKey = isMac ? e.metaKey : e.ctrlKey;
    
    if (cmdKey && e.key === 'a') {
        e.preventDefault();
        this.select();
    }
    
    if (cmdKey && e.key === 'c') {
        return true;
    }
    
    if (cmdKey && e.key === 'v') {
        return true;
    }
    
    if (cmdKey && e.key === 'x') {
        return true;
    }
    
    if (cmdKey && e.key === 'z') {
        return true;
    }
});

async function fetchAndSummarize() {
    const url = document.getElementById('url-input').value.trim();
    
    if (!url) {
        showError('请输入文章链接');
        return;
    }
    
    if (!isValidUrl(url)) {
        showError('请输入有效的URL链接');
        return;
    }
    
    hideAll();
    showLoading('正在抓取文章...');
    
    try {
        const response = await fetch('/api/fetch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        
        if (!data.success) {
            hideLoading();
            showError('抓取失败: ' + data.error);
            return;
        }
        
        currentArticle = data;
        
        showLoading('AI正在分析文章，请稍候...');
        
        const summaryResponse = await fetch('/api/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: data.title,
                content: data.content
            })
        });
        
        const summaryData = await summaryResponse.json();
        
        hideLoading();
        
        if (summaryData.success) {
            currentSummary = summaryData.summary;
            showPreview(data, summaryData.summary);
            showSuccess('文章抓取和AI总结完成！');
        } else {
            showError('AI总结失败: ' + summaryData.error);
        }
    } catch (error) {
        hideLoading();
        showError('网络错误: ' + error.message);
    }
}

async function downloadArticle() {
    if (!currentArticle || !currentSummary) {
        showError('没有可下载的总结');
        return;
    }
    
    const downloadBtn = document.getElementById('download-btn');
    downloadBtn.disabled = true;
    downloadBtn.textContent = '💾 准备下载...';
    
    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: currentArticle.title,
                content: currentArticle.content,
                url: currentArticle.url,
                summary: currentSummary
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = currentArticle.title + '.md';
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                if (filenameMatch && filenameMatch[1]) {
                    filename = filenameMatch[1].replace(/['"]/g, '');
                }
            }
            
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showSuccess('文件下载成功！请在浏览器下载文件夹中查看。');
        } else {
            const data = await response.json();
            showError('下载失败: ' + data.error);
        }
    } catch (error) {
        showError('下载错误: ' + error.message);
    } finally {
        downloadBtn.disabled = false;
        downloadBtn.textContent = '💾 下载总结文档';
    }
}

function showPreview(article, summary) {
    const now = new Date();
    const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const weekday = weekdays[now.getDay()];
    const dateStr = `${year}年${month}月${day}日 ${weekday}`;
    
    document.getElementById('article-title').textContent = article.title;
    document.getElementById('summary-date').textContent = dateStr;
    document.getElementById('article-url').textContent = article.url;
    document.getElementById('article-url').href = article.url;
    document.getElementById('summary-content').textContent = summary;
    document.getElementById('preview-section').style.display = 'block';
}

function showLoading(text) {
    document.getElementById('loading-text').textContent = text;
    document.getElementById('loading').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = '❌ ' + message;
    errorDiv.style.display = 'block';
    
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

function showSuccess(message) {
    document.getElementById('success-text').textContent = message;
    document.getElementById('success-message').style.display = 'block';
    
    setTimeout(() => {
        document.getElementById('success-message').style.display = 'none';
    }, 5000);
}

function hideAll() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('error-message').style.display = 'none';
    document.getElementById('preview-section').style.display = 'none';
    document.getElementById('success-message').style.display = 'none';
}

function resetForm() {
    document.getElementById('url-input').value = '';
    currentArticle = null;
    currentSummary = null;
    hideAll();
}

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}
