# Scope and Classification

## Principle

Classify by control or ownership responsibility in the target architecture, not by isolated words. Boundaries between the target subject and its neighbours vary by project; uncertain ownership is a clarification item, not a silent guess.

## Declare the target subject first

Before classifying anything, state:

1. `目标主体` (target subject/system): the thing whose in-scope behaviour we are extracting, with its project names and documented aliases.
2. `相邻系统/边界` (neighbouring systems and boundary): the upstream/downstream/control/physical layers the target subject exchanges data or commands with.
3. `权属口径` (authority): which layer owns authoritative data and which layer owns the physical/control action.

These three declarations become the anchor terms for the source sweep and the lens for the responsibility model. If the document itself is ambiguous about who owns a behaviour, that is a `待澄清` item, not a reason to guess.

## Responsibility model (template)

This is a default lens, not a project fact. Fill the generic rows with the actual systems in the current project; source text and the agreed architecture override it.

| Layer | Typical responsibility | Do not automatically assign to the target subject |
|---|---|---|
| Business / host (`上游业务系统`) | business demand, order/request intent, master or business records | real-time sequencing or device-level handshakes |
| Planning / orchestration (`上游编排系统`) | ownership of business records, waves/plans, allocation, work release, cross-process orchestration | low-level control unless explicitly required |
| **目标主体** (`the declared target`) | executable work, resource selection, routing/coordination, command orchestration, status aggregation, recovery coordination | physical control or authoritative business data unless explicitly required |
| Control / execution (`控制层/执行层`) | interlocks, I/O, motion/process sequence, safety chain, device-local state | cross-system prioritization or multi-node routing |
| Physical / equipment (`物理/设备层`) | the physical or peripheral actors (devices, services, operators) | cross-system business decisions |

If a customer document uses the target subject's name for a wider solution and places adjacent responsibilities (inventory, order, master data, planning) inside it, preserve the explicit project assignment as evidence, flag the deviation from the default model, and add a clarification about authoritative ownership and integration. Do not silently reassign or discard the stated requirement.

## Classification values

- `主体功能`: the target subject is explicitly or defensibly responsible for a behaviour that can be implemented and tested.
- `接口/协同`: the target subject exchanges data or coordinates a handshake, but another system owns part of the result.
- `非功能要求`: performance, availability, security, auditability, deployment, maintainability, observability, compatibility, localization, backup, or disaster recovery applying to the target subject.
- `待澄清`: ownership, trigger, data, acceptance criteria, exception policy, or architecture is insufficient or contradictory.
- `主体外职责`: evidence assigns the behaviour to another layer. Keep it in an exclusion/assumption register when it affects integration with the target subject.

## Evidence strength

- `明确`: the source directly states that the target subject/system/software shall perform the behaviour, or an unambiguous architecture/table assigns it to the target subject.
- `推断`: ownership follows from the stated flow or interface but is not directly assigned. Record the reasoning and assumption.
- `歧义`: wording supports multiple owners or behaviours. Do not promote it to the committed baseline.

Confidence (`高/中/低`) is separate from evidence strength. A direct but contradictory statement may be `明确 + 低` until the conflict is resolved.

## Ambiguity and boundary emphasis

Create a priority-review item whenever a statement explicitly names the target subject, uses a documented alias, or sits inside a clearly scoped section of the target subject and one or more of these conditions applies:

- `责任主体不明`: wording uses “系统/平台/软件/服务/上位系统” without a stable referent, or multiple actors can perform the action.
- `系统边界不明`: behaviour could belong to the target subject, an upstream/downstream system, a control layer, or an external vendor.
- `功能行为不明确`: wording says “支持/具备/实现/智能/自动/优化/相关功能”等 but does not define an observable behaviour.
- `接口契约不完整`: an interface is named without sufficient direction, trigger, schema, acknowledgement, correlation/idempotency, timeout, retry, error, ordering, or reconciliation rules.
- `异常归属不明`: fault, timeout, offline, retry, recovery, manual takeover, compensation, or forced completion is mentioned without a decision owner and end state.
- `数据权属不明`: inventory/location/task/equipment/status/user/master data is duplicated or cached without an authoritative owner and synchronization rule.
- `验收口径缺失`: terms such as real-time, efficient, stable, flexible, compatible, seamless, automatic, or configurable lack a measurable condition or expected result.
- `上下文指代不明`: headings, merged cells, diagrams, arrows, footnotes, or prior paragraphs are required to know what “系统/该功能/其/相关设备” means.
- `版本或冲突`: two sources or two parts of a source assign different owners, behaviours, values, or versions.

