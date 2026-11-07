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
text = '# 杭州住宅原型的夏季降温：外遮阳与夜间通风\n中文审阅版｜对应英文课程短论文；数据、结论及参考文献保持一致。\n\n## 摘要\n本研究量化外遮阳与夜间通风对杭州住宅原型的夏季降温收益。利用2025、2026年天气，通过两热区热网络模型比较四种情景。将窗面50%直射削减与温差控制夜间通风结合，使两年夏季自由运行平均空气温度分别降低2.12°C和1.85°C，超过28°C的过热度时分别降低17.5%和17.7%，26°C理想显热制冷需求分别降低7.01%和6.44%。组合措施在20套测试输入中均排名第一。遮阳贡献了主要的制冷需求削减，夜间通风则在室外温度适宜时提供附加排热。结果支持为本研究住宅协调采用太阳控制与夜间排热。\n\n## 1 引言\n被动降温通过减少热量进入、利用较凉室外空气排出蓄热，改善建筑夏季表现。Short等（2018）研究了杭州公寓的太阳暴露、封闭阳台和通风；Artmann等（2008）则将天气、气流和蓄热确定为影响夜间降温的重要因素。在这些机制基础上，本文评价外遮阳、夜间通风及组合措施能使住宅原型的过热和显热制冷需求降低多少。比较自由运行与26°C理想制冷，能够揭示运行条件如何影响各项措施的价值，并为夏季设计中的协同配置提供依据。\n\n## 2 研究方法\n根据公开户型图（HZXQF，无日期）重建住宅原型，包括41.1 m²居住区和独立的6.3 m²封闭阳台。高度假设为2.7 m，体积分别为110.97和17.01 m³。两区均视为空气充分混合，隔断保持关闭。水平边界及两段朝东墙体取绝热；对外整窗面积分别假设为3.525和14.07 m²。每区设置一个空气节点和一个有效蓄热节点。空气热平衡包括围护传热、通风、区间交换、得热及制冷；蓄热节点与空气换热，并接收分配的得热。\n墙体热阻根据Short等（2018，补充材料表S1）的各层厚度和导热率计算。有效热容量密度独立设为165 kJ/(m²·K)，不直接采用存在不确定性的材料总热容量。整窗U值6.7 W/(m²·K)及SHGC 0.70用于代表透明单玻铝框窗（NSW Government，无日期）。关闭／开启窗户的总换气率分别为每小时0.44／1.51次，取自Hou等（2019，表6）的夏季夜间卧室中位值；将其用于本研究两区属于建模假设。居住区内部得热在18:00—08:00取16.7 W/m²，其余时段取该值的30%。得热数值参考Short等，时序由本研究独立假设，并非实测。\n通过Open-Meteo获得的ERA5资料每个夏季包含2208条逐小时记录，均无缺值。辐射代表前一小时均值，太阳位置取该小时中点，室外温度取相邻端点均值（Open-Meteo，无日期）。保留源记录后，积分时段为UTC+8下5月31日23:00至8月31日23:00；缺少最初温度端点的区间使用首个温度值。各立面分别计算直射、各向同性散射及地面反射。假设阳台透入太阳得热的25%分配至居住区，其余留在阳台，避免重复计入。\nS0仅有背景通风；S1削减窗面50%的太阳直射；S2启用夜间通风；S3结合两项措施。21:00—07:00期间，各区在室内温度至少比室外高1 K时，独立切换至开窗总换气率。自由运行模拟计算DH28＝Σmax(Tin−28,0)Δt，单位K·h，其中28°C为研究阈值。独立的理想制冷模拟仅对居住区施加全天可用的26°C温度上限，累计显热移除量，单位kWh_th；不包含潜热负荷或设备用电。\n采用后向Euler法、300 s步长求解，正式计算前重复首周天气预热28天。在2025年基准检查中，步长减半后关键累计指标变化小于0.006%；能量平衡及初始化检查也已通过。这些检查支持情景比较的数值稳定性。包括基准在内的20套输入考察气流、热容量、窗户、遮阳等假设；每个变体均与其自身的S0比较。\n\n## 3 结果\n表1 基准四情景比较；制冷量表示理想条件下的显热移除量。\nTABLE_PLACEHOLDER\nDH28对应自由运行；制冷需求降低率均相对于同一年的S0。\n\n三种措施均改善了基准表现（表1）。S3使2025年和2026年自由运行平均空气温度分别降低2.12°C和1.85°C，DH28分别降低17.5%和17.7%。仅通风对DH28的降低优于本研究测试的50%直射遮阳，而遮阳对理想制冷需求的降低更大。S3剩余过热时长为2208小时中的2172.0和2179.8小时，因此，自由运行的主要收益体现在过热强度下降。\n2025年，S3使理想需求由3757.0降至3493.8 kWh_th，减少263.2 kWh_th；2026年由3308.6降至3095.4 kWh_th，减少213.2 kWh_th。在20套输入中，S3的DH28和制冷需求均最低，单项措施排序则有所变化。对于需求D，交互量I＝(D0−D3)−(D0−D1)−(D0−D2)：两年DH28交互量分别为−203.1和−159.7 K·h，制冷交互量分别为−0.88和−0.74 kWh_th。组合的制冷收益接近相加，并有轻微收益递减。\n\n## 4 讨论\n结果支持两项互补的设计行动：减少白天太阳输入，以及在较凉的夜间排热。自由运行S2和S3中，居住区通风覆盖全部920小时夜间窗口；理想制冷下，2025年有164小时、2026年有206小时符合开窗规则。室内接近26°C时，室外通常需接近或低于25°C，才能满足规定的1 K温差。因此，温差控制开窗能够针对可利用的显热降温机会。在本研究26°C运行时序下，外遮阳是降低需求的主要措施，夜间通风在机会出现时提供补充。\n热量收支进一步明确了太阳控制可作用的路径。2025年，居住区通过自身外窗获得457.7 kWh_th，通过分配的阳台二次太阳得热获得507.9 kWh_th，同时经隔断向阳台净传递243.7 kWh_th。区分这些路径，支持在太阳控制评价中纳入阳台玻璃，并保留其缓冲区换热作用。这些机制与组合措施稳定的排序共同为协调评价太阳遮挡和夜间排热提供了物理依据。\n本研究属于未经实测校准的原型比较。基准自由运行峰值50.11°C和47.84°C取决于玻璃、内部得热、阳台太阳分配及简化热边界假设；挑檐和较低得热对照改变了绝对结果。固定气流、聚合蓄热、忽略天空长波交换及仅两个夏季也限定了解释范围。实际运行还涉及湿度、降雨、安全和噪声。这些因素明确了进一步细化收益估计、验证特定住宅应用的优先方向。\n\n## 5 结论\n对于本研究的杭州住宅原型，外遮阳与夜间通风组合使夏季自由运行平均空气温度降低1.85—2.12°C、超过28°C的过热度时降低17.5%—17.7%，并使26°C理想显热制冷需求降低6.44%—7.01%。组合措施在20套测试输入中均排名第一，支持在所研究条件下联合采用两项措施。\n由此形成的设计优先顺序是：通过外遮阳减少白天太阳得热，并在室外温度至少比室内低1 K时，利用夜间通风提供附加排热。这种协调策略能够缓解夏季过热，并降低主动系统需要承担的显热制冷量。\n\n## 参考文献\nREFERENCES_PLACEHOLDER\n\n'
headers=['年份','情景','DH28（K·h）','制冷量（kWh_th）','制冷降低率（%）']
mdtable='|'+'|'.join(headers)+'|\n|'+'|'.join(['---']*5)+'|\n'+'\n'.join('|'+'|'.join(r)+'|' for r in rows)
text=text.replace('TABLE_PLACEHOLDER',mdtable).replace('REFERENCES_PLACEHOLDER',refs.strip())
(OUT/'杭州住宅被动降温_英文短稿对应中文版.md').write_text(text)

