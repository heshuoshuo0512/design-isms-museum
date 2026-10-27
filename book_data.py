# -*- coding: utf-8 -*-
"""现代设计通史主干、横向实践和延伸阅读的静态数据。

这里的章节不是 80 个视觉方向的别名，而是用时间、生产、媒介和权力
把现代设计的形成过程串起来。具体作品和人物仍应在使用本数据时逐条
对照一手材料与版本信息。
"""

BOOK_CHAPTERS = [
    {
        'key': 'industrial-modernity',
        'no': '01',
        'period': '1850s–1880s',
        'title': '工业化、城市与设计问题的出现',
        'thesis': '现代设计首先不是一种外观，而是工厂制、城市化、展览和消费社会共同制造的新问题：谁设计、谁生产、谁使用，以及如何让批量物品仍然具有秩序和尊严。',
        'context': '蒸汽动力、铁路、印刷和百货商店扩大了物品与信息的流通；机械复制提高了数量，却也暴露出粗劣制造、劳动异化、环境负担和审美等级的问题。',
        'actors': '工厂主、工人、工程师、工艺师、建筑师、改革者、博览会组织者、出版商和城市公共机构共同构成早期设计制度。',
        'places': '英国工业城市、伦敦国际博览会、法国和德国的工艺学校与制造业城市。',
        'practices': ['工业产品与机器生产', '展览、印刷和商业广告', '住宅、公共卫生与城市环境', '工艺教育和生产改革'],
        'turning_points': ['批量生产把形式、材料和生产效率变成同一个问题。', '国际博览会把工业产品、国家竞争和公共教育放在同一展场。', '工艺改革者开始以工作室、协会和学校回应工业化，而不是只在作品上反对机器。'],
        'works': ['1851 年伦敦万国工业博览会与水晶宫', '威廉·莫里斯的 Red House 与 Kelmscott Press', '约翰·拉斯金关于劳动、材料和建筑的批评'],
        'debate': '工艺美术运动既批评工业生产，又依赖出版、商业和中产阶级消费；“回到手工”并不能自动解决劳动和可负担性问题。',
        'legacy': '设计开始成为生产方式、材料寿命、劳动条件和日常环境的综合问题，为后来的现代主义教育和工业设计制度奠基。',
        'source_keys': ['forty', 'margolin', 'adamson'],
    },
    {
        'key': 'decorative-modernities',
        'no': '02',
        'period': '1880s–1914',
        'title': '新艺术、工艺改革与多种现代性',
        'thesis': '新艺术、维也纳分离派、德国制造联盟和日本工艺传播没有形成单一风格，它们共同探索如何让建筑、家具、字体、图案和商业环境适应新的城市生活。',
        'context': '电灯、钢铁、玻璃、铁路和大众印刷改变了城市感知；设计师同时面对历史样式的疲劳、机器生产的诱惑和民族文化身份的建构。',
        'actors': '工艺协会、制造联盟、百货商店、杂志、建筑师、画家、家具制造商和新式设计学校。',
        'places': '伦敦、巴黎、布鲁塞尔、维也纳、慕尼黑、格拉斯哥、柏林和东京。',
        'practices': ['建筑与室内整体设计', '海报、字体和商业印刷', '家具、玻璃、陶瓷和金属工艺', '设计展览与制造联盟'],
        'turning_points': ['新艺术把植物、曲线、铁和玻璃带入商业城市。', '维也纳分离派和德国制造联盟试图连接艺术、建筑、工业和国家经济。', '日本版画与工艺进入欧洲视觉文化，反过来改变欧洲对平面、空间和装饰的理解。'],
        'works': ['维克多·奥塔的塔塞尔住宅', '查尔斯·雷尼·麦金托什的格拉斯哥作品', '彼得·贝伦斯与 AEG 的建筑、产品和企业形象系统'],
        'debate': '“现代”并不只有一条西方进步路线；新艺术也可能服务于商业消费、民族主义和殖民展览。',
        'legacy': '整体环境、企业形象、字体和工业协作成为现代设计制度的前身。',
        'source_keys': ['raizman', 'sparke', 'margolin'],
    },
    {
        'key': 'avant-garde-propaganda',
        'no': '03',
        'period': '1905–1919',
        'title': '先锋艺术、革命与大众传播',
        'thesis': '未来主义、达达、构成主义和摄影蒙太奇把设计从装饰物变成组织公众注意力、传播政治主张和制造集体经验的工具。',
        'context': '战争、革命、电影、报纸和新印刷技术改变了图像传播的速度；艺术家开始把文字、照片、几何形和复制技术当作社会行动。',
        'actors': '艺术家、设计师、摄影师、出版编辑、革命机构、剧场、电影制作者和宣传部门。',
        'places': '意大利、苏黎世、柏林、莫斯科、彼得格勒和欧洲战时传播网络。',
        'practices': ['海报与政治传播', '摄影蒙太奇', '书籍、杂志和展览设计', '舞台、电影和公共视觉系统'],
        'turning_points': ['宣言和杂志把艺术运动组织成可传播的立场。', '构成主义将摄影、字体、几何构成和革命传播连接起来。', '复制技术使设计从独一作品转向可扩散的公共媒介。'],
        'works': ['马里内蒂《未来主义宣言》', '亚历山大·罗德琴科与瓦尔瓦拉·斯捷潘诺娃的构成主义传播设计', '约翰·哈特菲尔德的政治摄影蒙太奇'],
        'debate': '大众传播可以扩大公共参与，也可以服务宣传、审查和群众动员；“有效传播”不是中性的技术指标。',
        'legacy': '版式、摄影、文字和传播目标被纳入同一个设计系统，影响后来的广告、政治传播和信息界面。',
        'source_keys': ['meggs', 'margolin', 'forty'],
    },
    {
        'key': 'schools-and-systems',
        'no': '04',
        'period': '1919–1933',
        'title': '包豪斯、德·斯蒂尔与新字体',
        'thesis': '现代主义教育把设计变成一套可教学、可分工、可重复的工作方法：材料实验、形式分析、工业协作、网格组织和社会生活被放进同一课程。',
        'context': '第一次世界大战后的政治重建、住房需求和工业生产要求设计学校重新定义艺术与技术的关系。',
        'actors': '包豪斯教师与学生、德·斯蒂尔成员、建筑师、字体设计师、制造商和公共住房机构。',
        'places': '魏玛、德绍、柏林、莱顿、斯图加特和欧洲现代主义网络。',
        'practices': ['基础课程与材料实验', '建筑、家具和灯具设计', '字体、摄影和展览', '标准化生产与公共住房'],
        'turning_points': ['1919 年包豪斯成立，艺术教育开始明确面对工业生产。', '学校从手工艺理想转向工业协作和建筑综合。', '政治压力导致学校迁移并最终关闭，但教师和学生通过迁徙把方法带到不同国家。'],
        'works': ['包豪斯校舍与课程体系', '马塞尔·布劳耶的钢管家具', '扬·奇肖尔德《新字体》与现代版式实践'],
        'debate': '包豪斯常被压缩成几何、三原色和无衬线字体；实际历史包含性别分工、政治压力、商业合作和迁徙后的再解释。',
        'legacy': '设计教育、组件思维、材料实验、系统版式和跨学科协作成为现代设计的基础设施。',
        'source_keys': ['raizman', 'meggs', 'lees-maffei'],
    },
    {
        'key': 'industrial-consumer-design',
        'no': '05',
        'period': '1920s–1940s',
        'title': '工业设计、流线型与消费社会',
        'thesis': '工业设计在企业、广告、展览和消费市场中形成职业身份；形式不仅表达功能，也参与销售、品牌竞争和对未来生活的想象。',
        'context': '大规模制造、家用电器、汽车、广播和电影把设计纳入企业经营；经济危机与战争又暴露了消费设计和资源动员的矛盾。',
        'actors': '企业设计部门、独立工业设计师、工程师、广告商、零售商、政府和消费者。',
        'places': '美国制造业城市、纽约展览网络、欧洲工业企业和战时生产体系。',
        'practices': ['产品与家电设计', '汽车和交通工具', '包装、广告和企业品牌', '展览、橱窗和未来生活展示'],
        'turning_points': ['设计师进入企业，形式开始和市场策略、工程生产共同决策。', '流线型把速度、效率和未来感包装成消费符号。', '战争生产把材料、标准、维修和资源分配置于设计核心。'],
        'works': ['雷蒙德·罗维的产品与企业形象实践', '诺曼·贝尔·盖德斯的未来城市与交通想象', '1939 年纽约世界博览会的未来生活展示'],
        'debate': '“为过时而设计”推动销售，却加速资源消耗；工业设计的职业伦理不能只由市场增长衡量。',
        'legacy': '产品设计、品牌系统、用户研究和生产约束被整合为企业设计流程。',
        'source_keys': ['heskett', 'forty', 'raizman'],
    },
    {
        'key': 'war-reconstruction',
        'no': '06',
        'period': '1930s–1950s',
        'title': '战争、重建与设计的公共制度',
        'thesis': '战争、迁徙和战后重建让设计进入住房、交通、公共信息、教育和国家治理；现代设计既可能服务公共福祉，也可能服务国家动员。',
        'context': '设计教育和现代主义方法通过迁徙进入美洲、中东、亚洲等地；战争时期的标准、材料和信息系统延伸到和平时期的公共建设。',
        'actors': '政府机构、公共住房组织、设计学校、工程师、建筑师、工业企业和国际组织。',
        'places': '欧洲重建城市、美国设计机构、拉丁美洲现代化项目以及亚洲战后工业城市。',
        'practices': ['公共住房与城市规划', '交通与公共信息', '标准化生产和维修', '国家宣传与国际展览'],
        'turning_points': ['现代主义学校和专业网络因政治迁徙而扩散。', '战时生产将标准、材料和信息效率制度化。', '战后国家把设计用于住房、教育、公共卫生和现代化想象。'],
        'works': ['战后公共住房与城市重建项目', '联合国及国际展览中的现代化视觉系统', '企业与公共机构的标准化识别系统'],
        'debate': '现代主义的公共目标和国家权力始终纠缠；“进步”可能带来拆迁、同质化和对地方知识的压制。',
        'legacy': '设计被纳入公共服务、基础设施和国家制度，而不再只是私人产品或装饰。',
        'source_keys': ['margolin', 'sparke', 'papanek'],
    },
    {
        'key': 'systems-corporate-identity',
        'no': '07',
        'period': '1950s–1960s',
        'title': '国际主义、乌尔姆与企业系统',
        'thesis': '战后设计把网格、字体、标识、产品和信息组织成跨媒介系统；系统化提高了协作和一致性，也可能掩盖政治和商业权力。',
        'context': '跨国企业、航空、电视、公共交通和消费品牌需要在不同地点持续识别；设计学校开始把科学方法、工程和信息理论纳入课程。',
        'actors': '乌尔姆设计学院、企业设计部门、字体设计师、信息设计师、工程师和公共交通机构。',
        'places': '乌尔姆、苏黎世、纽约、伦敦、东京及跨国企业网络。',
        'practices': ['企业识别与品牌系统', '公共交通和导视', '信息图表与编辑设计', '产品、界面和服务的标准化'],
        'turning_points': ['国际主义版式将对齐、网格和中性字体变成可复制的视觉基础设施。', '乌尔姆将设计教育与工程、科学和系统分析连接。', '企业识别把标志、建筑、产品和员工行为纳入统一系统。'],
        'works': ['乌尔姆设计学院课程与实践', '奥托·艾舍与奥运会视觉系统', '纽约地铁与机场导视系统'],
        'debate': '系统的中性外观并不等于政治中性；企业识别也可能制造跨地域的消费秩序和文化同质化。',
        'legacy': '设计 token、组件库、设计规范、导视系统和跨团队协作都有这段系统史的回声。',
        'source_keys': ['raizman', 'heskett', 'lees-maffei'],
    },
    {
        'key': 'counterculture-participation',
        'no': '08',
        'period': '1960s–1970s',
        'title': '消费社会、反文化与参与式设计',
        'thesis': '设计不再只追求秩序和效率；反文化、环境运动、女性主义和参与式实践质疑“专家替用户设计”的模式。',
        'context': '电视、青年文化、生态危机和社会运动使设计面对消费主义、战争、环境和公共参与的后果。',
        'actors': '激进设计团体、社区组织、环境运动、教育者、批判理论家、企业和公共机构。',
        'places': '意大利激进设计网络、美国和欧洲反文化社区、拉丁美洲社会设计项目。',
        'practices': ['参与式设计与社区工作', '环境设计和可持续性', '激进建筑与反设计', '出版、海报和独立媒介'],
        'turning_points': ['设计师开始公开质疑消费、战争和资源浪费。', '社区参与把使用者从调查对象变成共同决策者。', '环境和社会责任进入设计评价，而不再只是形式问题。'],
        'works': ['Superstudio 与 Archizoom 的激进设计', '维克多·帕帕奈克《为真实世界而设计》', '参与式社区规划与环境设计实践'],
        'debate': '参与并不自动平等；谁有时间、知识和资源参加设计过程，仍然决定了谁的声音被听见。',
        'legacy': '服务设计、社会创新、设计正义和可持续设计都继承了对用户、环境和制度的追问。',
        'source_keys': ['papanek', 'dunne-raby', 'costanza-chock'],
    },
    {
        'key': 'postmodern-diy',
        'no': '09',
        'period': '1970s–1980s',
        'title': '后现代、朋克与多元视觉政治',
        'thesis': '后现代和朋克拒绝单一的现代主义语法，把历史引用、挪用、噪声、手工复制和身份政治重新带回设计。',
        'context': '大众媒介、亚文化、经济转型和新印刷技术降低了制作门槛；设计成为质疑权威、制造身份和组织社群的工具。',
        'actors': '建筑师、平面设计师、音乐社群、独立出版者、时装设计师、青年文化和商业品牌。',
        'places': '米兰、伦敦、纽约、柏林和独立音乐/出版网络。',
        'practices': ['后现代建筑与家具', '朋克海报和唱片封面', '独立出版与 DIY 印刷', '挪用、拼贴和身份表达'],
        'turning_points': ['设计开始主动引用历史并承认风格的混杂。', '朋克用低成本复制和手工痕迹绕开专业出版体系。', '孟菲斯把消费品、家具、色彩和反功能结合成公开的设计争论。'],
        'works': ['孟菲斯集团 1981 年米兰展览', 'Jamie Reid 的朋克唱片与海报设计', '艾普里尔·格雷曼的数字拼贴实验'],
        'debate': '反叛风格很快被商业吸收；挪用和拼贴也涉及文化所有权与谁能代表谁的问题。',
        'legacy': '数字设计中的混合媒介、故障、模板改写和社群审美都继承了这一阶段的反规范方法。',
        'source_keys': ['jencks', 'sparke', 'meggs'],
    },
    {
        'key': 'desktop-digital',
        'no': '10',
        'period': '1980s–1990s',
        'title': '个人计算机、桌面出版与数字图形',
        'thesis': '个人计算机把排版、图像处理、建模和出版工具带到设计师桌面；设计开始面对软件默认值、屏幕像素、文件格式和界面操作。',
        'context': '图形用户界面、激光打印、PostScript、桌面出版和数字字体改变了设计生产链，也重新分配了专业门槛。',
        'actors': '软件工程师、字体设计师、平面设计师、出版商、计算机公司、用户研究者和业余创作者。',
        'places': '硅谷、纽约、伦敦、旧金山以及全球桌面出版网络。',
        'practices': ['数字排版和字体设计', '图像处理与数字拼贴', '图形用户界面', '软件工具和文件格式设计'],
        'turning_points': ['图形界面把文件、桌面、窗口和工具变成计算机的可视隐喻。', '桌面出版缩短了设计到印刷的距离，也扩大了非专业生产。', '数字设计把“媒介材料”从纸张扩展到像素、屏幕和软件状态。'],
        'works': ['Apple Macintosh 图形界面', 'Aldus PageMaker 与桌面出版流程', '数字字体和后现代数字排版实践'],
        'debate': '软件的可用性和默认模板既降低门槛，也可能把设计限制为软件允许的选项。',
        'legacy': '今天的响应式布局、设计系统和生成式工具仍然继承“设计规则被写进软件”的转向。',
        'source_keys': ['manovich', 'friedberg', 'moggridge'],
    },
    {
        'key': 'web-open-networks',
        'no': '11',
        'period': '1990s–2000s',
        'title': '网页、开放网络与交互设计',
        'thesis': '网页把设计从固定版面变成链接、导航、加载、输入和更新的时间性系统；设计对象不再只是页面，而是使用者与信息之间的路径。',
        'context': '互联网、浏览器、搜索引擎、开源软件和网络社区改变了出版、商业、协作和知识传播。',
        'actors': '网页设计师、程序员、信息架构师、浏览器公司、开源社群、媒体机构和网络用户。',
        'places': 'CERN、硅谷、全球大学网络、独立网页社区和商业互联网平台。',
        'practices': ['信息架构与导航', '网页排版和 CSS', '交互状态与表单', '开源协作与网络出版'],
        'turning_points': ['超文本把阅读从线性页面变成可跳转的关系网络。', '网页标准把语义、结构、样式和脚本分离。', '交互设计将等待、错误、输入和反馈纳入视觉系统。'],
        'works': ['早期 CERN 网页与超文本实践', '网页标准、浏览器和 CSS 生态', '开源项目与个人主页文化'],
        'debate': '开放网络同时带来知识共享、商业监控、数字鸿沟和平台集中；“开放”需要制度和基础设施支撑。',
        'legacy': '现代产品设计、服务设计、设计系统和前端工程都以网页的交互性为基础。',
        'source_keys': ['manovich', 'moggridge', 'turner'],
    },
    {
        'key': 'mobile-platform',
        'no': '12',
        'period': '2000s–2010s',
        'title': '移动设备、平台界面与设计系统',
        'thesis': '触屏、定位、传感器和应用商店把界面带入日常生活；设计开始同时处理屏幕尺寸、行为数据、平台规范和持续更新。',
        'context': '智能手机和云服务让界面成为服务入口；设计系统、组件库和跨设备响应成为团队生产的基础设施。',
        'actors': '交互设计师、产品团队、平台公司、开发者、用户研究者、无障碍倡导者和数据分析团队。',
        'places': '全球移动互联网市场、硅谷、东亚制造与软件生态、城市公共服务网络。',
        'practices': ['移动交互与触屏手势', '设计系统和组件库', '数据驱动产品迭代', '响应式和无障碍界面'],
        'turning_points': ['触屏取消了鼠标和键盘的部分中介，手势、反馈和可达性成为设计问题。', '平台规范把颜色、间距、组件和行为写成可复用规则。', '持续迭代让“完成的作品”变成长期运行的服务。'],
        'works': ['智能手机操作系统与应用界面', 'Material Design 与平台设计系统', '移动公共服务和地图/支付界面'],
        'debate': '平台设计既提高便利性，也会制造注意力剥削、隐私收集、成瘾机制和对少数用户的不平等。',
        'legacy': '当代设计必须同时讨论视觉语言、代码、数据、商业模型和用户权利。',
        'source_keys': ['norman', 'moggridge', 'costanza-chock'],
    },
    {
        'key': 'global-critical-design',
        'no': '13',
        'period': '2010s–2020s',
        'title': '全球设计、去殖民与设计正义',
        'thesis': '现代设计史不能只讲欧美先锋和企业系统；全球设计、原住民知识、地方生产、残障经验和设计正义重新追问谁有资格定义问题。',
        'context': '全球供应链、平台经济、气候危机和社会运动让设计的资源、劳动、数据和代表权变得不可回避。',
        'actors': '社区组织、地方工匠、设计正义实践者、残障社群、原住民知识持有者、平台公司和公共机构。',
        'places': '亚洲、非洲、拉丁美洲、中东、原住民社区与跨国数字网络。',
        'practices': ['参与式与社区设计', '设计研究和批判性设计', '可持续材料与循环生产', '无障碍、包容和数据正义'],
        'turning_points': ['设计研究开始反思殖民知识和专家中心的工作方式。', '社区和边缘社群要求参与定义问题，而不只是被测试。', '设计正义把资源、权力、劳动和伤害纳入设计评价。'],
        'works': ['设计正义工具与社区工作坊', '批判性/思辨设计项目', '循环材料、地方生产和社会创新项目'],
        'debate': '“全球设计”不能只把非西方案例作为风格素材；必须说明知识来源、利益分配和代表关系。',
        'legacy': '设计的完成标准从漂亮、有效、可售扩展到可参与、可维护、可问责。',
        'source_keys': ['costanza-chock', 'escobar', 'dunne-raby'],
    },
    {
        'key': 'ai-climate',
        'no': '14',
        'period': '2020s–现在',
        'title': '人工智能、生态约束与后平台设计',
        'thesis': '生成式人工智能和气候危机把设计推向新的边界：设计师不只制作形式，还要决定数据、能源、版权、劳动、可解释性和责任如何进入系统。',
        'context': '模型生成、自动化内容、云计算、芯片供应链和极端气候同时改变设计生产与使用环境。',
        'actors': '设计师、程序员、数据劳动者、模型公司、平台、艺术家、监管者、研究者和受影响社群。',
        'places': '全球云计算基础设施、数据标注网络、创意产业和受气候风险影响的社区。',
        'practices': ['生成式设计与人机协作', '模型界面和解释性', '低能耗与循环设计', '算法审计和责任设计'],
        'turning_points': ['生成系统把“制作”转为提示、筛选、编辑和责任判断。', '模型训练暴露了版权、数据劳动和文化偏见问题。', '气候和资源约束要求设计重新面对维护、寿命和能源。'],
        'works': ['生成式设计工具与模型界面', '气候适应和循环设计项目', '算法透明、无障碍和数据正义实践'],
        'debate': '“生成”不等于原创，也不等于中立；设计者必须说明数据来源、劳动关系、能耗和错误后果。',
        'legacy': '未来的现代设计史需要把计算系统当作材料，把责任和维护当作形式的一部分。',
        'source_keys': ['costanza-chock', 'escobar', 'norman'],
    },
]

