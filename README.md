# 简单鹤（JDhe）· CyIME 安卓适配版 v9.3

> 本仓库是 **[rimeinn/rime-JDhe](https://github.com/rimeinn/rime-JDhe)**（GPL-3.0，作者：简单）的 **CyIME 安卓下游适配版**。
> 保留上游全部打字核心（9.3.0 码表、魔然 Lua 引擎、小鹤飞键、OpenCC 实时拆分），针对 Android 端重做入口方案 `jde`，并清理手机上用不到的桌面资产。

[![Release](https://img.shields.io/github/v/release/Ktouls/rime-JDhe-CyIME?label=release)](https://github.com/Ktouls/rime-JDhe-CyIME/releases)
[![License: GPL-3.0](https://img.shields.io/badge/license-GPL--3.0-blue)](LICENSE)
[![Fork of rime-JDhe](https://img.shields.io/badge/fork-rimeinn%2Frime--JDhe-informational)](https://github.com/rimeinn/rime-JDhe)

| 用途 | 链接 |
|---|---|
| 客户端下载 | **[CyIME Releases (Latest)](https://github.com/Cyletix/CyIME/releases/latest)** |
| 一键取方案 | 本页绿色 `Code` → `Download ZIP` |
| 本次发布 | [v9.3 Release](https://github.com/Ktouls/rime-JDhe-CyIME/releases/tag/v9.3)（`JDhe-CyIME-v9.3.zip` 手工导入用，`jde-9.3.zip` 为方案商店包） |
| 使用说明 | [README_CyIME.md](README_CyIME.md) |
| 上游原版 | [rimeinn/rime-JDhe](https://github.com/rimeinn/rime-JDhe) |
| 交接说明 | [GITHUB_HANDOFF.md](GITHUB_HANDOFF.md) |

---

## 一、30 秒安装

1. 安装 [CyIME](https://github.com/Cyletix/CyIME/releases/latest)。
2. 打开本仓库主页 → 绿色 **`Code`** → **`Download ZIP`**。
3. 把 ZIP **解压后**的全部内容（`*.schema.yaml`、`*.dict.yaml`、`cn_dicts/`、`lua/`、`opencc/`、`fonts/`、`other/`）放进 CyIME 的 **Rime 用户目录**（不要只放 ZIP，也不要保留外层文件夹）。
4. **字体防方框**（详见下一节）：把 `fonts/xime.custom.snippet.yaml` 里的三行并入 `xime.custom.yaml`。
5. 在 CyIME 中点 **重新部署**。首次编译全量整句词库约需数十秒，请耐心等待，不要强杀进程。
6. 「语言与方案」里**只启用「简单鹤」**。`jde_fixed`、`jdh_sentence`、`jde_pinyin` 是内部依赖方案，不要单独启用。

---

## 二、拆分字体配置（重要）

拆分注释依赖 `fonts/ChaiPUA.ttf`，与上游 `opencc/jdh_cf.ocd2` 配套，用于修复「将」等字显示 `☒` 缺字。

- **没有** `xime.custom.yaml` 时：把 `fonts/xime.custom.snippet.yaml` 复制到 Rime 根目录并改名为 `xime.custom.yaml`。
- **已有** `xime.custom.yaml` 时：只把下面三行**合并**进去，**切勿整文件覆盖**（否则会丢掉你原有的键盘、布局、配色等设置）。

```yaml
keyboard:
  fonts:
    comment_font: fonts/ChaiPUA.ttf
```

---

## 三、日常使用速查

| 场景 | 操作 | 说明 |
|---|---|---|
| 打字 / 简拼 / 整句 | 直接输入小鹤双拼 + 形码 | 整句中补 2 位形码在形码后加 `o`，例如 `yzdmpnowfti` |
| **实时拆分开关** | 有输入时按 **`` ` ``**（实体键盘 `Ctrl+i`） | 由 `lua/chaifen_toggle.lua` 控制，候选注释在 `不拆` / `扌斥` 间切换；想默认常开可把 `jde.schema.yaml` 里 `chaifen` 的 `reset: 0` 改为 `1` |
| 拼音 / 双拼反查 | **空输入**时按 **`` ` ``** 再打拼音 | 候选统一显示 `[字根·形码]` |
| 部件拆字反查 | `oiz` + 部件读音（**全拼**） | 复用内置 `radical_pinyin`（词典与编译均来自 CyIME 内置，不随包分发），适合查生僻字 |
| 关闭 `⌃` 简快码提示 | 改 `jde.schema.yaml` 的 `moran:` 段 | `quick_code_indicator` 置空，或 `enable_quick_code_hint: false` |
| 造词 | 输入 `//` | 魔然 `panacea` 加词 |

---

## 四、文件清单

| 文件 / 目录 | 作用 |
|---|---|
| `jde.schema.yaml` | 主方案「简单鹤」（id `jde`，与上游同名）：9.3 固词 + 整句 + 魔然 Lua + OpenCC 拆分 + 反引号反查 + `oiz` 拆字 |
| `jde_fixed.schema.yaml` / `jde_fixed.dict.yaml` / `cn_dicts/jde/*` | 9.3.0 固定简码表（已清理 `①` 占位符） |
| `jdh_sentence.schema.yaml` / `jdh_sentence.dict.yaml` | 清洗后的全量带形码整句词库，19 组飞键规则，模块化 `import_tables` |
| `jde_pinyin.schema.yaml` / `jde.dict.yaml` | 独立拼音反查方案与单字混合反查词典 |
| `cn_dicts/pinyin/{8105,41448,base,words,tencent,moe}.dict.yaml` | 整句模块化词库，单文件均 < 45 MB |
| `cn_dicts/my_user.dict.yaml` | 用户词组 |
| `lua/moran*.lua`、`lua/chaifen_toggle.lua`、`lua/zrmdb.txt` | 魔然核心脚本、手机端拆分开关、字根/辅码表 |
| `opencc/jdh_cf.json` / `opencc/jdh_cf.ocd2` | 官方简单鹤字根拆分词典 |
| `fonts/ChaiPUA.ttf` / `fonts/xime.custom.snippet.yaml` | 配套拆分字体与防覆盖配置片段 |
| 部件拆字反查 | 复用 CyIME 内置 `radical_pinyin` 方案（`oiz` + 部件全拼，词典与编译产物均来自内置，不随包分发） |
| `other/` | 上游字根图、更新日志、容错统计等资料 |

---

## 五、相对上游做了哪些改动

**新增（CyIME 入口与适配）**

- 新增主方案 `jde`，挂载 `jde_fixed` + `jdh_sentence` + 魔然 Lua + OpenCC 拆分 + 反引号反查，移除 `#` 与 `/` 的符号直出，`version: "9.3"`、`author: 简单`、`language: zh`。
- `jde_fixed`、`jdh_sentence` 改为不依赖桌面 `config_base.yaml` 的独立编译方案；`jdh_sentence` 通过 `import_tables` 复用 `cn_dicts/pinyin/*`，避开 GitHub 50 MB 单文件限制。
- 新增 `lua/chaifen_toggle.lua`（空输入按 `` ` `` 反查、输入中按 `` ` `` 切换拆分）与 `fonts/xime.custom.snippet.yaml`。

**清洗（手机端兼容性修复）**

- 移除 `cn_dicts/jde/` 中 **14,111 条** PC 端 `①` 占位词条（主码表 5,999 + 扩展 8,112），解决 `marw` 等四码首选被 `①` 抢占。
- 剔除 `cn_dicts/pinyin/base.dict.yaml` 中 **165 条**无拼音残缺词条，修正 `41448` 中 `貒 tuan;UE` → `tuan;ue`。
- 整句词库清洗 **152 条**无拼音残缺词条、**7 条**大写编码混杂词条，补齐 **19 组**小鹤飞键，恢复用户调频（锁定 1–2 码短码不参与调频）。
- 拆分注释格式统一为 `[字根·形码]`，修复多字节正则导致的 `··` 双点。

**清理（桌面端专用，手机用不到）**

- 删除上游的桌面入口 `jde.schema.yaml`（依赖 `reverse_pinyin`、`melt_eng`、图标与桌面 Lua 的那份）、`tiger.*`、`stroke.*`、`default.yaml`、`squirrel.yaml`、`squirrel.custom.yaml`、`*.gram`（约 51 MB 桌面语言模型）、`predict.db`（约 7 MB）。
- 同时移除依赖上述方案的桌面附属资产：`ico/`、`config_*.yaml`、`custom(自定义参考)/`、`en_dicts/`、`melt_eng.*`、`pinyin.*`、`reverse_pinyin.*`、`charset.*`、`sentence.schema.yaml`，以及 `lua/` 下的计算器、快捷启动等桌面脚本。上游原版需要这些功能时请直接使用上游仓库。

**工程**

- 主方案沿用上游的 id `jde` 与显示名「简单鹤」，但**同名不同内容**：本仓库的 `jde.schema.yaml` 是 CyIME 专用入口（不依赖桌面 `config_base.yaml`、`reverse_pinyin`、`melt_eng`、图标），上游的桌面版 `jde.schema.yaml` 未保留。改方案内容时请以本仓库这份为准，不要把上游那份直接覆盖回来，否则会缺依赖、装不上。
- `.gitignore` 忽略 `*.bin`、`*.userdb/`、`build/`、`sync/`、`*.gram`、`predict.db` 等编译产物，仓库内无任何产物文件。
- 全仓单文件最大 43.6 MB（`cn_dicts/pinyin/base.dict.yaml`），低于 GitHub 50 MB 警告线与 100 MB 硬限制。

---

## 六、致谢

- **码表作者「简单」** —— 简单鹤码表、字根体系与全部词库；本仓库只是它的安卓搬运与清洗。
- **[魔然 Project Moran](https://github.com/ksqsf/rime-moran)** —— 固词标记 `⌃`、出简让全、简快码提示、置顶造词、`//` 自造词等 Lua 引擎能力，`lua/moran*.lua` 与 `zrmdb.txt` 均来自魔然。
- **[rimeinn/rime-JDhe](https://github.com/rimeinn/rime-JDhe)** —— 本仓库的直接上游与全部桌面配置来源（GPL-3.0）。
- **[Cyletix/CyIME](https://github.com/Cyletix/CyIME)** —— 安卓端 Rime 客户端与内置 `radical_pinyin` 支持。
- 上游 README 中致谢的参考方案：[雾凇拼音](https://github.com/iDvel/rime-ice)、[飞鹤快拼](https://github.com/boomker/rime-fast-xhup)、[部件拆字方案](https://github.com/mirtlecn/rime-radical-pinyin)、[白霜拼音](https://github.com/gaboolic/rime-frost)、[虎码输入方案](https://github.com/ywxt/rime-huma)、[薄荷拼音](https://github.com/Mintimate/oh-my-rime)。

---

## 七、许可

本项目沿用上游 **GPL-3.0** 许可，见 [LICENSE](LICENSE)。分发、修改请同样遵循 GPL-3.0，并保留上游与本致谢。