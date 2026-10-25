from pathlib import Path
from pptx import Presentation
from docx import Document
from docx.shared import Pt
import re,json,zipfile
b=Path(__file__).resolve().parents[1];notes=json.loads((b/'speaker-notes.json').read_text());records=json.loads((b/'slide-records.json').read_text());basis=json.loads((b/'source/source-basis.json').read_text())
assert len(notes)==18
words=sum(len(re.findall(r"[\w’'-]+",n['script']+' '+n['transition'])) for n in notes[:-1])
intro=f'{words} spoken English words on slides 1–17. At 120–135 words/minute this is {words/135:.1f}–{words/120:.1f} minutes of continuous speech, before pauses and slide changes. Rehearse with figures and reserve Q&A within 10–12 minutes. Takeaways, Q&A and source-basis sections are not extra timed speech.'
D=Document();D.styles['Normal'].font.name='Noto Sans';D.styles['Normal'].font.size=Pt(11);D.add_heading('VineWeave Canopy — Presenter Guide V9',0);D.add_paragraph(intro);lines=['# Presenter Guide V9','',intro,'']
hints={10:'18kg/m²取自爬山虎工作簿范围上限，仍是假设；凌霄上限25，替换需复核荷载。',4:'先讲材料分区与数量；这是材料方案，不是整体安全结论。',5:'表中单价是按相同全长比较材料输入，不是最终单元总价；材料常数仍为工作簿输入。',6:'按原工作簿解释钢支撑与竹冠面；别把竹材单项指标的优势说成整套造价更低。',7:'先指33.25mm目标，再看两种理想边界；原表明确要求节点详图与转动刚度验算。',11:'先分清两类指标，再读后面的百分比；不能混用、相加或换算摄氏度。',12:'正午98.7%不能代表整段使用时间；时段与座椅位置要一起考虑。',13:'只说原CSV给出的参数情景结果；同覆盖比例不等于相同种植面积和材料投入。',14:'80到95覆盖增加2.8个百分点是时段均值；相同50%分布比较是正午值，别混成同一组。'}
for n in notes:
 title=f"{n['slide']:02d} | {n['title']}";D.add_heading(title,1);lines+=['## '+title,'']
 if n['slide'] in hints:D.add_paragraph('中文提示：'+hints[n['slide']]);lines+=['中文提示：'+hints[n['slide']],'']
 for label,key in [('Takeaway','takeaway'),('Spoken script','script'),('Transition','transition'),('Q&A','qa')]:D.add_paragraph(label+': '+n[key]);lines+=[label+': '+n[key],'']
 D.add_heading('Source basis — not spoken',2);lines+=['Source basis — not spoken:','']
 for src in n['sourceBasis']['sources']:D.add_paragraph(src);lines+=[src,'']
 D.add_paragraph(n['sourceBasis']['basis']);lines+=[n['sourceBasis']['basis'],'']
D.save(b/'Presenter-Guide-v9.docx');(b/'Presenter-Guide-v9.md').write_text('\n'.join(lines))
preview=['# VineWeave Canopy — V9','','**18 slides including references.** [Editable PowerPoint](VineWeave-Canopy-v9.pptx) · [PDF](VineWeave-Canopy-v9.pdf) · [Presenter guide](Presenter-Guide-v9.md) · [Statement/source audit](Statement-Evidence.md)','','Material reasoning: pages 4–6. Node/deflection: page 7. Shade methods/results: pages 11–14. Page 10 now links plant-screen wet-mass ranges to the beam assumption; page 12 retains its ideal-shadow GIF. No plant-growth timing or course-mapping page.','']
for r in records:
 preview += [f"## {r['number']:02d} — {r['title']}",'',f"![Slide {r['number']:02d}](slides/slide-{r['number']:02d}.png)",'']
 if r['number']==12:preview += ['Animated footprint: solar time 09:00–15:00; pale green = leaf-envelope shadow, dark green = target overlap. The moving dot runs from left (09:00) through centre (12:00) to right (15:00).','', '![Ideal shadow animation](assets/ideal-shadow-sequence.gif)','']