BOOK_LENSES = [
    {
        'key': 'practice',
        'title': '设计实践与媒介',
        'summary': '通史不能只按风格分组，还要看设计在哪些职业、材料、机构和生产链中发生。',
        'items': ['字体与排版：从印刷、网格到数字字体和可变字体。', '产品与家具：材料、制造、维修、消费和工业设计职业。', '建筑、室内与展览：空间、公共信息、城市治理和身体经验。', '交互、服务与界面：从操作、导航到平台、数据和持续迭代。'],
    },
    {
        'key': 'global',
        'title': '地域、殖民与知识流动',
        'summary': '现代设计不是欧洲形式向世界单向扩散；技术、教育、材料、殖民制度和地方知识共同塑造不同现代性。',
        'items': ['东亚：日本工业与平面设计、中国现代化与视觉传播、韩国和东南亚数字产业。', '南亚、非洲、中东与拉丁美洲：教育、国家建设、地方生产和全球供应链。', '迁徙与翻译：设计师、学校、出版物和企业如何跨境移动并改变语境。', '去殖民与设计正义：谁被引用、谁被排除、谁承担设计后果。'],
    },
    {
        'key': 'method',
        'title': '如何读设计史',
        'summary': '每个章节应同时区分一手材料、后来的历史研究、作品分析和当代转译，避免把网络标签写成古典主义或把风格当作因果。',
        'items': ['时间：作品、机构和技术的具体年代，而不是只写“现代”。', '地点：生产、展览、教育和传播发生在哪里。', '证据：作品、档案、宣言、出版物、口述史和研究文献分别承担什么作用。', '争议：谁被遗漏、谁从中获益、哪些叙述仍然需要修正。'],
    },
]

