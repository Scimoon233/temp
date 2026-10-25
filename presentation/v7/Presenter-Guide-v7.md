# Presenter Guide V7

1143 spoken English words on slides 1–17. At 120–135 words/minute this is 8.5–9.5 minutes of continuous speech, before pauses and slide changes. Rehearse with figures and reserve Q&A within 10–12 minutes. Takeaways, Q&A and source-basis sections are not extra timed speech.

## 01 | VineWeave Canopy

Takeaway: Introduce the project before the team credits.

Spoken script: VineWeave Canopy combines climbing plants with a tree-like support to provide pedestrian shade. Our group connects parametric geometry, material and construction choices, and shading analysis. The names below identify our responsibilities. We will explain both the design decisions and the evidence supporting them.

Transition: First, the final geometry and its drawing definitions.

Q&A: Where are the full roles? The cover retains the core allocation; the planning document records the complete supplied descriptions.

Source basis — not spoken:

User-supplied team-allocation screenshot; project title approved in conversation.

P1: final Rhino model and project modelling reports.

Cover roles follow the supplied five-person allocation; no dates or school logo.

## 02 | Define the final geometry—and how it is measured

Takeaway: Final dimensions need explicit definitions and readable technical views.

Spoken script: The final geometry has an overall height of about three point four eight metres and a plan extent of six point two two by six point six six metres. Its approximate maximum horizontal exterior span is six point nine one metres. For these curved supports, inclination is defined by the endpoint chord above horizontal. The accompanying drawing sheets explain that definition and the measured range.

Transition: Next, link those features to environmental potential.

Q&A: Is 6.91 metres a circular diameter? No. It is the maximum pair distance in the projected exterior mesh, not a foliage diameter or net usable width.

Source basis — not spoken:

P1: original project report §03 actual canopy geometry.

Supplement 数据/00_结构参数与Rhino检查.json; original final-model mesh/centre-lines.

research/supplemental-geometric-check.json: geometry derived from the supplied baseline mesh and support curves.

Dimensions ≈6.22×6.66×3.48m; maximum projected span ≈6.91m; support endpoint-chord angles ≈45.9–50.7°. Model-derived descriptors, not measured site dimensions.

## 03 | How the canopy can improve pedestrian comfort

Takeaway: Follow the sunlight, air and plant-water arrows; only shade is quantified here.

Spoken script: The crown and foliage intercept direct sun before it reaches people and the ground. The solar arrows identify the pathway quantified in our optical scenarios. Blue arrows show potential air paths through open sides, not a simulated wind improvement. The dashed plant-water arrows indicate possible evapotranspiration, which depends on healthy plants and water. Denser foliage can also resist airflow.

Transition: Material assignment follows the structural roles.

Q&A: Do these arrows show simulated temperature or wind? No. They explain physical mechanisms; the project quantifies shade, not cooling degrees or wind speed.

Source basis — not spoken:

Original analysis report §02 支架—植物—降温作用逻辑, table 遮阴/辐射/蒸腾/空气流动.

Original report: 没有把遮阴率换算为确定温降; no measured temperature/wind/Tmrt/UTCI results.

Source: 植物遮阴减少人体和地面直接太阳暴露; 叶片水分蒸发涉及潜热交换，收益受供水、气孔和天气影响; 开敞侧界保留侧向通道. Arrows explain reported mechanisms, not simulated fields.

## 04 | Assign materials to the roles they must perform

中文提示：先讲材料分区与数量；这是材料方案，不是整体安全结论。

Takeaway: The quantity schedule links a clear material role to a specific part of the model.

Spoken script: The take-off gives twelve ground-reaching supports and forty-seven crown members, with a total centre-line length of two hundred and eighty-eight point six six metres. We propose an eighty-by-four millimetre steel tube for supports and solid engineered bamboo for the crown. This is a material strategy, not proof that either zone is safe.

Transition: The screening table shows the inputs; the next decision is how to use them.

Q&A: Does the exterior model contain the final wall thickness? No. The pipe exterior and proposed material section must be distinguished.

Source basis — not spoken:

Cost-Analysis.xlsx / 材料比选!A17:G18; 几何与用量 section B.