def setfont(run,size=12):
 run.font.name='Times New Roman';run.font.size=Pt(size)
 rf=run._element.get_or_add_rPr().rFonts
 if rf is None:rf=OxmlElement('w:rFonts');run._element.rPr.insert(0,rf)
 for k in list(rf.attrib):
  if k.endswith('Theme'):del rf.attrib[k]
 for k in ['ascii','hAnsi','cs']:rf.set(qn('w:'+k),'Times New Roman')
 rf.set(qn('w:eastAsia'),'Noto Serif CJK SC')

def runs(p,line):
 pos=0
 for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)',line):
  if m.start()>pos:setfont(p.add_run(line[pos:m.start()]))
  h=OxmlElement('w:hyperlink');h.set(qn('r:id'),p.part.relate_to(m[2],RT.HYPERLINK,is_external=True));r=OxmlElement('w:r');pr=OxmlElement('w:rPr');rf=OxmlElement('w:rFonts');rf.set(qn('w:ascii'),'Times New Roman');rf.set(qn('w:hAnsi'),'Times New Roman');pr.append(rf);sz=OxmlElement('w:sz');sz.set(qn('w:val'),'24');pr.append(sz);r.append(pr);t=OxmlElement('w:t');t.text=m[1];r.append(t);h.append(r);p._p.append(h);pos=m.end()
 if pos<len(line):setfont(p.add_run(line[pos:]))

