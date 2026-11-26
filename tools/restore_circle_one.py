#!/usr/bin/env python3
"""补回被「清理 ① 占位」误删的正规 ①。

背景
----
本仓库为修「四码单字首选是 ①」，早期删除了 cn_dicts/jde/ 里大量含 ① 的词条。
上游 V9.1.0 日志原文：

    32. ①在一些四码符号处有冗余，删掉。

即只删**冗余**的 ①。但有两类 ① 是正规的，不该删：

1. `oy` 系列（`oy` + 数字键盘键位）的 1 号位：
       oyy → ① Ⅰ ㊀ （一） -1
   它没有 ② 同码（② 在 `oye`），所以不能用序列判定，需显式列出。

2. 符号组里 `①` 与 `②` 同码共存，说明 ① 是序列成员：
       ofyu → ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩
   这类用「① 与 ② 同码」自动判定。

判定为**冗余**的（保持删除）：
- 四码二位数符号：`oyyy` → `① ⑪`、`oyye` → `① ⑫` …
- 其余短码的 ①（`ck`/`ez`/`hq`/`kn` … 共 29 条）—— 维护者主动删除，不在补回范围

用法
----
    python3 tools/restore_circle_one.py
"""
import os
import sys
import urllib.request

UPSTREAM = ("https://raw.githubusercontent.com/rimeinn/rime-JDhe/"
            "main/cn_dicts/jde/jde.dict.yaml")
LOCAL = "cn_dicts/jde/jde.dict.yaml"
CACHE = "/tmp/up_jde.yaml"

# 显式列出：① 在这些码里是正规的，但同码没有 ② 可用于判定
EXPLICIT = {"oyy"}


def load_upstream():
    if os.path.isfile(CACHE) and os.path.getsize(CACHE) > 1_000_000:
        return open(CACHE, encoding="utf-8", errors="replace").read().split("\n")
    print("下载上游:", UPSTREAM)
    raw = urllib.request.urlopen(UPSTREAM, timeout=120).read().decode("utf-8")
    with open(CACHE, "w", encoding="utf-8") as fh:
        fh.write(raw)
    return raw.split("\n")


def parse_rows(lines, has_header):
    """解析成 {code: [word...]}，保持文件顺序"""
    data = {}
    body = lines
    if has_header:
        txt = "\n".join(lines)
        i = txt.find("\n...\n")
        body = txt[i + 5:].split("\n") if i >= 0 else lines
    for line in body:
        if not line or line.startswith("#") or "\t" not in line:
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        data.setdefault(parts[1].strip(), []).append(parts[0].strip())
    return data


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
    up = parse_rows(load_upstream(), False)
    local_lines = open(LOCAL, encoding="utf-8").read().split("\n")
    loc = parse_rows(local_lines, True)

    # 找出该保留但本地缺失的 (码, ①)
    targets = []
    for code, words in up.items():
        if "①" not in words:
            continue
        if "①" in loc.get(code, []):
            continue
        # ① 与 ② 同码 → 序列成员
        if "②" in words:
            targets.append((code, "序列：①与②同码"))
    for code in EXPLICIT:
        if "①" in up.get(code, []) and "①" not in loc.get(code, []):
            targets.append((code, "显式列出"))

    if not targets:
        print("无缺失，退出")
        return

    print(f"需补回 {len(targets)} 条：")
    for code, why in targets:
        # 插到同码第一条之前
        idx = None
        for i, line in enumerate(local_lines):
            if "\t" not in line:
                continue
            if line.split("\t")[1].strip() == code:
                idx = i
                break
        if idx is None:
            print(f"  [跳过] {code} 本地无此码")
            continue
        local_lines.insert(idx, f"①\t{code}")
        print(f"  [补] ①\t{code}  ({why})")

    open(LOCAL, "w", encoding="utf-8").write("\n".join(local_lines))
    print("已写入", LOCAL)


if __name__ == "__main__":
    main()