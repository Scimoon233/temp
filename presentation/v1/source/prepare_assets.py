from pathlib import Path
import os,sys,importlib.util,csv,json
os.environ['MPLCONFIGDIR']='/workspace/ppt-tools/cache/matplotlib'
sys.path.insert(0,'/workspace/ppt-tools/model-inspect')
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image
import rhino3dm as rh
B=Path('/workspace/ppt-extension/06_参数与植物生长情景模拟');OUT=Path(__file__).resolve().parents[1]/'assets'
sp=importlib.util.spec_from_file_location('sim',B/'复算/重算情景.py');sim=importlib.util.module_from_spec(sp);sp.loader.exec_module(sim)
cases=json.loads((B/'复算/input_data/cases.json').read_text());case={x['id']:x for x in cases}
meshes={c['id']:dict(np.load(B/'复算/input_data'/(c['id']+'.npz'))) for c in cases}
plt.rcParams.update({'savefig.transparent':True})
def render(name,cid='D_BASE',cover=None,view='axon',zoning=False):
 fig=plt.figure(figsize=(8,6));ax=fig.add_axes([0,0,1,1],projection='3d');mesh=meshes[cid]
 if zoning:
  m=rh.File3dm.Read(str(B/'模型/D_BASE.3dm'));counts=[0,0]
  for obj in m.Objects:
   if isinstance(obj.Geometry,rh.Curve):
    c=obj.Geometry;pts=np.array([[p.X,p.Y,p.Z]for p in [c.PointAt(t)for t in np.linspace(c.Domain.T0,c.Domain.T1,180)]])/1000
    steel=pts[:,2].min()<.1;counts[0 if steel else 1]+=1
    ax.plot(*pts.T,color='#3E6E9E'if steel else'#AA7E4A',linewidth=2.3)
  assert counts==[12,47],counts
 else:
  tris=mesh['vertices_m'][mesh['faces']]
  coll=Poly3DCollection(tris,facecolors='#557C65',edgecolors='#557C65',linewidths=0,alpha=1,shade=True,lightsource=matplotlib.colors.LightSource(azdeg=310,altdeg=50));ax.add_collection3d(coll)
 if cover:
  ll,_=sim.leaves(case[cid],cover);ax.add_collection3d(Poly3DCollection(ll,facecolors='#72A64C',edgecolors='none',alpha=.93))
 ax.set_xlim(-4,4);ax.set_ylim(-4,4);ax.set_zlim(0,4.4);ax.set_box_aspect((8,8,4.4));ax.set_axis_off()
 if view=='plan':ax.view_init(elev=90,azim=-90)
 elif view=='elevation':ax.view_init(elev=0,azim=-90)
 else:ax.view_init(elev=26,azim=-58)
 ax.set_proj_type('ortho');fig.savefig(OUT/name,dpi=160);plt.close(fig);print('RENDER',name,flush=True)
render('model-axon.png');render('model-plan.png',view='plan');render('model-elevation.png',view='elevation');render('material-zones.png',zoning=True)
for cid,name in [('W_SMALL','width-small.png'),('D_BASE','width-base.png'),('W_LARGE','width-large.png')]:render(name,cid)
for c in [0,.2,.5,.8,.95]:render(f'cover-{int(c*100):02d}.png',cover=c)
# Frame the scientific renders without changing their geometry. Comparison groups share one viewport.
def frame_group(names):
    ims=[Image.open(OUT/n).convert('RGBA') for n in names];bb=[im.getbbox() for im in ims]
    box=(max(0,min(q[0]for q in bb)-30),max(0,min(q[1]for q in bb)-30),min(ims[0].width,max(q[2]for q in bb)+30),min(ims[0].height,max(q[3]for q in bb)+30))
    for n,im in zip(names,ims):im.crop(box).save(OUT/n)
