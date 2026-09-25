# Agentic Application Framework: Reference Architecture, Conformance Model, and Development Process

## Purpose

This document consolidates the design rationale, observations, architectural analysis, and recommended refinements for an application-development framework intended to support both human developers and AI coding agents.

The central idea is that the framework should **not** operate as a mandatory application template. Instead, it should function as an **executable reference architecture** that demonstrates standards, boundaries, patterns, and required behaviours.

A coding agent should be able to examine the reference implementation, combine it with requirements, constraints, guardrails, and acceptance criteria, and then generate the smallest coherent application that satisfies those requirements.

The generated application is therefore expected to preserve **architectural intent and conformance**, but is not required to reproduce the structure or all components of the reference implementation.

---

# 1. Original Framework Structure

The application framework is divided into several broad areas:

- Web services
- API services
- Agent services
- Front-end applications
- Database services
- Configuration
- Shared function libraries organised into a hierarchy of modules

The primary deliverables are:

- Agents
- Front ends
- API definitions and services

The remaining framework components exist primarily to support the development and operation of those deliverables.

A useful conceptual distinction is therefore:

```text
APPLICATION DELIVERABLES
├── Agents
├── Front-end applications
└── APIs

FOUNDATION / SUPPORTING CAPABILITIES
├── Web services
├── Database services
├── Configuration
├── Shared libraries
├── Authentication / authorisation
├── Logging / observability
├── Security controls
└── Other platform capabilities
```

The supporting services also create functional boundaries and standardised interfaces, particularly for AI coding agents.

---

# 2. Design Philosophy

The framework follows a deliberately minimalist philosophy.

The preferred principles are:

1. Code should be largely self-documenting.
2. Documentation should explain architectural intent rather than restating implementation.
3. The reference code base should demonstrate a complete, working implementation.
4. The reference structure should not automatically become the required target structure.
5. Generated applications should include only what they actually require.
6. Mandatory controls must remain mandatory even when implementation details change.
7. The coding agent should reconcile all available inputs rather than mechanically copying framework code.
8. Conformance should be determined primarily through contracts, invariants, and tests.

This is materially different from a conventional framework.

A traditional framework normally says:

> Put your application inside this structure and follow these conventions.

This model instead says:

> Here is a known-good implementation of the architecture. Build the application that best satisfies the requirements while preserving the mandatory properties.

---

# 3. More Precise Architectural Definition

The system is better described as an:

**Executable Reference Architecture with a Conformance Harness**

rather than simply an application framework.

The core elements are:

```text
Architectural Intent
│
├── Mandatory invariants
├── Interface contracts
├── Security and operational standards
├── Application requirements
├── Acceptance criteria
│
└── Reference implementation
        │
        ▼
    Coding agent
        │
        ▼
Generated application
        │
        ▼
Conformance validation
```

The reference implementation proves that the architecture is feasible.

It should not be the sole authority for determining what the architecture means.

---

# 4. First Trial

The first development exercise produced an informative result.

A senior developer unfamiliar with the code base initially attempted to refactor the framework manually.

The developer concluded that the task could not reasonably be completed within a single sprint and that a coding agent was required to complete the work within the available time.

The senior developer also observed that the framework did not appear to have an immediately discernible conventional structure.

However, when the coding agent processed the framework, it successfully inferred the necessary structural and functional relationships and produced a working result.

The first test therefore passed.

This created useful dissonance:

- The human developer initially struggled to see the architecture.
- The coding agent successfully reconstructed enough of the architecture to generate the required application.
- The generated solution met the expected outcome.
- The process consumed a relatively large number of tokens.

This result should be treated as positive evidence, but not yet as proof of general reliability.

---

# 5. What the First Trial Demonstrated

The first trial suggests that the framework contains sufficient internal semantic coherence for architectural intent to be reconstructed from:

- module relationships;
- code behaviour;
- interfaces;
- dependencies;
- patterns;
- tests;
- configuration;
- and surrounding implementation context.

This is important.

The architecture appears to be encoded more strongly in **relationships and behaviour** than in immediately visible folder structure or conventional framework organisation.

