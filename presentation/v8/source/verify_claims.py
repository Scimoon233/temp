"""Check changed numeric claims against the provided workbook and supplement CSVs.
Original user attachments are required; they are not duplicated in this repository.
"""
from pathlib import Path
from openpyxl import load_workbook
import csv,json,hashlib,math
b=Path(__file__).resolve().parents[1];d=json.loads((b/'assets/chart-data.json').read_text())
root=Path('/workspace/ppt-extension/06_参数与植物生长情景模拟/数据')
workbook=next(Path('/workspace/attachments').rglob('Cost-Analysis.xlsx'))
w=load_workbook(workbook,data_only=True);s=w['挠度校核']
L=float(s['B31'].value)*1000;E=float(s['B11'].value)*1000;I=float(s['C22'].value);q=float(s['F31'].value)
assert math.isclose(5*q*L**4/(384*E*I),float(s['H31'].value),rel_tol=1e-8)
assert math.isclose(q*L**4/(384*E*I),float(s['H32'].value),rel_tol=1e-8)
target=L/float(s['B10'].value);assert target==33.25
assert math.isclose(float(s['H31'].value),100.533387276407,rel_tol=1e-8)
assert math.isclose(float(s['H32'].value),20.1066774552815,rel_tol=1e-8)
def rows(name):
 with (root/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
summary_name='02_参数与生长覆盖_汇总.csv';summary=rows(summary_name)
key='time_mean_equivalent_direct_blocked_percent'
parameter={r['case_id']:float(r[key]) for r in summary if r['season']=='Solstice' and float(r['cover'])==.5}
for k,v in d['parameter_means'].items():assert math.isclose(parameter[k],v,abs_tol=1e-7),(k,v,parameter[k])
covers={float(r['cover']):float(r[key]) for r in summary if r['season']=='Solstice' and r['case_id']=='D_BASE'}
for c,v in zip([0,.2,.5,.8,.95],d['cover_means']):assert math.isclose(covers[c],v,abs_tol=1e-7)
dist_name='05_相同50覆盖_分布敏感性.csv';dist=rows(dist_name);noon={r['pattern']:float(r['equivalent_direct_blocked_target_percent']) for r in dist if float(r['time_h'])==12.0}
assert all(math.isclose(a,b,abs_tol=1e-7) for a,b in zip(sorted(noon.values()),sorted(d['distribution_noon'])))
assert round(covers[.95]-covers[.8],1)==2.8
result={'source_files':{},'beam':{'L_mm':L,'E_N_per_mm2':E,'I_mm4':I,'q_N_per_mm':q,'simply_supported_mm':float(s['H31'].value),'ideal_fixed_mm':float(s['H32'].value),'adopted_target_mm':target,'ratios_to_target':[float(s['H31'].value)/target,float(s['H32'].value)/target]},'parameter_means':parameter,'baseline_cover_means':covers,'cover_80_to_95_gain_percentage_points':covers[.95]-covers[.8],'same_50_cover_noon':noon,'interpretation':'Arithmetic checks only; source inputs, plant/optical assumptions and ideal restraints remain assumptions.'}
for file in [workbook,root/summary_name,root/dist_name]:result['source_files'][file.name]=hashlib.sha256(file.read_bytes()).hexdigest()
(b/'Claim-Checks.json').write_text(json.dumps(result,indent=2))
print('Workbook beam results and ratios, seven parameter means, five cover means and same-cover noon values match supplied sources.')
