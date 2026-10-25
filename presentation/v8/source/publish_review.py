from pathlib import Path
from pptx import Presentation
from docx import Document
from docx.shared import Pt
import re,json,zipfile
b=Path(__file__).resolve().parents[1];notes=json.loads((b/'speaker-notes.json').read_text());records=json.loads((b/'slide-records.json').read_text());basis=json.loads((b/'source/source-basis.json').read_text())
assert len(notes)==18
words=sum(len(re.findall(r"[\w’'-]+",n['script']+' '+n['transition'])) for n in notes[:-1])
intro=f'{words} spoken English words on slides 1–17. At 120–135 words/minute this is {words/135:.1f}–{words/120:.1f} minutes of continuous speech, before pauses and slide changes. Rehearse with figures and reserve Q&A within 10–12 minutes. Takeaways, Q&A and source-basis sections are not extra timed speech.'
D=Document();D.styles['Normal'].font.name='Noto Sans';D.styles['Normal'].font.size=Pt(11);D.add_heading('VineWeave Canopy — Presenter Guide V8',0);D.add_paragraph(intro);lines=['# Presenter Guide V8','',intro,'']
hints={4:'先讲材料分区与数量；这是材料方案，不是整体安全结论。',5:'表中单价是按相同全长比较材料输入，不是最终单元总价；材料常数仍为工作簿输入。',6:'按原工作簿解释钢支撑与竹冠面；别把竹材单项指标的优势说成整套造价更低。',7:'先指33.25mm目标，再看两种理想边界；原表明确要求节点详图与转动刚度验算。',11:'先分清两类指标，再读后面的百分比；不能混用、相加或换算摄氏度。',12:'正午98.7%不能代表整段使用时间；时段与座椅位置要一起考虑。',13:'只说原CSV给出的参数情景结果；同覆盖比例不等于相同种植面积和材料投入。',14:'80到95覆盖增加2.8个百分点是时段均值；相同50%分布比较是正午值，别混成同一组。'}
for n in notes:
 title=f"{n['slide']:02d} | {n['title']}";D.add_heading(title,1);lines+=['## '+title,'']
 if n['slide'] in hints:D.add_paragraph('中文提示：'+hints[n['slide']]);lines+=['中文提示：'+hints[n['slide']],'']
 for label,key in [('Takeaway','takeaway'),('Spoken script','script'),('Transition','transition'),('Q&A','qa')]:D.add_paragraph(label+': '+n[key]);lines+=[label+': '+n[key],'']
 D.add_heading('Source basis — not spoken',2);lines+=['Source basis — not spoken:','']
 for src in n['sourceBasis']['sources']:D.add_paragraph(src);lines+=[src,'']
 D.add_paragraph(n['sourceBasis']['basis']);lines+=[n['sourceBasis']['basis'],'']
D.save(b/'Presenter-Guide-v8.docx');(b/'Presenter-Guide-v8.md').write_text('\n'.join(lines))
preview=['# VineWeave Canopy — V8','','**18 slides including references.** [Editable PowerPoint](VineWeave-Canopy-v8.pptx) · [PDF](VineWeave-Canopy-v8.pdf) · [Presenter guide](Presenter-Guide-v8.md) · [Statement/source audit](Statement-Evidence.md)','','Material reasoning: pages 4–6. Node/deflection: page 7. Shade methods/results: pages 11–14. Page 12 now uses a 25-frame ideal-shadow GIF. No plant-growth timing or course-mapping page.','']
for r in records:
 preview += [f"## {r['number']:02d} — {r['title']}",'',f"![Slide {r['number']:02d}](slides/slide-{r['number']:02d}.png)",'']
 if r['number']==12:preview += ['Animated footprint: solar time 09:00–15:00; pale green = leaf-envelope shadow, dark green = target overlap. The moving dot runs from left (09:00) through centre (12:00) to right (15:00).','', '![Ideal shadow animation](assets/ideal-shadow-sequence.gif)','']