The coding agent was able to infer those relationships.

The human developer was initially expecting the structure to be expressed more explicitly.

Those are not contradictory observations.

They reveal where the architectural information currently resides.

---

# 6. Strengths of the Approach

## 6.1 Strong distinction between deliverables and supporting capabilities

Separating application deliverables from foundation services is useful.

It encourages a basic architectural question:

> Does this code exist because this application needs it, or because the development environment provides the capability?

This makes it easier to omit unnecessary components.

---

## 6.2 Avoidance of framework cargo-culting

Traditional frameworks often encourage wholesale copying.

For example:

```text
new-project/
├── auth/
├── database/
├── queue/
├── scheduler/
├── telemetry/
├── migrations/
├── plugins/
├── adapters/
└── application/
```

The new application may only need a subset of those capabilities, but copying the framework often brings everything forward.

The proposed model instead asks:

> Which capabilities are actually required to satisfy the application objectives and architectural rules?

That is a better fit for AI-generated software.

---

## 6.3 Architectural intent is separated from implementation

A generated application does not need to preserve a particular folder hierarchy if the required behaviour survives.

For example, the reference implementation might be:

```text
framework/
├── web/
├── api/
├── agents/
└── database/
```

A generated application might instead use:

```text
service/
├── runtime/
├── interfaces/
├── persistence/
└── application/
```

Either may be valid if contracts, controls, and required behaviours remain intact.

---

## 6.4 Executable reference is better than purely descriptive documentation

A functioning reference implementation can demonstrate:

- correct interfaces;
- expected dependency relationships;
- security patterns;
- configuration behaviour;
- operational assumptions;
- logging conventions;
- deployment behaviour;
- and integration patterns.

This provides considerably stronger evidence than architecture documentation alone.

---

## 6.5 Appropriate optimisation freedom for coding agents

The agent is permitted to:

- reorganise the code;
- omit unused modules;
- replace reference components;
- simplify implementation;
- consolidate capabilities;
- select only relevant dependencies.

This allows generated applications to become smaller and more purpose-specific.

---

# 7. Important Weakness Exposed by the Trial

The senior developer's initial difficulty should not be dismissed.

If an experienced developer cannot rapidly determine the structure and intent of the code base, there is a maintainability cost.

The fact that a coding agent eventually succeeded does not remove that cost.

The coding agent may have succeeded by performing substantial inference:

```text
Inspect repository
    ↓
Infer dependencies
    ↓
Construct architectural hypothesis
    ↓
Inspect more code
    ↓
Reconcile exceptions
    ↓
Revise hypothesis
    ↓
Generate implementation
```

That process consumes tokens.

Humans pay essentially the same cost in time and cognitive effort.

This can be thought of as an **inference tax**.

The objective should therefore not be to add extensive documentation.

The objective should be to make the smallest amount of architectural intent explicit so neither humans nor agents need to repeatedly rediscover it.

---

# 8. Documentation Strategy

The minimalist documentation philosophy should remain.

However, documentation should distinguish between what the code can communicate and what the code cannot reliably communicate.

## 8.1 Information that usually does not need extensive documentation

Avoid duplicating facts such as:

```text
Function A calls Function B.
Module X contains Class Y.
Endpoint Z accepts JSON.
Class Q exposes methods R and S.
```

Humans and coding agents can inspect these directly.

---

## 8.2 Information that should be explicit

Document:

```text
WHY a boundary exists

WHICH behaviour is mandatory

WHICH choices are replaceable

WHAT must never be bypassed

WHAT downstream systems rely on

WHAT constitutes architectural conformance

WHEN a capability is required

WHEN a capability should be omitted
```

A useful rule is:

> Document intent, invariants, and contracts. Let the code document implementation.

---

# 9. Recommended Component Classification

Every significant framework capability should be classified into one of four categories.

| Classification | Meaning |
|---|---|
| **MUST** | Mandatory architectural, security, regulatory, or operational invariant |
| **CONTRACT** | Interface or behaviour that must remain compatible |
| **REFERENCE** | Known-good implementation that may be replaced |
| **OPTIONAL** | Capability included only when the target application requires it |

