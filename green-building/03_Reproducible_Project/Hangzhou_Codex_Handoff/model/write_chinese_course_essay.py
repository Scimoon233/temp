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
text='''# 杭州住宅原型中的遮阳与夜间通风：过热及显热制冷需求
中文审阅版｜对应英文课程短论文；数据、结论及参考文献保持一致。

## 摘要
外遮阳和夜间通风能够改善夏季室内环境，但其收益取决于住宅的运行方式。本研究使用杭州两个夏季的天气资料，通过两热区热网络模型比较四种情景。组合措施使2025年和2026年自由运行状态下超过28°C的过热度时分别降低17.5%和17.7%。在26°C理想制冷条件下，显热制冷需求分别降低7.0%和6.4%，而仅采用通风时分别仅降低0.6%和0.8%。满足开窗条件的时数减少，可以解释两种工况下效果差异的主要部分。这些结果来自未经实测校准的住宅原型：组合措施后仍存在大量过热，阳台及使用假设的不确定性也限制了结果对实际住宅的适用性。

## 1 引言
被动降温通过限制热量进入、利用有利室外条件，为绿色建筑设计提供支持。Short等（2018）针对杭州公寓研究了太阳暴露、封闭阳台和通风等气候适应问题。其研究为本地分析提供依据，但不能据此确定另一套住宅的性能。夜间通风还受到天气、气流和蓄热的影响（Artmann等，2008）。本文考察：遮阳和通风在自由运行与26°C制冷住宅中能否带来相近收益，以及组合收益是否超过单项收益之和。本文的贡献是利用两个历史夏季开展透明的原型比较，并非提出新的被动降温方法，也不将其视为杭州住宅的代表性评估。

## 2 研究方法
根据公开户型图（HZXQF，无日期）重建住宅原型，包括41.1 m²居住区和独立的6.3 m²封闭阳台。高度假设为2.7 m，体积分别为110.97和17.01 m³。两区均视为空气充分混合，隔断保持关闭。水平边界及两段朝东墙体取绝热；对外整窗面积分别假设为3.525和14.07 m²。每区设置一个空气节点和一个有效蓄热节点。空气热平衡包括围护传热、通风、区间交换、得热及制冷；蓄热节点与空气换热，并接收分配的得热。
墙体热阻根据Short等（2018，补充材料表S1）的各层厚度和导热率计算。有效热容量密度独立设为165 kJ/(m²·K)，不直接采用存在不确定性的材料总热容量。整窗U值6.7 W/(m²·K)及SHGC 0.70用于代表透明单玻铝框窗（NSW Government，无日期）。关闭／开启窗户的总换气率分别为每小时0.44／1.51次，取自Hou等（2019，表6）的夏季夜间卧室中位值；将其用于本研究两区属于建模假设。居住区内部得热在18:00—08:00取16.7 W/m²，其余时段取该值的30%。得热数值参考Short等，时序由本研究独立假设，并非实测。
通过Open-Meteo获得的ERA5资料每个夏季包含2208条逐小时记录，均无缺值。辐射代表前一小时均值，太阳位置取该小时中点，室外温度取相邻端点均值（Open-Meteo，无日期）。保留源记录后，积分时段为UTC+8下5月31日23:00至8月31日23:00；缺少最初温度端点的区间使用首个温度值。各立面分别计算直射、各向同性散射及地面反射。假设阳台透入太阳得热的25%分配至居住区，其余留在阳台，避免重复计入。
S0仅有背景通风；S1削减窗面50%的太阳直射；S2启用夜间通风；S3结合两项措施。21:00—07:00期间，各区在室内温度至少比室外高1 K时，独立切换至开窗总换气率。自由运行模拟计算DH28＝Σmax(Tin−28,0)Δt，单位K·h，其中28°C为研究阈值，并非热舒适合规限值。独立的理想制冷模拟仅对居住区施加全天可用的26°C温度上限，累计显热移除量，单位kWh_th；不包含潜热负荷或设备用电。
采用后向Euler法、300 s步长求解，正式计算前重复首周天气预热28天。在2025年基准检查中，步长减半后关键累计指标变化小于0.006%；能量平衡及初始化检查也已通过。这些检查说明数值计算一致，不代表已验证实际预测精度。包括基准在内的20套输入考察气流、热容量、窗户、遮阳等假设；每个变体均与其自身的S0比较。

## 3 结果
表1 基准四情景比较；制冷量表示理想条件下的显热移除量。
TABLE_PLACEHOLDER
DH28对应自由运行；制冷需求降低率均相对于同一年的S0。

表1显示两种工况下的单项措施排序不同：自由运行DH28方面，通风优于削减50%直射的遮阳；理想制冷需求方面，遮阳降低量更大。S3使两年平均空气温度分别降低2.12°C和1.85°C，DH28分别降低17.5%和17.7%。但在2208小时中，S3仍分别有2172.0和2179.8小时超过28°C。因此，措施降低了过热强度，却未消除过热状态。
2025年S3使理想需求由3757.0降至3493.8 kWh_th，2026年由3308.6降至3095.4 kWh_th。对于需求指标D，交互量定义为I＝(D0−D3)−(D0−D1)−(D0−D2)。两年DH28交互量分别为−203.1和−159.7 K·h，制冷交互量分别为−0.88和−0.74 kWh_th。组合措施效果最好，但没有超过单项收益之和；制冷收益接近相加，并有轻微收益递减。

## 4 讨论
运行工况之间的差异直接来自基于温差的控制。自由运行的S2和S3中，居住区在两年均覆盖全部920小时夜间窗口；理想制冷下，2025年仅164小时、2026年仅206小时满足开启条件，因为当室内接近26°C时，室外通常须接近或低于25°C，才能满足1 K门槛。因此，自由运行温度改善不能证明制冷需求会获得同等比例的降低。湿度、降雨、安全和噪声可能进一步限制实际开窗，这些影响未纳入模拟。
绝对温度需要谨慎解释。基准自由运行峰值达到50.11°C和47.84°C。热量账目显示太阳和内部得热是重要输入，但方程守恒不能证明假设的玻璃、使用情况或暴露条件与真实住宅一致。2025年，居住区通过自身外窗获得457.7 kWh_th太阳得热，从阳台分配获得507.9 kWh_th二次太阳得热，同时通过隔断向阳台净传递243.7 kWh_th。因此，阳台太阳输入和温差驱动交换具有不同作用。示意挑檐、隔断及较低得热对照改变了绝对结果，但均不构成实测校准。
在全部20套主要输入中，S3的DH28和制冷需求均最低，但单项措施排序发生变化。这支持在测试范围内有条件地优先考虑组合措施，不能据此给出普遍适用的降低比例。单一重建住宅、固定气流、聚合蓄热、简化太阳分配、忽略天空长波交换及仅两个夏季，均限制结果推广。对实际设计的启示是：应将太阳控制与夜间可利用温差、预定制冷设定温度共同评价。

## 5 结论
对本研究原型，遮阳与夜间通风的组合降低了过热强度和理想显热制冷需求，但自由运行中仍存在广泛过热。仅通风的制冷需求降低幅度明显小于其自由运行改善，因为26°C运行状态限制了符合条件的开窗时数。组合收益略低于单项相加收益。这些发现支持在明确的运行条件下比较被动措施，不构成实际节电证明，也不能预测杭州某一具体住宅的室温。

## 参考文献
REFERENCES_PLACEHOLDER
'''
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
doc.core_properties.title='杭州住宅被动降温：英文短稿对应中文版';doc.core_properties.author=''
path=OUT/'杭州住宅被动降温_英文短稿对应中文版.docx';doc.save(path)
# Translation checks: table rows copied exactly; key reported values must remain.
for value in ['17.5%','17.7%','7.0%','6.4%','2.12°C','1.85°C','2172.0','2179.8','164','206','50.11°C','47.84°C','457.7','507.9','243.7','0.006%']:
 assert value in text,value
assert refs.strip() in text
status={'status':'PASS','source':'course_essay/Hangzhou_Passive_Cooling_Course_Essay.md','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'version':'Chinese reading version of English course essay','new_model_runs':0,'table_rows_identical':True,'references_unchanged':True}
(OUT/'TRANSLATION_CHECKS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
print('Chinese reading version saved:',path)
