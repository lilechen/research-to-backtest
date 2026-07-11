---
name: extract-trading-system
description: 从一本交易书或一篇 paper 的 PDF 中,抽取一个完整、自足、人可执行的交易系统。用于把书或论文里散落的方法论、规则、参数、案例,蒸馏成一份按统一模板组织的交易系统规格,供个人交易者直接照做或进入下一步回测结构化。输入为 PDF 路径和资料类型(book/paper),输出为一份人可读的交易系统文档。
---

# 从文献抽取交易系统

## 核心流程

1. **先确认输入。** 接收 PDF 路径和 source_type(book 或 paper)。若用户未指定 source_type,从文件名或内容判断后向用户确认。
2. **先读全文,再下结论。** 必须精读整本 PDF,不得只读摘要或目录。长书按 `references/long-pdf-reading.md` 并行分段读完再合成。
3. **按模板蒸馏,不是按章节复述。** 用 `references/system-template.md` 的 13 节结构组织输出。每条规则都要落到可执行的动作或判据,不要停留在"要顺势而为"这类空泛道理。
4. **保留原话数字。** 凡参数、阈值、公式、案例数字,必须原样引用,不得改写。关键判据标注页码。
5. **区分书中明确与推断。** 书中明确写的内容与合理推断必须分开标注。推断标「推断」。
6. **诚实记录缺口。** 书里没有讲死的环节,必须进入第 12 节"缺口与补全",要么标「书中未明确」,要么给标注推断 + 理由。不得编造补全。
7. **站在人手动交易视角。** 全程从"一个人坐在屏幕前实际做交易"的角度写。不出现回测、代码、信号函数等量化表述。
8. **按 source_type 微调。** book 偏多判断词,要把"RS 改善""均线上行"这类描述尽量抠成可辨认的视觉判据;paper 偏 methodology,直接抽取已给出的公式、参数、信号构造,保留作者的定义。

## 工作流

1. 用 `mdls -name kMDItemNumberOfPages`(或 `pdfinfo`)查 PDF 页数。
2. 若页数 ≤ 80,单次精读即可;若 > 80,按 `references/long-pdf-reading.md` 并行 fan-out 多个 reader:
   - **分块默认 ~60 页/reader**(适配多种模型)。可放宽到 ~110 若模型稳定。
   - **读法二选一**:模型支持图像输入时,reader 用 Read 的 `pages` 参数视觉读 PDF;模型只支持文本时(试读报 `Model only support text input`),用 `references/extract-and-chunk.py` 把 PDF 按页段切成带 `=== PAGE N ===` 标记的 `.txt`,reader 读文本文件。
   - **笔记写文件**:reader 用 Write 把笔记写入 `/tmp/<书名>_notes_p<段>.md`,只返回一句确认(长笔记作消息返回会被截断)。
3. **所有 reader 返回后,启动 1 个 synthesizer agent**(见 `references/synthesizer-prompt.md`):
   - 替换占位符:`{{NOTES_GLOB}}` = `/tmp/<book>_notes_p*.md`、`{{OUTPUT_PATH}}` = 最终文档路径、`{{EXAMPLE_PATHS}}` = `examples/Weinstein/Weinstein.trading-system.md` + `examples/Clenow/Clenow.trading-system.md`(风格对齐)
   - **synthesizer 用分批 Write+Edit 模式**(骨架 Write + 13 节 + 附录的逐节 Edit,见 synthesizer-prompt.md),避免一次 Write 32k 字
   - synthesizer 读全部笔记 → 按 `references/system-template.md` 的 13 节合并去重 → 写文件 → 返回一句确认
   - **主对话不做合成长 Write**,避免 quota / context 风险。
4. **synthesizer 完成后,启动 1 个 critic agent**(见 `references/critic-prompt.md`):
   - 读合成文档 + 对照模板
   - 检查 13 节结构、页码引用、标记规范、数字保真、人交易视角、缺口诚实、元数据
   - 输出 PASS / PASS_WITH_WARN / FAIL 报告
   - **失败必须重新跑 synthesizer**(调整后重跑),不能跳过
5. critic 通过后,告诉用户文档路径与要点摘要(2-4 句)。
6. 更新仓库根目录 `STATUS.md`,标记该书的 Stage 1 状态为 ✅。

## 输出约束

- 输出文件名:`<name>.trading-system.md`。
- 严格按 13 节模板,不得增减顶级章节。
- 凡具体数字(如「30 周均线」「2% 风险」)原样引用。
- 关键判据尽量给章节/页码定位。
- 一书若含多个系统,抽主系统,变体记入第 12 节;若用户要求抽全部,各出一份。
- 全程人交易视角,禁止回测/代码表述。

## 参考资料

抽取分段笔记时,读取 `references/reader-prompt.md`。
组织最终输出时,读取 `references/system-template.md`。
处理长 PDF(>80 页)时,读取 `references/long-pdf-reading.md`。
合成步骤用 synthesizer agent,读取 `references/synthesizer-prompt.md`。
合成后质量检查用 critic agent,读取 `references/critic-prompt.md`。
PDF 文本提取脚本(纯文本模型用):`references/extract-and-chunk.py`。

整体进度跟踪见仓库根目录 `STATUS.md`。

## 风格参考

最终输出的密度、标记规范、案例格式参考 `examples/` 下已有文档:
- `examples/Weinstein/Weinstein.trading-system.md`——经典趋势/形态系统的抽取范例
- `examples/Clenow/Clenow.trading-system.md`——全定量、含大量参数表的量化趋势系统的抽取范例