Example:

```text
Capability: Authentication

MUST
- All inbound user operations are authenticated where required.
- Authentication state must not be trusted solely from client input.

CONTRACT
- Authentication returns the standard principal representation.

REFERENCE
- reference/auth/oauth.py

OPTIONAL
- OAuth is not required for trusted machine-only services when another
  approved authentication mechanism satisfies the contract.
```

This significantly reduces ambiguity.

---

# 10. Recommended Machine-Readable Architecture Manifest

A small architecture manifest can reduce the amount of inference required from every coding agent run.

For example:

```yaml
architecture:
  deliverables:
    - agents
    - frontend
    - api

  foundation:
    web:
      required_when:
        - external_http
      reference:
        - reference/services/web

    database:
      required_when:
        - persistent_state
      reference:
        - reference/services/database

    observability:
      required_when:
        - production_service
      reference:
        - reference/services/observability

  invariants:
    - id: AUTH-001
      description: all_external_operations_are_authorized

    - id: CFG-001
      description: runtime_secrets_are_externalized

    - id: LOG-001
      description: structured_logging_is_enabled

    - id: API-001
      description: published_api_contracts_are_validated

  freedoms:
    restructure_code: true
    omit_unused_reference_code: true
    replace_reference_implementation: true
    consolidate_components: true

  restrictions:
    bypass_security_boundaries: false
    weaken_interface_contracts: false
    remove_required_audit_events: false
```

The manifest should remain concise.

Its purpose is to provide the map, not duplicate the territory.

---

# 11. Authority Hierarchy

The reference implementation should not be treated as the highest architectural authority.

A recommended precedence order is:

```text
1. Security, legal, and organisational requirements
2. Architectural invariants
3. Interface contracts
4. Application requirements
5. Acceptance and conformance tests
6. Reference implementation
```

This prevents accidental implementation details from becoming permanent architectural doctrine.

---

# 12. Why This Matters

Suppose the agent sees:

```python
audit.log_event(
    event_type="privileged_action",
    principal=principal.id,
    resource=resource_id,
)
```

The agent may determine that no local application logic consumes the event and remove it.

That could be locally rational but architecturally wrong.

The event may exist for:

- security monitoring;
- auditability;
- compliance;
- forensic analysis;
- central observability;
- or external control systems.

Therefore, capabilities such as the following should normally be represented explicitly as invariants or contracts:

- authentication;
- authorisation;
- audit logging;
- telemetry;
- redaction;
- retry semantics;
- transaction boundaries;
- idempotency;
- failure handling;
- secrets management;
- configuration handling.

---

# 13. Conformance as the Primary Arbiter

A key principle should be:

> Structure is negotiable. Conformance is not.

The generated application should be free to use a different internal design provided that it passes the required validation.

A conformance suite may include:

```text
Functional tests
API contract tests
Security tests
Authorisation tests
Configuration tests
Database behavioural tests
Failure-mode tests
Observability tests
Performance thresholds
Dependency rules
Static analysis
Integration tests
```

Example test organisation:

```text
tests/
├── unit/
├── integration/
└── conformance/
    ├── architecture/
    ├── security/
    ├── api/
    ├── configuration/
    ├── observability/
    └── performance/
```

---

# 14. Example Architectural Conformance Test

A simple example:

```python
def test_privileged_routes_require_authorization(app):
    privileged_routes = [
        route
        for route in app.routes
        if getattr(route, "privileged", False)
    ]

    assert privileged_routes, "No privileged routes were discovered"

    for route in privileged_routes:
        assert route.requires_authorization is True
```

The exact implementation may vary.

The important principle is that the test validates the property rather than a particular module layout.

---

# 15. Reducing Token Consumption

The first agent run used many tokens because the coding agent had to infer the architecture.

That may have looked roughly like:

```text
Requirement
    ↓
Read repository
    ↓
Infer capabilities
    ↓
Infer dependencies
    ↓
Infer mandatory behaviour
    ↓
Resolve ambiguity
    ↓
Generate application
```

A better future process is:

