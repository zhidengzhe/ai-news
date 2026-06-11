# AI 资讯网站 实施计划

> **For Hermes:** 按任务顺序执行，完成后更新 PROJECT.md。

**Goal:** 将设计原型改造为可运行的静态网站，实现 cron 自动追加数据和 GitHub Pages 部署。

**Architecture:** 单 HTML 文件，内置 JS 数组存储数据 + 搜索/筛选逻辑。Cron 早报跑完后用脚本往 HTML 文件中追加数据。托管于 GitHub Pages。

**Tech Stack:** HTML + CSS + Vanilla JS，Bash 脚本追加数据，GitHub Pages 部署。

---

## 任务 1：将原型改造为正式版本（数据驱动）

**Objective:** 将 prototype.html 中的硬编码示例数据改为 JS 数组驱动，空数组，等 cron 填入。

**Files:**
- 创建: `~/projects/ai-news-site/index.html`

**Steps:**

### Step 1: 从 prototype.html 复制为 index.html

```bash
cp ~/projects/ai-news-site/prototype.html ~/projects/ai-news-site/index.html
```

### Step 2: 在 index.html 中添加数据结构

在 `</style>` 之后、`<body>` 之前插入：

```html
<script>
// 数据结构：每条含 7 个字段
// { date, field, company, person, content, impact, source }
const newsData = [];
</script>
```

### Step 3: 清空示例数据，改为 JS 渲染

删除 `<tbody>` 内的所有硬编码行（`<tr class="date-group">` 和 `<tr>` 数据行），替换为 JS 渲染逻辑。

在 `<tbody>` 内只留占位 ID：

```html
<tbody id="news-body"></tbody>
```

在 `</table>` 后添加渲染函数：

```javascript
function renderTable(data) {
  const tbody = document.getElementById('news-body');
  tbody.innerHTML = '';
  if (data.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:48px;color:var(--muted)">暂无数据，等待首次早报推送</td></tr>';
    return;
  }
  // 按日期分组，降序
  const grouped = {};
  data.forEach(item => {
    if (!grouped[item.date]) grouped[item.date] = [];
    grouped[item.date].push(item);
  });
  const dates = Object.keys(grouped).sort().reverse();
  dates.forEach(date => {
    const count = grouped[date].length;
    tbody.innerHTML += `<tr class="date-group"><td colspan="7">${date} · ${count}条</td></tr>`;
    grouped[date].forEach(item => {
      tbody.innerHTML += `
        <tr>
          <td class="date">${date.slice(5)}</td>
          <td class="field">${item.field}</td>
          <td class="company">${item.company || ''}</td>
          <td class="person">${item.person || ''}</td>
          <td class="content">${item.content}</td>
          <td class="impact">${item.impact}</td>
          <td class="source">${item.source}</td>
        </tr>`;
    });
  });
}

// 初始化渲染
renderTable(newsData);
```

### Step 4: 在正式版中保留示例数据以便预览

`newsData` 数组暂时保留 2-3 条示例数据，确保页面打开就能看到效果。等 cron 机制就绪后再清空。

### Step 5: 浏览器打开验证

```bash
explorer.exe ~/projects/ai-news-site/index.html
```

**验证:** 表格正常渲染，筛选栏可见，无报错。

---

## 任务 2：实现搜索/筛选功能

**Objective:** 搜索框和下拉筛选器联动，实时过滤表格。

**Files:**
- 修改: `~/projects/ai-news-site/index.html`

**Steps:**

### Step 1: 给筛选控件加 ID

```html
<input type="text" list="dates" id="filter-date" placeholder="日期">
<select id="filter-field">
  <option value="">全部领域</option>
  ...
</select>
<select id="filter-company">
  <option value="">全部公司</option>
  ...
</select>
<input type="text" id="filter-keyword" placeholder="搜索关键词">
```

### Step 2: 添加筛选逻辑

```javascript
function filterData() {
  const dateVal = document.getElementById('filter-date').value;
  const fieldVal = document.getElementById('filter-field').value;
  const companyVal = document.getElementById('filter-company').value;
  const keyword = document.getElementById('filter-keyword').value.toLowerCase();

  let filtered = newsData;
  if (dateVal) filtered = filtered.filter(item => item.date === dateVal);
  if (fieldVal) filtered = filtered.filter(item => item.field === fieldVal);
  if (companyVal) filtered = filtered.filter(item => item.company === companyVal);
  if (keyword) filtered = filtered.filter(item =>
    item.content.includes(keyword) || item.impact.includes(keyword) ||
    item.company.includes(keyword) || item.person.includes(keyword)
  );
  renderTable(filtered);
}

// 绑定事件
['filter-date','filter-field','filter-company','filter-keyword'].forEach(id => {
  document.getElementById(id).addEventListener(id === 'filter-keyword' ? 'input' : 'change', filterData);
});
```

