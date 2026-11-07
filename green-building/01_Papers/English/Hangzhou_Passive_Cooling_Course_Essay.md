# Shading and Night Ventilation in a Hangzhou Residential Prototype: Overheating and Sensible Cooling Demand

## Abstract

External shading and night ventilation can improve summer conditions, but their benefits depend on how a dwelling operates. A two-zone thermal-network model compared four scenarios using two summers of Hangzhou weather. Combined measures reduced free-running overheating degree-hours above 28°C by 17.5% in 2025 and 17.7% in 2026. Under ideal cooling at 26°C, sensible cooling demand fell by 7.0% and 6.4%, whereas ventilation alone reduced demand by only 0.6% and 0.8%. Fewer eligible opening hours explain much of this difference. These are uncalibrated prototype results: substantial residual overheating and uncertain balcony and occupancy assumptions limit their application to actual dwellings.

## 1. Introduction

Passive cooling contributes to green building design by limiting heat entry and exploiting favourable outdoor conditions. In Hangzhou apartments, Short et al. (2018) examined solar exposure, enclosed balconies and ventilation as adaptation issues. Their results motivate local investigation without establishing performance for a different dwelling. Night ventilation also depends on weather, airflow and thermal storage (Artmann et al., 2008). This essay asks whether shading and ventilation give comparable benefits in a free-running dwelling and one cooled to 26°C, and whether their combination provides more than additive benefits. Its contribution is a transparent prototype comparison under two historical summers, rather than a new passive-cooling method or a representative assessment of Hangzhou housing.

## 2. Methods

A public floor plan (HZXQF, n.d.) informed a reconstructed prototype comprising a 41.1 m² living zone and a separate 6.3 m² enclosed balcony. An assumed 2.7 m height gives volumes of 110.97 and 17.01 m³. Both zones are well mixed; the partition remains closed. Horizontal boundaries and two east-facing wall segments are adiabatic. Assumed external whole-window areas are 3.525 and 14.07 m². Each zone contains an air node and an effective thermal-mass node. Air balances include envelope conduction, ventilation, interzone exchange, gains and cooling; mass nodes exchange heat with the air and receive allocated gains.

Wall resistance uses layer thicknesses and conductivities from Short et al. (2018, supplementary Table S1). Effective heat capacity, assumed independently of uncertain material heat capacities, is 165 kJ/(m² K). Whole-window U = 6.7 W/(m² K) and SHGC = 0.70 represent clear single-glazed aluminium windows (NSW Government, n.d.). Closed/open total air-change rates of 0.44/1.51 per hour use summer-night bedroom medians from Hou et al. (2019, Table 6); transferring them to these zones is a modelling assumption. Living-zone gains are 16.7 W/m² from 18:00–08:00 and 30% otherwise. The magnitude draws on Short et al.; this schedule is independently assumed, not measured.

ERA5 data obtained through Open-Meteo provide 2,208 hourly records per summer, with no missing values. Radiation represents the preceding hour; solar position uses its midpoint and outdoor temperature uses adjacent endpoint means (Open-Meteo, n.d.). Preserving the source records yields intervals from 31 May 23:00 to 31 August 23:00, UTC+8; the first temperature is held constant for the missing initial endpoint. Direct, isotropic diffuse and ground-reflected radiation are calculated for each facade. An assumed 25% of admitted balcony solar gain is allocated to the living zone, with the remainder retained in the balcony, avoiding double counting.

S0 has background ventilation only; S1 removes 50% of window direct radiation; S2 enables night ventilation; S3 combines both. Each zone independently switches to the open-window total rate during 21:00–07:00 when indoor air is at least 1 K warmer than outdoors. Free-running simulations evaluate DH28 = Σmax(Tin − 28, 0)Δt, in K h, using a research threshold rather than a comfort-compliance limit. Separate ideal-cooling simulations impose a continuously available 26°C upper limit in the living zone only and sum sensible heat removal in kWh_th. They include neither latent loads nor equipment electricity.

Backward Euler integration uses 300 s steps after 28 days of repeated-first-week warm-up. In the 2025 baseline checks, halving the step changed key cumulative metrics by less than 0.006%; energy-balance and initialization checks also passed. These checks establish numerical consistency, not measured accuracy. Twenty input sets, including the baseline, test airflow, thermal mass, windows, shading and other assumptions; each variant is compared with its own S0.

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

