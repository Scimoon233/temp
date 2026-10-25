# V7逐项文字与依据对照

范围：主页面原生文字、表格单元、图表数值及讲稿句子。每页先列明来自用户材料的出处与依据，再列该页表述；同页表述对应其下所列来源。问句、标题和过渡用于组织已列材料，不构成新增实验结果。

“有材料出处”不等于材料中的假设已获验证。工程竹常数、湿植被荷载、透射率、报价和节点约束仍按输入/假设标注。原报告列出的外部文献并未冒充本轮已核验全文。

修改依据：Cost-Analysis.xlsx、原分析报告、参数/覆盖补充报告与CSV；新增算术复核见[Claim-Checks.json](Claim-Checks.json)。没有新增生长速率、实测温降、风速或结构安全结论。

## 01 — VineWeave Canopy

出处：

- User-supplied team-allocation screenshot; project title approved in conversation.
- P1: final Rhino model and project modelling reports.

材料依据／限定：Cover roles follow the supplied five-person allocation; no dates or school logo.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：GROUP 12
- 页面文字：VineWeave
- 页面文字：Canopy
- 页面文字：A tree-like climbing-plant support
- 页面文字：for pedestrian shade
- 页面文字：Parametric design  ·  Planting  ·  Shade performance
- 页面文字：TEAM & RESPONSIBILITIES
- 页面文字：臧唯羽
- 页面文字：Form & parametric
- 页面文字：modelling
- 页面文字：林新淇
- 页面文字：Materials &
- 页面文字：construction
- 页面文字：虞寒哲
- 页面文字：Shade performance
- 页面文字：& application
- 页面文字：徐世程
- 页面文字：PPT production
- 页面文字：& integration
- 页面文字：陈淼
- 页面文字：English presentation
- 页面文字：& Q&A

### 讲稿及答辩表述

- takeaway：Introduce the project before the team credits.
- script：VineWeave Canopy combines climbing plants with a tree-like support to provide pedestrian shade.
- script：Our group connects parametric geometry, material and construction choices, and shading analysis.
- script：The names below identify our responsibilities.
- script：We will explain both the design decisions and the evidence supporting them.
- transition：First, the final geometry and its drawing definitions.
- qa：Where are the full roles?
- qa：The cover retains the core allocation; the planning document records the complete supplied descriptions.

## 02 — Define the final geometry—and how it is measured

出处：

- P1: original project report §03 actual canopy geometry.
- Supplement 数据/00_结构参数与Rhino检查.json; original final-model mesh/centre-lines.
- research/supplemental-geometric-check.json: geometry derived from the supplied baseline mesh and support curves.

材料依据／限定：Dimensions ≈6.22×6.66×3.48m; maximum projected span ≈6.91m; support endpoint-chord angles ≈45.9–50.7°. Model-derived descriptors, not measured site dimensions.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：GEOMETRY & DRAWINGS
- 页面文字：Define the final geometry—and how it is measured
- 页面文字：Dimensioned plan/elevation views; a final parameter schedule, separate from sensitivity settings.
- 页面文字：Model records P1 and supplemental geometric check.
- 页面文字：Centre-line views; exterior dimensions rounded.
- 页面文字：Drawing sheets accompany the PPT.
- 页面文字：02
- 页面文字：6.22 m
- 页面文字：6.66 m
- 页面文字：PLAN
- 页面文字：3.48 m
- 页面文字：ELEVATION
- 页面文字：Curved support inclination is defined by its endpoint chord, not a local tangent.
- 表格：FINAL PARAMETER
- 表格：VALUE / DEFINITION
- 表格：Overall height
- 表格：≈3.48 m
- 表格：Plan extents
- 表格：≈6.22 × 6.66 m
- 表格：Maximum horizontal span
- 表格：≈6.91 m, exterior mesh
- 表格：Support inclination*
- 表格：45.9–50.7° to horizontal
- 表格：Member exterior diameter
- 表格：80 mm
- 表格：Corner / expansion
- 表格：0.85 / 1.08
- 页面文字：*Angle of each ground-reaching centre-line endpoint chord.
- 页面文字：Not a uniform member slope.

### 讲稿及答辩表述

- takeaway：Final dimensions need explicit definitions and readable technical views.
- script：The final geometry has an overall height of about three point four eight metres and a plan extent of six point two two by six point six six metres.
- script：Its approximate maximum horizontal exterior span is six point nine one metres.
- script：For these curved supports, inclination is defined by the endpoint chord above horizontal.
- script：The accompanying drawing sheets explain that definition and the measured range.
- transition：Next, link those features to environmental potential.
- qa：Is 6.91 metres a circular diameter?
- qa：No.
- qa：It is the maximum pair distance in the projected exterior mesh, not a foliage diameter or net usable width.

## 03 — How the canopy can improve pedestrian comfort

出处：

- Original analysis report §02 支架—植物—降温作用逻辑, table 遮阴/辐射/蒸腾/空气流动.
- Original report: 没有把遮阴率换算为确定温降; no measured temperature/wind/Tmrt/UTCI results.

