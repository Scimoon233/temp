"""Journal-style course layout, adapted from Jacobs et al. (2019).

Run write_course_essay.py, then write_chinese_course_essay.py. Course rules
override the sample's small fonts: all document text remains 12 pt, single spaced.
"""
from pathlib import Path
import json,re
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.text.run import Run
from copy import deepcopy

def font(run,zh=False):
    run.font.name='Times New Roman';run.font.size=Pt(12)
    pr=run._element.get_or_add_rPr();rf=pr.rFonts
    if rf is None:rf=OxmlElement('w:rFonts');pr.insert(0,rf)
    for k in list(rf.attrib):
        if k.endswith('Theme'):del rf.attrib[k]
    for k in ['ascii','hAnsi','cs']:rf.set(qn('w:'+k),'Times New Roman')
    rf.set(qn('w:eastAsia'),'Noto Serif CJK SC' if zh else 'Times New Roman')

def paragraph(container,text='',bold=False,italic=False,indent=False,heading=False,zh=False):
    p=container.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
    f=p.paragraph_format;f.line_spacing=1.;f.space_before=Pt(0);f.space_after=Pt(3)
    f.widow_control=True
    if indent:f.first_line_indent=Cm(.35)
    if heading:f.space_before=Pt(6);f.space_after=Pt(5);f.keep_with_next=True
    r=p.add_run(text);font(r,zh);r.bold=bold;r.italic=italic
    return p

def line(p,side='bottom',size='4'):
    pr=p._p.get_or_add_pPr();b=OxmlElement('w:pBdr');el=OxmlElement('w:'+side)
    for k,v in [('val','single'),('sz',size),('color','999999'),('space','5')]:el.set(qn('w:'+k),v)
    b.append(el);pr.append(b)

def configure(doc,zh=False):
    sec=doc.sections[0];sec.page_width=Cm(21);sec.page_height=Cm(29.7)
    sec.top_margin=Cm(1.65);sec.bottom_margin=Cm(1.65)
    sec.left_margin=sec.right_margin=Cm(1.5)
    sec.header_distance=sec.footer_distance=Cm(.75)
    for s in doc.styles:
        if s.type in [1,2]:
            s.font.name='Times New Roman';s.font.size=Pt(12);s.font.color.rgb=RGBColor(0,0,0)
            s.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Noto Serif CJK SC' if zh else 'Times New Roman')
            if s.type==1:
                s.paragraph_format.line_spacing=1.;s.paragraph_format.space_after=Pt(3)
    h=sec.header.paragraphs[0];h.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=h.add_run('Green Building | Course essay');font(r,zh);r.italic=True
    line(h)
    foot=sec.footer.paragraphs[0];foot.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');foot._p.append(field)
    # Explicit defaults cover page-number fields and the table's empty cells.
    defaults=doc.styles.element.find(qn('w:docDefaults'))
    if defaults is not None:
        for sz in defaults.findall('.//'+qn('w:sz')):sz.set(qn('w:val'),'24')
    return sec

def cell_label(cell,label,zh=False):
    p=paragraph(cell,label,heading=True,zh=zh);p.alignment=WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before=Pt(4);p.paragraph_format.space_after=Pt(9);line(p)

def clear_cell(cell):
    p=cell.paragraphs[0];p.paragraph_format.space_after=Pt(0)
    p.paragraph_format.line_spacing=1.;p.paragraph_format.keep_with_next=True
    p.paragraph_format.space_before=Pt(0)
    # Remove the unused initial paragraph; each cell receives content below.
    cell._tc.remove(p._p)

