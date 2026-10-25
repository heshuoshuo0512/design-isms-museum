# -*- coding: utf-8 -*-
"""生成 halls/<slug>.html —— 每个主义一个独立展厅页,整页按该主义风格渲染。"""
import html as H, os
from data import ISMS
from history_data import ISM_HISTORY
from knowledge import build_knowledge

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'halls')
os.makedirs(OUT, exist_ok=True)

BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
.topbar{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;gap:14px;
 height:48px;padding:0 18px;font-size:12px;backdrop-filter:blur(10px)}
.topbar a{color:inherit;text-decoration:none;opacity:.75}
.topbar a:hover{opacity:1}
.topbar .tt{margin-right:auto;font-weight:700;letter-spacing:.08em}
.hero{min-height:72vh;display:flex;flex-direction:column;justify-content:center;padding:110px 8vw 60px;position:relative;overflow:hidden}
.hero .big{font-size:clamp(46px,10vw,120px);line-height:1;margin:6px 0 10px}
.hero .en{font-size:clamp(15px,2.4vw,26px);opacity:.65;letter-spacing:.08em}
.hero .man{font-size:clamp(17px,2.4vw,26px);margin-top:26px;max-width:720px;line-height:1.6}
.meta{margin-top:26px;display:flex;gap:10px;flex-wrap:wrap;font-size:12px}
.meta span{padding:5px 12px;border:1px solid currentColor;opacity:.85}
.art{position:absolute;inset:0;pointer-events:none}
.art>*{position:absolute}
@keyframes floaty{50%{transform:translateY(-18px) rotate(3deg)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes tw{50%{opacity:.45}}
.wrap{max-width:960px;margin:0 auto;padding:70px 6vw}
.sec{margin-bottom:64px}
.kicker{font-size:11px;letter-spacing:.35em;text-transform:uppercase;opacity:.55;margin-bottom:14px}
.sec h3{font-size:clamp(22px,3.4vw,34px);margin-bottom:18px}
.prose{line-height:2;font-size:16px;max-width:720px}
.chips{display:flex;flex-wrap:wrap;gap:10px;list-style:none}
.chips li{font-size:13px;padding:8px 16px}
.tl{list-style:none;position:relative;padding-left:26px}
.tl::before{content:"";position:absolute;left:6px;top:6px;bottom:6px;width:2px;background:currentColor;opacity:.25}
.tl li{position:relative;padding:10px 0 10px 12px}
.tl li::before{content:"";position:absolute;left:-24px;top:18px;width:10px;height:10px;border-radius:50%;background:currentColor}
.tl b{display:block;font-size:18px}
.tl span{opacity:.75;font-size:14px}
pre{overflow-x:auto;padding:22px;font-size:14px;line-height:1.7;margin-top:6px}
.hallnav{display:flex;justify-content:space-between;gap:12px;padding:26px 6vw;font-size:14px}
.hallnav a{color:inherit;text-decoration:none;border:1px solid currentColor;padding:10px 20px;opacity:.85}
.hallnav a:hover{opacity:1}
footer{text-align:center;padding:40px 6vw 60px;font-size:12px;opacity:.5;line-height:2}
.rv{opacity:0;transform:translateY(28px);transition:opacity .7s ease,transform .7s ease}
.rv.in{opacity:1;transform:none}
.lede{font-size:clamp(18px,2.4vw,24px);line-height:2;font-weight:300;padding:0 0 24px;letter-spacing:.02em;border-bottom:1px solid currentColor;margin-bottom:44px}
.hint{font-size:13px;opacity:.55;margin:-8px 0 22px}

/* ---- 标本陈列系统 ---- */
.exgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:26px;margin:14px 0 0;perspective:1200px}
.ex{position:relative;padding:0;display:flex;flex-direction:column;overflow:hidden;
    border:1px solid currentColor;border-radius:14px;background:rgba(128,128,128,.03);
    transition:transform .5s cubic-bezier(.22,1,.36,1),box-shadow .5s cubic-bezier(.22,1,.36,1);
    transform-style:preserve-3d;will-change:transform}
.ex:hover{transform:translateY(-10px) scale(1.03);box-shadow:0 24px 60px rgba(0,0,0,.22),0 0 0 1px currentColor;z-index:2}
.ex-art{display:flex;align-items:center;justify-content:center;min-height:150px;width:100%;
        padding:28px 22px;position:relative;overflow:hidden}
.ex-art::before{content:"";position:absolute;inset:0;opacity:.04;pointer-events:none;
        background-image:radial-gradient(circle,currentColor 1px,transparent 1.4px);background-size:18px 18px;
        transition:opacity .3s}
.ex:hover .ex-art::before{opacity:.1}
.ex .xob{position:relative;z-index:1;transition:transform .4s cubic-bezier(.34,1.56,.64,1)}
.ex:hover .xob{transform:scale(1.15) rotate(-2deg);animation-play-state:paused}
.ex-cap{padding:14px 18px 16px;border-top:1px solid currentColor;font-size:12.5px;opacity:.78;line-height:1.65;
        display:flex;align-items:flex-start;gap:10px;transition:opacity .3s}
.ex:hover .ex-cap{opacity:1}
.ex-cap::before{content:"◈";flex-shrink:0;opacity:.5;font-size:13px;line-height:1.6;transition:transform .3s}
.ex:hover .ex-cap::before{transform:rotate(90deg);opacity:1}

/* ---- 标本入场编排 ---- */
.exgrid .ex{opacity:0;transform:translateY(30px) rotateX(8deg) scale(.96);
  transition:opacity .65s ease,transform .65s cubic-bezier(.22,1,.36,1)}
.exgrid .ex.in{opacity:1;transform:none}
.exgrid .ex:nth-child(2){transition-delay:.09s}
.exgrid .ex:nth-child(3){transition-delay:.18s}

/* ---- 悬停揭示代码 ---- */
.ex .ex-code{position:absolute;inset:auto 0 0 0;padding:12px 16px;font-family:ui-monospace,monospace;
  font-size:10.5px;line-height:1.5;background:rgba(0,0,0,.85);color:#7df9ff;
  transform:translateY(102%);transition:transform .38s cubic-bezier(.22,1,.36,1);
  max-height:55%;overflow:auto;white-space:pre-wrap;word-break:break-all;z-index:3;pointer-events:none;
  border-top:1px solid rgba(125,249,255,.3)}
.ex:hover .ex-code{transform:translateY(0)}

/* 触屏 / 窄屏适配(无精确指针即视为触屏) */
@media(pointer:coarse),(not(pointer:fine)){
  /* 自定义光标仅桌面(pointer:fine);触屏禁用其专用样式 */
  .cur-p,.cur-ripple{display:none!important}
}
@media(max-width:720px){
  .topbar{height:auto;min-height:44px;gap:8px;padding:8px 12px;font-size:11px;flex-wrap:wrap}
  .hero{padding:92px 6vw 44px;min-height:60vh}
  .wrap{padding:52px 5vw}
  .sec{margin-bottom:48px}
  pre{font-size:12px;padding:14px;-webkit-overflow-scrolling:touch}
  .exgrid{grid-template-columns:1fr;gap:18px}
  .ex-art{min-height:120px;padding:20px 16px}
  .ex:hover{transform:none;box-shadow:0 12px 30px rgba(0,0,0,.18)}
  .ex:hover .xob{transform:none}
  .ex:hover .ex-art::before{opacity:.04}
  .ex-cap::before{transform:none}
  /* 触屏点按揭示代码面板(1s 悬停模拟);JS 点击切换同样支持 */
  .ex:active .ex-code,.ex.code-revealed .ex-code{transform:translateY(0)}
  .ex:active .xob,.ex.code-revealed .xob{animation-play-state:paused}
  .hallnav{flex-wrap:wrap;padding:20px 5vw;font-size:12px;gap:10px}
  .hallnav a{padding:10px 14px;min-height:44px;display:inline-flex;align-items:center}
  .chips li{padding:10px 14px}
  .lede{margin-bottom:32px}
  footer{padding:32px 5vw 48px}
}
/* 尊重系统减少动态偏好 */
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.001s!important;animation-iteration-count:1!important;transition-duration:.001s!important}
  .rv,.exgrid .ex{opacity:1!important;transform:none!important}
}

