# -*- coding: utf-8 -*-
"""课程母题与现代设计条目的策展映射。

映射是知识库的前端转译层：一个主义可以跨越多个课内母题。
它不把扩展展厅目录冒充成课堂原样目录。
"""

COURSE_AXES = [
    {
        'key': 'planning',
        'no': '01',
        'title': '设计计划与问题解决',
        'en': 'PLAN / SOLVE',
        'focus': '从问题、使用者、场景与限制出发，让形式成为可解释的决定。',
        'question': '要解决谁的问题？条件、成本、材料和验收标准是什么？',
        'frontend': '先写用户任务、内容目标、约束条件与验收标准，再开始做视觉。',
        'feedback': '把 brief、决策日志和测试结果沉淀为设计计划案例。',
    },
    {
        'key': 'function',
        'no': '02',
        'title': '功能、使用者与形式',
        'en': 'FUNCTION / USER / FORM',
        'focus': '检验形式是否帮助使用者，而不是把“好看”当成设计结论。',
        'question': '形式是否帮助任务？装饰何时服务内容，何时遮蔽内容？',
        'frontend': '用信息架构、语义 HTML、视觉层级、操作反馈和同伴测试验证可用性。',
        'feedback': '把误读、任务路径和修改前后对照写回功能主义案例。',
    },
    {
        'key': 'material',
        'no': '03',
        'title': '材料与结构',
        'en': 'MATERIAL / STRUCTURE',
        'focus': '材料特性、结构关系与制作方式共同生成形式。',
        'question': '材料和制作方法怎样生成形式？结构应该隐藏还是显露？',
        'frontend': '把 DOM、布局、CSS 状态和动效当作数字材料与结构，而不是只贴纹理。',
        'feedback': '记录不同屏幕、输入方式和性能条件下的数字材料行为。',
    },
    {
        'key': 'production',
        'no': '04',
        'title': '工业生产与标准化',
        'en': 'PRODUCTION / STANDARD',
        'focus': '理解机器、批量生产和标准如何同时提升效率又制造约束。',
        'question': '怎样在效率与复用中保留质量、语境和差异？',
        'frontend': '用设计令牌、组件、数据驱动页面和性能预算支持多页面生产。',
        'feedback': '把组件清单、版本变化和标准化造成的损失做成课程案例。',
    },
    {
        'key': 'ornament',
        'no': '05',
        'title': '装饰与形式来源',
        'en': 'ORNAMENT / SOURCE',
        'focus': '追问纹样、字体、色彩和构图从何而来，避免把历史语境压扁成风格滤镜。',
        'question': '形式的来源是什么？它为什么属于这个主义，而不是泛泛的“好看”？',
        'frontend': '为视觉资产建立来源地图与转译说明，让装饰承担语义、导航或情绪功能。',
        'feedback': '把来源、改动和语境风险写进标本说明与评价量表。',
    },
    {
        'key': 'modernism',
        'no': '06',
        'title': '现代主义',
        'en': 'MODERNISM',
        'focus': '回应机器时代，以功能、结构、理性、网格和面向多数人的设计建立新形式。',
        'question': '艺术、工艺、技术、教育和生产怎样共同组织现代生活？',
        'frontend': '用网格、字体层级、内容优先和响应式系统组织复杂信息。',
        'feedback': '当固定网格在手机或无障碍场景失效时，区分原则与历史外观并回写课程。',
    },
    {
        'key': 'postmodern',
        'no': '07',
        'title': '后现代与反叛',
        'en': 'POSTMODERN / REBELLION',
        'focus': '反问唯一的好品味、统一秩序和单一功能，让多重语气与冲突进入设计。',
        'question': '表达更强之后，是否仍然可理解、可操作、可被不同人使用？',
        'frontend': '允许拼贴、故意冲突和陌生化，同时保留清晰结构、替代文本和键盘路径。',
        'feedback': '比较克制版与反叛版的理解结果，记录表达收益与使用代价。',
    },
    {
        'key': 'ethics',
        'no': '08',
        'title': '设计伦理与责任',
        'en': 'ETHICS / RESPONSIBILITY',
        'focus': '追问设计为谁服务，以及它是否排斥、操控、浪费资源或伪装价值。',
        'question': '谁被照顾，谁被排除？技术真的改善了生活吗？',
        'frontend': '把对比度、键盘访问、减少动效、包容性语言、性能和反暗黑模式作为发布门槛。',
        'feedback': '把可访问性审计、资源取舍和用户伤害风险写入评分量表。',
    },
]