Cost-Analysis.xlsx / 规格与连接!A4:E5; 模块化建造分析!A3.

Source split: 47 crown members, 219.28m, solid Ø80 bamboo; 12 ground-reaching steel Ø80×4 supports, 69.38m. Support text: 受压为主兼受风弯; crown text: 挠度在铰接下不满足L/200.

## 05 | Read the material inputs before making the choice

中文提示：表中单价是按相同全长比较材料输入，不是最终单元总价；材料常数仍为工作簿输入。

Takeaway: Material screening includes mechanical and practical conditions, not only carbon.

Spoken script: These are preliminary screening inputs. Each cost column assumes the same full member length; it is not the adopted unit budget. Steel offers much greater nominal bending capacity. Engineered bamboo is proposed for the crown, but stiffness, treatment and product-specific evidence are essential. Raw bamboo’s low reference cost does not remove its variability and maintenance issues.

Transition: These inputs motivate a hybrid strategy, with conditions attached.

Q&A: Are these all verified design values? No. They are workbook screening inputs, and the bamboo identity and properties must be confirmed consistently.

Source basis — not spoken:

Cost-Analysis.xlsx / 材料比选!A6:O13, selected rows 6,7,11,12,13.

Cost-Analysis.xlsx / 选型决策矩阵!A32:B34.

Five displayed rows retain workbook inputs. Cost assumes all 288.66m use that row’s material; it is not the final hybrid unit cost. Durability and environmental scoring are workbook judgements, not verified product lifetimes.

## 06 | Why steel supports and an engineered-bamboo crown?

中文提示：按原工作簿解释钢支撑与竹冠面；别把竹材单项指标的优势说成整套造价更低。

Takeaway: The material strategy follows structural roles and keeps feasibility conditions explicit.

Spoken script: The workbook combines screening with a structural feasibility gate. Steel is assigned to supports under compression and wind bending. Bamboo is adopted for the crown using cost and carbon inputs, but the deflection sheet requires node rotational-stiffness verification. The lower cards summarise the five material criteria. Member-input savings do not establish a lower total unit cost.

Transition: The next check shows why crown stiffness makes the joints important.

Q&A: Does the material screen establish a lower total unit cost? No. It compares equal-length member inputs. The separate unit budget includes nodes, installation and care. Low conductivity also does not establish a measured temperature benefit.

Source basis — not spoken:

Cost-Analysis.xlsx / 材料比选!A17:G18, A23:H24.

Cost-Analysis.xlsx / 挠度校核!A21:G23 and A46:B46.

Cost-Analysis.xlsx / 选型决策矩阵!A2:B2 and A28:B34; 规格与连接!A4:E5; 模块化建造分析!A3.

Workbook assigns steel to compression/wind-bending support role; tabulated EI steel145.2049 vs bamboo20.1062kN·m². Decision matrix requires feasibility gates in addition to scores. Row46 explicitly says 必须由结构同学出刚接节点详图并验算转动刚度 and the ≥3×simple-support assumption must hold. Five criteria follow the supplied rubric/workbook; no new performance result is claimed.

## 07 | The beam check sets a requirement for the joint

中文提示：先指33.25mm目标，再看两种理想边界；原表明确要求节点详图与转动刚度验算。

Takeaway: The adopted target is numerically between two ideal beam results; node verification is explicitly required by the workbook.

Spoken script: The same six point six five metre bamboo-member calculation gives one hundred point five millimetres with simple supports and twenty point one with ideal fixed ends. The adopted target is thirty-three point two five millimetres, shown between them. This makes rotational restraint a design requirement to investigate. The proposed node does not prove that restraint, and the member check does not verify the whole frame.

Transition: The proposed node also has a significant budget allowance.

Q&A: What must be verified next? Product stiffness, node moment–rotation behaviour, load transfer and the whole frame under relevant loads. The supplied workbook explicitly requires a node detail and rotational-stiffness verification.

Source basis — not spoken:

Cost-Analysis.xlsx / 挠度校核!B6:B16, A21:G23, A31:J32, A46:B46.

Cost-Analysis.xlsx / 模块化建造分析!A3.