### Step 3: 验证筛选

**验证:** 选「芯片」领域 → 只显示芯片相关行；输入「IPO」→ 只显示含 IPO 的行。

---

## 任务 3：建立 cron 自动追加数据机制

**Objective:** 每次午间/晚间早报跑完后，自动将新数据追加到 index.html 的 `newsData` 数组中。

**Files:**
- 创建: `~/projects/ai-news-site/scripts/append-data.sh`

**Steps:**

### Step 1: 创建追加脚本

```bash
#!/bin/bash
# 用法: echo '[{...},{...}]' | bash scripts/append-data.sh
# 从 stdin 读取 JSON 数组，追加到 index.html 的 newsData 中

INDEX="$HOME/projects/ai-news-site/index.html"
INPUT=$(cat)

# 在 newsData 数组末尾追加，匹配模式: const newsData = [...];
# 策略：找到 newsData 数组的 ]，在前面插入新数据
python3 -c "
import sys, json

html_path = '$INDEX'
new_items = json.loads(sys.stdin.read())

with open(html_path, 'r') as f:
    content = f.read()

# 找到 const newsData = [ 的位置
marker = 'const newsData = ['
pos = content.index(marker) + len(marker)

# 如果数组非空，找最后一个 ]; 的位置（newsData 的结束）
# 在 ] 前插入新数据
end_pos = content.index('];', pos)
indent = '  '
insertion = ''
for item in new_items:
    insertion += f'{indent}{json.dumps(item, ensure_ascii=False)},\n'

new_content = content[:pos] + '\n' + insertion + content[pos:]

with open(html_path, 'w') as f:
    f.write(new_content)

print(f'Appended {len(new_items)} items')
"
```

### Step 2: 测试追加

```bash
echo '[{"date":"2026-06-11","field":"测试","company":"TestCo","person":"张三","content":"测试内容","impact":"测试影响","source":"Test"}]' | bash ~/projects/ai-news-site/scripts/append-data.sh
```

**验证:** 打开 index.html，表格中应出现新行。

### Step 3: 修改早报 cron 任务，增加写入逻辑

在午间/晚间 cron prompt 末尾追加指令：

```
搜索完成后，除了分3批推送到微信，还需将每条简报整理为 JSON 数组，
通过 terminal 执行: echo '[JSON数组]' | bash ~/projects/ai-news-site/scripts/append-data.sh
```

### Step 4: 运行一次午间 cron 验证

```bash
cronjob action=run job_id=2f774029efda
```

**验证:** 检查 index.html 是否出现新数据，同时检查 GitHub Pages（部署后再验）。

---

## 任务 4：GitHub Pages 部署

**Objective:** 将 index.html 部署到 GitHub Pages，获得公开 URL。

**Prerequisite:** 需要一个 GitHub 账号和仓库名（如 `zhidengzhe/ai-news`）。

**Steps:**

### Step 1: 初始化 Git 仓库

```bash
cd ~/projects/ai-news-site
git init
git add index.html
git commit -m "init: AI 每日资讯网站"
```

### Step 2: 推送到 GitHub

```bash
git remote add origin git@github.com:zhidengzhe/ai-news.git
git branch -M main
git push -u origin main
```

### Step 3: 启用 GitHub Pages

在 GitHub 仓库 Settings → Pages → Source: Deploy from a branch → Branch: main → / (root) → Save。

### Step 4: 验证部署

访问 `https://zhidengzhe.github.io/ai-news/`

**验证:** 页面正常加载，数据显示正确。

### Step 5: 后续每次 cron 追加数据后自动推送

在上一步 append-data.sh 末尾追加：

```bash
cd ~/projects/ai-news-site
git add index.html
git commit -m "auto: $(date +%Y-%m-%d) 早报更新"
git push
```

---

## 执行顺序

1. 任务 1 → 改造原型为数据驱动
2. 任务 2 → 搜索/筛选
3. 任务 3 → cron 自动追加
4. 任务 4 → GitHub Pages 部署

---

## 验证清单

- [ ] index.html 浏览器打开正常显示
- [ ] 筛选器联动过滤
- [ ] cron 追加数据后刷新页面可见新行
- [ ] GitHub Pages URL 可访问
