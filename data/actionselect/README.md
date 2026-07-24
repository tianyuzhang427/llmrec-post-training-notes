# 自构造 ActionSelect

该资产包含 104 条精心构建的 ActionSelect 数据，所有答案 token 都能从题面中的用户历史逐字复制。

| 数据 | 规模 | 当前状态 |
| --- | ---: | --- |
| refined ActionSelect | 104 | 已进入训练验证 |

Action100 在直接父模型上带来一轮小幅提升。logs 和本地部署还观察到末项 SID 复读、双 SID 循环和数组不闭合；增加这类样本有所缓解，但问题尚未完全解决。

## 合成样例

```json
{
  "system": "",
  "prompt": "【用户交互历史】[合成历史]\n【目标兴趣】[合成主题]\n选出支持该兴趣的历史条目/no_think",
  "response": "<think>\n</think>\n[\"<|prod_begin|><s_a_1><s_b_2><s_c_3>\", \"<|video_begin|><s_a_4><s_b_5><s_c_6>\"]"
}
```

- [公开 manifest](manifest.json)
- [原始 example.jsonl](example.jsonl)
