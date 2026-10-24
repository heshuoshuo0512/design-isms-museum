# 主义馆 · ISM MUSEUM

一个纯 HTML/CSS/JavaScript 的前端设计主义线上展馆。

- 80 个设计主义展厅
- 大厅、4 行轮播长廊、真实年份时间轴
- 每个展厅包含历史、案例、特征、代码指纹和 CSS 交互标本
- 零框架、零图片、零运行时外部请求
- 首页新增“课程 ↔ 前端专业”双向赋能展区，展示课程语境、交互原型与反思回写的学习闭环
- 反哺机制明确为“命题卡 → 原型对照 → 验证记录 → 课程补丁”四份可回写产物
- 双向赋能区把课内八个母题逐一转译为前端问题、实践约束和课程回写产物
- `knowledge.html` 现代设计知识库：80 个条目索引、8 个课内母题分类与可回写的前端反哺库

## 本地运行

```bash
python3 -m http.server 8787
```

打开 <http://127.0.0.1:8787/>。

## 生成展厅

修改 `data.py` 或 `build.py` 后执行：

```bash
python3 build.py
```

## GitHub Pages

`main` 分支推送会由 `.github/workflows/pages.yml` 自动部署到 GitHub Pages。
