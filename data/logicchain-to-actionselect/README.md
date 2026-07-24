# LogicChain → ActionSelect

从 LogicChain 样本的核心事件中抽取 itemic token，投影成 ActionSelect 风格的弱标签。

| 项目 | 内容 |
| --- | --- |
| 资产 | `logicchain_to_action_select_direct_v0` |
| 可转换源样本 | 1,304 条 |
| 输出 | 1,298 条 |
| 投影标签 | 3,939 个 |
| 标签约束 | 每个 token 必须能从当前历史中逐字复制 |

LogicChain event 只标记核心演化证据，不能保证覆盖所有主题相关历史，因此该资产不是 FullRecall ActionSelect gold，只能作为低召回弱标签消融。

## 合成样例

```json
{
  "system": "",
  "prompt": "【用户交互历史】[合成历史]\n【兴趣主题】[合成主题]\n请选择相关历史条目/no_think",
  "response": "<think>\n</think>\n[\"<|video_begin|><s_a_1><s_b_2><s_c_3>\"]"
}
```

- [公开 manifest](manifest.json)
- [原始 example.jsonl](example.jsonl)