BOOK_VOLUMES = [
    {'key': 'chronology', 'label': '卷 I', 'title': '现代设计通史', 'status': '14 个连续章节：工业化 → 平台与人工智能。'},
    {'key': 'practice', 'label': '卷 II', 'title': '设计实践史', 'status': '8 条媒介与职业线：从字体、产品到服务和界面。'},
    {'key': 'global', 'label': '卷 III', 'title': '全球设计史', 'status': '8 个区域与跨殖民网络，避免单向扩散叙事。'},
    {'key': 'thought', 'label': '卷 IV', 'title': '设计思想与方法', 'status': '课程母题、系统、参与、批判和设计正义。'},
    {'key': 'directions', 'label': '卷 V', 'title': '80 个设计方向档案', 'status': '方向索引层，不冒充通史主干。'},
    {'key': 'reference', 'label': '卷 VI', 'title': '作品、人物、机构与来源', 'status': '当前先接入机构索引和 18 条本地延伸阅读。'},
]

PRACTICE_FIELDS = [
    {'key': 'graphic', 'title': '平面设计与视觉传播', 'period': '印刷时代 → 屏幕时代', 'scope': '海报、书籍、杂志、广告、品牌和公共信息如何组织集体注意力。', 'production': '印刷、摄影、复制、出版、广告网络和数字文件格式。', 'question': '传播效率提高时，谁能发声，谁被宣传、审查或算法排序遮蔽？'},
    {'key': 'type', 'title': '字体、排版与阅读', 'period': '铅字 → 数字字体 → 可变字体', 'scope': '字形、版式、语言、阅读速度和无障碍共同构成信息的物质界面。', 'production': '铸字、印刷、字体软件、屏幕渲染和跨语言排版。', 'question': '中性字体真的中性吗？标准字符集和默认字体排除了谁？'},
    {'key': 'product', 'title': '产品与工业设计', 'period': '工厂制 → 全球供应链', 'scope': '产品把材料、制造、成本、维修、人体和消费承诺绑定在一起。', 'production': '模具、装配、标准件、材料供应、包装、物流和售后服务。', 'question': '产品的便利性由谁的劳动、资源和废弃物来支付？'},
    {'key': 'space', 'title': '建筑、室内与公共空间', 'period': '城市化 → 基础设施与平台空间', 'scope': '空间设计同时安排身体路径、公共信息、居住权和社会关系。', 'production': '建筑材料、施工、规划、住房制度、展览和导视。', 'question': '现代化的空间改造改善了谁的生活，又驱逐了谁？'},
    {'key': 'exhibition', 'title': '展览、博物馆与公共信息', 'period': '世界博览会 → 交互式知识界面', 'scope': '展览把物品、国家、技术和公众组织成可观看、可教育的叙事。', 'production': '展陈结构、标签、影像、导视、教育项目和数字交互。', 'question': '展示不是透明窗口：谁决定什么可以成为历史？'},
    {'key': 'image', 'title': '摄影、电影与动态图像', 'period': '机械复制 → 流媒体与生成图像', 'scope': '镜头和剪辑改变了设计如何安排证据、记忆、速度和身份。', 'production': '相机、胶片、印刷、剪辑软件、平台编码和模型生成。', 'question': '图像越容易复制，来源、版权和真实感如何被确认？'},
    {'key': 'interaction', 'title': '交互、界面与信息可视化', 'period': '控制面板 → 图形界面 → 平台', 'scope': '界面把操作、状态、反馈、错误和数据关系转译给使用者。', 'production': '硬件、软件、设计系统、传感器、数据和用户研究。', 'question': '可用性指标之外，界面怎样分配权力、注意力和风险？'},
    {'key': 'service', 'title': '服务、组织与制度设计', 'period': '公共服务 → 网络平台与算法治理', 'scope': '服务设计处理跨部门流程、等待、资格、劳动和长期维护。', 'production': '组织流程、政策、客服、基础设施、数据库和一线劳动。', 'question': '当服务被设计成“无摩擦”，被隐藏的劳动和申诉路径在哪里？'},
]