材料依据／限定：Source: 植物遮阴减少人体和地面直接太阳暴露; 叶片水分蒸发涉及潜热交换，收益受供水、气孔和天气影响; 开敞侧界保留侧向通道. Arrows explain reported mechanisms, not simulated fields.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：FORM & COOLING LOGIC
- 页面文字：How the canopy can improve pedestrian comfort
- 页面文字：Three physical pathways, with the strength of evidence shown next to each.
- 页面文字：Shade: project P2/P5.
- 页面文字：Greening mechanisms: [1,2].
- 页面文字：Arrows are conceptual; no temperature or airflow field is simulated.
- 页面文字：03
- 页面文字：01  SHADE → LOWER EXPOSURE
- 页面文字：Direct sun on people and ground
- 页面文字：02  AIRFLOW
- 页面文字：Open sides retain possible air paths.
- 页面文字：Dense foliage can also add resistance.
- 页面文字：03  PLANT WATER
- 页面文字：Evapotranspiration may exchange latent heat; it needs healthy, watered plants.
- 页面文字：01  DIRECT SUN
- 页面文字：MODELLED
- 页面文字：Geometry + leaf location
- 页面文字：change useful shade.
- 页面文字：02 / 03: QUALITATIVE MECHANISMS
- 页面文字：Shade % does not equal cooling °C.

### 讲稿及答辩表述

- takeaway：Follow the sunlight, air and plant-water arrows; only shade is quantified here.
- script：The crown and foliage intercept direct sun before it reaches people and the ground.
- script：The solar arrows identify the pathway quantified in our optical scenarios.
- script：Blue arrows show potential air paths through open sides, not a simulated wind improvement.
- script：The dashed plant-water arrows indicate possible evapotranspiration, which depends on healthy plants and water.
- script：Denser foliage can also resist airflow.
- transition：Material assignment follows the structural roles.
- qa：Do these arrows show simulated temperature or wind?
- qa：No.
- qa：They explain physical mechanisms; the project quantifies shade, not cooling degrees or wind speed.

## 04 — Assign materials to the roles they must perform

出处：

- Cost-Analysis.xlsx / 材料比选!A17:G18; 几何与用量 section B.
- Cost-Analysis.xlsx / 规格与连接!A4:E5; 模块化建造分析!A3.

材料依据／限定：Source split: 47 crown members, 219.28m, solid Ø80 bamboo; 12 ground-reaching steel Ø80×4 supports, 69.38m. Support text: 受压为主兼受风弯; crown text: 挠度在铰接下不满足L/200.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：MATERIAL STRATEGY
- 页面文字：Assign materials to the roles they must perform
- 页面文字：Steel at the ground-reaching supports; proposed engineered bamboo across the crown.
- 页面文字：Project take-off and proposed member schedule (P1, P3).
- 页面文字：Sections and material mass remain preliminary specifications.
- 页面文字：04
- 表格：ZONE
- 表格：PROPOSED SECTION
- 表格：LENGTH
- 表格：12 steel supports
- 表格：Q355B tube / Ø80 × 4 mm
- 表格：69.38 m
- 表格：47 bamboo crown members
- 表格：Engineered bamboo / solid Ø80 mm
- 表格：219.28 m
- 表格：TOTAL
- 表格：59 members
- 表格：288.66 m
- 页面文字：Steel supports are proposed for force transfer and connection detailing.
- 页面文字：Crown bamboo requires stiffness, treatment and fabrication checks.

### 讲稿及答辩表述

- takeaway：The quantity schedule links a clear material role to a specific part of the model.
- script：The take-off gives twelve ground-reaching supports and forty-seven crown members, with a total centre-line length of two hundred and eighty-eight point six six metres.
- script：We propose an eighty-by-four millimetre steel tube for supports and solid engineered bamboo for the crown.
- script：This is a material strategy, not proof that either zone is safe.
- transition：The screening table shows the inputs; the next decision is how to use them.
- qa：Does the exterior model contain the final wall thickness?
- qa：No.
- qa：The pipe exterior and proposed material section must be distinguished.

## 05 — Read the material inputs before making the choice

出处：

- Cost-Analysis.xlsx / 材料比选!A6:O13, selected rows 6,7,11,12,13.
- Cost-Analysis.xlsx / 选型决策矩阵!A32:B34.

材料依据／限定：Five displayed rows retain workbook inputs. Cost assumes all 288.66m use that row’s material; it is not the final hybrid unit cost. Durability and environmental scoring are workbook judgements, not verified product lifetimes.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：MATERIAL SELECTION
- 页面文字：Read the material inputs before making the choice
- 页面文字：Representative screening inputs: section resistance, conductivity, carbon factor and equal-length material cost.
- 页面文字：Source: material-comparison workbook (P3). *Preliminary inputs; product, processing and factor boundaries need verification.
- 页面文字：05
- 表格：MATERIAL / SECTION
- 表格：BENDING* / kN·m
- 表格：λ* / W/(m·K)
- 表格：CARBON* / kgCO₂e/kg
- 表格：MATERIAL COST* / CNY / 288.66 m
- 表格：Q355B tube Ø80×4
- 表格：6.14
- 表格：50
- 表格：2.15
- 表格：18,394
- 表格：Q355B tube Ø80×3
- 表格：4.78
- 表格：50
- 表格：2.15
- 表格：13,983
- 表格：Engineered bamboo Ø80
- 表格：1.01
- 表格：0.22
- 表格：0.40
- 表格：10,158
- 表格：Treated timber Ø80
- 表格：0.85
- 表格：0.14
- 表格：1.10
- 表格：6,530
- 表格：Raw bamboo Ø80
- 表格：0.40
- 表格：0.18
- 表格：0.25
- 表格：4,330
- 表格：DURABILITY
- 表格：ENVIRONMENTAL ADAPTABILITY
- 表格：Protect steel coatings; treat bamboo; detail inspection and replacement.
- 表格：Check moisture, UV, wind exposure, local supply and plant suitability.

### 讲稿及答辩表述

