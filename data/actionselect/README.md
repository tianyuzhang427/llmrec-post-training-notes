# 自构造 ActionSelect

该资产包含 104 条精心构建的 ActionSelect 数据，所有答案 token 都能从题面中的用户历史逐字复制。

| 数据 | 规模 | 当前状态 |
| --- | ---: | --- |
| refined ActionSelect | 104 | 已进入训练验证 |

Action100 在直接父模型上带来一轮小幅提升。logs 和本地部署还观察到末项 SID 复读、双 SID 循环和数组不闭合；增加这类样本有所缓解，但问题尚未完全解决。

- [公开 manifest](manifest.json)
- [合成结构样例](example.jsonl)
