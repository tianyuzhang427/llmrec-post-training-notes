# C2T-SA 小包

从 caption → itemic token 数据中筛选 seed 未覆盖的 `prefix_s_a`，再按 OneReason R0 caption 的四域比例重平衡。

| 项目 | 内容 |
| --- | --- |
| 资产 | `r0_c2t_mixed_seed_unseen_prefix_sa_rebalanced_onereason_v1` |
| 规模 | 4,742 条 |
| 域分布 | 广告 1,181 / 直播 952 / 电商 1,218 / 视频 1,391 |
| 模式 | no-think 2,479 / think 2,263 |
| 覆盖 | 3,018 个唯一 `prefix_s_a`；4,742 个唯一完整 token |

该小包对应 `CEval-Letter + C2T` 主线中的 `+0.0077` 候选信号；变化较小且未重复验证，不写成稳定因果结论。

- [公开 manifest](manifest.json)
- [合成结构样例](example.jsonl)
