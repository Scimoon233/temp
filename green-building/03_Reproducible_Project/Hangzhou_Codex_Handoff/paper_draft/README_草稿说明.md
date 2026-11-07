# 论文草稿 v0.1

正文：杭州住宅被动降温研究_论文草稿_v0.1.docx；PDF版便于预览；Markdown版便于修改及差异比较。

本稿含摘要、引言、相关研究、对象与数据、数学方法、结果、讨论、结论、参考文献和附录，含8张表、9幅图。正文数值来自已保存结果自动生成，不含实测校准。作者、课程信息和指定引用样式尚未加入。

## 本轮按阶段完成的工作

| 阶段 | 已完成内容 | 结果位置 |
|---|---|---|
| 热量诊断 | 四情景两工况分区热流账目、正负与净累计、零太阳／零内部得热诊断 | results/draft_diagnostics/*ledger.csv、energy_budgets.csv、metrics.csv |
| 关键假设 | 阳台玻璃顶部0.5／1.0 m理想挑檐、隔断耦合半倍／双倍、较低得热与二次透入联合对照 | cases.json及正文表8 |
| 参数核查 | BASIX官方item5、Hou作者稿Table6、Short正文16.7含义、天气官方时标 | SOURCE_AUDIT.md |
| 模型核验 | 扩展模型基准再现、节点与分区收支、区间交换抵消、新工况步长收敛 | results/draft_diagnostics/checks.json |
| 结果整合 | 保留已跑320组主参数分析，新增112次复核／诊断／对照运行 | 原all_metrics.csv与补充metrics.csv |
| 论文草稿 | 已形成完整章节及实际图表，保留模型边界与未校准身份 | 本目录Word／PDF／Markdown |

112次补充运行包括96次（6套输入×两年×四情景×两工况，其中16次是基准再现）、8次零热源诊断、8次150秒步长复核。它们不应全部当作互不重复的新设计方案。

## 本轮选择

保留第一版透明参考基准；没有实测遮挡或住户时序依据，因此不以温度降低为目标重定基准。新增挑檐只削减阳台玻璃直射，采用无限宽顶部外侧挑檐近似，不是实测阳台构件，也没有完整计算散射遮挡。所有四情景在各对照内使用相同既有构件。

内部得热16.7 W/m²为原文模型假定，不是实测峰值。整窗和ACH数值已核对原始发布表，但转用本住宅仍为代理；高低时段、有效热容量及二次透入都是研究假设。阳台二次太阳输入与温差传热需分开：参考S0中，季节温差传热净方向由居住区流向阳台，同时有阳台二次太阳透入居住区。

诊断账目中solar为分配后热量，direct_window／secondary_solar仅用于分解Z1，不应将它们与solar重复相加；air_to_mass是区内交换，不是外部热源。正流量为入区，cooling与storage按正移热／储能增量定义，残差为前六热源项之和减storage和cooling。

## 复现

在项目根目录、安装依赖后：

```bash
export MPLCONFIGDIR="$PWD/.cache/matplotlib"
export OPENBLAS_NUM_THREADS=1
python model/draft_analysis.py
python model/write_draft.py
python model/export_draft_pdf.py
```

主分析若需从头复现，先按README_RUN.md运行run.py、checks.py与report.py。草稿额外依赖见requirements_draft.txt。所有代码以文件位置定位项目，不依赖原工作区绝对路径。

下一轮修改可优先围绕主假设依据、论述逻辑和篇幅，而不是删去高温或不利结果。PDF是对Markdown的独立排版，Word为可编辑版本；两者分页可能不同。