(b/'Preview.md').write_text('\n'.join(preview))
# Index every native text statement, table cell, chart entry and presenter sentence
# to the corresponding supplied-source section/cells. Evidence groups and limits
# remain explicit; this is traceability, not independent certification of inputs.
r=Presentation(b/'VineWeave-Canopy-v9.pptx');audit=['# V9逐项文字与依据对照','','范围：主页面原生文字、表格单元、图表数值及讲稿句子。每页先列明来自用户材料的出处与依据，再列该页表述；同页表述对应其下所列来源。问句、标题和过渡用于组织已列材料，不构成新增实验结果。','','“有材料出处”不等于材料中的假设已获验证。工程竹常数、湿植被荷载、透射率、报价和节点约束仍按输入/假设标注。原报告列出的外部文献并未冒充本轮已核验全文。','','修改依据：Cost-Analysis.xlsx、原分析报告、参数/覆盖补充报告与CSV；新增算术复核见[Claim-Checks.json](Claim-Checks.json)。没有新增生长速率、实测温降、风速或结构安全结论。',''];all_statements=[]
for i,sl in enumerate(r.slides,1):
 ref=basis[str(i)];audit += [f"## {i:02d} — {records[i-1]['title']}",'','出处：','']+['- '+x for x in ref['sources']]+['','材料依据／限定：'+ref['basis'],'','### 页面表述','']
 statements=[]
 for sh in sl.shapes:
  if sh.has_text_frame:
   for para in sh.text_frame.paragraphs:
    if para.text.strip():statements.append(('页面文字',para.text))
  if sh.has_table:
   for row in sh.table.rows:
    for c in row.cells:
     if c.text.strip():statements.append(('表格',c.text))
  if sh.has_chart:
   for ser in sh.chart.series:
    statements += [('图表数据',f'{cat.label}: {val}') for cat,val in zip(sh.chart.plots[0].categories,ser.values)]
 for kind,text in statements:
  for sentence in re.split(r'(?<=[.!?])\s+(?=[A-Z])',text):
   audit += ['- '+kind+'：'+sentence.replace('\n',' / ')];all_statements.append({'slide':i,'location':kind,'statement':sentence,'basis':str(i)})
 audit += ['','### 讲稿及答辩表述','']
 n=notes[i-1]
 for field in ['takeaway','script','transition','qa']:
  for sentence in re.split(r'(?<=[.!?])\s+(?=[A-Z])',n[field]):audit+=['- '+field+'：'+sentence];all_statements.append({'slide':i,'location':field,'statement':sentence,'basis':str(i)})
 audit+=['']
