from pathlib import Path
import json, shutil, zipfile
p=Path('/workspace/scratch/648fe18f6f13/geometry_boundary_v1')
src='https://www.hzxqf.com/house/120716888258.html'
rooms=[('R1','卧室 A',11.1,3.897,2.846),('R2','卧室 B',9.5,3.897,2.429),('R3','客厅及图示厅区',14.8,3.728,3.961),('R4','厨房',2.6,1.228,2.216),('R5','卫生间',3.1,2.380,None),('R6','阳台',6.3,3.897,1.625)]
# Lengths are local plan dimension references, not globally reconciled CAD geometry.
walls=[
('E01','卧室B北侧','R2','N',3.897,'外气','图示无窗'),
('E02','卧室B西侧','R2','W',2.429,'外气','W01'),
('E03','卧室A西侧','R1','W',2.846,'外气','图示无窗'),
('E04','阳台西侧','R6','W',1.625,'外气','W04'),
('E05','阳台南侧','R6','S',3.897,'外气','W05'),
('E06','阳台东侧','R6','E',1.625,'外气','W06'),
('E07','客厅南侧','R3','S',3.728,'外气','W03'),
('E08','客厅东侧含入户门','R3','E',3.961,'绝热简化','D01；相邻走廊仅为假设'),
('E09','厨房东侧','R4','E',2.216,'绝热简化','相邻户仅为假设'),
('E10','厨房北侧','R4','N',1.228,'外气','图示无窗'),
('E11','厨房西侧突出短墙','R4','W',None,'外气','存在短墙；长度不使用不闭合尺寸链推算'),
('E12','卫生间北侧','R5','N',2.380,'外气','W02')]
windows=[
('W01','E02','卧室B西窗',0.75,1.5,'窗线存在可见；宽、高均为建模假设',0.6,0.9),
('W02','E12','卫生间北窗',0.85,1.5,'窗线存在可见；宽、高均为建模假设',0.7,1.0),
('W03','E07','客厅南窗',0.75,1.5,'窗线存在可见；宽、高均为建模假设',0.6,0.9),
('W04','E04','阳台西侧围护',1.5,2.1,'图示玻璃线；整窗宽、高为假设',1.4,1.6),
('W05','E05','阳台南侧围护',3.7,2.1,'图示玻璃线；整窗宽、高为假设',3.6,3.8),
('W06','E06','阳台东侧围护',1.5,2.1,'图示玻璃线；整窗宽、高为假设',1.4,1.6)]
win_by={w[1]:w for w in windows}
def tab(head,rows):
 return '| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+''.join('| '+' | '.join(str(v) if v is not None else '待定' for v in row)+' |\n' for row in rows)
model={
 'version':'geometry_boundary_v1','source_url':src,'source_image':'selected_7105_floorplan.jpg',
 'status':'conditional_prototype_geometry_not_survey_or_closed_polygon',
 'source_gross_area_m2':71.05,'clear_height_assumption_m':2.7,
 'zones':[{'id':'Z1','name':'居住区','room_ids':['R1','R2','R3','R4','R5'],'area_assumption_m2':41.1,'volume_assumption_m3':110.97}, {'id':'Z2','name':'封闭阳台缓冲区','room_ids':['R6'],'area_assumption_m2':6.3,'volume_assumption_m3':17.01}],
 'room_inputs':[{'id':r[0],'name':r[1],'plan_label_area_m2':r[2],'plan_local_width_m':r[3],'plan_local_depth_m':r[4]} for r in rooms],
 'surfaces':[],'openings':[],
 'internal_interfaces':[
 {'id':'I01','rooms':['R1','R2'],'plan_local_length_m':3.897,'treatment':'same_air_node_no_interzone_flux'},
 {'id':'I02','rooms':['R1','R3'],'plan_local_length_m':2.846,'treatment':'same_air_node_no_interzone_flux'},
 {'id':'I03','rooms':['R2','R3'],'length_m':None,'treatment':'same_air_node_no_interzone_flux'},
 {'id':'I04','rooms':['R5','R3'],'plan_local_length_m':2.380,'treatment':'same_air_node_no_interzone_flux'},
 {'id':'I05','rooms':['R5','R4'],'length_m':None,'treatment':'same_air_node_no_interzone_flux'},
 {'id':'I06','rooms':['R4','R3'],'plan_local_length_m':1.228,'treatment':'open_passage_same_air_node'},
 {'id':'I07','rooms':['R1','R6'],'plan_local_length_m':3.897,'treatment':'interzone_heat_transfer','aperture_width_assumption_m':2.4,'aperture_height_assumption_m':2.1,'aperture_area_assumption_m2':5.04}],
 'orientation':{'convention':'clockwise_from_north','rotation_assumption_deg':0,'N':0,'E':90,'S':180,'W':270,'not_surveyed':True},
 'horizontal_boundaries':'mid_floor_adiabatic_assumption',
 'unknowns':['E11 length','globally reconciled closed polygon','actual adjacent spaces','measured window dimensions','actual floor level','true facade azimuth'],
 'model_ready':False}