```text
Requirement
    ↓
Capability catalogue
    ↓
Relevant contracts and invariants
    ↓
Retrieve only required reference components
    ↓
Generate application
```

This changes the reference repository from something that must be repeatedly reverse-engineered into something that can be selectively retrieved.

---

# 16. Recommended Capability Catalogue

Example:

```yaml
capabilities:
  persistence:
    description: durable application state

    required_when:
      - persistent_state

    contracts:
      - DB-001
      - DB-002

    reference:
      - reference/database

    dependencies:
      - configuration

    optional_components:
      - migrations
      - connection_pooling

    exclude_unless_required:
      - migration_cli
      - database_admin_ui

    tests:
      - tests/conformance/database
```

A coding agent should only load the corresponding implementation when the capability is required.

---

# 17. Coding-Agent Operating Instructions

A concise instruction set for coding agents could be:

```text
OBJECTIVE

Construct the smallest maintainable implementation that satisfies the
application requirements and all architectural conformance criteria.

AUTHORITATIVE ORDER

1. Security, legal, and organisational requirements
2. Architectural invariants
3. Interface contracts
4. Application requirements
5. Acceptance and conformance tests
6. Reference implementation

REFERENCE IMPLEMENTATION

The reference implementation demonstrates one valid solution.

It is not a mandatory project template.

YOU MAY

- reorganise implementation structure;
- replace reference components;
- simplify reference patterns;
- omit unused capabilities;
- consolidate components where appropriate;
- introduce equivalent implementations where permitted.

YOU MUST

- preserve required interfaces;
- preserve security boundaries;
- preserve required operational behaviour;
- satisfy architectural invariants;
- satisfy conformance tests;
- avoid adding capabilities without a requirement;
- avoid removing behaviour merely because it is not locally consumed.

BEFORE USING A REFERENCE COMPONENT

Classify it as one of:

- MUST
- CONTRACT
- REFERENCE
- OPTIONAL

When the reference implementation and explicitly stated architectural
intent appear inconsistent, the explicitly stated architectural intent
takes precedence.
```

---

# 18. Recommended End-to-End Development Process

The overall process can be expressed as follows.

## Stage 1: Define the objective

Identify:

- business need;
- user need;
- expected outcome;
- functional requirements;
- non-functional requirements;
- security constraints;
- operational constraints;
- success criteria.

---

## Stage 2: Provide framework context

The coding agent receives only the context required to perform the task:

- architectural intent;
- applicable invariants;
- interface contracts;
- capability catalogue;
- relevant implementation guidance;
- relevant reference modules;
- conformance tests.

---

## Stage 3: Analyse and plan

The coding agent:

1. interprets the requirements;
2. maps requirements to capabilities;
3. determines mandatory capabilities;
4. identifies optional capabilities;
5. excludes irrelevant framework components;
6. identifies required contracts;
7. proposes an implementation plan.

---

## Stage 4: Generate the implementation

The coding agent:

- creates the application-specific code;
- integrates the required supporting services;
- adapts or replaces reference components;
- avoids unnecessary framework code;
- preserves contracts and mandatory behaviours.

---

## Stage 5: Validate

Automated validation should include:

- unit testing;
- integration testing;
- API contract validation;
- security testing;
- architectural conformance testing;
- performance testing where applicable;
- configuration validation;
- failure-mode testing.

Failures return to implementation.

---

## Stage 6: Human review

The human developer or reviewer evaluates:

- maintainability;
- architectural coherence;
- implementation quality;
- security implications;
- unnecessary complexity;
- unnecessary framework inheritance;
- suitability for the target application.

Required changes return to generation or refinement.

---

## Stage 7: Deploy

The approved application is:

- packaged;
- configured;
- deployed;
- initialised;
- smoke-tested;
- verified in the target environment.

---

## Stage 8: Operate and improve

Operational experience feeds back into:

- conformance tests;
- reference implementations;
- capability metadata;
- coding-agent instructions;
- framework documentation;
- architectural standards.

The reference architecture should therefore evolve based on evidence from actual generated systems.

---

# 19. Recommended Validation Experiments

The first successful test should be followed by deliberately more difficult tests.