(b/'Statement-Evidence.md').write_text('\n'.join(audit));(b/'Statement-Evidence.json').write_text(json.dumps({'basis':basis,'statements':all_statements},ensure_ascii=False,indent=2))
(b/'README.md').write_text("""# VineWeave Canopy — V9

**18 slides including references. Plant page updated using the agreed minimal A revision.**

- **[Preview every slide](Preview.md)**
- [Editable PowerPoint](VineWeave-Canopy-v9.pptx) · [Static PDF](VineWeave-Canopy-v9.pdf)
- [Bilingual script](Bilingual-Script-v9.md) · [Bilingual Word](Bilingual-Script-v9.docx)
- [Presenter guide and sources](Presenter-Guide-v9.md) · [Word](Presenter-Guide-v9.docx)
- [Presentation bundle](Presentation-v9.zip)
- [Changes and evidence](Changes-and-Evidence.md) · [Statement audit](Statement-Evidence.md)

![Plant screen](slides/slide-10.png)

## Plant input linkage

The three-card layout remains. Cards now show adhesive tendrils / twining / aerial roots and the workbook wet-mass ranges 10–18 / 10–18 / 15–25 kg/m². The adopted 18 kg/m² beam input is explicitly linked to the upper end of the Boston ivy workbook range. Both the range and load remain assumptions: the original publication and area basis are unverified; no measured canopy load is claimed.

The alternative carries a load-review reminder. Seasonal leaf loss is presented as the workbook’s screening intent. Local climate and attachment remain checks. The unsupported star after the Latin name is removed, with a defined star now attached to the provisional wet-mass inputs. Roots/care quantities are retained.

No species was replaced. No growth-time estimate, LAI/leaf-thickness mass derivation, cold-tolerance threshold or Shanghai-specific winter-protection prescription was added. No original workbook was modified. Page 7 only gains a source cross-reference to page 10. Cost/carbon figures and design decisions are unchanged.

The three GIFs and five analytical charts are retained, including the page-12 ideal-shadow GIF. Text, plant ranges, footnotes and diagrams remain editable; rendered geometry/GIFs are images. Actual PowerPoint playback and timing still require rehearsal. [Validation](Validation.md).
""")
(b/'Changes-and-Evidence.md').write_text("""# V9精简A方案落实情况

| 修改 | 原材料依据 |
| --- | --- |
| 保留2株爬山虎＋1株使君子，凌霄备选 | Cost-Analysis.xlsx 爬藤植物选择A14:B14 |
| 三卡片补攀附方式：吸盘卷须、缠绕、气生根 | 爬藤植物选择C5:C7 |
| 三卡片补参考湿重10–18、10–18、15–25kg/m² | 爬藤植物选择F5:F7；第2行注明量级需核实 |
| 18kg/m²明确来自爬山虎范围上限 | 挠度校核B6/D6，明确指向爬山虎10–18取上限 |
| 备选凌霄提醒替换时重核荷载 | 其参考上限25高于当前18，未将其作为已采用荷载 |
| 季节性落叶＋攀附匹配写成筛选意图 | 植物表第2行；不冒充已验证的当地物候 |
| 删除Campsis后的悬空星号 | 星号改用于参考湿重，页脚给出含义与来源状态 |
| 保留1.2m³基质、滴灌、牵引与修剪 | 植物表第15行及原报告植物接口 |

第7页仅增加指向第10页的荷载来源标注。英文/中英讲稿、备注和文字依据清单同步更新；不增加页面。

没有加入LAI到主页面，没有声称用LAI和叶厚计算湿重，没有补未经核实的耐寒阈值，没有替换植物或恢复植物生长时间。没有修改原工作簿。预算、碳排、全钢/廊道等评价建议不属于此次选定的植物A方案，未额外改动。
""")
(b/'Validation.md').write_text(f"""# V9 validation

- 18-slide PPTX/PDF retained; native editable text, notes, shape bounds and PDF text bounds checked.
- Plant-page values traced to workbook 爬藤植物选择 F5:F7; load18 traced to 挠度校核 B6/D6. Source/area-basis uncertainty explicitly visible.
- Plant page and page-7 source footer visually reviewed. No dangling star after Campsis grandiflora.
- Five native charts/workbooks and three GIFs retained (25/5/25 frames). No optical, beam, cost or carbon numeric result changed.
- Page12 animation check and V7 original-input arithmetic checks carried forward unchanged.
- Statement/source index and English/bilingual notes regenerated. Actual PowerPoint playback and timing remain untested.

{intro}
""")
with zipfile.ZipFile(b/'Presentation-v9.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in ['VineWeave-Canopy-v9.pptx','VineWeave-Canopy-v9.pdf','Presenter-Guide-v9.docx','Bilingual-Script-v9.docx','Bilingual-Script-v9.md','README.md','Statement-Evidence.md','Claim-Checks.json','Ideal-Animation-Check.json','Plant-Input-Check.json','Changes-and-Evidence.md','Validation.md']:z.write(b/name,name)
print('Published:',len(notes),'slides;',words,'spoken words;',len(all_statements),'indexed text/data items.')