(b/'Preview.md').write_text('\n'.join(preview))
# Index every native text statement, table cell, chart entry and presenter sentence
# to the corresponding supplied-source section/cells. Evidence groups and limits
# remain explicit; this is traceability, not independent certification of inputs.
r=Presentation(b/'VineWeave-Canopy-v8.pptx');audit=['# V8逐项文字与依据对照','','范围：主页面原生文字、表格单元、图表数值及讲稿句子。每页先列明来自用户材料的出处与依据，再列该页表述；同页表述对应其下所列来源。问句、标题和过渡用于组织已列材料，不构成新增实验结果。','','“有材料出处”不等于材料中的假设已获验证。工程竹常数、湿植被荷载、透射率、报价和节点约束仍按输入/假设标注。原报告列出的外部文献并未冒充本轮已核验全文。','','修改依据：Cost-Analysis.xlsx、原分析报告、参数/覆盖补充报告与CSV；新增算术复核见[Claim-Checks.json](Claim-Checks.json)。没有新增生长速率、实测温降、风速或结构安全结论。',''];all_statements=[]
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
(b/'README.md').write_text("""# VineWeave Canopy — V8

**18 slides including references. Page 12 now uses an animated ideal-shadow footprint.**

- **[Preview all slides and the new GIF](Preview.md)**
- [Editable PowerPoint](VineWeave-Canopy-v8.pptx) · [Static PDF](VineWeave-Canopy-v8.pdf)
- [New GIF](assets/ideal-shadow-sequence.gif)
- [Presenter guide](Presenter-Guide-v8.md) · [Word](Presenter-Guide-v8.docx)
- [Bilingual script](Bilingual-Script-v8.md) · [Bilingual Word](Bilingual-Script-v8.docx)
- [Presentation bundle](Presentation-v8.zip)
- [Statement/source audit](Statement-Evidence.md) · [Animation check](Ideal-Animation-Check.json)

![Slide 12](slides/slide-12.png)

## Animation and evidence

The former three still images on page 12 are replaced with a 25-frame GIF using the same baseline continuous-leaf envelope, target and 09:00–15:00 solstice solar times at 15-minute intervals. Each frame's ideal overlap was checked against the existing curve; maximum absolute difference is below 1e-8 percentage points. This is a different metric from the fixed-50%-cover frame/leaf animation on page 15.

Pale green is the leaf-envelope shadow; dark green is the portion within the reference target. A moving dot indicates solar time. All time labels, legend, key values and the analytical chart remain native editable objects. The GIF itself is an image. Playback loops in the GIF encoding; actual PowerPoint playback still needs checking in the presentation software.

The page retains 09/12/15 values 47.2/98.7/47.2%, the solstice/equinox curves and their time means. PDF/gallery show a static noon keyframe; the GIF is also embedded separately in the GitHub preview. No new geometry, foliage, weather, growth or thermal result was introduced. Other slides are unchanged from V7 apart from version metadata; page count remains 18.

Three GIFs retain 25/5/25 frames on pages 12/14/15. Five native charts retain workbooks. Source references remain in notes and the statement audit. See [validation](Validation.md).
""")
(b/'Changes-and-Evidence.md').write_text("""# V8改动与依据

仅修改第12页呈现：三张静态阴影图替换为25帧GIF，右侧保留三个关键时刻数值，底部保留原时段曲线。英文与中英文讲稿同步更新该页说明。

动画使用原补充包中的太阳方向、连续叶面边界及投影函数，仍为30°N、夏至、同一目标区和09–15每15分钟采样。25帧重合率与既有夏至曲线逐项核对，误差小于1e-8个百分点，详见Ideal-Animation-Check.json。

浅绿为连续叶面阴影，深绿为其与参考目标区的重合。移动圆点只指示播放时刻；不是现场拍摄或新实验。时间文字、图例、关键数值和曲线仍可编辑。GIF内部不放文字。

没有改用第15页的50%叶簇覆盖动画，避免将等效直射遮挡与第12页理想重合率混用。PDF/缩略图为正午静态帧；GitHub预览同时提供真实GIF。

其他材料、节点与遮荫数据延续V7，并保留来源/假设说明。未恢复植物生长时间或课程映射页。
""")
(b/'Validation.md').write_text(f"""# V8 validation

- PPTX/PDF: 18 pages. Native text/table objects, notes, shape bounds and PDF text bounds checked.
- Page 12 links an embedded animated GIF. Three GIFs retain 25/5/25 frames; no text is baked into the new GIF.
- Five native charts and five embedded chart workbooks remain.
- All 25 new animation overlap values match the existing solstice curve within 1e-8 percentage points. Same supplied leaf-envelope geometry, target and solar function; no thermal/biological simulation.
- Static export uses noon frame; page 12 visually reviewed. Gallery includes the actual GIF separately.
- Source-basis references retained in 18 notes; statement index regenerated. Source input checks from V7 are carried forward unchanged.
- GIF playback in actual PowerPoint, fonts and presentation timing still require rehearsal.

{intro}
""")
with zipfile.ZipFile(b/'Presentation-v8.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in ['VineWeave-Canopy-v8.pptx','VineWeave-Canopy-v8.pdf','Presenter-Guide-v8.docx','Bilingual-Script-v8.docx','Bilingual-Script-v8.md','README.md','Statement-Evidence.md','Claim-Checks.json','Ideal-Animation-Check.json','Changes-and-Evidence.md','Validation.md']:z.write(b/name,name)
print('Published:',len(notes),'slides;',words,'spoken words;',len(all_statements),'indexed text/data items.')
