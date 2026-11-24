# 基准测试结果（三层杠杆）

## 输出层 — 答案 token

10 题 × 3 策略，cl100k_base 计数：

| 策略 | token | vs baseline | 关键信息保留 |
|---|---|---|---|
| baseline | 1644 | — | 100% |
| caveman | 577 | −64.9% | 100% |
| **TokenSaver** | **479** | **−70.9%** | **100%** |
| hybrid（每题取优） | 459 | −72.1% | 100% |

复现：`answers.md` + `count.py`。

## 输入层 — 命令输出 token

真实命令，raw vs token-saver 钩子 vs rtk：

| 命令 | raw | token-saver | rtk | token-saver% | rtk% |
|---|---|---|---|---|---|
| git status | 23 | 0 | 12 | 100% | 48% |
| git log | 438 | 49 | 203 | 89% | 54% |
| ls -la ~/.claude | 776 | — | 185 | — | 76% |
| find ~/.claude/plugins -type f | 143019 | — | 14 | — | 100% |
| **合计** | **144256** | **143844** | **414** | **0%** | **99.7%** |

结论：

- **rtk 是输入大头**：混合负载下 144256 → 414，−99.7%（`find` 这种巨型输出被压到 14 token）。
- **token-saver 钩子只做无损白名单**（git status −100%、git log −89%），不碰 ls/find，所以总表里贡献小。
- 两者互补：rtk 管全局，token-saver 钩子补两条无损 git 项。

复现：`input_bench.py`。

## 上下文层 — 持久上下文 token

| 项 | token |
|---|---|
| 全局 CLAUDE.md（`@RTK.md` 指针） | 5 |
| RTK.md | 98 |
| **持久上下文合计** | **103** |
| token-saver 规则注入（每会话固定成本） | 193 |

结论：

- 当前持久上下文已精简：5 token 指针替代常驻文档（臃肿 CLAUDE.md 常驻数千 token）。
- token-saver 每会话注入 193 token 规则集，换取三层自动执行；输出层每答案省 ~70%，多轮即回本。

## 总评

三层互补，各司其职：

| 层 | 主担当 | 幅度 |
|---|---|---|
| 输出 | TokenSaver 规则 | −70.9%（比 caveman 再 −17%） |
| 输入 | rtk（钩子） | −99.7% |
| 上下文 | 指针化 + 按需加载 | 数千 → 103 token |
