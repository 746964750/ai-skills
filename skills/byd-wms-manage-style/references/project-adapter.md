# wms-manage-font 适配点

路径均相对目标仓库根；skill 安装位置可以不同，不依赖作者的绝对路径。

## 现成入口

| 用途 | 位置 |
| --- | --- |
| 唯一管理端主题 | src/css/native-management.scss |
| 组件、主题注册 | src/main.js、src/components/controllers/index.js |
| 页面结构与导航 | src/views/layout/index.vue、src/views/layout/components/NavBar/index.vue、src/views/layout/components/tagsView.vue |
| 无 DOM 配置逻辑 | src/components/controllers/{FormState,SearchBoxState,GeneralGridState,DialogState}.js |
| 动态字段渲染 | src/components/Form/DomainContent.vue、DialogForm/DomainContent.vue、InlineGrid/DynamicScope.vue |
| 按钮名称、过滤、颜色 | src/utils/buttonLabel.js |
| SVG / 历史业务图标 | src/utils/resolveIcon.js、elementIconMap.js |
| 专用页面兼容 | src/css/legacy-layout-compat.scss |
| rem 构建 | vite.config.mjs、scripts/px2rem.mjs；main 引入 lib-flexible |

页面已直接持有原生模板，无 DOM State 组件仅借作用域插槽提供配置状态和原生 ref。保留该模型，不再将 Card/Dialog/GeneralGrid 全局包装组件带回管理页；也不把每个业务规则复制一遍。

## 查询区与表格

共通查询根 `.wms-search`，搜索卡片 `.el-card.wms-card`，内容 `.SearchcardBody`，字段结构 `.formDiv > .el-form > .el-row > .el-col`。标准主题已覆盖其旧 gutter、min-height 和重复下边距；新查询页优先保持这些语义锚点，不能在普通编辑表单上全局清 margin。

共通表格通过 `GeneralGridState` 保存选择、分页和 ref。原生列仍在调用页，selection/index 的 width/align 在该模板改。序号细化示例在 `src/views/customPage/FullyCustomizedPage/DocumentQuery/info.vue`，其 `document-index-column` 是页面局部规则，不是全局第三方类。

`GeneralGridState.inlineActions` 过滤无效操作，`inlineColumnWidth` 按有效图标/名称分配宽度，`paginationTotal` 仅用于 null 总数的显示回退。不要把显示 total=0 写回查询状态。现有仅序号或勾选模式由页面配置决定。

## 名称与事件

现有模板使用：

```vue
<el-button
  v-for="(item, index) in $visibleButtons(buttonContent, language)"
  :key="item.pkId || index"
  size="small"
  :type="$buttonType(item, 'primary')"
  :icon="$resolveIcon(item.icon)"
  @click="dynamicButtonClick(item)"
>
  {{ $buttonLabel(item, language, index) }}
</el-button>
```

三个按钮函数由现有 NativeControllers 插件提供。新项目通过模板的 labelFor/typeFor/iconFor 回调适配自己的配置，不要求复制本仓库 i18n 单例或字段 schema。

`viewName` 是权限组名，不能回退为按钮名；`infoCode=add` 也不等于运行时 clickEventType=add。真实配置曾有 4 条无可用名称/动作，用户确认隐藏；后台记录保持原样。

`DialogState.actions` 是有效按钮；默认 footer 使用 defaultSaveShow/defaultResetShow/defaultCancelShow。原始配置非空但有效列表为空时保留取消，不能仅用原 length 决定整个 footer 是否存在。

首次新增抽屉时，复用 `.wms-drawer` 的主题，并按 portable-layout.scss 将 footer 在原生 flex 流内贴底。现有项目未提供该抽屉结构时只补充所需锚定规则，不为一个抽屉重复导入所有基础布局。

## 兼容注意

- main 目前全局注册 Element Plus size=small，普通字段和弹窗 footer 必须显式 default。
- 业务字体可能由后端图标码指定，只保留在内部图标节点；数字占位图标如 1 不渲染。
- 已有 enum 值包含数字 0、布尔 false；查询与单选/多选不得按空值丢弃。
- 16 个长页面业务脚本移到同目录 .options.js。模板改动不把业务重新塞回 SFC，也不改相对导入。
- 库位已有排 displayStatus=1 会隐藏重复生成表单，是保留的业务约束；不因空白区域擅自允许生成。
- 浏览器当前页面正常不代表所有动态实例通过。原项目部分路由仍需后端配置/权限；没有真实 drawer 入口。

## 现有验证入口

`npm run test -- --maxWorkers=1`、`npm run build`、`node scripts/check-native-ui.cjs`，以及仓库 Harness。后者可能重写迁移路由清单，不能把生成的静态清单当真实页面通过记录。保护既有规则，不为消除存量失败改阈值。

最新真实证据在 `docs/validation/native-ui/`：`query-spacing-verification.json`、`index-column-verification.json` 和 `real-pages/verification.json`。这些是来源项目的历史证据，不随新页面自动继承通过状态。
