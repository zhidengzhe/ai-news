# AI 每日资讯网站

## 项目目标
把每日 AI 早报（午间+晚间各30条）自动存档到一个可浏览、可搜索的静态网站。

## 技术选型
- **形式**：静态 HTML + JS
- **数据流**：cron 自动推送（早报跑完后自动追加数据）
- **托管**：GitHub Pages（免费）
- **设计**：暖黑 #0d0b0b / 橙 #ff8a5f / 等宽字体

## 当前状态
🟡 网站已上线，sticky 表头待修

## 已完成
- [x] 静态网站（纯 HTML+JS）
- [x] GitHub Pages 部署 → https://zhidengzhe.github.io/ai-news/
- [x] 浏览器端搜索/筛选（日期、领域、公司、关键词）
- [x] 数据结构化（7列，按日期分组）
- [x] 视觉风格：暖黑/橙/等宽/悬停显现/光斑
- [x] 移动端卡片布局响应式
- [x] 标题栏 sticky + 筛选栏合并
- [x] 表头居中 + 列对齐（内容/影响左对齐）
- [x] 日期框宽度 145px
- [x] 正文字体 0.9rem
- [x] 领域名称「具身智能」统一
- [x] 早报 cron deliver 改为 origin（修复微信推送）
- [x] 6/10 数据扩充到 14 条
- [x] 6/12 数据已录入 30 条
- [x] SSH key 推送认证

## 待修
- [ ] sticky 表头：JS 方案已搭，fixed div 透明导致正文穿透（div 缺背景色——6/12 最后一版已补，待验证）
- [ ] 数据管道：cron → 自动写入 index.html newsData 数组
- [ ] 筛选状态持久化（localStorage）

## 项目路径
`~/projects/ai-news-site/`
仓库：`github.com/zhidengzhe/ai-news`
