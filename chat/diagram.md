# Technical Guidelines: API-Driven Diagram Generation and Browser Rendering

## 1. Purpose

This document defines a recommended architecture for generating, storing, and rendering technical diagrams using an AI model, middleware, a native JSON persistence format, Mermaid as a rendering target, and vanilla JavaScript in the browser.

The core design principle is:

> Store diagrams as canonical structured JSON. Treat Mermaid as a derived rendering format. Treat SVG as the final visual output.

This approach keeps the system deterministic, editable, secure, portable, and suitable for production use.

---

## 2. Design Goals

The solution should support:

* AI-assisted diagram generation from natural language prompts.
* Middleware-controlled validation and normalization.
* Native JSON storage as the durable source of truth.
* Browser-side rendering using vanilla JavaScript.
* Mermaid-based diagram rendering without requiring React or a complex frontend framework.
* Safe handling of AI-generated content.
* Future support for alternative renderers such as SVG, Canvas, React Flow, Excalidraw, or Graphviz.

---

## 3. Recommended Architecture

```text
User request
   ↓
OpenAI API
   ↓
Structured diagram JSON
   ↓
Middleware validation and normalization
   ↓
Database persistence
   ↓
Browser fetches canonical JSON
   ↓
Browser converts JSON to Mermaid syntax
   ↓
Mermaid renders SVG in the browser
```

The model should not be treated as the final renderer. The model should be used to infer structure, relationships, hierarchy, labels, and intent. Rendering should remain under application control.

---

## 4. Canonical Data Model

The middleware should store diagrams in a native JSON structure, not raw Mermaid syntax.

Example:

```json
{
  "id": "diag_001",
  "schema_version": "1.0",
  "type": "flowchart",
  "direction": "LR",
  "title": "Customer Support AI Agent",
  "nodes": [
    {
      "id": "inbox",
      "label": "Customer inbox",
      "shape": "rect"
    },
    {
      "id": "ingest",
      "label": "Message ingestion",
      "shape": "rect"
    },
    {
      "id": "agent",
      "label": "AI agent",
      "shape": "rect"
    },
    {
      "id": "approval",
      "label": "Human approval required?",
      "shape": "diamond"
    },
    {
      "id": "crm",
      "label": "CRM update",
      "shape": "rect"
    }
  ],
  "edges": [
    {
      "from": "inbox",
      "to": "ingest"
    },
    {
      "from": "ingest",
      "to": "agent"
    },
    {
      "from": "agent",
      "to": "approval"
    },
    {
      "from": "approval",
      "to": "crm",
      "label": "No"
    },
    {
      "from": "approval",
      "to": "agent",
      "label": "Revise"
    }
  ]
}
```

The JSON model is the durable product data. Mermaid is only an output adapter.

---

## 5. Why Store JSON Instead of Mermaid?

Mermaid is useful, but it should not usually be the system-of-record format.

Canonical JSON provides:

* Easier validation.
* Safer rendering.
* Cleaner database storage.
* Better diffing and versioning.
* Easier editing in a UI.
* Easier transformation into other formats.
* Less risk from arbitrary model-generated syntax.
* Better ability to enforce business rules.

Mermaid can be regenerated at any time from the canonical JSON.

---

## 6. Middleware Responsibilities

The middleware should handle the trusted parts of the workflow.

Responsibilities include:

1. Submit user intent to the AI model.
2. Request structured JSON only.
3. Validate the model output against a schema.
4. Reject or repair invalid diagrams.
5. Normalize node IDs.
6. Ensure every edge references valid nodes.
7. Enforce supported diagram types and shapes.
8. Store the canonical JSON.
9. Optionally cache derived Mermaid or SVG.
10. Return JSON to the browser for rendering.

The middleware should not blindly persist arbitrary model output.

---

## 7. AI Model Output Contract

The model should be instructed to return JSON only.

Example instruction:

```text
Return only canonical diagram JSON.
Do not return Mermaid.
Do not return Markdown.
All node IDs must be lowercase snake_case.
Every edge.from and edge.to must reference an existing node ID.
Supported node shapes are: rect, round, diamond, circle.
Supported diagram types are: flowchart.
```

The preferred production pattern is to combine prompting with structured schema enforcement.

The model’s role is to create a valid semantic graph. The renderer’s role is to create pixels.

---

## 8. Suggested JSON Schema Rules

At minimum, the schema should enforce:

* `type` must be one of the supported diagram types.
* `direction` must be one of `TD`, `TB`, `BT`, `LR`, or `RL`.
* `nodes` must be a non-empty array.
* Each node must have a unique `id`.
* Each node must have a non-empty `label`.
* Each node must use a supported `shape`.
* `edges` must be an array.
* Each edge must reference existing node IDs.
* Edge labels should be optional strings.
* Unknown fields should either be rejected or safely ignored.

Recommended supported node shapes:

```text
rect
round
diamond
circle
```

Recommended supported diagram type for the initial implementation:

```text
flowchart
```

