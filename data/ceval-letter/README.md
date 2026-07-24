# CEval-Letter

中文学科四选一题目，输出统一为“空 `<think>` + 单字母答案”。

| 项目 | 内容 |
| --- | --- |
| 资产 | `understanding_world_ceval_letter_no_think` |
| 来源 | C-Eval，需由使用者自行取得 |
| 规模 | 13,948 条 |
| 输出 | `<think>\n</think>\nA/B/C/D` |
| 答案分布 | A 3,197 / B 3,625 / C 3,680 / D 3,446 |

该数据对应清楚的早期整体正观测，但懂世界单项基本持平，不能解释为世界知识的独立提升。

## 合成样例

```json
{
  "system": "请直接遵循指示作答。",
  "prompt": "请回答以下选择题：\n[合成题干]\nA. [选项一]\nB. [选项二]\nC. [选项三]\nD. [选项四]\n/no_think",
  "response": "<think>\n</think>\nB"
}
```

- [公开 manifest](manifest.json)
- [原始 example.jsonl](example.jsonl)