GLOBAL_REGIONS = [
    {'key': 'east-asia', 'title': '东亚与日本、中国、朝鲜半岛', 'period': '19 世纪后期 → 当代数字产业', 'route': '工业化、国家建设、印刷教育、战后制造和平台产业形成多条现代设计路径。', 'practices': '工艺改革、平面传播、产品制造、建筑现代化、动漫与数字界面。', 'tension': '不能把东亚只写成西方现代主义的接受者，也不能把地区差异压缩成“东方美学”。', 'source_keys': ['margolin', 'sparke']},
    {'key': 'south-asia', 'title': '南亚与印度洋网络', 'period': '殖民印刷 → 后殖民国家建设 → 当代服务设计', 'route': '教育、手工艺、国家规划、地方语言和全球软件产业交织在一起。', 'practices': '字体与多语种传播、工艺与产业、公共信息、设计教育和数字服务。', 'tension': '现代化项目常同时继承殖民分类、地方知识和全球市场，不能只用“传统/现代”二分。', 'source_keys': ['margolin', 'escobar']},
    {'key': 'soviet-east-europe', 'title': '苏联与东欧', 'period': '先锋传播 → 社会主义现代化 → 转型与数字文化', 'route': '构成主义、国家生产、公共住房和技术教育形成与西方企业设计不同的制度语境。', 'practices': '政治海报、工业产品、城市系统、标准化和公共视觉传播。', 'tension': '先锋形式不能脱离宣传制度、资源分配和国家权力来阅读。', 'source_keys': ['margolin', 'raizman']},
    {'key': 'latin-america', 'title': '拉丁美洲', 'period': '现代化国家 → 依附与社会设计 → 当代社区实践', 'route': '建筑、平面、教育和公共项目在国家现代化、地方生产与不平等之间寻找位置。', 'practices': '公共建筑、社会住房、出版、身份设计、社区和环境项目。', 'tension': '“国际风格”进入地方时会被重新翻译，设计史需记录依附关系和地方主动性。', 'source_keys': ['margolin', 'papanek', 'escobar']},
    {'key': 'africa', 'title': '非洲与非洲离散网络', 'period': '殖民视觉制度 → 独立国家 → 当代未来想象', 'route': '身份、城市、工艺、媒体和全球供应链共同塑造多种现代设计实践。', 'practices': '公共传播、纺织与材料、城市视觉、音乐文化、科技和 Afrofuturism。', 'tension': '不能只把非洲作为素材或风格来源；要追问生产权、知识权和设计师自身的位置。', 'source_keys': ['margolin', 'costanza-chock']},
    {'key': 'middle-east', 'title': '中东与北非', 'period': '现代国家建设 → 跨区域媒体 → 数字平台', 'route': '书写传统、建筑现代化、国家传播、战争与迁徙共同影响视觉和空间设计。', 'practices': '阿拉伯字体、公共建筑、出版、广播电视、身份系统和数字服务。', 'tension': '宗教、语言、国家和殖民边界不能被一套“中东风格”覆盖。', 'source_keys': ['margolin', 'escobar']},
    {'key': 'north-atlantic', 'title': '欧洲与北美工业网络', 'period': '工业化 → 企业系统 → 平台资本', 'route': '这是现代设计史的一条重要主干，但不是世界设计史的全部。', 'practices': '工艺改革、现代主义学校、工业设计、品牌、计算机和交互设计。', 'tension': '必须同时看殖民贸易、移民、女性劳动、阶级和全球供应链，避免把主导地位写成自然进步。', 'source_keys': ['raizman', 'forty', 'margolin']},
    {'key': 'colonial-circuits', 'title': '殖民、迁徙与跨国供应链', 'period': '展览帝国 → 全球制造 → 平台劳动', 'route': '材料、劳动力、图像、学校和设计规范沿不平等的跨国路径流动。', 'practices': '世界博览会、资源开采、服装制造、电子装配、数据标注和文化挪用。', 'tension': '跨文化传播既可能是翻译，也可能是抽取；来源和利益分配必须进入作品档案。', 'source_keys': ['forty', 'costanza-chock', 'escobar']},
]

