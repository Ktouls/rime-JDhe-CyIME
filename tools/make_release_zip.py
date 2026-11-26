#!/usr/bin/env python3
"""按仓库当前内容重建 v9.3 发布包（两者同源，仅顶层目录名不同）。

旧包 JDhe-CyIME-v9.3.zip / jde-9.3.zip 是 11-24 打的，之后有 4 次提交
（oiz 修复、商店收录适配、命名调整、oyy 修复），因此必须重打而不是重传。

文件清单与旧包严格一致（29 项），顶层目录名按包区分：
    JDhe-CyIME-v9.3.zip  → JDhe-CyIME-v9.3/
    jde-9.3.zip          → jde-9.3/
"""
import os
import sys
import zipfile

REPO = "/workspace/rime-JDhe-CyIME"
FILES = [
    "README_CyIME.md",
    "xime.custom.yaml",
    "jde.schema.yaml",
    "jde_fixed.schema.yaml",
    "jde_fixed.dict.yaml",
    "jdh_sentence.schema.yaml",
    "jdh_sentence.dict.yaml",
    "jde_pinyin.schema.yaml",
    "jde.dict.yaml",
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
    ("JDhe-CyIME-v9.3.zip", "JDhe-CyIME-v9.3"),
    ("jde-9.3.zip", "jde-9.3"),
]


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "/workspace"
    missing = [f for f in FILES if not os.path.isfile(os.path.join(REPO, f))]
    if missing:
        raise SystemExit("仓库缺少文件: " + str(missing))

    for name, top in PACKAGES:
        path = os.path.join(outdir, name)
        if os.path.exists(path):
            os.remove(path)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for rel in FILES:
                src = os.path.join(REPO, rel)
                z.write(src, top + "/" + rel)
        print(f"{name}: {os.path.getsize(path)} bytes, {len(FILES)} 条目")

        # 立即校验要点
        with zipfile.ZipFile(path) as z:
            data = z.read(top + "/cn_dicts/jde/jde.dict.yaml").decode("utf-8", "replace")
            ok = "\n①\toyy\n" in data or data.startswith("①\toyy\n")
            print(f"   含『①\\toyy』= {ok}")
            if not ok:
                raise SystemExit("打包结果缺少 oyy 的 ①，中止")


if __name__ == "__main__":
    main()