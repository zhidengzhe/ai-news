#!/usr/bin/env python3
"""从 stdin 读取 JSON 数组，追加到 index.html 的 newsData 中。"""
import sys, json, re

INDEX = "/home/zhidengzhe/projects/ai-news-site/index.html"
PROJECT = "/home/zhidengzhe/projects/ai-news-site"

# 读取 stdin
raw = sys.stdin.read().strip()
if not raw:
    print("No data on stdin, skipping")
    sys.exit(0)

try:
    new_items = json.loads(raw)
    if not isinstance(new_items, list):
        raise ValueError("Input must be a JSON array")
except (json.JSONDecodeError, ValueError) as e:
    print(f"Invalid JSON input: {e}")
    sys.exit(1)

# 读取 index.html
with open(INDEX, 'r') as f:
    content = f.read()

# 找到 newsData 数组位置
marker = 'const newsData = ['
pos = content.index(marker) + len(marker)

# 构建插入内容
indent = '  '
insertion = ''
for item in new_items:
    insertion += f'{indent}{json.dumps(item, ensure_ascii=False)},\n'

# 如果数组非空（已有数据），在第一个现有元素前插入
# 如果数组为空（只有 ]），在 ] 前插入
new_content = content[:pos] + '\n' + insertion + content[pos:]

with open(INDEX, 'w') as f:
    f.write(new_content)

print(f"Appended {len(new_items)} items to index.html")

# 自动 git 推送
import subprocess, os
os.chdir(PROJECT)
subprocess.run(["git", "add", "index.html"], capture_output=True)
commit_msg = f"auto: {new_items[0].get('date','?')} 早报更新 ({len(new_items)}条)"
result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True)
if result.returncode == 0:
    subprocess.run(["git", "push"], capture_output=True)
    print("Git pushed")
else:
    print("Git commit skipped (no changes or git not configured)")