AXIS_SLUGS = {
    'planning': [
        'bauhaus', 'constructivism', 'swiss', 'minimalism', 'typographic', 'editorial',
        'blueprint', 'web1', 'retrogui', 'materialdesign', 'metro', 'bentogrid',
        'isometric', 'hightech', 'newchinese', 'midcentury', 'streamline', 'darkmode',
    ],
    'function': [
        'minimalism', 'swiss', 'bauhaus', 'flatdesign', 'skeuomorphism', 'neumorphism',
        'glassmorphism', 'claymorphism', 'brutalism', 'frutigeraero', 'bentogrid',
        'materialdesign', 'metro', 'corpmemphis', 'typographic', 'editorial', 'duotone',
        'flat3d', 'kinetictypo', 'liquidtypo', 'retrogui', 'web2gloss', 'darkmode',
        'isometric', 'pixelart', 'asciiart',
    ],
    'material': [
        'artsandcrafts', 'artnouveau', 'wabisabi', 'brutalism', 'hightech', 'blueprint',
        'papercut', 'claymorphism', 'neumorphism', 'glassmorphism', 'skeuomorphism',
        'lowpoly', 'flat3d', 'holographic', 'liquidtypo', 'steampunk', 'dieselpunk',
        'isometric', 'midcentury', 'newchinese', 'cottagecore', 'darkacademia',
        'retrofuturism', 'atompunk', 'pixelart',
    ],
    'production': [
        'bauhaus', 'constructivism', 'artdeco', 'streamline', 'midcentury', 'hightech',
        'pixelart', 'asciiart', 'retrogui', 'lowpoly', 'web1', 'web2gloss', 'materialdesign',
        'metro', 'aigenerative', 'duotone', 'flatdesign', 'bentogrid', 'frutigeraero',
        'corpmemphis', 'swiss', 'typographic', 'isometric', 'futurism', 'googie',
        'atompunk', 'retrofuturism',
    ],
    'ornament': [
        'artdeco', 'artnouveau', 'artsandcrafts', 'viennasecession', 'newchinese', 'opart',
        'psychedelic', 'psychedelicposter', 'popart', 'maximalism', 'memphis', 'doodle',
        'papercut', 'vaporwave', 'aurora', 'holographic', 'kawaii', 'cottagecore',
        'darkacademia', 'frutigeraero', 'duotone', 'pushpin', 'surrealism', 'afrofuturism',
        'wabisabi', 'liquidtypo', 'dreamcore', 'weirdcore',
    ],
    'modernism': [
        'bauhaus', 'constructivism', 'swiss', 'destijl', 'futurism', 'viennasecession',
        'minimalism', 'artdeco', 'streamline', 'midcentury', 'hightech', 'blueprint',
        'materialdesign', 'flatdesign', 'typographic', 'editorial', 'opart', 'web1',
        'retrogui', 'isometric', 'newchinese', 'googie', 'retrofuturism', 'metro',
    ],
    'postmodern': [
        'memphis', 'popart', 'dada', 'surrealism', 'antidesign', 'swisspunk', 'brutalism',
        'neubrutalism', 'grunge', 'punkxerox', 'photomontage', 'glitchart', 'vaporwave',
        'cyberpunk', 'y2k', 'aciddesign', 'maximalism', 'weirdcore', 'dreamcore', 'liminal',
        'psychedelic', 'doodle', 'liquidtypo', 'corpmemphis', 'web2gloss', 'darkacademia',
        'kawaii', 'synthwave', 'steampunk', 'dieselpunk', 'pushpin', 'asciiart',
        'aigenerative', 'cottagecore', 'papercut',
    ],
    'ethics': [
        'antidesign', 'solarpunk', 'afrofuturism', 'wabisabi', 'artsandcrafts', 'dada',
        'popart', 'aigenerative', 'cyberpunk', 'atompunk', 'dieselpunk', 'neumorphism',
        'glassmorphism', 'darkmode', 'minimalism', 'web1', 'brutalism', 'newchinese',
        'cottagecore', 'frutigeraero', 'hightech', 'lowpoly', 'y2k', 'retrofuturism',
        'materialdesign', 'kawaii', 'corpmemphis', 'liminal', 'dreamcore',
    ],
}

ISM_AXES = {}
for axis_key, slugs in AXIS_SLUGS.items():
    for slug in slugs:
        ISM_AXES.setdefault(slug, []).append(axis_key)
