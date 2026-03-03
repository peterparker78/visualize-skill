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
1. **Isomorphism test**: If you removed all text, would the structure alone communicate the concept?
2. **Education test**: Could someone learn something concrete from this? A good diagram teaches — it doesn't just label boxes.

Each shape mirrors behavior. Each color encodes purpose. Structure + labels explain the concept — no extra description needed.

## Depth Assessment

Before starting, classify the request:

**Simple/Conceptual** — overview, brainstorm, learning aid:
- 5-15 shapes, single-pass generation
- Focus on clarity and visual argument
- One zoom level

**Comprehensive/Technical** — architecture, protocol, detailed system:
- 15+ shapes, section-by-section generation (see Large Diagram Strategy)
- Research real specs/APIs/event names before drawing — never guess technical details
- Multi-zoom: summary flow visible at distance, detail visible when zoomed in
- Include evidence artifacts: code snippets, JSON payloads, real method names

## Workflow

1. **Assess depth** — Simple or Comprehensive? (see above)
2. **Analyze** the concept — sequential? hierarchical? cyclical? comparative?
3. **Select diagram type** matching the concept's nature (see Diagram Types)
4. **Select visual patterns** from [references/diagram-patterns.md](references/diagram-patterns.md) — ensure variety (no two major concepts use the same pattern)
5. **Plan layout** — sketch node positions, connections, and groupings mentally before writing JSON
6. **Generate `.excalidraw` JSON** — write valid Excalidraw JSON to `<name>.excalidraw`
   - For comprehensive diagrams: generate section-by-section (see Large Diagram Strategy)
7. **Validate layout** — run `python3 <skill_path>/scripts/validate_layout.py <name>.excalidraw --min-gap 20`
   - Fix all errors (overlapping shapes, lines through shapes) before rendering
   - Re-validate until PASS
8. **Render to PNG** — run `python3 <skill_path>/scripts/render_excalidraw.py <name>.excalidraw`
9. **Visual inspection** — Read the PNG with the Read tool and audit:
   - Text clipping or overflow beyond shape boundaries?
   - Overlapping elements the validator missed?
   - Unbalanced whitespace or lopsided composition?
   - Arrows landing in wrong places?
   - Readable at the rendered size?
   - Fix issues and re-render until satisfied
10. **Show the PNG** to the user

For schema details, read [references/excalidraw-schema.md](references/excalidraw-schema.md).
For layout patterns, read [references/diagram-patterns.md](references/diagram-patterns.md).
For colors, read [references/color-palette.md](references/color-palette.md).

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
| System architecture | **Architecture** | Fan-out from hubs, assembly lines, layers |

## Shape-Meaning Conventions

| Shape | Meaning | Excalidraw type |
|-------|---------|----------------|
| Rounded rectangle | Start/end points, terminals | `rectangle` + `roundness: {type: 3}` |
| Rectangle | Processes, actions, concrete steps | `rectangle` |
| Diamond | Decisions, branch points, conditions | `diamond` |
| Ellipse | Events, triggers, outputs, results | `ellipse` |
| Small dot (12x12 ellipse) | Timeline markers, bullet points | `ellipse` |

Use shape differences to encode meaning — not just for variety.

## Color Rules

Colors are defined in [references/color-palette.md](references/color-palette.md). Assign by semantic role, not randomly. Key principle: the same color always means the same thing within a diagram.

For mind maps: assign each primary branch a distinct color family, sub-nodes inherit parent color.

## Text & Container Discipline

**Default to free-floating text.** Only put text inside containers (shapes) when the container carries meaning (e.g., a process box, a decision diamond). Labels, annotations, titles, and legends should be free-floating text with typography hierarchy.

**Target: <30% of text elements inside containers.** This prevents the common "card grid" anti-pattern where every label is boxed.

**Typography hierarchy** (use size and color, not containers, to create hierarchy):
- Title: fontSize 28-32, white
- Section headers: fontSize 20-24, white
- Labels: fontSize 16-18, light gray `#ced4da`
- Annotations: fontSize 12-14, muted gray `#868e96`
- Monospace (`fontFamily: 3`): for code, commands, file names

## Size Hierarchy

| Level | Size | Use for |
|-------|------|---------|
| Hero | 200-300px wide, 80-150px tall | Central concept, main subject |
| Primary | 140-180px wide, 60-90px tall | Major branches, key steps |
| Secondary | 100-140px wide, 40-60px tall | Sub-items, leaves, details |
| Small | 60-100px wide, 30-40px tall | Annotations, markers, dots |

## Layout Essentials

- **Spacing**: 60px+ horizontal gaps, 50px+ vertical gaps between shapes
- **Dark theme** (default): background `#1e1e2e`, strokes white/light gray, light fills
- **Roughness**: Use `1` (sketchy hand-drawn look) for learning diagrams, `0` for technical
- **Opacity**: Always `100` for shapes. Use color and size for hierarchy, not transparency.
- **Z-order**: backgrounds first, then shapes, then text, then arrows last
- **Bindings**: Always add arrow refs to shape's `boundElements` and shape refs to arrow's `startBinding`/`endBinding`
- **IDs**: Use descriptive strings like `"trigger_rect"`, `"arrow_a_to_b"` — not random numbers

### Anti-Overlap Rules (Critical)

- **Leaf placement**: Place leaf/child nodes on the OPPOSITE side of their parent from the center hub. For top branches, leaves go above. For bottom branches, leaves go below. For side branches, leaves extend outward.
- **Line clearance**: Hub-to-branch lines must not pass through any leaf node bounding box. Mentally trace each line from center to branch and verify no other shape sits in the path.
- **Sibling spacing**: Leaf nodes sharing a parent must have 25px+ gap between them.
- **Validation**: Always run `validate_layout.py` after generating JSON. Fix all errors before rendering.

## Large Diagram Strategy

For diagrams with 15+ shapes, do NOT generate the entire JSON in a single pass.

**Section-by-section process:**
1. Divide the diagram into logical sections (3-6 sections)
2. Generate each section's elements sequentially
3. Use section-namespaced seeds (section 1: 100xxx, section 2: 200xxx) to prevent ID collisions
4. After each section, update cross-section arrow bindings immediately
5. After all sections: review full JSON for binding consistency and spacing balance

This prevents token limit issues and produces better-organized JSON.

## Quality Checklist

Run through before delivering the final diagram:

**Conceptual Quality:**
- [ ] Isomorphism test passes — structure communicates without text
- [ ] Visual variety — no two major concepts use the same pattern
- [ ] Container discipline — <30% text in containers
- [ ] Appropriate depth — matches Simple vs Comprehensive assessment

**Structural Quality:**
- [ ] All connections properly bound (startBinding/endBinding + boundElements)
- [ ] Clear flow direction — viewer knows where to start reading
- [ ] Size hierarchy — important things are bigger

**Layout Quality (automated + visual):**
- [ ] `validate_layout.py` returns PASS
- [ ] No text clipping beyond shape boundaries (visual check)
- [ ] Balanced composition — no large empty areas vs crowded areas
- [ ] Arrows route cleanly — no unexpected crossings
- [ ] Readable at rendered size

## Output

Save files to the current working directory:
- `<descriptive-name>.excalidraw` — editable in excalidraw.com or VS Code Excalidraw extension
- `<descriptive-name>.png` — rendered image for immediate viewing

Tell the user: "Open the `.excalidraw` file at https://excalidraw.com to edit, or view the PNG directly."