- takeaway：Material screening includes mechanical and practical conditions, not only carbon.
- script：These are preliminary screening inputs.
- script：Each cost column assumes the same full member length; it is not the adopted unit budget.
- script：Steel offers much greater nominal bending capacity.
- script：Engineered bamboo is proposed for the crown, but stiffness, treatment and product-specific evidence are essential.
- script：Raw bamboo’s low reference cost does not remove its variability and maintenance issues.
- transition：These inputs motivate a hybrid strategy, with conditions attached.
- qa：Are these all verified design values?
- qa：No.
- qa：They are workbook screening inputs, and the bamboo identity and properties must be confirmed consistently.

## 06 — Why steel supports and an engineered-bamboo crown?

出处：

- Cost-Analysis.xlsx / 材料比选!A17:G18, A23:H24.
- Cost-Analysis.xlsx / 挠度校核!A21:G23 and A46:B46.
- Cost-Analysis.xlsx / 选型决策矩阵!A2:B2 and A28:B34; 规格与连接!A4:E5; 模块化建造分析!A3.

材料依据／限定：Workbook assigns steel to compression/wind-bending support role; tabulated EI steel145.2049 vs bamboo20.1062kN·m². Decision matrix requires feasibility gates in addition to scores. Row46 explicitly says 必须由结构同学出刚接节点详图并验算转动刚度 and the ≥3×simple-support assumption must hold. Five criteria follow the supplied rubric/workbook; no new performance result is claimed.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：MATERIAL DECISION
- 页面文字：Why steel supports and an engineered-bamboo crown?
- 页面文字：Match structural roles first; weigh cost and environmental inputs together with practical constraints.
- 页面文字：Design rationale P1/P3/P4.
- 页面文字：Screening values are preliminary; the hybrid strategy is not an optimised or certified structure.
- 页面文字：06
- 页面文字：STEEL • 12 GROUND-REACHING MEMBERS
- 页面文字：Prioritise stiffness and force transfer
- 页面文字：The workbook assigns steel to supports under compression and wind bending.
- 页面文字：Its tabulated section stiffness EI exceeds the proposed bamboo section.
- 页面文字：ENGINEERED BAMBOO • 47 CROWN MEMBERS
- 页面文字：Use material benefits where feasible
- 页面文字：The workbook adopts bamboo for the crown using cost and carbon inputs.
- 页面文字：It also requires restrained joints and verification of node rotational stiffness.
- 页面文字：DURABILITY
- 页面文字：Coat steel; protect and inspect bamboo.
- 页面文字：COST
- 页面文字：Include joints, installation and care.
- 页面文字：CONDUCTIVITY
- 页面文字：A material property, not a cooling result.
- 页面文字：CARBON
- 页面文字：Verify product factors and boundaries.
- 页面文字：ADAPTABILITY
- 页面文字：Check moisture, UV and local supply.
- 页面文字：Source decision: bamboo crown + steel supports; node rotational stiffness still requires verification.

### 讲稿及答辩表述

- takeaway：The material strategy follows structural roles and keeps feasibility conditions explicit.
- script：The workbook combines screening with a structural feasibility gate.
- script：Steel is assigned to supports under compression and wind bending.
- script：Bamboo is adopted for the crown using cost and carbon inputs, but the deflection sheet requires node rotational-stiffness verification.
- script：The lower cards summarise the five material criteria.
- script：Member-input savings do not establish a lower total unit cost.
- transition：The next check shows why crown stiffness makes the joints important.
- qa：Does the material screen establish a lower total unit cost?
- qa：No.
- qa：It compares equal-length member inputs.
- qa：The separate unit budget includes nodes, installation and care.
- qa：Low conductivity also does not establish a measured temperature benefit.

## 07 — The beam check sets a requirement for the joint

出处：

- Cost-Analysis.xlsx / 挠度校核!B6:B16, A21:G23, A31:J32, A46:B46.
- Cost-Analysis.xlsx / 模块化建造分析!A3.

材料依据／限定：Same simplified 6.65m solidØ80 bamboo member; E10GPa, wet foliage18kg/m² inputs; deflections100.5333873/20.1066775mm. Adopted6650/200=33.25mm; ratios3.02356 and0.60471. Node plate/sleeve/grout/adhesive/bolts are proposed in source, not verified restraint.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：CONNECTIONS
- 页面文字：The beam check sets a requirement for the joint
- 页面文字：Same member and loading assumptions; different ideal end restraints produce different deflections.
- 页面文字：P3 simplified beam check: self-weight + assumed 18 kg/m² wet foliage.
- 页面文字：E = 10 GPa and adopted L/200 need product/design confirmation.
- 页面文字：07
- 页面文字：SIMPLIFIED MEMBER: L = 6.65 m  ·  SOLID Ø80 mm
- 图表数据：Simply supported: 100.533387276407
- 图表数据：Adopted L/200 target: 33.25
- 图表数据：Ideal fixed ends: 20.1066774552815
- 页面文字：Simple support: 3.02 × target   |   Ideal fixity: 0.60 × target
- 页面文字：PROPOSED SUPPORT-HEAD NODE
- 页面文字：Plate + sleeve + adhesive + bolts
- 页面文字：Concept: restraint is not yet demonstrated.
- 页面文字：Next: verify joint rotation and whole-frame behaviour before claiming compliance.

### 讲稿及答辩表述

- takeaway：The adopted target is numerically between two ideal beam results; node verification is explicitly required by the workbook.
- script：The same six point six five metre bamboo-member calculation gives one hundred point five millimetres with simple supports and twenty point one with ideal fixed ends.
- script：The adopted target is thirty-three point two five millimetres, shown between them.
- script：This makes rotational restraint a design requirement to investigate.
- script：The proposed node does not prove that restraint, and the member check does not verify the whole frame.
- transition：The proposed node also has a significant budget allowance.
- qa：What must be verified next?
- qa：Product stiffness, node moment–rotation behaviour, load transfer and the whole frame under relevant loads.
- qa：The supplied workbook explicitly requires a node detail and rotational-stiffness verification.

