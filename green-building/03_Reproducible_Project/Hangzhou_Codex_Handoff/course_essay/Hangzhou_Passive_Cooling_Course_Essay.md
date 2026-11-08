# External Shading and Night Ventilation in a Hangzhou Residential Prototype: Effects on Summer Overheating and Sensible Cooling Demand

## Highlights

• Combined measures lower mean summer air temperature by 1.85–2.12°C.
• Overheating degree-hours decrease by 17.5–17.7%.
• Ideal sensible cooling demand decreases by 6.44–7.01%.

## Abstract

This study evaluates how external shading and temperature-controlled night ventilation reduce summer overheating and sensible cooling demand in a Hangzhou residential prototype. A two-zone resistance–capacitance model used hourly weather for 2025 and 2026 to compare baseline, shading, ventilation and combined scenarios under free-running and 26°C ideal-cooling operation. Relative to baseline, combined measures lowered mean free-running air temperature by 1.85–2.12°C and overheating degree-hours above 28°C by 17.5–17.7%, while reducing ideal sensible cooling demand by 6.44–7.01%. Under baseline assumptions, night ventilation achieved the larger overheating reduction among the individual measures; shading achieved the larger cooling-demand reduction. The combination had the lowest overheating degree-hours and cooling demand across twenty tested input sets. These results support combining daytime solar control with night ventilation when outdoor air is at least 1°C cooler than indoors, prioritizing shading for demand reduction under ideal-cooling operation.

Keywords: External shading; Night ventilation; Thermal network; Overheating; Sensible cooling; Hangzhou.

## 1. Introduction


Passive cooling reduces heat entry and uses cooler outdoor air to discharge stored heat. Short et al. (2018) examined solar exposure, enclosed balconies and ventilation in Hangzhou apartments; Artmann et al. (2008) identified weather, airflow and thermal storage as determinants of night cooling. This study compares shading and night ventilation under free-running and 26°C ideal-cooling operation. Its contribution is to quantify their different effects on overheating and sensible demand within one dwelling and weather framework, and to test whether combined benefits persist as inputs change. This supports coordinating the measures according to operating conditions.

## 2. Methods


A public floor plan (HZXQF, n.d.) informed a prototype with a 41.1 m² living zone and separate 6.3 m² enclosed balcony. An assumed 2.7 m height gives volumes of 110.97 and 17.01 m³. Both zones are well mixed; the partition remains closed. Horizontal boundaries and two east-facing wall segments are adiabatic. External whole-window areas are assumed as 3.525 and 14.07 m². Each zone has air and effective thermal-mass nodes; balances include conduction, ventilation, interzone exchange, allocated gains and cooling.


Wall resistance uses layers from Short et al. (2018, supplementary Table S1). Effective heat capacity is independently assumed as 165 kJ/(m² K). Whole-window U = 6.7 W/(m² K) and SHGC = 0.70 represent clear single-glazed aluminium windows (NSW Government, n.d.). Closed/open total air-change rates of 0.44/1.51 per hour use summer-night bedroom medians from Hou et al. (2019, Table 6); zone transfer is an assumption. Living-zone gains are 16.7 W/m² during 18:00–08:00 and 30% otherwise. The magnitude draws on Short et al.; the schedule is independently assumed.


Open-Meteo supplies 2,208 hourly ERA5 records per summer, aligned in UTC+8 to the source radiation intervals (Open-Meteo, n.d.). Facade radiation includes direct, isotropic diffuse and ground-reflected components. An assumed 25% of admitted balcony solar gain is allocated to the living zone and the remainder to the balcony. Data alignment, initialization and diagnostic calculations are documented in the accompanying reproducible files.


S0 has background ventilation; S1 removes 50% of window direct radiation; S2 enables night ventilation; S3 combines both. Each zone independently uses the open-window rate during 21:00–07:00 when indoor air is at least 1 K warmer than outdoors. Free-running overheating is DH28 = Σmax(Tin − 28, 0)Δt, in K h. Separate ideal simulations impose a continuously available 26°C living-zone upper limit and sum sensible heat removal in kWh<sub>th</sub>, excluding latent loads and equipment electricity.


Backward Euler integration uses 300 s steps and 28 days of warm-up. Halving the step changed key 2025 baseline cumulative metrics by less than 0.006%; balance and initialization checks passed. Twenty discrete input sets test airflow, mass, windows, shading and other assumptions, each compared with its own S0.

## 3. Results

