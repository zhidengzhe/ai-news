# AI 每日资讯网站

## 项目目标
把每日 AI 早报（午间+晚间各30条）自动存档到一个可浏览、可搜索的静态网站。

## 技术选型
- **形式**：静态 HTML + JS
- **数据流**：cron 早报 → append-data.py 追加到 index.html newsData → git push 上线
- **托管**：GitHub Pages（免费）
- **设计**：暖黑 #0d0b0b / 橙 #ff8a5f / 等宽字体

## 当前状态
🟢 网站正常运行，数据每日自动更新

## 已完成
- [x] 静态网站（纯 HTML+JS）
- [x] GitHub Pages 部署 → https://zhidengzhe.github.io/ai-news/
- [x] 浏览器端搜索/筛选（日期、领域、公司、关键词）
- [x] 数据结构化（7列，按日期分组）
- [x] 视觉风格：暖黑/橙/等宽/悬停显现/光斑
- [x] 移动端卡片布局响应式
- [x] 标题栏 sticky + 筛选栏合并
- [x] 表头居中 + 列对齐（内容/影响左对齐）
- [x] sticky 表头修复（6/12：div 补背景色 #0d0b0b，正文不再穿透）
- [x] 日期框宽度 145px
- [x] 正文字体 0.9rem
- [x] 领域名称「具身智能」统一
- [x] 早报 cron deliver 改为 origin（修复微信推送）
- [x] 6/10 数据扩充到 14 条
- [x] 6/12 数据已录入 30 条
- [x] SSH key 推送认证
- [x] 数据管道：cron → append-data.py → 自动写入 index.html + git push（6/13 起每日自动运行）
- [x] 去重方案一（6/15：去掉词频≥2限制 + 空指纹跳过）
- [x] 去重方案二（6/16：CJK bigram + 非CJK分词 + 绝对值≥6兜底）

## 已知问题
- （暂无）

## 项目路径
`~/projects/ai-news-site/`
仓库：`github.com/zhidengzhe/ai-news`
