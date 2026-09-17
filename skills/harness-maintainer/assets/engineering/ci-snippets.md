# 接入现有 CI 的片段

只在确认平台、现有阶段、运行器和工具链后合并，不能整份覆盖流水线。以下假定 Linux runner 已准备项目 Python/Node/JDK 和锁定依赖，不包含安装步骤。Windows 使用对应命令并验证 UTF-8 输出与退出码。检查命令内部可能执行已审核的 Java 构建或 Lint。

## GitHub Actions

在现有 job 的检查步骤后添加，保持原工作目录和环境：

```yaml
- name: Harness checks
  run: python tools/harness/check.py all --root . --run-adapters > harness-report.json
- name: Preserve Harness report
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: harness-report
    path: harness-report.json
    if-no-files-found: error
```

action 使用仓库已批准的版本或提交 SHA；不为该示例升级原流水线。周定时按现有 workflow 的 on.schedule 合并，cron 使用平台时区语义；required checks/保护分支仍需授权管理者在远端验证。外部 PR 不获得归档写回凭据。

## GitLab CI

合并到项目实际检查 stage，保留原 rules、缓存和依赖关系：

```yaml
harness-check:
  stage: test
  script:
    - python tools/harness/check.py all --root . --run-adapters > harness-report.json
  artifacts:
    when: always
    paths:
      - harness-report.json
```

不要设置 allow_failure。周计划属于平台 pipeline schedules 设置：本地配置不能证明已启用。

## Jenkins

合并到现有 stage，保持原 agent/tool 环境：

```groovy
script {
    int result = sh(
        script: 'python tools/harness/check.py all --root . --run-adapters > harness-report.json',
        returnStatus: true
    )
    archiveArtifacts artifacts: 'harness-report.json', allowEmptyArchive: false
    if (result != 0) {
        error("Harness checks failed: ${result}")
    }
}
```

周扫描合并到现有 triggers，不另起高权限流水线。若命令未产生报告，归档失败也是失败，不忽略。

## 月归档

从本月真实全量扫描 artifact 获取报告，执行：

```text
python tools/harness/archive_quality.py --root . --report harness-report.json
python tools/harness/archive_quality.py --root . --report harness-report.json --write
```

第一条仅预览，第二条写 QUALITY_SCORE.md；写入不等于自动提交。按项目已批准机器人/PR 策略接入月任务，无写回权限时保留 artifact 并报告“自动归档待接入”。失败报告也要归档，同一报告按哈希去重。季度复审由确认的个人 owner 执行，不由定时脚本冒充。