## 08 — The unit budget includes fabrication, installation and care

出处：

- Cost-Analysis.xlsx / 造价明细, seven category totals and materials detail.

材料依据／限定：Seven-category sum 51,675.7187099CNY; materials30,549.3022975CNY; 12 nodes×1,000CNY=12,000CNY. All displayed prices remain estimates; component rows are included in total.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：BUDGET
- 页面文字：The unit budget includes fabrication, installation and care
- 页面文字：Preliminary total: CNY 51,676 per unit—not simply the price of the members.
- 页面文字：Source: Cost-Analysis.xlsx (P3).
- 页面文字：All rates remain reference estimates rather than confirmed quotations.
- 页面文字：08
- 图表数据：Materials: 30549.3022975
- 图表数据：Installation: 6050.0
- 图表数据：Other: 5679.6828674
- 图表数据：Fabrication: 5241.733545
- 图表数据：Maintenance: 2300.0
- 图表数据：Planting: 1165.0
- 图表数据：Transport: 690.0
- 页面文字：MATERIALS = 59.1% OF TOTAL
- 表格：KEY COMPONENT
- 表格：CNY
- 表格：Bamboo crown
- 表格：7,716
- 表格：Steel supports
- 表格：4,421
- 表格：12 rigid-head nodes
- 表格：12,000
- 表格：Counterweight
- 表格：3,402
- 页面文字：These component rows are part of the full total.
- 页面文字：Nodes are a larger allowance than the primary steel members.

### 讲稿及答辩表述

- takeaway：The budget makes the node trade-off visible.
- script：The preliminary total is approximately fifty-one thousand six hundred and seventy-six yuan.
- script：Materials are fifty-nine percent of this total; the other categories include fabrication, installation and care.
- script：Within materials, twelve proposed nodes account for twelve thousand yuan, more than the primary steel members.
- script：The component table is only part of the overall cost, not an additional total.
- transition：Next, the carbon and maintenance picture.
- qa：Are the node prices confirmed?
- qa：No.
- qa：They are the most uncertain allowance and need a defined detail and supplier quotation.

## 09 — Account for the members, base and maintenance needs

出处：

- Cost-Analysis.xlsx / 材料比选 carbon summary, adopted hybrid row.
- Cost-Analysis.xlsx / 模块化建造分析 and original report maintenance/interface proposals.

材料依据／限定：Adopted estimate: members1581.19629365 + base1088.64 + other150 =2819.83629365kgCO₂e; base38.61%. Factor boundaries not verified; no biogenic credit. Maintenance text follows protection/inspection proposals.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：CARBON & MAINTENANCE
- 页面文字：Account for the members, base and maintenance needs
- 页面文字：Current carbon estimate: approximately 2,820 kgCO₂e per unit.
- 页面文字：Workbook estimate (P3).
- 页面文字：Factor boundaries and node inclusion require checking; no biogenic-carbon credit is taken.
- 页面文字：09
- 图表数据：Primary members: 1581.19629365
- 图表数据：Counterweight: 1088.64
- 图表数据：Other components: 150.0
- 页面文字：≈ 2,820
- 页面文字：kgCO₂e / unit
- 表格：CONTRIBUTOR
- 表格：kgCO₂e
- 表格：Primary members
- 表格：1,581
- 表格：Counterweight
- 表格：1,089
- 表格：Other components
- 表格：150
- 页面文字：Counterweight ≈ 39% of the current estimate
- 表格：STEEL
- 表格：BAMBOO
- 表格：CONNECTIONS
- 表格：Protect coating
- 表格：Treat and inspect
- 表格：Check fixings and grout

### 讲稿及答辩表述

- takeaway：The estimate helps identify contributors and care responsibilities.
- script：The primary members and counterweight dominate the current carbon estimate.
- script：The counterweight contributes about thirty-nine percent, so foundation decisions also matter.
- script：We show the adopted estimate rather than claiming a verified life-cycle result.
- script：Outdoor performance also needs coating care, bamboo treatment and connection inspection.
- script：Product factors and the allowance for actual node materials still require checking.
- transition：Plant choice adds another set of requirements.
- qa：Is stored biological carbon deducted?
- qa：No.
- qa：It is not credited in this estimate, and factor boundaries are not yet fully aligned.

## 10 — Keep the planting mix conditional on the site

出处：

- Cost-Analysis.xlsx / 爬藤植物选择!A5:H7 and A14:B14.
- Cost-Analysis.xlsx / 模块化建造分析!A10:H10.
- Original analysis report §07 plant interface: 确认当地气候、攀附方式、根区、叶重、风荷载及落叶/落果维护.