## Test A: Near-reference application

Generate an application that closely resembles the reference implementation.

Purpose:

- establish a baseline;
- confirm expected capability mapping;
- identify obvious inference problems.

---

## Test B: Minimal application

Generate an application requiring only a small subset of the framework.

Purpose:

- test whether unnecessary code is correctly excluded;
- measure generated application size;
- measure token reduction.

---

## Test C: Unusual capability combination

Request a valid but uncommon set of capabilities.

Purpose:

- test composability;
- identify hidden coupling;
- expose assumptions built into the reference application.

---

## Test D: Remove an apparently unnecessary mandatory component

Deliberately obscure or remove a required cross-cutting concern.

Purpose:

- confirm that invariants and tests detect the missing behaviour.

---

## Test E: Conflicting reference and explicit instruction

Provide a reference implementation detail that differs from the current architectural requirement.

Purpose:

- verify that explicit intent overrides historical implementation.

---

## Test F: Fresh-agent test

Run the generation with a new coding-agent session and no previous conversational context.

Purpose:

- test whether the architecture is truly encoded in the repository and supporting metadata;
- avoid accidental dependence on prior context.

---

## Test G: Multi-model / multi-run comparison

Use several coding-agent runs or models.

Measure:

- consistency;
- architectural divergence;
- unnecessary code retention;
- conformance failures;
- token consumption;
- human review effort.

---

# 20. Metrics Worth Tracking

A useful evaluation set is:

```text
Functional correctness
Architectural conformance
Security failures
Unnecessary components retained
Generated code size
Token consumption
Agent iterations
Human review time
Post-generation defects
Deployment defects
Architectural deviations
Maintenance effort
Time to implement change
```

Over time this will allow comparison between:

- manual development;
- template-based development;
- agent-generated development from the reference architecture.

---

# 21. Communication Guidance by Audience

The architectural concept should remain the same, but the explanation should change according to the audience.

---

## 21.1 Senior Developers

Core message:

> The repository is a known-good executable reference, not a mandatory project template. Preserve contracts and invariants, but improve, simplify, or replace implementation where appropriate.

Important concepts:

- engineering judgement remains important;
- architecture is expressed through contracts and invariants;
- reference structure is intentionally non-authoritative;
- generated solutions may legitimately differ from the reference code;
- unnecessary framework inheritance is discouraged.

A useful review question is:

> Is this element an invariant, a contract, a useful reference pattern, or merely incidental implementation?

---

## 21.2 Foundation Engineers

Core message:

> Foundation engineering owns the stable capabilities, contracts, boundaries, and conformance mechanisms from which application implementations are generated.

Primary responsibilities:

- stable interfaces;
- security boundaries;
- configuration standards;
- observability;
- backward compatibility;
- capability metadata;
- reference implementations;
- conformance tests;
- dependency rules.

Foundation engineers are effectively maintaining the architectural language used by application generators.

---

## 21.3 Junior Developers

Core message:

> The framework is a working example, not a folder structure that must be copied.

Practical guidance:

- start with application requirements;
- use reference modules when useful;
- do not copy unused capabilities;
- do not bypass mandatory controls;
- rely on contracts and tests;
- ask whether a component is mandatory before preserving it.

Junior developers should not need to reverse-engineer the full architectural philosophy before safely making changes.

---

## 21.4 Technical Management

Core message:

> The organisation is moving from template-driven development toward constraint-driven application generation.

The coding agent has implementation freedom.

Engineering controls remain enforceable through:

- contracts;
- invariants;
- automated testing;
- security controls;
- versioned architecture metadata;
- human review.

Expected benefits include:

```text
Reduced boilerplate
Reduced unused code
Faster delivery
Greater implementation flexibility
Consistent controls
Reusable architectural knowledge
```

Required governance includes:

```text
Strong conformance testing
Versioned contracts
Human review
Security invariants
Repeatable agent instructions
Change control for architectural standards
```

---

## 21.5 Non-Technical Management

Core message:

> We maintain a proven application blueprint and mandatory engineering standards. AI development tools use those standards to build only the parts a new application needs. Engineers still define the standards, review the result, and maintain the underlying platform.

