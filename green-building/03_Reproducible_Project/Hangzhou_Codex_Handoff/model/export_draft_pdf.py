"""Export the generated Markdown draft to PDF; independent of Word/LibreOffice."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
P=Path(__file__).resolve().parents[1]/'paper_draft'
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
normal=ParagraphStyle('normal',fontName='STSong-Light',fontSize=10,leading=15,spaceAfter=7,wordWrap='CJK')
styles={1:ParagraphStyle('title',parent=normal,fontSize=19,leading=26,spaceAfter=16,textColor=colors.HexColor('#244d5e')),2:ParagraphStyle('h1',parent=normal,fontSize=14,leading=20,spaceBefore=12,spaceAfter=8,keepWithNext=True),3:ParagraphStyle('h2',parent=normal,fontSize=11.5,leading=17,spaceBefore=8,spaceAfter=6,keepWithNext=True)}
small=ParagraphStyle('small',parent=normal,fontSize=7.3,leading=10,spaceAfter=2)
caption=ParagraphStyle('caption',parent=normal,fontSize=9,leading=13,alignment=TA_CENTER)
flow=[];lines=(P/'杭州住宅被动降温研究_论文草稿_v0.1.md').read_text().splitlines();i=0
while i<len(lines):
 line=lines[i].strip()
 if not line:i+=1;continue
 if line.startswith('|'):
  rows=[]
  while i<len(lines) and lines[i].startswith('|'):
   cells=[x.strip() for x in lines[i].strip('|').split('|')]
   if not all(set(x)<=set('-: ') for x in cells):rows.append([Paragraph(escape(x),small) for x in cells])
   i+=1
  t=Table(rows,colWidths=[490/len(rows[0])]*len(rows[0]),repeatRows=1,hAlign='LEFT')
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dce9ed')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#a3b6bf')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
  flow.extend([t,Spacer(1,9)]);continue
 if line.startswith('!['):
  m=re.match(r'!\[(.*?)\]\((.*?)\)',line);path=P/m[2];w,h=ImageReader(str(path)).getSize();width=490;height=min(370,width*h/w)
  if height==370:width=height*w/h
  flow.append(KeepTogether([Image(str(path),width=width,height=height),Paragraph(escape(m[1]),caption),Spacer(1,10)]))
 else:
  m=re.match(r'^(#{1,3}) (.*)',line)
  flow.append(Paragraph(escape(m[2] if m else line),styles[len(m[1])] if m else normal))
 i+=1

def page(canvas,doc):
 canvas.setFont('STSong-Light',8);canvas.setFillColor(colors.HexColor('#4a6570'));canvas.drawString(45,815,'杭州住宅被动降温研究｜论文草稿 v0.1');canvas.drawRightString(550,27,f'第 {doc.page} 页')
path=P/'杭州住宅被动降温研究_论文草稿_v0.1.pdf'
SimpleDocTemplate(str(path),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=48,bottomMargin=44,title='杭州夏季住宅外遮阳与夜间通风：论文草稿',author='课程研究草稿').build(flow,onFirstPage=page,onLaterPages=page)
import fitz
pdf=fitz.open(path);print('PDF pages:',len(pdf))
preview=P.parent/'work'
preview.mkdir(exist_ok=True)
for idx in [0,min(6,len(pdf)-1)]:pdf[idx].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(str(preview/f'draft_preview_{idx+1}.png'))
assert len(pdf)>5 and '杭州' in pdf[0].get_text()
print('PDF verification: PASS',path.stat().st_size)
