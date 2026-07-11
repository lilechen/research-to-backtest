#!/usr/bin/env python3
"""
extract-and-chunk.py

从 PDF 提取文本并按页段切分,每段加 `=== PAGE N ===` 标记。
供 extract-trading-system skill 在「文本读法」模式下使用(纯文本模型)。

用法:
  python3 extract-and-chunk.py <PDF路径> [--chunk-size N] [--output-prefix PREFIX] [--start-page S] [--end-page E]

参数:
  PDF路径              必填
  --chunk-size N       每块页数,默认 60(更稳,适配多种模型)
  --output-prefix PREFIX  输出文件前缀,默认 /tmp/<PDF basename>_p
  --start-page S       起始页(1-indexed),默认 1
  --end-page E         结束页,默认 PDF 总页数
  --quiet              抑制进度输出

输出:
  <prefix><START>-<END>.txt 一组文件,每个文件每页前有 `=== PAGE N ===` 标记。

依赖:
  pdftotext (poppler)
  pdfinfo  (poppler,可选,仅当不传 --end-page 时需要)
"""

import argparse
import os
import subprocess
import sys


def pdf_total_pages(pdf_path: str) -> int:
    """用 pdfinfo 查页数,失败则用 pdfinfo 之外的方式或抛错。"""
    try:
        out = subprocess.run(
            ["pdfinfo", pdf_path],
            capture_output=True, text=True, check=True,
        ).stdout
    except FileNotFoundError:
        sys.exit("错误:未找到 pdfinfo。请安装 poppler(macOS: brew install poppler)。")
    except subprocess.CalledProcessError as e:
        sys.exit(f"错误:pdfinfo 失败: {e.stderr}")
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    sys.exit(f"错误:pdfinfo 输出中找不到 'Pages:' 行")


def extract_chunk(pdf_path: str, first: int, last: int, out_path: str, quiet: bool) -> None:
    """用 pdftotext 提取指定页段,加 PAGE 标记。"""
    try:
        raw = subprocess.run(
            ["pdftotext", "-layout", "-f", str(first), "-l", str(last), pdf_path, out_path + ".raw"],
            capture_output=True, text=True, check=True,
        )
    except FileNotFoundError:
        sys.exit("错误:未找到 pdftotext。请安装 poppler(macOS: brew install poppler)。")
    except subprocess.CalledProcessError as e:
        sys.exit(f"错误:pdftotext 失败(页 {first}-{last}): {e.stderr}")
    # pdftotext 默认用 form-feed (\f) 分页
    with open(out_path + ".raw", encoding="utf-8", errors="replace") as f:
        pages = f.read().split("\f")
    if pages and pages[-1].strip() == "":
        pages = pages[:-1]
    out = "".join(f"\n=== PAGE {first + i} ===\n{p}" for i, p in enumerate(pages))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    os.remove(out_path + ".raw")
    if not quiet:
        print(f"  ✓ {out_path} ({len(pages)} 页, {len(out)} chars)")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="从 PDF 提取文本,按页段切分,加 PAGE 标记。"
    )
    ap.add_argument("pdf", help="PDF 文件路径")
    ap.add_argument("--chunk-size", type=int, default=60,
                    help="每块页数,默认 60")
    ap.add_argument("--output-prefix", default=None,
                    help="输出文件前缀,默认 /tmp/<PDF basename>_p")
    ap.add_argument("--start-page", type=int, default=1, help="起始页(1-indexed)")
    ap.add_argument("--end-page", type=int, default=None, help="结束页,默认 PDF 总页数")
    ap.add_argument("--quiet", action="store_true", help="抑制进度输出")
    args = ap.parse_args()

    if not os.path.isfile(args.pdf):
        sys.exit(f"错误:PDF 文件不存在: {args.pdf}")

    if args.end_page is None:
        total = pdf_total_pages(args.pdf)
        end = total
        if not args.quiet:
            print(f"PDF 总页数: {total}")
    else:
        end = args.end_page

    if args.output_prefix is None:
        basename = os.path.splitext(os.path.basename(args.pdf))[0]
        # 把 basename 里可能让文件操作出问题的字符替换一下
        basename = basename.replace(" ", "_").replace("/", "_")
        prefix = f"/tmp/{basename}_p"
    else:
        prefix = args.output_prefix

    start = args.start_page
    chunk = args.chunk_size
    if not args.quiet:
        print(f"分块:每 {chunk} 页,总 {end - start + 1} 页,起始 {start},结束 {end}")
        print(f"输出前缀: {prefix}")

    chunk_count = 0
    s = start
    while s <= end:
        e = min(s + chunk - 1, end)
        out_path = f"{prefix}{s}-{e}.txt"
        extract_chunk(args.pdf, s, e, out_path, args.quiet)
        chunk_count += 1
        s = e + 1

    if not args.quiet:
        print(f"\n完成。共生成 {chunk_count} 个文本块。")
        print(f"下一步:把每个块作为一个 reader agent 读取,Write 到 {prefix.replace('/tmp/', '/tmp/')}notes_<START>-<END>.md")


if __name__ == "__main__":
    main()