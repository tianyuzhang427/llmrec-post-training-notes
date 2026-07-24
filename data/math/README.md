# 懂世界 Math

该方向包含两份证据状态不同的 21,799 条数学数据。

| 数据 | 内容 | 状态 |
| --- | --- | --- |
| Math23K letter-only | 中文基础数学四选一题 | 进入过 `B0_Math` 训练 |
| Math Diversity Delta | 多来源基础数学与结构化题型 | 本地验证通过，未做线上单变量验证 |

两份数据都使用 `<think>\n</think>\nA/B/C/D` 输出。Delta 匹配 Math23K 的行数、答案位置和监督 token 预算，目标是增加小学、初中题型和解题结构的广度，不是简单提高难度。

`B0_Math` 总分曾达到 `0.9573`，但完整训练 lineage 不足，不能把全部变化归因于 Math23K；Delta 也不能写成已经线上涨分。

- [公开 manifest](manifest.json)
- [合成结构样例](example.jsonl)
