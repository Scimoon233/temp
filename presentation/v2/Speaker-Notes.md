# VineWeave Canopy — V2 draft spoken notes

Not rehearsed. Takeaways, Q&A and Chinese cues are not part of the timed talk.

## Slide 1: VineWeave Canopy

VineWeave Canopy combines climbing plants with a tree-like support to provide pedestrian shade. Our group connects parametric geometry, material and construction choices, and shading analysis. The names below identify our responsibilities. We will explain both the design decisions and the evidence supporting them.

Transition: First, the design brief.

Q&A: Where are the full roles? The cover retains the core allocation; the planning document records the complete supplied descriptions.

## Slide 2: Translate the brief into five design decisions

The brief asks for more than a tree-like form. We connect materials, geometry, environmental performance, planting and assembly. This table shows the response and the work produced for each requirement. Shade has been calculated under explicit assumptions; airflow and real thermal comfort remain design and validation questions.

Transition: We begin with the model-building process.

Q&A: Does every row have an experiment? No. We distinguish model outputs, calculated scenarios, preliminary estimates and design proposals.

## Slide 3: From controlled centre lines to a measurable model

We start with centre lines, shape the crown and rebuild the members in Rhino. Grasshopper retains the fixed centre lines for pipe-radius control. Shape changes require the separate reconstruction method. We then extract dimensions and generate the analysis envelope.

Transition: Next, the spatial roles of the crown.

Q&A: Can the existing GH slider change every parameter? No. The delivered fixed-centreline GH controls pipe radius; crown-shape experiments use the reconstruction method.

## Slide 4: Let the crown, opening and edges perform different roles

The interwoven crown supports a proposed climbing envelope. The central leaf opening is explicitly assumed in the shade analysis, rather than measured from real plants. Maintaining it may require pruning. Around the support, an open edge preserves circulation and access. These roles explain the layout without claiming a proven ventilation gain.

Transition: Material assignment follows the member roles.

Q&A: Is the reference area fully usable? Not yet; actual foundation, roots, seating and access still need to be coordinated.

## Slide 5: Separate the support role from the crown role

The take-off gives twelve ground-reaching supports and forty-seven crown members, with a total centre-line length of two hundred and eighty-eight point six six metres. We propose an eighty-by-four millimetre steel tube for supports and solid engineered bamboo for the crown. This is a material strategy, not proof that either zone is safe.

Transition: We compare the screening inputs behind it.

Q&A: Does the exterior model contain the final wall thickness? No. The pipe exterior and proposed material section must be distinguished.

## Slide 6: Screen strength, cost, carbon and outdoor care together

These are preliminary screening inputs. Each cost column assumes the same full member length; it is not the adopted unit budget. Steel offers much greater nominal bending capacity. Engineered bamboo is proposed for the crown, but stiffness, treatment and product-specific evidence are essential. Raw bamboo’s low reference cost does not remove its variability and maintenance issues.

Transition: Crown stiffness leads directly to the connection question.

Q&A: Are these all verified design values? No. They are workbook screening inputs, and the bamboo identity and properties must be confirmed consistently.

## Slide 7: The crown is stiffness-sensitive: joints matter

The workbook applies self-weight and an assumed wet-foliage load. At the six point six five metre span, the simplified deflection changes from about one hundred millimetres under simple supports to twenty under ideal fixed ends. The adopted limit is thirty-three point two five millimetres. Actual joint and whole-frame stiffness still require verification.

Transition: Connection complexity also affects the budget.

Q&A: Do twelve nodes fix every crown member? That has not been demonstrated. Joint rotation and global load transfer still require modelling or testing.

## Slide 8: The unit budget includes fabrication, installation and care

The preliminary total is approximately fifty-one thousand six hundred and seventy-six yuan. Materials are fifty-nine percent of this total; the other categories include fabrication, installation and care. Within materials, twelve proposed nodes account for twelve thousand yuan, more than the primary steel members. The component table is only part of the overall cost, not an additional total.

Transition: Next, the carbon and maintenance picture.

Q&A: Are the node prices confirmed? No. They are the most uncertain allowance and need a defined detail and supplier quotation.

## Slide 9: Account for the members, base and maintenance needs

The primary members and counterweight dominate the current carbon estimate. The counterweight contributes about thirty-nine percent, so foundation decisions also matter. We show the adopted estimate rather than claiming a verified life-cycle result. Outdoor performance also needs coating care, bamboo treatment and connection inspection. Product factors and the allowance for actual node materials still require checking.

Transition: Plant choice adds another set of requirements.

Q&A: Is stored biological carbon deducted? No. It is not credited in this estimate, and factor boundaries are not yet fully aligned.

## Slide 10: Select climbers for support, season and maintenance

The source screen considered eight climbers. It proposes Boston ivy as the primary plant, Rangoon creeper as a companion, and trumpet creeper as an alternative. The unit allowance is two ivy plants, one creeper, substrate and drip irrigation. The mix remains subject to local suitability and attachment checks.

Transition: Plant choice raises the question of when shade becomes available.