def graphical_abstract(root,out,zh=False):
    """Show the intervention, separate operating modes, and resulting design choice."""
    for p in [Path('/usr/share/fonts/truetype/msttcorefonts'),Path('/workspace/work/course_essay/fonts')]:
        if p.exists():
            for f in p.glob('*.TTF'):font_manager.fontManager.addfont(str(f))
            for f in p.glob('*.ttf'):font_manager.fontManager.addfont(str(f))
    plt.rcParams.update({'font.family':'Times New Roman','font.size':12})
    data=pd.read_csv(root/'results/base_metrics.csv');values=[]
    for y in [2025,2026]:
        a=data[(data.year==y)&(data['mode']=='free')].set_index('scenario')
        b=data[(data.year==y)&(data['mode']=='ideal')].set_index('scenario')
        assert a.loc['S2','DH28_Kh']<a.loc['S1','DH28_Kh']
        assert b.loc['S1','cool_kWh_th']<b.loc['S2','cool_kWh_th']
        values.append([a.loc['S0','mean_C']-a.loc['S3','mean_C'],100*(1-a.loc['S3','DH28_Kh']/a.loc['S0','DH28_Kh']),100*(1-b.loc['S3','cool_kWh_th']/b.loc['S0','cool_kWh_th'])])
    ranges=[f'{min(v[i] for v in values):.{1 if i==1 else 2}f}–{max(v[i] for v in values):.{1 if i==1 else 2}f}' for i in range(3)]
    from matplotlib.patches import FancyBboxPatch
    fig,ax=plt.subplots(figsize=(4.72,3.65));fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
    fp=font_manager.FontProperties(family='Times New Roman',size=12)
    cjk={}
    if zh:
        # Matplotlib sees only the first face of some CJK collections. Extract the
        # fontconfig-selected SC face into a local cache, outside deliverables.
        import subprocess,tempfile
        from fontTools.ttLib import TTFont
        cache=Path(tempfile.gettempdir())/'green_building_font_cache';cache.mkdir(exist_ok=True)
        for bold,style in [(False,'Regular'),(True,'Bold')]:
            match=subprocess.check_output(['fc-match','-f','%{file}\n%{index}','Noto Serif CJK SC:style='+style],text=True).strip().splitlines()
            fontfile=Path(match[0]);face=int(match[1]) if len(match)>1 else 0
            if fontfile.suffix.lower()=='.ttc':
                extracted=cache/('NotoSerifCJK-SC-'+style+'.ttf')
                if not extracted.exists():
                    tt=TTFont(str(fontfile),fontNumber=face);tt.save(extracted);tt.close()
                fontfile=extracted
            cjk[bold]=font_manager.FontProperties(fname=str(fontfile),size=12)
    def text(x,y,s,bold=False,color='#172d3b'):
        prop=cjk[bold].copy() if zh else fp.copy();prop.set_weight('bold' if bold else 'normal')
        return ax.text(x,y,s,ha='center',va='center',fontproperties=prop,color=color,linespacing=1.12)
    def box(x,y,w,h,fill):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.005,rounding_size=0.012',facecolor=fill,edgecolor='#527084',linewidth=.8))
    def arrow(start,end):
        ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','lw':1,'color':'#527084'})
    text(.5,.968,'杭州住宅 · 2025—2026年夏季' if zh else 'Hangzhou dwelling · summers 2025–2026')
    box(.015,.755,.46,.145,'#edf3f6');box(.525,.755,.46,.145,'#edf3f6')
    text(.245,.827,'外遮阳\n减少白天太阳得热' if zh else 'External shading\nReduce daytime heat')
    text(.755,.827,'夜间通风\n排出室内蓄热' if zh else 'Night ventilation\nDischarge heat at night')
    arrow((.245,.75),(.39,.708));arrow((.755,.75),(.61,.708))
    box(.04,.63,.92,.075,'#dce9ee')
    text(.5,.668,'组合措施（S3）相对基准（S0）' if zh else 'Combined (S3) versus baseline (S0)',True)
    arrow((.39,.63),(.245,.59));arrow((.61,.63),(.755,.59))
    box(.015,.135,.46,.45,'#f6f8f9');box(.525,.135,.46,.45,'#f6f8f9')
    text(.245,.551,'无空调自由运行' if zh else 'No air conditioning',True)
    text(.245,.487,'平均室内空气温度' if zh else 'Mean indoor temperature')
    text(.245,.435,'降低 '+ranges[0]+'°C' if zh else 'Lower by '+ranges[0]+'°C',True)
    text(.245,.367,'超过28°C的过热度时' if zh else 'Overheating degree-hours')
    text(.245,.315,'降低 '+ranges[1]+'%' if zh else '(above 28°C): −'+ranges[1]+'%')
    text(.245,.205,'更有效的单项措施：\n夜间通风' if zh else 'Best single measure:\nnight ventilation')
    text(.755,.551,'维持26°C理想制冷' if zh else 'Cooling held at 26°C',True)
    text(.755,.453,'理想显热制冷需求' if zh else 'Ideal sensible demand')
    text(.755,.383,'降低 '+ranges[2]+'%' if zh else 'Lower by '+ranges[2]+'%',True)
    text(.755,.205,'更有效的单项措施：\n外遮阳' if zh else 'Best single measure:\nexternal shading')
    text(.5,.072,'白天遮阳；夜间室外至少比室内低1°C时通风。' if zh else 'Shade by day; open on cooler nights\n(outdoors at least 1°C below indoors).')
    out.mkdir(exist_ok=True);path=out/'Graphical_Abstract.png';fig.savefig(path,dpi=250);fig.savefig(out/'Graphical_Abstract.pdf');plt.close(fig)
    return path

