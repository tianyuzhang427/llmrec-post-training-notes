# 自构造 ActionSelect

以 104 条严格筛选的 anchor 为核心，扩展出 918 条候选 ActionSelect 数据；所有答案 token 必须来自题面可见历史。

| 数据 | 规模 | 当前状态 |
| --- | ---: | --- |
| strict anchor | 104 | 待人工语义复核 |
| Action918 candidate | 918 | `training_authorized=false` |

Action100 在直接父模型上有一轮正观测，但不能外推为 918 条一定有效。logs 和本地部署还观察到末项 SID 复读、双 SID 循环和数组不闭合；增加数据有所缓解，但问题尚未解决。

- [公开 manifest](manifest.json)
- [合成结构样例](example.jsonl)