Table 1. Baseline scenario comparison; cooling is ideal sensible heat removal.
|Year|Case|DH28 (K h)|Cooling (kWh<sub>th</sub>)|Cooling cut (%)|
|---|---|---|---|---|
|2025|S0|26,593.1|3,757.0|0.00|
|2025|S1|24,601.3|3,514.7|6.45|
|2025|S2|23,724.5|3,735.3|0.58|
|2025|S3|21,935.9|3,493.8|7.01|
|2026|S0|22,884.1|3,308.6|0.00|
|2026|S1|21,348.8|3,121.6|5.65|
|2026|S2|20,206.4|3,281.7|0.82|
|2026|S3|18,830.9|3,095.4|6.44|

All three measures improved the baseline (Table 1). In 2025, S3 lowered mean free-running air temperature from 40.04°C to 37.92°C; in 2026, from 38.36°C to 36.51°C. These are reductions of 2.12°C and 1.85°C, with DH28 falling by 17.5% and 17.7%. Under baseline assumptions, night ventilation reduced DH28 more than shading, while shading reduced ideal demand more. S3 overheating persisted for 2,172.0 and 2,179.8 of 2,208 hours; the main benefit was lower overheating intensity.


S3 reduced ideal demand by 263.2 kWh<sub>th</sub> in 2025 and 213.2 kWh<sub>th</sub> in 2026 (7.01% and 6.44%). Across twenty input sets and both summers, S3 had the lowest DH28 and demand, while individual rankings varied. Combined DH28 reductions ranged from 10.86% to 28.06%, and demand reductions from 3.63% to 13.43%, relative to each input set’s own baseline. These ranges describe the tested settings. Combined cooling benefits were approximately additive with slight diminishing returns.

## 4. Discussion and conclusions

### 4.1. Design implications

The results support reducing daytime solar input and discharging heat during cooler nights. Living-zone ventilation covered the 920-hour night window in free-running S2 and S3; with ideal cooling, only 164 hours in 2025 and 206 hours in 2026 met the opening rule. Indoor air near 26°C generally requires outdoor air near or below 25°C for the specified 1 K difference. Under the baseline 26°C schedule, shading is therefore the principal demand-reduction measure, complemented by ventilation when cooler outdoor air is available.

In 2025, living-zone solar gains through its own windows and allocated from the balcony were 457.7 and 507.9 kWh<sub>th</sub>, respectively; net partition exchange exported 243.7 kWh<sub>th</sub> to the balcony. These paths support including balcony glazing in solar control while retaining its buffer-zone heat exchange.

### 4.2. Scope and further work

High baseline temperatures and peaks (50.11°C and 47.84°C) reflect specified solar exposure, gains and boundaries. A 2025 boundary check with a 1 m overhang, half internal gains and zero secondary balcony solar allocation gave an S0 mean of 36.18°C. This identifies heat-input assumptions as important for absolute predictions. The uncalibrated lumped model uses fixed airflow and omits sky longwave exchange and latent loads; humidity, rain, security and noise also shape implementation.

### 4.3. Conclusions

For the modelled Hangzhou dwelling, combining external shading and night ventilation achieved a 1.85–2.12°C reduction in summer mean free-running air temperature, a 17.5–17.7% reduction in overheating degree-hours above 28°C, and a 6.44–7.01% reduction in ideal sensible cooling demand at 26°C. Its first-place ranking across twenty tested input sets supports using the measures together under the studied conditions.

The resulting design priority is to reduce daytime solar gains through external shading and use night ventilation to provide additional heat removal whenever the outdoor temperature is at least 1 K below indoor temperature. This coordinated strategy can moderate summer overheating and reduce the sensible cooling duty of active systems.

## References

Artmann, N., Manz, H., Heiselberg, P., 2008. Parameter study on performance of building cooling by night-time ventilation. Renewable Energy 33, 2589–2598. [10.1016/j.renene.2008.02.025](https://doi.org/10.1016/j.renene.2008.02.025).

Hou, J., Sun, Y., Chen, Q., et al., 2019. Air change rates in urban Chinese bedrooms. Indoor Air 29, 828–839. [10.1111/ina.12582](https://doi.org/10.1111/ina.12582).

HZXQF, n.d. Public listing and floor plan, 71.05 m² apartment. [Source page](https://www.hzxqf.com/house/120716888258.html) (accessed 7 November 2026).

NSW Government, n.d. Default Window Data, item 5. [Planning Portal](https://www.planningportal.nsw.gov.au/basix-thermal-comfort/diy-method/windows/frame-glass-types/default-window-data) (accessed 7 November 2026).

Open-Meteo, n.d. Historical Weather API: ERA5 and hourly variable definitions. [Documentation](https://open-meteo.com/en/docs/historical-weather-api) (accessed 7 November 2026).

Short, C.A., Song, J., Mottet, L., Chen, S., Wu, J., Ge, J., 2018. Challenges in the low-carbon adaptation of China’s apartment towers. Building Research & Information 46, 899–930. [10.1080/09613218.2018.1489465](https://doi.org/10.1080/09613218.2018.1489465).
