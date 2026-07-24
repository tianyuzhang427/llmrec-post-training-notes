# 数据资产

本目录只维护六类数据资产的公开说明，不包含任何比赛或第三方真实数据行。

每个子目录固定包含三个文件：

- `README.md`：任务内容、规模和证据边界；
- `manifest.json`：公开 lineage 与统计；
- `example.jsonl`：一条合成结构样例，不可用于训练或评测。

| 数据资产 | 正式版本 | 规模 | 合成样例 |
| --- | --- | ---: | --- |
| [CEval-Letter](ceval-letter/README.md) | `understanding_world_ceval_letter_no_think` | 13,948 | [在数据卡中查看](ceval-letter/README.md#合成样例) |
| [懂世界 Math](math/README.md) | Math23K letter-only + Math Diversity Delta | 21,799 + 21,799 | [在数据卡中查看](math/README.md#合成样例) |
| [Half Video](half-video/README.md) | `seed_recommend_video_diverse_half_v1` | 19,204 → 11,770 | [在数据卡中查看](half-video/README.md#合成样例) |
| [LogicChain → ActionSelect](logicchain-to-actionselect/README.md) | `logicchain_to_action_select_direct_v0` | 1,298 | [在数据卡中查看](logicchain-to-actionselect/README.md#合成样例) |
| [自构造 ActionSelect](actionselect/README.md) | `user_history_r2_action_select_refined_104_v5` | 104 | [在数据卡中查看](actionselect/README.md#合成样例) |
| [C2T-SA 小包](c2t-sa/README.md) | `r0_c2t_mixed_seed_unseen_prefix_sa_rebalanced_onereason_v1` | 4,742 | [在数据卡中查看](c2t-sa/README.md#合成样例) |