材料依据／限定：Source identifies Parthenocissus tricuspidata as main, Combretum indicum companion, Campsis grandiflora alternative; proposes2+1 plants,1.2m³ substrate and drip. Local suitability/attachment are checks, not new verified botanical claims.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：PLANTING STRATEGY
- 页面文字：Keep the planting mix conditional on the site
- 页面文字：Source proposal: 2 Boston ivy + 1 Rangoon creeper per unit; trumpet creeper is an alternative.
- 页面文字：Project planting screen P3.
- 页面文字：Botanical traits, attachment and local suitability need site/nursery confirmation.
- 页面文字：10
- 页面文字：PRIMARY • 2 PLANTS
- 页面文字：Boston ivy
- 页面文字：Parthenocissus tricuspidata
- 页面文字：Deciduous: summer leaf cover, winter leaf loss.
- 页面文字：Adhesive tendrils; train and check grip on the support.
- 页面文字：COMPANION • 1 PLANT
- 页面文字：Rangoon creeper
- 页面文字：Combretum indicum
- 页面文字：Source role: companion; twining climber.
- 页面文字：Confirm local suitability and attachment to the proposed rods.
- 页面文字：ALTERNATIVE
- 页面文字：Trumpet creeper
- 页面文字：Campsis grandiflora*
- 页面文字：Vigorous woody climber; check roots, pruning demand and attachment.
- 页面文字：Confirm nursery species.
- 页面文字：ROOTS + CARE
- 页面文字：Source allowance: 1.2 m³ substrate, drip irrigation, training and pruning.
- 页面文字：Plant traits and quantities follow the workbook; local suitability and attachment require confirmation.

### 讲稿及答辩表述

- takeaway：The 2+1 mix is a project proposal, not a verified choice for every city.
- script：The material schedule proposes two Boston ivy plants and one Rangoon creeper.
- script：Boston ivy is deciduous, so a summer canopy should not be presented as year-round cover.
- script：The source lists Rangoon creeper as a twining companion and trumpet creeper as an alternative.
- script：Local climate and attachment still need checking, as required by the analysis report.
- script：Guides, irrigation and pruning are part of the planting design.
- transition：Next, the optical method used to evaluate shade.
- qa：Is this mix suitable for every city?
- qa：No.
- qa：The analysis report requires checking local climate, climbing method, root space and maintenance.

## 11 — Two shade metrics answer different questions

出处：

- Original project report and 分析参数与汇总.json: ideal continuous-leaf projection.
- Supplement D_Structure_and_Plant_Cover_Simulation.docx, §01–02; 数据/模拟参数与汇总.json.

材料依据／限定：Supplement formula Aeq=Abare+(1−tau)(Aleaf−Aoverlap), tau=.15 assumed; same5×5m target excludingr.75m. Ideal leaf-envelope overlap and equivalent direct-beam blockage have different definitions; neither is temperature or total solar attenuation.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：ANALYSIS METHOD
- 页面文字：Two shade metrics answer different questions
- 页面文字：30°N · assumed X=east/Y=north · true solar time 09–15 · same reference zone.
- 页面文字：Solar geometry: NOAA [3].
- 页面文字：Project methods/assumptions P2/P5.
- 页面文字：Reference zone is not net usable floor area; no temperature change is calculated.
- 页面文字：11
- 页面文字：01
- 页面文字：SUN DIRECTION
- 页面文字：02
- 页面文字：MODEL + LEAVES
- 页面文字：03
- 页面文字：SHADOW PROJECTION
- 页面文字：04
- 页面文字：TARGET INTERSECTION
- 页面文字：01  IDEAL LEAF-SHADOW OVERLAP
- 页面文字：Where could a continuous leaf envelope cast shade?
- 页面文字：Leaf-envelope shadow on target ÷ target area.
- 页面文字：Used for the ideal daily / solar-season result.
- 页面文字：02  EQUIVALENT DIRECT-BEAM BLOCKAGE
- 页面文字：How much direct beam do the frame and assumed leaves block?
- 页面文字：Accounts for frame/leaf overlap and assumed leaf transmittance τ = 0.15; used for sensitivity tests.
- 页面文字：COMMON TARGET: 5 × 5 m MINUS r = 0.75 m → 23.23 m²
- 页面文字：Compare results within the same metric and time window; do not add the two percentages.

### 讲稿及答辩表述

- takeaway：Identify the metric and time window before interpreting any percentage.
- script：The first metric measures ideal leaf-envelope shadow on the target.
- script：The second includes frame shadows, assumed leaf patches, their overlap and transmittance.
- script：We use the first for the daily and solar-season result, and the second for parameter and coverage comparisons.
- script：The target is shared, but the percentages are not interchangeable.
- script：Neither is a temperature reduction.
- transition：First, read the ideal daily result across the full time window.
- qa：What is the second formula?
- qa：Aeq = Abare + (1 − τ)(Aleaf − Aoverlap), then divide by the target area.
- qa：It is equivalent direct-beam blockage under the stated optical assumptions, not total solar-energy attenuation.

## 12 — A noon peak does not ensure all-day shade

出处：

- Original 04_图表与计算数据/01_原参数_C_D_典型时刻遮阴.csv and 02_原参数_C_D_15分钟遮阴曲线.csv, final-model rows.
- Original report §结论与依据; §07 application and §08 evaluation.

