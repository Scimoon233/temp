# 汇报可读性、讲述支持与证据链审查

状态：基于已收到的旧项目包、Cost-Analysis.xlsx、新参数与覆盖情景包及现有大纲审查。未成功读取超过32MiB的整包更新，因此不能假定其中还有材料或引用修正；新模拟包已读取。尚未制作完整正式PPT或完成排练，结论是内容审查，不是版面或工程验收。

## 一、总体判断

当前可以形成有依据的课程概念设计汇报，核心证据为项目几何、明确假设下的遮阴投影和空间覆盖敏感性。还不能包装成已经完成结构优化、抗风验证或实测热舒适改善的工程成果。

缺少实体实验不等于几何情景分析不能展示。应按实际证据分别使用“项目模型数据”“情景计算”“初步估算”“设计意图”，不能把计算一致性升级成现实性能认证。

## 二、页面如何真正帮助汇报者

- 建议采用19页（18页主讲＋1页参考备份）；两种模拟分开，不把变量和指标挤进一页。19页是当前建议，不将用户尚未确认的调整冒称已确认。
- 每页一个结论、一幅主图或一个组合图；普通页正文约25—40英文词，表格页例外。字数只是辅助，图表标签数量、行长和观看距离也要检查。
- 讲述顺序由画面决定：先标题结论，再从左到右看图，最后一句意义。页面不能要求汇报者在多张图和多个数据表之间来回解释。
- 三个作用不同的条件分别放对应页：结构是假定节点、成本是估算、模拟是情景。其他限制留备注，不在每页重复长段免责声明。
- 重要来源和关键条件就地显示；引用和必要假设不能因精简而消失。
- 每页备注统一包含：核心结论一句、看图顺序（最多三步）、英文口述建议、前后页衔接、最可能的问题及有依据的回答。完整公式、来源状态和备选数据放备注，不能用小字塞在主页面。
- 演讲稿使用短句，通常一个呼吸一句；技术名词首次出现解释，不连续堆ideal overlap、equivalent blockage、LAI、Tmrt、UTCI。
- 页面13—15尽量统一配色、单位和参考区，明确指标变化；先展示两种指标定义，不让听众误以为98.7%和91.4%互相矛盾。
- 全程主讲约8分45秒—9分钟的目标尚需英文讲稿与排练验证；不能只按页数或每页词数宣称时间已达标。

## 三、逐项证据审查与展示处理

| 论点/内容 | 当前依据 | 缺失或逻辑跳步 | 正式展示处理 |
| --- | --- | --- | --- |
| 最终几何、数量、冠幅和高度 | 3dm、参数JSON、几何图与项目取量记录 | 本轮未在Rhino独立验证全部实体与杆长；建模有效不等于制造/施工有效 | 保留为项目模型数据，尺寸适度取整，不声称独立测量或认证 |
| 遮阴范围与逐时变化 | 可追溯CSV、投影方法、图表；新旧连续叶面基准吻合 | 场地、朝向、叶面与太阳输入是假设，无周边遮挡 | 主证据保留，结论限于本设定的参考区 |
| 冠幅和植物覆盖敏感性 | 1750行结果公式、70组积分均值与35组覆盖记录核对一致；有代码、模型 | 本轮未完整重算几何或原生运行Rhino；实际叶面/光学未测 | 保留情景比较；不称实测、真实生长模拟或优化证明 |
| 结构已经优化、最终方案最优 | 有参数对比，未见完整结构优化目标与过程 | 没有结构求解、应力/屈曲/整体稳定、约束、多目标搜索与最优性证据 | 删除“structurally optimised/optimal”作为已完成结论；改为parametric structural concept / parameter study |
| 竹冠在实际结构中满足挠度与承载 | 简支与理想固接单梁表，参数取值尚待补证 | 47根冠杆的真实约束、交叉连接与12处节点如何形成全结构刚度没有闭合证明；理想固接并非已实现 | 图标题写simplified boundary-condition check；说明固定端结果是假定，不写“structure passed” |
| 12个节点实现≥3倍刚度 | 方案文字和理想边界计算 | 无节点详图、转动刚度、试验或可信节点模型；胶层、套管与螺栓组合未验证 | 节点为proposed detail；“需实现的刚度条件”，不是既成刚度 |
| 支撑必须用钢、全竹必然失败 | 材料截面承载估算，表内引用约1.5kN·m需求 | 未见该需求的完整荷载/内力推导、长细比和屈曲验算 | 保留“proposed steel supports”，不宣称唯一可行材料或安全一票否决已有完整证明 |
| 配重抗倾覆与抗台风 | 假定风投影、配重体积与质量等 | 无完整风荷载路径、植被阻力、基础/地面承载、滑移与倾覆组合验算 | 配重作为待校核方案；删除“typhoon-resistant”“overturning verified” |
| 开敞侧界/中央孔改善通风 | 几何开放和一般机制推理 | 无场地来风、风阻模型、CFD或风速对照；孔洞不证明烟囱效应 | 只称保留气流通路的意图；一张概念图，短注not simulated |
| 实际降温、热舒适提高 | 研究动机与一般文献；几何遮阴结果 | 无辐射/气温/湿度/风的有效环境结果、Tmrt/UTCI或对照测量 | 写aims to reduce solar exposure；不写确定温降或已提升的舒适指数 |
| 竹材物性及选型优势 | 工作簿输入 | glubam与scrimber身份混用；f、E、密度、λ和碳因子缺统一产品证据 | proposed engineered bamboo；数字为preliminary；不把单材料属性泛化成系统优势 |
| 低导热所以竹材表面接近气温/不会伤植物 | λ的参考比较 | 表面温度还由太阳吸收、长波、风、湿度和热惯性决定，无表面测量 | 删除因果跳步；如保留只比较conductivity，不能断言表面安全 |
| 碳排约2820kgCO₂e | 工作簿主体、配重、其他构件求和 | 竹因子、钢处理、节点计入、生物碳及系统边界未核齐 | preliminary estimate；不能叫经认证A1–A3、全生命周期碳或最优碳方案 |
| 造价约51676CNY | 工作簿七类成本汇总算术一致 | 无实际报价，节点1000CNY/处最不确定；全额范围需统一 | preliminary budget；无需向听众逐条朗读单价，不声称已报价或经济最优 |
| 材料20年以上寿命、竹5—8年周期 | 源稿经验描述 | 缺实际产品、涂层厚度、暴露环境与维护依据 | 改为需防腐/定期复检等维护要求；删除保证年限 |
| 植物适生、湿重、LAI与生长周期 | 候选植物清单、未核量级输入 | 物种、气候、苗木与维护条件未验证；不应把覆盖标签配成年份 | 标proposed candidates；缺依据的年限/数值不作结论 |
| 预制与装配便捷、14人工日 | 模块与十步工序估算 | 新旧销接/刚接文字冲突；运输/吊装/养护尚无实操记录，人工日不是日历工期 | 方案流程可展示；14 person-days estimated；不称validated rapid installation |
| 完全干式、免焊、无损可逆 | 早期方案文字 | 与当前灌浆刚接及加工描述冲突 | 不作为当前卖点；说明可拆换性须由节点细化确认 |
| 遮住参考区等于座位实际可用 | 固定5×5m减中心圆的计算区、概念座椅图 | 真实配重/花池/根区/座椅占用与目标区未统一，尚非实际座位遮阴评估 | 使用reference zone，不称net usable shaded area；布置图为illustrative |

