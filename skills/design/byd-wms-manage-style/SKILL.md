---
name: byd-wms-manage-style
description: "为 Vue 3 + Element Plus 桌面管理端新增、改造或检查页面，复用 BYD WMS 蓝白主题、紧凑左排查询区、small 工具栏、40px 居中选择/序号列及统一弹窗。用于按本轮管理端标准统一样式；不用于 PDA、大屏、IO、3D 或打印布局。"
---

# BYD WMS 管理端统一样式

版本 `1.0.0`。复现已确认的管理端风格，不重新设计。人类开发者与不同 AI 模型使用同一套主题、模板、检查与验收标准；不要仅凭文字描述重新生成一套近似样式。

## 开始工作

先读目标仓库的 AGENTS.md，确认框架、主题入口、缩放、业务页及原处理函数。编码前读[固定样式契约](references/style-contract.md)。在 `wms-manage-font` 内工作时，再读[现有项目适配](references/project-adapter.md)，复用原主题、配置解析和事件；不得为了套模板改后端契约。

适用基线是 Vue `3.5.44`、Element Plus `2.14.7`、图标包 `2.3.2`，不代表自动升级到这些版本或“最新版”。其它框架说明兼容差异，仍按用户范围做事；不自动迁移框架、替换登录或修改构建缩放。

## 固定决策

1. 颜色、字体、间距和圆角取[标准主题](assets/runtime/native-management.scss)。主色 `#1758A7`、背景 `#F3F6FA`、白卡片、正文 `#263445`、辅助色 `#66758A`、边框 `#E2E8F0`；正文设计 14px、区块标题 16px。已有明确品牌覆盖须保留并记录，不能让模型自行调色。
2. 普通查询与编辑控件显式 `size="default"`。工具栏、查询按钮、行内操作及密集编辑显式 `small`；弹窗底部按钮 `default`。全局默认尺寸不能代替这些声明。
3. 查询区上下设计间距 **8px**、左右 **16px**；条件以 **320px** 设计列宽从左紧凑排列，行/列间隔 **8/16px**，不够宽时换行。去掉旧最小高度、列 padding-bottom、form-item margin-bottom 的叠加。不能恢复每字段占半行的分散布局。
4. 新增或本次调整的选择列、序号列使用原生 `width="40"`，不是 `min-width`；`align="center"` 和 `header-align="center"`。序号左右设计 padding 4px、不换行；选择单元格内部居中。旧页面未触及的兼容列不据此批量重写。
5. 查询、保存是主操作；重置、取消是普通操作；删除是危险色。图标用官方 SVG，业务字体图标只放图标节点，不能挂在按钮上。无有效图标时显示业务名称；图标按钮必须有辅助名称。
6. 动态名称按当前语言、兼容语言码、既有有效翻译、配置标题、已识别动作读取。**无有效名称且无可识别动作的记录隐藏**，不能用权限组名或“未命名操作”充当业务名称。只过滤显示，保留原对象、顺序、权限与点击参数；全部无效的弹窗保留取消，不补造提交。
7. 页面直接用原生 `el-card`、`el-form`、`el-table`、`el-pagination`、`el-dialog`、`el-drawer`。业务配置解析继续复用无 UI 逻辑；不新增 Card/Dialog/GeneralGrid 等视觉封装。
8. 管理端根、登录、传送层分别使用 `wms-management`、`wms-login`、`wms-dialog` / `wms-drawer` / `wms-popper`。宽表横向滚动，操作区允许换行，长弹窗内容滚动且底部操作可达；不能裁切操作、覆盖大屏或打印。

## 复用方式

- **已有本轮主题的项目**：不重复导入或覆盖主题。直接调整调用页的原生模板与所属查询布局，沿用现有工具函数和翻译机制。
- **首次接入兼容项目**：复制 `assets/runtime/`，先导入 Element Plus CSS，再导入 `native-management.scss`，然后按需导入 `portable-layout.scss`（只补足独立模板的语义布局）。项目已有同等结构时不重复接入。根节点为 `id="total-layout" class="wms-management"`。
- **列表页**：适配[原生查询表格模板](assets/templates/QueryTablePage.vue)。它只发出原始动作、查询、勾选和分页事件，不实现业务提交；将事件映射到原页面处理函数，保留加载与禁用条件。
- **编辑弹窗 / 详情抽屉**：适配[弹窗模板](assets/templates/EditDialog.vue)、[抽屉模板](assets/templates/DetailDrawer.vue)。示例字段由目标页面替换，必填/只读、异步校验、取消与保存语义仍来自原业务。
- **登录、导航、页签**：沿用目标项目品牌、菜单和路由，按样式契约使用标准主题；不把演示菜单、假权限或新认证逻辑接入业务。

