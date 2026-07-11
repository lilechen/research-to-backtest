# 长 PDF 并行读法

用于 >80 页的 PDF。单 agent 读长书会糊或漏,必须并行分段精读再合成。

## 流程

1. 查页数:`mdls -name kMDItemNumberOfPages "<PDF路径>"`(或 `pdfinfo "<PDF>" | grep Pages`)。
2. 计算分段:每个 reader 约 60 页(更稳,适配多种模型 / agent 容量)。页数 / 60 = reader 数(向上取整,至少 1)。
   - 例:442 页 -> 8 个 reader,每块约 55 页。
   - 例:339 页 -> 6 个 reader,各 1-57、58-113、114-170、171-226、227-283、284-339。
   - 例:120 页 -> 2 个 reader,各 1-60、61-120。
   - **若模型/agent 稳定,可放宽到 ~110 页**(原协议值);若 reader 频繁 stall/超时,降到 50 或 40。
3. 每个 reader 用 `references/reader-prompt.md` 的提示词,替换 `{{PDF_PATH}}`、`{{PAGE_START}}`、`{{PAGE_END}}`、`{{SOURCE_TYPE}}`,并行启动(用 Agent 工具,一个消息里多个调用)。
4. 每个 reader 读自己的页段(读法见下「两种读法」),按 13 节抽取笔记,保留数字/页码/原话。
5. 全部 reader 返回后,**启动 1 个 synthesizer agent** 把多份笔记合并成最终系统文档(详见「合成步骤」节)。

## 两种读法(视觉 vs 文本提取)

reader 读页段有两条路,取决于当前模型是否支持图像/PDF 视觉输入。

### A. 视觉读(模型支持图像输入时)

reader 用 Read 工具的 `pages` 参数,每次 20 页,从 `{{PAGE_START}}` 读到 `{{PAGE_END}}`。每页都读,不得跳过。

### B. 文本提取回退(模型只支持文本输入时)

部分模型(如 glm 系列)不支持图像输入,Read 的 `pages` 参数会报 `400 Model only support text input`。此时改用命令行 `pdftotext`(poppler)把每段页范围提取成带页码标记的文本文件,reader 读 `.txt` 而非 PDF。

步骤(在主对话执行,再分发给各 reader):

**首选:用现成脚本**(本目录 `extract-and-chunk.py`):

```bash
python3 references/extract-and-chunk.py "<PDF路径>" --chunk-size 60
```

输出为 `/tmp/<book>_p<START>-<END>.txt`,每页前有 `=== PAGE N ===` 标记。

**手工备选**(若不想用脚本):

```bash
# 1. 确认工具可用
which pdftotext          # 期望:/opt/homebrew/bin/pdftotext 等

# 2. 按页段提取(每段一个文件,-layout 保留排版)
pdftotext -layout -f <FIRST> -l <LAST> "<PDF路径>" /tmp/<book>_p<FIRST>-<LAST>.txt
```

再加 PAGE 标记(脚本同 extract-and-chunk.py 内的逻辑)。

reader 提示词相应改为:读 `/tmp/<book>_p<FIRST>-<LAST>.txt`,文件 >2000 行,用 Read 的 `offset` 参数分多次读完;页码以 `=== PAGE N ===` 标记为准。

> 检测信号:第一次试读 PDF 一页,若返回 `Model only support text input` / `image input not supported` 类错误,即切到 B 方案。只重跑失败的 reader,不重跑全部。

## 笔记交付:写文件,不回消息(重要)

reader 的 13 节笔记通常很长(数千字),作为消息返回给主对话**会被截断**(任务通知里的 `<result>` 只保留开头)。因此无论用哪种读法,reader 的提示词都应要求:

> 用 Write 工具把完整笔记写入 `/tmp/<book>_notes_p<FIRST>-<LAST>.md`,返回消息只写一句「已写入 …(约 N 字)」。不要把笔记内容作为消息返回。

合成者随后用 Read 工具读这些 `.md` 文件拿全文。

## 注意

- reader 之间不通信,各读各的;合成由 synthesizer agent 完成(见下节)。
- 合成者要消除 reader 间的重复和矛盾;矛盾处以页码为准,或标「推断」。
- 若某 reader 失败或被中断,只重跑那一段,不重跑全部。
- 前置页(封面/目录/致谢)通常无系统内容,reader 会自然略过。
- 文本提取(`pdftotext`)对扫描版 PDF(纯图像页)无效——那种情况必须用视觉读或 OCR。

## 合成步骤(用 synthesizer agent)

reader 完成后,**不要在主对话里手动读 N 份笔记 + 手写 13 节文档**(易 quota 紧、易长 context)。改用 **synthesizer agent**:

1. 用 Agent 工具启动 1 个 synthesizer agent,`run_in_background:true`(可选——若笔记总长 < 100k token,前台即可)。
2. 提示词模板见 `references/synthesizer-prompt.md`。替换占位符:
   - `{{NOTES_GLOB}}`:`/tmp/<book>_notes_p*.md`
   - `{{OUTPUT_PATH}}`:用户指定的最终文档路径
   - `{{EXAMPLE_PATHS}}`:本仓库 `examples/` 下已有的完整文档(Weinstein + Clenow),用于风格对齐
3. synthesizer 读完所有笔记后,直接 Write 最终文档到 `{{OUTPUT_PATH}}`,返回一句确认。

主对话收到 synthesizer 的「已写入」确认后,流程结束;不需要再做任何合成长 Write。
