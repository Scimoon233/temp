# External Shading and Night Ventilation in a Hangzhou Residential Prototype: Effects on Summer Overheating and Sensible Cooling Demand

## Highlights

• Combined measures lower mean summer air temperature by 1.85–2.12°C.
• Overheating degree-hours decrease by 17.5–17.7%.
• Ideal sensible cooling demand decreases by 6.44–7.01%.

## Abstract

This study evaluates how external shading and temperature-controlled night ventilation reduce summer overheating and sensible cooling demand in a Hangzhou residential prototype. A two-zone resistance–capacitance model used hourly weather for 2025 and 2026 to compare baseline, shading, ventilation and combined scenarios under free-running and 26°C ideal-cooling operation. Relative to baseline, combined measures lowered mean free-running air temperature by 1.85–2.12°C and overheating degree-hours above 28°C by 17.5–17.7%, while reducing ideal sensible cooling demand by 6.44–7.01%. Night ventilation achieved the larger overheating reduction among the individual measures; shading achieved the larger cooling-demand reduction. The combination had the lowest overheating degree-hours and cooling demand across twenty tested input sets. These results support combining daytime solar control with night ventilation when outdoor air is at least 1°C cooler than indoors, prioritizing shading for demand reduction under ideal-cooling operation.

Keywords: External shading; Night ventilation; Thermal network; Overheating; Sensible cooling; Hangzhou.

## 1. Introduction


Passive cooling can improve summer building performance by reducing heat entry and using cooler outdoor air to discharge stored heat. Short et al. (2018) examined solar exposure, enclosed balconies and ventilation in Hangzhou apartments, while Artmann et al. (2008) identified weather, airflow and thermal storage as important determinants of night cooling. Building on these mechanisms, this study evaluates how much external shading, night ventilation and their combination can reduce overheating and sensible cooling demand in a residential prototype. Comparing free-running and 26°C ideal-cooling operation reveals how operating conditions affect the value of each measure and provides a basis for coordinating them in summer design.

## 2. Methods


A public floor plan (HZXQF, n.d.) informed a reconstructed prototype comprising a 41.1 m² living zone and a separate 6.3 m² enclosed balcony. An assumed 2.7 m height gives volumes of 110.97 and 17.01 m³. Both zones are well mixed; the partition remains closed. Horizontal boundaries and two east-facing wall segments are adiabatic. Assumed external whole-window areas are 3.525 and 14.07 m². Each zone contains an air node and an effective thermal-mass node. Air balances include envelope conduction, ventilation, interzone exchange, gains and cooling; mass nodes exchange heat with the air and receive allocated gains.


Wall resistance uses layer thicknesses and conductivities from Short et al. (2018, supplementary Table S1). Effective heat capacity, assumed independently of uncertain material heat capacities, is 165 kJ/(m² K). Whole-window U = 6.7 W/(m² K) and SHGC = 0.70 represent clear single-glazed aluminium windows (NSW Government, n.d.). Closed/open total air-change rates of 0.44/1.51 per hour use summer-night bedroom medians from Hou et al. (2019, Table 6); transferring them to these zones is a modelling assumption. Living-zone gains are 16.7 W/m² from 18:00–08:00 and 30% otherwise. The magnitude draws on Short et al.; this schedule is independently assumed, not measured.


ERA5 data obtained through Open-Meteo provide 2,208 hourly records per summer, with no missing values. Radiation represents the preceding hour; solar position uses its midpoint and outdoor temperature uses adjacent endpoint means (Open-Meteo, n.d.). Preserving the source records yields intervals from 31 May 23:00 to 31 August 23:00, UTC+8; the first temperature is held constant for the missing initial endpoint. Direct, isotropic diffuse and ground-reflected radiation are calculated for each facade. An assumed 25% of admitted balcony solar gain is allocated to the living zone, with the remainder retained in the balcony, avoiding double counting.


