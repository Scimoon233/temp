"""Extract paper additions from existing seasonal results; no new simulation."""
from pathlib import Path
import hashlib,json
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'course_essay'

def main():
    base=pd.read_csv(ROOT/'results/base_metrics.csv')
    all_results=pd.read_csv(ROOT/'results/all_metrics.csv')
    diagnostic=pd.read_csv(ROOT/'results/draft_diagnostics/metrics.csv')
    cases=json.loads((ROOT/'results/draft_diagnostics/cases.json').read_text())
    evidence={'new_model_runs':0,'baseline':{},'sensitivity':{},'boundary_check':{},'interaction':{}}
    for year in [2025,2026]:
        f=base[(base.year==year)&(base['mode']=='free')].set_index('scenario')
        a=base[(base.year==year)&(base['mode']=='ideal')].set_index('scenario')
        evidence['baseline'][str(year)]={
            'S0_mean_C':float(f.loc['S0','mean_C']),
            'S3_mean_C':float(f.loc['S3','mean_C']),
            'mean_reduction_C':float(f.loc['S0','mean_C']-f.loc['S3','mean_C']),
            'S3_DH28_reduction_pct':float(f.loc['S3','DH28_Kh_reduction_pct']),
            'S3_cooling_reduction_pct':float(a.loc['S3','cool_kWh_th_reduction_pct'])}
        for frame,key in [(f,'DH28_Kh'),(a,'cool_kWh_th')]:
            values=frame[key]
            evidence['interaction'].setdefault(str(year),{})[key]=float((values['S0']-values['S3'])-(values['S0']-values['S1'])-(values['S0']-values['S2']))
        d=diagnostic[(diagnostic.year==year)&(diagnostic['mode']=='free')&(diagnostic.scenario=='S0')&(diagnostic.variant=='combined_lower_gain')].iloc[0]
        evidence['boundary_check'][str(year)]={'variant':'combined_lower_gain','scenario':'S0','mode':'free','mean_C':float(d.mean_C),'peak_C':float(d.peak_C)}
    assert all_results.variant.nunique()==20
    evidence['input_sets']=int(all_results.variant.nunique())
    for mode,key in [('free','DH28_Kh'),('ideal','cool_kWh_th')]:
        x=all_results[all_results['mode']==mode]
        groups=list(x.groupby(['variant','year']))
        assert all(g.set_index('scenario').loc['S3',key]==g[key].min() for _,g in groups)
        s=x[x.scenario=='S3'];column=key+'_reduction_pct'
        endpoints=[]
        for index in [s[column].idxmin(),s[column].idxmax()]:
            row=s.loc[index];endpoints.append({'variant':row.variant,'year':int(row.year),'reduction_pct':float(row[column])})
        evidence['sensitivity'][mode]={'metric':key,'S3_minimum_groups':len(groups),'group_count':len(groups),'min_pct':float(s[column].min()),'max_pct':float(s[column].max()),'endpoints':endpoints,'comparison':'Each variant uses its own same-year S0. Ranges are extrema over the tested settings.'}
    evidence['boundary_check_settings']=cases['combined_lower_gain']
    evidence['source_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['results/base_metrics.csv','results/all_metrics.csv','results/draft_diagnostics/metrics.csv','results/draft_diagnostics/cases.json']}
    OUT.mkdir(exist_ok=True)
    (OUT/'EVIDENCE_ADDITIONS_v1.6.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
    rows=[]
    variants=json.loads((ROOT/'results/variants.json').read_text())
    for name,settings in variants.items():rows.append('|'+name+'|'+('; '.join(f'{k}={v}' for k,v in settings.items()) or 'Baseline settings')+'|')
    interaction='\n'.join(f"|{y}|{v['DH28_Kh']:.4f}|{v['cool_kWh_th']:.4f}|" for y,v in evidence['interaction'].items())
    note='''# Supporting methods and evidence for the course essay v1.6

This file accompanies the three-page English paper. It preserves numerical details shortened in the main text and identifies the source of the added evidence. It is separate from the course-submission PDF. No thermal simulations were added for this revision.

## Weather alignment and initialization

Each summer contains 2,208 hourly ERA5 records obtained through Open-Meteo, with no missing values. Radiation values represent the preceding hour. Solar position is evaluated at its midpoint and outdoor temperature at the mean of adjacent endpoints. Preserving source records gives integration intervals from 31 May 23:00 to 31 August 23:00, UTC+8. The first outdoor-temperature value is held constant for the missing initial endpoint. Thus the source-preserving sequence is shifted by one hour relative to a midnight-to-midnight June–August calendar window.

Facade calculations include direct, isotropic diffuse and ground-reflected radiation. The baseline assigns 25% of admitted balcony solar gains to the living zone; the remainder stays in the balcony. Allocation conserves admitted solar energy. Partition conduction and small interzone air exchange are separate paths and are retained when secondary solar allocation changes.

The four-node RC model is integrated by backward Euler with 300 s steps. Warm-up repeats the first weather week over 28 days. Initial temperatures, warm-up sensitivity and nodal energy balances were checked. Halving the step in the 2025 baseline changed key cumulative metrics by less than 0.006%. The original checks are in `results/checks.json`, `results/numerical_checks.csv` and `results/draft_diagnostics/checks.json`.

## Added absolute temperatures and sensitivity ranges

The absolute means come from `results/base_metrics.csv`: 2025 S0/S3 = 40.04394/37.92318°C; 2026 S0/S3 = 38.36292/36.51186°C. They are seasonal living-zone air temperatures in free-running operation.

The twenty input sets comprise the baseline, eighteen single-parameter variants and one exposed-east-boundary variant. For every input set, year and operating mode, benefits are calculated relative to that input set's own S0. Across both summers, combined DH28 reductions are 10.86044–28.06232%, and ideal sensible-demand reductions 3.63017–13.43140%. S3 gives the minimum DH28 and cooling demand in all forty comparisons per metric. The ranges are extrema of discrete tested settings, not probability distributions or statistical confidence intervals. Individual-measure rankings can change with the input set.

The DH28 extrema occur at open-window rates of 0.8 and 3.0 air changes per hour. The cooling-demand extrema occur at 25% and 100% removal of window direct solar radiation. These endpoint associations show which tested settings span each reported range; they are not a global sensitivity index.

|Input set|Changed settings|
|---|---|
'''+ '\n'.join(rows)+'''

## Boundary check for high baseline temperatures

`combined_lower_gain` jointly applies a 1 m ideal balcony overhang, half internal gains and zero secondary balcony-to-living solar allocation. With S0 operation in this altered boundary case, the 2025 mean is 36.17978°C and peak 44.07820°C; the 2026 mean is 34.78506°C and peak 43.33767°C. Values are from `results/draft_diagnostics/metrics.csv`; exact settings are in `results/draft_diagnostics/cases.json` and `model/draft_analysis.py`.

This is a boundary-condition diagnostic, distinct from S3 shading-plus-ventilation operation. Three inputs change together, so the temperature difference does not identify an individual causal contribution. The case demonstrates the dependence of absolute predictions on solar and internal heat inputs; it is not field calibration or a replacement baseline chosen to lower the reported temperatures.

## Interaction calculation retained outside the short paper

For a demand metric D, I = (D0 − D3) − (D0 − D1) − (D0 − D2). A negative value means that the combined reduction is slightly smaller than the sum of individual reductions. The short paper retains the interpretation: approximately additive cooling benefits with slight diminishing returns.

|Year|I for DH28 (K h)|I for ideal cooling (kWh<sub>th</sub>)|
|---|---:|---:|
'''+interaction+'''

## 中文核对说明

本轮主稿补充了两年基准与组合的绝对平均室温、20套输入下的降幅范围，以及单项排序的基准参数条件；引言明确了在统一住宅和天气框架内比较两种运行条件的贡献。高温边界对照属于已有诊断结果，其S0均温36.18°C不应与S3混为一谈，也不构成实测校准。

完整英文数值证据见同目录`EVIDENCE_ADDITIONS_v1.6.json`。从项目根目录运行`python model/extract_course_evidence.py`可重新提取，不会运行或改写热模型结果。原模型复现命令见项目`README_RUN.md`。
'''
    (OUT/'方法补充与证据来源_v1.6.md').write_text(note)
    print(json.dumps({'new_model_runs':0,'inputs':20,'groups_per_metric':40,'evidence_written':True},ensure_ascii=False))

if __name__=='__main__':main()