DESIGN_INSTITUTIONS = [
    {'key': 'deutscher-werkbund', 'title': '德国制造联盟 Deutscher Werkbund', 'place': '德国', 'period': '1907 起', 'role': '连接艺术、工业、教育和国家经济的协会网络，推动设计与制造协作。', 'question': '标准化和民族工业目标如何与个体创作、工艺和市场发生冲突？', 'source_keys': ['raizman', 'margolin']},
    {'key': 'bauhaus', 'title': '包豪斯 Bauhaus', 'place': '魏玛、德绍、柏林', 'period': '1919–1933', 'role': '以基础课程、材料实验、建筑综合和工业协作重构设计教育。', 'question': '学校的教学神话如何遮蔽政治迁徙、性别分工和商业关系？', 'source_keys': ['raizman', 'lees-maffei']},
    {'key': 'ulm', 'title': '乌尔姆设计学院 Hochschule für Gestaltung Ulm', 'place': '乌尔姆', 'period': '1953–1968', 'role': '把设计教育与科学、工程、信息和系统分析连接起来。', 'question': '理性系统如何提高协作，又如何制造“中性”权威？', 'source_keys': ['raizman', 'heskett']},
    {'key': 'kelmscott', 'title': 'Kelmscott Press', 'place': '伦敦', 'period': '1891–1898', 'role': '以书籍、字体、纸张和印刷工艺回应工业复制，重新定义书籍作为整体设计。', 'question': '高质量手工出版如何面对价格、数量和可及性的现实？', 'source_keys': ['forty', 'adamson']},
    {'key': 'nid', 'title': '印度国家设计学院 National Institute of Design', 'place': '艾哈迈达巴德', 'period': '20 世纪 60 年代起', 'role': '在后殖民国家建设、工艺、工业和设计教育之间建立制度联系。', 'question': '国际现代主义如何在地方语言、材料和社会需求中被重新解释？', 'source_keys': ['margolin', 'escobar']},
    {'key': 'cervantes', 'title': '公共文化与设计展览网络', 'place': '跨城市', 'period': '19 世纪博览会 → 当代双年展', 'role': '展览和博物馆把设计、技术、国家身份与公众教育组织成可见叙事。', 'question': '展览选择和标签如何塑造“谁代表现代”的历史？', 'source_keys': ['margolin', 'lees-maffei']},
    {'key': 'cern-web', 'title': 'CERN 与早期万维网', 'place': '日内瓦附近', 'period': '1989–1990s', 'role': '超文本、网页标准和网络出版改变了信息组织与设计生产的边界。', 'question': '开放协议如何与后来浏览器、平台和商业基础设施共存？', 'source_keys': ['manovich', 'moggridge']},
    {'key': 'mit-media-lab', 'title': 'MIT Media Lab', 'place': '剑桥（马萨诸塞州）', 'period': '1985 起', 'role': '把计算、媒介、交互和实验性原型放进跨学科研究环境。', 'question': '实验室原型如何转化为公共技术，而不只成为企业创新叙事？', 'source_keys': ['moggridge', 'turner']},
]

