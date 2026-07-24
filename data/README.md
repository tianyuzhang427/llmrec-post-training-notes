# 数据资产

本目录维护六类数据资产的说明。除从比赛官方 seed 用户历史派生的 `actionselect/actionselect_104.jsonl` 外，其余目录不包含比赛或第三方真实数据行。

每个子目录至少包含三个文件：

- `README.md`：任务内容、规模和证据边界；
- `manifest.json`：公开 lineage 与统计；
- `example.jsonl`：一条合成结构样例，不可用于训练或评测。

LogicChain → ActionSelect 额外提供独立构建代码；ActionSelect 额外提供完整的 104 条训练数据。真实数据的使用边界见 [PUBLIC_RELEASE.md](../PUBLIC_RELEASE.md)。

| 数据资产 | 正式版本 | 规模 | 样例 / 数据 |
| --- | --- | ---: | --- |
| [CEval-Letter](ceval-letter/README.md) | `understanding_world_ceval_letter_no_think` | 13,948 | [在数据卡中查看](ceval-letter/README.md#合成样例) |
| [懂世界 Math](math/README.md) | Math23K + Math Plus | 21,799 + 21,799 | [构建、来源与样例](math/README.md) |
| [Half Video](half-video/README.md) | `seed_recommend_video_diverse_half_v1` | 19,204 → 11,770 | [在数据卡中查看](half-video/README.md#合成样例) |
| [LogicChain → ActionSelect](logicchain-to-actionselect/README.md) | `logicchain_to_action_select_direct_v0` | 1,298 | [提取方法与代码](logicchain-to-actionselect/README.md#怎么提取) |
| [自构造 ActionSelect](actionselect/README.md) | `user_history_r2_action_select_refined_104_v5` | 104 | [完整 JSONL](actionselect/actionselect_104.jsonl) |
| [Caption2Token](c2t-sa/README.md) | `r0_c2t_mixed_seed_unseen_prefix_sa_rebalanced_onereason_v1` | 4,742 | [筛选方法、统计与样例](c2t-sa/README.md) |
