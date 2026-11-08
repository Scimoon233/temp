"""Chinese reading version of the three-page English course essay; no new modelling."""
from pathlib import Path
import re,hashlib,json
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'course_essay_zh';OUT.mkdir(exist_ok=True)
source=ROOT/'course_essay/Hangzhou_Passive_Cooling_Course_Essay.md'
en=source.read_text()
refs=en.split('## References\n\n',1)[1]
tablelines=[line for line in en.splitlines() if line.startswith('|202')]
assert len(tablelines)==8
rows=[[c.strip() for c in line.strip('|').split('|')] for line in tablelines]
text = '# 杭州住宅原型的外遮阳与夜间通风：夏季过热与显热制冷需求\n中文审阅版｜对应英文课程短论文；数据、结论及参考文献保持一致。\n\n## 摘要\n本研究评价外遮阳与温差控制夜间通风对杭州住宅原型夏季过热和显热制冷需求的改善。两热区RC模型采用2025、2026年逐小时天气，在自由运行和26°C理想制冷两种条件下比较基准、遮阳、通风及组合情景。相对基准，组合措施使自由运行平均空气温度降低1.85—2.12°C、超过28°C的过热度时降低17.5%—17.7%，并使理想显热制冷需求降低6.44%—7.01%。在基准假设下，单项措施中夜间通风对减轻过热更有效，遮阳对降低制冷需求更有效。组合措施在20套测试输入中均取得最低的过热度时和制冷需求。结果支持联合采用白天太阳控制与夜间排热：当室外温度至少比室内低1°C时通风，并在理想制冷运行下优先以遮阳降低需求。\n\n## 1 引言\n被动降温通过减少得热、利用较凉室外空气排出蓄热改善夏季表现。Short等（2018）讨论杭州公寓的太阳暴露、封闭阳台和通风；Artmann等（2008）指出天气、气流及蓄热影响夜间降温。本文贡献是在统一住宅与天气框架内比较自由运行与26°C理想制冷，量化遮阳和夜间通风对过热、显热需求的不同作用，并检验组合收益的稳定性，为措施配置提供依据。\n\n## 2 研究方法\n根据公开户型图（HZXQF，无日期）建立41.1 m²居住区与独立6.3 m²封闭阳台原型。高度假设为2.7 m，体积为110.97和17.01 m³。两区空气充分混合，隔断关闭；水平边界及两段朝东墙体取绝热。对外整窗面积假设为3.525和14.07 m²。每区设空气与有效蓄热节点，热平衡包括围护传热、通风、区间交换、分配得热及制冷。\n墙体热阻采用Short等（2018，补充材料表S1）的分层资料；有效热容量密度独立假设为165 kJ/(m²·K)。整窗U值6.7 W/(m²·K)、SHGC 0.70代表透明单玻铝框窗（NSW Government，无日期）。关窗／开窗总换气率0.44／1.51次每小时取自Hou等（2019，表6）的夏季夜间卧室中位值，用于本研究两区属于假设。居住区内部得热18:00—08:00取16.7 W/m²，其余取30%；数值参考Short等，时序独立假设。\nOpen-Meteo提供每个夏季2208条逐小时ERA5记录，按UTC+8与源辐射时段对齐（Open-Meteo，无日期）。立面辐射包括直射、各向同性散射和地面反射。假设阳台透入太阳得热的25%分配至居住区，其余留在阳台。数据对齐、初始化和诊断计算详见配套可复现资料。\nS0为背景通风；S1削减窗面50%太阳直射；S2启用夜间通风；S3结合两项措施。21:00—07:00各区在室内至少比室外高1 K时独立切换至开窗换气率。自由运行过热度时DH28＝Σmax(Tin−28,0)Δt，单位K·h。独立理想模拟对居住区施加全天可用的26°C上限，累计显热移除量，单位kWh_th，不含潜热负荷和设备用电。\n后向Euler法采用300 s步长及28天预热。2025年基准步长减半后，关键累计指标变化小于0.006%；平衡及初始化检查通过。20套离散输入考察气流、热容量、窗户、遮阳等假设，每套与自身S0比较。\n\n## 3 结果\n表1 基准四情景比较；制冷量表示理想条件下的显热移除量。\nTABLE_PLACEHOLDER\nDH28对应自由运行；制冷需求降低率均相对于同一年的S0。\n三种措施均改善基准表现（表1）。2025年，S3使自由运行平均空气温度由40.04°C降至37.92°C；2026年由38.36°C降至36.51°C，分别降低2.12°C和1.85°C，DH28降低17.5%和17.7%。基准假设下，夜间通风对DH28的降低优于遮阳，遮阳对理想需求的降低更大。S3在2208小时中仍有2172.0和2179.8小时过热，主要收益是过热强度下降。\nS3使2025、2026年理想需求分别减少263.2和213.2 kWh_th（7.01%和6.44%）。20套输入及两个夏季中，S3的DH28和需求均最低，单项排序有所变化。相对于每套输入自身基准，组合的DH28降低率为10.86%—28.06%，需求降低率为3.63%—13.43%。这些范围描述所测试设置。组合制冷收益接近相加，并有轻微递减。\n\n## 4 讨论\n结果支持减少白天太阳输入，并在较凉夜间排热。自由运行S2和S3中，居住区通风覆盖全部920小时夜间窗口；理想制冷时，两年仅164和206小时满足开窗规则。室内接近26°C时，室外通常需接近或低于25°C，才能满足1 K温差。因此，基准26°C运行时序下，遮阳是降低需求的主要措施，通风在较凉空气可用时提供补充。\n2025年，居住区通过自身外窗和阳台太阳分配分别获得457.7、507.9 kWh_th，同时经隔断向阳台净传递243.7 kWh_th。这些路径支持在太阳控制中纳入阳台玻璃，并保留其缓冲区换热。\n较高的基准温度与峰值（50.11°C和47.84°C）反映了规定的太阳暴露、得热和边界。2025年一组边界对照采用1 m挑檐、内部得热减半及阳台二次太阳分配为零，S0平均温度为36.18°C，表明热输入假设对绝对预测的重要性。模型未经实测校准，采用聚合蓄热和固定气流，忽略天空长波交换与潜热负荷；湿度、降雨、安全和噪声也影响实施。\n\n## 5 结论\n对于本研究的杭州住宅原型，外遮阳与夜间通风组合使夏季自由运行平均空气温度降低1.85—2.12°C、超过28°C的过热度时降低17.5%—17.7%，并使26°C理想显热制冷需求降低6.44%—7.01%。组合措施在20套测试输入中均排名第一，支持在所研究条件下联合采用两项措施。\n由此形成的设计优先顺序是：通过外遮阳减少白天太阳得热，并在室外温度至少比室内低1 K时，利用夜间通风提供附加排热。这种协调策略能够缓解夏季过热，并降低主动系统需要承担的显热制冷量。\n\n## 参考文献\nREFERENCES_PLACEHOLDER\n\n'
headers=['年份','情景','DH28（K·h）','制冷量（kWh_th）','制冷降低率（%）']
mdtable='|'+'|'.join(headers)+'|\n|'+'|'.join(['---']*5)+'|\n'+'\n'.join('|'+'|'.join(r)+'|' for r in rows)
text=text.replace('TABLE_PLACEHOLDER',mdtable).replace('REFERENCES_PLACEHOLDER',refs.strip())
(OUT/'杭州住宅被动降温_英文短稿对应中文版.md').write_text(text)

from journal_course_layout import build_chinese
build_chinese(ROOT, OUT, text, rows)
# Translation checks: table rows copied exactly; key reported values must remain.
for value in ['17.5%', '17.7%', '7.01%', '6.44%', '2.12°C', '1.85°C', '40.04°C', '37.92°C', '38.36°C', '36.51°C', '10.86%', '28.06%', '3.63%', '13.43%', '36.18°C', '2172.0', '2179.8', '164', '206', '50.11°C', '47.84°C', '457.7', '507.9', '243.7', '0.006%']:
 assert value in text,value
assert refs.strip() in text
status={'status':'PASS','source':'course_essay/Hangzhou_Passive_Cooling_Course_Essay.md','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'version':'Chinese reading version of English course essay','new_model_runs':0,'table_rows_identical':True,'references_unchanged':True}
(OUT/'TRANSLATION_CHECKS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
print('Chinese reading version saved:',OUT)
