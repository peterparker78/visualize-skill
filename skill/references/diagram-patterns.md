# Diagram Pattern Library

## Table of Contents
- [Visual Patterns](#visual-patterns)
- [Flowchart Patterns](#flowchart-patterns)
- [Mind Map Patterns](#mind-map-patterns)
- [Learning Diagrams](#learning-diagrams)
- [Layout Rules](#layout-rules)
- [Complete Example](#complete-example)

## Visual Patterns

Compositional patterns to choose from. **Ensure variety** — no two major concepts in the same diagram should use the same pattern.

### Fan-Out
One source radiating to many targets. Use for hubs, event emitters, one-to-many relationships.
```
                --> [Target A]
[Source] -----> --> [Target B]
                --> [Target C]
```

### Convergence
Many inputs merging into one. Use for aggregation, funnels, synthesis.
```
[Input A] --\
[Input B] ----> [Result]
[Input C] --/
```

### Assembly Line
Linear transform chain. Use for pipelines, data processing, build steps.
```
[Raw] --> (Parse) --> [Structured] --> (Validate) --> [Clean] --> (Store) --> [DB]
```
Use different shapes for data (rectangles) vs transforms (ellipses/diamonds).

### Tree
Hierarchical branching using `line` elements + free-floating text (no boxes on leaves).
```
         Root
        / | \
      A   B   C
     / \
    A1  A2
```
Best for taxonomies, file systems, org charts. Use `line` type as scaffolding, NOT arrows.

### Spiral / Cycle
Sequence with return arrow. Use for feedback loops, iteration, continuous processes.
```
[Plan] --> [Do] --> [Check] --> [Act]
  ^                               |
  +-------------------------------+
```

### Cloud
Overlapping ellipses forming an amorphous group. Use for abstract concepts, state, context.
```
  (Memory)
(Context)(State)
  (Cache)
```

### Side-by-Side
Two parallel structures. Use for before/after, comparisons, tradeoffs.
```
[Before]          [After]
  |                  |
[Step 1]          [Step 1]
  |                  |
[Step 2]          [Step 2]
```
Place a "VS" or divider line between the two groups.

### Gap / Break
Visual whitespace or barrier between sections. Use for phase transitions, context resets.
```
[Phase 1] --> [Step] --> [Step]    |||    [Phase 2] --> [Step] --> [Step]
```

### Lines as Structure
Use `line` type (not arrows) as primary scaffolding — timelines, tree branches, dividers, grouping borders.
```
─────────────────────────────────
  2024    │    2025    │    2026
─────────────────────────────────
```

## Flowchart Patterns

### Linear Flow
```
[Start] --> [Process A] --> [Process B] --> [End]
```
- Use rectangles for processes, rounded for start/end
- Arrows flow left-to-right or top-to-bottom
- Space shapes 60-80px apart minimum

### Decision Flow
```
[Start] --> <Decision?> --Yes--> [Action A] --> [End]
                        --No---> [Action B] --> [End]
```
- Use diamonds for decisions
- Label arrows with decision outcomes
- Keep Yes/No paths visually distinct (different colors)

### Parallel Flow
```
[Start] --> [Fork] --> [Path A] --> [Join] --> [End]
                   --> [Path B] -->
```

### Shape-to-Meaning Mapping
| Shape | Meaning | Excalidraw type |
|-------|---------|----------------|
| Rounded rectangle | Start/End/Terminal | rectangle + roundness |
| Rectangle | Process/Action | rectangle |
| Diamond | Decision/Branch | diamond |
| Ellipse | Event/Trigger/Output | ellipse |

## Mind Map Patterns

### Radial Layout
Central topic in the middle, branches radiate outward:
```
                [Branch A]
                    |
[Branch D] --- [CENTRAL] --- [Branch B]
                    |
                [Branch C]
```

**Layout algorithm:**
1. Place central node at (500, 380) with hero size (200x100)
2. Calculate N branch positions evenly around a circle (radius 300-400px)
3. For each branch, place sub-branches further out (radius +200px) on the OPPOSITE side from center
4. Connect center→branch with colored lines (not arrows), branch→leaf with thinner lines
5. Leaves must NOT sit between their parent and the center

### Hierarchical Mind Map
```
[Root]
├── [Branch 1]
│   ├── [Leaf 1a]
│   └── [Leaf 1b]
├── [Branch 2]
│   └── [Leaf 2a]
└── [Branch 3]
```

**Layout algorithm:**
1. Root at top-center (400, 50)
2. First-level branches spread horizontally below (y + 150)
3. Each sub-level adds y + 120, spread under parent's x range
4. Connect parent to children with lines

### Color-Coding Branches
See [references/color-palette.md](color-palette.md) for the branch color assignment order. Sub-nodes inherit their parent branch color.

## Learning Diagrams

### Concept Comparison (VS diagram)
```
[Concept A]          VS          [Concept B]
- Feature 1                      - Feature 1
- Feature 2                      - Feature 2
```
Place two groups side by side with a "VS" text element between them. Use Side-by-Side pattern.

### Process Explanation
```
[Input] -> (Transform) -> [Intermediate] -> (Transform) -> [Output]
```
Use Assembly Line pattern. Different shapes for different roles.

### Hierarchy/Taxonomy
```
         [Parent Concept]
        /        |        \
[Type A]    [Type B]    [Type C]
```
Use Tree pattern with lines, prefer free-floating text for leaves.

### Cause-Effect Chain
```
[Root Cause] --> [Effect 1] --> [Effect 2] --> [Final Impact]
                     |
                 [Side Effect]
```

### Timeline/Sequence
```
[Step 1] --> [Step 2] --> [Step 3] --> [Step 4]
  2024        2025         2026         2027
```
Use Lines as Structure pattern for the timeline rail.

### Cycle Diagram
```
[Stage 1] --> [Stage 2]
    ^              |
    |              v
[Stage 4] <-- [Stage 3]
```
Use Spiral/Cycle pattern.

## Layout Rules

### Spacing
- Minimum 60px between shapes horizontally
- Minimum 50px between shapes vertically
- Arrow gap from shapes: 5-8px
- Canvas padding: 40px on all sides
- Hero nodes get 200px+ empty space around them

### Alignment
- Align related shapes on the same Y coordinate for horizontal flows
- Align related shapes on the same X coordinate for vertical flows
- Center text labels below or inside shapes

### Sizing
| Level | Width | Height | Use |
|-------|-------|--------|-----|
| Hero | 200-300 | 80-150 | Central node, main subject |
| Primary | 140-180 | 60-90 | Major branches, key steps |
| Secondary | 100-140 | 40-60 | Sub-items, leaves |
| Small | 60-100 | 30-40 | Markers, annotations |
| Title text | fontSize 28-32 | | |
| Label text | fontSize 16-20 | | |
| Annotation text | fontSize 12-16 | | |

### Dark Theme Defaults
- Background: `#1e1e2e` (deep navy)
- Stroke: `#ffffff` or `#ced4da` (light gray)
- Text: `#ffffff`
- Use lighter fill colors for contrast against dark bg

### Light Theme Defaults
- Background: `#ffffff`
- Stroke: `#1e1e1e`
- Text: `#1e1e1e`

## Complete Example

### Simple Flowchart (3-step process)

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "claude-visualize-skill",
  "elements": [
    {
      "id": "rect_start",
      "type": "rectangle",
      "x": 50,
      "y": 50,
      "width": 140,
      "height": 60,
      "strokeColor": "#4a9eed",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "groupIds": [],
      "frameId": null,
      "roundness": { "type": 3 },
      "seed": 100,
      "version": 1,
      "versionNonce": 1,
      "isDeleted": false,
      "boundElements": [
        { "id": "text_start", "type": "text" },
        { "id": "arrow_1", "type": "arrow" }
      ],
      "updated": 1,
      "link": null,
      "locked": false
    },
    {
      "id": "text_start",
      "type": "text",
      "x": 80,
      "y": 65,
      "width": 80,
      "height": 25,
      "text": "Start",
      "fontSize": 20,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "rect_start",
      "originalText": "Start",
      "autoResize": true,
      "lineHeight": 1.25,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 101,
      "version": 1,
      "versionNonce": 1,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1,
      "link": null,
      "locked": false
    },
    {
      "id": "rect_process",
      "type": "rectangle",
      "x": 270,
      "y": 50,
      "width": 140,
      "height": 60,
      "strokeColor": "#f59e0b",
      "backgroundColor": "#ffd8a8",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 200,
      "version": 1,
      "versionNonce": 1,
      "isDeleted": false,
      "boundElements": [
        { "id": "text_process", "type": "text" },
        { "id": "arrow_1", "type": "arrow" },
        { "id": "arrow_2", "type": "arrow" }
      ],
      "updated": 1,
      "link": null,
      "locked": false
    },
    {
      "id": "text_process",
      "type": "text",
      "x": 295,
      "y": 65,
      "width": 90,
      "height": 25,
      "text": "Process",
      "fontSize": 20,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "rect_process",
      "originalText": "Process",
      "autoResize": true,
      "lineHeight": 1.25,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 201,
      "version": 1,
      "versionNonce": 1,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1,
      "link": null,
      "locked": false
    },
    {
      "id": "rect_end",
      "type": "ellipse",
      "x": 490,
      "y": 50,
      "width": 120,
      "height": 60,
      "strokeColor": "#22c55e",
      "backgroundColor": "#b2f2bb",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 300,
      "version": 1,
      "versionNonce": 1,
      "isDeleted": false,
      "boundElements": [
        { "id": "text_end", "type": "text" },
        { "id": "arrow_2", "type": "arrow" }
      ],
      "updated": 1,
      "link": null,
      "locked": false
    },
    {
      "id": "text_end",
      "type": "text",
      "x": 520,
      "y": 65,
      "width": 60,
      "height": 25,
      "text": "Done",
      "fontSize": 20,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "rect_end",
      "originalText": "Done",
      "autoResize": true,
      "lineHeight": 1.25,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 301,
      "version": 1,
      "versionNonce": 1,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1,
      "link": null,
      "locked": false
    },
    {
      "id": "arrow_1",
      "type": "arrow",
      "x": 195,
      "y": 80,
      "width": 70,
      "height": 0,
      "points": [[0, 0], [70, 0]],
      "startBinding": { "elementId": "rect_start", "focus": 0, "gap": 5, "fixedPoint": null },
      "endBinding": { "elementId": "rect_process", "focus": 0, "gap": 5, "fixedPoint": null },
      "startArrowhead": null,
      "endArrowhead": "arrow",
      "strokeColor": "#ced4da",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "groupIds": [],
      "frameId": null,
      "roundness": { "type": 2 },
      "seed": 400,
      "version": 1,
      "versionNonce": 1,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1,
      "link": null,
      "locked": false
    },
    {
      "id": "arrow_2",
      "type": "arrow",
      "x": 415,
      "y": 80,
      "width": 70,
      "height": 0,
      "points": [[0, 0], [70, 0]],
      "startBinding": { "elementId": "rect_process", "focus": 0, "gap": 5, "fixedPoint": null },
      "endBinding": { "elementId": "rect_end", "focus": 0, "gap": 5, "fixedPoint": null },
      "startArrowhead": null,
      "endArrowhead": "arrow",
      "strokeColor": "#ced4da",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "groupIds": [],
      "frameId": null,
      "roundness": { "type": 2 },
      "seed": 401,
      "version": 1,
      "versionNonce": 1,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1,
      "link": null,
      "locked": false
    }
  ],
  "appState": {
    "viewBackgroundColor": "#1e1e2e",
    "gridSize": null
  },
  "files": {}
}
```