材料依据／限定：09/12/15 solstice overlap47.2/98.7/47.2%; 09–15 means75.3% solstice and49.8% equinox. Source advises seating by use time and reporting weakest periods; noon peak cannot describe the whole window.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：SHADE PERFORMANCE
- 页面文字：A noon peak does not ensure all-day shade
- 页面文字：Metric 01: ideal leaf-shadow overlap.
- 页面文字：Read the moving footprint and the full 09–15 window.
- 页面文字：Project projection data (P2, P5).
- 页面文字：Solar-season comparison under the assumed foliage geometry.
- 页面文字：12
- 页面文字：09:00
- 页面文字：47.2%
- 页面文字：12:00
- 页面文字：98.7%
- 页面文字：15:00
- 页面文字：47.2%
- 图表数据：09:00: 47.155661526250725
- 图表数据：None: 50.95515412268991
- 图表数据：None: 55.07011631579294
- 图表数据：None: 60.039564767330674
- 图表数据：10:00: 65.50654278454971
- 图表数据：None: 70.7723802048107
- 图表数据：None: 75.79576381742402
- 图表数据：None: 81.01882159676518
- 图表数据：11:00: 86.38341216660314
- 图表数据：None: 91.72295924019801
- 图表数据：None: 95.76669431441525
- 图表数据：None: 97.95178473599358
- 图表数据：12:00: 98.72481459764712
- 图表数据：None: 97.95178473599354
- 图表数据：None: 95.76669431441523
- 图表数据：None: 91.72295924019798
- 图表数据：13:00: 86.38341216660315
- 图表数据：None: 81.01882159676518
- 图表数据：None: 75.79576381742399
- 图表数据：None: 70.7723802048107
- 图表数据：14:00: 65.50654278454974
- 图表数据：None: 60.039564767330546
- 图表数据：None: 55.07011631579296
- 图表数据：None: 50.95515412269004
- 图表数据：15:00: 47.155661526250775
- 图表数据：09:00: 21.806368574443294
- 图表数据：None: 29.687120625398375
- 图表数据：None: 35.13483151321812
- 图表数据：None: 38.232603296876206
- 图表数据：10:00: 40.84379456356151
- 图表数据：None: 44.42122578139083
- 图表数据：None: 49.75245498148766
- 图表数据：None: 54.723445258224686
- 图表数据：11:00: 59.36744916873808
- 图表数据：None: 63.71937827724124
- 图表数据：None: 67.5361638686349
- 图表数据：None: 69.0650903902777
- 图表数据：12:00: 69.55856994686033
- 图表数据：None: 69.06509039027779
- 图表数据：None: 67.53616386863492
- 图表数据：None: 63.71937827724119
- 图表数据：13:00: 59.367449168738254
- 图表数据：None: 54.72344525822474
- 图表数据：None: 49.75245498148764
- 图表数据：None: 44.421225781390774
- 图表数据：14:00: 40.84379456356133
- 图表数据：None: 38.23260329687617
- 图表数据：None: 35.13483151321814
- 图表数据：None: 29.68712062539837
- 图表数据：15:00: 21.806368574443294
- 页面文字：09–15 TIME MEAN
- 页面文字：Solstice 75.3%
- 页面文字：Equinox 49.8%
- 页面文字：Design implication: check morning
- 页面文字：and afternoon seating exposure.

### 讲稿及答辩表述

- takeaway：Read the footprint and the whole time window, not only the noon peak.
- script：The solstice footprint overlaps about forty-seven percent of the target at nine and fifteen solar time, and almost ninety-nine percent at noon.
- script：The curve adds the intervening hours and an equinox solar case.
- script：Their means are about seventy-five and fifty percent.
- script：The noon peak therefore cannot stand for the whole use period: morning and afternoon exposure must be checked when placing seating.
- script：The equinox comparison changes solar conditions, not plant leaf cover.
- transition：We then change one geometric control at a time.
- qa：Does winter use the equinox result?
- qa：No.
- qa：Winter solar conditions and plant leaf states would need their own inputs.

## 13 — Expanding the crown raises mean blockage: 52.3% → 66.1%

出处：

- Supplement 数据/02_参数与生长覆盖_汇总.csv: Solstice, cover=.5, seven cases.
- Supplement 数据/00_结构参数与Rhino检查.json and report §01–02.

材料依据／限定：Expansion52.2795–66.1435%; height57.7692–62.6491%; corner59.0899–61.7752% (rounded). Largest tested max–min spread is expansion; this does not compare sensitivities per unit change. Source: a larger crown at equal cover percentage also requires more planted area; equal percentage does not imply equal material or plant inputs.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：GEOMETRY SENSITIVITY
- 页面文字：Expanding the crown raises mean blockage: 52.3% → 66.1%
- 页面文字：Metric 02: 09–15 mean blockage; one control at a time, 50% plan cover, solstice and τ = 0.15.
- 页面文字：Project parameter study (P5).
- 页面文字：Controls are not uniform scaling; larger cover percentage does not imply equal plant/material input.
- 页面文字：13
- 页面文字：SMALLER CROWN
- 页面文字：BASELINE
- 页面文字：LARGER CROWN
- 表格：CONTROL
- 表格：TESTED SETTINGS
- 表格：MEAN BLOCKAGE: LOW / BASE / HIGH
- 表格：Upper expansion
- 表格：0.92 / 1.08 / 1.24
- 表格：52.3% / 60.2% / 66.1%
- 表格：Upper-height control
- 表格：−0.4 / 0 / +0.4 m
- 表格：62.6% / 60.2% / 57.8%
- 表格：Corner factor
- 表格：0.55 / 0.85 / 1.00
- 表格：61.8% / 60.2% / 59.1%
- 页面文字：Wider crown → more planted area at the same cover percentage; input quantities are not held equal.

### 讲稿及答辩表述

- takeaway：The crown-width result is part of a broader seven-model parameter study.
- script：Seven cases change expansion, upper-height control or corner factor one at a time.
- script：At fifty percent cover, expansion changes mean blockage from fifty-two point three to sixty-six point one percent.
- script：The table retains the other results.
- script：The source report cautions that a larger crown at equal cover needs more planted area.
- script：These shade comparisons do not hold inputs equal or establish an optimum.
- transition：Next, keep the structure fixed and change foliage.
- qa：Does the height control shift the whole model by 0.4 metres?
- qa：No.
- qa：It is smoothly weighted; actual maximum heights must be read from the geometry records.

## 14 — Coverage amount alone does not determine useful shade

出处：

- Supplement 数据/02_参数与生长覆盖_汇总.csv: baseline Solstice cover0/.2/.5/.8/.95.
- Supplement 数据/05_相同50覆盖_分布敏感性.csv: cover=.5, solar time12.
- Supplement report §02: compare seat locations during occupied hours; same-cover spatial placement matters.

