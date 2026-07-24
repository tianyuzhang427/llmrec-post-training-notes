# 数据资产

本目录只维护六类数据资产的公开说明，不包含任何比赛或第三方真实数据行。

每个子目录固定包含三个文件：

- `README.md`：任务内容、规模和证据边界；
- `manifest.json`：公开 lineage 与统计；
- `example.jsonl`：一条合成结构样例，不可用于训练或评测。

| 数据资产 | 正式版本 | 规模 |
| --- | --- | ---: |
| [CEval-Letter](ceval-letter/README.md) | `understanding_world_ceval_letter_no_think` | 13,948 |
| [懂世界 Math](math/README.md) | Math23K letter-only + Math Diversity Delta | 21,799 + 21,799 |
| [Half Video](half-video/README.md) | `seed_recommend_video_diverse_half_v1` | 19,204 → 11,770 |
| [LogicChain → ActionSelect](logicchain-to-actionselect/README.md) | `logicchain_to_action_select_direct_v0` | 1,298 |
| [自构造 ActionSelect](actionselect/README.md) | strict 104 → Action918 | 104 / 918 |
| [C2T-SA 小包](c2t-sa/README.md) | `r0_c2t_mixed_seed_unseen_prefix_sa_rebalanced_onereason_v1` | 4,742 |
