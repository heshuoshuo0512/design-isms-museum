# -*- coding: utf-8 -*-
"""生成现代设计全书：全局设计史档案 + 课内补充视角。"""

import json
import os

from data import ISMS
from knowledge_data import COURSE_AXES, ISM_AXES, ISM_BRIDGES


BOOK_STAGES = [
    {
        'no': '01',
        'period': '工业化之前',
        'title': '手工、装饰与生活',
        'text': '材料、工艺、纹样和日常生活彼此相连，形式首先从制作与使用中长出来。',
    },
    {
        'no': '02',
        'period': '1800s → 1910s',
        'title': '机器带来的冲突',
        'text': '工业生产扩大了设计的规模，也带来手工、质量、标准和社会阶层之间的新矛盾。',
    },
    {
        'no': '03',
        'period': '1910s → 1950s',
        'title': '现代主义建立秩序',
        'text': '包豪斯、构成主义、风格派等方向尝试用功能、结构、技术和网格组织现代生活。',
    },
    {
        'no': '04',
        'period': '1950s → 1980s',
        'title': '消费、媒介与反叛',
        'text': '大众媒体和消费社会让图像加速复制，波普、达达、孟菲斯与反设计开始质疑单一秩序。',
    },
    {
        'no': '05',
        'period': '1990s → 2010s',
        'title': '网页成为新材料',
        'text': '浏览器、像素、界面和算法让设计从物件扩展到可交互、可更新的数字环境。',
    },
    {
        'no': '06',
        'period': '当下与以后',
        'title': '系统、身份与责任',
        'text': '设计面对无障碍、环境、文化来源、人工智能和平台权力，形式必须接受责任检验。',
    },
]


def _record(m):
    return {
        'slug': m['slug'],
        'no': m['no'],
        'zh': m['zh'],
        'en': m['en'],
        'era': m['era'],
        'period': m['period'],
        'manifesto': m['manifesto'],
        'prologue': m.get('prologue', ''),
        'history': m['history'],
        'reps': m['reps'],
        'traits': [[name, desc] for name, desc in m.get('traits', [])],
        'keywords': m['keywords'],
        'code': m.get('code', ''),
        'timeline': [[year, text] for year, text in m.get('tl', [])],
        'specimens': [cap for cap, _css, _js in m.get('exhibits', [])],
        'axes': ISM_AXES[m['slug']],
        **ISM_BRIDGES[m['slug']],
    }


