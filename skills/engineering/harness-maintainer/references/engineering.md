# 工程接入

## 部署布局

将 assets/project/tools 整体按相同相对路径合并到目标仓库；已有同名工具先比较用途，保留并调用等价能力，不覆盖现有实现。将 assets/project/harness.config.json 按实情填写到根目录。配置含占位/confirmed=false 时检查故意失败。

Python 3.10+、标准库；前端适配器需 Node 及项目可解析的 @babel/parser；Vue 还需 @vue/compiler-sfc 或 vue-template-compiler。Java 架构适配需 JDK jdeps、项目已核验的完整构建命令及 classes 目录。不要自动安装。语法不支持/动态依赖不可解析都报告缺口。

Vue 2 项目设置 frontend.vue_parser="vue2"；默认 auto 优先 SFC compiler 再回退 Vue 2 parser。不得以 parser 的成功替代模板编译/Lint。

统一入口：
- python tools/harness/check.py docs --root .
- python tools/lint/architecture.py --root . --run-adapters
- python tools/scripts/garbage_collect.py --root . --run-adapters
- python tools/harness/check.py all --root . --run-adapters

默认不执行配置中的命令，缺执行结果返回 2。--run-adapters 仅在已核验命令内容、用途及权限后使用；审计未获构建授权时只运行 docs 并报告其他未验证。脚本返回 0=该自动检查范围内通过，1=已发现违规，2=配置/依赖/执行错误或覆盖缺口。0 不是整个 Harness 验收通过。

## 配置与规则

完整配置示例在 [harness.config.json](../assets/project/harness.config.json)，只允许 schema=1。栈为 frontend/java/mixed/other；其他栈代码检查明确失败。source_roots 必须为仓库内存在目录，exclude 是相对于仓库根的 glob，匹配路径或父目录；默认排除依赖/产物，不排除历史违规。

architecture.rules 使用 fnmatch 路径 glob，from/to 为仓库相对 POSIX 路径，禁止匹配的有向依赖；每条含稳定 id、依据 reason。枚举模块 A→B 的禁止边可由 Agent 据地图生成；store→views、repository→controller 等同理。共享例外通过收窄规则表达，不能全局忽略违规。每条规则必须 confirmed=true；至少一个真实规则，不以假规则凑数。

frontend 适配器使用真实 AST 识别 import/export/require/字面量动态 import 和 TS 类型 import；Vue 用 SFC 解析器提取 script 和 script setup。相对路径、配置 aliases 和常见扩展名可解析；包导入视为外部依赖。项目 workspace 包必须登记 aliases；tsconfig/bundler 自定义解析条件必须核对，并在 resolution_reviewed=true 前完成验证。不支持的动态导入、非字面量 require、脚本 src 或 Vue 自定义 script lang 返回缺口。该规则不证明动态运行时或模板全局注册组件的依赖，需补项目工具/人工项。

java 适配器先运行配置 build（数组），再使用 jdeps -verbose:class -filter:none 读取编译依赖。配置 source_roots 与 class_dirs 覆盖所有生产模块；命令需进行完整 clean compile，禁止跳过实际模块。通过 class→源文件映射及源码覆盖核验，空产物/缺类/过时源/无法映射均失败。静态类型依赖不覆盖反射、Spring 配置/运行时注入；这些列人工项或用项目现有集成测试。jdeps 的平台/语言版本以项目 JDK 为准，不自动升级。

entropy.max_file_lines 为已批准行数上限；前端函数长度、console 和 debugger 由 AST 检查，使用项目已批准配置。疑似旧代码提示人工复核，默认作为覆盖缺口阻断，不能自动删代码。Java 语义日志/方法长度规则由项目已有 Checkstyle/PMD 等执行，java.entropy_command 必填且 coverage 必须确认；可参考 [Checkstyle 模板](../assets/engineering/checkstyle-harness.xml)，集成到现有配置，而非另建一个永不执行的 XML。

准确识别的未关联 Issue 的 TODO/FIXME 属于违规；疑似注释代码属于人工复核。确认是文档示例等误报后，负责人可批准 entropy.reviewed_comments 中的单条记录：path、报告提供的 sha256、reason、reviewer。只豁免该文件内完全相同的注释文本；文本变化需重新核验。不得批量生成记录当成历史基线，也不豁免真实旧代码。

Java 的 java.classpath 可列仓库内依赖 JAR/目录（构建可复制依赖到 target）；额外源码/字节码映射失败必须补适配，不能删除覆盖检查。反射和运行时注入仍需人工或项目现有测试。Checkstyle 模板只覆盖其中部分规则，部署时必须补齐 TODO/注释代码等项目规则并证明检查执行，才能确认 entropy_coverage_confirmed。

doc_sections 可覆盖已有文档标题列表（五篇必须保留），工具校验标题/非空、占位、owner、必读顺序和 Markdown 本地文件链接；不证明规则数、枚举完整度、符号语义、Mermaid 可运行或所有锚点有效，仍走人工验收。

## CI、CODEOWNERS 与维护

先识别现有平台、运行器、语言工具链、锁文件/缓存策略，再将四个检查接入原必跑阶段。不要为执行配置命令使用未审查的 PR 内容中的任意脚本或高权限 token。避免在外部 PR 代码上下文使用可写密钥。

按已确认的平台参考 [CI 接入片段](../assets/engineering/ci-snippets.md)，不能直接复制为完整流水线，也不能把其中 action 版本当作升级要求。

- GitHub/GitLab/Jenkins 等使用其既有配置语法增量修改，不新建替代原流水线。每个失败码必须向上传递；管道输出不能掩盖退出码。
- required checks/保护分支/至少一人 review 是远端管理设置，本地只能列待办，不能声称启用。
- CODEOWNERS 按平台发现现有位置并合并，使用确认的托管用户名/团队语法覆盖五篇、检查配置/工具；不得用中文姓名或企业微信冒充托管账号。
- 每周定时任务调用统一入口，失败也保存 JSON 报告为 CI artifact。每月用 archive_quality.py 将真实报告追加/更新 QUALITY_SCORE.md；脚本需显式 --write，默认仅预览。若自动写回需新权限/提交策略，先请求批准；未批准保留 artifact，自动归档状态为未接入。
- 季度人工复审由 owner 执行；本技能不创建后台定时任务，不代替远端 CI 调度。
- 报告只记录验证数据与待核验项，不捏造分数或阅读遵循率。

所有新增依赖和审批门槛按项目流程；用户要求完整落地不等于允许远端提权或修改保护分支。