DH28 refers to free running; cooling cuts are relative to the same year’s S0.

Table 1 shows distinct rankings: ventilation outperformed 50% direct shading for free-running DH28, while shading reduced ideal cooling demand more. S3 lowered mean air temperature by 2.12°C and 1.85°C and DH28 by 17.5% and 17.7%. However, S3 still exceeded 28°C for 2,172.0 and 2,179.8 of 2,208 hours. It reduced overheating intensity without resolving the overheating condition.

S3 reduced ideal demand from 3,757.0 to 3,493.8 kWh_th in 2025 and from 3,308.6 to 3,095.4 kWh_th in 2026. For a demand indicator D, interaction is I = (D0 − D3) − (D0 − D1) − (D0 − D2). DH28 interactions were −203.1 and −159.7 K h; cooling interactions were −0.88 and −0.74 kWh_th. The combination performed best but did not exceed additive benefits; cooling benefits were approximately additive, with slight diminishing returns.

## 4. Discussion

The operating-state difference follows directly from the temperature-based controller. In free-running S2 and S3, living-zone ventilation operated throughout the 920-hour night window in both years. With ideal cooling, only 164 hours in 2025 and 206 hours in 2026 qualified, because indoor air near 26°C generally requires outdoor air near or below 25°C to satisfy the 1 K rule. Thus, free-running temperature improvement is insufficient evidence for an equivalent reduction in cooling demand. Humidity, rain, security and noise could further restrict practical opening; their effects were not simulated.

Absolute temperatures require particular caution. Baseline free-running peaks reached 50.11°C and 47.84°C. Energy ledgers identify solar and internal gains as important inputs, but balanced equations cannot establish whether assumed glazing, occupancy or exposure match a real dwelling. In 2025, the living zone received 457.7 kWh_th through its external windows and 507.9 kWh_th as allocated secondary balcony solar gain, while transferring a net 243.7 kWh_th to the balcony through the partition. Balcony solar input and temperature-driven exchange therefore have distinct roles. Illustrative overhang, partition and reduced-gain comparisons changed absolute outcomes; none constitutes calibration.

S3 had the lowest DH28 and cooling demand in all twenty main input sets, although the ranking of individual measures changed. This supports a conditional preference for combined measures within the tested range, not a universal savings percentage. A single reconstructed dwelling, fixed airflow, lumped storage, simplified solar allocation, omitted sky longwave exchange and only two summers limit generalisation. The practical design lesson is to assess solar control together with the night-time temperature opportunity and intended cooling setpoint.

## 5. Conclusion

For this prototype, shading and night ventilation together reduced overheating intensity and ideal sensible cooling demand, but left extensive free-running overheating. Ventilation alone produced much smaller cooling-demand reductions than free-running improvements because the 26°C operating state restricted eligible opening hours. Combined benefits were slightly sub-additive. These findings support comparing passive measures under explicitly defined operating conditions; they do not establish actual electricity savings or predict indoor temperatures for a specific Hangzhou home.

## References

Artmann, N., Manz, H., Heiselberg, P., 2008. Parameter study on performance of building cooling by night-time ventilation. Renewable Energy 33, 2589–2598. [10.1016/j.renene.2008.02.025](https://doi.org/10.1016/j.renene.2008.02.025).

Hou, J., Sun, Y., Chen, Q., et al., 2019. Air change rates in urban Chinese bedrooms. Indoor Air 29, 828–839. [10.1111/ina.12582](https://doi.org/10.1111/ina.12582).

HZXQF, n.d. Public listing and floor plan, 71.05 m² apartment. [Source page](https://www.hzxqf.com/house/120716888258.html) (accessed 7 November 2026).

NSW Government, n.d. Default Window Data, item 5. [Planning Portal](https://www.planningportal.nsw.gov.au/basix-thermal-comfort/diy-method/windows/frame-glass-types/default-window-data) (accessed 7 November 2026).

Open-Meteo, n.d. Historical Weather API: ERA5 and hourly variable definitions. [Documentation](https://open-meteo.com/en/docs/historical-weather-api) (accessed 7 November 2026).

Short, C.A., Song, J., Mottet, L., Chen, S., Wu, J., Ge, J., 2018. Challenges in the low-carbon adaptation of China’s apartment towers. Building Research & Information 46, 899–930. [10.1080/09613218.2018.1489465](https://doi.org/10.1080/09613218.2018.1489465).
