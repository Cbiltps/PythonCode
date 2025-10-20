# 网页爬虫功能说明

## 🎯 功能概述

这个爬虫工具实现了以下完整的工作流程：

1. **爬取网页HTML** - 下载完整的网页内容
2. **下载所有图片** - 自动下载网页中的所有图片和GIF
3. **自动转换Markdown** - 将HTML转换为Markdown格式
4. **智能图片引用** - Markdown中的图片自动引用本地下载的图片

## 📁 输出目录结构

```
PythonCode/
├── html/           # HTML文件
│   └── domain_页面标题.html
├── images/         # 下载的图片（保留原始文件名）
│   ├── banner.jpg
│   ├── logo.png
│   └── photo.gif
└── markdown/       # 转换后的Markdown文件
    └── domain_页面标题.md  （图片链接已替换为 ../images/文件名）
```

## ✨ 核心特性

### 1. 保持图片顺序和位置
- 图片按HTML中出现的顺序下载
- 在Markdown中保持原有的位置和顺序
- 不会打乱图片的排列

### 2. 保留原始文件名
- 优先使用URL中的原始文件名
- 如果URL没有文件名，则使用 `image_001.jpg` 格式
- 自动处理文件名冲突（添加序号后缀）

### 3. 智能图片引用
- 自动替换图片URL为本地相对路径
- 使用 `../images/文件名` 格式
- Markdown中的图片可以正常显示

### 4. 支持多种图片属性
从以下属性提取图片URL：
- `src` - 标准属性
- `data-src` - 懒加载
- `data-original` - 原图
- `data-lazy-src` - 延迟加载

### 5. 支持多种图片格式
- JPG/JPEG
- PNG
- GIF
- WebP
- BMP
- SVG

## 🚀 使用方法

### 1. 配置URL
在 `simple_scraper.py` 中修改 `TARGET_URL_SIMPLE`：

```python
TARGET_URL_SIMPLE = "https://example.com/your-page"
```

### 2. 运行爬虫
```bash
python web_scrapy/simple_scraper.py
```

### 3. 查看结果
- HTML文件：`html/` 目录
- 图片文件：`images/` 目录
- Markdown文件：`markdown/` 目录

## 📋 执行流程

```
1. 爬取网页 → 保存HTML
          ↓
2. 解析HTML → 提取图片URL列表（保持顺序）
          ↓
3. 下载图片 → 保存到images/（保留原始文件名）
          ↓
4. 创建映射 → {原URL: 本地文件名}
          ↓
5. 转换HTML → 替换图片URL为本地路径
          ↓
6. 生成MD → 保存到markdown/
```

## 🔧 技术实现

### 图片顺序保持
使用**有序列表** + **字典映射**：
```python
img_urls_ordered = []        # 保持顺序
img_url_to_filename = {}     # URL映射到本地文件名
```

### 图片URL替换
1. 解析HTML，找到所有 `<img>` 标签
2. 将原始URL转换为绝对URL
3. 查找映射表，替换为本地路径 `../images/文件名`
4. 转换修改后的HTML为Markdown

### 相对路径设计
```
markdown/
  └── page.md  ← 在这里
images/
  └── photo.jpg  ← 引用这里

使用: ../images/photo.jpg
```

## 📦 依赖项

```toml
dependencies = [
    "requests",           # HTTP请求
    "beautifulsoup4",     # HTML解析
    "markdownify",        # HTML转Markdown
    "zstandard",          # 压缩支持
]
```

## 💡 示例输出

### Markdown文件内容
```markdown
# 页面标题

这是一段文字。

![图片描述](../images/banner.jpg)

更多内容...

![另一张图片](../images/logo.png)
```

### 控制台输出
```
正在爬取: https://example.com
✅ 成功保存HTML文件: html/example.com_page.html
📄 页面标题: Example Page
📊 文件大小: 12345 字符

🖼️  开始下载图片...
🔍 发现 5 个图片标签
📸 共找到 5 个唯一图片URL（按HTML中出现顺序）
  ✓ 下载图片: banner.jpg (15234 bytes)
  ✓ 下载图片: logo.png (3456 bytes)
  ...

✅ 成功下载 5 张图片到 images/ 文件夹

📝 开始转换为Markdown...
🔄 替换了 5 个图片链接为本地路径
✅ 成功转换为Markdown: markdown/example.com_page.md

🎉 爬取完成！
📁 HTML文件已保存到 html/ 文件夹
🖼️  图片文件已保存到 images/ 文件夹
📝 Markdown文件已保存到 markdown/ 文件夹（图片链接已替换为本地路径）
```

## ⚠️ 注意事项

1. **图片顺序**：严格按照HTML中的出现顺序下载和引用
2. **去重处理**：相同URL的图片只下载一次
3. **文件名冲突**：自动添加序号后缀避免覆盖
4. **相对路径**：Markdown使用相对路径，便于项目迁移
5. **懒加载支持**：自动处理各种懒加载属性

## 🎓 适用场景

- 📚 技术文档归档
- 📰 文章内容保存
- 🎨 图文素材采集
- 💾 网页离线浏览
- 📖 知识库构建
