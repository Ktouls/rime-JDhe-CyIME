#!/usr/bin/env python3
"""从提交 3bfc892（v9.3 首发打包点）重建原始发布包。

用于回滚：把误替换的 release 附件还原成 v9.3 首发时的内容。
输出到 /tmp/rollback/，结构与原包一致（29 项，顶层目录按包区分）。
"""
import os
import subprocess
import sys
import zipfile

REPO = "/workspace/rime-JDhe-CyIME"
COMMIT = "3bfc892"
OUTDIR = "/tmp/rollback"

# 原包 29 项清单（来自 3bfc892 与旧包实际内容的交集）
FILES = [
    "README_CyIME.md",
    "simplehe.schema.yaml",
    "jde_fixed.schema.yaml",
    "jde_fixed.dict.yaml",
    "jdh_sentence.schema.yaml",
    "jdh_sentence.dict.yaml",
    "simplehe_pinyin.schema.yaml",
    "simplehe.dict.yaml",
    "cn_dicts/jde/jde.dict.yaml",
    "cn_dicts/jde/jde_ext.dict.yaml",
    "cn_dicts/my_user.dict.yaml",
    "cn_dicts/pinyin/41448.dict.yaml",
    "cn_dicts/pinyin/8105.dict.yaml",
    "cn_dicts/pinyin/base.dict.yaml",
    "cn_dicts/pinyin/moe.dict.yaml",
    "cn_dicts/pinyin/tencent.dict.yaml",
    "cn_dicts/pinyin/words.dict.yaml",
    "lua/chaifen_toggle.lua",
    "lua/moran.lua",
    "lua/moran_express_translator.lua",
    "lua/moran_hint_filter.lua",
    "lua/moran_ijrq_filter.lua",
    "lua/moran_pin.lua",
    "lua/moran_reorder_filter.lua",
    "lua/zrmdb.txt",
    "opencc/jdh_cf.json",
    "opencc/jdh_cf.ocd2",
    "fonts/ChaiPUA.ttf",
    "fonts/xime.custom.snippet.yaml",
]

PACKAGES = [
    ("JDhe-CyIME-v9.3.zip", "JDhe-CyIME-v9.3", 27083448),
    ("jde-9.3.zip", "jde-9.3", 27080990),
]


def read_blob(rel):
    """从指定提交读出文件原始字节"""
    out = subprocess.check_output(
        ["git", "show", f"{COMMIT}:{rel}"], cwd=REPO)
    return out


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    # 先确认所有文件在该提交中存在
    for rel in FILES:
        try:
            read_blob(rel)
        except subprocess.CalledProcessError:
            raise SystemExit(f"提交 {COMMIT} 中不存在: {rel}")

    for name, top, expect in PACKAGES:
        path = os.path.join(OUTDIR, name)
        if os.path.exists(path):
            os.remove(path)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for rel in FILES:
                z.writestr(top + "/" + rel, read_blob(rel))
        size = os.path.getsize(path)
        print(f"{name}: {size} bytes (原始 {expect}, 差 {size-expect:+d})")


if __name__ == "__main__":
    main()