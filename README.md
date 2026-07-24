# OneReason / LLM-Rec SFT 复盘

## 已验证的提分路径

`懂用户` 为两个用户任务之和，`懂推荐` 为视频、电商、广告、直播四项之和。

> 表中分数均来自已经完成的线上评测。“已验证”表示整套配方曾达到该分数，不代表多因素阶段的每个改动都获得了单变量因果验证。

| 阶段 | 总分 | 懂物料 | 懂用户 | 懂推荐 | 懂世界 | 改动 / 备注 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 预训练直评 | 0.6704 | 0.1533 | 0.0091 | 0.3667 | 0.1413 | 起点；未做 SFT。 |
| LoRA Seed SFT | 0.8635 | 0.1840 | **0.1264** | 0.4174 | 0.1357 | 官方 seed dataset；LoRA 峰值学习率 `2e-4`。 |
| CEval-Letter | 0.9186 | 0.2146 | 0.1031 | 0.4648 | 0.1361 | 加入空 `<think>` + 单字母答案的 CEval 数据。 |
| CEval-Letter + C2T | 0.9263 | 0.2146 | 0.1078 | 0.4618 | 0.1420 | 加入 4,742 条 Caption2Token。 |
| + Math | 0.9573 | **0.2453** | 0.1105 | 0.4529 | 0.1487 | 第一次加入 Math 数据。 |
| + 多因素 | 0.9768 | 0.2146 | 0.1063 | **0.4949** | 0.1610 | LogicChain→Action + Math Plus + Item2 + 视频减半；非单变量对照。 |
| Action100 | **0.9881** | **0.2453** | 0.1157 | 0.4650 | **0.1621** | 在 `0.9768` 直接父模型上追加 Action100。 |

## 六类数据资产

每个目录只包含数据卡、公开 manifest 和一条合成样例。

| 主线 | 规模 | 样例 | 证据边界 |
| --- | ---: | --- | --- |
| [CEval-Letter](data/ceval-letter/README.md) | 13,948 | [查看样例](data/ceval-letter/README.md#合成样例) | 有清楚的早期整体正观测，但不是懂世界单项提升。 |
| [懂世界 Math](data/math/README.md) | 21,799 + 21,799 | [查看样例](data/math/README.md#合成样例) | Math23K 与 Math Plus 两层数据均经过验证，有利于提升懂世界。 |
| [Half Video](data/half-video/README.md) | 19,204 → 11,770 | [查看样例](data/half-video/README.md#合成样例) | 只减半视频行；缺少隔离因果对照。 |
| [LogicChain → ActionSelect](data/logicchain-to-actionselect/README.md) | 1,298 | [查看样例](data/logicchain-to-actionselect/README.md#合成样例) | 增加 ActionSelect 样本有利于缓解复读问题。 |
| [ActionSelect](data/actionselect/README.md) | 104 | [查看样例](data/actionselect/README.md#合成样例) | 104 条精心构建的 ActionSelect 数据带来小幅提升。 |
| [Caption2Token](data/c2t-sa/README.md) | 4,742 | [查看样例](data/c2t-sa/README.md#合成样例) | seed-unseen `prefix_s_a` + OneReason 域比例重平衡。 |

## 提分过程中的观察与判断

### 难样本预算

调整 item-token loss 权重和 focal `γ` 时，线上分数出现了超出预期的正向变化。由此推测，seed dataset 中存在大量简单且重复的样本：它们占用了训练预算，却没有提供足够的新信息。基于这一判断，我们清洗了“懂推荐”中占比最大的 Video domain，将视频样本减少约 50%，其他推荐域保持不变。线上结果验证了这一方向有效；但继续减少到 35% 后收益转负，说明真正有效的是适度去除冗余，而不是数据越少越好。

### 面向评测分布补数据

这是一种并不优雅、却在竞赛中确实有效的提分策略：根据评测题型补充同构训练数据，提高命中评测分布的概率。我们判断“懂世界”中包含较多数学单选题，因此先后加入 Math23K 和 Math Plus。“懂世界”从 LoRA Seed SFT 的 `0.1357`，提升至 Math23K 阶段的 `0.1487`，并在加入 Math Plus 后达到 `0.1610`。两层数学数据都有效提高了模型对“懂世界”评测题型的覆盖。

### 懂用户的 Prompt 扰动

评测日志中的角色、规则、schema、示例和版式比 seed 更丰富。基于这一观察，我们对 seed prompt 做了相应增强，但没有观察到明确的正向增益。由于后期实验同时引入了多个变量，目前仍无法证明 prompt 多样性能够独立提分。

### 评测结果波动的原因

一部分波动来自 LLM/VLM 推理过程本身的不稳定性，本文不再展开。另一部分波动可能来自训练过程：部分任务在许多更新步骤中没有获得有效监督，从而放大了 shuffle 和 packing 对训练结果的影响。

![官方 seed 本地 replay 的 optimizer-step 任务覆盖率](assets/optimizer-step-coverage.svg)

本地 replay 中，Recommendation 覆盖 `412/420` steps，ActionSelect 覆盖 `241/420`，LogicChain 覆盖 `279/420`，Material C2T 覆盖 `60/420`，Material T2C 覆盖 `40/420`。该 replay 并非平台的真实 batch trace，但它直观展示了任务间的更新机会并不均衡：多数更新步骤由 Recommendation 主导，而 Caption2Token 等低频任务只在少量步骤中获得监督。随着 shuffle 和 packing 改变，这些低频任务获得的有效更新次数也会变化，因此训练结果出现波动是符合直觉的。

### ActionSelect 复读

在评测日志和本地部署中，都观察到了末项 SID 复读、双 SID 循环以及 JSON 数组不闭合等问题。增加精心构建的 ActionSelect 数据能够缓解复读，但尚未彻底解决。后续仍需分别验证数据规模、数组终止监督、EOS/packing 和 decoding 策略的影响。

### 求其上而取其中

这次比赛最重要的教训，不只是哪一种数据配方有效，更在于目标设定决定了迭代方式。最初只是想利用闲暇时间争取进入复赛，这个目标过于保守，也让后续策略变得短视：没有优先在开发机上建立可重复的本地评测体系，而是过早依赖线上平台的反馈。

一旦缺少本地评测闭环，能够主动控制的就只剩下训练参数、loss 权重和数据集比例等少量变量；WanQing 线上平台每天仅提供 3–5 次评测机会，反馈既稀疏又带有波动，很难支持系统归因。更合理的路线应当是先建立可复现、可诊断的本地迭代体系，再用线上评测做最终校准。

深度学习本质上是一门实验科学，可靠的方向和直觉需要在持续、可复现的实验中形成。前期目标设定偏低，进一步导致了过早依赖线上平台的决策，显著压缩了迭代次数，也降低了实验效率；到了比赛后期，即使发现了新的问题，也已经缺少继续诊断和验证的空间。

所谓“求其上而取其中”：如果一开始就把目标设为理解并解决问题，即使不能达到理想上限，也更可能获得扎实的中间结果；如果目标只是勉强过线，最终往往也只能停留在过线附近。

## 目录

```text
.
├── README.md
├── PUBLIC_RELEASE.md
├── assets/
│   └── optimizer-step-coverage.svg
├── data/
│   ├── README.md
│   └── <asset>/
│       ├── README.md
│       ├── manifest.json
│       └── example.jsonl
└── scripts/
    └── check_release.py
```

发布前运行：

```bash
python scripts/check_release.py
```

数据许可和结果表述边界见 [PUBLIC_RELEASE.md](PUBLIC_RELEASE.md)。
