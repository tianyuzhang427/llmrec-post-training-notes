# LogicChain → ActionSelect

这条数据链将官方 seed dataset 中已有的 LogicChain 标注直接投影为 ActionSelect 格式。它不调用额外模型，也不重新生成标签；监督信号完全来自 `logic_chain.events[*].action` 中已经出现的 itemic token。

| 项目 | 内容 |
| --- | --- |
| 资产 | `logicchain_to_action_select_direct_v0` |
| seed 懂用户总行数 | 2,892 条 |
| 其中 LogicChain | 1,304 条 |
| 输出 | 1,298 条 |
| 投影标签 | 3,939 个 |
| 标签约束 | 每个 token 必须能从当前历史中逐字复制 |

## 怎么提取

每条 LogicChain 样本包含一段可见用户历史，以及一个结构化的 `logic_chain`：

```json
{
  "logic_chain": {
    "name": "[主题]",
    "events": [
      {
        "date": "[日期]",
        "action": "[行为描述 + itemic token]",
        "logic": "[与前一步的关系]"
      }
    ]
  }
}
```

投影过程如下：

1. 保留原始用户历史，不改写任何历史行为。
2. 使用 `logic_chain.name` 作为新的 ActionSelect 主题。
3. 按 event 顺序，从每个 `events[*].action` 中提取完整 itemic token。
4. 按首次出现顺序稳定去重，避免相同 SID 被多个 event 重复标注。
5. 检查每个输出 token 是否能从当前可见历史中逐字复制。
6. 将标签渲染为空 `<think>` 加 JSON 字符串数组，并统一使用 `/no_think` prompt。
7. action 中没有任何 itemic token 的样本直接拒绝，不使用 caption 或其他映射回填。

```text
原用户历史                         → 原样保留
logic_chain.name                  → ActionSelect 主题
events[*].action 中的 itemic token → 稳定去重后的 JSON 数组
events[*].date / logic            → 不进入最终 response
```

## 提取结果

| 检查项 | 结果 |
| --- | ---: |
| LogicChain 源样本 | 1,304 |
| 成功投影 | 1,298 |
| 无 itemic token、直接拒绝 | 6 |
| 原始 token 出现次数 | 4,037 |
| 去重后标签数 | 3,939 |
| 删除的重复 token | 98 |
| 全局唯一标签 | 3,855 |
| 输出标签不在可见历史中 | 0 |
| prompt / response 完全重复 | 0 |

## 为什么它只是弱标签

LogicChain 的目标是保留能够解释兴趣演化的 2–5 个核心事件；标准 ActionSelect 则倾向于找出主题下全部相关历史。因此，LogicChain 投影通常具有较高精度，但可能系统性漏掉平级相关或重复支持同一主题的历史行为。

这 1,298 条数据适合作为低召回弱标签，用来增加 ActionSelect 格式和 SID 数组监督；不能将其称为 FullRecall ActionSelect gold。

## 构建代码

目录内的 [build.py](build.py) 是去除项目内部依赖后的独立版本，只使用 Python 标准库：

```bash
python data/logicchain-to-actionselect/build.py \
  /path/to/懂用户.jsonl \
  /path/to/logicchain_actionselect.jsonl
```

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