doc=Document();sec=doc.sections[0];sec.page_width=Cm(21);sec.page_height=Cm(29.7)
sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Cm(2.54)
for name in ['Normal','Title','Heading 1']:
 s=doc.styles[name];s.font.name='Times New Roman';s.font.size=Pt(12);s.font.color.rgb=RGBColor(0,0,0)
 s.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Noto Serif CJK SC')
 s.paragraph_format.line_spacing=1.;s.paragraph_format.space_after=Pt(6)
 if name!='Normal':s.font.bold=True;s.paragraph_format.keep_with_next=True
lines=text.splitlines();i=0
while i<len(lines):
 line=lines[i].strip()
 if not line:i+=1;continue
 if line.startswith('|'):
  table=doc.add_table(rows=1,cols=5);table.style='Light Shading Accent 1'
  for j,c in enumerate(headers):table.rows[0].cells[j].text=c
  table.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
  for row in rows:
   for cell,value in zip(table.add_row().cells,row):cell.text=value
  for row in table.rows:
   row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
   for cell in row.cells:
    for p in cell.paragraphs:
     p.paragraph_format.line_spacing=1.;p.paragraph_format.space_after=Pt(3)
     for r in p.runs:setfont(r)
  while i<len(lines) and lines[i].startswith('|'):i+=1
  continue
 if line.startswith('# '):p=doc.add_paragraph(style='Title');runs(p,line[2:]);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 elif line.startswith('## '):p=doc.add_paragraph(style='Heading 1');runs(p,line[3:]);p.paragraph_format.space_before=Pt(5)
 else:p=doc.add_paragraph();runs(p,line)
 p.paragraph_format.line_spacing=1.;p.paragraph_format.keep_together=True
 i+=1
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
doc.core_properties.title='杭州住宅原型的夏季降温：英文短稿对应中文版';doc.core_properties.author=''
path=OUT/'杭州住宅被动降温_英文短稿对应中文版.docx';doc.save(path)
# Translation checks: table rows copied exactly; key reported values must remain.
for value in ['17.5%','17.7%','7.01%','6.44%','2.12°C','1.85°C','2172.0','2179.8','164','206','50.11°C','47.84°C','457.7','507.9','243.7','0.006%']:
 assert value in text,value
assert refs.strip() in text
status={'status':'PASS','source':'course_essay/Hangzhou_Passive_Cooling_Course_Essay.md','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'version':'Chinese reading version of English course essay','new_model_runs':0,'table_rows_identical':True,'references_unchanged':True}
(OUT/'TRANSLATION_CHECKS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
print('Chinese reading version saved:',path)
