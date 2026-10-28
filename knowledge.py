# -*- coding: utf-8 -*-
"""生成现代设计史与主义索引的统一阅读入口。"""

import json
import os

from data import ISMS
from history_data import ISM_HISTORY
from knowledge_data import COURSE_AXES, HISTORY_EVENTS, ISM_AXES, ISM_BRIDGES, ISM_EVENTS
from book_data import BOOK_CHAPTERS, BOOK_LENSES, BOOK_SOURCES, BOOK_VOLUMES, DESIGN_INSTITUTIONS, GLOBAL_REGIONS, PRACTICE_FIELDS
from book_archives import CHAPTER_ARCHIVES


if set(ISM_HISTORY) != {m['slug'] for m in ISMS}:
    missing = sorted({m['slug'] for m in ISMS} - set(ISM_HISTORY))
    extra = sorted(set(ISM_HISTORY) - {m['slug'] for m in ISMS})
    raise ValueError(f'方向历史深描覆盖不完整: missing={missing}, extra={extra}')


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
        'events': ISM_EVENTS[m['slug']],
        **ISM_HISTORY[m['slug']],
    }


def _json_script(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


CSS = r'''
*{box-sizing:border-box;margin:0;padding:0}
:root{color-scheme:dark;--bg:#0b0d11;--panel:#12151b;--panel-2:#171b22;--line:#2c313c;--text:#f1f2f5;--muted:#9297a3;--soft:#c2c5cc;--yellow:#ffd23f;--cyan:#7df9ff;--pink:#ff71ce;--mint:#a7ffea}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:-apple-system,"Helvetica Neue","PingFang SC","Noto Sans SC",sans-serif;line-height:1.7;overflow-x:hidden}
a{color:inherit}button,input{font:inherit}button{cursor:pointer}
.site-nav{max-width:1280px;margin:0 auto;padding:20px 5vw 12px;display:flex;align-items:center;justify-content:space-between;gap:24px;color:var(--muted);font:12px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.06em}.site-brand{text-decoration:none;color:var(--text);font-weight:700}.site-brand small{margin-left:8px;color:var(--muted);font-weight:400}.site-nav nav{display:flex;gap:18px;flex-wrap:wrap}.site-nav nav a{text-decoration:none}.site-nav nav a:hover,.site-nav nav a.active{color:var(--yellow)}
.site-nav nav .site-back{color:var(--yellow);margin-right:8px}.site-nav nav .site-back:hover{color:#fff}
.book-hero{max-width:1280px;margin:0 auto;padding:72px 5vw 76px;position:relative}.book-hero:before{content:"";position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,210,63,.08),transparent 38%),radial-gradient(circle at 90% 28%,rgba(125,249,255,.1),transparent 28%);pointer-events:none}.book-hero>*{position:relative}.eyebrow,.mode-kicker{color:#777d89;font:11px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.2em}.book-hero h1{max-width:850px;margin-top:18px;font-size:clamp(48px,9vw,112px);line-height:.98;letter-spacing:-.075em}.book-hero h1 em{font-style:normal;color:var(--yellow)}.hero-intro{max-width:720px;margin-top:24px;color:var(--soft);font-size:16px;line-height:2}.route-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:34px;max-width:980px}.route-card{min-height:148px;padding:18px;text-align:left;border:1px solid var(--line);border-radius:10px;background:var(--panel);color:var(--text);text-decoration:none;display:flex;flex-direction:column;justify-content:space-between;transition:border-color .2s,transform .2s,background .2s}.route-card:hover,.route-card:focus-visible{border-color:var(--yellow);background:var(--panel-2);transform:translateY(-3px);outline:none}.route-card.primary{border-color:var(--yellow);background:linear-gradient(145deg,rgba(255,210,63,.14),var(--panel))}.route-card .route-no{color:var(--yellow);font:11px ui-monospace,SFMono-Regular,Menlo,monospace}.route-card:nth-child(2) .route-no{color:var(--cyan)}.route-card:nth-child(3) .route-no{color:var(--pink)}.route-card strong{display:block;margin-top:20px;font-size:19px}.route-card small{display:block;margin-top:5px;color:var(--muted);font-size:12px;line-height:1.6}
.route-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
.book-main{max-width:1280px;margin:0 auto}.mode-panel{padding:38px 5vw 90px;border-top:1px solid #20242c}.mode-panel[hidden]{display:none}.mode-heading{display:flex;align-items:end;justify-content:space-between;gap:28px;margin-bottom:25px}.mode-heading h2{margin-top:8px;font-size:clamp(30px,4.5vw,58px);line-height:1.05;letter-spacing:-.05em}.mode-heading>p{max-width:510px;color:var(--muted);font-size:13px;line-height:1.9}.history-layout{display:grid;grid-template-columns:270px minmax(0,1fr);gap:14px;align-items:start}.history-nav{position:sticky;top:12px;padding:8px;border:1px solid var(--line);border-radius:12px;background:#101319}.history-nav button{width:100%;padding:13px 12px;text-align:left;border:0;border-bottom:1px solid #252a33;background:transparent;color:var(--muted)}.history-nav button:last-child{border-bottom:0}.history-nav button:hover,.history-nav button.active{background:rgba(255,210,63,.1);color:var(--text)}.history-nav .chapter-no{display:block;color:#777d89;font:10px ui-monospace,SFMono-Regular,Menlo,monospace}.history-nav button.active .chapter-no{color:var(--yellow)}.history-nav strong{display:block;margin-top:4px;font-size:13px}.history-nav small{display:block;margin-top:3px;color:#707581;font-size:10px}.history-reader{min-width:0;padding:29px;border:1px solid var(--line);border-radius:12px;background:linear-gradient(145deg,#171b23,#11141a)}.history-reader .reader-kicker{color:var(--cyan);font:11px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em}.history-reader h3{margin-top:12px;font-size:clamp(28px,4.8vw,56px);line-height:1.08;letter-spacing:-.05em}.history-period{margin-top:7px;color:#777d89;font:12px ui-monospace,SFMono-Regular,Menlo,monospace}.history-lede{margin-top:24px;padding:18px 20px;border-left:2px solid var(--yellow);background:rgba(255,210,63,.06);color:#e2e3e8;font-size:16px;line-height:1.9}.history-section{margin-top:25px;padding-top:18px;border-top:1px solid var(--line)}.history-section h4{font-size:12px;color:var(--yellow);letter-spacing:.08em}.history-section>p{margin-top:9px;color:#aeb2bd;font-size:13px;line-height:1.95}.history-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin-top:14px}.history-card{padding:15px;border-left:2px solid #777d89;background:rgba(255,255,255,.025)}.history-card:nth-child(2n){border-color:var(--cyan)}.history-card:nth-child(3n){border-color:var(--pink)}.history-card:nth-child(4n){border-color:var(--mint)}.history-card b{display:block;color:#e2e3e8;font-size:11px}.history-card p,.history-card li{margin-top:6px;color:#999eaa;font-size:12px;line-height:1.85}.history-card ul{padding-left:16px}.history-card li+li{margin-top:4px}.history-related{display:flex;flex-wrap:wrap;gap:7px;margin-top:13px}.history-related button,.reader-tag{padding:6px 9px;border:1px solid #3a404c;border-radius:6px;background:#1b2028;color:#c7cad2;font-size:11px}.history-related button:hover,.reader-tag:hover{border-color:var(--yellow);color:var(--yellow)}.history-application{margin-top:22px;border-top:1px solid var(--line)}.history-application summary{padding:13px 0;color:#aeb2bd;font-size:12px;cursor:pointer}.history-application[open] summary{color:var(--yellow)}.history-application p{color:#999eaa;font-size:12px;line-height:1.9}.history-application-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;padding-bottom:3px}.history-application-card{padding:13px;background:rgba(255,255,255,.025)}.history-application-card b{display:block;color:#ddd;font-size:11px;margin-bottom:5px}
.book-spine{margin:26px 0 30px;padding:22px;border:1px solid #38404d;border-radius:12px;background:linear-gradient(145deg,rgba(255,210,63,.06),rgba(125,249,255,.035))}.book-spine-head{display:flex;align-items:end;justify-content:space-between;gap:20px}.book-spine-head h3{margin-top:7px;font-size:clamp(24px,4vw,42px);line-height:1.1;letter-spacing:-.05em}.book-spine-head p{max-width:510px;color:#9da3ae;font-size:12px;line-height:1.85}.book-layout{display:grid;grid-template-columns:220px minmax(0,1fr);gap:10px;margin-top:19px;align-items:start}.book-nav{position:sticky;top:12px;max-height:calc(100vh - 25px);overflow:auto;padding:6px;border:1px solid #303744;border-radius:9px;background:#101319}.book-nav button{width:100%;padding:10px;text-align:left;border:0;border-bottom:1px solid #252a33;background:transparent;color:#969ba6}.book-nav button:last-child{border-bottom:0}.book-nav button:hover,.book-nav button.active{background:rgba(125,249,255,.08);color:#fff}.book-nav .book-no{display:block;color:#707581;font:10px ui-monospace,SFMono-Regular,Menlo,monospace}.book-nav button.active .book-no{color:var(--cyan)}.book-nav strong{display:block;margin-top:3px;font-size:11px;line-height:1.45}.book-nav small{display:block;margin-top:3px;color:#707581;font-size:9px}.book-reader{min-width:0;padding:23px;border:1px solid #303744;border-radius:9px;background:rgba(10,13,18,.42)}.book-reader .book-kicker{color:var(--cyan);font:10px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.13em}.book-reader h4{margin-top:10px;font-size:clamp(25px,4vw,48px);line-height:1.08;letter-spacing:-.05em}.book-reader .book-period{margin-top:5px;color:#777d89;font:11px ui-monospace,SFMono-Regular,Menlo,monospace}.book-thesis{margin-top:19px;padding:15px 17px;border-left:2px solid var(--yellow);background:rgba(255,210,63,.06);color:#e2e3e8;font-size:14px;line-height:1.9}.book-section{margin-top:20px;padding-top:15px;border-top:1px solid #2b313c}.book-section h5{color:var(--yellow);font-size:11px;letter-spacing:.08em}.book-section>p{margin-top:8px;color:#aeb3bd;font-size:12px;line-height:1.9}.book-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:10px}.book-card{padding:12px;border-left:2px solid #777d89;background:rgba(255,255,255,.025)}.book-card:nth-child(2n){border-color:var(--cyan)}.book-card:nth-child(3n){border-color:var(--pink)}.book-card:nth-child(4n){border-color:var(--mint)}.book-card b{display:block;color:#ddd;font-size:11px}.book-card p,.book-card li{margin-top:5px;color:#999eaa;font-size:11px;line-height:1.8}.book-card ul{padding-left:15px}.book-card li+li{margin-top:3px}.book-source-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:10px}.book-source{padding:11px;background:rgba(255,255,255,.025)}.book-source b{display:block;color:#dfe2e8;font-size:11px;line-height:1.5}.book-source small{display:block;margin-top:3px;color:var(--cyan);font:10px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}.book-source p{margin-top:5px;color:#9197a3;font-size:10.5px;line-height:1.75}.book-lenses{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:16px}.book-lens{padding:14px;border-top:2px solid var(--pink);background:rgba(255,255,255,.025)}.book-lens:nth-child(2){border-color:var(--cyan)}.book-lens:nth-child(3){border-color:var(--yellow)}.book-lens h4{font-size:12px}.book-lens p{margin-top:6px;color:#999eaa;font-size:11px;line-height:1.8}.book-lens ul{margin-top:7px;padding-left:15px;color:#aeb3bd;font-size:11px;line-height:1.8}.book-lens li+li{margin-top:3px}.book-library{margin-top:16px;border-top:1px solid #303744}.book-library summary{padding:13px 0;color:#aeb3bd;font-size:12px;cursor:pointer}.book-library[open] summary{color:var(--yellow)}.cross-index{margin-top:28px;padding-top:22px;border-top:1px solid #303744}.cross-index h3{font-size:21px;letter-spacing:-.03em}.cross-index p{margin-top:5px;color:#858b96;font-size:12px;line-height:1.8}
.chapter-archive-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin-top:11px}.chapter-archive{padding:13px 14px;border:1px solid #39414d;border-top:2px solid var(--cyan);background:rgba(255,255,255,.035)}.chapter-archive:nth-child(2n){border-top-color:var(--pink)}.chapter-archive:nth-child(3n){border-top-color:var(--yellow)}.chapter-archive .archive-kind{color:var(--cyan);font:9px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.1em}.chapter-archive:nth-child(2n) .archive-kind{color:var(--pink)}.chapter-archive h6{margin-top:6px;color:#e2e4e8;font-size:12px;line-height:1.5}.chapter-archive .archive-meta{display:block;margin-top:5px;color:#7d8590;font:10px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace}.chapter-archive p{margin-top:8px;color:#a0a6b0;font-size:11px;line-height:1.8}.book-reader .chapter-archive{border-color:#c5b9a7;background:rgba(255,255,255,.46)}.book-reader .chapter-archive .archive-kind{color:#8b5b16}.book-reader .chapter-archive:nth-child(2n) .archive-kind{color:#7b4d76}.book-reader .chapter-archive h6{color:#252a2f}.book-reader .chapter-archive .archive-meta{color:#776f63}.book-reader .chapter-archive p{color:#55595c}
.chapter-archive .archive-sources{display:block;margin-top:5px;color:#8f96a2;font-size:9px;line-height:1.55}.book-reader .chapter-archive .archive-sources{color:#8c6f43}
@media(max-width:760px){.chapter-archive-grid{grid-template-columns:1fr}}
.book-volumes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;margin-top:18px}.book-volume{padding:10px;border:1px solid #303744;border-radius:6px;background:rgba(255,255,255,.025)}.book-volume b{display:block;color:var(--yellow);font:10px ui-monospace,SFMono-Regular,Menlo,monospace}.book-volume strong{display:block;margin-top:4px;color:#e2e4e9;font-size:11px}.book-volume small{display:block;margin-top:4px;color:#858b96;font-size:10px;line-height:1.65}.book-archives{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:16px}.book-archive-panel{min-width:0;border:1px solid #303744;border-radius:8px;background:rgba(255,255,255,.018)}.book-archive-panel summary{padding:12px;color:#c2c6ce;font-size:11px;cursor:pointer}.book-archive-panel[open] summary{color:var(--yellow);border-bottom:1px solid #303744}.archive-grid{display:grid;gap:6px;padding:8px}.archive-card{padding:10px;background:rgba(255,255,255,.025)}.archive-card b{display:block;color:#e0e3e8;font-size:11px;line-height:1.5}.archive-card small{display:block;margin-top:3px;color:var(--cyan);font:9px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}.archive-card p{margin-top:5px;color:#979da8;font-size:10.5px;line-height:1.75}.archive-card p+p{color:#7f8692}.archive-card .archive-label{margin-top:7px;color:var(--pink);font-size:9px}
.direction-tools{display:flex;gap:10px;align-items:center;padding:14px;border:1px solid var(--line);border-radius:10px;background:rgba(255,255,255,.025)}.direction-search{flex:1;position:relative}.direction-search input{width:100%;height:43px;padding:0 13px 0 37px;border:1px solid #39404d;border-radius:8px;background:#0f1217;color:#f2f2f5;outline:none}.direction-search input:focus{border-color:var(--cyan);box-shadow:0 0 0 3px rgba(125,249,255,.08)}.direction-search span{position:absolute;left:13px;top:8px;color:#777d89}.direction-count{color:#777d89;font-size:11px;white-space:nowrap}.advanced-filter{margin-top:10px;border:1px solid #252a33;border-radius:8px}.advanced-filter summary{padding:10px 12px;color:#8d929e;font-size:11px;cursor:pointer}.advanced-filter[open] summary{color:var(--yellow)}.reader-filters{display:flex;flex-wrap:wrap;gap:6px;padding:0 12px 12px}.filter-label{width:100%;margin-top:7px;color:#656b76;font:10px ui-monospace,SFMono-Regular,Menlo,monospace}.reader-filter{padding:6px 8px;border:1px solid #343a46;border-radius:5px;background:transparent;color:#969ba6;font-size:10px}.reader-filter.active,.reader-filter:hover{border-color:var(--yellow);color:var(--yellow)}.direction-layout{display:grid;grid-template-columns:280px minmax(0,1fr);gap:14px;margin-top:14px;align-items:start}.direction-index{position:sticky;top:12px;max-height:calc(100vh - 25px);overflow:auto;padding:7px;border:1px solid var(--line);border-radius:12px;background:#101319}.direction-index button{width:100%;display:grid;grid-template-columns:32px minmax(0,1fr);gap:7px;padding:9px;border:0;border-bottom:1px solid #252a33;background:none;color:#979ca7;text-align:left}.direction-index button:last-child{border-bottom:0}.direction-index button:hover,.direction-index button.active{background:rgba(125,249,255,.08);color:#fff}.direction-index .index-no{color:#707581;font:10px ui-monospace,SFMono-Regular,Menlo,monospace}.direction-index button.active .index-no{color:var(--cyan)}.direction-index strong{display:block;font-size:12px}.direction-index small{display:block;margin-top:2px;color:#707581;font-size:10px}.direction-reader{min-width:0;padding:28px;border:1px solid var(--line);border-radius:12px;background:linear-gradient(145deg,#171b23,#11141a)}.direction-reader .reader-kicker{color:var(--cyan);font:11px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em}.direction-reader h3{margin-top:12px;font-size:clamp(30px,5vw,56px);line-height:1.05;letter-spacing:-.06em}.reader-en{margin-top:6px;color:#777d89;font:12px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.1em}.reader-manifesto{margin-top:20px;color:#e2e3e8;font-size:16px;line-height:1.9}.reader-part{margin-top:25px;padding-top:18px;border-top:1px solid var(--line)}.reader-part-head{display:flex;align-items:baseline;gap:10px}.reader-part-head span{color:var(--yellow);font:11px ui-monospace,SFMono-Regular,Menlo,monospace}.reader-part-head b{font-size:14px}.reader-part-head small{color:#777d89;font-size:10px}.reader-copy{margin-top:12px;color:#aeb2bd;font-size:13px;line-height:2}.reader-history-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:14px}.reader-history-card{padding:13px;border-left:2px solid #777d89;background:rgba(255,255,255,.025)}.reader-history-card:nth-child(2n){border-color:var(--cyan)}.reader-history-card:nth-child(3n){border-color:var(--pink)}.reader-history-card:nth-child(4n){border-color:var(--mint)}.reader-history-card.wide{grid-column:1/-1}.reader-history-card b{display:block;color:#ddd;font-size:11px}.reader-history-card p,.reader-history-card li{margin-top:6px;color:#999eaa;font-size:12px;line-height:1.85}.reader-history-card ul{padding-left:16px}.reader-history-card li+li{margin-top:4px}.reader-sub{margin-top:17px;padding-bottom:7px;border-bottom:1px solid var(--line);color:#777d89;font:10px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em}.reader-traits{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:12px}.reader-trait{padding:13px;background:rgba(255,255,255,.025)}.reader-trait strong{font-size:12px}.reader-trait p{margin-top:5px;color:#999eaa;font-size:11.5px;line-height:1.8}.reader-list{margin-top:10px;padding-left:18px;color:#aeb2bd;font-size:12px}.reader-list li+li{margin-top:6px}.reader-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}.reader-tag{cursor:pointer;text-decoration:none}.reader-event-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}.reader-event-tags button{padding:6px 9px;border:1px solid #4d3d25;border-radius:6px;background:#272219;color:var(--yellow);font-size:10.5px}.reader-event-tags button:hover{border-color:var(--yellow)}.reader-application{margin-top:22px;border-top:1px solid var(--line)}.reader-application summary{padding:13px 0;color:#aeb2bd;font-size:12px;cursor:pointer}.reader-application[open] summary{color:var(--yellow)}.reader-application-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;padding-bottom:5px}.reader-application-card{padding:13px;background:rgba(255,255,255,.025)}.reader-application-card b{display:block;font-size:11px;color:#ddd;margin-bottom:5px}.reader-application-card p{color:#999eaa;font-size:12px;line-height:1.85}.reader-more{margin-top:10px;border-top:1px solid var(--line)}.reader-more summary{padding:12px 0;color:#aeb2bd;font-size:12px;cursor:pointer}.reader-more[open] summary{color:var(--yellow)}.reader-open{display:inline-flex;margin-top:22px;padding:10px 13px;border:1px solid var(--yellow);border-radius:7px;color:var(--yellow);text-decoration:none;font-size:12px}.reader-open:hover{background:rgba(255,210,63,.1)}.index-empty{padding:24px;color:#8e939e;font-size:12px}.book-footer{max-width:1280px;margin:0 auto;padding:25px 5vw 50px;border-top:1px solid #20242c;color:#6f7580;text-align:center;font-size:11px}

.aesthetic-lab{margin-top:30px;padding:26px;border:1px solid #38404d;border-radius:12px;background:linear-gradient(145deg,rgba(125,249,255,.07),rgba(255,210,63,.04))}.aesthetic-lab .lab-kicker{color:var(--cyan);font:11px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.16em}.aesthetic-lab h3{margin-top:10px;font-size:clamp(24px,4vw,42px);line-height:1.1;letter-spacing:-.04em}.lab-intro{max-width:850px;margin-top:12px;color:#b5bac5;font-size:13px;line-height:1.95}.lab-exchange{display:grid;grid-template-columns:minmax(0,1fr) 70px minmax(0,1fr);gap:10px;align-items:stretch;margin-top:20px}.lab-exchange-card{padding:15px;border-left:2px solid var(--yellow);background:rgba(255,255,255,.035)}.lab-exchange-card:nth-child(3){border-color:var(--pink)}.lab-exchange-card b{display:block;color:#e6e8ed;font-size:12px}.lab-exchange-card p{margin-top:6px;color:#999eaa;font-size:11.5px;line-height:1.8}.lab-arrow{display:grid;place-items:center;color:var(--yellow);font:20px ui-monospace,SFMono-Regular,Menlo,monospace}.lab-contributions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:14px}.lab-contribution{padding:13px;border-top:2px solid var(--cyan);background:rgba(255,255,255,.025)}.lab-contribution:nth-child(2){border-color:var(--yellow)}.lab-contribution:nth-child(3){border-color:var(--pink)}.lab-contribution b{display:block;color:#ddd;font-size:11px}.lab-contribution p{margin-top:5px;color:#999eaa;font-size:11px;line-height:1.8}.lab-contribution code{display:block;margin-top:8px;color:#c9faff;font:10px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:normal}.lab-workbench{display:grid;grid-template-columns:250px minmax(0,1fr);gap:12px;margin-top:16px}.lab-controls{padding:15px;border:1px solid #343b47;border-radius:9px;background:#10141a}.lab-control{display:block;color:#9da3af;font-size:11px}.lab-control+.lab-control{margin-top:12px}.lab-control select{width:100%;height:36px;margin-top:6px;padding:0 8px;border:1px solid #3b4350;border-radius:6px;background:#171c24;color:#e8e9ed;font-size:11px}.lab-feedback{margin-top:18px;padding-top:13px;border-top:1px solid #2e3540}.lab-feedback>b{display:block;color:#ddd;font-size:11px}.lab-feedback>p{margin-top:4px;color:#777d89;font-size:10px;line-height:1.7}.lab-feedback-buttons{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:9px}.lab-feedback button{min-height:36px;padding:6px;border:1px solid #4b5260;border-radius:6px;background:#1b2028;color:#bfc3cc;font-size:10px}.lab-feedback button:hover,.lab-feedback button:focus-visible{border-color:var(--yellow);color:var(--yellow);outline:none}.lab-rule{margin-top:15px;padding-top:12px;border-top:1px solid #2e3540}.lab-rule b{display:block;color:#ddd;font-size:11px}.lab-rule code{display:block;margin-top:6px;color:#c9faff;font:10px/1.75 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:normal}.lab-source{margin-top:7px;color:#777d89;font-size:10px;line-height:1.7}.lab-stage{min-width:0;padding:15px;border:1px solid #343b47;border-radius:9px;background:#0e1116}.lab-stage-head{display:flex;align-items:baseline;justify-content:space-between;gap:10px;color:#ddd;font-size:12px}.lab-stage-head span{color:#777d89;font:10px ui-monospace,SFMono-Regular,Menlo,monospace}.lab-canvas{display:grid;grid-template-columns:repeat(var(--lab-cols,2),minmax(0,1fr));gap:var(--lab-gap,12px);margin-top:13px;min-height:300px;align-content:start}.lab-block{min-height:74px;padding:12px;border:1px solid var(--lab-accent,#ffd23f);background:rgba(255,255,255,.045);color:#e8e9ed}.lab-block[data-span="2"]{grid-column:span 2}.lab-block[data-priority="3"]{min-height:106px}.lab-block[data-priority="3"] b{font-size:15px}.lab-block[data-priority="1"]{opacity:.68}.lab-block-no{display:block;color:var(--lab-accent,#ffd23f);font:10px ui-monospace,SFMono-Regular,Menlo,monospace}.lab-block b{display:block;margin-top:7px;font-size:12px}.lab-block p{margin-top:5px;color:#aeb3bd;font-size:10.5px;line-height:1.7}.lab-canvas[data-model="grid"] .lab-block{border-radius:0}.lab-canvas[data-model="module"] .lab-block{border-style:dashed;border-radius:4px}.lab-canvas[data-model="perception"] .lab-block[data-group="a"]{border-color:var(--cyan);background:rgba(125,249,255,.08)}.lab-canvas[data-model="perception"] .lab-block[data-group="b"]{border-color:var(--pink);background:rgba(255,113,206,.07)}.lab-canvas[data-model="feedback"] .lab-block{border-radius:12px}.lab-canvas[data-model="feedback"] .lab-block[data-state="status"]{border-color:var(--mint);box-shadow:0 0 0 2px rgba(167,255,234,.08)}.lab-metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin-top:12px}.lab-metric{padding:9px 8px;background:rgba(255,255,255,.035)}.lab-metric b{display:block;color:#777d89;font-size:9px}.lab-metric span{display:block;margin-top:4px;color:var(--yellow);font:14px ui-monospace,SFMono-Regular,Menlo,monospace}.lab-status{margin-top:12px;padding-top:11px;border-top:1px solid #2e3540;color:#aeb3bd;font-size:11px;line-height:1.8}.lab-log{display:grid;gap:5px;margin:13px 0 0;padding:0;list-style:none}.lab-log li{padding:8px 10px;border-left:2px solid #555d6b;background:rgba(255,255,255,.025);color:#8e949f;font-size:10px;line-height:1.7}.lab-log li:first-child{border-color:var(--yellow);color:#c4c8d0}.lab-note{margin-top:12px;color:#6f7682;font-size:10px;line-height:1.8}@media(max-width:760px){.aesthetic-lab{padding:19px}.lab-exchange{grid-template-columns:1fr;gap:7px}.lab-arrow{transform:rotate(90deg);min-height:26px}.lab-contributions{grid-template-columns:1fr}.lab-workbench{grid-template-columns:1fr}.lab-canvas{grid-template-columns:repeat(2,minmax(0,1fr));min-height:0}.lab-block[data-span="2"]{grid-column:span 2}.lab-metrics{grid-template-columns:repeat(2,minmax(0,1fr))}}
.lab-block[data-priority="3"] b{font-size:var(--lab-priority-size,15px)}.lab-canvas.quiet .lab-block{background:transparent;border-radius:0;box-shadow:none}.lab-canvas.quiet .lab-block-no{color:#aeb3bd}

@media(max-width:760px){.site-nav{align-items:flex-start;flex-direction:column;gap:11px}.site-nav nav{gap:12px}.book-hero{padding:52px 5vw 60px}.hero-intro{font-size:13px}.route-grid{grid-template-columns:1fr}.route-card{min-height:120px}.mode-panel{padding:38px 5vw 65px}.mode-heading{display:block}.mode-heading>p{margin-top:12px}.history-layout,.direction-layout{display:flex;flex-direction:column}.history-nav,.direction-index{position:static;width:100%;max-height:280px}.history-reader,.direction-reader{padding:20px}.history-grid,.history-application-grid,.reader-history-grid,.reader-application-grid,.reader-traits{grid-template-columns:1fr}.reader-history-card.wide{grid-column:auto}.direction-tools{display:block}.direction-count{display:block;margin-top:8px}.book-footer{padding-bottom:35px}}
@media(max-width:760px){.book-volumes,.book-archives{grid-template-columns:1fr}.book-volume{padding:9px}.book-archive-panel{width:100%}}
@media(max-width:760px){.book-spine{padding:16px}.book-spine-head{display:block}.book-spine-head p{margin-top:10px}.book-layout{display:flex;flex-direction:column}.book-nav{position:static;width:100%;max-height:240px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px}.book-nav button{border:1px solid #252a33;border-radius:5px}.book-reader{padding:18px}.book-cards,.book-source-grid,.book-lenses{grid-template-columns:1fr}.book-lens{padding:12px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;transition-duration:.001s!important}}
.book-spine{border-color:#4b525d;background:linear-gradient(135deg,#151a21 0%,#11151b 55%,#1b2028 100%);box-shadow:0 24px 70px rgba(0,0,0,.22)}.book-spine:before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,transparent 0 49.8%,rgba(255,255,255,.04) 50%,transparent 50.2%),linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px);background-size:100% 100%,100% 28px;pointer-events:none}.book-spine>*{position:relative}.book-spine-head h3{font-size:clamp(30px,5vw,58px);color:#f4f0e7}.book-spine-head p{color:#aeb4bd}.book-volumes{gap:8px}.book-volume{min-height:104px;display:flex;flex-direction:column;justify-content:space-between;border:1px solid #3b434f;border-top:3px solid var(--yellow);background:rgba(255,255,255,.035);transition:transform .2s,border-color .2s,background .2s}.book-volume:nth-child(2){border-top-color:var(--cyan)}.book-volume:nth-child(3){border-top-color:var(--pink)}.book-volume:nth-child(4){border-top-color:var(--mint)}.book-volume:nth-child(5){border-top-color:#c89cff}.book-volume:nth-child(6){border-top-color:#ff9d71}.book-volume:hover{transform:translateY(-3px);border-color:#87909d;background:rgba(255,255,255,.08)}.book-volume b{font-size:11px}.book-volume strong{font-size:13px}.book-volume small{font-size:10.5px}.book-nav{padding:10px 0 10px 10px;border:0;border-left:1px solid #3b434f;border-radius:0;background:rgba(8,11,15,.62)}.book-nav button{position:relative;padding:14px 12px 14px 24px;border-bottom:1px solid #29303a;border-left:2px solid transparent}.book-nav button:before{content:"";position:absolute;left:7px;top:19px;width:7px;height:7px;border:1px solid #67717e;border-radius:50%;background:#11151b}.book-nav button.active{border-left-color:var(--yellow);background:linear-gradient(90deg,rgba(255,210,63,.13),transparent);color:#fff}.book-nav button.active:before{border-color:var(--yellow);background:var(--yellow);box-shadow:0 0 0 4px rgba(255,210,63,.12)}.book-nav .book-no{font-size:9px;letter-spacing:.06em}.book-nav strong{font-size:12px}.book-reader{padding:32px;border:0;border-radius:2px;background:linear-gradient(135deg,#f4f0e7,#e4ddcf);color:#20252b;box-shadow:12px 12px 0 rgba(0,0,0,.15);clip-path:polygon(0 0,100% 0,100% 99%,98% 100%,0 100%)}.book-reader:before{content:"ARCHIVE / READING COPY";display:block;padding-bottom:9px;border-bottom:1px solid #c2b8a7;color:#90733e;font:10px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.16em}.book-reader .book-kicker{margin-top:20px;color:#8b5b16;font-weight:700}.book-reader h4{color:#171b20;font-size:clamp(32px,5vw,64px);letter-spacing:-.065em}.book-reader .book-period{color:#6c6b67}.book-reader-meta{display:flex;flex-wrap:wrap;gap:7px;margin-top:18px;padding:10px 0;border-top:1px solid #c2b8a7;border-bottom:1px solid #c2b8a7}.book-reader-meta span{padding:5px 8px;border:1px solid #b9ad9b;color:#6d6558;font:9px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.04em}.book-reader-meta b{color:#242a30;font-weight:700}.book-thesis{margin-top:20px;border-left:5px solid #d28b22;background:rgba(255,255,255,.5);color:#2a3035;font-size:15px;box-shadow:inset 0 0 0 1px rgba(155,125,76,.1)}.book-section{border-top-color:#c5baaa}.book-section h5{color:#965e12}.book-section>p,.book-section>ul{color:#4a4d50}.book-section>ul{padding-left:20px;margin-top:10px}.book-section>ul li{line-height:1.9}.book-section>ul li+li{margin-top:4px}.book-card{border-left-color:#9b6b28;background:rgba(255,255,255,.48);box-shadow:0 1px 0 rgba(125,96,51,.1)}.book-card:nth-child(2n){border-color:#397a85}.book-card:nth-child(3n){border-color:#a05277}.book-card:nth-child(4n){border-color:#5e8a6d}.book-card b{color:#252a2f}.book-card p,.book-card li{color:#55595c}.book-reader .book-source{background:rgba(255,255,255,.5)}.book-reader .book-source b{color:#252a2f}.book-reader .book-source small{color:#7b5b2b}.book-reader .book-source p{color:#5b5d5e}.book-lens{min-height:178px}.book-archive-panel{background:rgba(255,255,255,.04)}
@media(max-width:760px){.book-reader{padding:22px;clip-path:none;box-shadow:6px 6px 0 rgba(0,0,0,.13)}.book-reader h4{font-size:clamp(30px,10vw,46px)}.book-reader-meta{gap:5px}.book-reader-meta span{font-size:8.5px}.book-nav{padding:8px;border-left:0}.book-nav button{padding-left:22px}.book-volume{min-height:92px}.book-spine-head h3{font-size:clamp(30px,10vw,46px)}}
.history-track-nav{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:4px 0 24px;padding:8px;border:1px solid #38404d;border-radius:10px;background:#10141a}.history-track-nav button{position:relative;min-height:70px;padding:11px 12px 11px 47px;text-align:left;border:1px solid transparent;border-radius:7px;background:transparent;color:#858c98}.history-track-nav button span{position:absolute;left:13px;top:14px;color:#5f6875;font:11px ui-monospace,SFMono-Regular,Menlo,monospace}.history-track-nav button strong{display:block;color:#c7cbd2;font-size:13px}.history-track-nav button small{display:block;margin-top:3px;color:#727a86;font-size:10px}.history-track-nav button:hover{border-color:#555f6d;background:rgba(255,255,255,.04)}.history-track-nav button.active{border-color:var(--yellow);background:linear-gradient(135deg,rgba(255,210,63,.16),rgba(255,210,63,.035));color:#fff}.history-track-nav button.active span{color:var(--yellow)}.history-track-nav button.active strong{color:#fff}.history-track-nav button[data-history-track-control="events"].active{border-color:var(--cyan);background:linear-gradient(135deg,rgba(125,249,255,.13),rgba(125,249,255,.03))}.history-track-nav button[data-history-track-control="events"].active span{color:var(--cyan)}.history-track-nav button[data-history-track-control="lab"].active{border-color:var(--pink);background:linear-gradient(135deg,rgba(255,113,206,.13),rgba(255,113,206,.03))}.history-track-nav button[data-history-track-control="lab"].active span{color:var(--pink)}[data-history-track][hidden]{display:none!important}
@media(max-width:760px){.history-track-nav{grid-template-columns:1fr;margin-bottom:18px}.history-track-nav button{min-height:54px;padding-left:42px}.history-track-nav button span{top:15px}.history-track-nav button strong{font-size:12px}.history-track-nav button small{font-size:9.5px}}
'''


HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>现代设计史与主义索引 · 主义馆</title>
<meta name="description" content="从现代设计史开始，理解 80 个设计方向、9 个历史事件与各自的独立展厅。">
<style>@@CSS@@</style>
</head>
<body>
<header class="site-nav">
  <a class="site-brand" href="index.html">主义馆 <small>ISM MUSEUM</small></a>
  <nav aria-label="全书路线">
    <a class="site-back" href="index.html" aria-label="返回主页">← 返回主页</a>
    <a href="#history" data-mode="history">历史路线</a>
    <a href="#directions" data-mode="directions">主义索引</a>
    <a href="corridor.html">漫游长廊</a>
  </nav>
</header>
<header class="book-hero">
  <div class="eyebrow">MODERN DESIGN HISTORY / READING ROUTE</div>
  <h1>现代设计史<br><em>与主义索引</em></h1>
  <p class="hero-intro">先沿历史理解现代设计如何形成，再选择一个方向深入。这里不是前端风格目录：前端、代码与标本都放在历史阅读之后。</p>
  <div class="route-grid" aria-label="选择阅读路线">
    <button class="route-card primary" type="button" data-mode="history"><span class="route-no">ROUTE 01</span><strong>从现代设计史开始</strong><small>14 个通史章节，另有 9 个横向事件，按时间理解生产、传播、教育和技术如何改变设计。</small></button>
    <button class="route-card" type="button" data-mode="directions"><span class="route-no">ROUTE 02</span><strong>按设计主义浏览</strong><small>80 个方向，每个方向都有自己的起源、人物、转折和争议。</small></button>
  </div>
</header>
<main class="book-main">
<section class="mode-panel" id="history" data-panel="history">
  <div class="mode-heading"><div><div class="mode-kicker">ROUTE 01 / HISTORY</div><h2>先读历史</h2></div><p>先读 14 个连续章节，再用 9 个横向事件交叉阅读。每章都把时间、地点、生产、作品、争议和延伸阅读放在一起。</p></div>
  <div class="history-track-nav" role="tablist" aria-label="历史阅读层级"><button type="button" class="active" data-history-track-control="book" role="tab" aria-selected="true"><span>01</span><strong>通史主干</strong><small>14 章连续时间线</small></button><button type="button" data-history-track-control="events" role="tab" aria-selected="false"><span>02</span><strong>横向事件</strong><small>9 个关联切面</small></button><button type="button" data-history-track-control="lab" role="tab" aria-selected="false"><span>03</span><strong>设计实验</strong><small>规则与人机反馈</small></button></div>
  <section class="book-spine" data-history-track="book" aria-labelledby="book-spine-title">
    <div class="book-spine-head"><div><div class="mode-kicker">VOLUME I / CHRONOLOGY</div><h3 id="book-spine-title">现代设计通史主干</h3></div><p>这不是 80 个方向的重新命名，而是一条从工业化、工艺改革、先锋传播、现代主义教育，到平台、人工智能和生态约束的连续历史线。</p></div>
    <div class="book-volumes" id="book-volumes" aria-label="现代设计全书六卷结构"></div>
    <div class="book-layout"><nav class="book-nav" id="book-nav" aria-label="现代设计通史章节"></nav><article class="book-reader" id="book-reader" aria-live="polite"></article></div>
    <div class="book-lenses" id="book-lenses" aria-label="全书横向阅读视角"></div>
    <div class="book-archives" aria-label="实践、全球与机构档案"><details class="book-archive-panel"><summary>卷 II · 设计实践史 · 8 条实践线</summary><div class="archive-grid" id="practice-archive"></div></details><details class="book-archive-panel"><summary>卷 III · 全球与权力关系 · 8 个区域线索</summary><div class="archive-grid" id="global-archive"></div></details><details class="book-archive-panel"><summary>卷 VI · 机构档案 · 8 个制度节点</summary><div class="archive-grid" id="institution-archive"></div></details></div>
    <details class="book-library"><summary>参考资料库（本地静态书目，不依赖运行时外部请求）</summary><div class="book-source-grid" id="book-source-grid"></div></details>
  </section>
  <div class="cross-index" data-history-track="events" hidden><h3>横向历史事件索引</h3><p>以下 9 个事件不是通史主目录，而是用生产、传播、教育、媒介和平台等问题重新连接各个方向。</p></div>
  <div class="history-layout" data-history-track="events" hidden><nav class="history-nav" id="history-nav" aria-label="现代设计史章节"></nav><article class="history-reader" id="history-reader" aria-live="polite"></article></div>
<div class="aesthetic-lab" id="aesthetic-lab" data-history-track="lab" aria-labelledby="aesthetic-lab-title" hidden>
  <div class="lab-kicker">BRIDGE / DESIGN AS COMPUTATIONAL KNOWLEDGE</div>
  <h3 id="aesthetic-lab-title">现代设计美学：艺术怎样给计算机新的问题</h3>
  <p class="lab-intro">艺术不会让 CPU 更快，也不会自动改善算法复杂度。它能提供的是计算机常常缺少的目标：什么叫清楚、什么叫有层级、什么叫可重复、什么叫不排除使用者。现代设计把这些判断转成网格、模块、感知组织和反馈规则，让计算机不只“生成结果”，还知道应该追求什么。</p>
  <div class="lab-exchange">
    <article class="lab-exchange-card"><b>计算机服务现代设计</b><p>把设计思想执行成约束和布局：排序内容、分配空间、保持对齐、处理响应式设备，并计算可读性和一致性指标。</p></article>
    <div class="lab-arrow" aria-hidden="true">↔</div>
    <article class="lab-exchange-card"><b>现代设计反哺计算机</b><p>把艺术判断变成计算目标：网格贡献布局约束，模块化贡献组件系统，感知组织贡献分组规则，交互设计贡献反馈和可恢复状态。</p></article>
  </div>
  <div class="lab-contributions">
    <article class="lab-contribution"><b>瑞士国际主义 · 网格与层级</b><p>不是复制红色海报，而是借鉴对齐、比例和信息优先级。</p><code>layout = sort(priority) + align(grid) + limit(lineLength)</code></article>
    <article class="lab-contribution"><b>包豪斯与工业设计 · 模块与标准</b><p>不是复制圆方三角，而是借鉴可复用单元、标准尺寸和生产关系。</p><code>component = token + state + reusableRule</code></article>
    <article class="lab-contribution"><b>格式塔与交互设计 · 感知与反馈</b><p>不是添加装饰，而是借鉴接近、相似、连续和反馈可见性。</p><code>group(gap) + signal(state) + recover(error)</code></article>
  </div>
  <div class="lab-workbench">
    <aside class="lab-controls" aria-label="计算原则实验控制">
      <label class="lab-control">借鉴的设计传统<select id="lab-model"><option value="grid">网格与信息层级</option><option value="module">模块与标准化</option><option value="perception">感知分组</option><option value="feedback">反馈与可恢复状态</option></select></label>
      <label class="lab-control">计算环境<select id="lab-device"><option value="desktop">桌面宽屏 · 1440px</option><option value="mobile">手机窄屏 · 390px</option></select></label>
      <div class="lab-feedback"><b>把艺术判断写回计算规则</b><p>这不是“喜欢 / 不喜欢”投票。每个判断都会改变目标函数或约束。</p><div class="lab-feedback-buttons"><button type="button" data-lab-feedback="hierarchy">层级不够</button><button type="button" data-lab-feedback="grouping">分组不清</button><button type="button" data-lab-feedback="ornament">装饰干扰</button><button type="button" data-lab-feedback="recovery">需要反馈</button></div></div>
      <div class="lab-rule"><b>当前可执行规则</b><code id="lab-rule"></code><p class="lab-source" id="lab-source"></p></div>
    </aside>
    <div class="lab-stage"><div class="lab-stage-head"><b id="lab-stage-title">计算结果</b><span id="lab-iteration">第 0 轮</span></div><div class="lab-canvas" id="lab-canvas" data-model="grid" aria-label="根据设计原则计算出的内容布局"></div><div class="lab-metrics" id="lab-metrics"></div><p class="lab-status" id="lab-status" aria-live="polite"></p></div>
  </div>
  <ol class="lab-log" id="lab-log" aria-label="设计判断回写记录"></ol>
  <p class="lab-note">本实验的反哺对象是“人机系统的目标函数和界面算法”，不是 CPU 硬件。反馈只保存在当前页面会话；它证明了设计思想可以成为计算规则，但尚未连接持久化用户研究或真实生产系统。</p>
</div>
</section>

<section class="mode-panel" id="directions" data-panel="directions" hidden>
  <div class="mode-heading"><div><div class="mode-kicker">ROUTE 02 / INDEX</div><h2>按设计主义浏览</h2></div><p>这里是方向索引，不是默认首页。搜索一个方向，读完它自己的历史，再进入对应独立展厅。</p></div>
  <div class="direction-tools"><label class="direction-search"><span>⌕</span><input id="direction-search" type="search" placeholder="搜索方向、人物、年代或历史问题" autocomplete="off"></label><span class="direction-count" id="direction-count" aria-live="polite"></span></div>
  <details class="advanced-filter"><summary id="filter-summary">高级筛选（历史事件 / 课程视角）</summary><div class="reader-filters" id="reader-filters"></div></details>
  <div class="direction-layout"><aside class="direction-index" id="direction-index" aria-label="设计方向索引"></aside><article class="direction-reader" id="direction-reader" aria-live="polite"></article></div>
</section>
</main>
<footer class="book-footer"><a href="index.html">回到主义馆入口</a> · 历史路线 → 方向索引 → 独立展厅</footer>
<script type="application/json" id="course-data">@@AXES@@</script>
<script type="application/json" id="event-data">@@EVENTS@@</script>
<script type="application/json" id="book-data">@@BOOK@@</script>
<script type="application/json" id="ism-data">@@RECORDS@@</script>
<script>
const events=JSON.parse(document.getElementById('event-data').textContent);
const axes=JSON.parse(document.getElementById('course-data').textContent);
const records=JSON.parse(document.getElementById('ism-data').textContent);
const bookData=JSON.parse(document.getElementById('book-data').textContent);
const chapters=bookData.chapters;
const lenses=bookData.lenses;
const sources=bookData.sources;
const volumes=bookData.volumes;
const practiceFields=bookData.practiceFields;
const globalRegions=bookData.globalRegions;
const institutions=bookData.institutions;
const sourceByKey=Object.fromEntries(sources.map(source=>[source.key,source]));
const chapterArchives=bookData.archives;
const eventByKey=Object.fromEntries(events.map(event=>[event.key,event]));
const axisByKey=Object.fromEntries(axes.map(axis=>[axis.key,axis]));
const recordBySlug=Object.fromEntries(records.map(record=>[record.slug,record]));
const historyNav=document.getElementById('history-nav');
const historyReader=document.getElementById('history-reader');
const directionIndex=document.getElementById('direction-index');
const bookNav=document.getElementById('book-nav');
const bookReader=document.getElementById('book-reader');
const bookLenses=document.getElementById('book-lenses');
const bookSourceGrid=document.getElementById('book-source-grid');
const directionReader=document.getElementById('direction-reader');
const search=document.getElementById('direction-search');
const bookVolumes=document.getElementById('book-volumes');
const practiceArchive=document.getElementById('practice-archive');
const globalArchive=document.getElementById('global-archive');
const institutionArchive=document.getElementById('institution-archive');
const count=document.getElementById('direction-count');
const filters=document.getElementById('reader-filters');
const filterSummary=document.getElementById('filter-summary');
const historyTrackControls=document.querySelectorAll('[data-history-track-control]');
let activeMode='history';
let activeEvent=events[0]?.key;
let activeSlug=records[0]?.slug;
let activeEventFilter='all';
let activeAxisFilter='all';
let activeHistoryTrack='book';
const esc=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
let activeChapter=chapters[0]?.key;
const eventLabel=key=>eventByKey[key]?.event||key;
const axisLabel=key=>axisByKey[key]?.title||key;
const list=items=>items?.length?`<ul class="reader-list">${items.map(item=>`<li>${esc(item)}</li>`).join('')}</ul>`:'<p class="reader-copy">暂无整理内容。</p>';
const bullets=items=>`<ul>${(items||[]).map(item=>`<li>${esc(item)}</li>`).join('')}</ul>`;
const sourceCards=keys=>`<div class="book-source-grid">${(keys||[]).map(key=>{const source=sourceByKey[key];return source?`<article class="book-source"><b>${esc(source.title)}</b><small>${esc(source.author)} · ${esc(source.year)} · ${esc(source.publisher)}</small><p>${esc(source.why)}</p></article>`:''}).join('')}</div>`;
const archiveSources=keys=>(keys||[]).map(key=>sourceByKey[key]?.author||key).join(' · ');
const archiveCards=key=>`<div class="chapter-archive-grid">${(chapterArchives[key]||[]).map(item=>`<article class="chapter-archive"><div class="archive-kind">${esc(item.kind)}</div><h6>${esc(item.title)}</h6><small class="archive-meta">${esc(item.date)} · ${esc(item.place)}</small><small class="archive-sources">档案依据：${esc(archiveSources(item.source_keys))}</small><p><b>${esc(item.people)}</b><br>${esc(item.institution)}<br>${esc(item.role)}</p></article>`).join('')}</div>`;
function renderBookNav(){
  bookNav.innerHTML=chapters.map(chapter=>`<button type="button" class="${chapter.key===activeChapter?'active':''}" data-book-chapter="${esc(chapter.key)}"><span class="book-no">CHAPTER ${esc(chapter.no)} · ${esc(chapter.period)}</span><strong>${esc(chapter.title)}</strong><small>${chapter.works.length} 个作品 · ${chapter.source_keys.length} 条来源</small></button>`).join('');
}
function renderBookReader(){
  const chapter=chapters.find(item=>item.key===activeChapter)||chapters[0];
  if(!chapter)return;
  bookReader.innerHTML=`<div class="book-kicker">VOLUME I / CHAPTER ${esc(chapter.no)}</div><h4>${esc(chapter.title)}</h4><div class="book-period">${esc(chapter.period)} · 主干章节</div><div class="book-reader-meta"><span>TIME <b>${esc(chapter.period)}</b></span><span>WORKS <b>${chapter.works.length}</b></span><span>PRACTICES <b>${chapter.practices.length}</b></span><span>SOURCES <b>${chapter.source_keys.length}</b></span></div><p class="book-thesis">${esc(chapter.thesis)}</p><section class="book-section"><h5>01 / 历史条件</h5><p>${esc(chapter.context)}</p><div class="book-cards"><article class="book-card"><b>参与者与制度</b><p>${esc(chapter.actors)}</p></article><article class="book-card"><b>地点与传播范围</b><p>${esc(chapter.places)}</p></article></div></section><section class="book-section"><h5>02 / 档案坐标</h5>${archiveCards(chapter.key)}</section><section class="book-section"><h5>03 / 设计实践线</h5><div class="book-cards">${chapter.practices.map(item=>`<article class="book-card"><b>实践档案</b><p>${esc(item)}</p></article>`).join('')}</div></section><section class="book-section"><h5>04 / 关键转折</h5>${bullets(chapter.turning_points)}</section><section class="book-section"><h5>05 / 作品与媒介线索</h5>${bullets(chapter.works)}</section><section class="book-section"><h5>06 / 争议与限制</h5><p>${esc(chapter.debate)}</p></section><section class="book-section"><h5>07 / 留下什么</h5><p>${esc(chapter.legacy)}</p></section><section class="book-section"><h5>08 / 延伸阅读</h5>${sourceCards(chapter.source_keys)}</section>`;
}
function renderBookLenses(){
  bookLenses.innerHTML=lenses.map(lens=>`<article class="book-lens"><h4>${esc(lens.title)}</h4><p>${esc(lens.summary)}</p><ul>${lens.items.map(item=>`<li>${esc(item)}</li>`).join('')}</ul></article>`).join('');
}
function renderBookSources(){
  bookSourceGrid.innerHTML=sources.map(source=>`<article class="book-source"><b>${esc(source.title)}</b><small>${esc(source.author)} · ${esc(source.year)} · ${esc(source.publisher)}</small><p>${esc(source.why)}</p></article>`).join('');
}
const archiveRefs=keys=>(keys||[]).map(key=>sourceByKey[key]?.author||key).join(' · ');
function renderBookVolumes(){
  bookVolumes.innerHTML=volumes.map(volume=>`<article class="book-volume"><b>${esc(volume.label)}</b><strong>${esc(volume.title)}</strong><small>${esc(volume.status)}</small></article>`).join('');
}
function renderBookArchives(){
  practiceArchive.innerHTML=practiceFields.map(item=>`<article class="archive-card"><b>${esc(item.title)}</b><small>${esc(item.period)}</small><p>${esc(item.scope)}</p><p>${esc(item.production)}</p><div class="archive-label">问题 · ${esc(item.question)}</div></article>`).join('');
  globalArchive.innerHTML=globalRegions.map(item=>`<article class="archive-card"><b>${esc(item.title)}</b><small>${esc(item.period)}</small><p>${esc(item.route)}</p><p>${esc(item.practices)}</p><div class="archive-label">张力 · ${esc(item.tension)}</div><small>${esc(archiveRefs(item.source_keys))}</small></article>`).join('');
  institutionArchive.innerHTML=institutions.map(item=>`<article class="archive-card"><b>${esc(item.title)}</b><small>${esc(item.place)} · ${esc(item.period)}</small><p>${esc(item.role)}</p><div class="archive-label">追问 · ${esc(item.question)}</div><small>${esc(archiveRefs(item.source_keys))}</small></article>`).join('');
}
const labModels={
  grid:{label:'网格与信息层级',source:'瑞士国际主义设计：借鉴网格、对齐、比例和信息优先级，不复制表面风格。',rule:'按 priority 排序 → 对齐共享网格 → 限制文字长度 → 检查层级差异。',columns:2,gap:14,hierarchy:82,grouping:68,consistency:76,recovery:48,accent:'#ffd23f'},
  module:{label:'模块与标准化',source:'包豪斯与工业设计：借鉴模块、标准尺寸和生产关系，不复制圆方三角。',rule:'共享 token → 重复组件 → 只允许有意义的状态差异 → 检查复用一致性。',columns:3,gap:10,hierarchy:68,grouping:78,consistency:88,recovery:52,accent:'#7df9ff'},
  perception:{label:'感知分组',source:'格式塔与信息设计：借鉴接近、相似、连续和闭合，把视觉判断变成分组规则。',rule:'先计算 group → 组内距离小于组间距离 → 用相似性标记关系 → 检查误读。',columns:2,gap:18,hierarchy:74,grouping:88,consistency:62,recovery:54,accent:'#ff71ce'},
  feedback:{label:'反馈与可恢复状态',source:'控制论、交互设计与人因：借鉴状态、反馈和纠错，不把界面当成一次性海报。',rule:'每个动作产生可见 status → 错误可恢复 → 状态变化可解释 → 检查任务是否完成。',columns:2,gap:12,hierarchy:72,grouping:70,consistency:68,recovery:92,accent:'#a7ffea'}
};
const labBlocks=[['01','核心命题','最重要的信息先进入阅读路径。',3,'a'],['02','背景','说明问题发生在什么历史和生产条件中。',2,'a'],['03','方法','把判断拆成可以重复执行的动作。',2,'b'],['04','材料','说明结构、媒介和设备带来的限制。',1,'b'],['05','案例','让抽象原则接受具体作品的检验。',2,'c'],['06','反馈','记录使用者是否理解并完成任务。',3,'c'],['07','责任','检查谁被帮助、谁被排除。',1,'d'],['08','下一轮','保留修改理由，而不是只保留最终样式。',2,'d']];
const labModel=document.getElementById('lab-model');
const labDevice=document.getElementById('lab-device');
const labCanvas=document.getElementById('lab-canvas');
const labStageTitle=document.getElementById('lab-stage-title');
const labIteration=document.getElementById('lab-iteration');
const labRule=document.getElementById('lab-rule');
const labSource=document.getElementById('lab-source');
const labMetrics=document.getElementById('lab-metrics');
const labStatus=document.getElementById('lab-status');
const labLog=document.getElementById('lab-log');
const labState={hierarchy:0,grouping:0,ornament:0,recovery:0};
let labRound=0;
const clamp=(value,min=0,max=100)=>Math.min(max,Math.max(min,value));
function renderLab(){
  const model=labModels[labModel.value];
  const mobile=labDevice.value==='mobile';
  const columns=mobile?Math.min(2,model.columns):model.columns;
  const gap=Math.max(8,model.gap-(labState.grouping/3));
  const hierarchy=clamp(model.hierarchy+labState.hierarchy);
  const grouping=clamp(model.grouping+labState.grouping);
  const consistency=clamp(model.consistency-labState.ornament+labState.hierarchy/3);
  const recovery=clamp(model.recovery+labState.recovery);
  labCanvas.dataset.model=labModel.value;
  labCanvas.classList.toggle('quiet',labState.ornament>0);
  labCanvas.style.setProperty('--lab-cols',columns);
  labCanvas.style.setProperty('--lab-gap',`${gap.toFixed(1)}px`);
  labCanvas.style.setProperty('--lab-accent',model.accent);
  labCanvas.style.setProperty('--lab-priority-size',`${(13+hierarchy/25).toFixed(1)}px`);
  labStageTitle.textContent=`计算结果 · ${model.label} · ${mobile?'390px':'1440px'}`;
  labIteration.textContent=`第 ${labRound} 轮`;
  labRule.textContent=`${model.rule} 当前间距 ${gap.toFixed(1)}px，${mobile?'窄屏限制为两列。':'宽屏使用 '+columns+' 列。'}`;
  labSource.textContent=model.source;
  labCanvas.innerHTML=labBlocks.map((block,index)=>{const span=index===0||index===5?'2':'1';return `<article class="lab-block" data-priority="${block[3]}" data-group="${block[4]}" data-state="${index===5?'status':''}" data-span="${span}"><span class="lab-block-no">${block[0]}</span><b>${block[1]}</b><p>${block[2]}</p></article>`}).join('');
  labMetrics.innerHTML=[['层级',hierarchy],['分组',grouping],['一致',consistency],['可恢复',recovery]].map(([label,value])=>`<div class="lab-metric"><b>${label}</b><span>${Math.round(value)}</span></div>`).join('');
  labStatus.textContent=`计算机正在执行“${model.label}”。这些分数不是美学真理，而是把设计判断暂时变成可讨论的评价指标。`;
}
function logLab(message){const item=document.createElement('li');item.textContent=message;labLog.prepend(item);while(labLog.children.length>5)labLog.lastElementChild.remove();}
function applyLabFeedback(type){
  let message='';
  if(type==='hierarchy'){labState.hierarchy+=14;message='层级不够：提高优先级差异，扩大主次信息的尺寸和排序差距。';}
  if(type==='grouping'){labState.grouping+=15;message='分组不清：收紧组内间距，同时提高组间关系的评价权重。';}
  if(type==='ornament'){labState.ornament+=18;message='装饰干扰：降低装饰权重，要求输出优先保留结构和信息。';}
  if(type==='recovery'){labModel.value='feedback';labState.recovery+=14;message='需要反馈：切换到状态优先模型，要求操作结果可见且错误可恢复。';}
  labRound+=1;renderLab();labStatus.textContent=`第 ${labRound} 轮已回写：${message}`;logLab(`第 ${labRound} 轮 · ${message}`);
}
labModel.addEventListener('change',()=>{labRound+=1;renderLab();logLab(`第 ${labRound} 轮 · 设计传统改为“${labModels[labModel.value].label}”。`)});
labDevice.addEventListener('change',()=>{labRound+=1;renderLab();logLab(`第 ${labRound} 轮 · 计算环境改为“${labDevice.value==='mobile'?'390px 窄屏':'1440px 宽屏'}”。`)});
document.querySelectorAll('[data-lab-feedback]').forEach(button=>button.addEventListener('click',()=>applyLabFeedback(button.dataset.labFeedback)));
renderLab();
logLab('第 0 轮 · 设计传统先被翻译成规则、约束和评价指标。');

function setHistoryTrack(track){
  activeHistoryTrack=['book','events','lab'].includes(track)?track:'book';
  document.querySelectorAll('[data-history-track]').forEach(panel=>{panel.hidden=panel.dataset.historyTrack!==activeHistoryTrack});
  historyTrackControls.forEach(control=>{const active=control.dataset.historyTrackControl===activeHistoryTrack;control.classList.toggle('active',active);control.setAttribute('aria-selected',String(active));});
}
function setMode(mode,updateHash=true){
  activeMode=mode==='directions'?'directions':'history';
  document.querySelectorAll('[data-panel]').forEach(panel=>{panel.hidden=panel.dataset.panel!==activeMode});
  document.querySelectorAll('[data-mode]').forEach(control=>control.classList.toggle('active',control.dataset.mode===activeMode));
  if(updateHash)history.replaceState(null,'','#'+activeMode);
}
function renderHistoryNav(){
  historyNav.innerHTML=events.map(event=>`<button type="button" class="${event.key===activeEvent?'active':''}" data-history-event="${esc(event.key)}"><span class="chapter-no">CHAPTER ${esc(event.no)} · ${esc(event.period)}</span><strong>${esc(event.event)}</strong><small>${event.slugs.length} 个关联方向</small></button>`).join('');
}
function renderHistory(){
  const event=eventByKey[activeEvent]||events[0];
  if(!event)return;
  const related=event.slugs.map(slug=>recordBySlug[slug]).filter(Boolean);
  historyReader.innerHTML=`<div class="reader-kicker">CHAPTER ${esc(event.no)} / ${esc(event.period)}</div><h3>${esc(event.event)}</h3><div class="history-period">现代设计史横向事件 · ${related.length} 个关联方向</div><p class="history-lede">${esc(event.context)}</p><div class="history-section"><h4>历史背景</h4><p>${esc(event.background)}</p></div><div class="history-section"><h4>这场历史变化由谁参与</h4><div class="history-grid"><article class="history-card"><b>参与者与机构</b><p>${esc(event.actors)}</p></article><article class="history-card"><b>历史追问</b><p>${esc(event.question)}</p></article><article class="history-card wide"><b>关键转折</b>${bullets(event.turning_points)}</article></div></div><div class="history-section"><h4>它如何进入设计</h4><div class="history-grid"><article class="history-card"><b>传播路径</b><p>${esc(event.pathways)}</p></article><article class="history-card"><b>历史结果</b><p>${esc(event.outcomes)}</p></article></div></div><div class="history-section"><h4>留下的矛盾</h4><div class="history-grid"><article class="history-card"><b>历史反思</b><p>${esc(event.reflection)}</p></article><article class="history-card"><b>争议与未完成</b><p>${esc(event.debates)}</p></article></div></div><div class="history-section"><h4>关联设计方向</h4><p class="reader-copy">读完事件后，再选择一个方向继续。</p><div class="history-related">${related.map(record=>`<button type="button" data-direction-slug="${esc(record.slug)}">${esc(record.zh)} · ${esc(record.en)}</button>`).join('')}</div></div><details class="history-application"><summary>设计影响与教学补充（最后阅读）</summary><div class="history-application-grid"><article class="history-application-card"><b>对设计的影响</b>${bullets(event.impact)}</article><article class="history-application-card"><b>设计引导</b>${bullets(event.guide)}</article><article class="history-application-card"><b>如何教授设计</b><p>${esc(event.teach)}</p></article></div></details>`;
  renderHistoryNav();
}
function renderFilters(){
  const eventButtons=[`<button class="reader-filter active" type="button" data-reader-event="all">全部事件 <span>${records.length}</span></button>`,...events.map(event=>`<button class="reader-filter" type="button" data-reader-event="${esc(event.key)}">${esc(event.no)} ${esc(event.event)} <span>${records.filter(record=>record.events.includes(event.key)).length}</span></button>`)];
  const axisButtons=[`<button class="reader-filter active" type="button" data-reader-axis="all">全部视角 <span>${records.length}</span></button>`,...axes.map(axis=>`<button class="reader-filter" type="button" data-reader-axis="${esc(axis.key)}">${esc(axis.no)} ${esc(axis.title)} <span>${records.filter(record=>record.axes.includes(axis.key)).length}</span></button>`)];
  filters.innerHTML='<span class="filter-label">按历史事件</span>'+eventButtons.join('')+'<span class="filter-label">按课程视角</span>'+axisButtons.join('');
}
function syncFilters(){
  filters.querySelectorAll('[data-reader-event]').forEach(button=>button.classList.toggle('active',button.dataset.readerEvent===activeEventFilter));
  filters.querySelectorAll('[data-reader-axis]').forEach(button=>button.classList.toggle('active',button.dataset.readerAxis===activeAxisFilter));
  const parts=[];if(activeEventFilter!=='all')parts.push(eventLabel(activeEventFilter));if(activeAxisFilter!=='all')parts.push(axisLabel(activeAxisFilter));filterSummary.textContent=parts.length?`筛选：${parts.join(' · ')}`:'高级筛选（历史事件 / 课程视角）';
}
function matches(record,query){
  if(!query)return true;
  const eventText=record.events.flatMap(key=>{const event=eventByKey[key];return event?[event.event,event.context,event.background,event.question,event.reflection,event.actors,event.pathways,event.outcomes,event.debates,event.teach,...event.turning_points,...event.impact,...event.guide]:[]});
  const text=[record.zh,record.en,record.era,record.period,record.manifesto,record.prologue,record.history,record.origin,record.figures,record.diffusion,record.debate,record.legacy,record.bridge,record.frontend,record.feedback,...record.turns,...record.reps,...record.keywords,...record.axes.map(axisLabel),...eventText].join(' ').toLowerCase();
  return text.includes(query);
}
function visibleRecords(){
  const query=search.value.trim().toLowerCase();
  return records.filter(record=>(activeEventFilter==='all'||record.events.includes(activeEventFilter))&&(activeAxisFilter==='all'||record.axes.includes(activeAxisFilter))&&matches(record,query));
}
function renderDirectionIndex(){
  const visible=visibleRecords();
  count.textContent=`显示 ${visible.length} / ${records.length} 个方向`;
  directionIndex.innerHTML=visible.length?visible.map(record=>`<button type="button" class="${record.slug===activeSlug?'active':''}" data-direction-slug="${esc(record.slug)}"><span class="index-no">${esc(record.no)}</span><span><strong>${esc(record.zh)}</strong><small>${esc(record.era)} · ${esc(record.en)}</small></span></button>`).join(''):'<div class="index-empty">没有找到匹配方向。换一个关键词或清除筛选。</div>';
  const selected=visible.find(record=>record.slug===activeSlug)||visible[0];
  if(selected){activeSlug=selected.slug;renderDirectionReader(selected);const activeButton=directionIndex.querySelector('button.active');if(activeButton){directionIndex.scrollTop=Math.max(0,activeButton.offsetTop-(directionIndex.clientHeight-activeButton.offsetHeight)/2)}}else directionReader.innerHTML='<div class="index-empty">当前筛选没有可阅读的方向。</div>';
}
function renderDirectionReader(record){
  const historyCards=[['起源与语境',`<p>${esc(record.origin)}</p>`],['核心人物与机构',`<p>${esc(record.figures)}</p>`],['关键转折',bullets(record.turns)],['传播路径',`<p>${esc(record.diffusion)}</p>`],['批评与争议',`<p>${esc(record.debate)}</p>`],['当代影响',`<p>${esc(record.legacy)}</p>`]];
  const traits=record.traits?.length?record.traits.map(([name,desc])=>`<article class="reader-trait"><strong>${esc(name)}</strong><p>${esc(desc)}</p></article>`).join(''):'<p class="reader-copy">暂无整理的形式特征。</p>';
  directionReader.innerHTML=`<div class="reader-kicker">DIRECTION ${esc(record.no)} / ${esc(record.period)}</div><h3>${esc(record.zh)}</h3><div class="reader-en">${esc(record.en)} · ${esc(record.era)}</div><p class="reader-manifesto">“${esc(record.manifesto)}”</p><section class="reader-part"><div class="reader-part-head"><span>01</span><b>历史脉络</b><small>先理解它为什么出现</small></div><p class="reader-copy">${esc(record.prologue||record.history)}</p><p class="reader-copy">${esc(record.history)}</p><div class="reader-history-grid">${historyCards.map(([title,body],index)=>`<article class="reader-history-card${index===2?' wide':''}"><b>${esc(title)}</b>${body}</article>`).join('')}</div><div class="reader-sub">关键年代节点</div>${list(record.timeline)}</section><section class="reader-part"><div class="reader-part-head"><span>02</span><b>设计语言</b><small>它如何被看见和使用</small></div><div class="reader-traits">${traits}</div><div class="reader-sub">形式关键词</div><div class="reader-tags">${(record.keywords||[]).map(word=>`<span class="reader-tag">${esc(word)}</span>`).join('')}</div></section><section class="reader-part"><div class="reader-part-head"><span>03</span><b>代表案例</b><small>它如何传播和留下影响</small></div>${list(record.reps)}</section><section class="reader-part"><div class="reader-part-head"><span>04</span><b>影响与历史关联</b><small>回到历史路线继续读</small></div><div class="reader-event-tags">${record.events.map(key=>`<button type="button" data-history-event="${esc(key)}">${esc(eventLabel(key))}</button>`).join('')}</div></section><details class="reader-application"><summary>05 · 当代转译与教学补充（最后阅读）</summary><div class="reader-application-grid"><article class="reader-application-card"><b>当代 / 前端转译</b><p>${esc(record.frontend)}</p></article><article class="reader-application-card"><b>课内关系</b><p>${esc(record.bridge)}</p></article><article class="reader-application-card"><b>课程回写</b><p>${esc(record.feedback)}</p></article></div></details><details class="reader-more"><summary>06 · CSS 标本与代码指纹（最后阅读）</summary><p class="reader-copy">${esc(record.code)}</p><div class="reader-tags">${(record.specimens||[]).map(item=>`<span class="reader-tag">${esc(item)}</span>`).join('')}</div></details><a class="reader-open" href="halls/${encodeURIComponent(record.slug)}.html">进入 ${esc(record.zh)} 独立展厅 →</a>`;
}
function routeToDirection(slug){activeSlug=slug;setMode('directions');renderDirectionIndex();document.getElementById('directions').scrollIntoView({behavior:'smooth'});}


document.addEventListener('click',event=>{
  const trackButton=event.target.closest('[data-history-track-control]');
  if(trackButton){setHistoryTrack(trackButton.dataset.historyTrackControl);return;}
  const bookButton=event.target.closest('[data-book-chapter]');
  if(bookButton){activeChapter=bookButton.dataset.bookChapter;renderBookNav();renderBookReader();return;}
  const mode=event.target.closest('[data-mode]');
  if(mode){event.preventDefault();if(mode.dataset.mode==='history')setHistoryTrack('book');setMode(mode.dataset.mode);document.getElementById(mode.dataset.mode).scrollIntoView({behavior:'smooth'});return;}
  const historyButton=event.target.closest('[data-history-event]');
  if(historyButton){activeEvent=historyButton.dataset.historyEvent;setHistoryTrack('events');renderHistory();if(activeMode!=='history'){setMode('history');document.getElementById('history').scrollIntoView({behavior:'smooth'})}return;}
  const directionButton=event.target.closest('[data-direction-slug]');
  if(directionButton){routeToDirection(directionButton.dataset.directionSlug);return;}
  const eventButton=event.target.closest('[data-reader-event]');
  const axisButton=event.target.closest('[data-reader-axis]');
  if(eventButton){activeEventFilter=eventButton.dataset.readerEvent;syncFilters();renderDirectionIndex();return;}
  if(axisButton){activeAxisFilter=axisButton.dataset.readerAxis;syncFilters();renderDirectionIndex();return;}
});
search.addEventListener('input',renderDirectionIndex);
renderBookNav();renderBookReader();renderBookLenses();renderBookVolumes();renderBookArchives();renderBookSources();renderFilters();syncFilters();renderHistory();renderDirectionIndex();setHistoryTrack('book');setMode(location.hash.slice(1)==='directions'?'directions':'history',false);
</script>
</body>
</html>
'''


def render_knowledge():
    records = [_record(m) for m in ISMS]
    return (HTML.replace('@@CSS@@', CSS)
            .replace('@@EVENTS@@', _json_script(HISTORY_EVENTS))
            .replace('@@BOOK@@', _json_script({'chapters': BOOK_CHAPTERS, 'lenses': BOOK_LENSES, 'sources': BOOK_SOURCES, 'volumes': BOOK_VOLUMES, 'practiceFields': PRACTICE_FIELDS, 'globalRegions': GLOBAL_REGIONS, 'institutions': DESIGN_INSTITUTIONS, 'archives': CHAPTER_ARCHIVES}))
            .replace('@@AXES@@', _json_script(COURSE_AXES))
            .replace('@@RECORDS@@', _json_script(records)))

def build_knowledge(base):
    path = os.path.join(base, 'knowledge.html')
    with open(path, 'w', encoding='utf-8') as file:
        file.write(render_knowledge())
    print('generated design history route', len(ISMS), 'directions', len(BOOK_CHAPTERS), 'book chapters,', len(HISTORY_EVENTS), 'cross events')

if __name__ == '__main__':
    build_knowledge(os.path.dirname(os.path.abspath(__file__)))