A useful analogy is building regulation.

The reference application is a completed building that demonstrates one valid implementation.

The standards define:

- what must be safe;
- what interfaces must work;
- what controls must exist;
- what inspections must pass.

A new building does not have to be an exact copy of the reference building.

---

## 21.6 Coding Agents

Coding agents should receive the most explicit rules.

They should be told clearly:

- what is authoritative;
- what is negotiable;
- what may be omitted;
- what must be preserved;
- what constitutes success;
- how to classify reference components;
- which tests determine conformance.

The aim is to reduce unnecessary inference while preserving implementation freedom.

---

# 22. Minimal Recommended Repository Additions

The framework should not be burdened with excessive documentation.

A small semantic layer is sufficient.

Recommended structure:

```text
repository/
├── ARCHITECTURE.md
├── capabilities.yaml
├── invariants.yaml
├── contracts/
│   ├── api/
│   ├── schemas/
│   └── interfaces/
├── tests/
│   └── conformance/
├── reference/
│   └── application/
└── src/
```

Potential role of each element:

## `ARCHITECTURE.md`

Contains:

- architectural intent;
- major boundaries;
- authority hierarchy;
- design principles;
- what is mandatory versus replaceable.

This should remain short.

---

## `capabilities.yaml`

Contains:

- available capabilities;
- activation conditions;
- dependencies;
- relevant reference modules;
- related tests.

---

## `invariants.yaml`

Contains mandatory properties.

Example:

```yaml
invariants:
  - id: SEC-001
    title: Authorize privileged operations
    statement: >
      Every privileged operation must be authorized before execution.

  - id: CFG-001
    title: Externalize secrets
    statement: >
      Secrets must not be embedded in application source code or static
      application configuration committed to source control.

  - id: AUD-001
    title: Preserve security audit events
    statement: >
      Security-relevant administrative and privileged actions must emit
      auditable events.
```

---

## `contracts/`

Contains machine-readable or directly testable contracts.

Examples:

- OpenAPI definitions;
- JSON schemas;
- event schemas;
- service interface specifications;
- database boundary definitions.

---

## `tests/conformance/`

Contains executable architectural validation.

This is where architectural intent becomes enforceable.

---

# 23. Deeper Engineering Interpretation

Traditional frameworks primarily reuse implementation.

This approach aims to reuse **architectural knowledge**.

Traditional model:

```text
Reference code
    ↓
Copy / inherit
    ↓
Modify
```

Proposed model:

```text
Requirements
+
Constraints
+
Architectural knowledge
+
Reference implementation
+
Acceptance tests
        ↓
    Coding agent
        ↓
Synthesised application
```

This is closer to a form of architectural compilation.

The inputs are:

- requirements;
- constraints;
- standards;
- examples;
- contracts;
- tests.

The output is software.

That model is particularly compatible with coding agents because the agent can optimise implementation while remaining bounded by explicit system-level requirements.

---

# 24. Primary Recommendation

The key recommendation is **not** to add extensive documentation or impose a more rigid framework structure.

Instead, add a thin semantic layer above the code.

That layer should make explicit:

- architectural intent;
- mandatory invariants;
- interface contracts;
- capability boundaries;
- component classification;
- conformance criteria.

The reference implementation should remain:

- executable;
- minimal;
- representative;
- replaceable;
- non-authoritative where explicit architecture says otherwise.

The desired outcome is:

```text
Humans can understand intent without reverse-engineering the repository.

Coding agents can retrieve only the context they need.

Generated applications contain only necessary capabilities.

Foundation engineers retain control over stable system boundaries.

Management receives consistent governance and delivery outcomes.

Architectural freedom remains high.

Conformance remains strict.
```

---

# 25. Concise Architectural Principle

The architecture can be summarised in one sentence:

> **Provide a known-good executable reference, make mandatory intent explicit, allow implementation freedom, and enforce outcomes through contracts and conformance tests.**

A second useful principle is:

> **Structure is negotiable. Conformance is not.**

And for documentation:

> **Document intent, invariants, and contracts. Let the code document implementation.**
