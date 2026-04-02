# AI Digest 额外内容源抓取指令

> 版本: 2.0 | 更新: 增加链接真实性硬性要求

## ⚠️ 铁律

- **每条内容必须附真实、可访问的链接**
- **搜索不到真实来源的内容，不写入日报**
- **禁止使用列表页/首页链接代替具体内容链接**

## 1. ArXiv / HuggingFace 热门论文

用 web_search 搜索：
- "huggingface daily papers today"
- "arxiv AI top papers this week"
- "site:huggingface.co/papers 2026"

**要求：**
- 每篇论文必须链到 `huggingface.co/papers/XXXX.XXXXX` 或 `arxiv.org/abs/XXXX.XXXXX` 格式的单篇页面
- 提取：论文标题、一句话摘要、链接
- 目标：3-5 篇
- **如果搜索结果只有月度列表页，用 web_fetch 打开列表页提取具体论文链接**

## 2. GitHub Trending AI 项目

用 web_search 搜索：
- "github trending AI LLM agent today"
- "github.com/trending AI projects"

**要求：**
- 每个项目链接必须是 `github.com/owner/repo` 格式
- 用 web_fetch 验证仓库确实存在（HTTP 200）
- 提取：项目名、描述、stars（如有）、链接
- 目标：3-5 个

## 3. AI 产品/工具发布

用 web_search 搜索：
- "AI tool product launch this week 2026"
- "new AI startup launch"
- "Product Hunt AI"

**要求：**
- 每个产品附官网或报道链接
- 目标：3-5 个

## 4. 中文 AI 动态

用 web_search 搜索：
- "AI 大模型 最新 本周"
- "国产大模型 新功能 2026"
- "量子位 AI 新闻"
- "36氪 AI"

**要求：**
- 附知乎/36氪/量子位等具体文章链接
- 目标：3-5 条

## 输出格式

将所有内容整理成 markdown，分四个板块，每条附**真实链接**。
