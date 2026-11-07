from pathlib import Path
import json,re,html
import pandas as pd
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'course_essay'
OUT.mkdir(exist_ok=True)
r=pd.read_csv(ROOT/'results/base_metrics.csv')
title='Shading and Night Ventilation in a Hangzhou Residential Prototype: Overheating and Sensible Cooling Demand'
sections=[
('Abstract',[
'External shading and night ventilation can improve summer conditions, but their benefits depend on how a dwelling operates. A two-zone thermal-network model compared four scenarios using two summers of Hangzhou weather. Combined measures reduced free-running overheating degree-hours above 28°C by 17.5% in 2025 and 17.7% in 2026. Under ideal cooling at 26°C, sensible cooling demand fell by 7.0% and 6.4%, whereas ventilation alone reduced demand by only 0.6% and 0.8%. Fewer eligible opening hours explain much of this difference. These are uncalibrated prototype results: substantial residual overheating and uncertain balcony and occupancy assumptions limit their application to actual dwellings.'
]),
('1. Introduction',[
'Passive cooling contributes to green building design by limiting heat entry and exploiting favourable outdoor conditions. In Hangzhou apartments, Short et al. (2018) examined solar exposure, enclosed balconies and ventilation as adaptation issues. Their results motivate local investigation without establishing performance for a different dwelling. Night ventilation also depends on weather, airflow and thermal storage (Artmann et al., 2008). This essay asks whether shading and ventilation give comparable benefits in a free-running dwelling and one cooled to 26°C, and whether their combination provides more than additive benefits. Its contribution is a transparent prototype comparison under two historical summers, rather than a new passive-cooling method or a representative assessment of Hangzhou housing.'
]),
('2. Methods',[
'A public floor plan (HZXQF, n.d.) informed a reconstructed prototype comprising a 41.1 m² living zone and a separate 6.3 m² enclosed balcony. An assumed 2.7 m height gives volumes of 110.97 and 17.01 m³. Both zones are well mixed; the partition remains closed. Horizontal boundaries and two east-facing wall segments are adiabatic. Assumed external whole-window areas are 3.525 and 14.07 m². Each zone contains an air node and an effective thermal-mass node. Air balances include envelope conduction, ventilation, interzone exchange, gains and cooling; mass nodes exchange heat with the air and receive allocated gains.',
'Wall resistance uses layer thicknesses and conductivities from Short et al. (2018, supplementary Table S1). Effective heat capacity, assumed independently of uncertain material heat capacities, is 165 kJ/(m² K). Whole-window U = 6.7 W/(m² K) and SHGC = 0.70 represent clear single-glazed aluminium windows (NSW Government, n.d.). Closed/open total air-change rates of 0.44/1.51 per hour use summer-night bedroom medians from Hou et al. (2019, Table 6); transferring them to these zones is a modelling assumption. Living-zone gains are 16.7 W/m² from 18:00–08:00 and 30% otherwise. The magnitude draws on Short et al.; this schedule is independently assumed, not measured.',
'ERA5 data obtained through Open-Meteo provide 2,208 hourly records per summer, with no missing values. Radiation represents the preceding hour; solar position uses its midpoint and outdoor temperature uses adjacent endpoint means (Open-Meteo, n.d.). Preserving the source records yields intervals from 31 May 23:00 to 31 August 23:00, UTC+8; the first temperature is held constant for the missing initial endpoint. Direct, isotropic diffuse and ground-reflected radiation are calculated for each facade. An assumed 25% of admitted balcony solar gain is allocated to the living zone, with the remainder retained in the balcony, avoiding double counting.',
'S0 has background ventilation only; S1 removes 50% of window direct radiation; S2 enables night ventilation; S3 combines both. Each zone independently switches to the open-window total rate during 21:00–07:00 when indoor air is at least 1 K warmer than outdoors. Free-running simulations evaluate DH28 = Σmax(Tin − 28, 0)Δt, in K h, using a research threshold rather than a comfort-compliance limit. Separate ideal-cooling simulations impose a continuously available 26°C upper limit in the living zone only and sum sensible heat removal in kWh_th. They include neither latent loads nor equipment electricity.',
'Backward Euler integration uses 300 s steps after 28 days of repeated-first-week warm-up. In the 2025 baseline checks, halving the step changed key cumulative metrics by less than 0.006%; energy-balance and initialization checks also passed. These checks establish numerical consistency, not measured accuracy. Twenty input sets, including the baseline, test airflow, thermal mass, windows, shading and other assumptions; each variant is compared with its own S0.'
]),
('3. Results',[]),
('4. Discussion',[
'The operating-state difference follows directly from the temperature-based controller. In free-running S2 and S3, living-zone ventilation operated throughout the 920-hour night window in both years. With ideal cooling, only 164 hours in 2025 and 206 hours in 2026 qualified, because indoor air near 26°C generally requires outdoor air near or below 25°C to satisfy the 1 K rule. Thus, free-running temperature improvement is insufficient evidence for an equivalent reduction in cooling demand. Humidity, rain, security and noise could further restrict practical opening; their effects were not simulated.',
'Absolute temperatures require particular caution. Baseline free-running peaks reached 50.11°C and 47.84°C. Energy ledgers identify solar and internal gains as important inputs, but balanced equations cannot establish whether assumed glazing, occupancy or exposure match a real dwelling. In 2025, the living zone received 457.7 kWh_th through its external windows and 507.9 kWh_th as allocated secondary balcony solar gain, while transferring a net 243.7 kWh_th to the balcony through the partition. Balcony solar input and temperature-driven exchange therefore have distinct roles. Illustrative overhang, partition and reduced-gain comparisons changed absolute outcomes; none constitutes calibration.',
'S3 had the lowest DH28 and cooling demand in all twenty main input sets, although the ranking of individual measures changed. This supports a conditional preference for combined measures within the tested range, not a universal savings percentage. A single reconstructed dwelling, fixed airflow, lumped storage, simplified solar allocation, omitted sky longwave exchange and only two summers limit generalisation. The practical design lesson is to assess solar control together with the night-time temperature opportunity and intended cooling setpoint.'
]),
('5. Conclusion',[
'For this prototype, shading and night ventilation together reduced overheating intensity and ideal sensible cooling demand, but left extensive free-running overheating. Ventilation alone produced much smaller cooling-demand reductions than free-running improvements because the 26°C operating state restricted eligible opening hours. Combined benefits were slightly sub-additive. These findings support comparing passive measures under explicitly defined operating conditions; they do not establish actual electricity savings or predict indoor temperatures for a specific Hangzhou home.'
])]
results=[
'Table 1 shows distinct rankings: ventilation outperformed 50% direct shading for free-running DH28, while shading reduced ideal cooling demand more. S3 lowered mean air temperature by 2.12°C and 1.85°C and DH28 by 17.5% and 17.7%. However, S3 still exceeded 28°C for 2,172.0 and 2,179.8 of 2,208 hours. It reduced overheating intensity without resolving the overheating condition.',
'S3 reduced ideal demand from 3,757.0 to 3,493.8 kWh_th in 2025 and from 3,308.6 to 3,095.4 kWh_th in 2026. For a demand indicator D, interaction is I = (D0 − D3) − (D0 − D1) − (D0 − D2). DH28 interactions were −203.1 and −159.7 K h; cooling interactions were −0.88 and −0.74 kWh_th. The combination performed best but did not exceed additive benefits; cooling benefits were approximately additive, with slight diminishing returns.'
]
refs=[
('Artmann, N., Manz, H., Heiselberg, P., 2008. Parameter study on performance of building cooling by night-time ventilation. Renewable Energy 33, 2589–2598. ', '10.1016/j.renene.2008.02.025','https://doi.org/10.1016/j.renene.2008.02.025'),
('Hou, J., Sun, Y., Chen, Q., et al., 2019. Air change rates in urban Chinese bedrooms. Indoor Air 29, 828–839. ','10.1111/ina.12582','https://doi.org/10.1111/ina.12582'),
('HZXQF, n.d. Public listing and floor plan, 71.05 m² apartment. ','Source page','https://www.hzxqf.com/house/120716888258.html'),
('NSW Government, n.d. Default Window Data, item 5. ','Planning Portal','https://www.planningportal.nsw.gov.au/basix-thermal-comfort/diy-method/windows/frame-glass-types/default-window-data'),
('Open-Meteo, n.d. Historical Weather API: ERA5 and hourly variable definitions. ','Documentation','https://open-meteo.com/en/docs/historical-weather-api'),
('Short, C.A., Song, J., Mottet, L., Chen, S., Wu, J., Ge, J., 2018. Challenges in the low-carbon adaptation of China’s apartment towers. Building Research & Information 46, 899–930. ','10.1080/09613218.2018.1489465','https://doi.org/10.1080/09613218.2018.1489465')]