Same simplified 6.65m solidØ80 bamboo member; E10GPa, wet foliage18kg/m² inputs; deflections100.5333873/20.1066775mm. Adopted6650/200=33.25mm; ratios3.02356 and0.60471. Node plate/sleeve/grout/adhesive/bolts are proposed in source, not verified restraint.

## 08 | The unit budget includes fabrication, installation and care

Takeaway: The budget makes the node trade-off visible.

Spoken script: The preliminary total is approximately fifty-one thousand six hundred and seventy-six yuan. Materials are fifty-nine percent of this total; the other categories include fabrication, installation and care. Within materials, twelve proposed nodes account for twelve thousand yuan, more than the primary steel members. The component table is only part of the overall cost, not an additional total.

Transition: Next, the carbon and maintenance picture.

Q&A: Are the node prices confirmed? No. They are the most uncertain allowance and need a defined detail and supplier quotation.

Source basis — not spoken:

Cost-Analysis.xlsx / 造价明细, seven category totals and materials detail.

Seven-category sum 51,675.7187099CNY; materials30,549.3022975CNY; 12 nodes×1,000CNY=12,000CNY. All displayed prices remain estimates; component rows are included in total.

## 09 | Account for the members, base and maintenance needs

Takeaway: The estimate helps identify contributors and care responsibilities.

Spoken script: The primary members and counterweight dominate the current carbon estimate. The counterweight contributes about thirty-nine percent, so foundation decisions also matter. We show the adopted estimate rather than claiming a verified life-cycle result. Outdoor performance also needs coating care, bamboo treatment and connection inspection. Product factors and the allowance for actual node materials still require checking.

Transition: Plant choice adds another set of requirements.

Q&A: Is stored biological carbon deducted? No. It is not credited in this estimate, and factor boundaries are not yet fully aligned.

Source basis — not spoken:

Cost-Analysis.xlsx / 材料比选 carbon summary, adopted hybrid row.

Cost-Analysis.xlsx / 模块化建造分析 and original report maintenance/interface proposals.

Adopted estimate: members1581.19629365 + base1088.64 + other150 =2819.83629365kgCO₂e; base38.61%. Factor boundaries not verified; no biogenic credit. Maintenance text follows protection/inspection proposals.

## 10 | Keep the planting mix conditional on the site

Takeaway: The 2+1 mix is a project proposal, not a verified choice for every city.

Spoken script: The material schedule proposes two Boston ivy plants and one Rangoon creeper. Boston ivy is deciduous, so a summer canopy should not be presented as year-round cover. The source lists Rangoon creeper as a twining companion and trumpet creeper as an alternative. Local climate and attachment still need checking, as required by the analysis report. Guides, irrigation and pruning are part of the planting design.

Transition: Next, the optical method used to evaluate shade.

Q&A: Is this mix suitable for every city? No. The analysis report requires checking local climate, climbing method, root space and maintenance.

Source basis — not spoken:

Cost-Analysis.xlsx / 爬藤植物选择!A5:H7 and A14:B14.

Cost-Analysis.xlsx / 模块化建造分析!A10:H10.

Original analysis report §07 plant interface: 确认当地气候、攀附方式、根区、叶重、风荷载及落叶/落果维护.

Source identifies Parthenocissus tricuspidata as main, Combretum indicum companion, Campsis grandiflora alternative; proposes2+1 plants,1.2m³ substrate and drip. Local suitability/attachment are checks, not new verified botanical claims.

## 11 | Two shade metrics answer different questions

中文提示：先分清两类指标，再读后面的百分比；不能混用、相加或换算摄氏度。

Takeaway: Identify the metric and time window before interpreting any percentage.

Spoken script: The first metric measures ideal leaf-envelope shadow on the target. The second includes frame shadows, assumed leaf patches, their overlap and transmittance. We use the first for the daily and solar-season result, and the second for parameter and coverage comparisons. The target is shared, but the percentages are not interchangeable. Neither is a temperature reduction.

Transition: First, read the ideal daily result across the full time window.

