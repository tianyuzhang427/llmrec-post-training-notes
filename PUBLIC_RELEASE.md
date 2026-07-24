# 公开发布边界

本仓库按公开研究复盘维护。除明确列出的 ActionSelect 104 文件外，不分发比赛数据或第三方数据行，也不主张拥有相关数据的再分发权。

## 包含

- 已记录的线上评测分数；
- 六类数据资产的数据卡与公开 manifest；
- 不含真实内容的合成结构样例；
- 104 条精心构建的 ActionSelect 训练数据；
- LogicChain → ActionSelect 的独立投影代码；
- optimizer-step 本地 replay 的聚合统计图；
- 发布前静态检查脚本。

## 不包含

- ActionSelect 104 以外的原始或处理后比赛数据；
- CEval、Math23K 等第三方数据行；
- 真实用户历史、caption、itemic token 映射或评测 prompt；
- 模型权重、LoRA adapter、embedding、索引和原始平台日志；
- API key、endpoint、账户信息或本地绝对路径。

除下述 ActionSelect 104 外，每位使用者必须从原始提供方获取数据，并遵守对应许可和比赛规则。Manifest 中的来源名称和行数只用于说明数据 lineage，不代表授予数据再分发权。

## ActionSelect 104 的来源

`data/actionselect/actionselect_104.jsonl` 的上游来源是比赛官方提供的 seed dataset，具体使用其中的用户历史记录。该文件不是官方原始标签的直接副本，而是我在可见用户历史上完成主题提取、Teacher/Judge 筛选和 ActionSelect 标签构造后得到的派生训练数据。

引用或继续使用该文件时，请同时注明：

- 上游来源：比赛官方 seed dataset 的用户历史部分；
- 派生来源：本仓库的 ActionSelect 104 构建流程；
- 使用边界：仍需遵守原比赛规则及上游数据约束。

仓库公开提供该派生文件及其复现说明，但不代表我对上游比赛数据进行了重新许可。

## 结果表述

- 分数来自单次线上评测，不是多 seed 均值；
- 多因素运行不能用于证明单个因素的因果收益；
- 约 `0.01` 以内的单次变化在未重复前只作为候选信号；
- 104 条精心构建的 ActionSelect 数据有一轮小幅正观测；
- Math Diversity Delta 尚无线上单变量结论。

## 软件许可

本初步打包目录暂未附加软件许可证。公开可见不自动等于获得复制、修改或再许可授权。