材料依据／限定：Mean blockage40.2187/48.6371/60.1972/67.9113/70.6955%;80→95 cover gives70.69545−67.91127=2.78418percentage points≈2.8pp. Noon patterns inner_spreading/dispersed/outer_first give77.4671/71.3662/62.6164%. These are distinct comparisons, not growth-time predictions.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：SPATIAL PLANT COVER
- 页面文字：Coverage amount alone does not determine useful shade
- 页面文字：Metric 02: fixed structure, five spatial-cover scenarios; 09–15 mean blockage under the same assumptions.
- 页面文字：Project spatial-cover calculation (P5).
- 页面文字：Frame/leaf overlap deducted, τ = 0.15; equivalent direct-beam blockage, not cooling.
- 页面文字：14
- 图表数据：0%: 40.21868884193895
- 图表数据：20%: 48.63711463942608
- 图表数据：50%: 60.19719328472306
- 图表数据：80%: 67.91126834429677
- 图表数据：95%: 70.6954503684305
- 页面文字：09–15 MEAN DIRECT-BEAM BLOCKAGE (%)
- 页面文字：PLAN COVER (%)
- 页面文字：80 → 95% cover adds only 2.8 pp here.
- 页面文字：VIEW SEQUENCE: 0 → 20 → 50 → 80 → 95% PLAN COVER
- 页面文字：Same 50% cover: noon blockage varies from 62.6% to 77.5%.
- 页面文字：Leaf location matters.

### 讲稿及答辩表述

- takeaway：The package tests both cover quantity and where that cover is placed.
- script：The curve separates plan cover from mean direct-beam blockage.
- script：Bare members already provide shade at zero leaf cover.
- script：From eighty to ninety-five percent cover, mean blockage increases by only two point eight percentage points in these scenarios.
- script：Separately, at the same fifty percent cover, the three layouts give noon blockage from sixty-two point six to seventy-seven point five percent.
- script：The supplied report therefore asks us to consider leaf location and occupied-hour seating, not coverage alone.
- transition：We connect that moving footprint to public use.
- qa：Why is 95% cover not 95% blockage?
- qa：Target intersection, frame overlap, leaf placement and transmittance all affect the metric.

## 15 — Put occupied-hour shade into the layout decision

出处：

- Original report §07 application scenarios and §08 evaluation/validation.
- Supplement report §02; fixed-cover daytime-shadow GIF and related CSV.

材料依据／限定：Source: compare seating during occupied hours; allow root/water/maintenance/circulation; measure shaded/unshaded environmental variables. No actual-street or measured-comfort result supplied.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：APPLICATION
- 页面文字：Put occupied-hour shade into the layout decision
- 页面文字：A rest node must coordinate seating, through movement, roots and a substantial base.
- 页面文字：Conceptual application P4; fixed-50%-cover projection P5.
- 页面文字：No real-site compliance or measured comfort result is claimed; method lead [4].
- 页面文字：15
- 页面文字：FIXED 50% PLAN COVER • SOLAR TIME 09:00 → 15:00
- 页面文字：01
- 页面文字：SEATING LOCATION
- 页面文字：Use the occupied-hour footprint, not just the crown outline or shadow centroid.
- 页面文字：02
- 页面文字：SPACE FOR ACCESS & ROOTS
- 页面文字：Allow for circulation, counterweight, root zone, irrigation and maintenance.
- 页面文字：03
- 页面文字：VALIDATE THE OUTCOME
- 页面文字：Confirm site and planting; compare radiation, temperature, humidity and wind.

### 讲稿及答辩表述

- takeaway：A practical layout must use the real occupied area, not only a reference square.
- script：The animation holds cover fixed while the sun moves.
- script：Seating should be checked during occupied hours, with room for circulation, the counterweight, roots and maintenance.
- script：The next verification step is a real-site assessment with simultaneous shaded and unshaded environmental observations.
- script：The current analysis does not establish net usable shaded floor area or a measured comfort improvement.
- transition：The last design link is construction organisation.
- qa：Are sensors a new project module here?
- qa：No.
- qa：This is the existing validation proposal, not a new monitoring-system design.

## 16 — Coordinate prefabricated modules and site interfaces

出处：

- Cost-Analysis.xlsx / 模块化建造分析!A3:H10 and labour/assembly sections.
- Cost-Analysis.xlsx / 造价明细 labour and counterweight entries.

材料依据／限定：Source modules: crown/supports/nodes/base/planting; grouting requires curing and changes reversibility. Base9072kg and labour14person-days are source estimates, not certified foundation or calendar programme.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：MODULAR CONSTRUCTION
- 页面文字：Coordinate prefabricated modules and site interfaces
- 页面文字：Numbered components help assembly; long members, heavy base and grouted joints constrain it.
- 页面文字：Project member/assembly and cost schedule (P3, P4).
- 页面文字：Proposed detail and labour quantities, not a tested construction programme.
- 页面文字：16
- 表格：MODULE
- 表格：WHAT IS PREPARED
- 表格：Crown
- 表格：47 formed/treatment-ready bamboo members
- 表格：Supports
- 表格：12 proposed galvanised steel members
- 表格：Connections
- 表格：Head nodes, sleeves, clamps and base flange
- 表格：Foundation
- 表格：Precast counterweight with anchorage
- 表格：Planting
- 表格：2 + 1 plants, substrate and drip provision
- 页面文字：01
- 页面文字：Prefab, treat & number
- 页面文字：02
- 页面文字：Lift base and set out
- 页面文字：03
- 页面文字：Support, align & assemble
- 页面文字：04
- 页面文字：Grout, cure & recheck
- 页面文字：05
- 页面文字：Plant, train & restore
- 页面文字：14 person-days estimated ≠ 14 calendar days.
- 页面文字：The ≈9.07 t base controls lifting; grouted nodes limit lossless reversal.

