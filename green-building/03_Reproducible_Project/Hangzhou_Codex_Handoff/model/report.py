"""Generate derived parameter register, result narrative, additional figures and status."""
from run import *

def table(headers,rows):
 return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(str(x) for x in row)+' |' for row in rows)+'\n'

def main():
 r=pd.read_csv(OUT/'all_metrics.csv');base=r[r.variant=='base'];g=geometry();p=json.loads((ROOT/'config/base.json').read_text());checks=json.loads((OUT/'checks.json').read_text())
 C,Hm,He,H12,win,wall,uw,ui=setup(p,g)
 refs={'ach_closed':('h^-1','交接文献代理','Hou等2019 Table6，尚未独立取得全文核对'), 'ach_open':('h^-1','交接文献代理','Hou等2019 Table6，总ACH'), 'gain_peak_W_m2':('W/m2','文献峰值代理+假设时序','Short等2018正文得热段'), 'mass_kJ_m2K':('kJ/(m2 K)','研究假设','有效容量，不从原材料总质量直接推定')}
 units={'dt_seconds':'s','warmup_days':'day','initial_C':'degC','mass_coupling_W_m2K':'W/(m2 K)','deltaT_K':'K','cooling_setpoint_C':'degC','rotation_deg':'degree','interzone_mixing_ACH_small_zone':'h^-1','outside_h_W_m2K':'W/(m2 K)'}
 rows=[]
 for k,v in p.items():
  unit,kind,source=refs.get(k,(units.get(k,'dimensionless'),'研究假设','docs/METHODS_模型与假设.md'))
  rows.append(dict(parameter=k,value=v,units=unit,evidence_class=kind,source_or_explanation=source))
 for key,value,unit,kind,source in [('Uwall',uw,'W/(m2 K)','推导','补充材料Table S1导热率/厚度+假设表面热阻'),('Upartition_opaque',ui,'W/(m2 K)','推导','补充材料Table S1内墙+两侧热阻'),('Uwindow',6.7,'W/(m2 K)','交接文献代理','BASIX item5，本轮未独立核对原表'),('SHGC',.7,'dimensionless','交接文献代理','BASIX item5，整窗'),('H12',H12,'W/K','推导','隔断UA及背景区间混合'),('air_density',1.2,'kg/m3','研究假设','固定空气密度'),('air_cp',1006,'J/(kg K)','研究假设','固定空气比热')]:
  rows.append(dict(parameter=key,value=value,units=unit,evidence_class=kind,source_or_explanation=source))
 for i in range(2):
  for key,value,unit in [(f'Z{i+1}_floor_area',g['zone_areas_m2'][i],'m2'),(f'Z{i+1}_volume',g['zone_volumes_m3'][i],'m3'),(f'C_air{i+1}',C[2*i],'J/K'),(f'C_mass{i+1}',C[2*i+1],'J/K'),(f'Hmass{i+1}',Hm[i],'W/K'),(f'H_envelope{i+1}',He[i],'W/K')]:
   rows.append(dict(parameter=key,value=value,units=unit,evidence_class='图示面积假设或推导',source_or_explanation='geometry_v2及热网络公式'))
 pd.DataFrame(rows).to_csv(OUT/'parameter_register.csv',index=False,encoding='utf-8-sig')
 frows=[];irows=[];rankrows=[];budgets=[]
 for y in [2025,2026]:
  for s in ['S0','S1','S2','S3']:
   f=base[(base.year==y)&(base['mode']=='free')&(base.scenario==s)].iloc[0]
   a=base[(base.year==y)&(base['mode']=='ideal')&(base.scenario==s)].iloc[0]
   frows.append([y,s,f'{f.mean_C:.2f}',f'{f.peak_C:.2f}',f'{f.OH28_h:.1f}',f'{f.DH28_Kh:.1f}',f'{f.DH28_Kh_reduction_pct:.2f}%'])
   irows.append([y,s,f'{a.cool_kWh_th:.1f}',f'{a.cool_kWh_th_m2:.2f}',f'{a.cool_kWh_th_reduction_pct:.2f}%',f'{a.vent1_hours:.1f}',f'{a.vent2_hours:.1f}'])
   h=pd.read_csv(OUT/f'hourly/{y}_free_{s}.csv')
   budgets.append(dict(year=y,scenario=s,solar_assigned_Z1_kWh=h.solar_Z1_W.sum()/1000,solar_retained_Z2_kWh=h.solar_Z2_W.sum()/1000,internal_Z1_kWh=h.internal_W.sum()/1000))
  for mode,metric in [('free','DH28_Kh'),('ideal','cool_kWh_th')]:
   a=r[(r.year==y)&(r['mode']==mode)];pv=a.pivot(index='variant',columns='scenario',values=metric)
   for v,row in pv.iterrows():rankrows.append(dict(year=y,mode=mode,variant=v,best=row.idxmin(),ranking='<'.join(row.sort_values().index)))
 pd.DataFrame(rankrows).to_csv(OUT/'rankings.csv',index=False);pd.DataFrame(budgets).to_csv(OUT/'solar_internal_budgets.csv',index=False)
 inter=pd.read_csv(OUT/'interactions.csv');inter=inter[(inter.variant=='base')&(((inter['mode']=='free')&(inter.metric=='DH28_Kh'))|((inter['mode']=='ideal')&(inter.metric=='cool_kWh_th')))]
 text='# 首版模型与分析结果（非论文定稿）\n\n实际完成：两年×四情景×两评价工况=16组基准运行；加19个OAT变体后共320组季节运行。无现场监测或实测校准。所有数值来自本包Python实际运行。\n\n'
 text+='## 自由运行：Z1空气温度与过热\n\n'+table(['年','方案','平均°C','子步峰值°C','OH28 h','DH28 K·h','DH28降低'],frows)
 text+='\n阈值28°C为研究阈值，评价期每年2208小时。S3平均降温2025为2.12°C、2026为1.85°C，峰值分别降低3.53°C、2.20°C；但S3仍有2172.0/2179.8小时超过28°C。这些措施不足以在本组假设下消除过热。DH26/DH30在base_metrics.csv，不能从空气温度直接推断完整热舒适。\n\n'
 text+='## 理想显热制冷：仅Z1，26°C全天上限\n\n'+table(['年','方案','kWh_th','kWh_th/m²','相对S0降低','Z1开窗h','Z2开窗h'],irows)
 text+='\nS3相对S0少移除263.2/213.2 kWh_th。S2仅降低0.58%/0.82%，不能用自由运行的过热改善百分比替代制冷需求降低率。Z1在26°C附近运行，1K开启门槛要求室外约≤25°C，因而夜间可开窗机会比自由运行明显减少；Z2未制冷，仍可在更多夜间开启。表中显热需求不含潜热、设备效率、风机及辅助电耗，不等于电耗。\n\n'
 text+='## 组合交互\n\n'+table(['年','工况','指标','I（原指标单位）'],[[a.year,a['mode'],a.metric,f'{a.interaction:.3f}'] for _,a in inter.iterrows()])
 text+='\n四个交互量均为负，组合收益小于两项收益之和。仅因为S3最低，不能称其有超相加协同效应。制冷交互不足1 kWh_th，宜解释为近似相加、略有收益递减，不赋予统计显著性。\n\n'
 text+='## 敏感性与排序\n\n'
 sr=[]
 for y in [2025,2026]:
  for mode,metric in [('free','DH28_Kh'),('ideal','cool_kWh_th')]:
   a=r[(r.year==y)&(r['mode']==mode)&(r.scenario=='S3')]
   sr.append([y,mode,f'{a[metric+"_reduction_pct"].min():.2f}—{a[metric+"_reduction_pct"].max():.2f}%'])
 text+=table(['年','工况','20套输入下S3相对各自S0改善范围'],sr)
 text+='\n两年全部20套输入中S3均最低。自由运行基准为S3<S2<S1<S0；开窗ACH=0.8或直射削减100%时改为S3<S1<S2<S0，说明单项排序有条件性。理想制冷两年20套输入均为S3<S1<S2<S0。范围是有限OAT情景包络，不是概率区间，不能外推为所有住宅的稳健排名。\n\n'
 text+='## 高温结果的解释与剩余限制\n\n自由运行出现45—50°C以上峰值是本模型真实输出，不能直接视为挂牌房实际室温。模型采用西/南等方向较大阳台玻璃、无邻楼/顶板遮挡、关闭低换气阳台、全天非零内部得热、固定整窗SHGC、简化围护动态与长波处理。即使内部得热减半，S0峰值仍为48.40/46.13°C，说明不能仅将高温归因于内部得热；阳台温升、二次透入与几何遮挡的不确定性同样重要。solar_internal_budgets.csv保留各区太阳分配及内部热量，后续精细模型应优先检查这些路径，而不是将数值守恒当作预测准确。当前不得将绝对室温或负荷用于真实住宅设备选型。\n\n'
 text+='模型已说明关键限制：太阳得热25%二次透入为假设；外墙无分层瞬态及天空长波；固定ACH不响应风速/开窗几何；两热区充分混合；上下邻接边界绝热；两年网格天气；不计算湿度、潜热、操作温度或住户真实开窗行为。外部BASIX/Hou参数仍属交接代理，后续论文引用须核对原表。\n\n'
 text+='## 核验与复现\n\n'
 mx=max(x['step_relative_change'] for x in checks['refinement_and_warmup'])
 text+=f'checks.json状态{checks["status"]}。2025四情景两工况300→150秒关键累计指标最大相对变化{mx*100:.5f}%；等温无得热最大偏差{checks["isothermal_no_gain_max_error_K"]:.2e} K；稳态理想制冷与独立静态热平衡偏差{checks["steady_ideal_error_W"]:.2e} W。所有320组季节运行最大节点残差{r.max_node_residual_W.max():.2e} W。残差属于离散方程数值核验，不是模型实测误差。\n\n'
 text+='按README_RUN.md顺序执行。数据边界保留全部2208个前一小时辐射区间，相对严格日历夏季整体提前一小时；首小时缺少前温度端点，以首值补齐。详见方法说明。\n'
 (ROOT/'docs/RESULTS_结果摘要.md').write_text(text,encoding='utf-8')
 dump(ROOT/'MODEL_STATUS.json',dict(status='first_version_simulated_and_numerically_checked',base_season_runs=16,total_season_runs=len(r),years=[2025,2026],calibrated=False,parameter_variants=20,checks='results/checks.json',remaining=['外部参数文献全文核对','复杂几何遮挡/多参数不确定性可扩展','论文定稿未生成']))
 fig,axes=plt.subplots(2,1,figsize=(12,6),sharey=True)
 for ax,y in zip(axes,[2025,2026]):
  d=weather(y);ax.plot(d.time,d.temperature_2m,lw=.6);ax.axhline(26,c='grey',ls='--',lw=.8);ax.set_title(str(y));ax.set_ylabel('Outdoor C')
 fig.tight_layout();fig.savefig(OUT/'figures/weather.png',dpi=180);plt.close(fig)
 # Export radiation components used by the default orientation, for independent review.
 for y in [2025,2026]:
  d=weather(y);beam,diff,refl,up=irradiance(d,p['rotation_deg'])
  radiation=pd.DataFrame({'interval_end_local':d.time,'solar_elevation_sin_midpoint':up})
  for i,o in enumerate(['N','E','S','W']):
   radiation[f'{o}_beam_W_m2']=beam[:,i];radiation[f'{o}_diffuse_W_m2']=diff[:,i];radiation[f'{o}_ground_W_m2']=refl[:,i]
  radiation.to_csv(OUT/f'facade_radiation_{y}.csv',index=False,float_format='%.6f')
 # Self-contained HTML viewer for convenient offline review, no external dependencies.
 import base64,html
 imgs=''.join(f'<h2>{name}</h2><img style="max-width:100%" src="data:image/png;base64,{base64.b64encode((OUT/"figures"/name).read_bytes()).decode()}">' for name in ['geometry.png','weather.png','scenario_comparison.png','week_2025.png','week_2026.png','sensitivity.png'])
 (OUT/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>杭州住宅模拟结果</title><body style="max-width:1200px;margin:auto;font-family:sans-serif"><h1>杭州住宅原型模拟结果</h1><p>无实测校准；显热需求不是电耗。详细解释见docs/RESULTS_结果摘要.md。</p>'+base.drop(columns=['variant']).round(3).to_html(index=False)+imgs+'</body>',encoding='utf-8')
 print('Report and parameter register generated',len(r),'runs')
if __name__=='__main__':main()