### Emphasis level

`关注级别` is an analyst review signal, not customer priority:

- `高`: ambiguity can materially change system boundary, commercial scope, safety, data authority, interface ownership, exception responsibility, availability, or acceptance.
- `中`: responsibility is mostly plausible but implementation, integration, estimation, or test design still depends on missing detail.
- `低`: responsibility is clear and only a minor wording or acceptance detail is missing. Keep it visible but do not let it dominate the review list.

Every emphasized item must include the exact source, ambiguity type, the plausible owners or interpretations, the scope/implementation impact, and one answerable clarification question. A single passage can support both a provisional function row and a priority-review item; do not force an either/or choice.

## Decision model

For each atomic statement:

1. Identify the actor named by the source. If none is named, keep actor unknown.
2. Identify the observable behaviour: trigger, decision/process, output/command, state change, or acceptance result.
3. Identify who owns the authoritative data and who controls the physical/control action.
4. Ask whether the target subject must implement logic, only exchange information, or merely expose/consume status.
5. Check whether the same behaviour is assigned elsewhere in another source.
6. Check the ambiguity conditions and set `重点标注`, `关注级别`, and `模糊类型`.
7. Choose a classification and evidence strength. If an architecture assumption is required, add a clarification question and keep the item highlighted until resolved.

## Capability checklist

Use this only as a coverage checklist; absence from a document is not proof that the function is required. The buckets are generic; the analyst should expand or prune them to match the target domain.

### Work and orchestration

- receive, validate, acknowledge, cancel, pause, resume, split, merge, prioritize, queue, dispatch, and complete executable work items
- choose resource/actor, enforce constraints, sequence dependent steps, and coordinate handoffs
- route/path selection, traffic/flow coordination, deadlock/blocked-path handling, congestion strategy, and re-routing where the target subject owns them

### Integration

- commands and handshakes with upstream, downstream, control, or device/external systems
- readiness, busy/fault/state signals; command/result correlation; timeout and retry policy
- startup, shutdown, online/offline, maintenance/bypass, simulation, or manual modes

### State, monitoring, and recovery

- work/actor/location state aggregation and synchronization
- alarms, events, logs, dashboards, notification, history, traceability, and KPI/report data
- exception detection, retry, rollback/compensation, re-dispatch, forced completion, cancellation, manual takeover, and recovery after restart/network loss

### Interfaces and data

- APIs/messages/files/database exchanges with neighbouring systems
- message schema, direction, trigger, frequency, correlation/idempotency, acknowledgement, error codes, timeout, retry, ordering, and reconciliation
- topology, entity, route, policy, mapping, user/role, and other configuration/master data owned or consumed by the target subject

### Non-functional and operational

- throughput/latency/concurrency/capacity targets and measurement conditions
- availability, redundancy, failover, recovery objectives, backup, upgrade, and deployment constraints
- authentication, authorization, audit, encryption, network zoning, data retention, localization, observability, maintainability, and compatibility

## Atomicity and deduplication

- Split independent verbs when they can be accepted or rejected separately.
- Keep trigger, normal behaviour, and exception behaviour distinct when each needs separate acceptance.
- Do not merge similar functions with different actors, interfaces, constraints, or owners.
- Merge exact semantic duplicates and attach multiple evidence records.
- Preserve conflicts as separate evidence rows linked to one clarification item.

## Common overreach to avoid

- Turning a process description into a committed function without explicit ownership.
- Assigning low-level control or safety logic to the target subject merely because it sends a command.
- Treating upstream planning/inventory/business behaviour as target-subject responsibility without architecture evidence.
- Inventing protocols, priorities, retry counts, throughput values, screens, reports, or acceptance criteria.
- Assuming a diagram arrow defines a full bidirectional interface contract.
