# WCS Scope and Classification

## Principle

Classify by control responsibility in the target architecture, not by isolated words such as “task”, “inventory”, “PLC”, or “AGV”. WCS boundaries vary by project; uncertain ownership is a clarification item.

## Responsibility model

| Layer | Typical responsibility | Do not automatically assign to WCS |
|---|---|---|
| Business/host (`ERP/MES/OMS`) | production or business demand, order intent, master/business records | real-time equipment sequencing |
| Planning/execution (`WMS/WES`) | inventory ownership, waves, allocation, work release, cross-process orchestration | device-level handshakes unless explicitly required |
| `WCS` | executable transport work, resource selection, route/traffic coordination, equipment command orchestration, status aggregation, recovery coordination | low-level motor/sensor control or authoritative business inventory unless explicitly required |
| Control (`PLC/SCADA/equipment controller`) | interlocks, I/O, motion sequence, safety chain, device-local state machine | warehouse-wide task prioritization or multi-device routing |
| Physical equipment | conveyors, lifts, stacker cranes, shuttles, robots, AGVs/AMRs, doors, scanners | cross-system business decisions |

This table is a default lens, not a project fact. Source text and the agreed architecture override it.

Some customer documents use “WCS” as the name of an entire warehouse software solution and place WMS-like inventory, order, or master-data capabilities inside it. In that case, preserve the explicit project assignment as evidence, flag the deviation from the default responsibility model, and add a clarification about authoritative ownership/integration. Do not silently reassign or discard the stated requirement.

## Classification values

- `WCS功能`: WCS is explicitly or defensibly responsible for a behavior that can be implemented and tested.
- `接口/协同`: WCS exchanges data or coordinates a handshake, but another system owns part of the result.
- `非功能要求`: performance, availability, security, auditability, deployment, maintainability, observability, compatibility, localization, backup, or disaster recovery applying to WCS.
- `待澄清`: ownership, trigger, data, acceptance criteria, exception policy, or architecture is insufficient or contradictory.
- `非WCS职责`: evidence assigns the behavior to another layer. Keep it in an exclusion/assumption register when it affects WCS integration.

## Evidence strength

- `明确`: the source directly states that WCS/system/software shall perform the behavior, or an unambiguous architecture/table assigns it to WCS.
- `推断`: WCS ownership follows from the stated flow or interface but is not directly assigned. Record the reasoning and assumption.
- `歧义`: wording supports multiple owners or behaviors. Do not promote it to the committed baseline.

Confidence (`高/中/低`) is separate from evidence strength. A direct but contradictory statement may be `明确 + 低` until the conflict is resolved.

## WCS ambiguity and boundary emphasis

Create a priority-review item whenever a statement explicitly names WCS, uses a documented WCS alias, or sits inside a clearly WCS-scoped section and one or more of these conditions applies:

- `责任主体不明`: wording uses “系统/平台/软件/上位系统” without a stable referent, or multiple actors can perform the action.
- `系统边界不明`: behavior could belong to WMS/WES/MES/ERP, WCS, PLC/SCADA, an equipment controller, or an equipment vendor.
- `功能行为不明确`: wording says “支持/具备/实现/智能/自动/优化/相关功能”等 but does not define an observable behavior.
- `接口契约不完整`: an interface is named without sufficient direction, trigger, schema, acknowledgement, correlation/idempotency, timeout, retry, error, ordering, or reconciliation rules.
- `异常归属不明`: fault, timeout, offline, retry, recovery, manual takeover, compensation, or forced completion is mentioned without a decision owner and end state.
- `数据权属不明`: inventory, location, task, equipment, user/permission, master data, or status is duplicated or cached without an authoritative owner and synchronization rule.
- `验收口径缺失`: terms such as real-time, efficient, stable, flexible, compatible, seamless, automatic, or configurable lack a measurable condition or expected result.
- `上下文指代不明`: headings, merged cells, diagrams, arrows, footnotes, or prior paragraphs are required to know what “系统/该功能/其/相关设备” means.
- `版本或冲突`: two sources or two parts of a source assign different owners, behaviors, values, or versions.