/* ---- 全局自定义光标 ---- */
@media(pointer:fine){
  *{cursor:none!important}
  #cur-dot{position:fixed;z-index:9999;width:6px;height:6px;border-radius:50%;background:#FFD23F;pointer-events:none;transform:translate(-50%,-50%);transition:width .2s,height .2s,background .2s;mix-blend-mode:difference}
  #cur-ring{position:fixed;z-index:9998;width:32px;height:32px;border-radius:50%;border:1.5px solid rgba(255,210,63,.75);pointer-events:none;transform:translate(-50%,-50%);transition:width .25s,height .25s,border-color .25s;mix-blend-mode:difference}
  body.cur-hover #cur-dot{width:14px;height:14px;background:#fff}
  body.cur-hover #cur-ring{width:56px;height:56px;border-color:rgba(255,255,255,.9);animation:cur-spin 3s linear infinite}
  body.cur-down #cur-ring{width:20px;height:20px}
  @keyframes cur-spin{to{transform:translate(-50%,-50%) rotate(360deg)}}
  .cur-p{position:fixed;z-index:9997;border-radius:50%;pointer-events:none;mix-blend-mode:screen}
  .cur-ripple{position:fixed;z-index:9996;border:2px solid #FFD23F;border-radius:50%;pointer-events:none;animation:rip .5s ease-out forwards}
  @keyframes rip{from{width:10px;height:10px;opacity:1}to{width:70px;height:70px;opacity:0}}
}
/* 粒子与涟漪在所有设备生效(JS 控制创建) */
.cur-p{position:fixed;z-index:9997;border-radius:50%;pointer-events:none;mix-blend-mode:screen}
.cur-ripple{position:fixed;z-index:9996;border:2px solid #FFD23F;border-radius:50%;pointer-events:none;animation:rip .5s ease-out forwards}
@keyframes rip{from{width:10px;height:10px;opacity:1}to{width:70px;height:70px;opacity:0}}.history-deep-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:18px}.history-deep-card{padding:15px;border:1px solid rgba(255,255,255,.16);background:rgba(0,0,0,.12)}.history-deep-card h4{margin-bottom:8px;font-size:12px;letter-spacing:.08em}.history-deep-card p,.history-deep-card li{font-size:12px;line-height:1.9;opacity:.78}.history-deep-card ul{padding-left:18px}.history-deep-card li+li{margin-top:5px}@media(max-width:720px){.history-deep-grid{grid-template-columns:1fr}}"""

# 每厅专属主题 css —— key: css 片段(选择器相对 body)
THEME_CSS = {
'neubrutalism': """
body{background:#FFD23F;color:#000;font-family:"Arial Black","Helvetica Neue",sans-serif}
::selection{background:#FF6B6B;color:#000}
.topbar{background:rgba(255,210,63,.9);border-bottom:4px solid #000}
.hero .big{text-transform:uppercase;font-weight:900;text-shadow:5px 5px 0 #FF6B6B}
.hero .man{background:#fff;border:4px solid #000;box-shadow:8px 8px 0 #000;padding:18px 22px;font-weight:700}
.meta span{border:3px solid #000;border-radius:0;font-weight:700;background:#fff;box-shadow:4px 4px 0 #000}
.a1{width:150px;height:150px;background:#FF6B6B;border:4px solid #000;box-shadow:10px 10px 0 #000;top:12%;right:8%;transform:rotate(9deg);animation:floaty 5s ease-in-out infinite}
.a2{width:90px;height:90px;background:#74B9FF;border:4px solid #000;box-shadow:8px 8px 0 #000;border-radius:50%;bottom:14%;right:20%;animation:floaty 6s 1s ease-in-out infinite}
.sec h3{font-weight:900;text-transform:uppercase}
.prose{background:#fff;border:4px solid #000;box-shadow:10px 10px 0 #000;padding:26px}
.chips li{border:3px solid #000;border-radius:0;background:#74B9FF;font-weight:700;box-shadow:4px 4px 0 #000}
pre{background:#000;color:#FFD23F;border:4px solid #000;box-shadow:10px 10px 0 #FF6B6B}
.hallnav a{border:3px solid #000;background:#fff;font-weight:700;box-shadow:5px 5px 0 #000}
""",
'minimalism': """
body{background:#fff;color:#111;font-family:"Helvetica Neue","PingFang SC",sans-serif}
::selection{background:#111;color:#fff}
.topbar{background:rgba(255,255,255,.9);border-bottom:1px solid #eee}
.hero .big{font-weight:200;letter-spacing:-.02em}
.hero .en{font-weight:300}
.hero .man{font-weight:300;color:#666}
.meta span{border-color:#ddd;border-radius:0;color:#888}
.a1{width:60px;height:2px;background:#111;top:50%;left:50%;transform:translateX(-50%);animation:breathe 6s ease-in-out infinite}
@keyframes breathe{50%{transform:translateX(-50%) scaleX(1.6);opacity:.4}}
.sec h3{font-weight:300}
.kicker{letter-spacing:.5em}
.chips li{border:1px solid #e5e5e5;color:#777}
pre{background:#fafafa;color:#555;border-left:2px solid #111}
.tl b{font-weight:400}
.hallnav a{border-color:#111}
""",
'swiss': """
body{background:#E30613;color:#fff;font-family:Helvetica,Arial,sans-serif}
::selection{background:#fff;color:#E30613}
.topbar{background:rgba(227,6,19,.92);border-bottom:2px solid #fff}
.hero{background:repeating-linear-gradient(0deg,rgba(255,255,255,.05) 0 1px,transparent 1px 110px),repeating-linear-gradient(90deg,rgba(255,255,255,.05) 0 1px,transparent 1px 110px)}
.hero .big{font-weight:700;text-transform:uppercase;letter-spacing:-.02em}
.a1{width:200px;height:200px;border-radius:50%;background:#fff;mix-blend-mode:exclusion;top:12%;right:10%;animation:floaty 7s ease-in-out infinite}
.a2{width:110px;height:110px;background:#fff;mix-blend-mode:exclusion;bottom:16%;right:26%;animation:floaty 9s 1s ease-in-out infinite}
.meta span{border-radius:0;border-width:2px}
.sec h3{font-weight:700;text-transform:uppercase;letter-spacing:-.01em}
.chips li{border:2px solid rgba(255,255,255,.6)}
pre{background:#fff;color:#E30613;font-weight:700}
.hallnav a{border-width:2px}
""",
'glassmorphism': """
body{background:linear-gradient(135deg,#667eea,#764ba2,#f093fb,#4facfe);background-size:300% 300%;animation:bgpan 16s ease infinite;color:#fff;font-family:"Helvetica Neue","PingFang SC",sans-serif}
@keyframes bgpan{50%{background-position:100% 50%}}
::selection{background:#fff;color:#764ba2}
.topbar{background:rgba(255,255,255,.12);border-bottom:1px solid rgba(255,255,255,.3);backdrop-filter:blur(16px)}
.hero .big{font-weight:800}
.a1{width:280px;height:280px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#f0f,#70f);top:8%;left:4%;animation:floaty 9s ease-in-out infinite;filter:blur(2px)}
.a2{width:200px;height:200px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#0ff,#04f);bottom:6%;right:6%;animation:floaty 11s ease-in-out infinite reverse;filter:blur(2px)}
.hero .man{background:rgba(255,255,255,.15);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.35);border-radius:20px;padding:18px 24px}
.meta span{border-color:rgba(255,255,255,.5);border-radius:99px;background:rgba(255,255,255,.12);backdrop-filter:blur(8px)}
.prose,.sec h3{border-radius:20px}
.prose{background:rgba(255,255,255,.13);backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.3);padding:28px;border-radius:20px;box-shadow:0 16px 40px rgba(0,0,0,.2)}
.chips li{background:rgba(255,255,255,.16);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.35);border-radius:99px}
pre{background:rgba(0,0,0,.35);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.3);border-radius:16px;color:#d9f7ff}
.hallnav a{border-color:rgba(255,255,255,.5);border-radius:99px;background:rgba(255,255,255,.1);backdrop-filter:blur(8px)}
""",
'neumorphism': """
body{background:#E0E5EC;color:#5a6a7e;font-family:"Helvetica Neue","PingFang SC",sans-serif}
::selection{background:#5a6a7e;color:#E0E5EC}
.topbar{background:rgba(224,229,236,.9);box-shadow:0 6px 14px #c3c9d1}
.hero .big{font-weight:700;color:#4a5a6e}
.hero .man,.prose,.chips li,pre{background:#E0E5EC}
.hero .man{border-radius:24px;padding:20px 26px;box-shadow:10px 10px 22px #b8bec7,-10px -10px 22px #fff}
.meta span{border:none;border-radius:99px;box-shadow:inset 4px 4px 8px #b8bec7,inset -4px -4px 8px #fff;padding:8px 16px}
.a1{width:170px;height:170px;border-radius:50%;top:14%;right:10%;background:#E0E5EC;box-shadow:12px 12px 26px #b8bec7,-12px -12px 26px #fff,inset 0 0 0 16px #E0E5EC,inset 5px 5px 10px #b8bec7;animation:floaty 8s ease-in-out infinite}
.a2{width:110px;height:60px;border-radius:99px;bottom:16%;right:26%;background:#E0E5EC;box-shadow:8px 8px 18px #b8bec7,-8px -8px 18px #fff;animation:floaty 7s 1s ease-in-out infinite}
.prose{border-radius:28px;padding:30px;box-shadow:12px 12px 26px #b8bec7,-12px -12px 26px #fff}
.chips li{border-radius:16px;box-shadow:6px 6px 12px #b8bec7,-6px -6px 12px #fff;padding:10px 18px}
pre{border-radius:20px;color:#4a5a6e;box-shadow:inset 8px 8px 16px #b8bec7,inset -8px -8px 16px #fff}
.hallnav a{border:none;border-radius:16px;box-shadow:6px 6px 12px #b8bec7,-6px -6px 12px #fff}
""",
'claymorphism': """
body{background:#F6E9F8;color:#6b5570;font-family:"Helvetica Neue","PingFang SC",sans-serif}
::selection{background:#B06AC0;color:#fff}
.topbar{background:rgba(246,233,248,.92);box-shadow:0 8px 20px rgba(180,130,210,.25)}
.hero .big{font-weight:800;color:#8a4a9a}
.hero .man{background:#fff;border-radius:32px;padding:20px 26px;box-shadow:inset -6px -6px 14px rgba(196,150,220,.3),inset 6px 6px 14px #fff,0 18px 36px rgba(180,130,210,.3)}
.meta span{border:none;border-radius:99px;background:#FFE0F0;color:#a0508a;font-weight:600;box-shadow:inset -3px -3px 8px rgba(230,150,200,.4),inset 3px 3px 8px #fff,0 6px 12px rgba(220,140,190,.25);padding:8px 16px}
.a1{width:180px;height:180px;border-radius:38% 62% 55% 45%/48% 42% 58% 52%;background:#C7E9FF;top:12%;right:9%;box-shadow:inset -10px -10px 22px rgba(90,160,220,.4),inset 10px 10px 22px #fff,0 20px 40px rgba(100,170,230,.35);animation:floaty 6s ease-in-out infinite}
.a2{width:100px;height:100px;border-radius:50%;background:#FFF3C7;bottom:14%;right:26%;box-shadow:inset -8px -8px 16px rgba(230,190,80,.4),inset 8px 8px 16px #fff,0 14px 28px rgba(230,190,80,.35);animation:floaty 7s 1.2s ease-in-out infinite}
.prose{background:#fff;border-radius:36px;padding:32px;box-shadow:inset -8px -8px 18px rgba(196,150,220,.25),inset 8px 8px 18px #fff,0 22px 44px rgba(180,130,210,.3)}
.chips li{border-radius:26px;background:#E4F3FF;color:#3a7ab0;font-weight:600;box-shadow:inset -4px -4px 10px rgba(120,180,230,.35),inset 4px 4px 10px #fff,0 8px 16px rgba(120,180,230,.25);padding:12px 20px}
pre{background:#fff;border-radius:28px;color:#6b5570;box-shadow:inset -6px -6px 14px rgba(196,150,220,.25),inset 6px 6px 14px #fff,0 16px 32px rgba(180,130,210,.25)}
.hallnav a{border:none;border-radius:26px;background:#FFE0F0;color:#a0508a;font-weight:600;box-shadow:inset -3px -3px 8px rgba(230,150,200,.4),inset 3px 3px 8px #fff,0 8px 16px rgba(220,140,190,.3)}
""",
'brutalism': """
body{background:#fff;color:#000;font-family:"Times New Roman",Times,serif}
::selection{background:#00e;color:#ff0}
.topbar{background:#c0c0c0;border-bottom:2px outset #fff;font-family:monospace;backdrop-filter:none}
.topbar a{color:#00e;text-decoration:underline}
.hero{min-height:60vh}
.hero .big{text-decoration:underline;font-family:"Times New Roman",serif}
.hero .en{color:#00e}
.hero .man{font-size:18px;color:#000}
.meta span{border:2px outset #ccc;background:#c0c0c0;color:#000;font-family:monospace;border-radius:0}
.a1{display:none}
.sec h3{text-decoration:underline}
.prose{border:2px inset #ccc;background:#fff;padding:24px;font-size:16px}
.chips li{border:2px inset #ccc;background:#eee;font-family:monospace;color:#000}
.tl{font-family:monospace}
pre{background:#000;color:#0f0;font-family:monospace;border:2px solid #000}
.hallnav{border-top:2px solid #000}
.hallnav a{border:2px outset #ccc;background:#c0c0c0;color:#000;font-family:monospace}
.rv{opacity:1;transform:none}
""",
'y2k': """
body{background:linear-gradient(180deg,#0a0a2e,#1a0a3e 60%,#3e0a5e);color:#fff;font-family:Verdana,"PingFang SC",sans-serif}
::selection{background:#ff71ce;color:#000}
.topbar{background:rgba(26,10,62,.85);border-bottom:2px solid;border-image:linear-gradient(90deg,#7df9ff,#ff71ce,#fffb96) 1}
.hero .stars{position:absolute;inset:0;background-image:radial-gradient(1px 1px at 20% 30%,#fff,transparent),radial-gradient(1px 1px at 40% 70%,#fff,transparent),radial-gradient(2px 2px at 60% 20%,#fff,transparent),radial-gradient(1px 1px at 80% 50%,#fff,transparent),radial-gradient(2px 2px at 90% 80%,#fff,transparent),radial-gradient(1px 1px at 10% 85%,#fff,transparent);animation:tw 3s ease-in-out infinite}
.hero .big{font-family:"Arial Black",Arial,sans-serif;font-style:italic;background:linear-gradient(180deg,#fff 20%,#7df9ff 45%,#b967ff 60%,#ff71ce);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 3px 0 rgba(255,113,206,.5))}
.hero .en{color:#7df9ff;font-style:italic;letter-spacing:.2em}
.hero .man{background:linear-gradient(160deg,rgba(160,230,255,.22),rgba(255,120,220,.16));border:2px solid;border-image:linear-gradient(135deg,#7df9ff,#ff71ce) 1;border-radius:4px 20px 4px 20px;padding:18px 24px;backdrop-filter:blur(6px)}
.meta span{border-color:#7df9ff;color:#7df9ff;border-radius:0}
.a1{width:160px;height:160px;border-radius:50%;background:radial-gradient(circle at 32% 28%,#fff 0%,#7df9ff 25%,#b967ff 60%,#2a0a4e 100%);box-shadow:0 0 60px rgba(185,103,255,.7);top:12%;right:10%;animation:floaty 5s ease-in-out infinite}
.a2{width:80px;height:80px;background:linear-gradient(135deg,#fffb96,#ff71ce);clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);bottom:16%;right:26%;animation:spin 8s linear infinite}
.prose{background:rgba(125,249,255,.08);border:1px solid rgba(125,249,255,.4);border-radius:4px 20px 4px 20px;padding:28px;color:#d9f7ff;backdrop-filter:blur(4px)}
.chips li{border:1px solid rgba(125,249,255,.5);color:#d9f7ff;background:rgba(125,249,255,.08)}
pre{background:rgba(0,0,0,.5);border:1px solid #7df9ff;color:#7df9ff}
.hallnav a{border-color:#ff71ce;color:#ff71ce}
""",
'cyberpunk': """
body{background:#050508;color:#0ff;font-family:"Courier New",monospace}
::selection{background:#f0f;color:#000}
body::after{content:"";position:fixed;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.35) 0 2px,transparent 2px 4px);pointer-events:none;z-index:60}
.topbar{background:rgba(5,5,8,.9);border-bottom:1px solid #0ff;color:#0ff}
.hero{background:linear-gradient(rgba(0,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,0,255,.06) 1px,transparent 1px);background-size:44px 44px}
.hero .big{color:#fff;text-transform:uppercase;text-shadow:3px 0 #f0f,-3px 0 #0ff;animation:glitch 3s infinite}
@keyframes glitch{0%,91%,100%{transform:none}92%{transform:translate(2px,-2px)}94%{transform:translate(-3px,1px)}96%{transform:none}}
.hero .en{color:#f0f}
.hero .man{border:1px solid #0ff;padding:18px 24px;color:#b0e0e0;background:rgba(0,255,255,.05);clip-path:polygon(14px 0,100% 0,100% calc(100% - 14px),calc(100% - 14px) 100%,0 100%,0 14px)}
.meta span{border:1px solid #f0f;color:#f0f;border-radius:0}
.a1{width:190px;height:190px;border:1px solid #0ff;border-radius:50%;top:14%;right:9%;animation:spin 14s linear infinite;opacity:.6}
.a1::before{content:"";position:absolute;inset:22px;border:1px dashed #f0f;border-radius:50%}
.a2{width:120px;height:8px;background:#f0f;bottom:20%;right:24%;clip-path:polygon(0 0,100% 0,calc(100% - 8px) 100%,8px 100%);animation:floaty 3s ease-in-out infinite}
.prose{border-left:3px solid #f0f;padding:24px;color:#b0e0e0;background:rgba(255,0,255,.04)}
.chips li{border:1px solid #0ff;background:rgba(0,255,255,.07);color:#0ff;clip-path:polygon(6px 0,100% 0,100% 100%,0 100%,0 6px)}
.tl b{color:#f0f}
pre{background:#000;border:1px solid #0ff;color:#0f0}
.hallnav a{border:1px solid #0ff;color:#0ff;clip-path:polygon(8px 0,100% 0,100% 100%,0 100%,0 8px)}
""",
'darkmode': """
body{background:#121212;color:#e6e6e6;font-family:-apple-system,"Helvetica Neue","PingFang SC",sans-serif}
::selection{background:#8ab4f8;color:#121212}
.topbar{background:rgba(18,18,18,.92);border-bottom:1px solid #2c2c2c}
.hero .big{font-weight:700}
.hero .en{color:#8ab4f8}
.hero .man{color:#b8b8b8;background:#1e1e1e;border:1px solid #2c2c2c;border-radius:16px;padding:20px 26px}
.meta span{border:1px solid #3a3a3a;color:#8ab4f8;border-radius:99px;background:#1e1e1e}
.a1{width:130px;height:130px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#3a3a3a,#1a1a1a);box-shadow:0 0 80px rgba(138,180,248,.25),inset -14px -10px 0 rgba(138,180,248,.12);top:16%;right:12%;animation:floaty 9s ease-in-out infinite}
.a2{width:8px;height:8px;border-radius:50%;background:#8ab4f8;box-shadow:0 0 24px 6px rgba(138,180,248,.5);bottom:22%;right:30%;animation:tw 2.4s ease-in-out infinite}
.prose{background:#1e1e1e;border:1px solid #2c2c2c;border-radius:16px;padding:30px;color:#c8c8c8}
.chips li{background:#2a2a2a;border:1px solid #3a3a3a;color:#cfcfcf;border-radius:10px}
.kicker{color:#8ab4f8;opacity:.8}
pre{background:#0d0d0d;border:1px solid #2c2c2c;border-radius:12px;color:#a5d6a7}
.hallnav a{border-color:#3a3a3a;border-radius:10px;background:#1e1e1e}
""",
'maximalism': """
body{background:repeating-linear-gradient(45deg,#FF2D78 0 60px,#FFE600 60px 120px,#00C2FF 120px 180px,#7B2FFF 180px 240px);color:#111;font-family:"Arial Black","PingFang SC",sans-serif}
::selection{background:#7B2FFF;color:#FFE600}
.topbar{background:#111;color:#FFE600;border-bottom:6px solid #FF2D78}
.topbar a{color:#FFE600}
.hero .big{color:#fff;text-transform:uppercase;font-style:italic;text-shadow:4px 4px 0 #FF2D78,8px 8px 0 #00C2FF,12px 12px 0 #111;transform:rotate(-1.5deg)}
.hero .en{color:#FFE600;font-weight:800;text-shadow:2px 2px 0 #111}
.hero .man{background:#fff;border:5px dashed #FF2D78;outline:5px dotted #00C2FF;outline-offset:6px;padding:20px 26px;font-weight:800;transform:rotate(1deg);box-shadow:10px 10px 0 #7B2FFF}
.meta span{border:3px solid #111;border-radius:99px;background:#FFE600;font-weight:800;transform:rotate(-2deg)}
.meta span:nth-child(even){background:#00C2FF;color:#fff;transform:rotate(2deg)}
.a1{width:140px;height:140px;background:#fff;border:5px solid #111;border-radius:50%;top:12%;right:8%;animation:spin 9s linear infinite}
.a1::before{content:"★";position:absolute;inset:0;display:grid;place-items:center;font-size:70px;color:#FF2D78}
.a2{width:90px;height:90px;background:#7B2FFF;border:4px dashed #FFE600;bottom:14%;right:24%;transform:rotate(14deg);animation:floaty 4s ease-in-out infinite}
.prose{background:#fff;border:5px solid #111;padding:30px;box-shadow:12px 12px 0 #FF2D78;transform:rotate(-.8deg);font-weight:600}
.chips li{border:3px solid #111;border-radius:99px;background:#FFE600;font-weight:800;transform:rotate(-1.5deg);box-shadow:4px 4px 0 #111}
.chips li:nth-child(2n){background:#00C2FF;color:#fff;transform:rotate(1.5deg)}
.chips li:nth-child(3n){background:#FF2D78;color:#fff}
pre{background:#111;color:#FFE600;border:5px dashed #00C2FF;transform:rotate(.6deg)}
.hallnav a{border:4px solid #111;background:#FFE600;color:#111;font-weight:800;box-shadow:6px 6px 0 #111}
""",
'flatdesign': """
body{background:#1ABC9C;color:#fff;font-family:"Segoe UI","Helvetica Neue","PingFang SC",sans-serif}
::selection{background:#E74C3C;color:#fff}
.topbar{background:#16A085;border-bottom:none;backdrop-filter:none}
.hero .big{font-weight:800}
.meta span{border:none;background:#16A085;border-radius:2px;font-weight:600}
.a1{width:130px;height:130px;background:#E74C3C;top:12%;right:10%;transform:rotate(12deg);animation:floaty 6s ease-in-out infinite}
.a2{width:70px;height:70px;background:#F39C12;border-radius:50%;top:38%;right:24%;animation:floaty 5s 1s ease-in-out infinite}
.a3{width:150px;height:56px;background:#3498DB;bottom:14%;right:12%;transform:rotate(-6deg);animation:floaty 7s .5s ease-in-out infinite}
.prose{background:#16A085;padding:30px;border-radius:2px}
.chips li{border-radius:2px;font-weight:600;padding:10px 18px}
.chips li:nth-child(1){background:#E74C3C}.chips li:nth-child(2){background:#3498DB}
.chips li:nth-child(3){background:#F39C12;color:#333}.chips li:nth-child(4){background:#9B59B6}
.chips li:nth-child(5){background:#2C3E50}
pre{background:#2C3E50;color:#1ABC9C;border-radius:2px}
.tl b{color:#FFE28A}
.hallnav a{border:none;background:#E74C3C;border-radius:2px;font-weight:600}
.hallnav a:last-child{background:#3498DB}
""",
'skeuomorphism': """
body{background:linear-gradient(180deg,#3a2a1a,#241a10);color:#f0e6d2;font-family:Georgia,"Songti SC",serif}
::selection{background:#c4956a;color:#241a10}
.topbar{background:linear-gradient(180deg,#4a3826,#33261a);border-bottom:1px solid #1a1208;box-shadow:0 2px 8px rgba(0,0,0,.6);color:#d8c8a8}
.hero .big{font-family:Georgia,serif;text-shadow:0 2px 4px rgba(0,0,0,.6)}
.hero .en{color:#c4956a}
.hero .man{background:repeating-linear-gradient(0deg,#f4ecd8 0 30px,#e8dcc0 30px 31px);color:#4a3826;border-radius:8px;padding:22px 28px;box-shadow:0 14px 36px rgba(0,0,0,.6),inset 0 0 30px rgba(120,90,50,.25);border:2px dashed rgba(90,60,30,.4)}
.meta span{border:1px solid #611;border-radius:6px;background:linear-gradient(180deg,#d44,#a22);color:#fff;text-shadow:0 -1px 0 rgba(0,0,0,.4);box-shadow:0 2px 4px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.4)}
.a1{width:92px;height:92px;border-radius:50%;background:conic-gradient(#ddd,#999,#eee,#888,#ddd);box-shadow:0 8px 20px rgba(0,0,0,.6),inset 0 2px 3px #fff;top:14%;right:12%;animation:spin 20s linear infinite}
.a2{width:160px;height:100px;background:repeating-linear-gradient(90deg,#8a6a45 0 12px,#6b4f30 12px 24px);border-radius:6px;box-shadow:0 10px 24px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.2);bottom:14%;right:24%}
.prose{background:repeating-linear-gradient(0deg,#f4ecd8 0 30px,#e8dcc0 30px 31px);color:#4a3826;border-radius:8px;padding:34px;box-shadow:0 18px 44px rgba(0,0,0,.65),inset 0 0 40px rgba(120,90,50,.3);border:2px dashed rgba(90,60,30,.4)}
.prose a{color:#5a7ab0}
.chips li{background:linear-gradient(180deg,#fff,#ddd);border:1px solid #a89070;border-radius:20px;color:#5a4530;font-weight:600;box-shadow:0 2px 4px rgba(0,0,0,.3),inset 0 1px 0 #fff;padding:10px 20px;text-shadow:0 1px 0 #fff}
.tl b{color:#e8c890}
pre{background:#1a1208;border:1px solid #4a3826;color:#d8b878;border-radius:6px;box-shadow:inset 0 2px 12px rgba(0,0,0,.8)}
.hallnav a{border:1px solid #6b4f30;border-radius:8px;background:linear-gradient(180deg,#8a6a45,#6b4f30);color:#f0e6d2;box-shadow:0 4px 10px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.25);text-shadow:0 -1px 0 rgba(0,0,0,.4)}
""",
'retrofuturism': """
body{background:linear-gradient(180deg,#0b2b3a 0%,#134a5e 55%,#ff7e5f 85%,#feb47b 100%);color:#fff;font-family:Futura,"Century Gothic","PingFang SC",sans-serif}
::selection{background:#ff7e5f;color:#0b2b3a}
.topbar{background:rgba(11,43,58,.9);border-bottom:3px solid rgba(255,255,255,.6)}
.hero .big{font-weight:300;font-style:italic;letter-spacing:.14em;text-transform:uppercase;text-shadow:0 4px 20px rgba(0,0,0,.5)}
.hero .en{letter-spacing:.3em;font-style:italic;color:#ffd93b}
.a1{width:260px;height:260px;border-radius:50%;background:linear-gradient(180deg,#ffd93b,#ff7e5f);box-shadow:0 0 90px rgba(255,126,95,.7);top:8%;left:50%;transform:translateX(-50%);-webkit-mask:repeating-linear-gradient(0deg,#000 0 20px,transparent 20px 26px);mask:repeating-linear-gradient(0deg,#000 0 20px,transparent 20px 26px)}
.a2{width:400px;height:86px;border:8px solid rgba(255,255,255,.85);border-radius:50%;top:calc(8% + 88px);left:50%;transform:translateX(-50%) rotateX(72deg);box-shadow:0 0 30px rgba(255,255,255,.5)}
.hero .man{margin-top:170px;text-shadow:0 2px 10px rgba(0,0,0,.5);font-style:italic}
.meta span{border-radius:99px;border-width:2px;background:rgba(11,43,58,.55);backdrop-filter:blur(4px)}
.sec h3{font-weight:300;font-style:italic;letter-spacing:.12em;text-transform:uppercase}
.prose{background:rgba(11,43,58,.6);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.35);border-radius:99px 24px 24px 99px;padding:30px 40px}
.chips li{border-radius:99px;background:rgba(11,43,58,.55);border:1px solid rgba(255,255,255,.4);backdrop-filter:blur(4px)}
.tl b{color:#ffd93b}
pre{background:rgba(11,43,58,.75);border:2px solid rgba(255,255,255,.5);border-radius:16px;color:#ffd93b}
.hallnav a{border-radius:99px;border-width:2px;background:rgba(11,43,58,.55)}
""",
'bentogrid': """
body{background:#F5F5F7;color:#1d1d1f;font-family:-apple-system,"Helvetica Neue","PingFang SC",sans-serif}
::selection{background:#0071E3;color:#fff}
.topbar{background:rgba(245,245,247,.85);border-bottom:1px solid #e2e2e6}
.hero .big{font-weight:800;letter-spacing:-.03em}
.hero .man{background:#fff;border-radius:24px;padding:22px 28px;box-shadow:0 8px 24px rgba(0,0,0,.06);font-size:clamp(17px,2.2vw,24px)}
.meta span{border:none;border-radius:99px;background:#0071E3;color:#fff;font-weight:600}
.a1{width:180px;height:180px;border-radius:32px;background:linear-gradient(135deg,#FF9A8B,#FF6A88);top:10%;right:8%;animation:floaty 6s ease-in-out infinite}
.a2{width:110px;height:110px;border-radius:28px;background:#BFE3FF;bottom:12%;right:24%;animation:floaty 7s 1s ease-in-out infinite}
.prose{background:#fff;border-radius:24px;padding:32px;box-shadow:0 8px 24px rgba(0,0,0,.06)}
.chips li{border-radius:18px;font-weight:600;padding:12px 20px}
.chips li:nth-child(1){background:#BFE3FF;color:#0a4a8a}.chips li:nth-child(2){background:#D9F7C4;color:#2a6a10}
.chips li:nth-child(3){background:#FFE3B3;color:#8a5200}.chips li:nth-child(4){background:#F3D1FF;color:#6a1a8a}
.chips li:nth-child(5){background:#FFD1DC;color:#8a1a3a}
.kicker{color:#0071E3;opacity:.85}
pre{background:#1d1d1f;border-radius:20px;color:#7ee0a3}
.hallnav a{border:none;border-radius:18px;background:#1d1d1f;color:#fff}
.hallnav a:last-child{background:#0071E3}
""",
'bauhaus': """
body{background:#F5EFE0;color:#111;font-family:Futura,"Century Gothic","PingFang SC",sans-serif}
::selection{background:#D32F2F;color:#fff}
.topbar{background:rgba(245,239,224,.92);border-bottom:4px solid #111}
.hero .big{font-weight:800;text-transform:uppercase;letter-spacing:-.02em}
.hero .en{letter-spacing:.2em}
.hero .man{background:#fff;border:3px solid #111;padding:20px 26px;box-shadow:8px 8px 0 #111}
.meta span{border:2px solid #111;border-radius:0;background:#fff;font-weight:700}
.a1{width:170px;height:170px;background:#D32F2F;top:10%;right:9%}
.a2{width:170px;height:170px;background:#1976D2;border-radius:50%;top:34%;right:22%}
.a3{width:0;height:0;border-left:85px solid transparent;border-right:85px solid transparent;border-bottom:150px solid #FDD835;bottom:8%;right:10%}
.prose{background:#fff;border:3px solid #111;padding:30px;box-shadow:8px 8px 0 #D32F2F}
.chips li{border:2px solid #111;background:#fff;font-weight:700}
.chips li:nth-child(3n+1){background:#FDD835}.chips li:nth-child(3n+2){background:#D32F2F;color:#fff}.chips li:nth-child(3n){background:#1976D2;color:#fff}
pre{background:#111;color:#FDD835}
.tl b{color:#D32F2F}
.hallnav a{border:3px solid #111;background:#fff;font-weight:700}
""",
'constructivism': """
body{background:#E8E0D0;color:#111;font-family:"Arial Black","PingFang SC",sans-serif}
::selection{background:#C62828;color:#E8E0D0}
.topbar{background:rgba(232,224,208,.94);border-bottom:6px solid #111}
.hero{background:repeating-linear-gradient(45deg,transparent 0 180px,rgba(198,40,40,.08) 180px 200px)}
.hero .big{font-weight:900;text-transform:uppercase;transform:rotate(-2deg);letter-spacing:-.03em}
.hero .en{color:#C62828;font-weight:900;letter-spacing:.15em;transform:rotate(-2deg)}
.hero .man{background:#111;color:#E8E0D0;padding:20px 26px;transform:rotate(-1deg);font-weight:800;box-shadow:10px 10px 0 #C62828}
.meta span{border:3px solid #111;border-radius:0;background:#C62828;color:#fff;font-weight:900;transform:rotate(-1.5deg)}
.a1{width:300px;height:26px;background:#C62828;top:16%;right:4%;transform:rotate(-24deg)}
.a2{width:200px;height:200px;background:#111;top:34%;right:16%;transform:rotate(-24deg);clip-path:polygon(0 0,100% 0,100% 30%,30% 100%,0 100%)}
.a3{width:150px;height:150px;border:10px solid #C62828;border-radius:50%;bottom:8%;right:6%;transform:rotate(-12deg)}
.sec h3{font-weight:900;text-transform:uppercase;transform:rotate(-1deg)}
.prose{background:#fff;border-left:14px solid #C62828;padding:30px;font-weight:600;box-shadow:8px 8px 0 #111}
.chips li{border:3px solid #111;background:#fff;font-weight:800;transform:rotate(-1deg)}
.chips li:nth-child(even){background:#C62828;color:#fff;transform:rotate(1deg)}
.tl b{color:#C62828;text-transform:uppercase}
pre{background:#111;color:#E8E0D0;border-top:8px solid #C62828}
.hallnav a{border:3px solid #111;background:#111;color:#E8E0D0;font-weight:900;text-transform:uppercase}
""",
'artdeco': """
body{background:#0e0e12;color:#d4af37;font-family:Didot,"Bodoni MT",Georgia,"Songti SC",serif}
::selection{background:#d4af37;color:#0e0e12}
.topbar{background:rgba(14,14,18,.94);border-bottom:1px solid #d4af37;letter-spacing:.2em}
.hero{background:repeating-conic-gradient(from 180deg at 50% 130%,transparent 0 8deg,rgba(212,175,55,.07) 8deg 10deg)}
.hero .big{font-weight:400;letter-spacing:.25em;text-transform:uppercase;text-shadow:0 0 40px rgba(212,175,55,.4)}
.hero .en{letter-spacing:.5em;text-transform:uppercase}
.hero .man{border:1px solid #d4af37;padding:20px 30px;letter-spacing:.05em;background:rgba(212,175,55,.05)}
.meta span{border:1px solid #d4af37;border-radius:0;letter-spacing:.15em}
.a1{width:220px;height:220px;top:10%;right:8%;background:repeating-conic-gradient(from 180deg at 50% 100%,#d4af37 0 6deg,transparent 6deg 14deg);-webkit-mask:radial-gradient(circle at 50% 100%,#000 0 68%,transparent 69%);mask:radial-gradient(circle at 50% 100%,#000 0 68%,transparent 69%);animation:floaty 9s ease-in-out infinite}
.a2{width:120px;height:120px;border:1px solid #d4af37;transform:rotate(45deg);bottom:14%;right:26%}
.a3{width:70px;height:70px;border:1px solid #d4af37;bottom:16%;right:32%;transform:rotate(45deg)}
.sec h3{font-weight:400;letter-spacing:.3em;text-transform:uppercase}
.prose{border:1px solid #d4af37;background:rgba(212,175,55,.05);padding:34px;line-height:2.2}
.chips li{border:1px solid #d4af37;letter-spacing:.08em;padding:10px 20px}
pre{background:#16161c;border:1px solid #d4af37;color:#d4af37}
.tl b{color:#d4af37;font-weight:400;letter-spacing:.15em}
.hallnav a{border:1px solid #d4af37;letter-spacing:.2em}
""",
'memphis': """
body{background:#FFF7F0;color:#111;font-family:"Comic Sans MS","PingFang SC",sans-serif}
::selection{background:#FF6FA5;color:#fff}
.topbar{background:rgba(255,247,240,.94);border-bottom:4px dashed #111}
.hero{background-image:radial-gradient(circle,#111 2.5px,transparent 3px);background-size:42px 42px}
.hero .big{font-weight:900;transform:rotate(-2deg);text-shadow:4px 4px 0 #40C4FF}
.hero .en{color:#FF6FA5;font-weight:700}
.hero .man{background:#fff;border:4px solid #111;padding:20px 26px;box-shadow:8px 8px 0 #FF6FA5;transform:rotate(.8deg)}
.meta span{border:3px solid #111;background:#FFE94A;font-weight:700;border-radius:0;transform:rotate(-1.5deg)}
.a1{width:150px;height:150px;background:#40C4FF;border-radius:50%;border:4px solid #111;top:10%;right:8%;animation:floaty 5s ease-in-out infinite}
.a2{width:170px;height:36px;background:repeating-linear-gradient(90deg,#FF6FA5 0 16px,transparent 16px 30px);top:38%;right:20%;transform:rotate(-10deg)}
.a3{width:0;height:0;border-left:55px solid transparent;border-right:55px solid transparent;border-bottom:96px solid #FFE94A;filter:drop-shadow(4px 4px 0 #111);bottom:10%;right:10%;animation:floaty 6s 1s ease-in-out infinite}
.sec h3{font-weight:900;transform:rotate(-1deg)}
.prose{background:#fff;border:4px solid #111;padding:30px;box-shadow:10px 10px 0 #40C4FF;font-weight:600}
.chips li{border:3px solid #111;font-weight:700;transform:rotate(-1deg);background:#fff}
.chips li:nth-child(4n+1){background:#FFE94A}.chips li:nth-child(4n+2){background:#FF6FA5;color:#fff}
.chips li:nth-child(4n+3){background:#40C4FF}.chips li:nth-child(4n){background:#7CFC9A;transform:rotate(1.5deg)}
pre{background:#111;color:#7CFC9A;border:4px dashed #FF6FA5}
.hallnav a{border:4px solid #111;background:#FFE94A;font-weight:700;box-shadow:5px 5px 0 #111}
""",
'popart': """
body{background:#FFDE00;color:#111;font-family:"Arial Black","PingFang SC",sans-serif}
::selection{background:#E4002B;color:#FFDE00}
.topbar{background:rgba(255,222,0,.94);border-bottom:5px solid #111}
.hero{background-image:radial-gradient(circle,#111 2px,transparent 2.4px);background-size:14px 14px}
.hero .big{font-weight:900;text-transform:uppercase;color:#E4002B;-webkit-text-stroke:3px #111;text-shadow:6px 6px 0 #111}
.hero .en{font-weight:900;letter-spacing:.2em}
.hero .man{background:#fff;border:4px solid #111;padding:20px 26px;font-weight:800;box-shadow:8px 8px 0 #E4002B;transform:rotate(-1deg)}
.meta span{border:3px solid #111;background:#fff;font-weight:900;border-radius:0}
.a1{width:150px;height:150px;background:#E4002B;border-radius:50%;border:5px solid #111;top:10%;right:8%;animation:floaty 5s ease-in-out infinite}
.a2{width:120px;height:120px;background:#2196F3;border:5px solid #111;bottom:12%;right:22%;transform:rotate(10deg);animation:floaty 6s 1s ease-in-out infinite}
.prose{background:#fff;border:4px solid #111;padding:30px;box-shadow:10px 10px 0 #2196F3;font-weight:600;background-image:radial-gradient(circle,rgba(0,0,0,.14) 1.5px,transparent 1.8px);background-size:12px 12px}
.chips li{border:3px solid #111;font-weight:900;padding:10px 18px;background:#fff}
.chips li:nth-child(odd){background:#E4002B;color:#FFDE00}.chips li:nth-child(3n){background:#2196F3;color:#fff}
pre{background:#111;color:#FFDE00;border:4px solid #E4002B}
.hallnav a{border:4px solid #111;background:#E4002B;color:#FFDE00;font-weight:900;box-shadow:5px 5px 0 #111}
""",
'vaporwave': """
body{background:linear-gradient(180deg,#2B0A54,#4A1A6E 60%,#FF71CE 130%);color:#01CDFE;font-family:"MS PGothic","Courier New","PingFang SC",monospace}
::selection{background:#FF71CE;color:#2B0A54}
.topbar{background:rgba(43,10,84,.92);border-bottom:1px solid #01CDFE;letter-spacing:.15em}
.hero .big{color:#FF71CE;font-weight:900;font-style:italic;text-shadow:0 0 30px rgba(255,113,206,.7),4px 4px 0 #01CDFE;letter-spacing:.1em}
.hero .en{letter-spacing:.6em;color:#fff}
.hero .man{background:rgba(1,205,254,.08);border:1px solid #01CDFE;padding:20px 26px;letter-spacing:.12em;box-shadow:0 0 30px rgba(1,205,254,.25);color:#d9faff}
.meta span{border:1px solid #FF71CE;color:#FF71CE;border-radius:0;letter-spacing:.2em}
.a1{width:180px;height:180px;top:10%;right:10%;background:conic-gradient(#e8e8e8 0 25%,#2B0A54 0 50%,#e8e8e8 0 75%,#2B0A54 0);clip-path:polygon(50% 0,90% 10%,100% 50%,90% 90%,50% 100%,10% 90%,0 50%,10% 10%);opacity:.8;animation:spin 24s linear infinite}
.a2{width:220px;height:120px;background:linear-gradient(180deg,#FF71CE,#B14BFF);clip-path:polygon(50% 0,100% 100%,0 100%);bottom:6%;right:6%;opacity:.85;filter:blur(1px)}
.a3{width:100%;height:3px;background:linear-gradient(90deg,transparent,#01CDFE,transparent);bottom:20%;left:0;animation:tw 2s ease-in-out infinite}
.prose{background:rgba(43,10,84,.7);border:1px solid #01CDFE;padding:30px;color:#d9faff;letter-spacing:.05em;box-shadow:0 0 40px rgba(1,205,254,.15)}
.chips li{border:1px solid #01CDFE;color:#d9faff;background:rgba(1,205,254,.08);letter-spacing:.08em}
.tl b{color:#FF71CE;letter-spacing:.15em}
pre{background:#0d0318;border:1px solid #FF71CE;color:#01CDFE;letter-spacing:.05em}
.hallnav a{border:1px solid #01CDFE;color:#01CDFE;letter-spacing:.15em}
""",
'frutigeraero': """
body{background:linear-gradient(180deg,#87CEEB 0%,#BFE8F5 45%,#5BB85D 100%);color:#0A3A5A;font-family:Frutiger,"Segoe UI","PingFang SC",sans-serif}
::selection{background:#5BB85D;color:#fff}
.topbar{background:rgba(255,255,255,.4);backdrop-filter:blur(14px);border-bottom:1px solid rgba(255,255,255,.7)}
.hero .big{font-weight:800;color:#fff;text-shadow:0 2px 20px rgba(10,58,90,.4)}
.hero .en{color:#0A3A5A;font-weight:600}
.hero .man{background:rgba(255,255,255,.5);backdrop-filter:blur(12px) saturate(160%);border:1px solid rgba(255,255,255,.9);border-radius:22px;padding:20px 26px;box-shadow:inset 0 1px 0 #fff,0 14px 34px rgba(10,58,90,.2)}
.meta span{border:none;border-radius:99px;background:rgba(255,255,255,.55);backdrop-filter:blur(8px);font-weight:600;box-shadow:inset 0 1px 0 #fff,0 4px 12px rgba(10,58,90,.15);padding:8px 16px}
.a1{width:90px;height:90px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:radial-gradient(circle at 32% 28%,rgba(255,255,255,.95) 0%,rgba(255,255,255,.25) 22%,rgba(135,206,235,.5) 60%,rgba(70,160,220,.65));top:12%;right:12%;animation:floaty 5s ease-in-out infinite;box-shadow:0 8px 20px rgba(70,160,220,.4)}
.a2{width:60px;height:60px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:radial-gradient(circle at 32% 28%,rgba(255,255,255,.95) 0%,rgba(255,255,255,.25) 22%,rgba(135,206,235,.5) 60%,rgba(70,160,220,.65));top:26%;right:26%;animation:floaty 6s 1s ease-in-out infinite}
.a3{width:44px;height:44px;border-radius:50%;background:radial-gradient(circle at 32% 28%,rgba(255,255,255,.95),rgba(91,184,93,.5));bottom:16%;right:14%;animation:floaty 7s 2s ease-in-out infinite}
.prose{background:rgba(255,255,255,.55);backdrop-filter:blur(14px) saturate(160%);border:1px solid rgba(255,255,255,.9);border-radius:26px;padding:32px;box-shadow:inset 0 1px 0 #fff,0 18px 40px rgba(10,58,90,.18)}
.chips li{border-radius:99px;background:rgba(255,255,255,.6);backdrop-filter:blur(8px);font-weight:600;box-shadow:inset 0 1px 0 #fff,0 6px 14px rgba(10,58,90,.15);padding:10px 18px;border:1px solid rgba(255,255,255,.9)}
.tl b{color:#0A6A3A}
pre{background:rgba(10,58,90,.85);color:#BFE8F5;border-radius:18px;box-shadow:inset 0 1px 0 rgba(255,255,255,.3)}
.hallnav a{border:none;border-radius:99px;background:rgba(255,255,255,.6);backdrop-filter:blur(8px);font-weight:600;box-shadow:inset 0 1px 0 #fff,0 6px 16px rgba(10,58,90,.2);color:#0A3A5A}
""",
'aciddesign': """
body{background:#0A0A0A;color:#D9FF3D;font-family:"Arial Black","PingFang SC",sans-serif}
::selection{background:#B14BFF;color:#D9FF3D}
.topbar{background:rgba(10,10,10,.92);border-bottom:2px solid;border-image:linear-gradient(90deg,#D9FF3D,#B14BFF,#FF3DE8) 1}
.hero .big{font-weight:900;font-style:italic;background:linear-gradient(135deg,#D9FF3D,#B14BFF 55%,#FF3DE8);-webkit-background-clip:text;background-clip:text;color:transparent;filter:contrast(130%) saturate(150%);transform:skewX(-4deg)}
.hero .en{color:#B14BFF;font-style:italic;letter-spacing:.2em}
.hero .man{border:1px solid #B14BFF;padding:20px 26px;color:#e8ffb0;background:linear-gradient(135deg,rgba(217,255,61,.08),rgba(177,75,255,.12));transform:rotate(-.6deg)}
.meta span{border:1px solid #D9FF3D;color:#D9FF3D;border-radius:0;font-style:italic}
.a1{width:170px;height:170px;border-radius:50%;background:conic-gradient(#D9FF3D,#B14BFF,#FF3DE8,#0ff,#D9FF3D);filter:blur(24px);top:12%;right:10%;animation:spin 10s linear infinite;opacity:.8}
.a2{width:120px;height:120px;background:linear-gradient(135deg,#FF3DE8,#B14BFF);clip-path:polygon(50% 0,63% 38%,98% 38%,68% 59%,79% 91%,50% 70%,21% 91%,32% 59%,2% 38%,37% 38%);bottom:14%;right:24%;animation:spin 8s linear infinite reverse}
.prose{border-left:4px solid #D9FF3D;background:linear-gradient(135deg,rgba(217,255,61,.06),rgba(177,75,255,.1));padding:30px;color:#e8ffb0}
.chips li{border:1px solid #B14BFF;color:#e8ffb0;background:rgba(177,75,255,.1);font-style:italic}
.tl b{color:#FF3DE8}
pre{background:#000;border:1px solid #D9FF3D;color:#D9FF3D}
.hallnav a{border:2px solid #D9FF3D;color:#D9FF3D;font-style:italic}
.hallnav a:last-child{border-color:#B14BFF;color:#B14BFF}
""",
'pixelart': """
body{background:#1A1C2C;color:#F4F4F4;font-family:"Courier New",monospace}
::selection{background:#FF004D;color:#F4F4F4}
.topbar{background:#262B44;border-bottom:4px solid #000;box-shadow:0 4px 0 rgba(0,0,0,.4);letter-spacing:.1em}
.hero .big{font-weight:900;color:#FF004D;text-shadow:4px 4px 0 #000;letter-spacing:0}
.hero .en{color:#FFCD75;letter-spacing:.2em}
.hero .man{background:#262B44;border:4px solid #000;padding:20px 26px;box-shadow:6px 6px 0 #000}
.meta span{border:3px solid #000;background:#FF004D;color:#fff;border-radius:0;font-weight:700;box-shadow:3px 3px 0 #000;padding:6px 12px}
.a1{width:144px;height:144px;top:12%;right:10%;background:conic-gradient(#FF004D 0 25%,#000 0 50%,#FF004D 0 75%,#000 0);background-size:36px 36px;image-rendering:pixelated;animation:floaty 4s steps(4) infinite}
.a2{width:96px;height:96px;background:#41A6F6;bottom:14%;right:26%;box-shadow:6px 6px 0 #000;animation:floaty 5s steps(5) infinite}
.prose{background:#262B44;border:4px solid #000;padding:30px;box-shadow:6px 6px 0 #000}
.chips li{border:3px solid #000;border-radius:0;font-weight:700;box-shadow:3px 3px 0 #000;padding:8px 14px}
.chips li:nth-child(3n+1){background:#FF004D}.chips li:nth-child(3n+2){background:#41A6F6}.chips li:nth-child(3n){background:#73EFF7;color:#000}
.tl b{color:#FFCD75}
pre{background:#000;color:#73EFF7;border:4px solid #262B44}
.hallnav a{border:3px solid #000;background:#FF004D;color:#fff;font-weight:700;box-shadow:4px 4px 0 #000;border-radius:0}
.hallnav a:last-child{background:#41A6F6}
""",
'aurora': """
body{background:#0a0a12;color:#fff;font-family:-apple-system,"Helvetica Neue","PingFang SC",sans-serif}
::selection{background:#7C3AED;color:#fff}
.topbar{background:rgba(10,10,18,.75);backdrop-filter:blur(14px);border-bottom:1px solid rgba(255,255,255,.08)}
.hero{background:radial-gradient(45% 60% at 18% 28%,rgba(124,58,237,.5),transparent),radial-gradient(50% 50% at 82% 18%,rgba(6,182,212,.4),transparent),radial-gradient(60% 55% at 50% 95%,rgba(236,72,153,.35),transparent)}
.hero .big{font-weight:800;letter-spacing:-.03em}
.hero .en{color:#a5a5c0}
.hero .man{color:#d5d5e8}
.meta span{border:1px solid rgba(255,255,255,.2);border-radius:99px;color:#c9c9e0;backdrop-filter:blur(6px)}
.a1{width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,#7C3AED,transparent 70%);filter:blur(50px);top:6%;left:6%;animation:orb1 12s ease-in-out infinite}
.a2{width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,#06B6D4,transparent 70%);filter:blur(50px);bottom:0;right:8%;animation:orb1 15s ease-in-out infinite reverse}
.a3{width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,#EC4899,transparent 70%);filter:blur(44px);top:40%;right:32%;animation:orb1 10s ease-in-out infinite}
@keyframes orb1{50%{transform:translate(50px,-36px) scale(1.12)}}
.prose{background:rgba(255,255,255,.05);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.12);border-radius:22px;padding:32px;color:#d5d5e8}
.chips li{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:99px;color:#c9c9e0;padding:10px 18px}
.kicker{color:#a78bfa;opacity:.9}
.tl b{color:#a78bfa}
pre{background:rgba(0,0,0,.5);border:1px solid rgba(255,255,255,.14);border-radius:16px;color:#7ee0a3}
.hallnav a{border:1px solid rgba(255,255,255,.2);border-radius:99px;background:rgba(255,255,255,.05);backdrop-filter:blur(8px)}
""",
'papercut': """
body{background:#FFF8E7;color:#5A4632;font-family:"Comic Sans MS","PingFang SC",sans-serif}
::selection{background:#E8634A;color:#fff}
.topbar{background:rgba(255,248,231,.94);border-bottom:3px dashed #C9B896}
.hero .big{font-weight:800;color:#E8634A}
.hero .man{background:#fff;border-radius:255px 15px 225px 15px/15px 225px 15px 255px;padding:22px 30px;box-shadow:3px 6px 0 rgba(0,0,0,.12)}
.meta span{border:none;border-radius:255px 15px 225px 15px/15px 225px 15px 255px;background:#FFE0B2;font-weight:600;box-shadow:2px 4px 0 rgba(0,0,0,.1);padding:8px 16px}
.a1{width:160px;height:160px;border-radius:60% 40% 55% 45%/50% 60% 40% 50%;background:#FFD3B6;box-shadow:4px 8px 0 rgba(0,0,0,.1);top:10%;right:8%;animation:floaty 6s ease-in-out infinite}
.a2{width:110px;height:110px;border-radius:40% 60% 45% 55%/55% 45% 60% 40%;background:#A8E6CF;box-shadow:4px 8px 0 rgba(0,0,0,.1);bottom:14%;right:22%;animation:floaty 7s 1s ease-in-out infinite}
.a3{width:70px;height:70px;border-radius:55% 45% 60% 40%/45% 55% 40% 60%;background:#FF8B94;box-shadow:3px 6px 0 rgba(0,0,0,.1);top:38%;right:30%;animation:floaty 5s .5s ease-in-out infinite}
.prose{background:#fff;border-radius:255px 15px 225px 15px/15px 225px 15px 255px;padding:34px;box-shadow:4px 8px 0 rgba(0,0,0,.12)}
.chips li{border-radius:255px 15px 225px 15px/15px 225px 15px 255px;font-weight:600;padding:10px 18px;box-shadow:2px 4px 0 rgba(0,0,0,.1)}
.chips li:nth-child(4n+1){background:#FFD3B6}.chips li:nth-child(4n+2){background:#A8E6CF}
.chips li:nth-child(4n+3){background:#FFAAA5;color:#6b1f14}.chips li:nth-child(4n){background:#DCD3FF}
.tl b{color:#E8634A}
pre{background:#5A4632;color:#FFF8E7;border-radius:15px 255px 15px 225px/225px 15px 255px 15px;box-shadow:4px 8px 0 rgba(0,0,0,.15)}
.hallnav a{border:none;border-radius:255px 15px 225px 15px/15px 225px 15px 255px;background:#E8634A;color:#fff;font-weight:600;box-shadow:3px 6px 0 rgba(0,0,0,.15)}
.hallnav a:last-child{background:#5BB85D}
""",
'doodle': """
body{background:#FFFDF5;color:#111;font-family:"Comic Sans MS","Segoe Print","PingFang SC",cursive}
::selection{background:#F25C54;color:#fff}
.topbar{background:rgba(255,253,245,.94);border-bottom:3px solid #111;border-radius:0 0 255px 15px/0 0 25px 15px}
.hero .big{font-weight:900;transform:rotate(-1.5deg)}
.hero .big u{text-decoration-style:wavy;text-decoration-color:#F25C54}
.hero .en{transform:rotate(1deg)}
.hero .man{border:3px solid #111;border-radius:255px 15px 225px 15px/15px 225px 15px 255px;padding:20px 28px;transform:rotate(-.8deg);background:#fff}
.meta span{border:2px solid #111;border-radius:255px 15px 225px 15px/15px 225px 15px 255px;background:#fff;transform:rotate(-1deg)}
.a1{width:150px;height:150px;border:4px solid #111;border-radius:52% 48% 55% 45%/48% 55% 45% 52%;top:10%;right:8%;background:#F25C54;transform:rotate(3deg);animation:floaty 5s ease-in-out infinite}
.a2{width:110px;height:14px;background:#F25C54;top:36%;right:22%;border-radius:99px;transform:rotate(-4deg)}
.a3{width:80px;height:80px;border:3px dashed #111;border-radius:50%;bottom:12%;right:10%;animation:spin 14s linear infinite}
.sec h3{transform:rotate(-.8deg)}
.prose{background:#fff;border:3px solid #111;border-radius:255px 15px 225px 15px/15px 225px 15px 255px;padding:32px;transform:rotate(-.4deg)}
.chips li{border:2px solid #111;border-radius:255px 15px 225px 15px/15px 225px 15px 255px;background:#fff;transform:rotate(-1deg);padding:10px 18px}
.chips li:nth-child(odd){transform:rotate(1.2deg)}
.chips li:nth-child(3n){background:#FFE9A8}
.tl b{color:#F25C54}
pre{background:#111;color:#FFE9A8;border-radius:15px 255px 15px 225px/225px 15px 255px 15px;transform:rotate(.4deg)}
.hallnav a{border:3px solid #111;border-radius:255px 15px 225px 15px/15px 225px 15px 255px;background:#fff}
.hallnav a:last-child{background:#F25C54;color:#fff}
""",
'psychedelic': """
body{background:radial-gradient(circle at 50% 0%,#FF6F00,#FF3DE8 40%,#4A148C 80%);color:#76FF03;font-family:"Comic Sans MS","PingFang SC",fantasy}
::selection{background:#76FF03;color:#4A148C}
.topbar{background:rgba(74,20,140,.85);border-bottom:3px wavy #76FF03;letter-spacing:.1em}
.hero .big{font-weight:900;font-style:italic;color:#FFEB3B;text-shadow:3px 3px 0 #FF3DE8,6px 6px 0 #4A148C;transform:rotate(-2deg);letter-spacing:-.02em}
.hero .en{color:#76FF03;font-style:italic;letter-spacing:.2em}
.hero .man{color:#fff;font-style:italic;text-shadow:0 2px 12px rgba(0,0,0,.4)}
.meta span{border:2px solid #76FF03;color:#76FF03;border-radius:99px;transform:rotate(-2deg)}
.a1{width:220px;height:220px;border-radius:50%;background:repeating-conic-gradient(#FF3DE8 0 15deg,#FFEB3B 15deg 30deg,#76FF03 30deg 45deg,#4A148C 45deg 60deg);top:10%;right:8%;animation:spin 20s linear infinite;opacity:.85}
.a2{width:120px;height:120px;border-radius:50%;border:6px wavy #FFEB3B;bottom:14%;right:24%;animation:spin 12s linear infinite reverse}
.sec h3{font-style:italic;color:#FFEB3B;text-shadow:2px 2px 0 #FF3DE8}
.prose{color:#fff;background:rgba(74,20,140,.55);border:3px wavy #76FF03;border-radius:40px 8px 40px 8px;padding:32px;font-style:italic}
.chips li{border:2px solid #FFEB3B;color:#FFEB3B;background:rgba(255,59,232,.2);border-radius:99px;transform:rotate(-1.5deg);font-style:italic}
.chips li:nth-child(even){transform:rotate(1.5deg);border-color:#76FF03;color:#76FF03}
.tl b{color:#FFEB3B}
pre{background:#1a0520;border:3px wavy #FF3DE8;color:#76FF03;border-radius:24px}
.hallnav a{border:2px solid #76FF03;color:#76FF03;border-radius:99px;font-style:italic}
""",
'grunge': """
body{background:#2B2620;color:#C9BFA8;font-family:"Courier New","PingFang SC",monospace;filter:none}
::selection{background:#8B3A2A;color:#C9BFA8}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:55;opacity:.5;background-image:radial-gradient(circle at 20% 30%,rgba(0,0,0,.5) 0 2px,transparent 3px),radial-gradient(circle at 70% 60%,rgba(0,0,0,.4) 0 1.5px,transparent 2.5px),radial-gradient(circle at 45% 80%,rgba(139,58,42,.3) 0 3px,transparent 4px);background-size:90px 90px,60px 60px,140px 140px}
.topbar{background:rgba(43,38,32,.94);border-bottom:4px solid #1a1712;letter-spacing:.05em}
.hero .big{font-weight:900;color:#E8E0C8;text-shadow:3px 3px 0 #8B3A2A;transform:rotate(-1.5deg);letter-spacing:-.02em}
.hero .en{color:#8B3A2A;font-weight:700}
.hero .man{background:#3A342C;border-left:6px solid #8B3A2A;padding:20px 26px;transform:rotate(.5deg);box-shadow:6px 8px 0 rgba(0,0,0,.4)}
.meta span{border:2px dashed #C9BFA8;border-radius:0;transform:rotate(-1deg);background:#1a1712}
.a1{width:170px;height:200px;background:#3A342C;top:10%;right:8%;transform:rotate(4deg);box-shadow:8px 10px 0 rgba(0,0,0,.5);border:2px dashed #8B3A2A}
.a1::before{content:"";position:absolute;top:-14px;left:30%;width:70px;height:26px;background:rgba(200,180,120,.4);transform:rotate(-4deg)}
.a2{width:120px;height:120px;background:#8B3A2A;bottom:12%;right:24%;transform:rotate(-7deg);opacity:.7;clip-path:polygon(0 8%,10% 0,90% 4%,100% 20%,95% 90%,85% 100%,15% 95%,0 85%)}
.sec h3{transform:rotate(-1deg);color:#E8E0C8}
.prose{background:#3A342C;padding:32px;transform:rotate(-.4deg);box-shadow:8px 10px 0 rgba(0,0,0,.45);border-top:3px solid #8B3A2A}
.chips li{border:2px dashed #C9BFA8;background:#1a1712;transform:rotate(-1deg);padding:8px 14px}
.chips li:nth-child(even){transform:rotate(1.3deg)}
.tl b{color:#E8E0C8}
pre{background:#1a1712;border:2px dashed #8B3A2A;color:#C9BFA8;transform:rotate(.3deg)}
.hallnav a{border:2px dashed #C9BFA8;background:#1a1712;transform:rotate(-.8deg)}
.hallnav a:last-child{transform:rotate(.8deg);border-color:#8B3A2A;color:#E8E0C8}
.rv{opacity:1;transform:none}
""",
'editorial': """
body{background:#FAF7F2;color:#1A1A1A;font-family:Georgia,"Songti SC","Noto Serif SC",serif}
::selection{background:#B08D4A;color:#fff}
.topbar{background:rgba(250,247,242,.95);border-bottom:1px solid #1A1A1A;font-family:Georgia,serif;letter-spacing:.12em}
.hero .big{font-family:"Playfair Display",Didot,Georgia,"Songti SC",serif;font-weight:700;line-height:1;letter-spacing:-.01em}
.hero .big::after{content:"";display:block;width:90px;height:4px;background:#B08D4A;margin-top:18px}
.hero .en{font-style:italic;letter-spacing:.18em;color:#B08D4A}
.hero .man{font-size:clamp(19px,2.6vw,27px);line-height:1.9;font-style:italic;color:#3a3a3a}
.meta span{border:none;border-top:1px solid #1A1A1A;border-bottom:1px solid #1A1A1A;border-radius:0;letter-spacing:.15em;padding:6px 14px;font-style:italic}
.a1{width:1px;height:60%;background:#1A1A1A;top:20%;right:12%}
.a2{width:130px;height:130px;border:1px solid #B08D4A;border-radius:50%;bottom:14%;right:22%}
.sec h3{font-family:"Playfair Display",Didot,Georgia,serif;font-weight:700}
.prose{line-height:2.3;font-size:17px;max-width:680px}
.prose::first-letter{font-size:4.2em;float:left;line-height:.85;padding:6px 10px 0 0;font-family:Didot,Georgia,serif;color:#B08D4A}
.chips li{border:none;border-bottom:1px solid #1A1A1A;border-radius:0;font-style:italic;padding:6px 4px}
.chips li b{font-style:normal}
.tl b{font-family:Didot,Georgia,serif;font-weight:700}
pre{background:#1A1A1A;color:#e8e0c8;font-family:"Courier New",monospace}
.hallnav a{border:none;border-top:1px solid #1A1A1A;border-bottom:1px solid #1A1A1A;font-style:italic;padding:10px 16px}
""",
'swisspunk': """
body{background:#E30613;color:#fff;font-family:Helvetica,Arial,"PingFang SC",sans-serif}
::selection{background:#F2D500;color:#111}
.topbar{background:rgba(227,6,19,.94);border-bottom:3px solid #111;font-weight:700}
.hero{background:repeating-linear-gradient(0deg,rgba(255,255,255,.08) 0 1px,transparent 1px 74px),repeating-linear-gradient(90deg,rgba(255,255,255,.08) 0 1px,transparent 1px 74px)}
.hero .big{font-weight:900;text-transform:uppercase;letter-spacing:-.05em;transform:rotate(-2deg);text-shadow:5px 5px 0 #111}
.hero .en{font-weight:700;letter-spacing:.2em;color:#F2D500;transform:skewX(-8deg)}
.hero .man{background:#fff;color:#111;border:5px solid #111;padding:20px 24px;transform:rotate(1deg) skewX(-2deg);box-shadow:9px 9px 0 #111;font-weight:700}
.meta span{border:3px solid #111;border-radius:0;background:#F2D500;color:#111;font-weight:800;transform:rotate(-2deg)}
.a1{width:190px;height:190px;border:8px solid #fff;background:#E30613;top:12%;right:8%;transform:rotate(12deg);animation:spin 13s linear infinite}
.a2{width:130px;height:74px;background:#F2D500;border:5px solid #111;bottom:15%;right:23%;transform:skewX(-18deg) rotate(7deg);animation:floaty 5s ease-in-out infinite}
.sec h3{font-weight:900;text-transform:uppercase;letter-spacing:-.02em;transform:skewX(-4deg)}
.prose{background:#fff;color:#111;border:4px solid #111;padding:28px;box-shadow:10px 10px 0 #111;transform:rotate(-.6deg)}
.chips li{border:3px solid #111;background:#F2D500;color:#111;font-weight:800;transform:rotate(-1deg);box-shadow:4px 4px 0 #111}
.chips li:nth-child(even){background:#fff}
pre{background:#111;color:#F2D500;border:4px solid #fff;box-shadow:7px 7px 0 #111}
.tl b{color:#F2D500;text-transform:uppercase}
.hallnav a{border:3px solid #111;background:#F2D500;color:#111;font-weight:800;box-shadow:5px 5px 0 #111}
""",
'wabisabi': """
body{background:#F4F0E8;color:#4D493F;font-family:"Hiragino Mincho ProN","Songti SC",serif}
::selection{background:#9E6B4E;color:#fff}
.topbar{background:rgba(244,240,232,.9);border-bottom:1px solid #C7B8A2;letter-spacing:.08em}
.hero .big{font-weight:400;letter-spacing:.12em;color:#5D574E}
.hero .en{font-style:italic;letter-spacing:.2em;color:#9E6B4E}
.hero .man{font-size:clamp(18px,2.5vw,26px);line-height:2;color:#756956;max-width:620px}
.meta span{border:1px solid #C7B8A2;border-radius:0;color:#756956;letter-spacing:.08em}
.a1{width:180px;height:140px;border-radius:46% 54% 50% 43%;background:#C7B8A2;opacity:.55;top:12%;right:8%;animation:floaty 10s ease-in-out infinite}
.a2{width:100px;height:100px;border:1px solid #9E6B4E;border-radius:50%;bottom:15%;right:25%;opacity:.65;animation:floaty 12s 1s ease-in-out infinite}
.sec h3{font-weight:400;letter-spacing:.2em;color:#756956}
.prose{background:rgba(255,252,245,.65);border:1px solid #D6CCBC;padding:32px;line-height:2.3;color:#5D574E}
.chips li{border:1px solid #D6CCBC;border-radius:2px;background:#ECE5D9;color:#756956;padding:9px 16px}
pre{background:#3D3A34;color:#E8E1D6;border-radius:2px;border:1px solid #9E6B4E}
.tl b{color:#9E6B4E;font-weight:400;letter-spacing:.12em}
.hallnav a{border:1px solid #B9AA95;color:#756956;background:rgba(255,252,245,.45);letter-spacing:.08em}
""",
'typographic': """
body{background:#F5F2EB;color:#111;font-family:Helvetica,Arial,"PingFang SC",sans-serif}
::selection{background:#D32F2F;color:#fff}
.topbar{background:rgba(245,242,235,.95);border-bottom:2px solid #111;font-size:11px;letter-spacing:.08em}
.hero .big{font-weight:900;letter-spacing:-.09em;text-transform:uppercase;line-height:.86}
.hero .en{font-weight:700;letter-spacing:.35em;color:#D32F2F;text-transform:uppercase}
.hero .man{font-size:clamp(18px,2.5vw,25px);font-weight:700;line-height:1.3;border-left:9px solid #D32F2F;padding:10px 20px;max-width:660px}
.meta span{border:2px solid #111;border-radius:0;font-weight:700;padding:6px 12px}
.a1{width:220px;height:220px;border:8px solid #111;color:#D32F2F;top:10%;right:8%;font-size:130px;animation:spin 20s linear infinite}
.a1::after{content:"A";position:absolute;inset:0;display:grid;place-items:center;font:900 170px/.8 Helvetica;color:#D32F2F}
.a2{width:180px;height:8px;background:#D32F2F;bottom:19%;right:21%;box-shadow:0 18px 0 #111,0 36px 0 #D32F2F;animation:floaty 6s ease-in-out infinite}
.sec h3{font-weight:900;text-transform:uppercase;letter-spacing:-.05em}
.prose{border-left:9px solid #111;background:#fff;padding:30px;font-size:17px;line-height:2}
.chips li{border:none;border-bottom:2px solid #111;border-radius:0;background:transparent;color:#111;font-weight:700;padding:8px 4px}
pre{background:#111;color:#F5F2EB;border-left:8px solid #D32F2F}
.tl b{color:#D32F2F;font-weight:900}
.hallnav a{border:2px solid #111;border-radius:0;background:#fff;color:#111;font-weight:700}
""",
'antidesign': """
body{background:#E8E6DF;color:#111;font-family:Impact,"Arial Black","PingFang SC",sans-serif}
::selection{background:#FF00A8;color:#fff}
.topbar{background:#00FF66;color:#111;border-bottom:8px dotted #FF00A8;font-family:monospace;transform:rotate(-1deg)}
.hero{background:repeating-linear-gradient(12deg,transparent 0 90px,rgba(255,0,168,.12) 90px 114px)}
.hero .big{font-weight:900;color:#FF00A8;text-transform:uppercase;transform:rotate(4deg);text-shadow:8px 8px 0 #00FF66}
.hero .en{font-family:monospace;color:#7B2FFF;letter-spacing:-.03em;transform:rotate(-3deg)}
.hero .man{background:#00FF66;border:7px dotted #111;color:#111;padding:16px 20px;transform:rotate(-2deg);box-shadow:12px 12px 0 #FF00A8}
.meta span{border:4px dotted #111;border-radius:0;background:#FF6B00;color:#fff;font-weight:900;transform:rotate(3deg)}
.a1{width:180px;height:140px;background:#7B2FFF;border:8px solid #111;top:10%;right:7%;transform:rotate(15deg);animation:floaty 4s ease-in-out infinite}
.a2{width:110px;height:110px;background:#00FF66;border:5px dashed #FF00A8;bottom:13%;right:24%;transform:rotate(-22deg);animation:spin 7s linear infinite}
.sec h3{font-weight:900;text-transform:uppercase;transform:skewX(-8deg)}
.prose{background:#fff;border:6px dotted #111;padding:26px;transform:rotate(1deg);box-shadow:10px 10px 0 #7B2FFF}
.chips li{border:4px dotted #111;border-radius:0;background:#00FF66;color:#111;font-weight:900;transform:rotate(-2deg)}
pre{background:#111;color:#00FF66;border:6px dotted #FF00A8}
.tl b{color:#FF00A8;font-weight:900}
.hallnav a{border:5px dotted #111;background:#FF6B00;color:#fff;font-weight:900;transform:rotate(-2deg)}
""",
'hightech': """
body{background:#25313A;color:#DCE5E8;font-family:"Arial Narrow",Arial,"PingFang SC",sans-serif}
::selection{background:#D86B32;color:#fff}
.topbar{background:rgba(37,49,58,.94);border-bottom:4px solid #B7C4CC;color:#DCE5E8;letter-spacing:.1em}
.hero{background:linear-gradient(rgba(183,196,204,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(183,196,204,.08) 1px,transparent 1px);background-size:48px 48px}
.hero .big{font-weight:800;letter-spacing:.03em;text-shadow:4px 4px 0 #D86B32}
.hero .en{color:#D86B32;letter-spacing:.22em;font-family:monospace}
.hero .man{border:4px solid #B7C4CC;background:#34434D;color:#F2F6F7;padding:20px 24px;box-shadow:9px 9px 0 #D86B32;clip-path:polygon(12px 0,100% 0,100% calc(100% - 12px),calc(100% - 12px) 100%,0 100%,0 12px)}
.meta span{border:2px solid #B7C4CC;border-radius:0;background:#34434D;color:#DCE5E8;font-family:monospace}
.a1{width:180px;height:180px;border:12px solid #697A85;border-radius:50%;background:transparent;top:11%;right:9%;animation:spin 18s linear infinite}
.a1::before{content:"";position:absolute;inset:24px;border:3px dashed #D86B32;border-radius:50%}
.a2{width:180px;height:24px;background:#D86B32;bottom:19%;right:20%;transform:rotate(-28deg);box-shadow:0 14px 0 #B7C4CC;animation:floaty 5s ease-in-out infinite}
.sec h3{font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#F2F6F7}
.prose{background:#34434D;border:3px solid #697A85;border-left:12px solid #D86B32;padding:30px;line-height:2}
.chips li{border:2px solid #B7C4CC;background:#34434D;color:#DCE5E8;border-radius:0;font-family:monospace;padding:9px 15px}
pre{background:#172127;color:#D86B32;border:3px solid #697A85;box-shadow:8px 8px 0 #111820}
.tl b{color:#D86B32;font-family:monospace}
.hallnav a{border:3px solid #B7C4CC;background:#34434D;color:#DCE5E8;font-family:monospace}
""",
'newchinese': """
body{background:#F3EFE6;color:#38362F;font-family:"Songti SC","Noto Serif SC",Georgia,serif}
::selection{background:#B52B2B;color:#fff}
.topbar{background:rgba(243,239,230,.94);border-bottom:1px solid #5C574E;letter-spacing:.12em}
.hero{background:radial-gradient(ellipse at 82% 18%,rgba(92,87,78,.1),transparent 30%)}
.hero .big{font-weight:400;letter-spacing:.08em;color:#3E3A33}
.hero .en{font-style:italic;color:#B52B2B;letter-spacing:.2em}
.hero .man{font-size:clamp(18px,2.4vw,25px);line-height:2;color:#5C574E;border-left:3px solid #B52B2B;padding:12px 22px;background:rgba(255,252,245,.6)}
.meta span{border:1px solid #9C9484;border-radius:0;background:#FFFCF5;color:#5C574E;letter-spacing:.08em}
.a1{width:190px;height:150px;border-radius:50%;background:radial-gradient(ellipse,#222 0 14%,rgba(70,70,70,.3) 48%,transparent 72%);filter:blur(3px);top:11%;right:8%;animation:floaty 11s ease-in-out infinite}
.a2{width:86px;height:86px;border:5px solid #B52B2B;color:#B52B2B;bottom:16%;right:25%;transform:rotate(-10deg);animation:spin 18s linear infinite}
.sec h3{font-weight:400;letter-spacing:.22em;color:#5C574E}
.prose{background:#FFFCF5;border:1px solid #C9C0AF;border-left:4px solid #B52B2B;padding:32px;line-height:2.3}
.chips li{border:1px solid #C9C0AF;border-radius:0;background:#FFFCF5;color:#5C574E;padding:9px 16px}
pre{background:#38362F;color:#F3EFE6;border-left:6px solid #B52B2B}
.tl b{color:#B52B2B;font-weight:400;letter-spacing:.12em}
.hallnav a{border:1px solid #9C9484;background:#FFFCF5;color:#5C574E;letter-spacing:.08em}
""",
'opart': """
body{background:#fff;color:#111;font-family:Arial,"PingFang SC",sans-serif}
::selection{background:#111;color:#fff}
.topbar{background:#fff;border-bottom:3px solid #111;font-weight:700;letter-spacing:.08em}
.hero{background:repeating-radial-gradient(ellipse at 75% 30%,transparent 0 34px,rgba(0,0,0,.08) 35px 38px)}
.hero .big{font-weight:900;letter-spacing:-.07em;text-transform:uppercase}
.hero .en{font-weight:700;letter-spacing:.3em;color:#D7263D}
.hero .man{border:4px solid #111;background:#fff;padding:18px 24px;transform:skewX(-4deg);font-weight:700}
.meta span{border:2px solid #111;border-radius:0;background:#fff;color:#111;font-weight:700}
.a1{width:220px;height:220px;border-radius:50%;background:repeating-conic-gradient(#111 0 8deg,#fff 8deg 16deg);top:9%;right:8%;animation:spin 16s linear infinite}
.a2{width:140px;height:140px;background:repeating-radial-gradient(circle,#D7263D 0 4px,#fff 4px 10px);bottom:13%;right:24%;animation:floaty 6s ease-in-out infinite}
.sec h3{font-weight:900;text-transform:uppercase;letter-spacing:.04em}
.prose{background:#fff;border:3px solid #111;padding:28px;box-shadow:8px 8px 0 #D7263D}
.chips li{border:2px solid #111;border-radius:0;background:#fff;color:#111;font-weight:700}
pre{background:#111;color:#fff;border:4px solid #D7263D}
.tl b{color:#D7263D;font-weight:900}
.hallnav a{border:3px solid #111;background:#fff;color:#111;font-weight:700}
""",
'duotone': """
body{background:#3A0CA3;color:#fff;font-family:"Helvetica Neue","PingFang SC",sans-serif}
::selection{background:#FF4D6D;color:#fff}
.topbar{background:rgba(58,12,163,.92);border-bottom:2px solid #FF4D6D}
.hero{background:linear-gradient(135deg,rgba(255,77,109,.2),transparent 45%),radial-gradient(circle at 85% 18%,rgba(255,183,3,.3),transparent 28%)}
.hero .big{font-weight:800;letter-spacing:-.04em;color:#FFB3C1}
.hero .en{color:#FFB3C1;letter-spacing:.22em}
.hero .man{background:#FF4D6D;color:#fff;border:4px solid #FFB3C1;padding:18px 24px;box-shadow:9px 9px 0 #03045E;font-weight:700}
.meta span{border:2px solid #FFB3C1;border-radius:0;background:#5A189A;color:#fff}
.a1{width:210px;height:210px;border-radius:50%;background:linear-gradient(135deg,#FFB703,#3A0CA3);border:4px solid #FFB3C1;top:10%;right:8%;animation:spin 18s linear infinite}
.a2{width:120px;height:120px;background:linear-gradient(135deg,#00B4D8,#03045E);border-radius:20px;bottom:14%;right:24%;animation:floaty 7s ease-in-out infinite}
.sec h3{font-weight:800;color:#FFB3C1}
.prose{background:#5A189A;border:2px solid #FFB3C1;padding:30px;line-height:2}
.chips li{border:2px solid #FFB3C1;border-radius:0;background:#FF4D6D;color:#fff;font-weight:700}
pre{background:#03045E;color:#FFB3C1;border:3px solid #FF4D6D}
.tl b{color:#FFB703;font-weight:800}
.hallnav a{border:2px solid #FFB3C1;background:#5A189A;color:#fff}
""",
'flat3d': """
body{background:#F7F9FC;color:#243447;font-family:"Segoe UI","Helvetica Neue","PingFang SC",sans-serif}
::selection{background:#FFB703;color:#243447}
.topbar{background:rgba(247,249,252,.92);border-bottom:1px solid #D9E2EC;box-shadow:0 4px 12px rgba(36,52,71,.08)}
.hero{background:linear-gradient(30deg,rgba(189,224,254,.22) 12%,transparent 12.5% 87%,rgba(189,224,254,.22) 87.5%)}
.hero .big{font-weight:800;letter-spacing:-.05em}
.hero .en{font-weight:600;color:#277DA1;letter-spacing:.18em}
.hero .man{background:#fff;border-radius:14px;padding:20px 26px;box-shadow:0 12px 0 -4px rgba(36,52,71,.14);font-weight:500}
.meta span{border:none;border-radius:12px;background:#BDE0FE;color:#18577A;font-weight:700;box-shadow:0 5px 0 rgba(36,52,71,.1)}
.a1{width:150px;height:150px;background:#FFB703;clip-path:polygon(50% 0,100% 28%,100% 72%,50% 100%,0 72%,0 28%);top:11%;right:8%;animation:floaty 6s ease-in-out infinite}
.a2{width:120px;height:90px;background:#A2D2FF;transform:skewY(-28deg) rotate(30deg);bottom:14%;right:24%;box-shadow:14px 12px 0 #FFAFCC;animation:floaty 7s 1s ease-in-out infinite}
.sec h3{font-weight:700;letter-spacing:-.02em}
.prose{background:#fff;border-radius:18px;padding:30px;box-shadow:0 12px 24px rgba(36,52,71,.08)}
.chips li{border-radius:12px;background:#CDEAC0;color:#32643B;font-weight:600;box-shadow:0 5px 0 rgba(36,52,71,.1);padding:10px 18px}
pre{background:#243447;color:#CDEAC0;border-radius:14px;box-shadow:0 8px 0 rgba(36,52,71,.12)}
.tl b{color:#277DA1;font-weight:700}
.hallnav a{border:none;border-radius:12px;background:#243447;color:#fff;box-shadow:0 5px 0 rgba(36,52,71,.15)}
""",
'aigenerative': """
body{background:#111827;color:#F8FAFC;font-family:-apple-system,"Helvetica Neue","PingFang SC",sans-serif}
::selection{background:#A78BFA;color:#111827}
.topbar{background:rgba(17,24,39,.9);border-bottom:1px solid #4C1D95;backdrop-filter:blur(12px)}
.hero{background:radial-gradient(42% 60% at 18% 24%,rgba(99,102,241,.35),transparent),radial-gradient(36% 48% at 86% 20%,rgba(236,72,153,.3),transparent)}
.hero .big{font-weight:800;letter-spacing:-.04em;background:linear-gradient(120deg,#C4B5FD,#F0ABFC,#67E8F9);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero .en{color:#C4B5FD;letter-spacing:.22em}
.hero .man{background:rgba(67,56,202,.2);border:1px solid #818CF8;border-radius:12px;padding:20px 24px;color:#E0E7FF;box-shadow:0 0 30px rgba(99,102,241,.18)}
.meta span{border:1px solid #818CF8;border-radius:99px;background:rgba(99,102,241,.16);color:#C4B5FD;backdrop-filter:blur(8px)}
.a1{width:220px;height:220px;border-radius:50%;background:radial-gradient(circle,#818CF8,transparent 68%);filter:blur(18px);top:8%;right:8%;animation:floaty 8s ease-in-out infinite}
.a2{width:130px;height:130px;border:1px solid #F0ABFC;border-radius:50%;background:conic-gradient(from 20deg,transparent,#EC4899,transparent,#6366F1,transparent);bottom:14%;right:23%;animation:spin 10s linear infinite}
.sec h3{font-weight:700;color:#C4B5FD;letter-spacing:.03em}
.prose{background:rgba(31,41,55,.82);border:1px solid #4C1D95;border-radius:14px;padding:30px;color:#E0E7FF;line-height:2}
.chips li{border:1px solid #6366F1;border-radius:99px;background:rgba(99,102,241,.14);color:#C4B5FD;padding:10px 18px}
pre{background:#0B1020;border:1px solid #818CF8;border-radius:12px;color:#A7F3D0}
.tl b{color:#F0ABFC;font-weight:700}
.hallnav a{border:1px solid #818CF8;border-radius:99px;background:rgba(67,56,202,.2);color:#E0E7FF}
""",
'artsandcrafts': """
body{background:#F3E7CF;color:#3B4A2F;font-family:Georgia,"Times New Roman",serif}
::selection{background:#9A4E2F;color:#FFF8EA}
.topbar{background:#E8D7B7;border-bottom:3px solid #7A4E2D;color:#3B4A2F}
.hero{background:repeating-linear-gradient(45deg,rgba(122,78,45,.08) 0 2px,transparent 2px 14px),radial-gradient(circle at 80% 20%,rgba(154,78,47,.2),transparent 30%)}
.hero .big{font-weight:700;letter-spacing:-.04em;color:#6B3F29}
.hero .en{font-style:italic;color:#9A4E2F;letter-spacing:.2em}
.hero .man{background:#FFF8EA;border:2px solid #7A4E2D;border-radius:4px;padding:20px 24px;box-shadow:8px 8px 0 rgba(122,78,45,.2)}
.meta span{border:1px solid #9A4E2F;border-radius:2px;background:#FFF8EA;color:#6B3F29}
.a1{width:190px;height:190px;border:12px solid #9A4E2F;border-radius:50% 40% 50% 40%;background:repeating-radial-gradient(circle,#E7B27D 0 5px,#FFF8EA 5px 10px);top:9%;right:8%;animation:floaty 8s ease-in-out infinite}
.a2{width:120px;height:150px;background:linear-gradient(120deg,#3B6B4A,#9A4E2F);clip-path:polygon(50% 0,90% 24%,76% 100%,24% 100%,10% 24%);bottom:12%;right:24%;animation:floaty 7s 1s ease-in-out infinite}
.sec h3{font-weight:700;color:#6B3F29;letter-spacing:.08em}
.prose{background:#FFF8EA;border:1px solid #C28B5C;border-left:6px solid #9A4E2F;padding:30px;line-height:2.1}
.chips li{border:1px solid #C28B5C;border-radius:2px;background:#E7D6B6;color:#3B4A2F;padding:9px 16px}
pre{background:#3B4A2F;color:#F3E7CF;border:4px solid #7A4E2D}
.tl b{color:#9A4E2F;font-weight:700}
.hallnav a{border:1px solid #7A4E2D;background:#FFF8EA;color:#6B3F29}
""",
'artnouveau': """
body{background:#F4EAD2;color:#244D43;font-family:"Didot",Georgia,serif}
::selection{background:#B0475A;color:#FFF9E8}
.topbar{background:rgba(255,249,232,.9);border-bottom:2px solid #B47A32;color:#244D43}
.hero{background:radial-gradient(ellipse at 15% 30%,rgba(71,122,93,.18),transparent 28%),radial-gradient(ellipse at 86% 20%,rgba(176,71,90,.18),transparent 30%)}
.hero .big{font-weight:500;letter-spacing:-.05em;color:#477A5D}
.hero .en{color:#B0475A;letter-spacing:.24em;font-style:italic}
.hero .man{background:#FFF9E8;border:2px solid #B47A32;border-radius:48% 8% 48% 8%;padding:20px 26px;box-shadow:0 8px 0 rgba(176,71,90,.15)}
.meta span{border:1px solid #B47A32;border-radius:48% 8% 48% 8%;background:#FFF9E8;color:#477A5D}
.a1{width:200px;height:200px;border:3px solid #B47A32;border-radius:50% 8% 50% 8%;background:radial-gradient(ellipse at 30% 30%,#B0475A 0 8%,transparent 9%),radial-gradient(ellipse at 70% 70%,#477A5D 0 9%,transparent 10%);top:8%;right:8%;animation:spin 18s linear infinite}
.a2{width:120px;height:170px;background:linear-gradient(160deg,#477A5D,#B0475A);border-radius:50% 8% 50% 8%;transform:rotate(-24deg);bottom:12%;right:24%;animation:floaty 7s ease-in-out infinite}
.sec h3{font-weight:500;color:#477A5D;letter-spacing:.1em}
.prose{background:#FFF9E8;border:1px solid #D2A65B;border-radius:28% 4% 28% 4%;padding:30px;line-height:2.1}
.chips li{border:1px solid #B47A32;border-radius:48% 8% 48% 8%;background:#F1DFC0;color:#477A5D}
pre{background:#244D43;color:#F4EAD2;border:3px solid #B0475A;border-radius:18% 2% 18% 2%}
.tl b{color:#B0475A;font-weight:500}
.hallnav a{border:1px solid #B47A32;border-radius:48% 8% 48% 8%;background:#FFF9E8;color:#244D43}
""",
'viennasecession': """
body{background:#F2E6C9;color:#332B25;font-family:"Helvetica Neue",Arial,sans-serif}
::selection{background:#B58B2A;color:#FFF8E5}
.topbar{background:#FFF8E5;border-bottom:4px solid #B58B2A;color:#332B25}
.hero{background:repeating-linear-gradient(45deg,rgba(181,139,42,.12) 0 2px,transparent 2px 24px),linear-gradient(90deg,transparent 48%,rgba(51,43,37,.1) 49% 51%,transparent 52%)}
.hero .big{font-weight:700;letter-spacing:.02em;color:#332B25}
.hero .en{color:#8A681B;letter-spacing:.28em;text-transform:uppercase}
.hero .man{background:#FFF8E5;border:3px solid #B58B2A;padding:18px 24px;box-shadow:8px 8px 0 #332B25}
.meta span{border:2px solid #B58B2A;border-radius:0;background:#F7EFD9;color:#6B531B;font-weight:700}
.a1{width:200px;height:200px;border:10px solid #B58B2A;background:repeating-linear-gradient(0deg,transparent 0 20px,rgba(181,139,42,.7) 20px 23px),repeating-linear-gradient(90deg,transparent 0 20px,rgba(181,139,42,.7) 20px 23px);top:8%;right:8%;animation:spin 20s linear infinite}
.a2{width:125px;height:125px;background:#B58B2A;clip-path:polygon(50% 0,61% 39%,100% 50%,61% 61%,50% 100%,39% 61%,0 50%,39% 39%);bottom:14%;right:25%;animation:floaty 6s ease-in-out infinite}
.sec h3{font-weight:700;color:#8A681B;letter-spacing:.16em}
.prose{background:#FFF8E5;border:3px solid #B58B2A;padding:30px;box-shadow:8px 8px 0 rgba(51,43,37,.2)}
.chips li{border:2px solid #B58B2A;border-radius:0;background:#F7EFD9;color:#332B25;font-weight:700}
pre{background:#332B25;color:#F2E6C9;border:4px double #B58B2A}
.tl b{color:#8A681B;font-weight:700}
.hallnav a{border:2px solid #332B25;background:#FFF8E5;color:#332B25;font-weight:700}
""",
'futurism': """
body{background:#17202A;color:#F5F0E6;font-family:Impact,"Arial Narrow",sans-serif}
::selection{background:#E84A27;color:#17202A}
.topbar{background:#10171E;border-bottom:3px solid #E84A27;letter-spacing:.08em}
.hero{background:repeating-linear-gradient(-18deg,transparent 0 34px,rgba(232,74,39,.16) 35px 39px),linear-gradient(110deg,transparent 45%,rgba(242,177,52,.2) 46% 51%,transparent 52%)}
.hero .big{font-weight:900;font-style:italic;letter-spacing:-.08em;text-transform:uppercase;text-shadow:8px 0 #E84A27,16px 0 #F2B134}
.hero .en{color:#F2B134;font-style:italic;letter-spacing:.18em}
.hero .man{background:#263746;border:4px solid #E84A27;padding:18px 24px;transform:skewX(-8deg);font-weight:700}
.meta span{border:2px solid #F2B134;border-radius:0;background:#263746;color:#F5F0E6;font-weight:700;transform:skewX(-8deg)}
.a1{width:215px;height:95px;background:repeating-linear-gradient(-18deg,#E84A27 0 8px,transparent 8px 22px);clip-path:polygon(0 20%,100% 0,82% 100%,0 76%);top:13%;right:7%;animation:floaty 5s ease-in-out infinite}
.a2{width:130px;height:130px;border:8px solid #F2B134;background:#E84A27;clip-path:polygon(50% 0,61% 35%,100% 22%,70% 48%,100% 72%,61% 65%,50% 100%,39% 65%,0 78%,30% 48%,0 25%,39% 35%);bottom:12%;right:24%;animation:spin 9s linear infinite}
.sec h3{font-weight:900;font-style:italic;color:#F2B134;letter-spacing:.06em;text-transform:uppercase}
.prose{background:#263746;border-left:7px solid #E84A27;padding:28px;line-height:1.8;transform:skewX(-1deg)}
.chips li{border:2px solid #F2B134;border-radius:0;background:#E84A27;color:#17202A;font-weight:900;transform:skewX(-6deg)}
pre{background:#0E151B;color:#F2B134;border:4px solid #E84A27}
.tl b{color:#E84A27;font-weight:900}
.hallnav a{border:3px solid #F2B134;background:#263746;color:#F5F0E6;font-weight:700;transform:skewX(-6deg)}
""",
'dada': """
body{background:#ECE7DD;color:#151515;font-family:"Courier New",monospace}
::selection{background:#D43D2F;color:#FFFDF5}
.topbar{background:#FFFDF5;border-bottom:3px dashed #D43D2F;color:#151515}
.hero{background:linear-gradient(13deg,transparent 0 45%,rgba(212,61,47,.14) 46% 52%,transparent 53%),repeating-linear-gradient(-4deg,transparent 0 28px,rgba(21,21,21,.07) 29px 31px)}
.hero .big{font-weight:900;letter-spacing:-.1em;transform:rotate(-2deg);text-transform:uppercase}
.hero .en{color:#D43D2F;letter-spacing:.1em;transform:rotate(2deg)}
.hero .man{background:#FFFDF5;border:3px dashed #151515;padding:18px 24px;transform:rotate(1deg);box-shadow:7px 7px 0 #D43D2F}
.meta span{border:2px dashed #151515;border-radius:0;background:#D9D3C7;color:#151515;transform:rotate(-2deg)}
.a1{width:190px;height:190px;border:6px dashed #151515;border-radius:50%;background:#D43D2F;top:10%;right:8%;animation:spin 13s linear infinite}
.a2{width:120px;height:150px;background:#151515;clip-path:polygon(8% 0,92% 8%,76% 100%,20% 90%);transform:rotate(12deg);bottom:12%;right:24%;animation:floaty 6s ease-in-out infinite}
.sec h3{font-weight:900;letter-spacing:.06em;transform:rotate(-1deg)}
.prose{background:#FFFDF5;border:3px dashed #151515;padding:28px;transform:rotate(.6deg);box-shadow:8px 8px 0 rgba(212,61,47,.45)}
.chips li{border:2px dashed #151515;border-radius:0;background:#D43D2F;color:#FFFDF5;transform:rotate(-2deg)}
pre{background:#151515;color:#D9F20B;border:4px dashed #D43D2F}
.tl b{color:#D43D2F;font-weight:900}
.hallnav a{border:3px dashed #151515;background:#FFFDF5;color:#151515;transform:rotate(1deg)}
""",
'destijl': """
body{background:#F7F7F2;color:#111;font-family:Arial,Helvetica,sans-serif}
::selection{background:#D52B1E;color:#fff}
.topbar{background:#fff;border-bottom:6px solid #111;color:#111}
.hero{background:linear-gradient(90deg,transparent 0 31%,#111 31% 34%,transparent 34% 67%,#111 67% 70%,transparent 70%),linear-gradient(0deg,transparent 0 45%,#111 45% 49%,transparent 49%);background-size:100% 100%}
.hero .big{font-weight:900;letter-spacing:-.08em;text-transform:uppercase}
.hero .en{color:#2457A6;letter-spacing:.24em;font-weight:700}
.hero .man{background:#fff;border:5px solid #111;padding:18px 24px;box-shadow:10px 10px 0 #D52B1E}
.meta span{border:3px solid #111;border-radius:0;background:#F2C500;color:#111;font-weight:900}
.a1{width:190px;height:190px;background:#D52B1E;border:8px solid #111;top:9%;right:8%;animation:spin 18s linear infinite}
.a2{width:130px;height:130px;background:#2457A6;border:8px solid #111;bottom:14%;right:24%;animation:floaty 7s ease-in-out infinite}
.sec h3{font-weight:900;letter-spacing:.12em;text-transform:uppercase}
.prose{background:#fff;border:5px solid #111;padding:28px;box-shadow:12px 12px 0 #F2C500}
.chips li{border:3px solid #111;border-radius:0;background:#D52B1E;color:#fff;font-weight:700}
pre{background:#111;color:#F2C500;border:5px solid #2457A6}
.tl b{color:#D52B1E;font-weight:900}
.hallnav a{border:4px solid #111;border-radius:0;background:#fff;color:#111;font-weight:900}
""",
'surrealism': """
body{background:#DDEBEB;color:#193A52;font-family:Georgia,"Times New Roman",serif}
::selection{background:#C15A4B;color:#F8F6E9}
.topbar{background:rgba(248,246,233,.88);border-bottom:2px solid #193A52;color:#193A52}
.hero{background:radial-gradient(ellipse at 18% 24%,rgba(193,90,75,.25),transparent 24%),radial-gradient(circle at 82% 18%,rgba(229,184,92,.28),transparent 22%)}
.hero .big{font-weight:500;letter-spacing:-.05em;color:#193A52}
.hero .en{color:#C15A4B;font-style:italic;letter-spacing:.2em}
.hero .man{background:#F8F6E9;border:3px solid #193A52;border-radius:50% 12% 50% 12%;padding:20px 24px;box-shadow:14px 14px 0 rgba(193,90,75,.3)}
.meta span{border:1px solid #193A52;border-radius:50% 12% 50% 12%;background:#F8F6E9;color:#C15A4B}
.a1{width:180px;height:100px;border:4px solid #193A52;border-radius:50%;background:radial-gradient(circle at 50% 50%,#193A52 0 11%,#C15A4B 12% 20%,#F8F6E9 21% 43%,transparent 44%);top:11%;right:8%;animation:floaty 8s ease-in-out infinite}
.a2{width:130px;height:90px;background:#E5B85C;border:3px solid #193A52;border-radius:8px 8px 50% 50%;transform:rotate(-8deg);bottom:14%;right:24%;animation:floaty 6s 1s ease-in-out infinite}
.sec h3{font-weight:500;color:#C15A4B;letter-spacing:.08em}
.prose{background:#F8F6E9;border:2px solid #193A52;border-radius:50% 12% 50% 12%;padding:30px;line-height:2}
.chips li{border:1px solid #193A52;border-radius:50% 12% 50% 12%;background:#E5B85C;color:#193A52}
pre{background:#193A52;color:#F8F6E9;border:4px solid #C15A4B;border-radius:12px}
.tl b{color:#C15A4B;font-weight:700}
.hallnav a{border:2px solid #193A52;border-radius:50% 12% 50% 12%;background:#F8F6E9;color:#193A52}
""",
'streamline': """
body{background:#CFE4EA;color:#173B50;font-family:"Helvetica Neue",Arial,sans-serif}
::selection{background:#E36B38;color:#fff}
.topbar{background:rgba(238,247,247,.9);border-bottom:2px solid #173B50;color:#173B50}
.hero{background:repeating-linear-gradient(0deg,transparent 0 14px,rgba(23,59,80,.13) 14px 16px),linear-gradient(110deg,transparent 0 60%,rgba(227,107,56,.2) 60% 64%,transparent 64%)}
.hero .big{font-weight:700;letter-spacing:-.07em}
.hero .en{color:#E36B38;letter-spacing:.24em;font-weight:600}
.hero .man{background:#EEF7F7;border:2px solid #173B50;border-radius:42px;padding:20px 26px;box-shadow:0 9px 0 #A4B9BD}
.meta span{border:1px solid #173B50;border-radius:42px;background:#EEF7F7;color:#173B50;box-shadow:0 4px 0 #A4B9BD}
.a1{width:220px;height:90px;background:repeating-linear-gradient(0deg,transparent 0 12px,#E36B38 12px 16px);border-radius:60% 18px 18px 60%;transform:skewX(-18deg);top:12%;right:7%;animation:floaty 6s ease-in-out infinite}
.a2{width:130px;height:100px;background:#EEF7F7;border:6px solid #173B50;border-radius:70% 18px 18px 70%;box-shadow:10px 8px 0 #E36B38;bottom:14%;right:24%;animation:floaty 7s 1s ease-in-out infinite}
.sec h3{font-weight:700;letter-spacing:.12em;color:#173B50}
.prose{background:#EEF7F7;border:1px solid #A4B9BD;border-radius:24px;padding:30px;box-shadow:0 8px 0 rgba(23,59,80,.12)}
.chips li{border:1px solid #173B50;border-radius:42px;background:#E36B38;color:#fff;font-weight:700}
pre{background:#173B50;color:#CFE4EA;border-left:6px solid #E36B38}
.tl b{color:#E36B38;font-weight:700}
.hallnav a{border:2px solid #173B50;border-radius:42px;background:#EEF7F7;color:#173B50}
""",
'photomontage': """
body{background:#E2E0D8;color:#1B1B1B;font-family:Arial,Helvetica,sans-serif}
::selection{background:#D2372B;color:#F7F5ED}
.topbar{background:#F7F5ED;border-bottom:3px solid #1B1B1B;color:#1B1B1B}
.hero{background:linear-gradient(105deg,transparent 0 46%,rgba(210,55,43,.24) 47% 51%,transparent 52%),linear-gradient(160deg,transparent 0 50%,rgba(25,59,89,.12) 50% 74%,transparent 74%)}
.hero .big{font-weight:900;letter-spacing:-.08em;text-transform:uppercase}
.hero .en{color:#D2372B;letter-spacing:.2em;font-weight:900}
.hero .man{background:#F7F5ED;border:3px solid #1B1B1B;padding:18px 24px;transform:rotate(-1deg);box-shadow:8px 8px 0 #D2372B}
.meta span{border:2px solid #1B1B1B;border-radius:0;background:#F7F5ED;color:#1B1B1B;transform:rotate(1deg)}
.a1{width:190px;height:145px;background:linear-gradient(110deg,#193B59 0 31%,#E2E0D8 31% 48%,#D2372B 48% 68%,#222 68%);clip-path:polygon(2% 8%,45% 0,98% 12%,91% 90%,52% 100%,0 84%);border:4px solid #1B1B1B;top:9%;right:8%;animation:floaty 7s ease-in-out infinite}
.a2{width:130px;height:130px;background:#D2372B;border:5px solid #1B1B1B;clip-path:polygon(0 8%,72% 0,100% 22%,82% 68%,100% 100%,28% 84%,0 100%,16% 42%);bottom:13%;right:24%;animation:spin 12s linear infinite}
.sec h3{font-weight:900;letter-spacing:.05em;text-transform:uppercase}
.prose{background:#F7F5ED;border:3px solid #1B1B1B;padding:28px;transform:rotate(.5deg);box-shadow:10px 10px 0 rgba(210,55,43,.35)}
.chips li{border:2px solid #1B1B1B;border-radius:0;background:#D2372B;color:#F7F5ED;font-weight:900}
pre{background:#1B1B1B;color:#E2E0D8;border:4px solid #D2372B}
.tl b{color:#D2372B;font-weight:900}
.hallnav a{border:3px solid #1B1B1B;background:#F7F5ED;color:#1B1B1B;font-weight:700}
""",
'midcentury': """
body{background:#F2E9D8;color:#24333B;font-family:"Helvetica Neue",Arial,sans-serif}
::selection{background:#D65A38;color:#FFF9EC}
.topbar{background:#FFF9EC;border-bottom:2px solid #4E8B86;color:#24333B}
.hero{background:radial-gradient(circle at 80% 18%,#E3B33B 0 7%,transparent 8%),linear-gradient(135deg,transparent 60%,rgba(36,51,59,.1) 60%)}
.hero .big{font-weight:700;letter-spacing:-.06em}
.hero .en{color:#D65A38;letter-spacing:.2em}
.hero .man{background:#FFF9EC;border:0;border-radius:18px;padding:20px 26px;box-shadow:10px 10px 0 #D98A45}
.meta span{border:0;border-radius:18px;background:#E3B33B;color:#24333B;box-shadow:0 5px 0 #D98A45;font-weight:700}
.a1{width:180px;height:180px;border-radius:50%;background:repeating-conic-gradient(from 8deg,transparent 0 10deg,#4E8B86 10deg 13deg,transparent 13deg 32deg),#E3B33B;box-shadow:0 0 0 8px #F2E9D8;top:9%;right:8%;animation:spin 16s linear infinite}
.a2{width:125px;height:100px;border-radius:58% 58% 18% 18%;background:#D65A38;box-shadow:12px 12px 0 #4E8B86;bottom:14%;right:24%;animation:floaty 7s ease-in-out infinite}
.sec h3{font-weight:700;letter-spacing:.04em;color:#4E8B86}
.prose{background:#FFF9EC;border-radius:18px;padding:30px;box-shadow:10px 10px 0 rgba(217,138,69,.5)}
.chips li{border:0;border-radius:18px;background:#4E8B86;color:#FFF9EC;box-shadow:0 4px 0 #D98A45}
pre{background:#24333B;color:#E3B33B;border-left:6px solid #D65A38}
.tl b{color:#D65A38;font-weight:700}
.hallnav a{border:0;border-radius:18px;background:#24333B;color:#FFF9EC;box-shadow:0 4px 0 #D98A45}
""",
'googie': """
body{background:#FF5A36;color:#FFF7D6;font-family:"Arial Black","Helvetica Neue",sans-serif}
::selection{background:#FFE600;color:#1C1740}
.topbar{background:#1C1740;border-bottom:4px solid #FFE600;color:#FFF7D6}
.hero{background:radial-gradient(circle at 80% 18%,#FFE600 0 9%,transparent 10%),repeating-linear-gradient(-12deg,transparent 0 24px,rgba(255,230,0,.22) 25px 29px)}
.hero .big{font-weight:900;letter-spacing:-.07em;text-transform:uppercase;text-shadow:6px 6px 0 #1C1740}
.hero .en{color:#FFE600;letter-spacing:.22em;font-weight:900}
.hero .man{background:#FFE600;color:#1C1740;border:5px solid #1C1740;border-radius:50% 50% 45% 45%;padding:18px 24px;transform:rotate(-4deg);box-shadow:10px 10px 0 #1C1740}
.meta span{border:3px solid #1C1740;border-radius:50%;background:#FFF7D6;color:#1C1740;font-weight:900}
.a1{width:180px;height:180px;background:#FFE600;clip-path:polygon(50% 0,61% 35%,96% 14%,70% 43%,100% 50%,69% 57%,90% 91%,58% 68%,50% 100%,41% 68%,9% 91%,31% 57%,0 50%,31% 43%,4% 14%,39% 35%);top:10%;right:8%;animation:spin 12s linear infinite}
.a2{width:130px;height:86px;background:#FFE600;border:6px solid #1C1740;border-radius:50% 50% 45% 45%;transform:rotate(-8deg);bottom:14%;right:24%;animation:floaty 6s ease-in-out infinite}
.sec h3{font-weight:900;color:#FFE600;letter-spacing:.08em;text-transform:uppercase}
.prose{background:#1C1740;border:4px solid #FFE600;padding:28px;box-shadow:10px 10px 0 #FFF7D6}
.chips li{border:3px solid #1C1740;border-radius:50%;background:#FFE600;color:#1C1740;font-weight:900}
pre{background:#1C1740;color:#FFE600;border:5px solid #FFF7D6}
.tl b{color:#FFE600;font-weight:900}
.hallnav a{border:4px solid #1C1740;background:#FFF7D6;color:#1C1740;font-weight:900}
""",
'atompunk': """
body{background:#183B56;color:#D9F2E6;font-family:"Trebuchet MS",Arial,sans-serif}
::selection{background:#F7D154;color:#183B56}
.topbar{background:#10283A;border-bottom:3px solid #F7D154;color:#D9F2E6}
.hero{background:radial-gradient(circle at 82% 20%,rgba(247,209,84,.3),transparent 24%),repeating-radial-gradient(circle at 18% 70%,transparent 0 30px,rgba(247,209,84,.12) 31px 33px)}
.hero .big{font-weight:800;letter-spacing:-.05em}
.hero .en{color:#F7D154;letter-spacing:.2em}
.hero .man{background:#244F69;border:3px solid #F7D154;padding:20px 24px;box-shadow:8px 8px 0 #FF7043}
.meta span{border:2px solid #F7D154;border-radius:0;background:#244F69;color:#D9F2E6}
.a1{width:190px;height:190px;border:8px double #F7D154;border-radius:50%;background:repeating-conic-gradient(transparent 0 14deg,#FF7043 15deg 18deg,transparent 19deg 30deg),#244F69;top:8%;right:8%;animation:spin 17s linear infinite}
.a2{width:125px;height:125px;background:#F7D154;border:7px solid #183B56;border-radius:50%;box-shadow:0 0 0 5px #FF7043;bottom:14%;right:24%;animation:floaty 7s ease-in-out infinite}
.sec h3{font-weight:800;color:#F7D154;letter-spacing:.08em}
.prose{background:#244F69;border:2px solid #F7D154;padding:30px;line-height:2}
.chips li{border:2px solid #F7D154;border-radius:0;background:#FF7043;color:#183B56;font-weight:700}
pre{background:#10283A;color:#F7D154;border:4px solid #FF7043}
.tl b{color:#F7D154;font-weight:800}
.hallnav a{border:2px solid #F7D154;background:#244F69;color:#D9F2E6}
""",
'blueprint': """
body{background:#0B3B6E;color:#D8F3FF;font-family:"Courier New",monospace}
::selection{background:#78D6F7;color:#0B3B6E}
.topbar{background:#082D55;border-bottom:1px solid #78D6F7;color:#D8F3FF}
.hero{background:linear-gradient(#2b6590 1px,transparent 1px),linear-gradient(90deg,#2b6590 1px,transparent 1px);background-size:24px 24px}
.hero .big{font-weight:700;letter-spacing:.05em}
.hero .en{color:#78D6F7;letter-spacing:.2em}
.hero .man{background:rgba(18,76,128,.8);border:2px solid #D8F3FF;padding:18px 24px;box-shadow:6px 6px 0 rgba(120,214,247,.25)}
.meta span{border:1px solid #D8F3FF;border-radius:0;background:#124C80;color:#D8F3FF;font-family:monospace}
.a1{width:190px;height:190px;border:2px solid #D8F3FF;background:repeating-linear-gradient(0deg,transparent 0 21px,rgba(216,243,255,.2) 22px),repeating-linear-gradient(90deg,transparent 0 21px,rgba(216,243,255,.2) 22px);top:8%;right:8%;animation:spin 20s linear infinite}
.a2{width:125px;height:125px;border:2px solid #78D6F7;background:transparent;clip-path:polygon(50% 0,100% 100%,0 100%);bottom:14%;right:24%;animation:floaty 7s ease-in-out infinite}
.sec h3{font-weight:700;color:#78D6F7;letter-spacing:.14em}
.prose{background:#124C80;border:1px solid #78D6F7;padding:30px;line-height:1.9}
.chips li{border:1px solid #D8F3FF;border-radius:0;background:#124C80;color:#D8F3FF;font-family:monospace}
pre{background:#082D55;color:#D8F3FF;border:2px solid #78D6F7}
.tl b{color:#78D6F7;font-weight:700}
.hallnav a{border:1px solid #D8F3FF;border-radius:0;background:#124C80;color:#D8F3FF}
""",
'pushpin': """
body{background:#F04D3A;color:#F7E7C6;font-family:Georgia,"Times New Roman",serif}
::selection{background:#E2B93B;color:#1C2340}
.topbar{background:#1C2340;border-bottom:4px solid #E2B93B;color:#F7E7C6}
.hero{background:linear-gradient(135deg,rgba(226,185,59,.25) 0 18%,transparent 18% 42%,rgba(46,140,131,.2) 42% 58%,transparent 58%),repeating-linear-gradient(-8deg,transparent 0 32px,rgba(28,35,64,.12) 33px 35px)}
.hero .big{font-weight:900;letter-spacing:-.06em;text-shadow:5px 5px 0 #1C2340}
.hero .en{color:#E2B93B;letter-spacing:.2em;font-weight:700}
.hero .man{background:#F7E7C6;color:#1C2340;border:4px solid #1C2340;padding:18px 24px;transform:rotate(-2deg);box-shadow:9px 9px 0 #E2B93B}
.meta span{border:2px solid #1C2340;border-radius:0;background:#2E8C83;color:#F7E7C6;transform:rotate(2deg)}
.a1{width:170px;height:130px;background:#E2B93B;clip-path:polygon(50% 0,61% 17%,82% 8%,83% 30%,100% 42%,84% 57%,92% 79%,68% 77%,50% 100%,34% 78%,8% 88%,16% 61%,0 45%,18% 31%,16% 8%,39% 17%);border:5px solid #1C2340;top:10%;right:8%;animation:floaty 6s ease-in-out infinite}
.a2{width:130px;height:100px;background:#2E8C83;border:6px solid #1C2340;transform:rotate(-7deg);bottom:14%;right:24%;animation:spin 14s linear infinite}
.sec h3{font-weight:900;color:#E2B93B;letter-spacing:.08em}
.prose{background:#F7E7C6;color:#1C2340;border:4px solid #1C2340;padding:28px;box-shadow:10px 10px 0 #E2B93B}
.chips li{border:3px solid #1C2340;border-radius:0;background:#2E8C83;color:#F7E7C6;font-weight:700}
pre{background:#1C2340;color:#E2B93B;border:4px solid #E2B93B}
.tl b{color:#E2B93B;font-weight:900}
.hallnav a{border:3px solid #1C2340;background:#F7E7C6;color:#1C2340;font-weight:700}
""",
'psychedelicposter': """
body{background:#5B1B9A;color:#F7FF00;font-family:Impact,"Arial Black",sans-serif}
::selection{background:#FF3BBE;color:#5B1B9A}
.topbar{background:#28105A;border-bottom:4px solid #21E6C1;color:#F7FF00}
.hero{background:repeating-radial-gradient(circle at 78% 24%,#F7FF00 0 10px,#FF3BBE 10px 20px,#21E6C1 20px 30px,#5B1B9A 30px 40px);background-size:260px 260px}
.hero .big{font-weight:900;letter-spacing:-.09em;transform:skewX(-8deg);text-shadow:4px 4px 0 #FF3BBE}
.hero .en{color:#21E6C1;letter-spacing:.12em;transform:skewX(-8deg)}
.hero .man{background:#28105A;border:4px solid #F7FF00;border-radius:48% 52% 44% 56%;padding:18px 24px;transform:skewX(-8deg)}
.meta span{border:2px solid #F7FF00;border-radius:50%;background:#FF3BBE;color:#5B1B9A;font-weight:900}
.a1{width:180px;height:180px;border-radius:50%;background:repeating-radial-gradient(circle,#F7FF00 0 8px,#FF3BBE 8px 16px,#21E6C1 16px 24px,#5B1B9A 24px 32px);border:5px solid #17152E;top:9%;right:8%;animation:spin 10s linear infinite}
.a2{width:130px;height:130px;background:#21E6C1;clip-path:polygon(50% 0,62% 36%,100% 50%,62% 64%,50% 100%,38% 64%,0 50%,38% 36%);bottom:14%;right:24%;animation:floaty 6s ease-in-out infinite}
.sec h3{font-weight:900;color:#21E6C1;letter-spacing:.06em}
.prose{background:#28105A;border:3px solid #F7FF00;border-radius:20px;padding:28px;line-height:1.8}
.chips li{border:2px solid #F7FF00;border-radius:50%;background:#FF3BBE;color:#5B1B9A;font-weight:900}
pre{background:#17152E;color:#F7FF00;border:4px solid #21E6C1}
.tl b{color:#FF3BBE;font-weight:900}
.hallnav a{border:3px solid #F7FF00;border-radius:99px;background:#28105A;color:#F7FF00}
""",
'punkxerox': """
body{background:#0B0B0D;color:#F2F0E6;font-family:"Courier New",monospace;filter:contrast(1.05)}
::selection{background:#D9F20B;color:#0B0B0D}
.topbar{background:#202026;border-bottom:3px dashed #D9F20B;color:#F2F0E6}
.hero{background:repeating-linear-gradient(0deg,rgba(242,240,230,.08) 0 2px,transparent 2px 6px),linear-gradient(14deg,transparent 0 46%,rgba(217,242,11,.2) 47% 52%,transparent 53%)}
.hero .big{font-weight:900;letter-spacing:-.08em;text-transform:uppercase;text-shadow:3px 3px 0 #D9F20B}
.hero .en{color:#D9F20B;letter-spacing:.08em}
.hero .man{background:#F2F0E6;color:#0B0B0D;border:3px solid #0B0B0D;padding:18px 24px;transform:rotate(-2deg);box-shadow:7px 7px 0 #D9F20B}
.meta span{border:2px dashed #F2F0E6;border-radius:0;background:#202026;color:#D9F20B;transform:rotate(2deg)}
.a1{width:185px;height:140px;background:#F2F0E6;border:5px solid #D9F20B;clip-path:polygon(0 8%,72% 0,100% 22%,82% 68%,100% 100%,28% 84%,0 100%,16% 42%);top:9%;right:8%;animation:floaty 5s ease-in-out infinite}
.a2{width:130px;height:130px;background:#D9F20B;border:4px solid #F2F0E6;transform:rotate(-8deg);bottom:14%;right:24%;animation:spin 11s linear infinite}
.sec h3{font-weight:900;color:#D9F20B;letter-spacing:.08em;text-transform:uppercase}
.prose{background:#F2F0E6;color:#0B0B0D;border:3px dashed #0B0B0D;padding:28px;transform:rotate(.5deg)}
.chips li{border:2px dashed #F2F0E6;border-radius:0;background:#D9F20B;color:#0B0B0D;font-weight:900}
pre{background:#202026;color:#D9F20B;border:4px solid #F2F0E6}
.tl b{color:#D9F20B;font-weight:900}
.hallnav a{border:3px dashed #F2F0E6;background:#202026;color:#D9F20B}
""",
'asciiart': """
body{background:#001B12;color:#B7FF6A;font-family:monospace}
::selection{background:#00FF9C;color:#001B12}
.topbar{background:#062A1C;border-bottom:1px solid #00FF9C;color:#B7FF6A}
.hero{background:repeating-linear-gradient(0deg,rgba(0,255,156,.08) 0 2px,transparent 2px 6px),radial-gradient(circle at 80% 20%,rgba(0,255,156,.2),transparent 30%)}
.hero .big{font-weight:700;letter-spacing:.04em;text-shadow:0 0 10px #00FF9C}
.hero .en{color:#00FF9C;letter-spacing:.16em}
.hero .man{background:#062A1C;border:1px solid #00FF9C;padding:18px 24px;box-shadow:0 0 18px rgba(0,255,156,.25)}
.meta span{border:1px solid #00FF9C;border-radius:0;background:#062A1C;color:#B7FF6A;font-family:monospace}
.a1{width:190px;height:150px;border:2px solid #00FF9C;background:#062A1C;color:#B7FF6A;box-shadow:inset 0 0 20px rgba(0,255,156,.2);top:9%;right:8%;animation:floaty 7s ease-in-out infinite}
.a2{width:125px;height:125px;border:2px solid #B7FF6A;background:repeating-conic-gradient(#00FF9C 0 8deg,transparent 8deg 16deg);bottom:14%;right:24%;animation:spin 9s linear infinite}
.sec h3{font-weight:700;color:#00FF9C;letter-spacing:.1em}
.prose{background:#062A1C;border:1px solid #00FF9C;padding:28px;line-height:1.8}
.chips li{border:1px solid #00FF9C;border-radius:0;background:#062A1C;color:#B7FF6A;font-family:monospace}
pre{background:#000D09;color:#B7FF6A;border:2px solid #00FF9C;text-shadow:0 0 6px #00FF9C}
.tl b{color:#00FF9C;font-weight:700}
.hallnav a{border:1px solid #00FF9C;border-radius:0;background:#062A1C;color:#B7FF6A}
""",
'retrogui': """
body{background:#000080;color:#FFF;font-family:Arial,sans-serif}
::selection{background:#FFFF00;color:#000080}
.topbar{background:#C0C0C0;border-bottom:3px outset #fff;color:#000;font-size:12px}
.hero{background:repeating-linear-gradient(0deg,transparent 0 3px,rgba(255,255,255,.08) 3px 4px),#000080}
.hero .big{font-weight:900;letter-spacing:-.06em;text-shadow:2px 2px 0 #000}
.hero .en{color:#FFFF00;letter-spacing:.14em;font-weight:700}
.hero .man{background:#C0C0C0;color:#000;border:2px outset #fff;padding:16px 20px;box-shadow:3px 3px 0 #000}
.meta span{border:2px outset #fff;border-radius:0;background:#C0C0C0;color:#000;font-size:12px}
.a1{width:180px;height:140px;background:#C0C0C0;border:3px outset #fff;box-shadow:4px 4px 0 #000;top:9%;right:8%;animation:floaty 7s ease-in-out infinite}
.a2{width:120px;height:120px;background:#000080;border:4px inset #fff;box-shadow:3px 3px 0 #000;bottom:14%;right:24%;animation:spin 12s linear infinite}
.sec h3{font-weight:900;color:#FFFF00;font-size:18px}
.prose{background:#C0C0C0;color:#000;border:3px outset #fff;padding:24px;font-size:13px;box-shadow:4px 4px 0 #000}
.chips li{border:2px outset #fff;border-radius:0;background:#C0C0C0;color:#000;font-size:12px}
pre{background:#000;color:#00FF00;border:3px inset #fff}
.tl b{color:#FFFF00;font-weight:900}
.hallnav a{border:3px outset #fff;border-radius:0;background:#C0C0C0;color:#000;font-weight:700;font-size:12px}
""",
'lowpoly': """
body{background:#1B263B;color:#E0E1DD;font-family:"Segoe UI",Arial,sans-serif}
::selection{background:#FFB703;color:#1B263B}
.topbar{background:#101827;border-bottom:2px solid #415A77;color:#E0E1DD}
.hero{background:linear-gradient(135deg,rgba(65,90,119,.55) 0 30%,transparent 30% 52%,rgba(119,141,169,.3) 52% 74%,transparent 74%)}
.hero .big{font-weight:800;letter-spacing:-.06em}
.hero .en{color:#FFB703;letter-spacing:.18em}
.hero .man{background:#415A77;border:2px solid #778DA9;padding:20px 24px;clip-path:polygon(3% 0,100% 7%,96% 100%,0 93%)}
.meta span{border:1px solid #778DA9;border-radius:0;background:#415A77;color:#E0E1DD;clip-path:polygon(5% 0,100% 8%,94% 100%,0 92%)}
.a1{width:180px;height:180px;background:linear-gradient(135deg,#FFB703 0 33%,#FB8500 33% 58%,#219EBC 58% 78%,#8ECAE6 78%);clip-path:polygon(50% 0,92% 26%,82% 81%,50% 100%,14% 78%,5% 28%);top:9%;right:8%;animation:floaty 7s ease-in-out infinite}
.a2{width:130px;height:120px;background:linear-gradient(135deg,#778DA9 0 42%,#E0E1DD 42% 58%,#1B263B 58%);clip-path:polygon(0 88%,18% 52%,33% 70%,52% 22%,69% 62%,100% 40%,100% 100%,0 100%);bottom:14%;right:24%;animation:spin 15s linear infinite}
.sec h3{font-weight:800;color:#FFB703;letter-spacing:.06em}
.prose{background:#415A77;border:1px solid #778DA9;padding:30px;clip-path:polygon(1% 0,100% 4%,98% 100%,0 96%)}
.chips li{border:1px solid #778DA9;border-radius:0;background:#219EBC;color:#E0E1DD;clip-path:polygon(4% 0,100% 8%,94% 100%,0 92%)}
pre{background:#101827;color:#8ECAE6;border:3px solid #FFB703}
.tl b{color:#FFB703;font-weight:800}
.hallnav a{border:2px solid #778DA9;background:#415A77;color:#E0E1DD;clip-path:polygon(3% 0,100% 7%,96% 100%,0 93%)}
""",
'web1': """
body{background:#000080;color:#FFF;font-family:"Times New Roman",serif}
::selection{background:#FFFF00;color:#000080}
.topbar{background:#000040;border-bottom:3px solid #FFFF00;color:#FFF}
.hero{background:repeating-linear-gradient(0deg,transparent 0 20px,rgba(255,255,0,.12) 20px 22px),#000080}
.hero .big{font-weight:900;letter-spacing:-.05em;text-decoration:underline}
.hero .en{color:#FFFF00;letter-spacing:.12em;text-decoration:underline}
.hero .man{background:#F0F0F0;color:#000080;border:4px outset #fff;padding:16px 20px;font-weight:700}
.meta span{border:3px outset #fff;border-radius:0;background:#FFFF00;color:#000080;font-family:Arial,sans-serif}
.a1{width:180px;height:120px;background:#FFFF00;border:5px outset #fff;box-shadow:6px 6px 0 #000;top:9%;right:8%;animation:floaty 5s ease-in-out infinite}
.a2{width:125px;height:125px;background:#00FF00;border:4px inset #fff;color:#000080;bottom:14%;right:24%;animation:spin 8s linear infinite}
.sec h3{font-weight:900;color:#FFFF00;text-decoration:underline}
.prose{background:#F0F0F0;color:#000080;border:4px outset #fff;padding:24px;line-height:1.6}
.chips li{border:3px outset #fff;border-radius:0;background:#FFFF00;color:#000080;font-weight:700;text-decoration:underline}
pre{background:#000;color:#00FF00;border:4px inset #fff}
.tl b{color:#FFFF00;font-weight:900}
.hallnav a{border:4px outset #fff;border-radius:0;background:#F0F0F0;color:#000080;font-weight:700}
""",
'web2gloss': """
body{background:#0B5FA5;color:#FFF;font-family:"Helvetica Neue",Arial,sans-serif}
::selection{background:#FF75B5;color:#fff}
.topbar{background:linear-gradient(#5CB8F2,#0B5FA5);border-bottom:2px solid #07528F;box-shadow:0 3px 8px rgba(0,0,0,.3)}
.hero{background:radial-gradient(ellipse at 50% 0,#fff6 0 10%,transparent 40%),linear-gradient(180deg,#168DE2,#0B5FA5)}
.hero .big{font-weight:800;letter-spacing:-.05em;text-shadow:0 2px 3px #07528F}
.hero .en{color:#FFB6E6;letter-spacing:.2em;font-weight:700}
.hero .man{background:linear-gradient(180deg,#fff,#B8E6FF 25%,#168DE2);color:#07528F;border:1px solid #07528F;border-radius:14px;padding:18px 24px;box-shadow:inset 0 2px #fff,0 7px 12px #00408066}
.meta span{border:1px solid #fff;border-radius:99px;background:linear-gradient(#FFB6E6,#FF6BA8);color:#07528F;box-shadow:inset 0 2px #fff,0 3px 7px #004080}
.a1{width:190px;height:145px;border-radius:50%;background:linear-gradient(180deg,#fff,#8ED6FF 22%,#168DE2);border:1px solid #fff;box-shadow:inset 0 2px #fff,0 8px 16px #00408099;top:8%;right:8%;animation:floaty 7s ease-in-out infinite}
.a2{width:125px;height:125px;border-radius:99px;background:linear-gradient(135deg,#FFB6E6,#FF6BA8);border:4px solid #fff;box-shadow:0 0 0 2px #D83B8A,0 7px 14px #00408099;bottom:14%;right:24%;animation:spin 12s linear infinite}
.sec h3{font-weight:800;color:#FFB6E6;text-shadow:0 2px 2px #07528F}
.prose{background:rgba(255,255,255,.18);border:1px solid #fff;border-radius:14px;padding:30px;box-shadow:inset 0 1px #fff,0 7px 14px #00408066}
.chips li{border:1px solid #fff;border-radius:99px;background:linear-gradient(#fff,#8ED6FF);color:#07528F;box-shadow:inset 0 2px #fff,0 4px 8px #00408066}
pre{background:#07528F;color:#BDEBFF;border:2px solid #FF75B5;border-radius:9px;box-shadow:inset 0 2px #0004}
.tl b{color:#FF75B5;font-weight:800}
.hallnav a{border:1px solid #fff;border-radius:99px;background:linear-gradient(#5CB8F2,#0B5FA5);color:#fff;box-shadow:inset 0 1px #fff,0 4px 8px #00408066}
""",
'glitchart': """
body{background:#0D0D18;color:#F4F4FF;font-family:Arial,Helvetica,sans-serif;filter:contrast(1.08)}
::selection{background:#FF3864;color:#0D0D18}
.topbar{background:#141425;border-bottom:2px solid #00E5FF;color:#F4F4FF}
.hero{background:repeating-linear-gradient(0deg,rgba(255,255,255,.1) 0 2px,transparent 2px 6px),linear-gradient(105deg,#24104F 0 27%,#FF3864 27% 44%,#08D9FF 44% 69%,#141425 69%)}
.hero .big{font-weight:900;letter-spacing:-.08em;text-shadow:-5px 0 #FF1744,5px 0 #00E5FF;transform:skewX(-8deg)}
.hero .en{color:#00E5FF;letter-spacing:.16em;text-shadow:2px 0 #FF1744}
.hero .man{background:#1C1B31;border:2px solid #FF3864;padding:18px 24px;box-shadow:5px 0 #00E5FF,-5px 0 #FF1744}
.meta span{border:1px solid #00E5FF;border-radius:0;background:#1C1B31;color:#F4F4FF;text-shadow:2px 0 #FF1744}
.a1{width:200px;height:130px;background:repeating-linear-gradient(0deg,rgba(255,255,255,.18) 0 2px,transparent 2px 6px),linear-gradient(105deg,#24104F 0 27%,#FF3864 27% 44%,#08D9FF 44% 69%,#141425 69%);border:3px solid #00E5FF;top:8%;right:8%;animation:floaty 5s steps(3) infinite}
.a2{width:130px;height:130px;background:#FF3864;border:4px solid #00E5FF;clip-path:polygon(0 8%,72% 0,100% 22%,82% 68%,100% 100%,28% 84%,0 100%,16% 42%);bottom:14%;right:24%;animation:spin 8s steps(8) infinite}
.sec h3{font-weight:900;color:#00E5FF;text-shadow:3px 0 #FF1744}
.prose{background:#1C1B31;border:1px solid #FF3864;padding:28px;box-shadow:5px 0 #00E5FF,-5px 0 #FF1744}
.chips li{border:1px solid #00E5FF;border-radius:0;background:#FF3864;color:#0D0D18;font-weight:900}
pre{background:#080810;color:#00E5FF;border:3px solid #FF3864;text-shadow:2px 0 #FF1744}
.tl b{color:#FF3864;font-weight:900}
.hallnav a{border:2px solid #00E5FF;background:#1C1B31;color:#F4F4FF;text-shadow:2px 0 #FF1744}
""",
'synthwave': """
body{background:#18083B;color:#FFE8FA;font-family:"Arial Black","Helvetica Neue",sans-serif}
::selection{background:#FF3CA6;color:#18083B}
.topbar{background:#32105F;border-bottom:2px solid #FF3CA6;color:#FFE8FA}
.hero{background:linear-gradient(180deg,#12062F 0%,#3D126B 55%,#FF4D9D 100%);background-size:100% 180%}
.hero .big{font-weight:900;font-style:italic;letter-spacing:-.08em;background:linear-gradient(180deg,#fff,#A4B5FF 35%,#FF5CB8 52%,#4B1E92);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero .en{color:#FF3CA6;letter-spacing:.22em;text-shadow:0 0 10px #FF3CA6}
.hero .man{background:rgba(50,16,95,.82);border:2px solid #FF3CA6;padding:18px 24px;box-shadow:0 0 22px rgba(255,60,166,.35)}
.meta span{border:1px solid #FF3CA6;border-radius:99px;background:#32105F;color:#FFE8FA;box-shadow:0 0 10px #FF3CA655}
.a1{width:190px;height:190px;border-radius:50%;background:linear-gradient(#FFD166 0 38%,#FF4D9D 39% 48%,#7A2EFF 49%);box-shadow:0 0 25px #FF3CA6,0 0 55px #FF3CA699;top:9%;right:8%;animation:floaty 6s ease-in-out infinite}
.a2{width:150px;height:95px;background:repeating-linear-gradient(0deg,transparent 0 10px,#FF34B4 10px 12px),linear-gradient(90deg,#29105E,#08D9FF);transform:perspective(180px) rotateX(55deg);bottom:14%;right:22%;animation:floaty 7s 1s ease-in-out infinite}
.sec h3{font-weight:900;color:#FF3CA6;letter-spacing:.1em;text-shadow:0 0 9px #FF3CA6}
.prose{background:rgba(50,16,95,.78);border:1px solid #FF3CA6;padding:30px;box-shadow:0 0 24px #FF3CA633}
.chips li{border:1px solid #FF3CA6;border-radius:99px;background:#32105F;color:#FFE8FA;box-shadow:0 0 10px #FF3CA633}
pre{background:#0C0522;color:#A4B5FF;border:2px solid #FF3CA6;box-shadow:0 0 14px #FF3CA644}
.tl b{color:#FF3CA6;font-weight:900}
.hallnav a{border:1px solid #FF3CA6;border-radius:99px;background:#32105F;color:#FFE8FA;box-shadow:0 0 10px #FF3CA633}
""",
'steampunk': """
body{background:#2B1D14;color:#F2D6A2;font-family:Georgia,"Times New Roman",serif}
::selection{background:#C58A3B;color:#2B1D14}
.topbar{background:#3B291C;border-bottom:5px solid #9A672A;color:#F2D6A2}
.hero{background:radial-gradient(circle at 80% 20%,rgba(200,138,59,.4),transparent 25%),repeating-linear-gradient(45deg,rgba(241,210,154,.06) 0 2px,transparent 2px 16px)}
.hero .big{font-weight:700;letter-spacing:-.04em}
.hero .en{color:#C58A3B;letter-spacing:.18em;font-variant:small-caps}
.hero .man{background:#3B291C;border:6px solid #9A672A;padding:18px 24px;box-shadow:inset 0 0 0 3px #F1D29A,0 7px 14px #111}
.meta span{border:2px solid #C58A3B;border-radius:0;background:#3B291C;color:#F2D6A2;box-shadow:inset 0 0 0 2px #6F461E}
.a1{width:170px;height:170px;border:14px dotted #C58A3B;border-radius:50%;background:radial-gradient(circle,#4A2D18 0 14%,#D0A24B 15% 21%,#6F461E 22% 29%,#B8792C 30%);top:8%;right:8%;animation:spin 10s linear infinite}
.a2{width:125px;height:125px;border:8px solid #9A672A;border-radius:50%;background:conic-gradient(from 220deg,#6C3024 0 24%,#E2A83B 24% 30%,#3B291C 30% 100%);bottom:14%;right:24%;animation:floaty 7s ease-in-out infinite}
.sec h3{font-weight:700;color:#C58A3B;letter-spacing:.1em}
.prose{background:#3B291C;border:4px double #C58A3B;padding:28px;box-shadow:inset 0 0 0 3px #F1D29A}
.chips li{border:2px solid #C58A3B;border-radius:0;background:#6F461E;color:#F2D6A2}
pre{background:#1A100B;color:#F1D29A;border:5px solid #9A672A}
.tl b{color:#C58A3B;font-weight:700}
.hallnav a{border:3px double #C58A3B;background:#3B291C;color:#F2D6A2}
""",
'dieselpunk': """
body{background:#24221F;color:#E8D8B4;font-family:Arial,"Helvetica Neue",sans-serif;filter:sepia(.12)}
::selection{background:#C75C32;color:#24221F}
.topbar{background:#38332E;border-bottom:4px double #E8D8B4;color:#E8D8B4}
.hero{background:linear-gradient(135deg,rgba(199,92,50,.45),transparent 52%),repeating-linear-gradient(45deg,transparent 0 20px,rgba(232,216,180,.08) 20px 22px)}
.hero .big{font-weight:900;letter-spacing:.02em;text-transform:uppercase}
.hero .en{color:#C75C32;letter-spacing:.18em;font-weight:700}
.hero .man{background:#38332E;border:4px double #E8D8B4;padding:18px 24px;box-shadow:8px 8px 0 #161514}
.meta span{border:2px double #E8D8B4;border-radius:0;background:#38332E;color:#E8D8B4}
.a1{width:180px;height:180px;border:7px double #C75C32;border-radius:50%;background:repeating-conic-gradient(transparent 0 20deg,#78907A 21deg 25deg),#292723;top:9%;right:8%;animation:spin 18s linear infinite}
.a2{width:125px;height:95px;background:linear-gradient(135deg,#C75C32,#6F2F26);border:4px double #E8D8B4;box-shadow:7px 7px 0 #161514;bottom:14%;right:24%;animation:floaty 6s ease-in-out infinite}
.sec h3{font-weight:900;color:#C75C32;letter-spacing:.12em;text-transform:uppercase}
.prose{background:#38332E;border:3px double #E8D8B4;padding:28px;box-shadow:8px 8px 0 #161514}
.chips li{border:2px double #E8D8B4;border-radius:0;background:#C75C32;color:#24221F;font-weight:700}
pre{background:#161514;color:#E8D8B4;border:4px solid #C75C32}
.tl b{color:#C75C32;font-weight:900}
.hallnav a{border:3px double #E8D8B4;background:#38332E;color:#E8D8B4}
""",
'solarpunk': """
body{background:#E6F2C7;color:#23412D;font-family:"Trebuchet MS",Arial,sans-serif}
::selection{background:#F4A261;color:#23412D}
.topbar{background:#F9FFF3;border-bottom:2px solid #2F6947;color:#23412D}
.hero{background:radial-gradient(circle at 82% 18%,rgba(247,214,91,.65),transparent 22%),linear-gradient(145deg,rgba(88,183,122,.25),transparent 55%)}
.hero .big{font-weight:800;letter-spacing:-.05em;color:#2F6947}
.hero .en{color:#D8783F;letter-spacing:.2em}
.hero .man{background:#F9FFF3;border:2px solid #2F6947;border-radius:18px;padding:20px 24px;box-shadow:0 8px 0 #2F6947}
.meta span{border:1px solid #2F6947;border-radius:99px;background:#D9F2B4;color:#23412D}
.a1{width:180px;height:180px;border-radius:65% 35% 65% 35%;background:linear-gradient(135deg,#F7D65B 0 18%,#58B77A 19% 100%);transform:rotate(-38deg);box-shadow:0 0 24px rgba(247,214,91,.7);top:9%;right:8%;animation:floaty 6s ease-in-out infinite}
.a2{width:130px;height:130px;border:3px solid #2F6947;border-radius:50%;background:radial-gradient(circle,#F7D65B 0 10%,#58B77A 11% 55%,#D9F2B4 56%);bottom:14%;right:24%;animation:spin 15s linear infinite}
.sec h3{font-weight:800;color:#2F6947;letter-spacing:.08em}
.prose{background:#F9FFF3;border:1px solid #A7CF8B;border-left:6px solid #58B77A;border-radius:14px;padding:30px;line-height:2}
.chips li{border:1px solid #2F6947;border-radius:99px;background:#D9F2B4;color:#23412D}
pre{background:#23412D;color:#D9F2B4;border:3px solid #F4A261}
.tl b{color:#D8783F;font-weight:800}
.hallnav a{border:1px solid #2F6947;border-radius:99px;background:#F9FFF3;color:#23412D}
""",
'corpmemphis': """
body{background:#F7F0E7;color:#1E2440;font-family:"Arial Rounded MT Bold","Trebuchet MS",Arial,sans-serif}
::selection{background:#FF6B6B;color:#fff}
.topbar{background:#fff;border-bottom:2px solid #1E2440;color:#1E2440}
.hero{background:radial-gradient(circle at 16% 24%,#FFCF56 0 6%,transparent 7%),linear-gradient(135deg,transparent 0 68%,rgba(93,95,239,.18) 68%),linear-gradient(45deg,transparent 0 52%,rgba(0,180,170,.18) 52%)}
.hero .big{font-weight:900;letter-spacing:-.07em;color:#5D5FEF}
.hero .en{color:#FF6B6B;letter-spacing:.16em}
.hero .man{background:#fff;border:0;border-radius:44% 56% 62% 38%;padding:20px 24px;box-shadow:16px 12px 0 -7px #FFCF56}
.meta span{border:0;border-radius:99px;background:#5D5FEF;color:#fff;font-weight:700;box-shadow:0 5px 0 #1E2440}
.a1{width:170px;height:140px;background:#FF6B6B;border-radius:48% 52% 40% 60%;transform:rotate(-10deg);box-shadow:28px 20px 0 -10px #5D5FEF,38px 24px 0 -13px #FFCF56;top:9%;right:8%;animation:floaty 7s ease-in-out infinite}
.a2{width:130px;height:110px;background:#00B4AA;border-radius:44% 56% 62% 38%;box-shadow:24px -14px 0 -8px #5D5FEF,-28px 20px 0 -12px #FFCF56;bottom:14%;right:24%;animation:spin 14s linear infinite}
.sec h3{font-weight:900;color:#5D5FEF;letter-spacing:.04em}
.prose{background:#fff;border:0;border-radius:28px;padding:30px;box-shadow:14px 12px 0 -5px #FFCF56}
.chips li{border:0;border-radius:99px;background:#FF6B6B;color:#fff;font-weight:700;box-shadow:0 5px 0 #1E2440}
pre{background:#1E2440;color:#FFCF56;border-radius:18px;box-shadow:8px 8px 0 #5D5FEF}
.tl b{color:#FF6B6B;font-weight:900}
.hallnav a{border:0;border-radius:99px;background:#5D5FEF;color:#fff;box-shadow:0 5px 0 #1E2440}
""",
'dreamcore': """
body{background:#686FA8;color:#FFF2FC;font-family:"Trebuchet MS","Helvetica Neue",sans-serif}
::selection{background:#FFB7D5;color:#322C70}
.topbar{background:rgba(32,28,72,.55);border-bottom:1px solid rgba(255,255,255,.45);backdrop-filter:blur(8px);color:#FFF2FC}
.hero{background:linear-gradient(135deg,rgba(116,125,181,.35),rgba(255,183,213,.3)),radial-gradient(circle at 80% 20%,rgba(255,255,255,.25),transparent 28%)}
.hero .big{font-weight:500;letter-spacing:-.06em;text-shadow:0 0 12px #FFB7D5}
.hero .en{color:#FFB7D5;letter-spacing:.2em}
.hero .man{background:rgba(32,28,72,.66);border:1px solid rgba(255,255,255,.5);padding:20px 24px;box-shadow:0 0 30px rgba(255,210,237,.45)}
.meta span{border:1px solid rgba(255,255,255,.55);border-radius:99px;background:rgba(255,255,255,.16);color:#FFF2FC;backdrop-filter:blur(8px)}
.a1{width:200px;height:140px;background:linear-gradient(90deg,#747DB5 0 13%,#D5C7E9 13% 22%,#9BA7DC 22% 31%,#EEE0D1 31% 68%,#A1ACDC 68% 78%,#747DB5 78%);border:8px solid rgba(255,255,255,.42);box-shadow:0 0 35px rgba(255,210,237,.65);filter:blur(.2px);top:8%;right:8%;animation:floaty 8s ease-in-out infinite}
.a2{width:130px;height:100px;background:rgba(32,28,72,.66);border:1px solid rgba(255,255,255,.5);color:#FFF2FC;box-shadow:0 0 22px #FFB7D555;bottom:14%;right:24%;animation:spin 17s linear infinite}
.sec h3{font-weight:600;color:#FFB7D5;letter-spacing:.08em}
.prose{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.35);border-radius:18px;padding:30px;line-height:2;backdrop-filter:blur(8px)}
.chips li{border:1px solid rgba(255,255,255,.45);border-radius:99px;background:rgba(255,255,255,.15);color:#FFF2FC}
pre{background:#201C48;color:#FFB7D5;border:1px solid rgba(255,255,255,.4)}
.tl b{color:#FFB7D5;font-weight:600}
.hallnav a{border:1px solid rgba(255,255,255,.5);border-radius:99px;background:rgba(32,28,72,.6);color:#FFF2FC}
""",
'weirdcore': """
body{background:#191625;color:#F6F0FF;font-family:Arial,Helvetica,sans-serif;filter:contrast(1.08)}
::selection{background:#D6FF00;color:#191625}
.topbar{background:#2A2238;border-bottom:3px solid #D6FF00;color:#F6F0FF}
.hero{background:repeating-linear-gradient(0deg,rgba(255,255,255,.1) 0 2px,transparent 2px 7px),radial-gradient(circle at 80% 20%,rgba(214,255,0,.24),transparent 25%)}
.hero .big{font-weight:900;letter-spacing:-.08em;text-shadow:5px 5px 0 #FF4F9A;transform:rotate(-1deg)}
.hero .en{color:#D6FF00;letter-spacing:.15em}
.hero .man{background:#2A2238;border:2px solid #D6FF00;padding:18px 24px;box-shadow:6px 6px 0 #FF4F9A;transform:rotate(1deg)}
.meta span{border:2px solid #D6FF00;border-radius:50%;background:#2A2238;color:#F6F0FF;transform:rotate(-2deg)}
.a1{width:180px;height:130px;border-radius:50% 50% 45% 55%;background:#F1EBD7;border:4px solid #292238;box-shadow:0 0 0 6px #D6FF00;top:9%;right:8%;animation:floaty 5s ease-in-out infinite}
.a2{width:125px;height:125px;background:#D6FF00;border:4px solid #292238;clip-path:polygon(50% 0,60% 38%,100% 50%,60% 62%,50% 100%,40% 62%,0 50%,40% 38%);bottom:14%;right:24%;animation:spin 9s steps(9) infinite}
.sec h3{font-weight:900;color:#D6FF00;text-shadow:4px 4px 0 #FF4F9A}
.prose{background:#2A2238;border:2px solid #D6FF00;padding:28px;box-shadow:5px 5px 0 #FF4F9A}
.chips li{border:2px solid #D6FF00;border-radius:0;background:#FF4F9A;color:#191625;font-weight:900}
pre{background:#0F0C18;color:#D6FF00;border:3px solid #FF4F9A}
.tl b{color:#D6FF00;font-weight:900}
.hallnav a{border:2px solid #D6FF00;background:#2A2238;color:#F6F0FF;box-shadow:3px 3px 0 #FF4F9A}
""",
'liminal': """
body{background:#C5C8D2;color:#252733;font-family:"Helvetica Neue",Arial,sans-serif;filter:saturate(.75)}
::selection{background:#D6AF70;color:#252733}
.topbar{background:#DBDDE3;border-bottom:2px solid #6F7480;color:#252733}
.hero{background:linear-gradient(90deg,#9A9DAA 0 7%,#EEEBDD 7% 12%,#A9ACB8 12% 18%,#EEEBDD 18% 82%,#A9ACB8 82% 88%,#EEEBDD 88% 93%,#9A9DAA 93%)}
.hero .big{font-weight:400;letter-spacing:-.05em}
.hero .en{color:#6F7480;letter-spacing:.22em}
.hero .man{background:#DBDDE3;border:8px solid #6F7480;padding:18px 24px;box-shadow:inset 0 0 26px rgba(66,71,85,.3),0 8px 12px rgba(0,0,0,.2)}
.meta span{border:1px solid #6F7480;border-radius:0;background:#EEEBDD;color:#252733}
.a1{width:190px;height:112px;background:#EEEBDD;border:8px solid #6F7480;box-shadow:inset 0 0 26px rgba(66,71,85,.4),0 8px 12px rgba(0,0,0,.25);top:9%;right:8%;animation:floaty 8s steps(2) infinite}
.a2{width:85px;height:130px;background:linear-gradient(90deg,#6A4B3B,#B07B56 48%,#553A30);border:6px solid #302A2C;color:#F4E3C3;bottom:14%;right:24%;animation:spin 19s linear infinite}
.sec h3{font-weight:500;color:#6F7480;letter-spacing:.1em}
.prose{background:#DBDDE3;border:1px solid #9A9DAA;padding:30px;box-shadow:inset 0 0 22px rgba(66,71,85,.16),0 8px 12px rgba(0,0,0,.16)}
.chips li{border:1px solid #6F7480;border-radius:0;background:#EEEBDD;color:#252733}
pre{background:#252733;color:#EEEBDD;border:3px solid #D6AF70}
.tl b{color:#8D7041;font-weight:700}
.hallnav a{border:1px solid #6F7480;background:#DBDDE3;color:#252733}
""",
'darkacademia': """
body{background:#211A1A;color:#F2E9D8;font-family:Georgia,"Songti SC",serif}
::selection{background:#B58B57;color:#211A1A}
.topbar{background:#332522;border-bottom:3px solid #B58B57;color:#F2E9D8}
.hero{background:radial-gradient(ellipse at 80% 20%,rgba(181,139,87,.25),transparent 24%),linear-gradient(90deg,transparent 0 78%,rgba(0,0,0,.25) 100%)}
.hero .big{font-weight:500;letter-spacing:-.05em}
.hero .en{color:#B58B57;letter-spacing:.18em;font-style:italic}
.hero .man{background:#332522;border-left:4px solid #B58B57;padding:20px 24px;box-shadow:0 18px 40px rgba(0,0,0,.35)}
.meta span{border:1px solid #B58B57;border-radius:0;background:#332522;color:#F2E9D8}
.a1{width:180px;height:180px;border:2px solid #B58B57;border-radius:50%;background:radial-gradient(circle at 50% 42%,#FFE6A3 0 9%,#C9984A 10% 18%,#5A402B 19% 24%,transparent 25%),#211A1A;box-shadow:0 0 18px rgba(181,139,87,.6);top:8%;right:8%;animation:floaty 7s ease-in-out infinite}
.a2{width:130px;height:100px;background:#E7D7B8;color:#30231F;border-left:6px solid #9A714D;box-shadow:8px 8px 0 rgba(0,0,0,.28);transform:rotate(-3deg);bottom:14%;right:24%;animation:spin 16s linear infinite}
.sec h3{font-weight:500;color:#B58B57;letter-spacing:.12em}
.prose{background:#332522;border:1px solid #5A402B;border-left:4px solid #B58B57;padding:30px;line-height:2}
.chips li{border:1px solid #B58B57;border-radius:0;background:#5A402B;color:#F2E9D8}
pre{background:#171212;color:#E7D7B8;border:3px solid #B58B57}
.tl b{color:#B58B57;font-weight:700}
.hallnav a{border:1px solid #B58B57;background:#332522;color:#F2E9D8}
""",
'cottagecore': """
body{background:#F2E8D5;color:#4F604B;font-family:Georgia,"Times New Roman",serif}
::selection{background:#B66B61;color:#FFF8E7}
.topbar{background:#FFF8E7;border-bottom:2px solid #B9C8A2;color:#4F604B}
.hero{background:repeating-linear-gradient(90deg,rgba(190,109,96,.16) 0 2px,transparent 2px 28px),radial-gradient(circle at 80% 20%,rgba(185,200,162,.38),transparent 28%)}
.hero .big{font-weight:500;letter-spacing:-.04em;color:#5C694D}
.hero .en{color:#B66B61;letter-spacing:.18em;font-style:italic}
.hero .man{background:#FFF8E7;border:1px solid #B9C8A2;border-radius:2px 18px 3px 12px;padding:20px 24px;box-shadow:0 8px 0 #B9C8A2}
.meta span{border:1px solid #B66B61;border-radius:18px;background:#F8E7C4;color:#4F604B}
.a1{width:180px;height:140px;border-radius:55% 45% 48% 52%;background:radial-gradient(circle at 50% 44%,#F6C453 0 8%,transparent 9%),radial-gradient(ellipse at 30% 35%,#E9979A 0 16%,transparent 17%),radial-gradient(ellipse at 72% 52%,#8DB39E 0 15%,transparent 16%),#FFF8E7;top:9%;right:8%;animation:floaty 7s ease-in-out infinite}
.a2{width:130px;height:110px;background:#F8E7C4;border:8px solid #F6EFD8;box-shadow:0 7px 0 #B9C8A2;transform:rotate(3deg);bottom:14%;right:24%;animation:spin 15s linear infinite}
.sec h3{font-weight:500;color:#B66B61;letter-spacing:.08em}
.prose{background:#FFF8E7;border:1px solid #D5BFA2;border-radius:2px 18px 3px 12px;padding:30px;line-height:2}
.chips li{border:1px solid #B9C8A2;border-radius:18px;background:#F8E7C4;color:#4F604B}
pre{background:#4F604B;color:#F2E8D5;border-left:5px solid #B66B61}
.tl b{color:#B66B61;font-weight:700}
.hallnav a{border:1px solid #B9C8A2;border-radius:18px;background:#FFF8E7;color:#4F604B}
""",
'materialdesign': """
body{background:#F5F7FA;color:#263238;font-family:Roboto,"Helvetica Neue",Arial,sans-serif}
::selection{background:#6200EE;color:#fff}
.topbar{background:#fff;border-bottom:1px solid #E0E3E7;box-shadow:0 3px 8px rgba(38,50,56,.16);color:#263238}
.hero{background:radial-gradient(circle at 80% 20%,rgba(98,0,238,.14),transparent 25%),linear-gradient(135deg,#fff,transparent 68%)}
.hero .big{font-weight:700;letter-spacing:-.05em}
.hero .en{color:#6200EE;letter-spacing:.18em;font-weight:500}
.hero .man{background:#fff;border-radius:4px;padding:20px 24px;box-shadow:0 6px 12px rgba(0,0,0,.24)}
.meta span{border:0;border-radius:4px;background:#EDE7F6;color:#6200EE;box-shadow:0 3px 6px rgba(38,50,56,.18)}
.a1{width:180px;height:180px;border-radius:4px;background:#6200EE;box-shadow:0 8px 18px rgba(98,0,238,.35);top:9%;right:8%;animation:floaty 7s ease-in-out infinite}
.a2{width:125px;height:125px;border-radius:50%;background:#03DAC6;box-shadow:0 6px 12px rgba(38,50,56,.24);bottom:14%;right:24%;animation:spin 13s linear infinite}
.sec h3{font-weight:600;color:#6200EE;letter-spacing:.05em}
.prose{background:#fff;border-radius:4px;padding:30px;box-shadow:0 6px 12px rgba(0,0,0,.18)}
.chips li{border:0;border-radius:4px;background:#EDE7F6;color:#6200EE;box-shadow:0 3px 6px rgba(0,0,0,.16)}
pre{background:#263238;color:#B2DFDB;border-radius:4px;box-shadow:0 4px 8px rgba(0,0,0,.2)}
.tl b{color:#6200EE;font-weight:700}
.hallnav a{border:0;border-radius:4px;background:#6200EE;color:#fff;box-shadow:0 4px 8px rgba(0,0,0,.2)}
""",
'metro': """
body{background:#1A1A1A;color:#FFF;font-family:"Segoe UI",Arial,sans-serif}
::selection{background:#00A4EF;color:#1A1A1A}
.topbar{background:#111;border-bottom:2px solid #00A4EF;color:#FFF}
.hero{background:linear-gradient(90deg,transparent 0 62%,#00A4EF 62% 75%,transparent 75%),linear-gradient(0deg,transparent 0 60%,rgba(242,80,34,.5) 60% 72%,transparent 72%)}
.hero .big{font-weight:300;letter-spacing:-.08em;font-size:clamp(44px,9vw,96px)}
.hero .en{color:#00A4EF;letter-spacing:.15em;font-weight:300}
.hero .man{background:#252525;border-left:5px solid #00A4EF;padding:18px 24px;font-weight:300}
.meta span{border:0;border-radius:0;background:#00A4EF;color:#fff;font-weight:700}
.a1{width:190px;height:130px;background:#00A4EF;box-shadow:0 0 0 8px #7FBA00,0 0 0 16px #F25022;top:9%;right:8%;animation:floaty 7s ease-in-out infinite}
.a2{width:125px;height:125px;background:#F25022;clip-path:polygon(0 0,100% 0,100% 100%,0 100%);transform:rotate(45deg);bottom:14%;right:24%;animation:spin 12s linear infinite}
.sec h3{font-weight:300;color:#00A4EF;letter-spacing:.04em}
.prose{background:#252525;border-left:5px solid #7FBA00;padding:30px;line-height:1.9}
.chips li{border:0;border-radius:0;background:#7FBA00;color:#1A1A1A;font-weight:700}
pre{background:#111;color:#00A4EF;border-left:5px solid #F25022}
.tl b{color:#00A4EF;font-weight:700}
.hallnav a{border:0;border-radius:0;background:#00A4EF;color:#fff;font-weight:700}
""",
'kinetictypo': """
body{background:#111;color:#FFF;font-family:Arial,"Helvetica Neue",sans-serif}
::selection{background:#E7FF4F;color:#111}
.topbar{background:#1D1D1D;border-bottom:3px solid #E7FF4F;color:#FFF}
.hero{background:linear-gradient(110deg,transparent 0 35%,rgba(255,60,172,.25) 36% 52%,transparent 53%),repeating-linear-gradient(-12deg,transparent 0 38px,rgba(231,255,79,.12) 39px 43px)}
.hero .big{font-weight:900;letter-spacing:-.1em;text-transform:uppercase;transform:skewX(-7deg)}
.hero .en{color:#E7FF4F;letter-spacing:.2em;font-weight:800}
.hero .man{background:#1D1D1D;border:3px solid #E7FF4F;padding:18px 24px;box-shadow:6px 6px 0 #FF3CAC;transform:skewX(-5deg)}
.meta span{border:2px solid #E7FF4F;border-radius:0;background:#1D1D1D;color:#FFF;transform:skewX(-5deg)}
.a1{width:200px;height:100px;background:#E7FF4F;clip-path:polygon(0 30%,100% 0,82% 100%,0 70%);transform:skewX(-12deg);top:10%;right:8%;animation:floaty 4s ease-in-out infinite}
.a2{width:135px;height:135px;background:#FF3CAC;clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%);bottom:14%;right:24%;animation:spin 8s linear infinite}
.sec h3{font-weight:900;color:#E7FF4F;letter-spacing:.08em;text-transform:uppercase}
.prose{background:#1D1D1D;border:2px solid #FF3CAC;padding:28px;box-shadow:6px 6px 0 #E7FF4F}
.chips li{border:2px solid #E7FF4F;border-radius:0;background:#FF3CAC;color:#111;font-weight:900}
pre{background:#080808;color:#E7FF4F;border:3px solid #FF3CAC}
.tl b{color:#FF3CAC;font-weight:900}
.hallnav a{border:2px solid #E7FF4F;background:#1D1D1D;color:#FFF;transform:skewX(-5deg)}
""",
'holographic': """
body{background:#171327;color:#F7F4FF;font-family:"Helvetica Neue",Arial,sans-serif}
::selection{background:#B8FFF0;color:#281D3A}
.topbar{background:rgba(40,33,61,.86);border-bottom:1px solid #B8FFF0;backdrop-filter:blur(10px);color:#F7F4FF}
.hero{background:radial-gradient(circle at 18% 28%,rgba(255,120,200,.35),transparent 30%),conic-gradient(from 20deg,rgba(255,120,200,.16),rgba(255,230,109,.15),rgba(113,246,213,.18),rgba(124,155,255,.16),rgba(255,120,200,.16))}
.hero .big{font-weight:800;letter-spacing:-.06em;background:linear-gradient(120deg,#FF78C8,#FFE66D,#71F6D5,#7C9BFF);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero .en{color:#B8FFF0;letter-spacing:.22em}
.hero .man{background:rgba(40,33,61,.72);border:1px solid rgba(255,255,255,.7);border-radius:8px;padding:20px 24px;box-shadow:0 0 26px rgba(184,255,240,.3)}
.meta span{border:1px solid #B8FFF0;border-radius:99px;background:rgba(184,255,240,.12);color:#F7F4FF;backdrop-filter:blur(8px)}
.a1{width:190px;height:145px;border-radius:8px;background:linear-gradient(120deg,#FFB7E8,#B8FFF0 28%,#FFF59D 48%,#B8C8FF 72%,#FFB7E8);background-size:220% 220%;border:1px solid #fff;box-shadow:0 0 24px rgba(184,255,240,.5);top:8%;right:8%;animation:floaty 7s ease-in-out infinite}
.a2{width:130px;height:130px;border-radius:99px;background:conic-gradient(from 20deg,#FF78C8,#FFE66D,#71F6D5,#7C9BFF,#FF78C8);border:3px solid rgba(255,255,255,.8);box-shadow:0 0 24px rgba(184,255,240,.4);bottom:14%;right:24%;animation:spin 11s linear infinite}
.sec h3{font-weight:700;color:#B8FFF0;letter-spacing:.08em}
.prose{background:rgba(40,33,61,.72);border:1px solid rgba(255,255,255,.35);border-radius:14px;padding:30px;backdrop-filter:blur(10px)}
.chips li{border:1px solid #B8FFF0;border-radius:99px;background:rgba(184,255,240,.12);color:#F7F4FF}
pre{background:#0E0A1D;color:#B8FFF0;border:1px solid #FF78C8;border-radius:8px}
.tl b{color:#FF78C8;font-weight:700}
.hallnav a{border:1px solid #B8FFF0;border-radius:99px;background:rgba(40,33,61,.7);color:#F7F4FF}
""",
'liquidtypo': """
body{background:#17132D;color:#F7F4FF;font-family:Arial,"Helvetica Neue",sans-serif}
::selection{background:#A7FFEA;color:#17132D}
.topbar{background:#29204B;border-bottom:2px solid #A7FFEA;color:#F7F4FF}
.hero{background:radial-gradient(ellipse at 18% 28%,rgba(255,91,180,.32),transparent 30%),radial-gradient(ellipse at 82% 20%,rgba(167,255,234,.22),transparent 28%)}
.hero .big{font-weight:900;letter-spacing:-.1em;color:#A7FFEA;text-shadow:0 0 14px #A7FFEA}
.hero .en{color:#FF62B0;letter-spacing:.18em}
.hero .man{background:#29204B;border:2px solid #A7FFEA;border-radius:42% 58% 54% 46%;padding:20px 24px;box-shadow:inset 8px -8px 0 rgba(255,91,180,.2)}
.meta span{border:1px solid #A7FFEA;border-radius:42% 58% 54% 46%;background:#29204B;color:#F7F4FF}
.a1{width:190px;height:130px;background:#231B45;border-radius:42% 58% 54% 46%;border:2px solid #A7FFEA;box-shadow:inset 8px -8px 0 rgba(255,91,180,.35),0 0 20px rgba(167,255,234,.25);top:9%;right:8%;animation:floaty 6s ease-in-out infinite}
.a2{width:130px;height:110px;background:#FF62B0;border-radius:20% 80% 35% 65%;box-shadow:0 0 24px rgba(255,98,176,.45);bottom:14%;right:24%;animation:spin 14s linear infinite}
.sec h3{font-weight:800;color:#A7FFEA;letter-spacing:.05em}
.prose{background:#29204B;border:1px solid #A7FFEA;border-radius:28% 72% 35% 65%;padding:30px;line-height:2}
.chips li{border:1px solid #A7FFEA;border-radius:42% 58% 54% 46%;background:#231B45;color:#F7F4FF}
pre{background:#0D091C;color:#A7FFEA;border:2px solid #FF62B0;border-radius:16px}
.tl b{color:#FF62B0;font-weight:800}
.hallnav a{border:1px solid #A7FFEA;border-radius:42% 58% 54% 46%;background:#29204B;color:#F7F4FF}
""",
'kawaii': """
body{background:#FFF0F5;color:#6E4B5E;font-family:"Arial Rounded MT Bold","Trebuchet MS",Arial,sans-serif}
::selection{background:#F4A6B8;color:#6E4B5E}
.topbar{background:#fff;border-bottom:3px solid #F4A6B8;color:#6E4B5E}
.hero{background:radial-gradient(circle at 80% 18%,#BDE7FF 0 7%,transparent 8%),radial-gradient(circle at 18% 24%,#FFD1E3 0 8%,transparent 9%),#FFF0F5}
.hero .big{font-weight:900;letter-spacing:-.06em;color:#F4A6B8;text-shadow:3px 3px 0 #fff}
.hero .en{color:#9AC7E2;letter-spacing:.18em}
.hero .man{background:#fff;border:3px solid #F4A6B8;border-radius:48% 52% 50% 50%;padding:18px 24px;box-shadow:0 8px 0 #F8CDD8}
.meta span{border:2px solid #fff;border-radius:999px;background:#BDE7FF;color:#6A5072;box-shadow:0 4px 0 #9AC7E2}
.a1{width:150px;height:125px;border-radius:48% 52% 50% 50%;background:#fff;border:4px solid #F4A6B8;box-shadow:0 8px 0 #F8CDD8;top:9%;right:8%;animation:floaty 6s ease-in-out infinite}
.a2{width:125px;height:125px;border-radius:50%;background:#BDE7FF;border:4px solid #fff;box-shadow:0 4px 0 #9AC7E2;bottom:14%;right:24%;animation:spin 12s linear infinite}
.sec h3{font-weight:900;color:#F4A6B8;letter-spacing:.06em}
.prose{background:#fff;border:2px solid #F4A6B8;border-radius:24px;padding:30px;box-shadow:0 8px 0 #F8CDD8}
.chips li{border:2px solid #fff;border-radius:999px;background:#FFD1E3;color:#6E4B5E;box-shadow:0 4px 0 #F8CDD8}
pre{background:#6E4B5E;color:#FFF0F5;border:3px solid #F4A6B8;border-radius:16px}
.tl b{color:#F4A6B8;font-weight:900}
.hallnav a{border:2px solid #F4A6B8;border-radius:999px;background:#fff;color:#6E4B5E;box-shadow:0 4px 0 #F8CDD8}
""",
'afrofuturism': """
body{background:#160D2D;color:#F7E7B2;font-family:"Trebuchet MS","Helvetica Neue",sans-serif}
::selection{background:#17C3B2;color:#160D2D}
.topbar{background:#2B1744;border-bottom:2px solid #17C3B2;color:#F7E7B2}
.hero{background:radial-gradient(circle at 70% 20%,#FF6B35 0 8%,transparent 28%),radial-gradient(circle at 18% 72%,rgba(23,195,178,.25),transparent 25%)}
.hero .big{font-weight:800;letter-spacing:-.05em;background:linear-gradient(110deg,#F7E7B2,#FF6B35,#17C3B2);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero .en{color:#17C3B2;letter-spacing:.2em}
.hero .man{background:#2B1744;border:2px solid #17C3B2;padding:20px 24px;box-shadow:0 0 28px rgba(23,195,178,.35)}
.meta span{border:1px solid #17C3B2;border-radius:99px;background:#2B1744;color:#F7E7B2}
.a1{width:180px;height:180px;border:3px solid #17C3B2;border-radius:50%;background:radial-gradient(circle at 50% 50%,#FF6B35 0 13%,transparent 14%),radial-gradient(circle at 30% 30%,#F7E7B2 0 2px,transparent 3px),#160D2D;box-shadow:0 0 28px rgba(23,195,178,.45);top:8%;right:8%;animation:spin 17s linear infinite}
.a2{width:130px;height:130px;border-radius:50%;background:radial-gradient(circle at 42% 38%,#F7E7B2 0 9%,#FFB627 10% 34%,#FF6B35 35% 63%,#4C1D4F 64%);border:3px solid #F7E7B2;bottom:14%;right:24%;animation:floaty 7s ease-in-out infinite}
.sec h3{font-weight:800;color:#17C3B2;letter-spacing:.08em}
.prose{background:#2B1744;border:1px solid #17C3B2;padding:30px;line-height:2;box-shadow:0 0 24px rgba(23,195,178,.2)}
.chips li{border:1px solid #17C3B2;border-radius:99px;background:#FF6B35;color:#160D2D;font-weight:700}
pre{background:#0D071C;color:#F7E7B2;border:3px solid #17C3B2}
.tl b{color:#FF6B35;font-weight:800}
.hallnav a{border:1px solid #17C3B2;border-radius:99px;background:#2B1744;color:#F7E7B2}
""",
'isometric': """
body{background:#F7F1E3;color:#243447;font-family:"Segoe UI","Helvetica Neue",Arial,sans-serif}
::selection{background:#FFB703;color:#243447}
.topbar{background:#fff;border-bottom:2px solid #D9E2EC;color:#243447}
.hero{background:linear-gradient(135deg,rgba(189,224,254,.35) 0 33%,transparent 33% 55%,rgba(111,168,199,.2) 55% 72%,transparent 72%)}
.hero .big{font-weight:800;letter-spacing:-.06em}
.hero .en{color:#FFB703;letter-spacing:.18em;font-weight:700}
.hero .man{background:#fff;border-radius:4px;padding:20px 26px;box-shadow:12px 12px 0 -4px rgba(36,52,71,.14)}
.meta span{border:0;border-radius:4px;background:#BDE0FE;color:#18577A;font-weight:700;box-shadow:0 5px 0 rgba(36,52,71,.12)}
.a1{width:120px;height:120px;background:linear-gradient(135deg,#FFB703 0 50%,#FB8500 50%);transform:skewY(-30deg) rotate(30deg);box-shadow:22px 18px 0 #8ECAE6,44px 36px 0 #BDE0FE;top:11%;right:9%;animation:floaty 7s ease-in-out infinite}
.a2{width:140px;height:100px;background:linear-gradient(135deg,transparent 0 48%,#355C7D 49% 62%,transparent 63%),linear-gradient(155deg,#BDE0FE 0 49%,#6FA8C7 50% 72%,#355C7D 73%);clip-path:polygon(0 88%,18% 52%,33% 70%,52% 22%,69% 62%,100% 40%,100% 100%,0 100%);bottom:14%;right:24%;animation:spin 15s linear infinite}
.sec h3{font-weight:700;color:#355C7D;letter-spacing:.04em}
.prose{background:#fff;border-radius:8px;padding:30px;box-shadow:12px 12px 0 -4px rgba(36,52,71,.14)}
.chips li{border:0;border-radius:5px;background:#CDEAC0;color:#32643B;font-weight:600;box-shadow:0 5px 0 rgba(36,52,71,.1)}
pre{background:#243447;color:#BDE0FE;border-radius:5px;box-shadow:0 8px 0 rgba(36,52,71,.12)}
.tl b{color:#FFB703;font-weight:700}
.hallnav a{border:0;border-radius:5px;background:#243447;color:#fff;box-shadow:0 5px 0 rgba(36,52,71,.15)}
""",
}

BASE_JS = """
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));

/* 保底:IO 不可靠的环境(无头/老 WebView)——滚动与超时双保险 */
(function(){
  var check=function(){
    document.querySelectorAll('.rv:not(.in)').forEach(function(el){
      var r=el.getBoundingClientRect();
      if(r.top<innerHeight*.92&&r.bottom>0){el.classList.add('in');io.unobserve(el)}
    });
  };
  addEventListener('scroll',check,{passive:true});
  addEventListener('resize',check,{passive:true});
  setInterval(check,600);
  setTimeout(check,100);
  setTimeout(function(){document.querySelectorAll('.rv:not(.in)').forEach(function(el){el.classList.add('in')})},3000);
})();

/* 触屏点按标本卡:切换代码面板(非精确指针才注册) */
(function(){
  if(matchMedia('(pointer:fine)').matches)return;
  document.addEventListener('click',function(e){
    var ex=e.target.closest('.ex');
    if(!ex)return;
    ex.classList.toggle('code-revealed');
  },{passive:true});
})();

/* 自定义光标:点+拖尾环+CSS 粒子+点击涟漪(仅桌面指针) */
(function(){
  if(!matchMedia('(pointer:fine)').matches)return;
  var dot=document.createElement('div'); dot.id='cur-dot';
  var ring=document.createElement('div'); ring.id='cur-ring';
  document.body.appendChild(dot); document.body.appendChild(ring);
  var mx=innerWidth/2,my=innerHeight/2,rx=mx,ry=my,lx=mx,ly=my;
  addEventListener('mousemove',function(e){
    mx=e.clientX;my=e.clientY;
    dot.style.left=mx+'px';dot.style.top=my+'px';
    var dx=mx-lx,dy=my-ly;
    if(dx*dx+dy*dy>200){spawnP(mx,my);lx=mx;ly=my}
  },{passive:true});
  (function loop(){rx+=(mx-rx)*.16;ry+=(my-ry)*.16;
    ring.style.left=rx+'px';ring.style.top=ry+'px';requestAnimationFrame(loop)})();
  addEventListener('mousedown',function(e){document.body.classList.add('cur-down');ripple(e.clientX,e.clientY)});
  addEventListener('mouseup',function(){document.body.classList.remove('cur-down')});
  function spawnP(x,y){
    var p=document.createElement('span');p.className='cur-p';
    var sz=3+Math.random()*4;
    p.style.cssText='left:'+x+'px;top:'+y+'px;width:'+sz+'px;height:'+sz+'px;background:'+(Math.random()<.5?'#FFD23F':'#fff')+';transition:transform .4s ease-out,opacity .4s ease-out';
    document.body.appendChild(p);
    requestAnimationFrame(function(){
      var a=Math.random()*Math.PI*2,d=16+Math.random()*32;
      p.style.transform='translate('+Math.cos(a)*d+'px,'+Math.sin(a)*d+'px) scale(0)';
      p.style.opacity='0';
    });
    setTimeout(function(){p.remove()},420);
  }
  function ripple(x,y){
    var r=document.createElement('span');r.className='cur-ripple';
    r.style.cssText='left:'+x+'px;top:'+y+'px;transform:translate(-50%,-50%)';
    document.body.appendChild(r);setTimeout(function(){r.remove()},500);
  }
  // 事件委托代替逐个监听
  document.addEventListener('mouseover',function(e){
    if(e.target.closest('a,button,.xob,[role=button]')) document.body.classList.add('cur-hover');
  },{passive:true});
  document.addEventListener('mouseout',function(e){
    if(e.target.closest('a,button,.xob,[role=button]')) document.body.classList.remove('cur-hover');
  },{passive:true});
})();
"""

def render(m, prev_m, next_m):
    e = H.escape
    hero_art = ''.join(f'<div class="a{i+1}"></div>' for i in range(3))
    traits = ''.join(f'<li><b>{e(t)}</b> — {e(d)}</li>' for t, d in m['traits'])
    tl = ''.join(f'<li class="rv"><b>{e(y)}</b><span>{e(t)}</span></li>' for y, t in m['tl'])
    reps = ''.join(f'<li class="rv">{e(r)}</li>' for r in m['reps'])
    kw = '、'.join(m['keywords'])
    seo = f"{m['zh']}({m['en']})设计主义:起源、人物、转折、传播、争议、影响与代表案例。{kw} | 主义馆 ISM MUSEUM"
    prologue = m.get('prologue', '')
    history_deep = f'''<div class="history-deep-grid"><article class="history-deep-card"><h4>起源与语境</h4><p>{e(m['origin'])}</p></article><article class="history-deep-card"><h4>核心人物与机构</h4><p>{e(m['figures'])}</p></article><article class="history-deep-card"><h4>关键转折</h4><ul>{''.join(f'<li>{e(item)}</li>' for item in m['turns'])}</ul></article><article class="history-deep-card"><h4>传播路径</h4><p>{e(m['diffusion'])}</p></article><article class="history-deep-card"><h4>批评与争议</h4><p>{e(m['debate'])}</p></article><article class="history-deep-card"><h4>当代影响</h4><p>{e(m['legacy'])}</p></article></div>'''
    exhibits = ''.join(f'''<figure class="ex rv" data-x="{i}">
      <div class="ex-art"><span class="xob" style="{css}"></span></div>
      <figcaption class="ex-cap">{e(cap)}</figcaption>
      <div class="ex-code">{e(css)}</div>
      {f'<script>(function(){{var el=document.querySelector(\'[data-x="{i}"] .xob\');{js}}})()</script>' if js else ''}
    </figure>''' for i, (cap, css, js) in enumerate(m.get('exhibits', [])))
    exhibit_sec = f'''  <section class="sec rv">
    <div class="kicker">Specimens</div>
    <h3>馆内标本</h3>
    <p class="hint">全部质感由 CSS 实时绘制,无一张图片。可直接检视元素、复制样式。</p>
    <div class="exgrid">{exhibits}</div>
  </section>''' if exhibits else ''
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(m['zh'])} {e(m['en'])} · 主义馆展厅 HALL {m['no']}</title>
<meta name="description" content="{e(seo)}">
<meta name="keywords" content="{e(kw)}">
<meta property="og:title" content="{e(m['zh'])} {e(m['en'])} · 主义馆">
<meta property="og:description" content="{e(m['manifesto'])}">
<style>{BASE_CSS}{THEME_CSS[m['slug']]}</style>
</head>
<body>
<div class="topbar">
  <a href="../index.html">← 大厅</a>
  <a href="../corridor.html">长廊</a>
  <a href="../timeline.html">时间轴</a>
  <a href="../knowledge.html">全书</a>
  <a href="../index.html#door-{m['slug']}">返回门位</a>
</div>

<header class="hero">
  <div class="art"><div class="stars"></div>{hero_art}</div>
  <div style="position:relative">
    <span class="kicker">HALL {m['no']} · {e(m['period'])}</span>
    <h1 class="big">{e(m['zh'])}</h1>
    <div class="en">{e(m['en'])} · {e(m['era'])}</div>
    <p class="man">“{e(m['manifesto'])}”</p>
    <div class="meta"><span>{e(m['era'])}</span><span>{e(m['period'])}</span></div>
  </div>
</header>

<main class="wrap">
  {f'<p class="lede rv">{e(prologue)}</p>' if prologue else ''}
  <section class="sec rv">
    <div class="kicker">Archive</div>
    <h3>历史档案</h3>
    <p class="prose">{e(m['history'])}</p>
  </section>
  <section class="sec rv">
    <div class="kicker">History / Deep Reading</div>
    <h3>历史深描</h3>
    <p class="prose">从起源、人物、转折和传播路径继续阅读，并保留批评与争议；下面的前端标本只是应用层，不替代这段历史。</p>
    {history_deep}
  </section>
  {exhibit_sec}
  <section class="sec rv">
    <div class="kicker">Archive</div>
    <h3>代表案例</h3>
    <ul class="chips">{reps}</ul>
  </section>
  <section class="sec rv">
    <div class="kicker">Traits</div>
    <h3>风格特征</h3>
    <ul class="chips">{traits}</ul>
  </section>
  <section class="sec rv">
    <div class="kicker">Fingerprint</div>
    <h3>代码指纹</h3>
    <pre><code>{e(m['code'])}</code></pre>
  </section>
  <section class="sec rv">
    <div class="kicker">Timeline</div>
    <h3>年代坐标</h3>
    <ul class="tl">{tl}</ul>
  </section>
</main>

<nav class="hallnav">
  <a href="{prev_m['slug']}.html">← {e(prev_m['zh'])}</a>
  <a href="../index.html">返回大厅</a>
  <a href="{next_m['slug']}.html">{e(next_m['zh'])} →</a>
</nav>
<footer>主义馆 ISM MUSEUM · HALL {m['no']}/80 · 本展厅全部质感由 CSS 绘制,无一张图片</footer>
<script>{BASE_JS}</script>
</body>
</html>"""

for m in ISMS:
    m.update(ISM_HISTORY[m['slug']])
for i, m in enumerate(ISMS):
    prev_m = ISMS[(i - 1) % len(ISMS)]
    next_m = ISMS[(i + 1) % len(ISMS)]
    with open(os.path.join(OUT, m['slug'] + '.html'), 'w', encoding='utf-8') as f:
        f.write(render(m, prev_m, next_m))
print('generated', len(ISMS), 'hall pages')
build_knowledge(BASE)