BOOK_SOURCES = [
    {'key': 'forty', 'title': 'Objects of Desire: Design and Society since 1750', 'author': 'Adrian Forty', 'year': '1986', 'publisher': 'Thames & Hudson', 'why': '把物品、生产、消费和社会价值联系起来，适合支撑工业化、消费社会和产品设计章节。'},
    {'key': 'margolin', 'title': 'World History of Design', 'author': 'Victor Margolin', 'year': '2015–2017', 'publisher': 'Bloomsbury Academic', 'why': '提供跨时期、跨地域的设计史框架，提醒通史不能只围绕欧美先锋叙述。'},
    {'key': 'raizman', 'title': 'A History of Modern Design', 'author': 'David Raizman', 'year': '2003', 'publisher': 'Laurence King', 'why': '覆盖现代设计的学校、运动、职业和制度变化，是时间主干的基础读物。'},
    {'key': 'meggs', 'title': "Meggs' History of Graphic Design", 'author': 'Philip B. Meggs and Alston W. Purvis', 'year': '2016', 'publisher': 'Wiley, 6th ed.', 'why': '补足平面设计、字体、印刷、摄影、广告和数字传播，而不是只看建筑或产品。'},
    {'key': 'sparke', 'title': 'An Introduction to Design and Culture: 1900 to the Present', 'author': 'Penny Sparke', 'year': '2004', 'publisher': 'Routledge', 'why': '把设计放回日常生活、消费文化、性别和现代文化生产中。'},
    {'key': 'lees-maffei', 'title': 'Design History: Understanding Theory and Method', 'author': 'Grace Lees-Maffei and Rebecca Houze, eds.', 'year': '2010', 'publisher': 'Berg', 'why': '提供设计史研究的方法、档案和学科边界，避免把网站内容写成无来源的风格目录。'},
    {'key': 'adamson', 'title': 'The Invention of Craft', 'author': 'Glenn Adamson', 'year': '2013', 'publisher': 'Bloomsbury Academic', 'why': '帮助区分工艺、手工、工业生产和现代设计制度，不把“手工”浪漫化。'},
    {'key': 'heskett', 'title': 'Toothpicks and Logos: Design in Everyday Life', 'author': 'John Heskett', 'year': '2002', 'publisher': 'Oxford University Press', 'why': '从日常物品和生产系统解释设计如何进入生活，而不仅是博物馆作品。'},
    {'key': 'papanek', 'title': 'Design for the Real World', 'author': 'Victor Papanek', 'year': '1971', 'publisher': 'Pantheon Books', 'why': '支撑社会责任、环境、消费批判和设计伦理章节。'},
    {'key': 'norman', 'title': 'The Design of Everyday Things', 'author': 'Donald A. Norman', 'year': '2013', 'publisher': 'Basic Books, revised ed.', 'why': '连接工业设计、人因、可理解性、错误恢复和交互设计。'},
    {'key': 'manovich', 'title': 'The Language of New Media', 'author': 'Lev Manovich', 'year': '2001', 'publisher': 'MIT Press', 'why': '解释数字媒介、数据库、界面、模块性和可编程性如何改变设计对象。'},
    {'key': 'friedberg', 'title': 'The Virtual Window: From Alberti to Microsoft', 'author': 'Anne Friedberg', 'year': '2006', 'publisher': 'MIT Press', 'why': '把窗口、屏幕和视觉框架放进更长的视觉媒介史。'},
    {'key': 'moggridge', 'title': 'Designing Interactions', 'author': 'Bill Moggridge', 'year': '2007', 'publisher': 'MIT Press', 'why': '补足交互设计职业、案例、原型和人机关系的历史。'},
    {'key': 'turner', 'title': 'From Counterculture to Cyberculture', 'author': 'Fred Turner', 'year': '2006', 'publisher': 'University of Chicago Press', 'why': '解释反文化、个人计算机和网络想象之间的社会与思想联系。'},
    {'key': 'dunne-raby', 'title': 'Speculative Everything: Design, Fiction, and Social Dreaming', 'author': 'Anthony Dunne and Fiona Raby', 'year': '2013', 'publisher': 'MIT Press', 'why': '支撑批判性设计、思辨设计和设计不只解决问题的传统。'},
    {'key': 'costanza-chock', 'title': 'Design Justice: Community-Led Practices to Build the Worlds We Need', 'author': 'Sasha Costanza-Chock', 'year': '2020', 'publisher': 'MIT Press', 'why': '补足参与、权力、残障、种族、社区和设计正义。'},
    {'key': 'escobar', 'title': 'Designs for the Pluriverse', 'author': 'Arturo Escobar', 'year': '2018', 'publisher': 'Duke University Press', 'why': '提供去殖民、地方知识、多元世界和设计政治的理论入口。'},
    {'key': 'jencks', 'title': 'The Language of Post-Modern Architecture', 'author': 'Charles Jencks', 'year': '1977', 'publisher': 'Rizzoli', 'why': '支撑后现代对现代主义单一语言的批判及其建筑与视觉扩散。'},
]