for w in windows:
 model['openings'].append(dict(id=w[0],surface_id=w[1],name=w[2],whole_window_width_assumption_m=w[3],whole_window_height_assumption_m=w[4],whole_window_area_assumption_m2=round(w[3]*w[4],4),width_sensitivity_m=[w[6],w[7]],height_sensitivity_m=([1.2,1.8] if w[0] in ['W01','W02','W03'] else [1.8,2.4]),evidence=w[5],geometric_openable_area_m2=None,effective_ventilation_area_m2=None))
for s in walls:
 ga=None if s[4] is None else round(s[4]*2.7,4)
 wa=round(win_by[s[0]][3]*win_by[s[0]][4],4) if s[0] in win_by else 0
 model['surfaces'].append(dict(id=s[0],name=s[1],room_id=s[2],drawing_direction=s[3],plan_local_length_m=s[4],baseline_boundary_assumption=s[5],gross_area_from_assumed_height_m2=ga,window_area_assumption_m2=wa,opaque_area_conditional_m2=None if ga is None else round(ga-wa,4),notes=s[6]))
text='# 杭州住宅几何边界表 v1\n\n日期：2026-11-06。用途：绿色建筑课程论文的遮阳与夜间通风模拟。\n\n'
text+='**已完成房间、外围墙段、门窗、内部连接和水平边界的编号与分类。它是公开户型图对应的条件化建模表，不是实测建筑图，也不是已经闭合的 CAD 几何。所有外气／邻户判断和窗尺寸假设均保留来源状态。尚未运行模拟。**\n\n'
text+=f'来源：[71.05 m² 挂牌户型]({src})。原图见本包 `selected_7105_floorplan.jpg`，保持原始图像。图面上为北、下为南、左为西、右为东；这是依示意北箭头确定的方向。基准取整体旋转角 0°，真实方位未测定，不能沿用论文原户的方位。\n\n'
text+='## 1. 面积与分区\n\n71.05 m² 是挂牌建筑面积，不能据此计算空气体积。本版本明确采用图中房间标注面积作为**原型净面积假设**，并把层高统一设为 2.7 m；这些体积是条件值。阳台按封闭缓冲区独立建模。\n\n'
text+=tab(['房间','图示空间','图示面积 m²','局部宽度 m','局部进深 m','假设体积 m³'],[(r[0],r[1],r[2],r[3],r[4],round(r[2]*2.7,2)) for r in rooms])
text+='\n居住区 Z1：R1—R5，41.1 m²，110.97 m³。阳台 Z2：R6，6.3 m²，17.01 m³。合计 47.4 m²，127.98 m³。Z1 内视为空气充分混合，不能报告逐卧室独立温度。\n\n'
text+='**尺寸核对：** 卧室A、B、阳台及客厅的局部宽×深与标注面积大体吻合。例如卧室A为 3.897×2.846=11.091 m²。厨房为 1.228×2.216=2.721 m²，与标签2.6 m²不同。因此面积与局部尺寸分别保存，不能强制解释为同一套精确净尺寸。顶部尺寸链 3.897+2.380+1.228=7.505 m，底部 3.897+3.728=7.625 m，相差0.120 m，可能涉及墙厚或标注口径，尚无依据裁定。左侧另有1742标注，起止点不清，本版本不使用。\n\n'
text+='## 2. 外围墙段及边界\n\n“外气”是本版本的基准暴露假设；图中有窗线不等于证明所有相邻墙段都面向室外。E08按相邻走廊、E09按相邻户简化为绝热，均不代表实际邻接关系。下列墙长为局部投影尺寸，墙高统一假设2.7 m；面积并非实际测量。\n\n'
text+=tab(['编号','墙段','方向','局部长 m','基准边界假设','关联门窗'],[(s[0],s[1],s[3],s[4],s[5],s[6]) for s in walls])
text+='\nE11 是厨房向北突出形成的西向短墙。其存在可从轮廓识别，长度留空；不得用存在口径矛盾的垂直尺寸链差额当作确定长度。E01—E12完整列出可辨认的外围拓扑段，但整体墙线尚未组成统一坐标下的闭合多边形。卧室A南侧与阳台之间另记为 I07，不能再计作直接对外墙。\n\n'
text+='## 3. 门窗与开口\n\n图中没有窗尺寸表。以下宽度按图示比例选为粗略原型值，高度由研究者设定；区间是研究用敏感性范围，**不是测量误差或统计置信区间**。面积按包含窗框的整窗洞口统一计算，以便后续与整窗U值、SHGC口径一致。阳台侧面采用整窗高度2.1 m，余下墙高作不透明围护。\n\n'
text+=tab(['编号','所在墙段','名称','假设宽 m','假设高 m','整窗面积 m²','宽度敏感性 m'],[(w[0],w[1],w[2],w[3],w[4],round(w[3]*w[4],3),f'{w[6]}—{w[7]}') for w in windows])
text+='\nW01—W03高度敏感性取1.2—1.8 m；W04—W06取1.8—2.4 m。居住区直接对外整窗总面积3.525 m²，阳台对外整窗总面积14.070 m²，两者属于不同热区，太阳得热不可直接合并到Z1。窗框比例、可开启比例及有效通风面积均未知。基于ACH的初版模型无需把几何开口面积转换成风量；如果以后改用风压通风模型，必须另补开窗方式与流量系数。\n\n'
text+=tab(['编号','连接关系','图面识别','初版处理'],[
('D01','R3—入户外侧','东侧入户门可见','基准关闭；随E08绝热，不计直接外气通风'),
('D02','R2—R3','卧室B内门可见','Z1内部，不另算区域间传热'),
('D03','R1—R3','卧室A内门可见','Z1内部，不另算区域间传热'),
('D04','R5—R3','卫生间下侧开口可见，门型未定','Z1内部'),
('O01','R4—R3','厨房下侧与客厅连通','Z1内部开放通道'),
('O02','R1—R6','卧室A与阳台间宽开口，门扇未明确','假设存在可关闭隔断，洞口2.4×2.1=5.04 m²；不是图中已确认玻璃门')])
text+='\nO02为关键假设：若没有可关闭隔断，Z1与Z2应合并，不可仍按两个独立空气区计算。基准关闭时，5.04 m²开口的构造及传热系数尚需定义；余下面积 3.897×2.7−5.04=5.4819 m²作实体墙参考。打开时应定义区间空气交换，不能自动套用室外ACH。\n\n'
text+='## 4. 内部连接与水平边界\n\n'
text+=tab(['界面','相邻空间','图示/局部长度 m','Z1充分混合时处理'],[
('I01','R1—R2',3.897,'内部热容量可保留，区域间净传热不单列'),
('I02','R1—R3',2.846,'同上；局部尺寸仅供构造规模参考'),
('I03','R2—R3',None,'门墙组合；长度不猜测'),
('I04','R5—R3',2.380,'含开口，内部'),
('I05','R5—R4',None,'内部；长度待定'),
('I06','R4—R3',1.228,'开放连接，不虚设完整实墙'),
('I07','R1—R6',3.897,'Z1—Z2边界；传导、透光和开口交换单独处理')])
text+='\n'
text+=tab(['水平表面','条件面积 m²','基准假设','限制'],[
('Z1地板',41.1,'中间楼层，绝热','不适用于底层直接接地'),
('Z1顶板',41.1,'中间楼层，绝热','不适用于顶层屋面'),
('Z2地板',6.3,'邻接同温空间，绝热','悬挑底板实际暴露情况未知'),
('Z2顶板',6.3,'邻接同温空间，绝热','阳台顶板实际构造未知')])
text+='\n绝热仅指边界净热通量取零，不意味着构件没有蓄热容量。窗、实体墙和门洞面积应分别计入，避免重复。\n\n'
text+='## 5. 条件面积表与建模交接\n\n以下是上述局部长、层高和窗假设生成的面积，用于核对参数表。E11未解决，因此**不输出完整外墙总面积或窗墙比**。E08门所在边界整体采用绝热简化，无需假装已有门洞尺寸。\n\n'
text+=tab(['墙段','条件毛面积 m²','假设整窗面积 m²','条件不透明面积 m²'],[(s['id'],s['gross_area_from_assumed_height_m2'],s['window_area_assumption_m2'],s['opaque_area_conditional_m2']) for s in model['surfaces']])
text+='\n**这一轮已完成：** 6个房间、2个热区、12个外围墙段、6处对外窗/玻璃围护、6处门或连通口、7个内部界面和4个水平表面的边界登记。JSON与本表保持同一口径。\n\n'
text+='**启动计算前仍需处理：**\n\n1. E11长度及统一坐标轮廓：回到图纸逐段描线，解释0.120 m尺寸差；若无法解决，可明确采用重建原型几何，但不能将其称为原图精确还原。\n2. O02隔断：选择可关闭门窗构造及参数，或改为合并阳台的单区模型。\n3. 确认基准暴露假设的研究用途，并将E08、E09改为外气边界进行敏感性比较；不能声称它们实际邻接走廊或邻户。\n4. 等效热容量、内表面耦合、太阳辐射换算、开窗控制与散热时段属于后续热模型输入，本表未代为完成。\n\n'
text+='**论文方法写法：** 本研究以公开住宅户型图构建几何原型。房间面积与局部尺寸采用图示信息，未提供的窗尺寸、相邻空间与楼层条件以显式情景假设表示。阳台独立为缓冲热区，居住空间简化为充分混合空气区。模拟结果用于比较既定边界条件下的遮阳与通风效果，不代表该挂牌住宅的实测性能。\n'
(p/'Geometry_Boundary_Table.md').write_text(text,encoding='utf-8')
(p/'geometry_boundary_v1.json').write_text(json.dumps(model,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy('/workspace/scratch/648fe18f6f13/master_data/01_geometry/selected_7105_floorplan.jpg',p/'selected_7105_floorplan.jpg')
assert abs(sum(r[2] for r in rooms)-47.4)<1e-9
assert len(model['surfaces'])==12 and len(model['openings'])==6
assert all(s['opaque_area_conditional_m2'] is None or s['opaque_area_conditional_m2']>=0 for s in model['surfaces'])
assert abs(sum(w['whole_window_area_assumption_m2'] for w in model['openings'][:3])-3.525)<1e-9
out=p.parent/'Hangzhou_Geometry_Boundary_v1.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n in ['Geometry_Boundary_Table.md','geometry_boundary_v1.json','selected_7105_floorplan.jpg']:
  z.write(p/n,n)
 assert z.testzip() is None
print(json.dumps({'output':str(out),'rooms':6,'zones':2,'perimeter_surfaces':12,'external_openings':6,'checks':'passed','global_polygon_closed':False},ensure_ascii=False))
