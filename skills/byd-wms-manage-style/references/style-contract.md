# 管理端样式契约 1.0.0

## 尺寸口径

来源为 wms-manage-font 2026-10-15 的原生组件改造及后续真实截图修正。兼容基线 Vue 3.5.44 / Element Plus 2.14.7 / icons-vue 2.3.2。来源工作区未提交，不能把旧 HEAD 3854511 当作这些样式已经存在的发布版本；实际资产以 manifest 散列为准。

以下 px 除原生列宽外均是设计值。当前项目会将 SCSS 转 rem，1536px 实测中 8px 设计间距约为 7.2 CSS px、默认输入约为 28.8 CSS px；这些实测不是其它视口下的硬编码目标。

## 主题与骨架

| 项目 | 固定设计值 |
| --- | --- |
| 主色 / 背景 | #1758A7 / #F3F6FA |
| 面板 / 正文 / 辅助 / 边框 | #FFFFFF / #263445 / #66758A / #E2E8F0 |
| 其它语义色 | Element Plus 成功、警告、危险色，不全部改成主色 |
| 中文字体 | Microsoft YaHei、PingFang SC、system-ui、sans-serif |
| 正文 / 分区标题 / 页签 | 14 / 16 / 13px；分区标题 font-weight 600 |
| 间距 | 8 / 12 / 16 / 24px |
| 卡片 / 控件 / 弹窗圆角 | 8 / 6 / 12px |
| 卡片阴影 | 0 2px 6px rgb(38 52 69 / 3%) |
| 桌面页面 padding / 分区 gap | 16px / 12px；窄屏页面 padding 12px |
| 卡片标题栏 | min-height 48px、padding 8px 16px、flex 可换行 |
| 数据区 padding | 16px；使用 min-width:0，宽表内部横向滚动 |

顶部保留品牌标识，设计高度 60px；侧栏展开 220px、收起 60px；页签栏高 48px、页签高 30px。现有项目复用 shell，新增项目按该几何适配原生导航，不复制业务菜单和路由。导航选中项浅蓝背景、主色文字、左侧 3px 强调线。登录白面板、宽 400px、padding 40px、主按钮高 40px；这是登录例外，工具栏仍 small。

页面层级：查询卡片 → 数据卡片（标题、操作区、表格）→ 分页。编辑页保持同一标题、字段和底部操作顺序，不将保存按钮散放在字段之间。

## 查询区：必须使用紧凑左排

- 搜索卡片内容 padding **8px 16px**；不要叠加旧 12px、18px margin 或 45/70px min-height。
- 每组条件设计宽 **320px**，最大宽 100%，从左排列，row-gap **8px**、column-gap **16px**。不使用 justify-content:space-between、每个条件固定 50% 或大百分比 label-width 制造空隙。
- 标签宽度随文字，标签到控件 8px；控件 flex:1、min-width:0。输入、选择、日期 size=default。
- 使用旧 el-row/el-col 时覆盖查询区内的 inline gutter、列底 padding、form-item margin 与旧 el-col-div min-height；不要覆盖编辑弹窗的同名结构。
- 条件变多自然换行，校验信息留在所属字段下方，不能被 overflow:hidden 或固定区块高度裁掉。

## 操作区与按钮

| 用途 | 原生尺寸 | 语义 |
| --- | --- | --- |
| 查询、工具栏、行内操作 | small | 查询/新增/保存等主操作 primary |
| 重置、取消 | 工具栏 small；弹窗 footer default | default |
| 删除 / 明确 DELETE 请求 | 与所在操作区一致 | danger |
| 业务自定义动作 | 与所在操作区一致 | 保留配置语义色 |
| 编辑弹窗 footer | default | 保存 primary，取消 default |

按钮 gap 8px，操作容器可换行；不能靠全局默认 small 或按钮上的 iconfont 类控制尺寸。查询/新增用明确文本；仅图标的密集行操作可用 Tooltip + aria-label。避免 loading 时重复请求，禁用条件继续来自原业务。

名称解析优先级：当前语言 fViewName → 兼容语言码 → 既有中文/英文等有效翻译 → buttonTitle/fButtonTitle → 前端已识别的动作名称。权限字段 viewName、infoCode 或 URL 不是业务名称来源。不能从 URL 猜动作后补写名称。

无名称且无已识别动作的记录作为无效显示配置过滤；保留原记录、顺序、权限和对象。不能自动删除后台记录或改 clickEventType。无图标但有名称时显示名称，并按名称分配行操作列宽。弹窗所有配置按钮无效时仅保留安全取消，不凭空显示保存。

## 表格、选择与序号

| 部分 | 标准 |
| --- | --- |
| 密集数据表 | size=small、正文设计 14px、cell line-height 22px |
| 表头 | 背景 #F5F8FC、正文 #52657C、padding 10px 0、font-weight 600 |
| 数据行 | padding 8px 0；条纹 #FAFBFD；hover #EDF4FC |
| 选择列 | **width=40 CSS px**，align/header-align center，cell padding 0，内部 flex 居中 |
| 序号列 | **width=40 CSS px**，align/header-align center，cell 左右设计 padding 4px，nowrap |
| 业务列 | 保留配置顺序、显隐、对齐、固定、排序和宽度；不可一律改成 40px |

宽度使用 `width="40"`，不能以 min-width=40 代替，否则会被伸展。序号保持原索引规则，不在样式任务中改成跨页全局序号。存在 checkbox 与 index 切换的旧列，只调整本次授权模式；新增页明确两种模式的宽度。

分页控制 current-page/page-size 并配对 update 事件，不同时绑定旧事件再发重复请求。null/undefined 初始 total 在渲染端回退 0，页面原始状态和请求字段不变；请求过程中保留已有 total。页码、pageSize 类型和“全部”的业务约定由原代码决定。

## 编辑、弹窗、抽屉及下拉层

- 普通编辑字段 default；常规字段间距 12–18px、分区间距 24px。label 和 content 最小宽度允许收缩，长标签可按原布局换行。
- el-dialog class=wms-dialog；el-drawer class=wms-drawer；select/date 等传送的下拉层 popper-class=wms-popper。普通布局作用域不能依赖 body 祖先，不能影响监控或打印。
- header padding 20px 24px 16px；body padding 20px 24px；footer padding 12px 24px，上边框、右对齐、按钮 gap 8px。
- dialog max-width:calc(100vw - 32px)；≤992px 时最小宽度 min(560px, calc(100vw - 24px))、最大 calc(100vw - 24px)。长内容限制 body 高度并滚动，取消和保存不能藏在被裁掉的容器内。
- 抽屉详情分组展示，窄屏用可达的宽度、明细表横向滚动。footer 采用原生 flex 流内 margin-top:auto 贴底，不使用 fixed；独立模板由 portable-layout.scss 补足。抽屉模板只保证相同主题，不预设业务详情结构。原项目没有真实抽屉实例，历史模拟图不能宣称现场通过。
- 使用原生 v-model/model-value、关闭回调和表单 validate Promise；取消时是否清空/恢复由原业务决定，不把关闭等同保存。

## 修改边界

不修改接口 URL、payload、权限码、后端配置、枚举、按钮动作、校验及联动。动态列和控件继续由原配置生成。0/false/数值 ID 不转字符串、不使用 truthy 判断丢失值。

监控、大屏、IO、3D、打印、PDA不套该主题；前者保留独立布局，PDA使用自己的触控规范。仅样式任务不修改认证、请求拦截器或路由。不得通过改变缩放/隐藏内容来伪造一致性。
