# Fork 下游发布交接文档（基于 rimeinn/rime-JDhe 适配 CyIME）

> 本包是 **Fork 自 [`rimeinn/rime-JDhe`](https://github.com/rimeinn/rime-JDhe) 的下游覆盖包**。直接将本包全部文件解压覆盖到你 Fork 后的仓库根目录即可提交推送，无需重复存放 73 MB 大文件。

> **发布时的命名调整**：原始覆盖包把主方案命名为 `simplehe`；本仓库已按上游仓库名统一改为 **`jde`**（`jde.schema.yaml` / `jde.dict.yaml` / `jde_pinyin.schema.yaml`，方案 id 与上游主方案一致、显示名沿用上游的「简单鹤」），下文文件名同步为改名后的写法。

---

## 1. 上下游关系（给发布 AI 编写 README / Release 用）

- **上游仓库**：[rimeinn/rime-JDhe](https://github.com/rimeinn/rime-JDhe)（GPL-3.0）
- **目标客户端**：[Cyletix/CyIME](https://github.com/Cyletix/CyIME)（Android Rime，下载页：[CyIME Releases (Latest)](https://github.com/Cyletix/CyIME/releases/latest)）
- **下游定位**：在完整保留上游桌面版文件的基础上，新增针对 CyIME 安卓端的独立入口方案 `jde.schema.yaml`，并修复上游词库在手机端的兼容性问题。

---

## 2. 本包覆盖 / 新增的文件清单（其余文件直接继承上游）

### 新增 / 改写的 CyIME 入口文件
- `jde.schema.yaml`：CyIME 主方案（`version: "9.3"`、`author: 简单`、`language: zh`；挂载 `jde_fixed` + `jdh_sentence` + 魔然 Lua + OpenCC 拆分 + `` ` ``/`oiz` 反查；移除 `#` 与 `/` 防符号直出；统一注释为 `[字根·形码]`）。
- `jde_fixed.schema.yaml`：CyIME 专用的 `jde_fixed` 内部编译方案（不依赖桌面 `config_base.yaml`）。
- `jdh_sentence.schema.yaml` & `jdh_sentence.dict.yaml`：模块化整句编译方案，**通过 `import_tables` 直接复用上游 `cn_dicts/pinyin/*`**（单文件均低于 45 MB，完全避开 GitHub 50 MB 大文件警告），并补齐 19 组小鹤飞键与用户调频。
- `jde_pinyin.schema.yaml` & `jde.dict.yaml`：独立反查方案与单字混合反查词典（注释格式同步为 `[字根·形码]`）。
- `lua/chaifen_toggle.lua`：手机端状态感知开关（空输入按 `` ` `` 进反查，输入中按 `` ` `` 切换实时拆分）。
- `fonts/ChaiPUA.ttf` & `fonts/xime.custom.snippet.yaml`：与上游 `opencc/jdh_cf.ocd2` 配套的拆分字体及 CyIME 防覆盖配置片段。
- `README_CyIME.md`：CyIME 用户安装与使用指南。
- `.gitignore`：忽略 Rime 编译产物（`*.bin`、`*.userdb/`、`build/`、`sync/`）。

### 清洗修复的上游词库文件（直接覆盖上游同名文件）
- `cn_dicts/jde/jde.dict.yaml` & `cn_dicts/jde/jde_ext.dict.yaml`：清理了 **14,111 条** PC 端 `①` 占位词条（解决手机端 `marw` 等四码单字首选为 `①` 的问题）。
- `cn_dicts/pinyin/base.dict.yaml` & `cn_dicts/pinyin/41448.dict.yaml`：剔除上游 `base` 中 **165 条**无拼音残缺词条，修正 `41448` 中 `貒 tuan;UE` 为小写 `tuan;ue`。

### 直接继承上游的文件（本包未重复包含）
- `jde_fixed.dict.yaml`、`cn_dicts/my_user.dict.yaml`
- `cn_dicts/pinyin/{8105,tencent,moe,words}.dict.yaml`
- `lua/moran*.lua`（6 个核心脚本）
- `opencc/jdh_cf.json` & `opencc/jdh_cf.ocd2`
- `LICENSE`（GPL-3.0）

---

## 3. 给发布 AI 的操作指引

1. **Git 提交**：Fork `rimeinn/rime-JDhe` 后，将本覆盖包解压覆盖到仓库根目录，`git status` 确认无 >50 MB 新增单文件后即可正常 `git push`。
2. **README 编写**：在仓库根目录保留或更新 `README.md`，说明本仓库为 `rimeinn/rime-JDhe` 的 CyIME 下游适配版，并将 `README_CyIME.md` 作为 CyIME 用户的安装与使用说明（重点提示 `fonts/xime.custom.snippet.yaml` 需合并进 `xime.custom.yaml`，不可整文件覆盖）。
3. **GitHub Release 打包**：发布 Release 时，打包供 CyIME 用户直接导入的精简包，只需包含：`jde.schema.yaml`、`jde_fixed.schema.yaml`、`jde_fixed.dict.yaml`、`jdh_sentence.schema.yaml`、`jdh_sentence.dict.yaml`、`jde_pinyin.schema.yaml`、`jde.dict.yaml`、`cn_dicts/jde/*`、`cn_dicts/pinyin/*`、`cn_dicts/my_user.dict.yaml`、`lua/moran*.lua`、`lua/chaifen_toggle.lua`、`opencc/jdh_cf.*`、`fonts/*`、`README_CyIME.md`。