def front(doc,title,abstract,root,out,zh=False):
    p=paragraph(doc,title,bold=True,zh=zh);p.alignment=WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before=Pt(18);p.paragraph_format.space_after=Pt(12)
    # An empty author/affiliation block is reserved for the student's real details.
    p=paragraph(doc,'',zh=zh);p.paragraph_format.space_after=Pt(15);line(p)
    table=doc.add_table(rows=2,cols=2);table.autofit=False
    widths=[5.05,12.95]
    for row in table.rows:
        for c,w in zip(row.cells,widths):c.width=Cm(w);clear_cell(c)
    for c,w in zip(table.columns,widths):c.width=Cm(w)
    cells=[c for row in table.rows for c in row.cells]
    # Different cell margins create the sample's broad separator between columns.
    for i,c in enumerate(cells):
        margins=OxmlElement('w:tcMar')
        for name,val in [('left','0'),('right','350' if i%2==0 else '0'),('top','80'),('bottom','80')]:
            e=OxmlElement('w:'+name);e.set(qn('w:w'),val);e.set(qn('w:type'),'dxa');margins.append(e)
        c._tc.get_or_add_tcPr().append(margins)
    cell_label(cells[0],'HIGHLIGHTS',zh);cell_label(cells[1],'GRAPHICAL ABSTRACT',zh)
    points=(['组合措施降低夏季平均室温1.85—2.12°C。','过热度时降低17.5%—17.7%。','理想显热制冷需求降低6.44%—7.01%。'] if zh else [
        'Combined measures lower mean summer air temperature by 1.85–2.12°C.',
        'Overheating degree-hours decrease by 17.5–17.7%.',
        'Ideal sensible cooling demand decreases by 6.44–7.01%.'])
    for t in points:
        p=paragraph(cells[0],'• '+t,zh=zh);p.alignment=WD_ALIGN_PARAGRAPH.LEFT;p.paragraph_format.space_after=Pt(8)
    p=paragraph(cells[1]);p.add_run().add_picture(str(graphical_abstract(root,out,zh)),width=Cm(12))
    p=paragraph(cells[1],'Ranges span 2025–2026; S3 relative to S0. Single measures compare S1 with S2 for the baseline parameters.' if not zh else '范围对应2025、2026年，降幅均为S3相对S0；单项措施排序对应基准参数下S1与S2的比较。',zh=zh)
    p.alignment=WD_ALIGN_PARAGRAPH.LEFT
    cell_label(cells[2],'ARTICLE INFO',zh);cell_label(cells[3],'ABSTRACT',zh)
    paragraph(cells[2],'Keywords:' if not zh else '关键词：',italic=True,zh=zh)
    for word in (['External shading','Night ventilation','Thermal network','Overheating','Sensible cooling','Hangzhou'] if not zh else ['外遮阳','夜间通风','热网络','过热','显热制冷','杭州']):
        p=paragraph(cells[2],word,zh=zh);p.alignment=WD_ALIGN_PARAGRAPH.LEFT
    paragraph(cells[3],abstract,zh=zh)
    # A new page mirrors the published reference: only front matter on page 1.
    sec=doc.add_section(WD_SECTION_START.NEW_PAGE)
    cols=sec._sectPr.find(qn('w:cols'));cols.set(qn('w:num'),'2');cols.set(qn('w:space'),'284')

def heading(doc,text,zh=False,sub=False):
    p=paragraph(doc,text,bold=not sub,italic=sub,heading=True,zh=zh)
    p.alignment=WD_ALIGN_PARAGRAPH.LEFT