for n in ['model-axon.png','model-plan.png','model-elevation.png','material-zones.png']:frame_group([n])
frame_group(['width-small.png','width-base.png','width-large.png'])
frame_group([f'cover-{int(c*100):02d}.png'for c in [0,.2,.5,.8,.95]])
# GIF contains geometry only. Titles, legend, metrics and scenario text are editable slide objects.
frames=[]
for c in [0,.2,.5,.8,.95]:
 im=Image.open(OUT/f'cover-{int(c*100):02d}.png').convert('RGBA');bg=Image.new('RGBA',im.size,'#F8F7F2');bg.alpha_composite(im);frames.append(bg.convert('RGB'))
frames[0].save(OUT/'cover-sequence.gif',save_all=True,append_images=frames[1:],duration=1700,loop=1,disposal=2)
# Text-free ideal leaf projections: analytic polygons and fixed reference zone, same scale.
from matplotlib.patches import Polygon as PP,Circle,Rectangle
outer,inner=sim.boundary(case['D_BASE'])
for t in [9,12,15]:
 v=sim.solar(23.44,t);o=sim.project(outer,v);i=sim.project(inner,v)
 fig,ax=plt.subplots(figsize=(5.5,4));ax.set_position([.015,.015,.97,.97]);ax.fill(o[:,0],o[:,1],color='#8EB394',alpha=.55);ax.fill(i[:,0],i[:,1],color='#F8F7F2');ax.add_patch(Rectangle((-2.5,-2.5),5,5,fill=False,ec='#AA7E4A',lw=2));ax.add_patch(Circle((0,0),.75,fill=False,ec='#AA7E4A',lw=1.5));ax.plot(0,0,'o',color='#173C51',ms=4);ax.set(xlim=(-7,7),ylim=(-5,5),aspect='equal');ax.axis('off');fig.savefig(OUT/f'ideal-shadow-{t:02d}.png',dpi=180);plt.close(fig)
# Fixed 50% coverage, changing sun: native mask projection with distinct frame/leaf overlap.
g=sim.grid(.018,lo=(-7,-5),hi=(7,5));ll,_=sim.leaves(case['D_BASE'],.5);frames=[]
for t in np.arange(9,15.001,.25):
 bare,leaf=sim.masks(meshes['D_BASE'],ll,sim.solar(23.44,t),g)
 arr=np.zeros((*bare.shape,3),dtype=np.uint8);arr[:]=[248,247,242];arr[leaf]=[161,192,153];arr[bare]=[55,81,70]
 fig,ax=plt.subplots(figsize=(7,5));ax.set_position([.02,.02,.96,.96]);ax.imshow(arr,origin='lower',extent=(-7,7,-5,5),interpolation='nearest');ax.add_patch(Rectangle((-2.5,-2.5),5,5,fill=False,ec='#AA7E4A',lw=2));ax.add_patch(Circle((0,0),.75,fill=False,ec='#AA7E4A',lw=1.5));ax.set(xlim=(-7,7),ylim=(-5,5),aspect='equal');ax.axis('off');fig.savefig(OUT/'_frame.png',dpi=120,facecolor='#F8F7F2');plt.close(fig)
 im=Image.open(OUT/'_frame.png').convert('RGB');frames.append(im.copy())
 if t in [9,12,15]:im.save(OUT/f'combined-shadow-{int(t):02d}.png')
frames[0].save(OUT/'shadow-sequence.gif',save_all=True,append_images=frames[1:],duration=350,loop=1,disposal=2)
(OUT/'_frame.png').unlink()
# Data used for native PowerPoint charts.
with (B/'数据/02_参数与生长覆盖_汇总.csv').open(encoding='utf-8-sig') as f:summary=list(csv.DictReader(f))
find=lambda cid,stage:float(next(x for x in summary if x['case_id']==cid and x['season']=='Solstice' and x['stage']==stage)['time_mean_equivalent_direct_blocked_percent'])
data={'width_means':[find(c,'S2')for c in ['W_SMALL','D_BASE','W_LARGE']],'cover_means':[find('D_BASE',stage)for stage in ['S0','S1','S2','S3','S4']],'cost_labels':['Materials','Installation','Other','Fabrication','Maintenance','Planting','Transport'],'cost_values':[30549.3022975,6050,5679.6828674,5241.733545,2300,1165,690]}
(OUT/'chart-data.json').write_text(json.dumps(data,indent=2))
print('COMPLETE',flush=True)
