# PDA 视觉契约 1.0.0

## 基线与优先级

源码基线：`wms-pda-front@be27cf4`，提取日期 2026-10-15。标准资产在本技能内，不依赖原项目的路径、服务器、账号或历史对话。明确的用户要求优先；没有明确风格变更时，以 manifest 锁定的 CSS/组件为准，再参考本说明与截图。下面数值是资产的解释，修改标准须同步更新两者。

## 颜色、字体与尺寸

| 用途 | 固定值 | 实现 |
| --- | --- | --- |
| 主文案 | `#20334a` | `--pda-ink` |
| 标签/辅助文案 | `#61748b` | `--pda-muted` |
| 背景 / 面板 | `#f0f4f8` / `#ffffff` | `--pda-bg` / `--pda-surface` |
| 边线 / 标题栏 | `#dce5ef` / `#173553` | `--pda-line` / `--pda-navy` |
| 主操作 | `#1769ba` | `--el-color-primary`，浅色阶见标准 CSS |
| 标题栏底边 | `#53b4bf`，3px | 保留位置与厚度，不扩展为装饰渐变 |
| 成功 / 危险 | `#16836d` / `#cf4050` | 状态颜色，业务确认常规使用 primary |
| 正文字体 | Segoe UI、PingFang SC、Microsoft YaHei、sans-serif | 不引入远程字体 |
| 工具标识 | Consolas、monospace | WMS / PDA 等短标识，字距 1px |
| 字号 | 正文/按钮 14px；输入 16px；移动标签 13px | 页面标题 18px/650，行高 1.4 |
| 触控高度 | 控件 ≥44px；底部按钮 ≥46px；登录输入/按钮 ≥48px | 不依赖 Element Plus 默认 32px |
| 圆角 | 基础控件 8px；主面板 12px；明细 10px；登录卡 16px | 不用胶囊式主按钮 |

普通作业页使用平面、清晰的工业终端视觉；除既有登录背景/极浅阴影外，不添加大面积渐变、玻璃效果、悬浮装饰、营销标语或展示型大数字。

## 作业页骨架

```text
PdaPage（100% / 100dvh，纵向 flex）
├─ header：返回按钮 + h1 标题 + PDA 标识，最小高 64px，底边 3px
├─ body：flex:1 / min-height:0 / overflow:auto
│  └─ panel：白色，最大宽 760px，居中
│     ├─ itemLine：字段标签 + 输入/选择/只读值
│     └─ itemDivBig：12px 间隔的明细卡片或 el-empty
└─ actions：白底顶部分割线，独立于内容滚动，安全区底距
```

- 标准内容外边距 16px，面板 padding 20px；小于 480px 时分别 12px/16px。
- 表单行间距 16px，标签宽 112px，横向间隙 12px。小于 480px 时标签占整行，行内纵向间距 7px。
- 明细容器上距 20px，卡片 body padding 16px，明细行间距 10px；移动明细列为 `minmax(80px, 38%) minmax(0, 1fr)`。
- 长物料名、批次、条码换行；数量可使用 tabular-nums。不要通过省略内容解决明细溢出。
- 底部 padding 12px 16px，底部至少 safe-area；按钮间距 10px，flex 换行，basis 100px。返回/切换默认按钮，确认 primary。不要把所有按钮设为 danger。
- 只读字段保留可识别底色 `#f3f7fb` 与数据色 `#27667b`；禁用字段使用主题定义的可读颜色，不能看起来像空白。

## 查询、弹窗与反馈

- 表格使用 el-table，必要时 column min-width；横向滚动留在表格内，禁止整个页面横向滚动。表头 `#edf3f9`，单元格上下 12px。
- 移动分页 `total, prev, jumper, next`，按钮 44px，允许 total 单独占行。不要用 transform 缩小，不能使用非法 `pager-count=3`。
- 切换条件时查询第 1 页，翻页使用同一条件；异步请求保持 total，不先置 0。保留旧结果并显示 loading；失败时停止 loading 并保留可重试路径。
- 弹窗宽 `min(480px, calc(100vw - 32px))`，padding 20px，圆角 12px，标题 18px；头/尾有分隔线，footer 按钮 gap 10px。不要设 width=100% 或只设桌面固定宽。
- 确认框宽 420px、最大 `100vw - 32px`。消息最大 `100vw - 24px`，文字允许换行。
- 消息、确认框与对话框可能 Teleport 到 body，因此主题不能全部包进业务页 scoped 样式。
- 空明细使用 el-empty，作业页 image-size=64；菜单加载用 el-skeleton，失败用 el-result + 重试，空权限单独提示。不可用成功占位假装业务请求已完成。

## 登录与菜单

- 登录：背景沿用标准 SCSS 渐变；白卡最大 400px，padding 28px、顶蓝边 4px；logo 保留项目原图，最大展示宽 90px；主标题 23px。语言选择放卡片右上，字段标签在上，输入/按钮 48px。
- 菜单：同色标题栏 + 3px 底边；内容最大 760px；默认两列，≥640px 三列，gap 12px；作业按钮最小高 106px、圆角 12px、白底，图标 22px/蓝色，文字 14px/600。≤340px 标题/语言允许换行、网格 gap 8px。
- 作业图标按语义选用 Box/Download/Upload/Search/RefreshLeft/Connection/Grid 等 SVG；不要恢复旧 font-class 字符串。后台菜单名称与权限筛选由业务层提供，不能凭视觉需要新增作业入口。

## 与业务的接口

模板里的 `code/name/qty/id`、`scan-tray`、`search` 是 UI 示例，不是 WMS 字段标准。按已有接口映射，不重命名后端契约。为保持截图可重复，可以在独立临时预览中注入明确标注的模拟数据；不得把模拟请求处理写入正式入口。

`PdaPage` 不负责路由、鉴权或请求。它只接收 title、发出 back、渲染 default/actions 插槽。保留 ref 在原页面作用域，以现有 mounted/activated 或用户流程管理焦点。

## 不允许的风格漂移

- 在页面覆盖 `--pda-*`、Element Plus 主色/字体/尺寸变量，或重写 `.pda-page*`、`.body .itemLine`、通用 `.el-*` 尺寸。
- 红色标题栏、全红按钮、10–12px 主字体、small/mini 全局控件、旧 el-icon 字体、Element UI 的 slot/.sync/type=text 写法。
- 负边距、缩放分页、window.screen 高度运算、fixed 底部按钮、78% 明细容器、重复滚动条、复制另一套主题。
- 为追求“更漂亮”改字体/圆角/色板/间距，未说明用户批准的偏离，或在工具不可用时伪造视觉通过。
