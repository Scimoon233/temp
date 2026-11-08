# Hangzhou Green Building course paper

当前英文课程论文及全部支撑资料的Git迁移快照，目标仓库为Scimoon233/temp，存放于green-building/。本目录包含全部研究交付物；远程推送状态应以GitHub实际分支为准。

## 当前版本

v1.4已修正Word、PDF与Markdown的热量单位下标，th以正式下标显示，正文仍为12 pt。沿用v1.3已统一标题、摘要与结论的研究对象，并用中英文机制—结果示意图替换旧柱状图，明确区分无空调过热与26°C理想显热需求。保留Jacobs参考文章的首页摘要区和双栏正文，英文稿含参考文献共3页，12 pt Times New Roman、单倍行距。数值结果不变。详见[摘要与图文摘要说明](01_Papers/English/摘要与图文摘要修改说明_v1.3.md)。

## 先看论文

- [英文论文PDF（含参考文献共3页）](01_Papers/English/Hangzhou_Passive_Cooling_Course_Essay.pdf)
- [英文论文Word](01_Papers/English/Hangzhou_Passive_Cooling_Course_Essay.docx)
- [英文论文Markdown](01_Papers/English/Hangzhou_Passive_Cooling_Course_Essay.md)
- [中文审阅版](01_Papers/Chinese_Reading/杭州住宅被动降温_英文短稿对应中文版.md)
- [交付总览](00_交付总览.md)

## 范围及真实进度

研究主题：杭州夏季住宅外遮阳与夜间通风对自由运行过热及理想显热制冷需求的影响。居住区41.1 m²、阳台6.3 m²、高度2.7 m；两热区四节点RC模型，2025/2026年天气，S0—S3四情景。

已完成320组主分析及112次补充复核、诊断和结构对照；模型未实测校准。英文课程稿采用Times New Roman 12 pt、单倍行距，包含参考文献共3页。中文4页版仅供审阅。历史14页中文稿为技术背景，不可误作课程提交稿。显热kWh_th不等于实际电耗。

## 目录

01_Papers为最新中英文短稿；02_Figures为支撑图；03_Reproducible_Project/Hangzhou_Codex_Handoff为保留原相对路径的完整研究项目；04_Format_Reference为Jacobs等的格式参考PDF及来源；05_Supporting_Documents为中文方法、结果、大纲与核查记录。

## 复现

进入03_Reproducible_Project/Hangzhou_Codex_Handoff，按README_RUN.md安装依赖并运行。进一步核查paper_draft/SOURCE_AUDIT.md和results/draft_diagnostics。当前稿件没有通过学校查重，不承诺相似率为零。

## 完整性

OUTPUT_MANIFEST.json为已整理交付文件清单；MIGRATION_CHECKS.json记录本次快照与来源逐文件比对结果。迁移采用复制，原环境资料保留。

## 大文件恢复

中英文课程论文、全部模拟资料及Jacobs正式发表版PDF均直接可见。仅25 MB的Jacobs接受稿因上传接口单次16 MiB限制，以三个原始二进制分块保存。进入本目录运行`python restore_large_reference.py`即可恢复原PDF；脚本验证每块及完整文件的SHA-256，无网络依赖。原始资料和清单中的内容未删减或改写。
