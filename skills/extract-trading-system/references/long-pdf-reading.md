# 长 PDF 并行读法

用于 >80 页的 PDF。单 agent 读长书会糊或漏,必须并行分段精读再合成。

## 流程

1. 查页数:`mdls -name kMDItemNumberOfPages "<PDF路径>"`。
2. 计算分段:每个 reader 约 110 页。页数 / 110 = reader 数(向上取整,至少 1)。
   - 例:442 页 -> 4 个 reader,各 1-111、112-222、223-333、334-442。
3. 每个 reader 用 `references/reader-prompt.md` 的提示词,替换 `{{PDF_PATH}}`、`{{PAGE_START}}`、`{{PAGE_END}}`、`{{SOURCE_TYPE}}`,并行启动(用 Agent 工具,一个消息里多个调用)。
4. 每个 reader 用 Read 工具按 20 页/块读自己的页段,按 13 节抽取笔记,保留数字/页码/原话。
5. 全部 reader 返回后,合成者(主对话)把多份笔记按 13 节合并、去重、理顺,产出最终系统文档。

## 注意

- reader 之间不通信,各读各的;合成在主对话做。
- 合成者要消除 reader 间的重复和矛盾;矛盾处以页码为准,或标「推断」。
- 若某 reader 失败或被中断,只重跑那一段,不重跑全部。
- 前置页(封面/目录/致谢)通常无系统内容,reader 会自然略过。
