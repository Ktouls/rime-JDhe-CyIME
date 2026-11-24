# 简单鹤（JDhe）v9.3 安装与使用指南

适用于 **Android + [CyIME](https://github.com/Cyletix/CyIME/releases/latest)**。桌面端（Weasel / Squirrel / fcitx5）请使用上游 [rimeinn/rime-JDhe](https://github.com/rimeinn/rime-JDhe)。

---

## 一、导入方案

1. 在 GitHub 仓库页点绿色 **`Code`** → **`Download ZIP`**，得到本仓库的完整压缩包。
2. 用手机自带文件管理器（或 MT、ZArchiver）**解压**到任意临时目录。
3. 将解压出的全部内容移动到 CyIME 的 **Rime 用户目录**：
   - 文件：`jde.schema.yaml`、`jde_fixed.schema.yaml`、`jde_fixed.dict.yaml`、`jdh_sentence.schema.yaml`、`jdh_sentence.dict.yaml`、`jde_pinyin.schema.yaml`、`jde.dict.yaml`
   - 目录：`cn_dicts/`、`lua/`、`opencc/`、`fonts/`
4. 注意不要把 ZIP 里那一层外层文件夹一起搬进去，否则 Rime 读不到方案。

---

## 二、配置拆分字体（防方框 / 防 `☒`）

拆分注释依赖 `fonts/ChaiPUA.ttf`（与 `opencc/jdh_cf.ocd2` 配套）。

| 你的情况 | 做法 |
|---|---|
| Rime 目录下**没有** `xime.custom.yaml` | 把 `fonts/xime.custom.snippet.yaml` 复制到 Rime 根目录，改名为 `xime.custom.yaml` |
| 目录下**已有** `xime.custom.yaml` | 只把下面三行**合并**进现有文件，**切勿整文件覆盖** |

```yaml
keyboard:
  fonts:
    comment_font: fonts/ChaiPUA.ttf
```

整文件覆盖会丢掉你已有的键盘布局、候选样式、配色等全部自定义设置。

---

## 三、部署与启用

1. 打开 CyIME → 设置 → 点 **重新部署**。
2. 首次部署要编译全量整句词库（合计 80 MB 左右），**约需数十秒**，期间无进度条属正常，请勿强杀进程。
3. 部署完成后在「语言与方案」中**只勾选「简单鹤」**。
   - `jde_fixed`、`jdh_sentence`、`jde_pinyin` 都是被依赖的内部方案，勾选会引入多余候选。
4. 若方案列表里看不到「简单鹤」，请确认 `jde.schema.yaml` 位于 Rime 用户目录根部，然后重新部署。

---

## 四、日常操作

| 场景 | 操作 | 结果 |
|---|---|---|
| 打字 / 简拼 / 整句 | 小鹤双拼 + 形码直接输入 | 整句中补 2 位形码请在其后加 `o`（如 `yzdmpnowfti`） |
| 实时拆分 | 有编码输入时按 **`` ` ``** | 候选注释在 `不拆` / `扌斥` 之间切换（实体键盘 `Ctrl+i`） |
| 默认常驻拆分 | 改 `jde.schema.yaml` 的 `chaifen: reset:` | `0` → `1` |
| 拼音 / 双拼反查 | **空输入**时按 **`` ` ``** 再打拼音 | 候选显示 `[字根·形码]` |
| 部件拆字 | `oiz` + 部件读音（**全拼**） | 查生僻字 |
| 自造词 | 输入 `//` | 魔然加词入口 |
| 简快码提示 `⌃` | 改 `jde.schema.yaml` 的 `moran:` 段 | `quick_code_indicator: ""` 或 `enable_quick_code_hint: false` 即可关闭 |

---

## 五、常见问题

- **` 键没有反应**：确认 `lua/chaifen_toggle.lua` 已放入 `lua/` 目录，且 `jde.schema.yaml` 的 `processors` 第一项是 `lua_processor@*chaifen_toggle`。
- **候选出现方框**：字体片段没合并，或 `xime.custom.yaml` 里 `comment_font` 路径不是 `fonts/ChaiPUA.ttf`。
- **四码单字首选是 `①`**：词库没被本仓库版本覆盖，重新按第一节导入并重新部署。
- **部署卡住 / 内存紧张**：先删除 Rime 目录下的 `build/` 再部署；本仓库已剔除桌面 `.gram` 语言模型与 `predict.db`，正常不会卡顿。
- **想恢复桌面功能**：直接使用上游 [rimeinn/rime-JDhe](https://github.com/rimeinn/rime-JDhe)。

---

## 六、许可与致谢

方案沿用上游 **GPL-3.0**（见 [LICENSE](LICENSE)）。码表作者「简单」，Lua 引擎来自 [魔然 Project Moran](https://github.com/ksqsf/rime-moran)，上游为 [rimeinn/rime-JDhe](https://github.com/rimeinn/rime-JDhe)，客户端为 [Cyletix/CyIME](https://github.com/Cyletix/CyIME)。