Additional types such as sequence diagrams, state diagrams, class diagrams, and entity relationship diagrams can be added later as separate schemas.

---

## 9. Database Storage Pattern

A practical persisted record may look like this:

```json
{
  "diagram_id": "diag_001",
  "schema_version": "1.0",
  "canonical_spec": {
    "type": "flowchart",
    "direction": "LR",
    "nodes": [],
    "edges": []
  },
  "derived": {
    "mermaid": null,
    "svg_cache": null
  },
  "created_at": "2026-06-23T10:00:00Z",
  "updated_at": "2026-06-23T10:00:00Z"
}
```

The `canonical_spec` is authoritative.

The `derived` section is optional and should be treated as disposable cache.

---

## 10. Browser Rendering Strategy

The browser should:

1. Fetch the canonical JSON from the middleware.
2. Convert the JSON into Mermaid syntax.
3. Ask Mermaid to parse and render the diagram.
4. Insert the generated SVG into the DOM.

This can be done with vanilla JavaScript.

Example:

```html
<div id="diagram"></div>

<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
    theme: "default"
  });

  const diagramJson = {
    id: "diag_001",
    type: "flowchart",
    direction: "LR",
    title: "Customer Support AI Agent",
    nodes: [
      { id: "inbox", label: "Customer inbox", shape: "rect" },
      { id: "ingest", label: "Message ingestion", shape: "rect" },
      { id: "agent", label: "AI agent", shape: "rect" },
      { id: "approval", label: "Human approval required?", shape: "diamond" },
      { id: "crm", label: "CRM update", shape: "rect" }
    ],
    edges: [
      { from: "inbox", to: "ingest" },
      { from: "ingest", to: "agent" },
      { from: "agent", to: "approval" },
      { from: "approval", to: "crm", label: "No" },
      { from: "approval", to: "agent", label: "Revise" }
    ]
  };

  function escapeMermaidLabel(value) {
    return String(value ?? "")
      .replace(/"/g, "#quot;")
      .replace(/\n/g, "<br/>");
  }

  function renderNode(node) {
    const id = node.id;
    const label = escapeMermaidLabel(node.label);

    switch (node.shape) {
      case "diamond":
        return `${id}{"${label}"}`;
      case "circle":
        return `${id}(("${label}"))`;
      case "round":
        return `${id}("${label}")`;
      case "rect":
      default:
        return `${id}["${label}"]`;
    }
  }

  function renderEdge(edge) {
    const label = edge.label ? `|${escapeMermaidLabel(edge.label)}|` : "";
    return `${edge.from} -->${label} ${edge.to}`;
  }

  function toMermaid(spec) {
    if (spec.type !== "flowchart") {
      throw new Error(`Unsupported diagram type: ${spec.type}`);
    }

    const direction = spec.direction || "TD";

    return [
      `flowchart ${direction}`,
      ...spec.nodes.map(node => `  ${renderNode(node)}`),
      ...spec.edges.map(edge => `  ${renderEdge(edge)}`)
    ].join("\n");
  }

  async function renderDiagram(spec, targetElementId) {
    const target = document.getElementById(targetElementId);
    const mermaidText = toMermaid(spec);

    try {
      await mermaid.parse(mermaidText);

      const renderId = `mermaid-${spec.id || crypto.randomUUID()}`;
      const { svg } = await mermaid.render(renderId, mermaidText);

      target.innerHTML = svg;
    } catch (error) {
      console.error(error);
      target.textContent = "Unable to render diagram.";
    }
  }

  renderDiagram(diagramJson, "diagram");
</script>
```

---

## 11. Security Guidelines

AI-generated diagram content should be treated as untrusted input.

Recommended security controls:

* Use Mermaid with `securityLevel: "strict"`.
* Validate JSON server-side before storage.
* Escape all labels before generating Mermaid syntax.
* Do not allow arbitrary Mermaid from the model unless explicitly needed.
* Do not enable clickable links or embedded HTML by default.
* Do not persist raw unvalidated model output.
* Use a restrictive Content Security Policy where possible.
* Avoid rendering diagrams with elevated privileges.
* Consider sandboxing if allowing rich Mermaid features later.

For most use cases, avoid Mermaid features that allow links, scripts, callbacks, or raw HTML.

---

## 12. Rendering Modes

There are three useful rendering modes.

### 12.1 Client-side render

The browser receives JSON and renders the diagram using Mermaid.

Best for:

* Lightweight applications.
* Interactive editing.
* Fast iteration.
* Avoiding server render infrastructure.

### 12.2 Server-side render

The backend converts JSON to SVG and sends rendered SVG to the browser.

Best for:

* Static exports.
* PDFs.
* Emails.
* Environments where frontend JavaScript is restricted.
* Strict rendering consistency.

### 12.3 Hybrid render

The backend stores canonical JSON and may cache Mermaid or SVG as derived artifacts.

Best for:

* Production applications.
* Performance optimization.
* Repeated viewing of stable diagrams.
* Auditability plus fast display.