`assets/preview/` 是独立的模拟视觉样例，数据明确标记为演示，不导入生产路由或拦截器。在已有 Vue/Vite 项目根放置完整 skill 后，用项目现有 dev 服务访问 `/skills/design/byd-wms-manage-style/assets/preview/index.html`；若目录不同，相应替换 URL 路径。不能通过 file:// 直接运行 Vue SFC。预览入口仅为本轮 rem/lib-flexible 基线准备，接入其它缩放项目时不将该入口导入生产。

有图像能力时参照[查询表格](assets/preview/query-1440.png)、[编辑弹窗](assets/preview/edit-dialog.png)、[详情抽屉](assets/preview/detail-drawer.png)；三图均为合成演示数据，只验证模板视觉，不代表现场业务验收。

## 尺寸与值类型

本轮项目保留 `px2rem(remUnit=60)` 和 lib-flexible；SCSS 中 8px/320px 是**设计尺寸**，实际 CSS px 随根字号变化。原生表格 `width="40"` 则是组件计算的 40 CSS px。不要通过改全局缩放来凑截图，不将其与 PDA 的 44px 触控规范混用。新项目保留自己的已确认缩放机制，记录实测差异。

保留 `0`、`false`、数字 ID 与数组类型。单选/多选显式 value，分页受控属性配更新事件；总数初始为空时显示为 0。加载时保留已知 total，避免页码被夹回 1；每次查询/翻页只发出一次业务请求。不能因样式修改重设数据枚举或凭字段名字推断业务。

## 检查与交付

按[验收规范](references/acceptance.md)检查实际布局与交互，运行现有测试、Lint、构建和仓库要求的检查。静态工具只读，不修改目标文件、不替代仓库门禁：

```sh
python <skill-dir>/scripts/check_style.py --assets-only
python <skill-dir>/scripts/check_style.py --project . --page src/views/SomePage.vue
```

可重复 `--page`；标准主题不在默认路径时传 `--theme src/wms-style/native-management.scss`，独立接入的布局补充可传 `--foundation src/wms-style/portable-layout.scss`。输出区分 error 与 review；退出 0 只表示可解析的静态项通过，动态配置、视觉和功能仍要验收。浏览器可用时以只读 DOM 运行[布局探针](scripts/browser_layout_probe.js)，不读 token、密码或内部应用状态。

至少核对 1920×1080、1440×900、1280×720、768px 宽度；左排换行问题补测 480px。检查表头、序号 1/10/20、选择/全选、查询/重置、分页、弹窗保存/取消、窄屏页脚与长翻译。真实提交仅在已授权业务范围内执行；普通样式回归以打开和取消为主。

如实列出已验证、存量问题和未验证项。登录失效时用正常登录入口恢复，不绕过鉴权，不把空表或演示数据标成真实回归通过。明确偏离时记录用户要求与影响，不改标准文件让检查变绿。

## 分享给其他开发者或模型

分享**整个目录**，不要只复制 SKILL.md。`manifest.json` 锁定版本和文件散列；`agents/openai.yaml` 只是 Codex 发现元数据，其他模型不依赖它，也不依赖本机工具路径。

Codex 调用 `$byd-wms-manage-style`。其它 AI / 人类可从仓库入口读取本文件，使用同一资产和检查命令。可直接复制的任务前缀：

> 阅读并遵循 skills/design/byd-wms-manage-style/SKILL.md，复用其主题和原生组件模板完成本次管理端页面需求。固定查询区间距、按钮尺寸、40px 居中列和传送层作用域；保留原接口、权限与业务事件。执行静态及浏览器验收，报告偏离和未验证项。

更新标准时同步契约、资产、模拟基准图与 manifest，先验证再分发；不自动拉取网上“最新风格”。一致性来自共同资产和验收，不承诺模型仅阅读文字便必然生成完全一致的页面。