S0 has background ventilation only; S1 removes 50% of window direct radiation; S2 enables night ventilation; S3 combines both. Each zone independently switches to the open-window total rate during 21:00–07:00 when indoor air is at least 1 K warmer than outdoors. Free-running simulations evaluate DH28 = Σmax(Tin − 28, 0)Δt, in K h, using 28°C as a research threshold. Separate ideal-cooling simulations impose a continuously available 26°C upper limit in the living zone only and sum sensible heat removal in kWh_th. They include neither latent loads nor equipment electricity.


Backward Euler integration uses 300 s steps after 28 days of repeated-first-week warm-up. In the 2025 baseline checks, halving the step changed key cumulative metrics by less than 0.006%; energy-balance and initialization checks also passed. These checks support numerically stable scenario comparisons. Twenty input sets, including the baseline, test airflow, thermal mass, windows, shading and other assumptions; each variant is compared with its own S0.

## 3. Results

Table 1. Baseline scenario comparison; cooling is ideal sensible heat removal.
|Year|Case|DH28 (K h)|Cooling (kWh_th)|Cooling cut (%)|
|---|---|---|---|---|
|2025|S0|26,593.1|3,757.0|0.00|
|2025|S1|24,601.3|3,514.7|6.45|
|2025|S2|23,724.5|3,735.3|0.58|
|2025|S3|21,935.9|3,493.8|7.01|
|2026|S0|22,884.1|3,308.6|0.00|
|2026|S1|21,348.8|3,121.6|5.65|
|2026|S2|20,206.4|3,281.7|0.82|
|2026|S3|18,830.9|3,095.4|6.44|

All three measures improved baseline performance (Table 1). S3 reduced mean free-running air temperature by 2.12°C in 2025 and 1.85°C in 2026, and DH28 by 17.5% and 17.7%. Night ventilation alone reduced DH28 more than the tested 50% direct shading; shading produced the greater reduction in ideal cooling demand. Residual S3 overheating lasted 2,172.0 and 2,179.8 of 2,208 hours, so the principal free-running benefit was lower overheating intensity.


S3 reduced ideal demand by 263.2 kWh_th in 2025, from 3,757.0 to 3,493.8 kWh_th, and by 213.2 kWh_th in 2026, from 3,308.6 to 3,095.4 kWh_th. Across all twenty input sets, S3 had the lowest DH28 and cooling demand; individual-measure rankings varied. For demand D, interaction I = (D0 − D3) − (D0 − D1) − (D0 − D2) was −203.1 and −159.7 K h for DH28, and −0.88 and −0.74 kWh_th for cooling. Combined cooling benefits were approximately additive with slight diminishing returns.

## 4. Discussion and conclusions

### 4.1. Design implications

The results support two complementary design actions: reduce daytime solar input and discharge heat during cooler night hours. Living-zone ventilation operated throughout the 920-hour night window in free-running S2 and S3. With ideal cooling, 164 hours in 2025 and 206 hours in 2026 met the opening rule: indoor air near 26°C generally needs outdoor air near or below 25°C to provide the specified 1 K difference. Temperature-controlled opening therefore targets the available sensible cooling opportunity. Under the tested 26°C schedule, external shading is the principal demand-reduction measure, complemented by night ventilation when this opportunity occurs.

Heat balances clarify which paths solar control can address. In 2025, the living zone received 457.7 kWh_th through its own external windows and 507.9 kWh_th as allocated secondary balcony solar gain, while transferring a net 243.7 kWh_th to the balcony through the partition. Distinguishing these paths supports including balcony glazing in solar-control assessment while retaining its buffer-zone heat exchange. Together with the stable combination ranking, this provides a physical basis for evaluating solar exclusion and night-time discharge as a coordinated strategy.

### 4.2. Scope and further work

The analysis is an uncalibrated prototype comparison. Baseline free-running peaks of 50.11°C and 47.84°C depend on assumed glazing, internal gains, balcony solar allocation and simplified thermal boundaries; overhang and reduced-gain comparisons changed absolute outcomes. Fixed airflow, lumped storage, omitted sky longwave exchange and two summers also bound interpretation. Actual operation additionally involves humidity, rain, security and noise. These factors define priorities for refining the estimated benefits and testing application to particular dwellings.

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