def hyperlink(p,label,url):
 h=OxmlElement('w:hyperlink');h.set(qn('r:id'),p.part.relate_to(url,RT.HYPERLINK,is_external=True));run=OxmlElement('w:r');prop=OxmlElement('w:rPr')
 fonts=OxmlElement('w:rFonts')
 for k in ['ascii','hAnsi','eastAsia','cs']:fonts.set(qn('w:'+k),'Times New Roman')
 prop.append(fonts);size=OxmlElement('w:sz');size.set(qn('w:val'),'24');prop.append(size);color=OxmlElement('w:color');color.set(qn('w:val'),'000000');prop.append(color)
 run.append(prop);t=OxmlElement('w:t');t.text=label;run.append(t);h.append(run);p._p.append(h)

def textp(doc,text,style=None):
 p=doc.add_paragraph(text,style);p.paragraph_format.space_after=Pt(5);p.paragraph_format.line_spacing=1.;p.paragraph_format.keep_together=True
 for run in p.runs:
  run.font.name='Times New Roman';run.font.size=Pt(12)
  rf=run._element.get_or_add_rPr().rFonts
  for k in list(rf.attrib):
   if k.endswith('Theme'):del rf.attrib[k]
  for k in ['ascii','hAnsi','eastAsia','cs']:rf.set(qn('w:'+k),'Times New Roman')
 return p