_REQUIRED_CHAPTER_FIELDS = {'key', 'no', 'period', 'title', 'thesis', 'context', 'actors', 'places', 'practices', 'turning_points', 'works', 'debate', 'legacy', 'source_keys'}
if len(BOOK_CHAPTERS) != 14:
    raise ValueError(f'通史主干应有 14 个章节，实际为 {len(BOOK_CHAPTERS)}')
for chapter in BOOK_CHAPTERS:
    if set(chapter) != _REQUIRED_CHAPTER_FIELDS:
        raise ValueError(f"通史章节 {chapter.get('key')} 字段不完整: {sorted(set(chapter) ^ _REQUIRED_CHAPTER_FIELDS)}")

_source_keys = {source['key'] for source in BOOK_SOURCES}
for chapter in BOOK_CHAPTERS:
    missing = sorted(set(chapter['source_keys']) - _source_keys)
    if missing:
        raise ValueError(f"通史章节 {chapter['key']} 引用了不存在的来源: {missing}")

if len(BOOK_LENSES) != 3 or any(set(lens) != {'key', 'title', 'summary', 'items'} for lens in BOOK_LENSES):
    raise ValueError('全书横向阅读视角字段不完整')

_ARCHIVE_FIELDS = {
    'practice': {'key', 'title', 'period', 'scope', 'production', 'question'},
    'global': {'key', 'title', 'period', 'route', 'practices', 'tension', 'source_keys'},
    'institution': {'key', 'title', 'place', 'period', 'role', 'question', 'source_keys'},
}
if len(BOOK_VOLUMES) != 6 or any(set(volume) != {'key', 'label', 'title', 'status'} for volume in BOOK_VOLUMES):
    raise ValueError('全书六卷结构字段不完整')
for archive_name, archive_items in [('practice', PRACTICE_FIELDS), ('global', GLOBAL_REGIONS), ('institution', DESIGN_INSTITUTIONS)]:
    if not archive_items or any(set(item) != _ARCHIVE_FIELDS[archive_name] for item in archive_items):
        raise ValueError(f'{archive_name} 档案字段不完整')
for archive_name, archive_items in [('global', GLOBAL_REGIONS), ('institution', DESIGN_INSTITUTIONS)]:
    for item in archive_items:
        missing = sorted(set(item['source_keys']) - _source_keys)
        if missing:
            raise ValueError(f"{archive_name} 档案 {item['key']} 引用了不存在的来源: {missing}")
