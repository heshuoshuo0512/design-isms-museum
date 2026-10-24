# -*- coding: utf-8 -*-
"""生成现代设计知识库页面。"""

import html
import json
import os

from data import ISMS
from knowledge_data import COURSE_AXES, ISM_AXES


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
    }


def _json_script(value):
    """让 JSON 安全地嵌入 script[type=application/json]。"""
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{color-scheme:dark;--bg:#0b0b0f;--surface:#14161d;--surface-2:#181b24;--line:#292c37;--muted:#858894;--text:#eeeef3;--yellow:#FFD23F;--cyan:#7DF9FF;--pink:#FF71CE;--mint:#A7FFEA}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:-apple-system,"Helvetica Neue","PingFang SC","Noto Sans SC",sans-serif;line-height:1.6;overflow-x:hidden}
a{color:inherit}
button,input{font:inherit}
button{cursor:pointer}
.kb-top{max-width:1240px;margin:0 auto;padding:24px 6vw 0;display:flex;justify-content:space-between;gap:20px;align-items:center;color:#777;font-size:12px;letter-spacing:.08em}
.kb-top a{text-decoration:none;color:#aaa;transition:color .2s}.kb-top a:hover{color:var(--yellow)}
.kb-top nav{display:flex;gap:18px;flex-wrap:wrap}
.kb-hero{position:relative;max-width:1240px;margin:0 auto;padding:84px 6vw 76px;overflow:hidden}
.kb-hero:before{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(circle at 10% 25%,rgba(255,210,63,.12),transparent 26%),radial-gradient(circle at 86% 72%,rgba(125,249,255,.1),transparent 30%)}
.kb-hero>*{position:relative}
.kb-kicker{color:#777;font:11px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.25em;margin-bottom:18px}
.kb-hero h1{font-size:clamp(42px,8vw,96px);line-height:1.03;letter-spacing:-.06em;max-width:820px;background:linear-gradient(110deg,var(--yellow),#ff8e8e 34%,var(--cyan) 72%,var(--pink));-webkit-background-clip:text;background-clip:text;color:transparent}
.kb-lede{max-width:760px;margin-top:24px;color:#aaa;line-height:2;font-size:15px}
.kb-hero-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}
.kb-cta{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:10px 20px;border:1px solid #3a3d49;border-radius:99px;text-decoration:none;color:#eee;font-size:13px;transition:transform .2s,border-color .2s,box-shadow .2s}
.kb-cta:hover{transform:translateY(-2px);border-color:var(--cyan);box-shadow:0 10px 30px rgba(125,249,255,.1)}
.kb-cta.primary{background:var(--yellow);border-color:var(--yellow);color:#111;font-weight:800}
.kb-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;max-width:680px;margin-top:48px}
.kb-stat{padding:16px 18px;border-top:2px solid var(--line);background:rgba(255,255,255,.025)}
.kb-stat:nth-child(1){border-color:var(--yellow)}.kb-stat:nth-child(2){border-color:var(--cyan)}.kb-stat:nth-child(3){border-color:var(--pink)}
.kb-stat strong{display:block;font-size:28px;line-height:1.1}.kb-stat span{display:block;margin-top:6px;color:#888;font-size:12px}
.kb-section{max-width:1240px;margin:0 auto;padding:72px 6vw 0}
.kb-section:last-of-type{padding-bottom:90px}
.kb-section-head{display:flex;align-items:end;justify-content:space-between;gap:24px;margin-bottom:28px}
.kb-section-head .kb-kicker{margin-bottom:8px}
.kb-section-head h2{font-size:clamp(26px,4vw,44px);line-height:1.15}
.kb-section-head p{max-width:560px;color:#858894;font-size:13px;line-height:1.9}
.kb-scope{margin:-8px 0 24px;padding:14px 16px;border:1px dashed #383b48;border-radius:10px;color:#9295a1;font-size:12px;line-height:1.8;background:rgba(125,249,255,.025)}
.kb-scope b{color:var(--cyan)}
.axis-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.axis-card{position:relative;padding:24px;border:1px solid var(--line);border-radius:16px;background:linear-gradient(145deg,rgba(20,22,29,.98),rgba(17,19,26,.96));overflow:hidden}
.axis-card:before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--axis-color,var(--yellow))}
.axis-card:nth-child(4n+1){--axis-color:var(--yellow)}.axis-card:nth-child(4n+2){--axis-color:var(--cyan)}.axis-card:nth-child(4n+3){--axis-color:var(--pink)}.axis-card:nth-child(4n){--axis-color:var(--mint)}
.axis-top{display:flex;justify-content:space-between;gap:12px;color:#777;font:11px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em}
.axis-top .axis-count{color:var(--axis-color)}
.axis-card h3{margin-top:12px;font-size:22px}.axis-en{color:#777;font:11px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em}
.axis-focus{margin-top:14px;color:#c4c5ce;font-size:13px;line-height:1.8}
.axis-detail{margin-top:16px;padding-top:13px;border-top:1px solid #292c37}.axis-detail b{display:block;color:#ddd;font-size:12px;margin-bottom:5px}.axis-detail p{color:#858894;font-size:12.5px;line-height:1.8}
.axis-related{display:flex;flex-wrap:wrap;gap:6px;margin-top:16px}.axis-related span{padding:4px 8px;border:1px solid #343744;border-radius:99px;color:#aaa;font-size:11px}
.axis-open{display:inline-flex;margin-top:18px;color:var(--axis-color);font-size:12px;text-decoration:none}.axis-open:hover{text-decoration:underline}
.library-tools{padding:18px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.025)}
.library-tools-top{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.search-wrap{position:relative;flex:1 1 260px}.search-wrap input{width:100%;height:44px;padding:0 14px 0 40px;border:1px solid #353844;border-radius:10px;background:#101217;color:#eee;outline:none}.search-wrap input:focus{border-color:var(--cyan);box-shadow:0 0 0 3px rgba(125,249,255,.08)}.search-icon{position:absolute;left:14px;top:10px;color:#777;font-size:17px}
.library-result{color:#777;font-size:12px;white-space:nowrap}.filter-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}.filter{padding:7px 11px;border:1px solid #343744;border-radius:99px;background:transparent;color:#999;font-size:11px;transition:.2s}.filter:hover,.filter.active{border-color:var(--yellow);background:rgba(255,210,63,.1);color:#eee}.filter span{color:#777;margin-left:3px}.filter.active span{color:var(--yellow)}
.ism-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:20px}.ism-card{display:flex;flex-direction:column;min-height:330px;padding:20px;border:1px solid #272a35;border-radius:14px;background:#12141a;transition:transform .2s,border-color .2s,box-shadow .2s}.ism-card:hover{transform:translateY(-4px);border-color:#4a4d5d;box-shadow:0 16px 36px rgba(0,0,0,.22)}
.ism-top{display:flex;justify-content:space-between;gap:10px;color:#777;font:10px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em}.ism-top .ism-era{color:var(--cyan)}.ism-card h3{font-size:21px;margin-top:12px}.ism-en{color:#777;font:11px ui-monospace,SFMono-Regular,Menlo,monospace}.ism-manifesto{margin-top:12px;color:#ddd;font-size:13px;line-height:1.8}.ism-history{margin-top:10px;color:#858894;font-size:12px;line-height:1.8}.ism-meta{display:flex;gap:10px;flex-wrap:wrap;margin-top:13px;color:#777;font-size:11px}.ism-tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:auto;padding-top:14px}.ism-tags span{padding:4px 7px;color:#9a9ca6;background:#1a1d25;border-radius:5px;font-size:10px}.ism-footer{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:15px;padding-top:12px;border-top:1px solid #292c37}.ism-footer small{color:#666;font-size:10px}.ism-open{color:var(--yellow);font-size:12px;text-decoration:none}.ism-open:hover{text-decoration:underline}.empty{padding:42px 20px;text-align:center;color:#777;border:1px dashed #343744;border-radius:14px;margin-top:20px}.empty[hidden]{display:none}
.kb-footer{padding:28px 6vw 46px;border-top:1px solid #1d1f27;color:#666;text-align:center;font-size:11px;line-height:1.9}.kb-footer a{text-decoration:none;color:#aaa}.kb-footer a:hover{color:var(--yellow)}
@media(max-width:900px){.ism-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:720px){.kb-top{padding:18px 5vw 0;align-items:flex-start;flex-direction:column}.kb-top nav{gap:12px}.kb-hero{padding:60px 5vw 58px}.kb-lede{font-size:13px}.kb-stats{grid-template-columns:1fr;margin-top:34px}.kb-section{padding:54px 5vw 0}.kb-section:last-of-type{padding-bottom:64px}.kb-section-head{display:block}.kb-section-head p{margin-top:12px}.axis-grid,.ism-grid{grid-template-columns:1fr}.axis-card{padding:20px}.library-tools-top{align-items:stretch;display:block}.library-result{display:block;margin-top:10px}.filter-row{gap:6px}.filter{font-size:10px;padding:7px 9px}.ism-card{min-height:0}.kb-footer{padding-left:5vw;padding-right:5vw}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;transition-duration:.001s!important}}
"""

HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>现代设计知识库 · 主义馆</title>
<meta name="description" content="现代设计知识库：80 个设计方向、8 个课内母题，以及从课程到前端实践再回写课程的反哺分类。">
<style>@@CSS@@</style>
</head>
<body>
<div class="kb-top">
  <a href="index.html">← 返回主义馆大厅</a>
  <nav><a href="corridor.html">长廊</a><a href="timeline.html">时间轴</a><a href="#feedback">反哺库</a><a href="#library">80 个条目</a></nav>
</div>
<header class="kb-hero">
  <div class="kb-kicker">DESIGN KNOWLEDGE BASE / COURSE ↔ FRONTEND</div>
  <h1>现代设计<br>知识库</h1>
  <p class="kb-lede">把现代设计的历史、形式、材料、生产和责任整理成可检索的知识层；再把课内方向转译成前端约束，用原型、测试与技术取舍把结果反哺回课程。</p>
  <div class="kb-hero-actions"><a class="kb-cta primary" href="#feedback">进入反哺库 ↓</a><a class="kb-cta" href="#library">检索 80 个设计方向</a></div>
  <div class="kb-stats"><div class="kb-stat"><strong>80</strong><span>现代设计方向与完整展厅档案</span></div><div class="kb-stat"><strong>08</strong><span>课内母题与前端转译分类</span></div><div class="kb-stat"><strong>04</strong><span>可回写课程的证据产物</span></div></div>
</header>
<main>
<section class="kb-section" id="feedback">
  <div class="kb-section-head"><div><div class="kb-kicker">FEEDBACK LIBRARY</div><h2>反哺库 · 课内方向如何进入前端</h2></div><p>每个分类都回答三件事：课内在问什么，前端要做什么，做完以后什么证据可以回到课程。</p></div>
  <div class="kb-scope"><b>知识边界：</b>80 个展厅是扩展后的现代设计索引；8 个母题是根据课内重点建立的策展映射。一个主义可以跨越多个分类，分类用于设计实践与课程反思，不把扩展目录冒充成课堂原样目录。</div>
  <div class="axis-grid" id="axis-grid"></div>
</section>
<section class="kb-section" id="library">
  <div class="kb-section-head"><div><div class="kb-kicker">ARCHIVE INDEX</div><h2>现代设计索引</h2></div><p>按课内母题筛选主义，搜索历史、形式、代表案例和关键词；进入条目可以继续查看完整历史档案、CSS 标本、代码指纹与年代坐标。</p></div>
  <div class="library-tools">
    <div class="library-tools-top"><label class="search-wrap"><span class="search-icon">⌕</span><input id="search" type="search" placeholder="搜索主义、关键词、历史或案例" autocomplete="off"></label><span class="library-result" id="result-count" aria-live="polite"></span></div>
    <div class="filter-row" id="filters" aria-label="按课内母题筛选"></div>
  </div>
  <div class="ism-grid" id="ism-grid"></div>
  <div class="empty" id="empty" hidden>没有找到匹配条目。换一个关键词，或回到“全部母题”。</div>
</section>
</main>
<footer class="kb-footer">主义馆 ISM MUSEUM · <a href="index.html">回到大厅</a> · 知识库将历史档案、课程母题与前端验证放在同一条可回写链路中。</footer>
<script type="application/json" id="course-data">@@AXES@@</script>
<script type="application/json" id="ism-data">@@RECORDS@@</script>
<script>
const axes=JSON.parse(document.getElementById('course-data').textContent);
const records=JSON.parse(document.getElementById('ism-data').textContent);
const axisByKey=Object.fromEntries(axes.map(axis=>[axis.key,axis]));
const axisGrid=document.getElementById('axis-grid');
const filters=document.getElementById('filters');
const ismGrid=document.getElementById('ism-grid');
const search=document.getElementById('search');
const resultCount=document.getElementById('result-count');
const empty=document.getElementById('empty');
let activeAxis='all';
const esc=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const shorten=(value,length=145)=>{const text=String(value??'').replace(/\s+/g,' ').trim();return text.length>length?text.slice(0,length)+'…':text};
const axisLabel=key=>axisByKey[key]?.title||key;
const related=key=>records.filter(record=>record.axes.includes(key));

function renderAxisCards(){
  axisGrid.innerHTML=axes.map(axis=>{
    const items=related(axis.key);
    return `<article class="axis-card">
      <div class="axis-top"><span>${esc(axis.no)} · ${esc(axis.en)}</span><span class="axis-count">${items.length} 个关联条目</span></div>
      <h3>${esc(axis.title)}</h3>
      <p class="axis-focus">${esc(axis.focus)}</p>
      <div class="axis-detail"><b>课内追问</b><p>${esc(axis.question)}</p></div>
      <div class="axis-detail"><b>前端转译</b><p>${esc(axis.frontend)}</p></div>
      <div class="axis-detail"><b>课程回写</b><p>${esc(axis.feedback)}</p></div>
      <div class="axis-related">${items.slice(0,6).map(item=>`<span>${esc(item.zh)}</span>`).join('')}${items.length>6?`<span>+${items.length-6} 个</span>`:''}</div>
      <a class="axis-open" href="#library" data-axis-link="${esc(axis.key)}">查看此分类的全部条目 →</a>
    </article>`;
  }).join('');
}

function renderFilters(){
  filters.innerHTML=[`<button class="filter active" type="button" data-axis="all">全部 <span>${records.length}</span></button>`,...axes.map(axis=>`<button class="filter" type="button" data-axis="${esc(axis.key)}">${esc(axis.no)} ${esc(axis.title)} <span>${related(axis.key).length}</span></button>`)].join('');
  filters.addEventListener('click',event=>{
    const button=event.target.closest('[data-axis]');
    if(!button)return;
    activeAxis=button.dataset.axis;
    filters.querySelectorAll('.filter').forEach(item=>item.classList.toggle('active',item===button));
    renderRecords();
  });
}

function renderRecords(){
  const query=search.value.trim().toLowerCase();
  const visible=records.filter(record=>{
    const axisMatch=activeAxis==='all'||record.axes.includes(activeAxis);
    const haystack=[record.zh,record.en,record.era,record.period,record.manifesto,record.prologue,record.history,...record.reps,...record.keywords,...record.axes.map(axisLabel)].join(' ').toLowerCase();
    return axisMatch&&(!query||haystack.includes(query));
  });
  resultCount.textContent=`显示 ${visible.length} / ${records.length} 个条目`;
  empty.hidden=visible.length!==0;
  ismGrid.innerHTML=visible.map(record=>`<article class="ism-card">
    <div class="ism-top"><span>HALL ${esc(record.no)}</span><span class="ism-era">${esc(record.era)}</span></div>
    <h3>${esc(record.zh)}</h3><div class="ism-en">${esc(record.en)}</div>
    <p class="ism-manifesto">“${esc(record.manifesto)}”</p>
    <p class="ism-history">${esc(shorten(record.history))}</p>
    <div class="ism-meta"><span>${record.timeline.length} 个时间节点</span><span>${record.specimens.length} 个 CSS 标本</span></div>
    <div class="ism-tags">${record.axes.map(axis=>`<span>${esc(axisLabel(axis))}</span>`).join('')}</div>
    <div class="ism-footer"><small>${esc(record.reps.slice(0,2).join(' · '))}</small><a class="ism-open" href="halls/${encodeURIComponent(record.slug)}.html">完整档案 ↗</a></div>
  </article>`).join('');
}

document.addEventListener('click',event=>{
  const link=event.target.closest('[data-axis-link]');
  if(!link)return;
  event.preventDefault();
  activeAxis=link.dataset.axisLink;
  const button=filters.querySelector(`[data-axis="${CSS.escape(activeAxis)}"]`);
  if(button){filters.querySelectorAll('.filter').forEach(item=>item.classList.toggle('active',item===button));}
  renderRecords();
  document.getElementById('library').scrollIntoView({behavior:'smooth'});
});
search.addEventListener('input',renderRecords);
renderAxisCards();
renderFilters();
renderRecords();
</script>
</body>
</html>
'''


def render_knowledge():
    records = [_record(m) for m in ISMS]
    return HTML.replace('@@CSS@@', CSS).replace('@@AXES@@', _json_script(COURSE_AXES)).replace('@@RECORDS@@', _json_script(records))


def build_knowledge(base):
    path = os.path.join(base, 'knowledge.html')
    with open(path, 'w', encoding='utf-8') as file:
        file.write(render_knowledge())
    print('generated knowledge base', len(ISMS), 'records', len(COURSE_AXES), 'course axes')


if __name__ == '__main__':
    build_knowledge(os.path.dirname(os.path.abspath(__file__)))
