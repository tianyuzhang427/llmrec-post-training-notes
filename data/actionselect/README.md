# 自构造 ActionSelect

该资产包含 104 条精心构建的 ActionSelect 数据，所有答案 token 都能从题面中的用户历史逐字复制。

| 数据 | 规模 | 当前状态 |
| --- | ---: | --- |
| refined ActionSelect | 104 | 已进入训练验证 |

Action100 在直接父模型上带来一轮小幅提升。logs 和本地部署还观察到末项 SID 复读、双 SID 循环和数组不闭合；增加这类样本有所缓解，但问题尚未完全解决。

## 直接使用

- [下载完整 ActionSelect 104 JSONL](actionselect_104.jsonl)
- 行数：`104`
- 文件大小：`1,806,802 bytes`
- SHA-256：`55c40c214f10830e650800927acc87f68abf324618f1ec7fd83285524e1f4b4b`
- 字段：`system`、`prompt`、`response`

## 数据来源

- 上游数据：比赛官方提供的 seed dataset；
- 使用部分：seed dataset 中的用户历史记录；
- 派生方式：从用户历史中构造兴趣演化主题，经 Teacher/Judge 筛选后，从被选中的历史事件中复制 itemic token 形成 ActionSelect 标签；
- 数据性质：由官方 seed 用户历史派生的训练数据，不是官方 ActionSelect gold 的直接副本。

引用或继续使用该文件时，应同时注明比赛官方 seed dataset 与本仓库的派生流程，并遵守原比赛规则及上游数据约束。本仓库公开该派生文件，不代表对上游比赛数据进行重新许可。完整边界见 [公开发布说明](../../PUBLIC_RELEASE.md)。

## 104 条是怎么提取的

### 1. 构造严格长链母本

首先从独立的 UserProfile 用户历史中生成候选兴趣演化链。候选需要同时满足本地结构门槛、Teacher 标注和独立 Judge 审核：

- 历史中存在能够组成同一主题演化过程的多个状态；
- Teacher 给出主题、状态划分和每个状态对应的 event indexes；
- Judge 检查主题是否由历史支持、所选事件是否准确，以及是否遗漏关键状态；
- 标签只能来自被 Teacher 选中的事件，不能从不可见 caption 或外部知识中补充。

这一流程得到 103 条严格长链样本，且对应 103 个不同用户。

### 2. 加入一条短链

短链候选经过相同的 Teacher / Judge 流程，只保留唯一一条 Teacher `high`、Judge `accept/high` 的两状态样本。它与 103 条长链合并后得到最终 104 条。

### 3. 从事件生成 ActionSelect 标签

Teacher 为每个兴趣状态标出相关 event indexes。随后按可见历史中的首次出现顺序取出这些事件的 itemic token，并进行稳定去重：

```text
Teacher 选中的 event indexes
→ 对应历史事件中的 itemic token
→ 按历史首次出现顺序排列
→ 去重
→ JSON 字符串数组
```

因此，每个 response 都满足：

- token 格式合法；
- token 能从 prompt 的用户历史中逐字复制；
- 标签无重复；
- 标签顺序与历史时间顺序一致；
- response 为合法 JSON 数组；
- prompt 以 `/no_think` 结尾。

### 4. 对齐线上 Prompt

我将主题统一润色为简洁的中文“从 A 到 B”表达，并将 prompt 对齐评测日志中的三段式结构：

```text
角色任务
主题
输出格式要求
```

共保留四种语义等价的 prompt surface，每种 26 条。最终版本将 104 条 `system` 全部置空，以匹配 seed dataset 和 ActionSelect 评测日志的默认契约。

### 5. 切分与检查

| split | 行数 |
| --- | ---: |
| train | 84 |
| dev | 10 |
| test_internal | 10 |

自动门槛检查覆盖 JSON、token 合法性、可见历史复制、去重、时间顺序、`/no_think`、参考集重复和冻结字段。最终文件保留全部 104 条，便于直接复现 Action100 附近的数据配方。

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
