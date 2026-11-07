# 接手后的运行入口

已完成第一版模型与分析，未写整篇论文定稿。原START_HERE.md/CURRENT_STATE.json保留交接时状态；完成状态请看MODEL_STATUS.json。

建议阅读顺序：

1. docs/RESULTS_结果摘要.md：实际结果、组合交互、敏感性及适用限制。
2. docs/METHODS_模型与假设.md：闭合几何、四节点方程、辐射、控制与时间口径。
3. results/parameter_register.csv、config/base.json、config/geometry_v2.json：参数及证据身份。
4. results/review.html：离线图表总览，图片已内嵌，不访问外部网络。
5. results/checks.json、results/numerical_checks.csv：数值检查证据。

## 复现命令

在本目录中运行（Python 3.10+；本次版本记录见requirements.txt及results/runtime.json）：

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
export MPLCONFIGDIR="$PWD/.cache/matplotlib"
export OPENBLAS_NUM_THREADS=1
python verify_handoff.py
python model/run.py
python model/checks.py
python model/report.py
```

已有依赖时直接运行最后四条即可，模拟过程不需联网；只有安装依赖需要网络。Windows可用`.venv\Scripts\activate`并相应设置环境变量，源码无系统绝对路径。

`python model/run.py --base-only`仅运行16组基准，覆盖all_metrics及variants输出；要恢复完整320组与敏感性图，重新执行不带参数的命令。避免同时在同一输出目录运行基准与完整分析。敏感性变体在源码run_all定义、results/variants.json有快照。checks检验本版默认研究参数；若研究设计有实质修改，需相应更新测试设置及说明。

## 主要输出

| 文件 | 内容 |
|---|---|
| config/base.json | 可修改的基准控制及热参数 |
| config/geometry_v2.json | 闭合简化几何，不覆盖v1 |
| results/geometry_surfaces.csv | 各墙段毛面积、窗与实体墙面积、边界 |
| results/parameter_register.csv | 数值、单位、来源与假设身份 |
| results/hourly/*.csv | 两年四情景两工况共16份逐时结果 |
| results/base_metrics.csv | 基准16组峰值、OH/DH、显热量及开窗小时 |
| results/all_metrics.csv | 320组（含基准）汇总；敏感性逐时值按源码确定性复现 |
| results/variants.json | 20套输入（基准+19变体）的具体改动 |
| results/interactions.csv | 组合交互量，保留负值 |
| results/rankings.csv | 每套输入的四方案排序 |
| results/solar_internal_budgets.csv | 太阳得热分区及内部得热累计 |
| results/weather_summary.csv、weather_QA.json | 原始天气与时间一致性核对 |
| results/representative_week_*.json | 事先规定的最热168小时天气周 |
| results/figures | 几何、天气、代表周、对照、敏感性图 |
| results/checks.json | 物理与数值检查结果；不是实测校准 |
| results/review.html | 离线图表总览 |

逐时温度为小时内子步均值，peak_substep_C为小时内最高值；OH/DH以300秒子步计算，不从逐时均温再估算。night_window为该小时是否处于预定夜间窗口；vent1/2_fraction是实际开启比例。cool_W是该小时平均显热移除功率，求和除1000即kWh_th；理想制冷只控制Z1，自由运行cool_W恒为零。热流正值为得热或移热量的绝对量，详见方法方程。

原始资料的SHA-256仍可由verify_handoff.py验证。原MANIFEST只覆盖交接资料，新文件另见ANALYSIS_MANIFEST.json。不存在原始室温实测校准；不将热负荷写成实际电耗。外部参数文献仍需在论文定稿前核对。
