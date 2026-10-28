# -*- coding: utf-8 -*-
"""通史章节的结构化档案坐标。

这些条目把章节中的概括性作品线索拆成时间、地点、人物、机构和设计
作用，作为读者继续查档的入口；它们不是完整馆藏目录，具体版本、馆藏
编号和页码仍需逐条核验。
"""

from book_data import BOOK_CHAPTERS, BOOK_SOURCES

CHAPTER_ARCHIVES = {
    'industrial-modernity': [
        {'kind': '展览', 'title': '1851 年伦敦万国工业博览会与水晶宫', 'date': '1851', 'place': '伦敦·海德公园', 'people': '亨利·科尔、约瑟夫·帕克斯顿及博览会组织网络', 'institution': '英国皇家艺术、制造与商业促进机构', 'role': '把工业产品、国家竞争、公共教育和玻璃/铁结构放进同一个大众展场。', 'source_keys': ['forty', 'margolin']},
        {'kind': '住宅 / 工艺', 'title': 'Red House 红屋', 'date': '1859–1860', 'place': '英国·贝克斯利希思', 'people': '威廉·莫里斯、菲利普·韦布', 'institution': '莫里斯工作室与工艺生产网络', 'role': '把建筑、家具、壁纸和日常使用作为整体环境问题，回应工业化生产。', 'source_keys': ['forty', 'adamson']},
        {'kind': '出版 / 延伸', 'title': 'Kelmscott Press', 'date': '1891 起（后续延伸）', 'place': '伦敦·汉默史密斯', 'people': '威廉·莫里斯、爱德华·伯恩-琼斯等', 'institution': 'Kelmscott Press', 'role': '把工艺批评转化为字体、纸张、插图和印刷流程的出版实践。', 'source_keys': ['adamson', 'meggs']},
    ],
    'decorative-modernities': [
        {'kind': '建筑', 'title': '塔塞尔住宅 Hôtel Tassel', 'date': '1892–1893', 'place': '比利时·布鲁塞尔', 'people': '维克多·奥塔', 'institution': '私人住宅与新艺术建筑实践', 'role': '以铁、玻璃、曲线和室内整体设计回应新的城市住宅生活。', 'source_keys': ['raizman', 'sparke']},
        {'kind': '学校 / 建筑', 'title': '格拉斯哥艺术学院', 'date': '1897–1909', 'place': '英国·格拉斯哥', 'people': '查尔斯·雷尼·麦金托什', 'institution': 'Glasgow School of Art', 'role': '把建筑结构、家具、光线和图案作为同一个空间系统处理。', 'source_keys': ['raizman', 'sparke']},
        {'kind': '企业系统', 'title': 'AEG 的建筑、产品与识别实践', 'date': '1907 起', 'place': '德国·柏林及工业网络', 'people': '彼得·贝伦斯及 AEG 设计团队', 'institution': 'AEG / 德国制造联盟网络', 'role': '将企业建筑、产品、电器广告和视觉识别纳入工业组织。', 'source_keys': ['raizman', 'margolin']},
    ],
    'avant-garde-propaganda': [
        {'kind': '宣言 / 出版', 'title': '《未来主义宣言》', 'date': '1909', 'place': '巴黎·《费加罗报》传播', 'people': '菲利波·托马索·马里内蒂', 'institution': '未来主义杂志与宣言网络', 'role': '用宣言、速度、机械和城市经验把艺术立场变成可复制的公共传播。', 'source_keys': ['meggs', 'margolin']},
        {'kind': '剧场 / 社群', 'title': 'Cabaret Voltaire 与达达', 'date': '1916', 'place': '瑞士·苏黎世', 'people': '雨果·巴尔、艾米·亨宁斯及达达社群', 'institution': 'Cabaret Voltaire', 'role': '通过表演、声音、拼贴和出版反对稳定的艺术语言与战争秩序。', 'source_keys': ['margolin', 'meggs']},
        {'kind': '海报 / 政治传播', 'title': '《用红色楔子击入白军》', 'date': '1919', 'place': '俄国革命传播网络', 'people': '埃尔·利西茨基', 'institution': '革命海报与印刷传播机构', 'role': '将几何形、文字方向、颜色对立和政治行动压缩成可扩散图像。', 'source_keys': ['meggs', 'margolin']},
    ],
    'schools-and-systems': [
        {'kind': '学校', 'title': '包豪斯成立与魏玛课程', 'date': '1919', 'place': '德国·魏玛', 'people': '沃尔特·格罗皮乌斯、教师与学生群体', 'institution': 'Bauhaus', 'role': '把基础课程、材料实验、工艺和建筑综合成可教学的设计方法。', 'source_keys': ['raizman', 'lees-maffei']},
        {'kind': '建筑 / 学校', 'title': '包豪斯德绍校舍', 'date': '1925–1926', 'place': '德国·德绍', 'people': '沃尔特·格罗皮乌斯与包豪斯团队', 'institution': 'Bauhaus Dessau', 'role': '让建筑、家具、标识、空间使用和学校组织成为现代主义教育的可见系统。', 'source_keys': ['raizman', 'margolin']},
        {'kind': '出版 / 字体', 'title': '《新字体》 Die neue Typographie', 'date': '1928', 'place': '德国·柏林传播', 'people': '扬·奇肖尔德', 'institution': '现代版式与印刷出版网络', 'role': '将非对称构成、无衬线字体、网格和信息层级写成可讨论的方法。', 'source_keys': ['meggs', 'raizman']},
    ],
    'industrial-consumer-design': [
        {'kind': '产品', 'title': 'Coldspot 冰箱设计', 'date': '1934', 'place': '美国·家电市场', 'people': '雷蒙德·罗维与设计团队', 'institution': 'Sears / 冷藏设备生产与零售网络', 'role': '显示外观、品牌、工程、销售和消费欲望如何共同构成工业产品。', 'source_keys': ['heskett', 'forty']},
        {'kind': '展览 / 想象', 'title': 'Futurama 未来城市展项', 'date': '1939', 'place': '美国·纽约世界博览会', 'people': '诺曼·贝尔·盖德斯与 General Motors', 'institution': '1939 New York World’s Fair', 'role': '用模型、交通和基础设施叙事把企业技术包装成可观看的未来生活。', 'source_keys': ['forty', 'raizman']},
        {'kind': '出版 / 交通', 'title': 'Magic Motorways', 'date': '1940', 'place': '美国·全国公路想象', 'people': '诺曼·贝尔·盖德斯', 'institution': '工业设计、汽车和公共基础设施传播', 'role': '把道路、汽车、城市秩序和消费现代性连接成一套视觉化方案。', 'source_keys': ['heskett', 'forty']},
    ],
    'war-reconstruction': [
        {'kind': '制度 / 重建', 'title': '战后公共住房与城市重建项目', 'date': '1945–1955', 'place': '欧洲重建城市及跨国援助网络', 'people': '建筑师、工程师、政府住房机构与居民组织', 'institution': '公共住房、城市规划和重建机构', 'role': '让材料配给、标准构件、卫生、交通和居住权进入设计决策。', 'source_keys': ['margolin', 'papanek']},
        {'kind': '产品 / 材料', 'title': '模压胶合板与战后家具实验', 'date': '1940s–1950s', 'place': '美国·洛杉矶及工业生产网络', 'people': '查尔斯与雷·伊姆斯', 'institution': '家具制造商与材料研发团队', 'role': '把战时材料技术转译为可批量生产、贴合身体并进入家庭的产品。', 'source_keys': ['raizman', 'heskett']},
        {'kind': '公共信息', 'title': '战后国际展览与现代化传播', 'date': '1945–1960', 'place': '欧洲、美洲与亚洲城市', 'people': '政府、设计学校、国际组织和展览团队', 'institution': '国际展览与公共传播系统', 'role': '以展览、导视和宣传把重建、技术和国家现代化变成可见叙事。', 'source_keys': ['margolin', 'sparke']},
    ],
    'systems-corporate-identity': [
        {'kind': '学校 / 制度', 'title': '乌尔姆设计学院', 'date': '1953–1968', 'place': '德国·乌尔姆', 'people': '马克斯·比尔、奥托·艾舍、汤姆ás·马尔多纳多等', 'institution': 'Hochschule für Gestaltung Ulm', 'role': '把设计教育连接到工程、信息、科学和系统分析。', 'source_keys': ['raizman', 'lees-maffei']},
        {'kind': '字体', 'title': 'Helvetica', 'date': '1957', 'place': '瑞士·明兴与苏黎世字体网络', 'people': '马克斯·米丁格、爱德华·霍夫曼', 'institution': 'Haas 字体铸造厂', 'role': '成为跨语言传播、企业识别和公共导视中可复制的字体基础设施。', 'source_keys': ['meggs', 'raizman']},
        {'kind': '产品 / 系统', 'title': 'Braun SK 4 唱机与收音机', 'date': '1956', 'place': '德国·克朗贝格', 'people': '汉斯·古格洛特、迪特·拉姆斯', 'institution': 'Braun', 'role': '把产品结构、操作界面、材料和企业设计规范组织成连续系统。', 'source_keys': ['heskett', 'raizman']},
    ],
    'counterculture-participation': [
        {'kind': '出版 / 社群', 'title': 'Whole Earth Catalog', 'date': '1968 起', 'place': '美国·加州及反文化网络', 'people': '斯图尔特·布兰德与编辑社群', 'institution': 'Whole Earth Catalog', 'role': '把工具、生态、社区、自给和信息共享放进一份可流通的设计资源目录。', 'source_keys': ['papanek', 'turner']},
        {'kind': '建筑 / 思辨', 'title': 'Superstudio《连续纪念碑》', 'date': '1969', 'place': '意大利·佛罗伦萨设计网络', 'people': 'Superstudio 团体', 'institution': '激进建筑与设计出版网络', 'role': '用不可居住的网格想象质疑功能主义、城市扩张和消费环境。', 'source_keys': ['dunne-raby', 'sparke']},
        {'kind': '出版 / 伦理', 'title': '《为真实世界而设计》', 'date': '1971', 'place': '欧美设计教育传播', 'people': '维克多·帕帕奈克', 'institution': '设计教育与社会责任讨论网络', 'role': '将生态、残障、战争、消费和设计职业责任放进同一批判框架。', 'source_keys': ['papanek', 'lees-maffei']},
    ],
    'postmodern-diy': [
        {'kind': '展览 / 团体', 'title': '孟菲斯集团首展', 'date': '1981', 'place': '意大利·米兰', 'people': '埃托雷·索特萨斯与孟菲斯成员', 'institution': 'Memphis Milano', 'role': '用历史引用、强色彩、装饰和反功能挑战现代主义的单一语法。', 'source_keys': ['jencks', 'sparke']},
        {'kind': '音乐 / 海报', 'title': '《God Save the Queen》唱片封面', 'date': '1977', 'place': '英国·朋克出版与音乐网络', 'people': 'Jamie Reid、Sex Pistols', 'institution': '独立唱片与朋克社群', 'role': '用拼贴、挪用和低成本复制制造反权威的视觉身份。', 'source_keys': ['meggs', 'sparke']},
        {'kind': '海报 / 数字排版', 'title': 'Does It Make Sense?', 'date': '1986', 'place': '美国·旧金山设计网络', 'people': '艾普里尔·格雷曼', 'institution': '数字图形与设计教育网络', 'role': '把扫描、低分辨率、分层文字和数字失真带入平面设计。', 'source_keys': ['meggs', 'manovich']},
    ],
    'desktop-digital': [
        {'kind': '软件 / 语言', 'title': 'PostScript', 'date': '1982', 'place': '美国·硅谷与印刷产业', 'people': 'Adobe 工程与字体团队', 'institution': 'Adobe Systems', 'role': '把页面、字体和图形描述为可传输、可输出的数字指令。', 'source_keys': ['manovich', 'meggs']},
        {'kind': '设备 / 界面', 'title': 'Apple Macintosh', 'date': '1984', 'place': '美国·加州', 'people': 'Apple 设计与工程团队', 'institution': 'Apple', 'role': '以桌面、窗口、图标和鼠标把计算操作转译为可视化工作环境。', 'source_keys': ['friedberg', 'manovich']},
        {'kind': '软件 / 出版', 'title': 'Aldus PageMaker', 'date': '1985', 'place': '美国·桌面出版市场', 'people': 'Aldus 软件团队', 'institution': 'Aldus / 桌面出版生态', 'role': '让排版、图像和打印流程进入个人计算机，重新分配出版门槛。', 'source_keys': ['meggs', 'manovich']},
    ],
    'web-open-networks': [
        {'kind': '提案 / 协议', 'title': '万维网提案', 'date': '1989', 'place': '瑞士·CERN', 'people': '蒂姆·伯纳斯-李', 'institution': 'CERN 信息系统网络', 'role': '把超文本、地址、浏览器和服务器组织成开放的信息交换系统。', 'source_keys': ['manovich', 'moggridge']},
        {'kind': '网页 / 发布', 'title': '第一个网站与早期网页标准', 'date': '1991 起', 'place': 'CERN 与全球大学网络', 'people': 'CERN 网页协作者', 'institution': 'World Wide Web / CERN', 'role': '网页从研究基础设施变成可链接、可更新、可复制的公共媒介。', 'source_keys': ['manovich', 'turner']},
        {'kind': '浏览器 / 社群', 'title': 'Mosaic 浏览器', 'date': '1993', 'place': '美国·NCSA', 'people': 'NCSA 浏览器团队', 'institution': 'National Center for Supercomputing Applications', 'role': '图像、链接、窗口和鼠标操作降低了网络阅读与出版的门槛。', 'source_keys': ['manovich', 'moggridge']},
    ],
    'mobile-platform': [
        {'kind': '设备 / 界面', 'title': '第一代 iPhone', 'date': '2007', 'place': '美国·全球移动市场', 'people': 'Apple 硬件、软件与交互团队', 'institution': 'Apple / App Store 生态', 'role': '把触屏、传感器、移动网络和应用服务整合为日常界面。', 'source_keys': ['norman', 'moggridge']},
        {'kind': '方法 / 网页', 'title': 'Responsive Web Design', 'date': '2010', 'place': '全球网页设计网络', 'people': 'Ethan Marcotte', 'institution': '网页标准与前端社区', 'role': '用流动网格、弹性图像和媒体查询回应多尺寸设备。', 'source_keys': ['moggridge', 'manovich']},
        {'kind': '系统 / 组件', 'title': 'Material Design', 'date': '2014', 'place': '全球 Android 与 Google 服务', 'people': 'Google 设计团队', 'institution': 'Google', 'role': '把颜色、层级、组件、动效和状态写成跨产品设计系统。', 'source_keys': ['norman', 'moggridge']},
    ],
    'global-critical-design': [
        {'kind': '学校 / 制度', 'title': '印度国家设计学院 NID', 'date': '1961 起（历史回溯）', 'place': '印度·艾哈迈达巴德', 'people': '设计教育者、工艺者和工业合作网络', 'institution': 'National Institute of Design', 'role': '在后殖民国家建设中连接设计教育、工艺、工业和地方语言。', 'source_keys': ['margolin', 'escobar']},
        {'kind': '理论 / 书籍', 'title': 'Designs for the Pluriverse', 'date': '2018', 'place': '拉丁美洲与跨地域设计研究', 'people': 'Arturo Escobar', 'institution': '去殖民设计与社会运动网络', 'role': '质疑单一现代化方案，强调多元世界、地方知识和共同设计。', 'source_keys': ['escobar', 'costanza-chock']},
        {'kind': '社群 / 方法', 'title': 'Design Justice 社区实践', 'date': '2010s–2020s', 'place': '跨地域社区与数字网络', 'people': 'Sasha Costanza-Chock 与社区设计者', 'institution': 'Design Justice Network', 'role': '把参与、残障、种族、资源分配和谁承担设计后果放进方法核心。', 'source_keys': ['costanza-chock', 'lees-maffei']},
    ],
    'ai-climate': [
        {'kind': '模型 / 界面', 'title': '生成式人工智能对话界面', 'date': '2020s', 'place': '全球云计算与软件服务网络', 'people': '模型研究者、设计师、数据劳动者和使用者', 'institution': '模型公司、平台与开源社群', 'role': '把制作转为提示、筛选、编辑、溯源和错误责任的协作流程。', 'source_keys': ['norman', 'costanza-chock']},
        {'kind': '政策 / 责任', 'title': '算法透明、版权与数据劳动讨论', 'date': '2020s', 'place': '跨国平台、创意产业与监管网络', 'people': '艺术家、设计师、研究者、劳动者和监管者', 'institution': '平台治理与公共政策机构', 'role': '把训练数据、能源、版权、偏见、劳动和可解释性纳入设计评价。', 'source_keys': ['costanza-chock', 'escobar']},
        {'kind': '材料 / 生态', 'title': '循环设计与气候适应项目', 'date': '2020s', 'place': '受资源与气候风险影响的社区', 'people': '社区组织、工程师、设计师和维护者', 'institution': '地方生产、公共基础设施与循环经济网络', 'role': '把寿命、维修、能源、材料来源和长期维护从附加要求变成设计条件。', 'source_keys': ['papanek', 'escobar']},
    ],
}

_REQUIRED_ARCHIVE_FIELDS = {'kind', 'title', 'date', 'place', 'people', 'institution', 'role', 'source_keys'}
_chapter_keys = {chapter['key'] for chapter in BOOK_CHAPTERS}
_source_keys = {source['key'] for source in BOOK_SOURCES}
if set(CHAPTER_ARCHIVES) != _chapter_keys:
    raise ValueError('结构化档案必须覆盖全部通史章节')
for chapter_key, entries in CHAPTER_ARCHIVES.items():
    if len(entries) < 2 or any(set(entry) != _REQUIRED_ARCHIVE_FIELDS for entry in entries):
        raise ValueError(f'章节档案字段不足: {chapter_key}')
    for entry in entries:
        missing = sorted(set(entry['source_keys']) - _source_keys)
        if missing:
            raise ValueError(f"章节档案 {entry['title']} 引用了不存在的来源: {missing}")