Q&A: What is the second formula? Aeq = Abare + (1 − τ)(Aleaf − Aoverlap), then divide by the target area. It is equivalent direct-beam blockage under the stated optical assumptions, not total solar-energy attenuation.

Source basis — not spoken:

Original project report and 分析参数与汇总.json: ideal continuous-leaf projection.

Supplement D_Structure_and_Plant_Cover_Simulation.docx, §01–02; 数据/模拟参数与汇总.json.

Supplement formula Aeq=Abare+(1−tau)(Aleaf−Aoverlap), tau=.15 assumed; same5×5m target excludingr.75m. Ideal leaf-envelope overlap and equivalent direct-beam blockage have different definitions; neither is temperature or total solar attenuation.

## 12 | A noon peak does not ensure all-day shade

中文提示：正午98.7%不能代表整段使用时间；时段与座椅位置要一起考虑。

Takeaway: Read the footprint and the whole time window, not only the noon peak.

Spoken script: The solstice footprint overlaps about forty-seven percent of the target at nine and fifteen solar time, and almost ninety-nine percent at noon. The curve adds the intervening hours and an equinox solar case. Their means are about seventy-five and fifty percent. The noon peak therefore cannot stand for the whole use period: morning and afternoon exposure must be checked when placing seating. The equinox comparison changes solar conditions, not plant leaf cover.

Transition: We then change one geometric control at a time.

Q&A: Does winter use the equinox result? No. Winter solar conditions and plant leaf states would need their own inputs.

Source basis — not spoken:

Original 04_图表与计算数据/01_原参数_C_D_典型时刻遮阴.csv and 02_原参数_C_D_15分钟遮阴曲线.csv, final-model rows.

Original report §结论与依据; §07 application and §08 evaluation.

09/12/15 solstice overlap47.2/98.7/47.2%; 09–15 means75.3% solstice and49.8% equinox. Source advises seating by use time and reporting weakest periods; noon peak cannot describe the whole window.

## 13 | Expanding the crown raises mean blockage: 52.3% → 66.1%

中文提示：只说原CSV给出的参数情景结果；同覆盖比例不等于相同种植面积和材料投入。

Takeaway: The crown-width result is part of a broader seven-model parameter study.

Spoken script: Seven cases change expansion, upper-height control or corner factor one at a time. At fifty percent cover, expansion changes mean blockage from fifty-two point three to sixty-six point one percent. The table retains the other results. The source report cautions that a larger crown at equal cover needs more planted area. These shade comparisons do not hold inputs equal or establish an optimum.

Transition: Next, keep the structure fixed and change foliage.

Q&A: Does the height control shift the whole model by 0.4 metres? No. It is smoothly weighted; actual maximum heights must be read from the geometry records.

Source basis — not spoken:

Supplement 数据/02_参数与生长覆盖_汇总.csv: Solstice, cover=.5, seven cases.

Supplement 数据/00_结构参数与Rhino检查.json and report §01–02.

Expansion52.2795–66.1435%; height57.7692–62.6491%; corner59.0899–61.7752% (rounded). Largest tested max–min spread is expansion; this does not compare sensitivities per unit change. Source: a larger crown at equal cover percentage also requires more planted area; equal percentage does not imply equal material or plant inputs.

## 14 | Coverage amount alone does not determine useful shade

中文提示：80到95覆盖增加2.8个百分点是时段均值；相同50%分布比较是正午值，别混成同一组。

Takeaway: The package tests both cover quantity and where that cover is placed.

Spoken script: The curve separates plan cover from mean direct-beam blockage. Bare members already provide shade at zero leaf cover. From eighty to ninety-five percent cover, mean blockage increases by only two point eight percentage points in these scenarios. Separately, at the same fifty percent cover, the three layouts give noon blockage from sixty-two point six to seventy-seven point five percent. The supplied report therefore asks us to consider leaf location and occupied-hour seating, not coverage alone.

Transition: We connect that moving footprint to public use.

Q&A: Why is 95% cover not 95% blockage? Target intersection, frame overlap, leaf placement and transmittance all affect the metric.

Source basis — not spoken:

Supplement 数据/02_参数与生长覆盖_汇总.csv: baseline Solstice cover0/.2/.5/.8/.95.

