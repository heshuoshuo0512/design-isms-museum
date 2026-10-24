# 主义馆 · ISM MUSEUM

一个纯 HTML/CSS/JavaScript 的前端设计主义线上展馆。

- 80 个设计主义展厅
- 大厅、4 行轮播长廊、真实年份时间轴
- 每个展厅包含历史、案例、特征、代码指纹和 CSS 交互标本
- 零框架、零图片、零运行时外部请求

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
