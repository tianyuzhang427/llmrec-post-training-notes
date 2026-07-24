# Caption2Token

Caption2Token 的任务是根据物料描述生成对应的 itemic token。这里使用的是一个 `4,742` 条的小包，而不是大规模覆盖集；内部资产版本为 `r0_c2t_mixed_seed_unseen_prefix_sa_rebalanced_onereason_v1`。

```text
[物料 caption]
    ↓
<|video_begin|><s_a_1><s_b_2><s_c_3>
```

itemic token 由域标记和三层语义编码组成：

- `prefix_s_a`：域标记加第一层语义编码，例如 `<|video_begin|><s_a_1>`，代表较粗的语义簇；
- `prefix_ab`：继续加入第二层编码，例如 `<|video_begin|><s_a_1><s_b_2>`；
- 完整 token：再加入 `<s_c_3>`，对应更细粒度的物料位置。

## 我是怎么构建的

1. 从清洗后的 Caption2Token 混合池出发，共有 `11,689` 条可选数据，同时包含 think 与 no-think 两种形式。
2. 只保留官方 seed 中没有出现过的 `prefix_s_a`，让有限的数据预算优先覆盖新的粗粒度语义簇。
3. 按 OneReason R0 caption 的广告、直播、电商和视频比例重新分配四个域的配额，避免小包被某个域主导。
4. 在每个域内先尽可能覆盖不同的 `prefix_s_a`，再为已有前缀补充额外样本。

最终得到 `4,742` 条数据、`3,018` 个不同的 `prefix_s_a`、`4,550` 个不同的 `prefix_ab`，并且每条数据对应的完整 token 都不重复。

## 数据统计

| 项目 | 数值 |
| --- | ---: |
| 数据行数 | 4,742 |
| 原始大小 | 3.8 MB |
| gzip 大小 | 1.1 MB |
| 唯一完整 token | 4,742 |
| 唯一 `prefix_ab` | 4,550 |
| 唯一 `prefix_s_a` | 3,018 |

| 域 | 条数 | 占比 | think | no-think |
| --- | ---: | ---: | ---: | ---: |
| 广告 | 1,181 | 24.91% | 577 | 604 |
| 直播 | 952 | 20.08% | 498 | 454 |
| 电商 | 1,218 | 25.69% | 560 | 658 |
| 视频 | 1,391 | 29.33% | 628 | 763 |
| **合计** | **4,742** | **100%** | **2,263** | **2,479** |

文件 SHA-256：

```text
e10f784107575aeb2aa0edae4244ecdf69fa14f7dfe1387c40b1eafee3535dd4
```

本仓库暂不分发真实 caption 与 token 对；这里保留筛选方法、统计和校验值。

## 验证结果

在 `CEval-Letter` 配方上加入这个 Caption2Token 小包后，总分从 `0.9186` 提升至 `0.9263`，即 `+0.0077`；“懂世界”同时从 `0.1361` 变化至 `0.1420`。这是一次直接父配方上的小幅正向结果，但尚未重复验证，因此不将它表述为稳定的因果增益。

## 合成样例

`example.jsonl` 只展示任务结构，不对应比赛或第三方真实物料：

```json
{
  "system": "根据物料描述生成匹配的 itemic token。",
  "prompt": "请根据以下短视频描述生成对应 token：[合成且不对应真实物料的描述]/no_think",
  "response": "<think>\n</think>\n<|video_begin|><s_a_1><s_b_2><s_c_3>"
}
```

think 模式执行同一个映射任务，只是在 `<think>...</think>` 中增加简短的物料语义摘要。

- [查看 manifest](manifest.json)
- [查看合成样例](example.jsonl)