Supplement 数据/05_相同50覆盖_分布敏感性.csv: cover=.5, solar time12.

Supplement report §02: compare seat locations during occupied hours; same-cover spatial placement matters.

Mean blockage40.2187/48.6371/60.1972/67.9113/70.6955%;80→95 cover gives70.69545−67.91127=2.78418percentage points≈2.8pp. Noon patterns inner_spreading/dispersed/outer_first give77.4671/71.3662/62.6164%. These are distinct comparisons, not growth-time predictions.

## 15 | Put occupied-hour shade into the layout decision

Takeaway: A practical layout must use the real occupied area, not only a reference square.

Spoken script: The animation holds cover fixed while the sun moves. Seating should be checked during occupied hours, with room for circulation, the counterweight, roots and maintenance. The next verification step is a real-site assessment with simultaneous shaded and unshaded environmental observations. The current analysis does not establish net usable shaded floor area or a measured comfort improvement.

Transition: The last design link is construction organisation.

Q&A: Are sensors a new project module here? No. This is the existing validation proposal, not a new monitoring-system design.

Source basis — not spoken:

Original report §07 application scenarios and §08 evaluation/validation.

Supplement report §02; fixed-cover daytime-shadow GIF and related CSV.

Source: compare seating during occupied hours; allow root/water/maintenance/circulation; measure shaded/unshaded environmental variables. No actual-street or measured-comfort result supplied.

## 16 | Coordinate prefabricated modules and site interfaces

Takeaway: The assembly work is more specific than a generic prefabrication claim.

Spoken script: The proposal divides the system into crown members, supports, connections, base and planting. Numbering and preassembly help site organisation. However, the heavy counterweight governs lifting, and the sleeve-and-grout node requires curing and checks. The fourteen-person-day allowance is labour, not a calendar programme. A fully dry, losslessly reversible system should not be claimed.

Transition: Finally, our delivered work and its next checks.

Q&A: Is the node a finished construction detail? No. Its geometry, stiffness, fabrication and quality controls need to be resolved together.

Source basis — not spoken:

Cost-Analysis.xlsx / 模块化建造分析!A3:H10 and labour/assembly sections.

Cost-Analysis.xlsx / 造价明细 labour and counterweight entries.

Source modules: crown/supports/nodes/base/planting; grouting requires curing and changes reversibility. Base9072kg and labour14person-days are source estimates, not certified foundation or calendar programme.

## 17 | Connect geometry, construction and useful shade

Takeaway: The contribution is a connected body of design work with a clear evidence boundary.

Spoken script: The group delivers a parametric form and take-off, a proposed material and build-up strategy, and reproducible shade scenarios. The supplement adds seven parameter models, five cover states and seventeen hundred and fifty time-step results. These outputs make the design decisions traceable. Product data, joint behaviour, plant suitability and real-site performance are the next checks. Thank you.

Transition: We welcome your questions.

Q&A: What can be stated most confidently? The defined project geometry and the calculated shade scenarios under their explicit assumptions.

Source basis — not spoken:

P1 supplied Rhino/GH model; P3 workbook; P2/P5 analysis reports and datasets.

Supplement 数据/01_参数与生长覆盖_时段结果.csv and native-model checks.

Work summary traces three supplied streams; seven parameter cases, five cover states and1750main result rows. Remaining checks reflect explicitly assumed inputs and unverified nodes/site conditions.

## 18 | References and project evidence

Takeaway: Source labels let the audience distinguish literature, project calculations and proposals.

Spoken script: This is a reference and question page, not part of the planned spoken sequence. It identifies the literature leads and project evidence. Specific product parameters and standards still require original-source checks.

Transition: Return to the relevant result slide during questions.

Q&A: Why are some data preliminary? The supplied package contains assumptions and estimates that have not all been traced to product-specific or primary evidence.

Source basis — not spoken:

Original analysis report bibliography entries for Watanabe etal2014, Hoelscher etal2016, NOAA and UTCI.

User-provided project files P1–P5.

Bibliographic leads were supplied by the project; original-source checks remain pending. No DOI or new literature conclusion is invented.
