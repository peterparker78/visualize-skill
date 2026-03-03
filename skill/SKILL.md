---
name: visualize
description: >
  Generate visual diagrams as Excalidraw JSON (.excalidraw) and PNG files for learning and
  explanation. Supports flowcharts, mind maps, concept comparisons, process explanations,
  hierarchies, timelines, and cycle diagrams. Use when the user says /visualize, asks to
  "draw a diagram", "visualize this", "make a flowchart", "create a mind map", or wants
  any visual explanation of a concept, process, or system. Also triggers on requests like
  "explain X visually", "diagram this", or "show me how X works as a diagram".
---

# Visualize Skill

Generate educational Excalidraw diagrams that teach through structure, not decoration.

## Core Philosophy

**Argue visually, don't just display.** Every diagram must pass two tests:
1. **Isomorphism test**: Does the visual structure mirror the concept's behavior? The flow itself should teach.
2. **Education test**: Could someone learn something concrete from this? A good diagram teaches — it doesn't just label boxes.

Each shape mirrors behavior. Each color encodes purpose. Structure + labels explain the concept — no extra description needed.

## Workflow

1. **Analyze** the concept to identify its structure (sequential? hierarchical? cyclical? comparative?)
2. **Select diagram type** matching the concept's nature (see Diagram Types below)
3. **Plan layout** — sketch node positions, connections, and groupings mentally before writing JSON
4. **Generate `.excalidraw` JSON** — write valid Excalidraw JSON to `<name>.excalidraw`
5. **Validate layout** — run `python3 <skill_path>/scripts/validate_layout.py <name>.excalidraw --min-gap 20`
   - Fix all errors (overlapping shapes, lines passing through unrelated shapes) before rendering
   - Warnings about close shapes should also be addressed
   - Re-validate until PASS
6. **Render to PNG** — run `python3 <skill_path>/scripts/render_excalidraw.py <name>.excalidraw`
7. **Show the PNG** to the user using the Read tool

For schema details, read [references/excalidraw-schema.md](references/excalidraw-schema.md).
For layout patterns and a complete JSON example, read [references/diagram-patterns.md](references/diagram-patterns.md).

## Diagram Types

| Request | Type | Layout |
|---------|------|--------|
| Process, workflow, how-to | **Flowchart** | Left-to-right or top-to-bottom linear/branching |
| Brainstorm, topic overview | **Mind Map** | Radial from center or hierarchical tree |
| "X vs Y", tradeoffs | **Comparison** | Side-by-side groups with VS separator |
| Categories, taxonomy | **Hierarchy** | Tree from top to bottom |
| Repeating process | **Cycle** | Circular arrangement with arrows |
| Steps over time | **Timeline** | Horizontal with time markers |
| How something works | **Process Explanation** | Shape-per-role flow with transforms |

## Shape-Meaning Conventions

- **Rounded rectangle**: Start/end points, terminals
- **Rectangle**: Processes, actions, concrete steps
- **Diamond**: Decisions, branch points, conditions
- **Ellipse**: Events, triggers, outputs, results
- Use shape differences to encode meaning — not just for variety

## Color Rules

Assign colors by semantic role, not randomly:
- **Blue** (#4a9eed / #a5d8ff): Primary flow, main concepts
- **Green** (#22c55e / #b2f2bb): Success, output, completion
- **Amber** (#f59e0b / #ffd8a8): Processing, transformation, warnings
- **Red** (#ef4444 / #ffc9c9): Errors, critical paths, blockers
- **Purple** (#8b5cf6 / #d0bfff): Decisions, logic, branching
- **Teal** (#06b6d4 / #c3fae8): Data, inputs, external systems

For mind maps: assign each primary branch a distinct color family, sub-nodes inherit parent color.

## Layout Essentials

- **Spacing**: 60px+ horizontal gaps, 50px+ vertical gaps between shapes
- **Standard sizes**: Rectangles 140x60, diamonds/ellipses 80x80, titles fontSize 28
- **Dark theme** (default): background `#1e1e2e`, strokes white/light gray, light fills
- **Roughness**: Use `1` (sketchy hand-drawn look) for learning diagrams
- **Z-order**: backgrounds first, then shapes, then text, then arrows last
- **Bindings**: Always add arrow refs to shape's `boundElements` and shape refs to arrow's `startBinding`/`endBinding`

### Anti-Overlap Rules (Critical)

- **Leaf placement**: Place leaf/child nodes on the OPPOSITE side of their parent from the center hub. For top branches, leaves go above. For bottom branches, leaves go below. For side branches, leaves extend outward.
- **Line clearance**: Hub-to-branch lines must not pass through any leaf node bounding box. Mentally trace each line from center to branch and verify no other shape sits in the path.
- **Sibling spacing**: Leaf nodes sharing a parent must have 25px+ gap between them horizontally and vertically.
- **Validation**: Always run `validate_layout.py` after generating JSON. Fix all errors before rendering.

## Output

Save files to the current working directory:
- `<descriptive-name>.excalidraw` — editable in excalidraw.com or VS Code Excalidraw extension
- `<descriptive-name>.png` — rendered image for immediate viewing

Tell the user: "Open the `.excalidraw` file at https://excalidraw.com to edit, or view the PNG directly."
