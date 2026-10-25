"""Render the supplied ideal leaf-envelope projection over the existing 25 times.
This changes presentation only; no new leaf or thermal scenario is introduced.
"""
from pathlib import Path
import os,sys,importlib.util,json,io
os.environ['MPLCONFIGDIR']='/workspace/ppt-tools/cache/matplotlib'
sys.path.insert(0,'/workspace/ppt-tools/model-inspect')
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MP
from matplotlib.patches import PathPatch,Rectangle,Circle
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from PIL import Image
b=Path(__file__).resolve().parents[1];out=b/'assets';B=Path('/workspace/ppt-extension/06_参数与植物生长情景模拟')
sp=importlib.util.spec_from_file_location('sim',B/'复算/重算情景.py');sim=importlib.util.module_from_spec(sp);sp.loader.exec_module(sim)
case=next(c for c in json.loads((B/'复算/input_data/cases.json').read_text()) if c['id']=='D_BASE');outer,inner=sim.boundary(case)
d=json.loads((out/'chart-data.json').read_text());frames=[];records=[]
def patch(ax,geom,color):
 if geom.is_empty:return
 if geom.geom_type=='Polygon':
  g=orient(geom,sign=1);p=MP.make_compound_path(MP(np.asarray(g.exterior.coords),closed=True),*[MP(np.asarray(r.coords),closed=True) for r in g.interiors]);ax.add_patch(PathPatch(p,facecolor=color,edgecolor='none'))
 else:
  for g in geom.geoms:patch(ax,g,color)
for j,t in enumerate(np.arange(9,15.001,.25)):
 sun=sim.solar(23.44,t);shadow=Polygon(sim.project(outer,sun),[sim.project(inner,sun)[::-1]]);overlap=shadow.intersection(sim.TARGET)
 val=100*overlap.area/sim.TARGET.area;expected=d['ideal_curves']['Solstice'][j];assert abs(val-expected)<1e-8
 fig=plt.figure(figsize=(9,4.2),facecolor='#F8F7F2');ax=fig.add_axes([.02,.02,.96,.82]);patch(ax,shadow,'#C1D3BE');patch(ax,overlap,'#639274');ax.add_patch(Rectangle((-2.5,-2.5),5,5,fill=False,ec='#AA7E4A',lw=1.5));ax.add_patch(Circle((0,0),.75,fill=False,ec='#AA7E4A',lw=1.1));ax.plot(0,0,'o',color='#173C51',ms=3);ax.set(xlim=(-7,7),ylim=(-4,4),aspect='equal');ax.axis('off')
 # The moving dot is encoded in the GIF; all time labels/legend remain editable in PPT.
 tl=fig.add_axes([.20,.90,.60,.04]);tl.plot([9,15],[.5,.5],color='#A7B7A2',lw=1.5)
 for tick in [9,12,15]:tl.plot([tick,tick],[.32,.68],color='#AA7E4A',lw=1)
 tl.plot(t,.5,'o',color='#346A55',ms=7);tl.set(xlim=(8.85,15.15),ylim=(0,1));tl.axis('off')
 buf=io.BytesIO();fig.savefig(buf,dpi=120,facecolor='#F8F7F2');plt.close(fig);buf.seek(0);im=Image.open(buf).convert('RGB');frames.append(im.copy())
 if t==12:im.save(out/'ideal-shadow-animated-static.png')
 records.append({'solar_time_h':float(t),'overlap_percent':val,'source_curve_percent':expected})
frames[0].save(out/'ideal-shadow-sequence.gif',save_all=True,append_images=frames[1:],duration=[1000 if r['solar_time_h'] in [9.,12.,15.] else 280 for r in records],loop=0,disposal=2)
with Image.open(out/'ideal-shadow-sequence.gif') as gif:assert gif.n_frames==25
(b/'Ideal-Animation-Check.json').write_text(json.dumps({'metric':'ideal continuous-leaf target overlap','latitude_N':30,'declination_deg':23.44,'solar_time_h':[9,15],'interval_minutes':15,'frames':25,'max_absolute_curve_difference_percentage_points':max(abs(r['overlap_percent']-r['source_curve_percent'])for r in records),'dynamic_text':False,'values':records},indent=2))
print('Created 25-frame ideal-shadow GIF; all values match the existing source curve.')