def results_table(doc,root,zh=False):
    for text in (['表1','四情景的自由运行过热度时和理想显热制冷需求。'] if zh else ['Table 1','Free-running overheating and ideal sensible cooling by scenario.']):
        p=paragraph(doc,text,zh=zh);p.alignment=WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.keep_with_next=True
    data=pd.read_csv(root/'results/base_metrics.csv');t=doc.add_table(rows=1,cols=4);t.autofit=False
    widths=[1.2,2.6,2.6,2.1]
    labels=['情景','DH28\n(K h)','Qs\n(kWh_th)','降低\n(%)'] if zh else ['Case','DH28\n(K h)','Qs\n(kWh_th)','Cut\n(%)']
    for c,label in zip(t.rows[0].cells,labels):c.text=label
    for y in [2025,2026]:
        c=t.add_row().cells[0];c.merge(t.rows[-1].cells[-1]);c.text=str(y)
        for s in ['S0','S1','S2','S3']:
            a=data[(data.year==y)&(data['mode']=='free')&(data.scenario==s)].iloc[0]
            b=data[(data.year==y)&(data['mode']=='ideal')&(data.scenario==s)].iloc[0]
            vals=[s,f'{a.DH28_Kh:,.1f}',f'{b.cool_kWh_th:,.1f}',f'{b.cool_kWh_th_reduction_pct:.2f}']
            for c,val in zip(t.add_row().cells,vals):c.text=val
    for col,w in zip(t.columns,widths):col.width=Cm(w)
    for i,row in enumerate(t.rows):
        row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
        for c,w in zip(row.cells,widths):
            c.width=Cm(w)
            for p in c.paragraphs:
                p.paragraph_format.line_spacing=1.;p.paragraph_format.space_after=Pt(1)
                if i in [0,1]:p.paragraph_format.keep_with_next=True
                for r in p.runs:font(r,zh);r.bold=i in [0,1,6]
    t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
    margins=OxmlElement('w:tblCellMar')
    for side in ['left','right']:
        e=OxmlElement('w:'+side);e.set(qn('w:w'),'30');e.set(qn('w:type'),'dxa');margins.append(e)
    t._tbl.tblPr.append(margins)
    border=OxmlElement('w:tblBorders')
    for side in ['top','bottom']:
        e=OxmlElement('w:'+side);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');border.append(e)
    t._tbl.tblPr.append(border)
    paragraph(doc,'Qs为26°C理想显热移除量；降低率相对同年S0。' if zh else 'Qs: ideal sensible heat removal at 26°C. Cuts are relative to the same year’s S0.',zh=zh)

def link(p,label,url,zh=False):
    h=OxmlElement('w:hyperlink');h.set(qn('r:id'),p.part.relate_to(url,RT.HYPERLINK,is_external=True))
    r=OxmlElement('w:r');pr=OxmlElement('w:rPr');rf=OxmlElement('w:rFonts')
    for k in ['ascii','hAnsi','cs']:rf.set(qn('w:'+k),'Times New Roman')
    pr.append(rf);size=OxmlElement('w:sz');size.set(qn('w:val'),'24');pr.append(size);r.append(pr)
    text=OxmlElement('w:t');text.text=label;r.append(text);h.append(r);p._p.append(h)

def thermal_unit_subscripts(doc):
    """Typeset the thermal qualifier, preserving each run's font and emphasis."""
    for element in list(doc.element.body.iter(qn('w:r'))):
        original=Run(element,None).text
        if 'kWh_th' not in original:continue
        parent=element.getparent();index=parent.index(element)
        for part in re.split('(kWh_th)',original):
            pieces=[('kWh',False),('th',True)] if part=='kWh_th' else [(part,False)]
            for value,subscript in pieces:
                if not value:continue
                clone=deepcopy(element);run=Run(clone,None);run.text=value
                if subscript:run.font.subscript=True
                parent.insert(index,clone);index+=1
        parent.remove(element)

def save(doc,out,name,title,zh=False):
    doc.core_properties.title=title;doc.core_properties.subject='Green Building course essay';doc.core_properties.author=''
    for spacing in doc.styles.element.findall('.//'+qn('w:spacing')):
        if spacing.get(qn('w:line')) is not None:spacing.set(qn('w:line'),'240');spacing.set(qn('w:lineRule'),'auto')
    thermal_unit_subscripts(doc)
    path=out/(name+'.docx');doc.save(path);print('Saved',path)