Q&A: Is Rangoon creeper confirmed for the site? No. Climate, winter survival and leaf habit must be checked before adopting the mix.

## Slide 11: Opening the structure is not the same as a mature canopy

There are two readiness gates. The structure can open only after the required acceptance conditions, while vegetation must reach an agreed shade target during occupied hours. The provided cover scenarios have no growth durations. We therefore show the sequence without invented months or years. Nursery starting size, species, climate and maintenance data are needed to estimate when the target can be met.

Transition: We next separate the environmental mechanisms.

Q&A: How long until full use? The current evidence does not support a month estimate. Structural acceptance and vegetation shade readiness must be assessed separately.

## Slide 12: Different mechanisms need different evidence

Shading is the mechanism directly analysed. Plant evapotranspiration depends on water and weather. Open sides retain potential airflow paths, but denser foliage may also add resistance. These mechanisms explain the design intent; they do not prove a temperature reduction, chimney effect or improved wind speed in this canopy.

Transition: Here is how the shade metrics are calculated.

Q&A: Are the dashed arrows simulation results? No. They are a conceptual explanation of the proposed open layout.

## Slide 13: Project shade onto one fixed reference zone

We project the geometry along the solar direction and intersect it with the same target. The fixed target excludes a central disk. Ideal overlap uses a continuous leaf envelope. Equivalent blockage includes opaque frame shadows and assumed leaf transmittance, with overlap deducted. The two metrics are different, and neither is a temperature change.

Transition: First, the ideal time-dependent result.

Q&A: Was numerical resolution checked? The supplied package includes raster spot checks; five versus two-point-five millimetre results differ by up to about 1.06 percentage points in those samples, not as an overall error bound.

## Slide 14: The shadow position and solar season both matter

The solstice footprint overlaps about forty-seven percent of the target at nine and fifteen solar time, and almost ninety-nine percent at noon. The curve adds the intervening hours and an equinox solar case. Their means are about seventy-five and fifty percent. This is a comparison of solar conditions under hypothetical foliage, not a seasonal growth forecast.

Transition: We then change one geometric control at a time.

Q&A: Does winter use the equinox result? No. Winter solar conditions and plant leaf states would need their own inputs.

## Slide 15: Seven models test three geometry controls

The work includes width, upper-height control and corner factor, with a shared baseline. At fifty percent cover, mean blockage rises from fifty-two point three to sixty-six point one percent as the crown expands. The table records the other controls too. These are controlled shade comparisons, not proof of an optimum or of structural safety after changing geometry.

Transition: Next, keep the structure fixed and change foliage.

Q&A: Does the height control shift the whole model by 0.4 metres? No. It is smoothly weighted; actual maximum heights must be read from the geometry records.

## Slide 16: Coverage amount alone does not determine useful shade

The five plan-cover states give mean blockage of about forty, forty-nine, sixty, sixty-eight and seventy-one percent. Bare members already provide shade at zero leaf cover. At the same fifty percent cover, three spatial layouts also produce different noon results. Coverage percentage therefore does not describe where useful shade falls, and the stages do not predict biological growth duration.

Transition: We connect that moving footprint to public use.

Q&A: Why is 95% cover not 95% blockage? Target intersection, frame overlap, leaf placement and transmittance all affect the metric.

## Slide 17: Put occupied-hour shade into the layout decision

The animation holds cover fixed while the sun moves. Seating should be checked during occupied hours, with room for circulation, the counterweight, roots and maintenance. The next verification step is a real-site assessment with simultaneous shaded and unshaded environmental observations. The current analysis does not establish net usable shaded floor area or a measured comfort improvement.

Transition: The last design link is construction organisation.

Q&A: Are sensors a new project module here? No. This is the existing validation proposal, not a new monitoring-system design.

## Slide 18: Coordinate prefabricated modules and site interfaces

The proposal divides the system into crown members, supports, connections, base and planting. Numbering and preassembly help site organisation. However, the heavy counterweight governs lifting, and the sleeve-and-grout node requires curing and checks. The fourteen-person-day allowance is labour, not a calendar programme. A fully dry, losslessly reversible system should not be claimed.

Transition: Finally, our delivered work and its next checks.

Q&A: Is the node a finished construction detail? No. Its geometry, stiffness, fabrication and quality controls need to be resolved together.

## Slide 19: Connect geometry, construction and useful shade

The group delivers a parametric form and take-off, a proposed material and build-up strategy, and reproducible shade scenarios. The supplement adds seven parameter models, five cover states and seventeen hundred and fifty time-step results. These outputs make the design decisions traceable. Product data, joint behaviour, biological establishment and real-site performance are the next checks. Thank you.

Transition: We welcome your questions.

Q&A: What can be stated most confidently? The defined project geometry and the calculated shade scenarios under their explicit assumptions.

## Slide 20: References and project evidence

This is a reference and question page, not part of the planned spoken sequence. It identifies the literature leads and project evidence. Specific product parameters and standards still require original-source checks.

Transition: Return to the relevant result slide during questions.

Q&A: Why are some data preliminary? The supplied package contains assumptions and estimates that have not all been traced to product-specific or primary evidence.
