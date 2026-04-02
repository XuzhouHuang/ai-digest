# AI Digest 额外内容源抓取指令

## 1. ArXiv 热门论文
用 web_search 搜索以下关键词（选最相关的结果）：
- "huggingface daily papers"
- "arxiv AI top papers today"
- "machine learning papers trending"

提取 3-5 篇最热门论文：标题、作者（如有）、一句话摘要、链接

## 2. GitHub Trending AI 项目
用 web_fetch 抓取 https://github.com/trending?since=daily
筛选包含以下关键词的项目：llm, agent, model, ai, ml, gpt, claude, transformer, copilot
提取 5-10 个：项目名、描述、stars 数、链接

## 3. AI 产品发布
用 web_search 搜索：
- "AI tool product launch this week"
- "new AI startup launch 2026"
提取 3-5 个新产品：名称、一句话描述、链接

## 4. 中文 AI 动态
用 web_search 搜索：
- "AI 大模型 最新发布"
- "国产大模型 新功能 2026"
- "量子位 AI 新闻"
提取 3-5 条：标题、来源、链接

## 输出格式
将所有内容整理成 markdown，分四个板块，每条附链接。