### Emphasis level

`关注级别` is an analyst review signal, not customer priority:

- `高`: ambiguity can materially change system boundary, commercial scope, safety, data authority, interface ownership, exception responsibility, availability, or acceptance.
- `中`: responsibility is mostly plausible but implementation, integration, estimation, or test design still depends on missing detail.
- `低`: responsibility is clear and only a minor wording or acceptance detail is missing. Keep it visible but do not let it dominate the review list.

Every emphasized item must include the exact source, ambiguity type, the plausible owners or interpretations, the scope/implementation impact, and one answerable clarification question. A single passage can support both a provisional function row and a priority-review item; do not force an either/or choice.

## Decision model

For each atomic statement:

1. Identify the actor named by the source. If none is named, keep actor unknown.
2. Identify the observable behavior: trigger, decision/process, output/command, state change, or acceptance result.
3. Identify who owns the authoritative data and who controls the physical action.
4. Ask whether WCS must implement logic, only exchange information, or merely expose/consume status.
5. Check whether the same behavior is assigned elsewhere in another source.
6. Check the WCS ambiguity conditions and set `重点标注`, `关注级别`, and `模糊类型`.
7. Choose a classification and evidence strength. If an architecture assumption is required, add a clarification question and keep the item highlighted until resolved.

## WCS capability checklist

Use this only as a coverage checklist; absence from a document is not proof that the function is required.

### Task and orchestration

- receive, validate, acknowledge, cancel, pause, resume, split, merge, prioritize, queue, dispatch, and complete executable tasks
- choose equipment/resource, enforce constraints, sequence dependent moves, and coordinate handoffs
- route/path selection, traffic control, deadlock/blocked-path handling, congestion strategy, and re-routing where WCS owns them

### Equipment integration

- commands and handshakes for conveyors, lifts, stacker cranes, shuttles, robots, AGVs/AMRs, sorters, doors, scanners, weighers, print/apply, or other devices
- readiness, busy/fault/state signals; command/result correlation; timeout and retry policy
- startup, shutdown, online/offline, maintenance/bypass, simulation, or manual modes

### State, monitoring, and recovery

- task/equipment/location state aggregation and synchronization
- alarms, events, logs, dashboards, notification, history, traceability, and KPI/report data
- exception detection, retry, rollback/compensation, re-dispatch, forced completion, cancellation, manual takeover, and recovery after restart/network loss

### Interfaces and data

- APIs/messages/files/database exchanges with WMS/WES/MES/ERP/PLC/SCADA/equipment controllers
- message schema, direction, trigger, frequency, correlation/idempotency, acknowledgement, error codes, timeout, retry, ordering, and reconciliation
- topology, equipment, station, route, policy, mapping, user/role, and other configuration/master data owned or consumed by WCS

### Non-functional and operational

- throughput/latency/concurrency/capacity targets and measurement conditions
- availability, redundancy, failover, recovery objectives, backup, upgrade, and deployment constraints
- authentication, authorization, audit, encryption, network zoning, data retention, localization, observability, maintainability, and compatibility

## Atomicity and deduplication

- Split independent verbs when they can be accepted or rejected separately.
- Keep trigger, normal behavior, and exception behavior distinct when each needs separate acceptance.
- Do not merge similar functions with different equipment, interfaces, constraints, or owners.
- Merge exact semantic duplicates and attach multiple evidence records.
- Preserve conflicts as separate evidence rows linked to one clarification item.

## Common overreach to avoid

- Turning a process description into a committed WCS function without explicit ownership.
- Assigning low-level interlocks or safety logic to WCS merely because WCS sends a command.
- Treating WMS inventory/allocation behavior as WCS responsibility without architecture evidence.
- Inventing protocols, priorities, retry counts, throughput values, screens, reports, or acceptance criteria.
- Assuming a diagram arrow defines a full bidirectional interface contract.