### 讲稿及答辩表述

- takeaway：The assembly work is more specific than a generic prefabrication claim.
- script：The proposal divides the system into crown members, supports, connections, base and planting.
- script：Numbering and preassembly help site organisation.
- script：However, the heavy counterweight governs lifting, and the sleeve-and-grout node requires curing and checks.
- script：The fourteen-person-day allowance is labour, not a calendar programme.
- script：A fully dry, losslessly reversible system should not be claimed.
- transition：Finally, our delivered work and its next checks.
- qa：Is the node a finished construction detail?
- qa：No.
- qa：Its geometry, stiffness, fabrication and quality controls need to be resolved together.

## 17 — Connect geometry, construction and useful shade

出处：

- P1 supplied Rhino/GH model; P3 workbook; P2/P5 analysis reports and datasets.
- Supplement 数据/01_参数与生长覆盖_时段结果.csv and native-model checks.

材料依据／限定：Work summary traces three supplied streams; seven parameter cases, five cover states and1750main result rows. Remaining checks reflect explicitly assumed inputs and unverified nodes/site conditions.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：WORK SUMMARY
- 页面文字：Connect geometry, construction and useful shade
- 页面文字：Three design workstreams now have traceable outputs.
- 页面文字：Synthesis of project records P1–P5.
- 页面文字：Product, joint and site-specific evidence are the next verification priorities.
- 页面文字：17
- 页面文字：GEOMETRY
- 页面文字：Rhino/GH model and parameters
- 页面文字：Final form, drawings and material take-off
- 页面文字：MATERIALS & BUILD-UP
- 页面文字：Screening, sections, budget and modules
- 页面文字：Proposed interfaces and implementation constraints
- 页面文字：PERFORMANCE
- 页面文字：Time-dependent shade and sensitivity
- 页面文字：Geometry, cover and spatial-distribution effects
- 页面文字：7 PARAMETER MODELS
- 页面文字：5 COVER STATES
- 页面文字：1,750 TIME-STEP RESULTS
- 页面文字：Next: confirm products and joints, check plant suitability, and test the real site.

### 讲稿及答辩表述

- takeaway：The contribution is a connected body of design work with a clear evidence boundary.
- script：The group delivers a parametric form and take-off, a proposed material and build-up strategy, and reproducible shade scenarios.
- script：The supplement adds seven parameter models, five cover states and seventeen hundred and fifty time-step results.
- script：These outputs make the design decisions traceable.
- script：Product data, joint behaviour, plant suitability and real-site performance are the next checks.
- script：Thank you.
- transition：We welcome your questions.
- qa：What can be stated most confidently?
- qa：The defined project geometry and the calculated shade scenarios under their explicit assumptions.

## 18 — References and project evidence

出处：

- Original analysis report bibliography entries for Watanabe etal2014, Hoelscher etal2016, NOAA and UTCI.
- User-provided project files P1–P5.

材料依据／限定：Bibliographic leads were supplied by the project; original-source checks remain pending. No DOI or new literature conclusion is invented.

### 页面表述

- 页面文字：GREEN BUILDING
- 页面文字：REFERENCES / Q&A
- 页面文字：References and project evidence
- 页面文字：Method sources and project inputs are separate; drawings, brief and schedules accompany the deck.
- 页面文字：Literature entries were supplied with project records; original-source checks remain pending.
- 页面文字：Unverified factors are not presented as certified standards.
- 页面文字：18
- 页面文字：[1] OUTDOOR SHADE & COMFORT
- 页面文字：Watanabe et al. (2014).
- 页面文字：Evaluation of outdoor thermal comfort in sunlight, building shade, and pergola shade during summer in a humid subtropical region.
- 页面文字：Building and Environment, 82, 556–565.
- 页面文字：[2] GREENING MECHANISMS
- 页面文字：Hoelscher et al. (2016).
- 页面文字：Quantifying cooling effects of facade greening: Shading, transpiration and insulation.
- 页面文字：Energy and Buildings, 114, 283–290.
- 页面文字：[3] SOLAR GEOMETRY
- 页面文字：NOAA Global Monitoring Division.
- 页面文字：General Solar Position Calculations.
- 页面文字：gml.noaa.gov/grad/solcalc/solareqns.PDF
- 页面文字：[4] COMFORT METHOD
- 页面文字：UTCI Calculator / COST Action 730.
- 页面文字：www.utci.org/utci_calc.php
- 页面文字：Method lead only; no project UTCI result is reported.
- 页面文字：PROJECT RECORDS
- 页面文字：P1 Model & take-off  •  P2 Ideal shade analysis  •  P3 Cost-Analysis.xlsx
- 页面文字：P4 Proposed design & build-up  •  P5 Parameter and spatial-cover simulation
- 页面文字：Project models, optical scenarios and estimates are identified separately from published literature.

### 讲稿及答辩表述

- takeaway：Source labels let the audience distinguish literature, project calculations and proposals.
- script：This is a reference and question page, not part of the planned spoken sequence.
- script：It identifies the literature leads and project evidence.
- script：Specific product parameters and standards still require original-source checks.
- transition：Return to the relevant result slide during questions.
- qa：Why are some data preliminary?
- qa：The supplied package contains assumptions and estimates that have not all been traced to product-specific or primary evidence.
