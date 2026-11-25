#!/usr/bin/env python3
"""补回 oyy 的正规 ①（**仅此一条**）。

背景
----
本仓库为修「四码单字首选是 ①」，早期删除了 cn_dicts/jde/ 里大量含 ① 的词条。
上游 V9.1.0 日志原文：

    32. ①在一些四码符号处有冗余，删掉。

但 oy 系列是「oy + 数字键盘键位」的快速数字符号，属于正规候选位：

    oyy(y=1) → ① Ⅰ ㊀ （一） -1
    oye(e=2) → ② Ⅱ ㊁
    oys(s=3) → ③ Ⅲ ㊂
    ... 共 10 组

其中 oyy 的 ① 被一并删掉，需补回（放最前，与上游顺序一致）。

**只补 oyy 这一条。** 其余短码的 ①（ck / ez / hq / kn / qc / vn / zq ... 共 29 条）
是维护者主动删除的，不属于本脚本范围，不要补。
"""
import os

LOCAL = "cn_dicts/jde/jde.dict.yaml"
CODE = "oyy"
WORD = "①"
ANCHOR = "Ⅰ\t" + CODE          # 插在它之前


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
    lines = open(LOCAL, encoding="utf-8").read().split("\n")

    if f"{WORD}\t{CODE}" in lines:
        print(f"{WORD}\\t{CODE} 已存在，无需补")
        return

    idx = None
    for i, line in enumerate(lines):
        if line == ANCHOR:
            idx = i
            break
    if idx is None:
        raise SystemExit(f"找不到锚点 {ANCHOR!r}，请人工确认")

    lines.insert(idx, f"{WORD}\t{CODE}")
    open(LOCAL, "w", encoding="utf-8").write("\n".join(lines))
    print(f"已补 {WORD}\\t{CODE}（在第 {idx} 行前）")


if __name__ == "__main__":
    main()