doc=Document();sec=doc.sections[0]
sec.page_width=Cm(21);sec.page_height=Cm(29.7)
sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Cm(2.54)
sec.header_distance=sec.footer_distance=Cm(1.27)
for st in doc.styles:
 if st.type==1 or st.type==2:
  st.font.name='Times New Roman';st.font.size=Pt(12)
  if st.element.rPr is not None and st.element.rPr.rFonts is not None:
   for k in list(st.element.rPr.rFonts.attrib):
    if k.endswith('Theme'):del st.element.rPr.rFonts.attrib[k]
   for k in ['ascii','hAnsi','eastAsia','cs']:st.element.rPr.rFonts.set(qn('w:'+k),'Times New Roman')
  if st.type==1:
   st.paragraph_format.line_spacing=1.;st.paragraph_format.space_before=Pt(0);st.paragraph_format.space_after=Pt(5)
for name in ['Heading 1','Heading 2','Title']:
 doc.styles[name].font.bold=True;doc.styles[name].font.color.rgb=RGBColor(0,0,0);doc.styles[name].paragraph_format.keep_with_next=True
p=textp(doc,title,'Title');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_after=Pt(8)
md=['# '+title,'']
for heading,paragraphs in sections:
 p=textp(doc,heading,'Heading 1');p.paragraph_format.space_before=Pt(5);md+=['## '+heading,'']
 if heading=='3. Results':
  cap='Table 1. Baseline scenario comparison; cooling is ideal sensible heat removal.'
  textp(doc,cap);md.append(cap)
  headers=['Year','Case','DH28\n(K h)','Cooling\n(kWh_th)','Cooling\ncut (%)']
  tb=doc.add_table(rows=1,cols=5);tb.autofit=False
  widths=[Cm(1.3),Cm(1.2),Cm(3.5),Cm(3.8),Cm(3.8)]
  for i,(c,w) in enumerate(zip(tb.rows[0].cells,widths)):c.text=headers[i];c.width=w
  tr=tb.rows[0]._tr.get_or_add_trPr();repeat=OxmlElement('w:tblHeader');tr.append(repeat)
  md+=['|Year|Case|DH28 (K h)|Cooling (kWh_th)|Cooling cut (%)|','|---|---|---|---|---|']
  for y in [2025,2026]:
   for s in ['S0','S1','S2','S3']:
    f=r[(r.year==y)&(r['mode']=='free')&(r.scenario==s)].iloc[0];a=r[(r.year==y)&(r['mode']=='ideal')&(r.scenario==s)].iloc[0]
    vals=[str(y),s,f'{f.DH28_Kh:,.1f}',f'{a.cool_kWh_th:,.1f}',f'{a.cool_kWh_th_reduction_pct:.2f}']
    row=tb.add_row()
    for i,c in enumerate(row.cells):c.text=vals[i];c.width=widths[i]
    md.append('|'+ '|'.join(vals)+'|')
  for ri,row in enumerate(tb.rows):
   trp=row._tr.get_or_add_trPr();cant=OxmlElement('w:cantSplit');trp.append(cant)
   for cell in row.cells:
    for p in cell.paragraphs:
     p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(2);p.paragraph_format.line_spacing=1.
     for run in p.runs:run.font.name='Times New Roman';run.font.size=Pt(12);run.bold=ri==0
  tblpr=tb._tbl.tblPr;border=OxmlElement('w:tblBorders')
  for side in ['top','bottom','insideH']:
   el=OxmlElement('w:'+side);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'888888');border.append(el)
  tblpr.append(border)
  note='DH28 refers to free running; cooling cuts are relative to the same year’s S0.'
  textp(doc,note);md+=['',note,'']
  for paragraph in results:textp(doc,paragraph);md += [paragraph,'']
 for paragraph in paragraphs:textp(doc,paragraph);md += [paragraph,'']