def build_english(root,out,title,sections,results,refs,data):
    doc=Document();configure(doc);parts=dict(sections)
    front(doc,title,parts['Abstract'][0],root,out)
    md=['# '+title,'','## Highlights','','• Combined measures lower mean summer air temperature by 1.85–2.12°C.','• Overheating degree-hours decrease by 17.5–17.7%.','• Ideal sensible cooling demand decreases by 6.44–7.01%.','','## Abstract','',parts['Abstract'][0],'','Keywords: External shading; Night ventilation; Thermal network; Overheating; Sensible cooling; Hangzhou.','']
    for name in ['1. Introduction','2. Methods','3. Results']:
        heading(doc,name);md+=['## '+name,'']
        if name=='3. Results':
            results_table(doc,root)
            md+=['Table 1. Baseline scenario comparison; cooling is ideal sensible heat removal.','|Year|Case|DH28 (K h)|Cooling (kWh_th)|Cooling cut (%)|','|---|---|---|---|---|']
            for y in [2025,2026]:
                for s in ['S0','S1','S2','S3']:
                    a=data[(data.year==y)&(data['mode']=='free')&(data.scenario==s)].iloc[0];b=data[(data.year==y)&(data['mode']=='ideal')&(data.scenario==s)].iloc[0]
                    md.append(f'|{y}|{s}|{a.DH28_Kh:,.1f}|{b.cool_kWh_th:,.1f}|{b.cool_kWh_th_reduction_pct:.2f}|')
            ps=results
        else:ps=parts[name]
        for text in ps:paragraph(doc,text,indent=True);md += ['',text,'']
    heading(doc,'4. Discussion and conclusions');md+=['## 4. Discussion and conclusions','']
    for sub,ps in [('4.1. Design implications',parts['4. Discussion'][:2]),('4.2. Scope and further work',parts['4. Discussion'][2:]),('4.3. Conclusions',parts['5. Conclusion'])]:
        heading(doc,sub,sub=True);md+=['### '+sub,'']
        for text in ps:paragraph(doc,text,indent=True);md += [text,'']
    heading(doc,'References');md+=['## References','']
    for prefix,label,url in refs:
        p=paragraph(doc,prefix);link(p,label,url);r=p.add_run(' (accessed 7 November 2026).' if 'n.d.' in prefix else '.');font(r)
        p.paragraph_format.left_indent=Cm(.35);p.paragraph_format.first_line_indent=Cm(-.35)
        md.append(prefix+'['+label+']('+url+')'+(' (accessed 7 November 2026).' if 'n.d.' in prefix else '.')+'\n')
    save(doc,out,'Hangzhou_Passive_Cooling_Course_Essay',title)
    (out/'Hangzhou_Passive_Cooling_Course_Essay.md').write_text('\n'.join(md).replace('kWh_th','kWh<sub>th</sub>'))

def build_chinese(root,out,text,rows):
    doc=Document();configure(doc,True);title=text.splitlines()[0][2:]
    abstract=text.split('## 摘要\n',1)[1].split('\n\n## ',1)[0]
    front(doc,title,abstract,root,out,True)
    # English section organization is mirrored in the Chinese reading copy.
    text=text.replace('## 4 讨论','## 4 讨论与结论\n### 4.1 设计启示').replace('本研究属于未经实测校准的原型比较。','### 4.2 研究范围与后续工作\n本研究属于未经实测校准的原型比较。').replace('## 5 结论','### 4.3 结论')
    body=text.split('## 1 引言',1)[1];lines=('## 1 引言'+body).splitlines();in_table=False
    for line_ in lines:
        line_=line_.strip()
        if not line_:continue
        if line_.startswith('|'):
            if not in_table:results_table(doc,root,True);in_table=True
            continue
        if line_.startswith('表1 ') or line_.startswith('DH28对应自由运行'):continue
        if line_.startswith('### '):heading(doc,line_[4:],True,True)
        elif line_.startswith('## '):heading(doc,line_[3:],True)
        else:
            p=paragraph(doc,'',indent=True,zh=True);pos=0
            for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)',line_):
                font(p.add_run(line_[pos:m.start()]),True);link(p,m[1],m[2],True);pos=m.end()
            font(p.add_run(line_[pos:]),True)
    save(doc,out,'杭州住宅被动降温_英文短稿对应中文版',title,True)
    (out/'杭州住宅被动降温_英文短稿对应中文版.md').write_text(text.replace('kWh_th','kWh<sub>th</sub>'))
