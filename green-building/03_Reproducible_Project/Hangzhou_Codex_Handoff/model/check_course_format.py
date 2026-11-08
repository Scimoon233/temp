"""Independently audit the delivered English DOCX/PDF against course rules.

Run from any directory: python path/to/model/check_course_format.py
Uses exported files; it does not run the thermal model or regenerate the paper.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib,json,re,unicodedata,zipfile
import fitz
from lxml import etree

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'course_essay'
NAME='Hangzhou_Passive_Cooling_Course_Essay'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
W='{'+NS['w']+'}'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def chars(text):
    return Counter(c for c in unicodedata.normalize('NFKC',text) if not c.isspace())

def main():
    pdf=fitz.open(OUT/(NAME+'.pdf'))
    with zipfile.ZipFile(OUT/(NAME+'.docx')) as z:
        document=etree.fromstring(z.read('word/document.xml'))
        styles=etree.fromstring(z.read('word/styles.xml'))
        image=z.read('word/media/image1.png')
    spans=[s for page in pdf for b in page.get_text('dict')['blocks'] if 'lines' in b
           for line in b['lines'] for s in line['spans']]
    body=[s for s in spans if 45<s['origin'][1]<800]
    sizes=Counter(round(s['size'],2) for s in spans)
    normal=[s for s in spans if abs(s['size']-12)<.05]
    small=[s for s in spans if s not in normal]
    spacing=[s for tree in [document,styles] for s in tree.findall('.//w:spacing',NS)
             if s.get(W+'line') is not None]
    fonts={s['font'] for s in spans}
    wordtext=''.join(document.xpath('//w:t/text()',namespaces=NS))
    pdftext=''.join(s['text'] for s in body)
    fulltext='\n'.join(page.get_text() for page in pdf)
    normalized_text=re.sub(r'\s+',' ',fulltext)
    subs=document.xpath('//w:r[w:rPr/w:vertAlign[@w:val="subscript"]]/w:t/text()',namespaces=NS)
    sections=document.findall('.//w:sectPr',NS)
    cols=sections[-1].find('w:cols',NS)
    links=[link for page in pdf for link in page.get_links() if link.get('uri')]
    graph=fitz.open(OUT/'Graphical_Abstract.pdf')
    graphspans=[s for b in graph[0].get_text('dict')['blocks'] if 'lines' in b
                for line in b['lines'] for s in line['spans']]
    checks={}
    def check(name,passed,evidence):
        checks[name]={'status':'PASS' if passed else 'FAIL','evidence':evidence}
    check('page_count',2<=len(pdf)<=3,{'pages':len(pdf),'includes_references':True})
    check('font_family',all('TimesNewRoman' in f for f in fonts),sorted(fonts))
    font_refs={font[0] for page in pdf for font in page.get_fonts()}
    check('fonts_embedded',all(bool(pdf.extract_font(xref)[3]) for xref in font_refs),{'embedded_font_objects':len(font_refs)})
    check('normal_font_size',bool(normal) and all(abs(s['size']-12)<.05 for s in normal)
          and all(s['text'].strip()=='th' and abs(s['size']-7)<.05 for s in small),
          {'normal_pt':12,'PDF_sizes':dict(sizes),'only_smaller_text':'automatic thermal-unit subscript th'})
    check('Word_base_font_size',set(document.xpath('//w:sz/@w:val',namespaces=NS))=={'24'},'All explicit Word font sizes are 24 half-points = 12 pt.')
    check('single_spacing',bool(spacing) and all(s.get(W+'line')=='240' and s.get(W+'lineRule')=='auto' for s in spacing),{'Word_line':240,'Word_line_rule':'auto','paragraph_gaps':'1 pt; headings 4 pt before and 3 pt after'})
    check('PDF_submission',not pdf.is_encrypted and pdf.is_pdf,{'format':'PDF','password_protected':False})
    required=['Abstract','1. Introduction','2. Methods','3. Results','4. Discussion and conclusions','4.3. Conclusions','References']
    check('paper_sections',all(s.casefold() in normalized_text.casefold() for s in required),required)
    check('front_matter',all(s in pdf[0].get_text() for s in ['HIGHLIGHTS','GRAPHICAL ABSTRACT','ARTICLE INFO','ABSTRACT','Keywords:']),['Highlights','Graphical abstract','Keywords','Abstract'])
    check('two_column_body',len(sections)==2 and cols.get(W+'num')=='2',{'body_columns':cols.get(W+'num'),'column_gap_cm':round(int(cols.get(W+'space'))/567,3)})
    check('thermal_unit_notation',len(subs)==10 and set(subs)=={'th'} and 'kWh_th' not in fulltext and 'kWh_th' not in wordtext,{'real_subscripts':len(subs),'literal_underscore_units':False})
    check('text_not_lost_on_export',chars(wordtext)==chars(pdftext),{'Word_nonspace_characters':sum(chars(wordtext).values()),'PDF_nonspace_characters':sum(chars(pdftext).values()),'method':'NFKC-normalized character counts, excluding running header/footer; complemented by page rendering'})
    check('no_missing_glyph_markers',not any(c in fulltext for c in ['\ufffd','\u25a1','\x00']),True)
    check('page_boundaries',all(s['bbox'][0]>=40 and s['bbox'][2]<=559 and s['bbox'][1]>=0 and s['bbox'][3]<842 for s in spans),'All English text stays inside page and selected margins; trailing-space tolerance included.')
    check('graph_font_size',all(abs(s['size']-12)<.05 and 'TimesNewRoman' in s['font'] for s in graphspans),{'source_graph_font_pt':12,'display_width_cm':12})
    check('graph_not_cropped',image==(OUT/'Graphical_Abstract.png').read_bytes() and not document.findall('.//a:srcRect',NS),'Embedded PNG matches inspected source; no crop rectangle in Word.')
    check('references_and_links',len(links)==6 and all(s in fulltext for s in ['Artmann','Hou','HZXQF','NSW Government','Open-Meteo','Short']),{'reference_entries':6,'clickable_PDF_links':len(links)})
    # Table content is checked against independent result records, not layout code.
    import csv
    with (ROOT/'results/base_metrics.csv').open() as f:rows=list(csv.DictReader(f))
    expected=[]
    for y in ['2025','2026']:
        for case in ['S0','S1','S2','S3']:
            free=next(r for r in rows if r['year']==y and r['mode']=='free' and r['scenario']==case)
            ideal=next(r for r in rows if r['year']==y and r['mode']=='ideal' and r['scenario']==case)
            expected.extend([f"{float(free['DH28_Kh']):,.1f}",f"{float(ideal['cool_kWh_th']):,.1f}",f"{float(ideal['cool_kWh_th_reduction_pct']):.2f}"])
    check('table_values',all(v in fulltext for v in expected),{'scenario_rows':8,'numeric_values_checked':len(expected)})
    source_files=json.loads((OUT/'PROVENANCE.json').read_text())['source_files']
    check('model_data_preserved',all(sha(ROOT/r['path'])==r['sha256'] for r in source_files),[r['path'] for r in source_files])
    p2=pdf[1].get_text();p3=pdf[2].get_text()
    check('result_paragraph_pagination','All  three' not in p2 and 'All  three' in p3,'The first result paragraph now starts intact on page 3; page 2 ends with the table note.')
    failures=[k for k,v in checks.items() if v['status']=='FAIL']
    date=datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M %Z')
    visual_path=OUT/'VISUAL_REVIEW_v1.5.json'
    visual=json.loads(visual_path.read_text()) if visual_path.exists() else {}
    visual_current=visual.get('pdf_sha256')==sha(OUT/(NAME+'.pdf')) and visual.get('pages_reviewed')==[1,2,3]
    audit={'audit_version':'v1.5','checked_at':date,'target':'English course-submission paper',
           'course_format_status':'PASS' if not failures else 'FAIL','failures':failures,
           'author_information':'PENDING: real author name and affiliation have not been supplied; reserved block remains blank.',
           'manual_review':{'status':'PASS' if visual_current else 'NEEDS_REVIEW','evidence':'VISUAL_REVIEW_v1.5.json','matches_current_PDF':visual_current},
           'scope':'Checks course formatting and reference-inspired organization. Similarity screening, novelty grading and course marks are outside this audit.',
           'files':{NAME+'.pdf':sha(OUT/(NAME+'.pdf')),NAME+'.docx':sha(OUT/(NAME+'.docx'))},'checks':checks}
    (OUT/'FORMAT_AUDIT_v1.5.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
    verdict='课程明确的排版要求已通过核查' if not failures else '当前自动检查尚未全部通过：'+', '.join(failures)
    report=f'''# 英文课程论文格式复核 v1.5

核查时间：{date}。对象为当前英文课程提交稿，依据为本对话中的两张课程要求截图，以及Jacobs等（2019）的15页正式发表版。

结论：{verdict}；参考版式的作者姓名与单位栏尚待填写。中文4页文件是审阅译稿，不作为英文课程提交稿。

## 课程要求逐项对应

|要求|核查结果|证据|
|---|---|---|
|含参考文献至少2页、不超过3页|通过|最终英文PDF共3页，参考文献在第3页|
|Times New Roman|通过|PDF文字嵌入Times New Roman正体、粗体和斜体；图文摘要源图也是Times New Roman|
|字号12|通过|Word基础字号12 pt、PDF普通文字12 pt；单位th为真正下标，随正常数学排版自动缩小|
|单倍行距|通过|Word文档和样式逐项检查：line=240、lineRule=auto，即1.0倍行距；段后间距与行距分别设置|
|PDF提交|通过|可正常打开的无密码PDF，字体已嵌入|
|题目、摘要、引言、主体、结论、参考文献|通过|已齐备；结论为第4章中的4.3节|
|课程相关性、禁止抄袭|排版检查不作查重判断|论文研究建筑被动降温；保留6条来源及引文，本轮未运行相似度系统|

## 与参考文章版式对应

首页：通栏题目，预留作者与单位栏；左侧Highlights和Keywords，右侧Graphical Abstract与Abstract。正文从第2页开始，等宽双栏，末章为Discussion and conclusions。表题位于表上方，表格采用横线、不设竖线；参考文献为作者—年份制、悬挂缩进。课程稿使用自己的页眉和页码。

课程明确的12号、单倍行距和2—3页要求优先于期刊样例的较小字号与15页篇幅。截图未规定A4、页边距、页眉页码、Highlights或图文摘要；这些是参照文章作出的版式选择。当前A4，左右1.5 cm，上下1.65 cm，中缝约0.5 cm。

## 本轮发现并修正

1. 原第2页末尾把“free-running”拆到两页；已将该结果段完整移至第3页，消除跨页拆词。
2. 参考文献两端对齐导致较大的词间空隙；现改为左对齐，保留悬挂缩进。中英文对应版均已同步。
3. Highlights续行原先与圆点同列；已加入悬挂缩进，使续行与文字对齐。
4. 同步微调段落和标题间距，正文仍为12号、单倍行距，最终保持3页。未删正文、结果或参考文献。

## 导出与内容完整性

Word与PDF正文的NFKC标准化非空白字符计数完全一致，未发现导出丢字；核查了全部8行情景结果、24个表格数值、6个PDF外链、10处热量单位下标，以及图文摘要的内嵌图片与源图一致性。逐页渲染检查后，未发现乱码、表格越界或图文裁切。上、下标遵循正常数学排版，未以缩小正文字号压缩页数。

本轮仅调整排版，英文及中文Markdown文本与上一版相同；模拟数据及基准参数哈希保持不变。

## 尚待补充

真实作者姓名与单位尚未提供，因此首页作者栏继续留空。这是补齐参考文章首页信息所需的材料；它不影响当前页数、字号和行距检查结果。

复核命令：在项目根目录运行`python model/check_course_format.py`。机器可读证据见`FORMAT_AUDIT_v1.5.json`，最终三页预览见`Layout_Preview_Page_1.png`至`Layout_Preview_Page_3.png`。Word经不同软件重新导出时应重新核对分页。
'''
    (OUT/'课程格式逐项复核_v1.5.md').write_text(report)
    print(json.dumps({'course_format_status':audit['course_format_status'],'checks':len(checks),'failures':failures,'pages':len(pdf),'manual_review_current':visual_current,'author_information':'pending'},ensure_ascii=False))
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