def _json_script(value):
    """让 JSON 安全地嵌入 script[type=application/json]。"""
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{color-scheme:dark;--bg:#0c0d10;--paper:#15171d;--paper-2:#1b1e26;--line:#303440;--muted:#898c98;--text:#efeff4;--yellow:#ffd23f;--cyan:#7df9ff;--pink:#ff71ce;--mint:#a7ffea}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:-apple-system,"Helvetica Neue","PingFang SC","Noto Sans SC",sans-serif;line-height:1.65;overflow-x:hidden}
a{color:inherit}button,input{font:inherit}button{cursor:pointer}
.book-top{max-width:1280px;margin:0 auto;padding:22px 5vw 0;display:flex;align-items:center;justify-content:space-between;gap:20px;color:#7f828d;font:12px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em}.book-top a{text-decoration:none}.book-top a:hover{color:var(--yellow)}.book-top nav{display:flex;gap:16px;flex-wrap:wrap}
.book-cover{max-width:1280px;margin:0 auto;padding:88px 5vw 74px;position:relative;overflow:hidden}.book-cover:before{content:"";position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,210,63,.08),transparent 38%),radial-gradient(circle at 90% 50%,rgba(125,249,255,.11),transparent 30%);pointer-events:none}.book-cover>*{position:relative}.book-kicker{color:#7f828d;font:11px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.24em;margin-bottom:18px}.book-cover h1{font-size:clamp(50px,10vw,118px);line-height:.95;letter-spacing:-.07em;max-width:900px}.book-cover h1 em{font-style:normal;color:var(--yellow)}.book-lede{max-width:780px;margin-top:24px;color:#b5b7c0;font-size:16px;line-height:2}.book-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:30px}.book-action{display:inline-flex;align-items:center;min-height:44px;padding:10px 18px;border:1px solid #3c404c;border-radius:99px;text-decoration:none;font-size:13px}.book-action:hover{border-color:var(--cyan);transform:translateY(-2px)}.book-action.primary{background:var(--yellow);border-color:var(--yellow);color:#111;font-weight:800}.book-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;max-width:700px;margin-top:48px}.book-stat{padding:15px 17px;border-top:2px solid var(--line);background:rgba(255,255,255,.025)}.book-stat:nth-child(1){border-color:var(--yellow)}.book-stat:nth-child(2){border-color:var(--cyan)}.book-stat:nth-child(3){border-color:var(--pink)}.book-stat strong{display:block;font-size:28px;line-height:1.1}.book-stat span{display:block;margin-top:5px;color:#898c98;font-size:12px}
.book-main{max-width:1280px;margin:0 auto}.book-section{padding:68px 5vw 0}.book-section:last-child{padding-bottom:94px}.section-head{display:flex;align-items:end;justify-content:space-between;gap:24px;margin-bottom:24px}.section-kicker{color:#777b86;font:11px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.22em;margin-bottom:8px}.section-head h2{font-size:clamp(27px,4vw,46px);line-height:1.1}.section-head>p{max-width:560px;color:#8c8f9a;font-size:13px;line-height:1.9}
.contents-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.contents-link{display:block;padding:18px;border:1px solid var(--line);border-radius:12px;background:rgba(255,255,255,.025);text-decoration:none;transition:border-color .2s,transform .2s}.contents-link:hover{border-color:var(--yellow);transform:translateY(-3px)}.contents-link b{display:block;color:var(--yellow);font:11px ui-monospace,SFMono-Regular,Menlo,monospace;margin-bottom:9px}.contents-link span{font-size:14px;color:#dedfe5}.contents-link small{display:block;margin-top:6px;color:#777b86;font-size:11px;line-height:1.6}
.arc{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.arc-step{min-height:190px;padding:18px 14px;border-right:1px solid var(--line);position:relative}.arc-step:last-child{border-right:0}.arc-step b{display:block;color:var(--yellow);font:11px ui-monospace,SFMono-Regular,Menlo,monospace;margin-bottom:20px}.arc-step strong{display:block;font-size:16px;line-height:1.35}.arc-step em{display:block;margin-top:7px;color:var(--cyan);font:11px ui-monospace,SFMono-Regular,Menlo,monospace;font-style:normal}.arc-step p{margin-top:13px;color:#858894;font-size:11.5px;line-height:1.75}
.lens-note{padding:14px 16px;margin-bottom:18px;border-left:2px solid var(--cyan);background:rgba(125,249,255,.04);color:#aeb1bc;font-size:12.5px;line-height:1.8}.lens-note b{color:var(--cyan)}.lens-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.lens-card{border:1px solid var(--line);border-radius:12px;background:rgba(255,255,255,.025);overflow:hidden}.lens-card[open]{border-color:#4a4d5b}.lens-card summary{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:17px 18px;list-style:none;cursor:pointer}.lens-card summary::-webkit-details-marker{display:none}.lens-card summary:after{content:"+";color:#777}.lens-card[open] summary:after{content:"−";color:var(--yellow)}.lens-card summary b{color:var(--yellow);font:11px ui-monospace,SFMono-Regular,Menlo,monospace}.lens-card summary span{font-size:15px;color:#e4e5ea}.lens-body{padding:0 18px 18px}.lens-focus{color:#aeb1bc;font-size:12.5px;line-height:1.8;padding-bottom:13px;border-bottom:1px solid var(--line)}.lens-columns{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:13px}.lens-columns b{display:block;color:#ddd;font-size:11px;margin-bottom:5px}.lens-columns p{color:#858894;font-size:11.5px;line-height:1.75}.lens-count{display:flex;flex-wrap:wrap;gap:5px;margin-top:14px}.lens-count span{padding:4px 7px;border-radius:5px;background:#20232c;color:#aeb1bc;font-size:10.5px}.lens-jump{margin-top:14px;border:0;background:none;color:var(--cyan);font-size:11px;padding:0}.lens-jump:hover{text-decoration:underline}
.reader-tools{padding:17px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.025)}.reader-tools-row{display:flex;gap:10px;align-items:center}.reader-search{position:relative;flex:1}.reader-search input{width:100%;height:44px;padding:0 14px 0 38px;border:1px solid #3a3e4a;border-radius:9px;background:#101217;color:#eee;outline:none}.reader-search input:focus{border-color:var(--cyan);box-shadow:0 0 0 3px rgba(125,249,255,.08)}.reader-search span{position:absolute;left:13px;top:9px;color:#777;font-size:17px}.reader-count{color:#777;font-size:11px;white-space:nowrap}.reader-filters{display:flex;gap:6px;flex-wrap:wrap;margin-top:12px}.reader-filter{padding:6px 9px;border:1px solid #363a46;border-radius:99px;background:none;color:#9497a3;font-size:10.5px}.reader-filter:hover,.reader-filter.active{border-color:var(--yellow);background:rgba(255,210,63,.1);color:#eee}.reader-filter.active span{color:var(--yellow)}
.reader-layout{display:grid;grid-template-columns:300px minmax(0,1fr);gap:14px;margin-top:16px;align-items:start}.book-index{position:sticky;top:14px;max-height:calc(100vh - 30px);overflow:auto;border:1px solid var(--line);border-radius:14px;background:#111319;padding:8px}.index-item{width:100%;display:grid;grid-template-columns:36px 1fr;gap:8px;text-align:left;padding:10px;border:0;border-bottom:1px solid #242731;background:none;color:#999;cursor:pointer}.index-item:last-child{border-bottom:0}.index-item:hover{background:#1b1e26;color:#eee}.index-item.active{background:rgba(255,210,63,.1);color:#fff}.index-item .index-no{color:#777;font:10px ui-monospace,SFMono-Regular,Menlo,monospace}.index-item.active .index-no{color:var(--yellow)}.index-item strong{display:block;font-size:12px;font-weight:600}.index-item small{display:block;margin-top:2px;color:#6f737e;font-size:10px}.index-empty{padding:25px 12px;color:#777;font-size:12px}
.book-reader{min-width:0;padding:27px;border:1px solid var(--line);border-radius:14px;background:linear-gradient(145deg,#171a22,#12141a)}.reader-kicker{color:var(--cyan);font:11px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em}.book-reader h3{font-size:clamp(30px,5vw,52px);line-height:1.05;margin-top:12px}.reader-en{color:#777;font:12px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.1em;margin-top:6px}.reader-manifesto{margin-top:20px;color:#e5e5eb;font-size:17px;line-height:1.8}.reader-copy{margin-top:17px;color:#a4a7b2;font-size:13px;line-height:2}.reader-copy strong{color:#ddd}.reader-divider{height:1px;background:var(--line);margin:24px 0}.reader-axes{display:flex;flex-wrap:wrap;gap:6px}.reader-axis{padding:5px 8px;border-radius:5px;color:#111;background:var(--yellow);font-size:10.5px}.reader-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:15px}.reader-block{padding:14px;border-left:2px solid #3b3f4c;background:rgba(0,0,0,.12)}.reader-block:nth-child(2){border-color:var(--cyan)}.reader-block:nth-child(3){border-color:var(--pink)}.reader-block b{display:block;color:#ddd;font-size:11px;margin-bottom:6px}.reader-block p{color:#8e919c;font-size:11.5px;line-height:1.8}.reader-lower{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:15px}.reader-list{list-style:none;color:#8e919c;font-size:11.5px;line-height:1.8}.reader-list li+li{margin-top:4px}.reader-list li:before{content:"·";color:var(--yellow);margin-right:7px}.reader-tags{display:flex;flex-wrap:wrap;gap:5px}.reader-tags span{padding:4px 7px;background:#20232c;border-radius:5px;color:#aeb1bc;font-size:10.5px}.reader-more{margin-top:15px;border-top:1px solid var(--line);padding-top:13px}.reader-more summary{cursor:pointer;color:#bbb;font-size:12px}.reader-timeline{margin-top:12px;border-left:1px solid #3b3f4c;padding-left:14px}.reader-timeline p{color:#858894;font-size:11.5px;line-height:1.75}.reader-timeline p+p{margin-top:8px}.reader-timeline b{color:var(--yellow);margin-right:7px}.reader-open{display:inline-flex;margin-top:20px;padding:9px 13px;border:1px solid #454957;border-radius:99px;color:#eee;text-decoration:none;font-size:11px}.reader-open:hover{border-color:var(--yellow);color:var(--yellow)}
.book-footer{padding:28px 5vw 48px;border-top:1px solid #22252e;color:#686c77;text-align:center;font-size:11px;line-height:1.9}.book-footer a{text-decoration:none;color:#aaa}.book-footer a:hover{color:var(--yellow)}
@media(max-width:1000px){.arc{grid-template-columns:repeat(3,minmax(0,1fr))}.arc-step:nth-child(3){border-right:0}.arc-step:nth-child(n+4){border-top:1px solid var(--line)}.reader-layout{grid-template-columns:240px minmax(0,1fr)}}
@media(max-width:720px){.book-top{padding:17px 5vw 0;align-items:flex-start;flex-direction:column}.book-top nav{gap:11px}.book-cover{padding:62px 5vw 58px}.book-lede{font-size:13px}.book-stats{grid-template-columns:1fr;margin-top:34px}.book-section{padding:52px 5vw 0}.book-section:last-child{padding-bottom:68px}.section-head{display:block}.section-head>p{margin-top:12px}.contents-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.arc{grid-template-columns:1fr}.arc-step{min-height:0;border-right:0;border-bottom:1px solid var(--line)}.arc-step:last-child{border-bottom:0}.arc-step:nth-child(n+4){border-top:0}.arc-step b{margin-bottom:8px}.arc-step p{margin-top:7px}.lens-grid{grid-template-columns:1fr}.lens-columns{grid-template-columns:1fr;gap:9px}.reader-tools-row{display:block}.reader-count{display:block;margin-top:9px}.reader-layout{display:flex;flex-direction:column;margin-top:12px}.book-index{position:static;width:100%;max-height:260px}.book-reader{padding:20px}.reader-grid,.reader-lower{grid-template-columns:1fr;gap:9px}.book-reader h3{font-size:34px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;transition-duration:.001s!important}}
"""


HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>现代设计全书 · 主义馆</title>
<meta name="description" content="现代设计全书：80 个设计方向、历史主线、课内补充与前端转译。">
<style>@@CSS@@</style>
</head>
<body>
<div class="book-top">
  <a href="index.html">← 返回主义馆大厅</a>
  <nav><a href="#contents">目录</a><a href="#arc">历史主线</a><a href="#course-lens">课内补充</a><a href="#reader">设计索引</a></nav>
</div>
<header class="book-cover">
  <div class="book-kicker">THE DESIGN BOOK / 80 MOVEMENTS + COURSE LENS</div>
  <h1>现代设计<br><em>全书</em></h1>
  <p class="book-lede">这不是把课纲扩写成目录,也不是把 80 个风格堆成画廊。这里以现代设计的历史、形式、材料、生产、媒介与责任为全局主线,把课内知识作为一组阅读镜头,再把它们转成前端可以验证的实践问题。</p>
  <div class="book-actions"><a class="book-action primary" href="#reader">打开设计索引 ↓</a><a class="book-action" href="#course-lens">看课内补充</a></div>
  <div class="book-stats"><div class="book-stat"><strong>80</strong><span>设计方向与完整展厅档案</span></div><div class="book-stat"><strong>06</strong><span>历史阶段与现代设计主线</span></div><div class="book-stat"><strong>08</strong><span>课内母题作为补充视角</span></div></div>
</header>
<main class="book-main">
<section class="book-section" id="contents">
  <div class="section-head"><div><div class="section-kicker">TABLE OF CONTENTS</div><h2>先看全局,再进入条目</h2></div><p>全书分为历史主线、课内补充和设计索引三层。课程不是边界,而是帮助你理解全局设计史的提问方式。</p></div>
  <div class="contents-grid">
    <a class="contents-link" href="#arc"><b>01 / HISTORY</b><span>现代设计的历史主线</span><small>从手工与装饰走向系统、媒介与责任</small></a>
    <a class="contents-link" href="#course-lens"><b>02 / COURSE LENS</b><span>课内知识补充</span><small>八个母题如何读全局,并转成前端问题</small></a>
    <a class="contents-link" href="#reader"><b>03 / INDEX</b><span>八十个设计方向</span><small>搜索、筛选并打开任意一条完整档案</small></a>
    <a class="contents-link" href="timeline.html"><b>04 / TIMELINE</b><span>独立时间轴</span><small>按年代回看风格之间的连续与分叉</small></a>
  </div>
</section>
<section class="book-section" id="arc">
  <div class="section-head"><div><div class="section-kicker">THE LONG ARC</div><h2>设计如何不断改变问题</h2></div><p>风格不是孤立的外观,而是对生产方式、生活方式、技术媒介和社会关系的回应。</p></div>
  <div class="arc" id="arc-grid"></div>
</section>
<section class="book-section" id="course-lens">
  <div class="section-head"><div><div class="section-kicker">COURSE AS A LENS</div><h2>课内补充 · 八个阅读镜头</h2></div><p>展开一个母题,看它在全书中连接哪些设计方向,以及它如何转译成前端的可验证问题。</p></div>
  <div class="lens-note"><b>阅读方法：</b>先用历史主线理解“为什么出现”,再用课内母题追问“它解决了什么、影响了谁、今天如何实践”,最后回到具体设计条目。</div>
  <div class="lens-grid" id="lens-grid"></div>
</section>
<section class="book-section" id="reader">
  <div class="section-head"><div><div class="section-kicker">DESIGN INDEX / READER</div><h2>全书索引 · 逐条阅读</h2></div><p>索引只展示条目骨架,选中后在右侧阅读完整内容。每条档案同时保留历史资料、形式关键词和课内—前端补充。</p></div>
  <div class="reader-tools"><div class="reader-tools-row"><label class="reader-search"><span>⌕</span><input id="reader-search" type="search" placeholder="搜索主义、年代、历史、案例或前端关系" autocomplete="off"></label><span class="reader-count" id="reader-count" aria-live="polite"></span></div><div class="reader-filters" id="reader-filters" aria-label="按课内补充视角筛选"></div></div>
  <div class="reader-layout"><aside class="book-index" id="book-index" aria-label="设计条目索引"></aside><article class="book-reader" id="book-reader" aria-live="polite"></article></div>
</section>
</main>
<footer class="book-footer">主义馆 ISM MUSEUM · <a href="index.html">回到大厅</a> · 现代设计全书把全局历史与课内实践放在同一条阅读路径上。</footer>
<script type="application/json" id="stage-data">@@STAGES@@</script>
<script type="application/json" id="course-data">@@AXES@@</script>
<script type="application/json" id="ism-data">@@RECORDS@@</script>
<script>
const stages=JSON.parse(document.getElementById('stage-data').textContent);
const axes=JSON.parse(document.getElementById('course-data').textContent);
const records=JSON.parse(document.getElementById('ism-data').textContent);
const axisByKey=Object.fromEntries(axes.map(axis=>[axis.key,axis]));
const arcGrid=document.getElementById('arc-grid');
const lensGrid=document.getElementById('lens-grid');
const index=document.getElementById('book-index');
const reader=document.getElementById('book-reader');
const search=document.getElementById('reader-search');
const count=document.getElementById('reader-count');
const filters=document.getElementById('reader-filters');
let activeAxis='all';
let activeSlug=records[0]?.slug;
const esc=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const short=value=>String(value??'').replace(/\s+/g,' ').trim();
const axisLabel=key=>axisByKey[key]?.title||key;
const axisRecords=key=>records.filter(record=>record.axes.includes(key));
function renderArc(){arcGrid.innerHTML=stages.map(stage=>`<article class="arc-step"><b>${esc(stage.no)}</b><strong>${esc(stage.title)}</strong><em>${esc(stage.period)}</em><p>${esc(stage.text)}</p></article>`).join('')}
function renderLenses(){lensGrid.innerHTML=axes.map(axis=>{const items=axisRecords(axis.key);return `<details class="lens-card"><summary><span>${esc(axis.no)} · ${esc(axis.title)}</span><b>${items.length} 个方向</b></summary><div class="lens-body"><p class="lens-focus">${esc(axis.focus)}</p><div class="lens-columns"><div><b>课内追问</b><p>${esc(axis.question)}</p></div><div><b>前端转译</b><p>${esc(axis.frontend)}</p></div><div><b>课程回写</b><p>${esc(axis.feedback)}</p></div></div><div class="lens-count">${items.slice(0,8).map(item=>`<span>${esc(item.zh)}</span>`).join('')}${items.length>8?`<span>+${items.length-8} 个</span>`:''}</div><button class="lens-jump" type="button" data-lens-jump="${esc(axis.key)}">在全书索引中查看全部 →</button></div></details>`}).join('')}
function renderFilters(){filters.innerHTML=[`<button class="reader-filter active" type="button" data-reader-axis="all">全部 <span>${records.length}</span></button>`,...axes.map(axis=>`<button class="reader-filter" type="button" data-reader-axis="${esc(axis.key)}">${esc(axis.no)} ${esc(axis.title)} <span>${axisRecords(axis.key).length}</span></button>`)].join('')}
function matches(record,query){if(!query)return true;const haystack=[record.zh,record.en,record.era,record.period,record.manifesto,record.prologue,record.history,record.bridge,record.frontend,record.feedback,...record.reps,...record.keywords,...record.axes.map(axisLabel)].join(' ').toLowerCase();return haystack.includes(query)}
function visibleRecords(){const query=search.value.trim().toLowerCase();return records.filter(record=>(activeAxis==='all'||record.axes.includes(activeAxis))&&matches(record,query))}
function renderIndex(){const visible=visibleRecords();count.textContent=`显示 ${visible.length} / ${records.length} 个方向`;index.innerHTML=visible.length?visible.map(record=>`<button class="index-item${record.slug===activeSlug?' active':''}" type="button" data-reader-slug="${esc(record.slug)}"><span class="index-no">${esc(record.no)}</span><span><strong>${esc(record.zh)}</strong><small>${esc(record.era)} · ${esc(record.en)}</small></span></button>`).join(''):'<div class="index-empty">没有找到匹配条目。换一个关键词或回到全部。</div>';const selected=visible.find(record=>record.slug===activeSlug)||visible[0];if(selected){activeSlug=selected.slug;renderReader(selected)}else{reader.innerHTML='<p class="index-empty">当前筛选没有可阅读的条目。</p>'}}
function list(items){return items?.length?`<ul class="reader-list">${items.map(item=>`<li>${esc(item)}</li>`).join('')}</ul>`:'<p class="reader-copy">暂无整理内容。</p>'}
function renderReader(record){if(!record)return;const axesText=record.axes.map(axis=>`<span class="reader-axis">${esc(axisLabel(axis))}</span>`).join('');const timeline=record.timeline?.length?record.timeline.map(([year,text])=>`<p><b>${esc(year)}</b>${esc(text)}</p>`).join(''):'<p>暂无时间节点。</p>';reader.innerHTML=`<div class="reader-kicker">HALL ${esc(record.no)} / ${esc(record.era)} / ${esc(record.period)}</div><h3>${esc(record.zh)}</h3><div class="reader-en">${esc(record.en)}</div><p class="reader-manifesto">“${esc(record.manifesto)}”</p><p class="reader-copy"><strong>导言：</strong>${esc(record.prologue||record.history)}</p><p class="reader-copy"><strong>历史位置：</strong>${esc(record.history)}</p><div class="reader-divider"></div><div class="reader-axes">${axesText}</div><div class="reader-grid"><div class="reader-block"><b>课内关系</b><p>${esc(record.bridge)}</p></div><div class="reader-block"><b>前端转译</b><p>${esc(record.frontend)}</p></div><div class="reader-block"><b>课程回写</b><p>${esc(record.feedback)}</p></div></div><div class="reader-lower"><div class="reader-block"><b>代表案例</b>${list(record.reps)}</div><div class="reader-block"><b>形式关键词</b><div class="reader-tags">${(record.keywords||[]).map(word=>`<span>${esc(word)}</span>`).join('')}</div></div></div><details class="reader-more"><summary>展开时间节点与 CSS 标本</summary><div class="reader-timeline">${timeline}</div><div class="reader-tags" style="margin-top:12px">${(record.specimens||[]).map(item=>`<span>${esc(item)}</span>`).join('')}</div></details><a class="reader-open" href="halls/${encodeURIComponent(record.slug)}.html">打开 ${esc(record.zh)} 完整展厅 ↗</a>`}
filters.addEventListener('click',event=>{const button=event.target.closest('[data-reader-axis]');if(!button)return;activeAxis=button.dataset.readerAxis;filters.querySelectorAll('.reader-filter').forEach(item=>item.classList.toggle('active',item===button));renderIndex()});
index.addEventListener('click',event=>{const button=event.target.closest('[data-reader-slug]');if(!button)return;activeSlug=button.dataset.readerSlug;renderIndex()});
lensGrid.addEventListener('click',event=>{const button=event.target.closest('[data-lens-jump]');if(!button)return;activeAxis=button.dataset.lensJump;const filter=filters.querySelector(`[data-reader-axis="${CSS.escape(activeAxis)}"]`);if(filter){filters.querySelectorAll('.reader-filter').forEach(item=>item.classList.toggle('active',item===filter))}renderIndex();document.getElementById('reader').scrollIntoView({behavior:'smooth'})});
search.addEventListener('input',renderIndex);
renderArc();renderLenses();renderFilters();renderIndex();
</script>
</body>
</html>
'''


def render_knowledge():
    records = [_record(m) for m in ISMS]
    return (HTML.replace('@@CSS@@', CSS)
            .replace('@@STAGES@@', _json_script(BOOK_STAGES))
            .replace('@@AXES@@', _json_script(COURSE_AXES))
            .replace('@@RECORDS@@', _json_script(records)))


def build_knowledge(base):
    path = os.path.join(base, 'knowledge.html')
    with open(path, 'w', encoding='utf-8') as file:
        file.write(render_knowledge())
    print('generated design book', len(ISMS), 'records', len(COURSE_AXES), 'course lenses')


if __name__ == '__main__':
    build_knowledge(os.path.dirname(os.path.abspath(__file__)))
