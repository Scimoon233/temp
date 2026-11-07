"""Parse NOAA ISD mandatory fields; preserve source groups and QC flags.
Run from this directory: python process_weather.py
No interpolation, gap filling, or station mixing is performed.
"""
from pathlib import Path
import csv, gzip, json, math
from datetime import datetime, timedelta, timezone
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent
SOURCE = 'https://www.ncei.noaa.gov/pub/data/noaa/2022/584570-99999-2022.gz'

def value(s, missing, scale=1):
    return '' if s == missing else int(s) / scale

rows = []
for i, s in enumerate(gzip.decompress((ROOT/'noaa_2022.gz').read_bytes()).decode().splitlines(), 1):
    t = datetime.strptime(s[15:27], '%Y%m%d%H%M').replace(tzinfo=timezone.utc)
    r = dict(source_line=i, station_id=s[4:15], utc=t.isoformat(),
             beijing_time=(t+timedelta(hours=8)).strftime('%Y-%m-%d %H:%M'),
             latitude=value(s[28:34], '+99999',1000), longitude=value(s[34:41],'+999999',1000),
             elevation_m=value(s[46:51],'+9999'),report_type=s[41:46],
             temperature_C=value(s[87:92],'+9999',10),temperature_qc=s[92],
             dewpoint_C=value(s[93:98],'+9999',10),dewpoint_qc=s[98],
             wind_direction_deg=value(s[60:63],'999'),wind_direction_qc=s[63],
             wind_type=s[64],wind_speed_m_s=value(s[65:69],'9999',10),wind_speed_qc=s[69])
    r['location_group'] = 'city_synoptic' if r['report_type']=='FM-12' and 120.15 <= r['longitude'] <= 120.18 else 'xiaoshan_airport'
    r['temperature_pass_all_qc'] = int(r['temperature_C']!='' and r['temperature_qc'] in ('1','5'))
    r['rh_percent_derived'] = ''
    if r['temperature_pass_all_qc'] and r['dewpoint_C']!='' and r['dewpoint_qc'] in ('1','5'):
        T, Td = r['temperature_C'], r['dewpoint_C']
        r['rh_percent_derived'] = round(100*math.exp(17.625*Td/(243.04+Td)-17.625*T/(243.04+T)),2)
    rows.append(r)

def write(name, data):
    with (ROOT/name).open('w', newline='', encoding='utf-8-sig') as f:
        w=csv.DictWriter(f, fieldnames=list(data[0]));w.writeheader();w.writerows(data)

write('noaa_2022_observations_all_groups.csv',rows)
summer=[r for r in rows if '2022-07-01' <= r['beijing_time'][:10] <= '2022-08-31']
city=[r for r in summer if r['location_group']=='city_synoptic']
airport=[r for r in summer if r['location_group']=='xiaoshan_airport']
write('hangzhou_city_2022_JulAug_observations.csv',city)
write('xiaoshan_airport_2022_JulAug_observations.csv',airport)
daily=[]
for date in sorted(set(r['beijing_time'][:10] for r in city)):
    rs=[r for r in city if r['beijing_time'].startswith(date)]
    valid=[r['temperature_C'] for r in rs if r['temperature_pass_all_qc']]
    daily.append(dict(date_beijing=date,n_observations=len(rs),n_temperature_pass_qc=len(valid),
                      minimum_sampled_C=min(valid) if valid else '',maximum_sampled_C=max(valid) if valid else ''))
write('hangzhou_city_sampled_daily_extrema.csv',daily)
unique=sorted({r['utc'] for r in city if r['temperature_pass_all_qc']})
gaps=Counter((datetime.fromisoformat(b)-datetime.fromisoformat(a)).total_seconds()/3600 for a,b in zip(unique,unique[1:]))
qa=dict(source=SOURCE,year_records=len(rows),location_groups=dict(Counter(r['location_group'] for r in rows)),
        summer_records=len(summer),summer_city_records=len(city),summer_airport_records=len(airport),
        summer_city_temperature_qc_counts=dict(Counter(r['temperature_qc'] for r in city)),
        summer_city_unique_good_timestamps=len(unique),summer_city_good_time_gaps_hours=dict(gaps),
        summer_city_good_first_utc=unique[0],summer_city_good_last_utc=unique[-1],
        location_report_counts={str(k):v for k,v in Counter((r['latitude'],r['longitude'],r['elevation_m'],r['report_type']) for r in rows).items()},
        notes=['The station identifier merges city synoptic and airport records; never merge solely by station ID.',
               'City observations are approximately three-hourly, not a complete hourly series.',
               'Daily extrema are extrema of retained observations, not official daily maximum/minimum.',
               'RH is derived from temperature and dewpoint with a Magnus approximation, not directly observed RH.',
               'Solar radiation is not extracted from this mandatory-section parser.'])
(ROOT/'weather_quality_report.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
print(json.dumps(qa,ensure_ascii=False,indent=2))
print('HEATWAVE',json.dumps([r for r in daily if '2022-08-11'<=r['date_beijing']<='2022-08-15']))