Recommended default:

```text
Store JSON.
Generate Mermaid on demand.
Render in browser.
Optionally cache SVG.
```

---

## 13. Versioning Guidelines

Include a `schema_version` field in every diagram record.

Example:

```json
{
  "schema_version": "1.0"
}
```

Versioning allows the schema to evolve without breaking existing diagrams.

Possible future schema changes:

* Grouped nodes.
* Swimlanes.
* Subgraphs.
* Theming.
* Node metadata.
* Edge types.
* Layout hints.
* Comments.
* Ownership/audit fields.
* Alternative rendering engines.

Never assume all persisted diagrams conform to the latest schema.

---

## 14. Error Handling

The system should handle errors at each stage.

### Model output errors

Possible issue:

```text
The model returns malformed JSON.
```

Recommended handling:

* Reject the response.
* Ask the model to repair the JSON.
* Log the error.
* Do not persist the invalid response.

### Schema validation errors

Possible issue:

```text
An edge references a missing node.
```

Recommended handling:

* Reject or repair the diagram.
* Return a clear error to the caller.
* Do not render partially invalid graphs unless explicitly supported.

### Mermaid render errors

Possible issue:

```text
The generated Mermaid syntax fails to parse.
```

Recommended handling:

* Display a fallback error message.
* Log the generated Mermaid text for debugging.
* Keep the canonical JSON intact.
* Repair the JSON-to-Mermaid adapter rather than editing the persisted data manually.

---

## 15. Diagram Editing Model

For editable diagrams, edits should modify the canonical JSON, not the Mermaid text.

Example operations:

```text
Add node
Remove node
Rename node
Change node shape
Add edge
Remove edge
Change edge label
Change layout direction
```

Each operation should update the JSON model, after which Mermaid is regenerated.

This keeps the editor deterministic and avoids round-tripping through Mermaid syntax.

---

## 16. Recommended API Endpoints

A simple middleware API could expose:

```text
POST /diagrams/generate
GET /diagrams/:id
PUT /diagrams/:id
POST /diagrams/:id/render
DELETE /diagrams/:id
```

Example responsibilities:

### `POST /diagrams/generate`

Accepts natural language intent and returns validated canonical JSON.

### `GET /diagrams/:id`

Returns the stored canonical JSON.

### `PUT /diagrams/:id`

Updates the canonical JSON after validation.

### `POST /diagrams/:id/render`

Optionally returns Mermaid, SVG, or both as derived artifacts.

### `DELETE /diagrams/:id`

Deletes the diagram record.

---

## 17. Recommended Data Contract

Example response from `GET /diagrams/:id`:

```json
{
  "diagram_id": "diag_001",
  "schema_version": "1.0",
  "canonical_spec": {
    "type": "flowchart",
    "direction": "LR",
    "title": "Customer Support AI Agent",
    "nodes": [
      {
        "id": "inbox",
        "label": "Customer inbox",
        "shape": "rect"
      }
    ],
    "edges": []
  }
}
```

Example render response:

```json
{
  "diagram_id": "diag_001",
  "format": "mermaid",
  "content": "flowchart LR\n  inbox[\"Customer inbox\"]"
}
```

---

## 18. Implementation Principles

Use the following principles when building the system:

1. The model generates structure, not final pixels.
2. JSON is the source of truth.
3. Mermaid is a rendering adapter.
4. SVG is an output artifact.
5. Middleware validates all model output.
6. Browser rendering should be simple and deterministic.
7. AI-generated text should be treated as untrusted input.
8. Diagram editing should mutate JSON, not Mermaid.
9. Derived artifacts should be disposable.
10. Schema versioning should be included from the beginning.

---

## 19. Initial MVP Scope

The initial version should support only:

* Flowcharts.
* Direction: `TD`, `LR`.
* Node shapes: `rect`, `round`, `diamond`, `circle`.
* Directed edges.
* Optional edge labels.
* Browser-side Mermaid rendering.
* Server-side JSON validation.
* Stored canonical JSON.

Avoid supporting advanced Mermaid features in the MVP, such as:

* Raw Mermaid editing.
* Clickable links.
* Embedded HTML.
* Custom themes.
* Complex subgraphs.
* Sequence diagrams.
* Class diagrams.
* State diagrams.
* Arbitrary user-authored Mermaid.

These can be added later once the security and data model are stable.

---

## 20. Summary Recommendation

The best implementation is:

```text
OpenAI API
+ structured JSON output
+ middleware schema validation
+ canonical JSON persistence
+ browser-side JSON-to-Mermaid adapter
+ Mermaid SVG rendering in vanilla JavaScript
```

This gives the system a clean separation of concerns:

```text
AI model: infer diagram structure
Middleware: validate and persist
JSON: durable source of truth
Mermaid: rendering syntax
Browser: visual rendering
SVG: final display artifact
```

This design avoids coupling the product data model to a single rendering language while still getting the speed and convenience of Mermaid for browser-based diagram rendering.