## 四、讲述的三类措辞

### 可以明确说

- “The project model contains 59 members.”（来源为项目模型）
- “Under the stated assumptions, increasing crown width raises equivalent direct-beam blockage in the reference zone.”
- “The scenarios account for overlapping frame and foliage shadows.”

### 应限定后再说

- “The fixed-end result illustrates the stiffness required; actual joint restraint has not been verified.”
- “The preliminary unit budget is approximately CNY 51,676.”
- “Open sides are intended to retain airflow paths; no wind-field simulation is claimed.”

### 当前不应说

- “The structure is optimised and safe.”
- “The canopy improves ventilation and reduces air temperature by …”
- “The plants reach 95% cover in year …”
- “The system is fully reversible / typhoon-proof / maintenance-free.”
- “Lower thermal conductivity proves that the bamboo stays near air temperature.”

## 五、对页面的具体处理

1. 成员页用短语忠实概括，姓名与职责完整；原图文字保留在配套文档/备注，不照贴长表。
2. 第5—6页解释材料角色与初步筛选，不做“钢已安全、竹已验证”的排名或通过标记。
3. 第7页标题建议Boundary Conditions Govern Deflection。只看两柱图和必要约束，不用绿色大勾表示实际结构过关。
4. 第9页碳总量标Preliminary，不把估算范围包装为已核全生命周期边界。
5. 第11页标题建议Open Sides and a Porous Crown；意图图不画暗示强抽风的粗上升箭头。
6. 第12页先说明两种指标，公式和完整假设不主讲；第13页只说理想几何重合，第14—15页只说等效直射阻断。
7. 第14页以相同覆盖和时间条件比较冠幅，提醒更大不等于最优；第15页以相同结构比较覆盖，不讲未校准年限。
8. 第16页应用图不称真实场地或合规图；第17页区分person-days和days，灌浆养护不能隐藏。
9. 第18页结论统一收束为参数化结构概念、条件下的遮阴潜力、待验证的材料与实施方案；不在最后升级为“已实现热舒适改善”。

## 六、每页备注给汇报者的标准帮助

每页5项：

1. 一句Takeaway（听众需要记住什么）。
2. 看图顺序（指哪一处、解释哪个数字）。
3. 英文口述（按总时长预算，短句、能自然说出来）。
4. Transition（自然引到下一页）。
5. Q&A（一个最可能问题、一个不夸大证据的回答）。

示例：植物覆盖页

Takeaway：Useful blockage increases with cover in the assumed scenarios.

看图顺序：先看0%裸架，再看50%和95%，最后说明三个数都是时段平均等效直射阻断率。

口述草稿：The frame already blocks some sunlight before foliage develops. Holding the structure fixed, our assumed cover scenarios give mean direct-beam blockage of about forty, sixty and seventy-one percent. These are spatial cover scenarios, not a timetable for real plant growth.

Transition：We then use the occupied-hour shade footprint to organise seating and circulation.

Q&A：How long does it take to reach 95% cover? Answer：We have not calibrated a growth duration. That requires species, site and maintenance evidence.

以上只是备注形式示例，非已完成或排练验证的全套讲稿。

## 七、优先需要补证的项目

A. 影响方案成立：工程竹产品和参数；节点刚度及整体稳定；植被风荷载与配重/基础。
B. 影响数值可信度：材料碳因子边界与节点计入；实际报价；真实植物分布/透射及场地。
C. 不补也可作为明确设计意图展示：通风、维护、概念布置与施工流程，但不能写成实验结果。

课程展示仍可继续；应把可信计算放在叙事中心，未闭合内容明确为方案或下一步，而不是用更多小字解释一个过强结论。