p=textp(doc,'References','Heading 1');md+=['## References','']
for prefix,label,url in refs:
 p=textp(doc,prefix);hyperlink(p,label,url);p.add_run(' (accessed 7 November 2026).' if 'n.d.' in prefix else '.')
 p.paragraph_format.left_indent=Cm(.5);p.paragraph_format.first_line_indent=Cm(-.5)
 md.append(prefix+'['+label+']('+url+')'+(' (accessed 7 November 2026).' if 'n.d.' in prefix else '.')+'\n')
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');rpr=OxmlElement('w:rPr');sz=OxmlElement('w:sz');sz.set(qn('w:val'),'24');rpr.append(sz);run=OxmlElement('w:r');run.append(rpr);t=OxmlElement('w:t');t.text='1';run.append(t);fld.append(run);footer._p.append(fld)
doc.core_properties.title=title;doc.core_properties.subject='Green Building course essay';doc.core_properties.author=''
# Align document defaults as well as all used styles; avoid future style reflow.
for spacing in doc.styles.element.findall('.//' + qn('w:spacing')):
 if spacing.get(qn('w:line')) is not None:
  spacing.set(qn('w:line'),'240');spacing.set(qn('w:lineRule'),'auto')
path=OUT/'Hangzhou_Passive_Cooling_Course_Essay.docx';doc.save(path)
(OUT/'Hangzhou_Passive_Cooling_Course_Essay.md').write_text('\n'.join(md))
body=' '.join([title]+[v for _,ps in sections for v in ps]+results+[a+b for a,b,_ in refs])
print('Estimated words (excluding table numbers):',len(re.findall(r"\b[\w’'-]+\b",body)))
print('Saved',path)
