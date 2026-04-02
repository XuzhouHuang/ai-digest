# AI Digest 每日日报生成流程

> 版本: 2.0 | 更新日期: 2026-04-02 | 更新原因: QA 审查发现链接不真实、内容未验证

## 流程（必须按顺序执行）

```
Step 1: 抓取 → Step 2: 生成 → Step 3: 验证 → Step 4: QA 审查 → Step 5: 发布
```

### Step 1: 抓取原始数据

**follow-builders**:
```bash
cd /usr/lib/node_modules/openclaw/skills/follow-builders/scripts && node prepare-digest.js 2>/dev/null > /tmp/fb-digest.json
```

**额外来源**（按 extra-sources-prompt.md 执行 web_search）

### Step 2: 生成日报 markdown

按 daily-digest-template.md 的板块结构整理内容。

**⚠️ 硬性要求：**
- 每条内容必须附**真实、具体**的来源链接
- 论文必须链到 arxiv 或 HuggingFace **单篇论文页面**，不可链到列表页
- GitHub 项目必须链到**具体仓库页面**
- X 推文链接来自 follow-builders JSON 中的 `url` 字段，不可自行编造
- **禁止杜撰**：如果搜索不到某条内容的真实来源，不写入日报

### Step 3: 链接验证（DevAgent 自查）

生成后、提交审查前，DevAgent 必须：
1. 用 `web_fetch` 抽查至少 **5 条**链接的 HTTP 状态码
2. 状态码非 200 的链接 → 删除该条目或替换为可用链接
3. 验证结果记录在 commit message 中

### Step 4: QA 独立审查

CEO spawn QA Agent，按 qa-agent.md 的审查清单执行：
- frontmatter 完整性
- 板块完整性
- 再次抽查 3 条链接
- 内容准确性
- 格式规范
- Hugo 构建

**QA 结果：**
- ✅ PASS → 进入 Step 5
- ❌ FAIL → 退回 Step 2，DevAgent 修改后重新提交

### Step 5: 发布

**只有 QA PASS 后才可执行：**
```bash
cd /home/openclaw/workspace/ai-digest && git add -A && git commit -m "日报 YYYY-MM-DD [QA PASS]" && git push
```

然后发送 Discord 摘要通知。

---

## 禁止事项

1. ❌ 未经 QA 审查就 push
2. ❌ 链接指向列表页/首页而非具体内容
3. ❌ 杜撰论文名、项目名、推文内容
4. ❌ DevAgent 跳过链接自查步骤
