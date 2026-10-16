---
name: byd-wms-pda-style
description: 为 WMS PDA 手持终端新增、改造或检查 Vue 3 + Element Plus 页面，复用固定蓝灰主题、PdaPage 骨架、表单、扫码明细、菜单、登录与弹窗样式。用于“按 PDA 风格做页面”“统一 PDA 样式”及 PDA 页面开发；不用于桌面管理后台、看板或业务接口重构。
metadata:
  short-description: 以标准组件、主题资产和可执行检查约束 PDA 页面风格
---

# BYD WMS PDA 统一样式

目标是复现已有 PDA 视觉规范，不是重新设计。人类开发者和不同 AI 模型都使用本目录中的同一套资产。版本 `1.0.0`，视觉基线来自 `wms-pda-front` 提交 `be27cf4`；该提交号只作追溯，运行本技能不需要访问原仓库或个人电脑。

## 适用边界

- 先读目标项目 AGENTS.md，定位版本、样式入口、PdaPage、翻译入口和本次页面。已有实现先复用，不注册两份主题/组件。
- 针对 Vue 3 + Element Plus。其它框架或不同品牌风格需说明兼容差异，按用户范围处理，不顺手迁移框架或覆盖全站。
- 模板基于 Element Plus `2.14.7`、`@element-plus/icons-vue` `2.3.2` 验证；这是基线，不是“始终最新版”。沿用已锁定的兼容版本，升级另按用户范围执行。
- 只迁移展示结构；保留路由、权限、接口/字段/枚举、扫码 ref 与事件、焦点复位、加载/禁用条件及后端判定。示例 UI 事件不能当成现有后端契约。

## 固定视觉契约

编码前读 [样式契约](references/style-contract.md)，以 [标准主题](assets/runtime/base.css)、[标准骨架](assets/runtime/PdaPage.vue) 为准；有图像能力时看 [360px 基准截图](assets/preview/operation-360.png)。截图使用模拟数据，只比对视觉。

固定项不得由模型自由发挥：

1. 深蓝标题栏、3px 青色底边、蓝色主操作、蓝灰背景、白色面板；复用主题变量，不重新调色。
2. 业务页只用一套 PdaPage：默认插槽为内容、`actions` 为按钮、`back` 调用原页面返回逻辑。
3. 表单沿用 `itemLine` / `itemName`；明细沿用 `itemDivBig` / `itemDiv` + `el-card shadow="never"`。不为相同用途另造布局。
4. 默认字号 14px、输入 16px；输入/选择/普通按钮至少 44px 高、底部按钮至少 46px 高。不恢复 mini/small 风格或缩放分页。
5. 小于 480px 表单标签在控件上方，明细卡片保持两列并允许长名称/条码换行；内容最大宽 760px。
6. 控件/反馈/表格/分页/弹窗使用 Element Plus；图标用 SVG 组件。保留业务条码等专用组件。
7. 内容独立滚动，底部操作在骨架 flex 流内；不在页面内固定定位按钮、硬算屏幕高度或用嵌套百分比高度滚动区。

可变项：字段、标题、接口适配、列定义、业务明细、翻译词条。特殊结构使用专属局部 class，不覆盖主题、骨架和基础控件尺寸。用户明确要求改变风格时尊重要求，列出偏离；不能改写基线来让检查通过。

## 模板与接入

- 扫码/确认/明细：[OperationPage.vue](assets/templates/OperationPage.vue)。原 `@input` 和 Enter 触发时机不擅自互换；示例 emit 待映射到原处理函数。
- 查询/表格/分页：[QueryPage.vue](assets/templates/QueryPage.vue)。请求开始保留 total，防止新版分页将页码夹回 1；条件变化从第 1 页查，翻页保留条件，每个事件只触发一次查询。
- 登录：[LoginPanel.vue](assets/templates/LoginPanel.vue) + [login.scss](assets/runtime/login.scss)。保留原认证、加密与 token 逻辑，图片/系统名由项目提供。
- 菜单：[MenuPanel.vue](assets/templates/MenuPanel.vue) + [menu.scss](assets/runtime/menu.scss)。后端菜单过滤由原逻辑负责；区分加载、失败重试、空权限。
- 弹窗/异常页：按样式契约。条码保留原编码与尺寸参数，容器预览可等比缩放。

已有基线时直接复用，不重复复制。首次接入兼容项目时将 `assets/runtime/` 原样复制到例如 `src/pda-style/`，按 [install.js](assets/runtime/install.js) 注册；先 Element Plus CSS，后标准主题，且只引入一次。登录/菜单 SCSS 仅对应页面引入。全站接入必须在用户授权范围内。

首次接入的最小入口顺序如下；不要把此段重复加入已有基线的项目：

```js
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { installPdaStyle } from './pda-style/install.js'

app.use(ElementPlus, { size: 'default' })
installPdaStyle(app) // 有 i18n 时传 { translate }，或沿用已存在的 $tx
```

保留原翻译工具；基线用 `$tx`，其它工具通过 installer 的 `translate` 适配。仅无 i18n 的中文项目使用缺省直出。新固定文案同步词条；条码、物料名、业务枚举 value 不翻译。

不加载旧字体图标兼容层，不启用 lib-flexible，不将全局 CSS 转 rem；不修改其它工程构建入口。

## 完工检查

运行静态检查（Python 3 标准库；目标路径相对 `--project`）：

```sh
python <skill-dir>/scripts/check_style.py --assets-only
python <skill-dir>/scripts/check_style.py --project . --page src/views/SomePage.vue
```

默认核对 `src/css/base.css`、`src/components/PdaPage/index.vue`；首次复制到其它位置时：

```sh
python <skill-dir>/scripts/check_style.py --project . --theme src/pda-style/base.css --shell src/pda-style/PdaPage.vue --page src/views/SomePage.vue
```

可重复 `--page`。脚本检查资产完整性、主题/骨架漂移、旧组件写法与覆盖，不改文件。退出 1 要处理或说明用户批准的偏离；退出 0 仅代表静态通过。

按 [验收规范](references/acceptance.md) 检查 320×640、360×740、640×360 与桌面；用 [浏览器布局探针](scripts/browser_layout_probe.js) 读取真实 DOM 计算样式和溢出，不能把源码尺寸当渲染证据。检查扫码焦点/清空/回车、返回、加载/重复提交、空/错状态、分页、弹窗及中英文长文本。运行目标项目真实构建/检查，区分新增问题、存量问题与环境阻塞。

交付修改、检查结果、视觉/交互证据及未验证项。模拟数据验证不等于现场 PDA/WMS 联调；没有浏览器或图片能力时明确视觉未验收，不能仅凭技能执行就承诺完全一致。

## 跨开发者与跨模型

分享整个文件夹，不能只复制 SKILL.md；`manifest.json` 锁定资产与版本。Codex 安装后调用 `$byd-wms-pda-style`；其它 AI 工具/人类直接读本文件及对应引用，使用相同资产和命令。`agents/openai.yaml` 只是 Codex UI 元数据，不是运行依赖。

可直接交给任何模型：

> 阅读并遵循仓库 skills/design/byd-wms-pda-style/SKILL.md，复用主题、PdaPage 和页面模板完成本次 PDA 页面需求；保留接口和扫码行为，执行静态检查与窄屏验收，列出偏离和未验证项。

原仓库由 AGENTS.md 链接此入口，其它项目可加入相同指引。明确更新标准时同时更新规范、资产、预览、manifest，重新验证后分发；不自动从网络拉“最新样式”。
