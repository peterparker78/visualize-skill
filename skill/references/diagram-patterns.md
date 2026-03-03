# Diagram Pattern Library

## Table of Contents
- [Flowchart Patterns](#flowchart-patterns)
- [Mind Map Patterns](#mind-map-patterns)
- [Learning Diagrams](#learning-diagrams)
- [Layout Rules](#layout-rules)
- [Complete Example](#complete-example)

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
| Parallelogram | Input/Output (use diamond rotated) | diamond |

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
1. Place central node at (400, 300) with larger size (200x80)
2. Calculate N branch positions evenly around a circle (radius 250-350px)
3. For each branch, place sub-branches further out (radius +200px)
4. Connect with curved arrows or lines

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
Assign each primary branch a distinct color family:
- Branch 1: Blue family (#4a9eed stroke, #a5d8ff fill)
- Branch 2: Green family (#22c55e stroke, #b2f2bb fill)
- Branch 3: Amber family (#f59e0b stroke, #ffd8a8 fill)
- Branch 4: Purple family (#8b5cf6 stroke, #d0bfff fill)
- Branch 5: Red family (#ef4444 stroke, #ffc9c9 fill)
- Branch 6: Teal family (#06b6d4 stroke, #c3fae8 fill)

Sub-nodes inherit their parent branch color.

## Learning Diagrams

### Concept Comparison (VS diagram)
```
[Concept A]          VS          [Concept B]
- Feature 1                      - Feature 1
- Feature 2                      - Feature 2
- Feature 3                      - Feature 3
```
Place two groups side by side with a "VS" text element between them.

### Process Explanation
Show a concept's mechanism step by step:
```
[Input] -> (Transform) -> [Intermediate] -> (Transform) -> [Output]
```
Use different shapes for different roles in the process.

### Hierarchy/Taxonomy
```
         [Parent Concept]
        /        |        \
[Type A]    [Type B]    [Type C]
   |            |
[Sub-A1]   [Sub-B1]
```

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
Horizontal layout with time annotations below.

### Cycle Diagram
```
[Stage 1] --> [Stage 2]
    ^              |
    |              v
[Stage 4] <-- [Stage 3]
```

## Layout Rules

### Spacing
- Minimum 60px between shapes horizontally
- Minimum 50px between shapes vertically
- Arrow gap from shapes: 5-8px
- Canvas padding: 40px on all sides

### Alignment
- Align related shapes on the same Y coordinate for horizontal flows
- Align related shapes on the same X coordinate for vertical flows
- Center text labels below or inside shapes

### Sizing
- Standard shape: 140x60px (rectangle), 80x80px (diamond/ellipse)
- Title text: fontSize 28-32
- Label text: fontSize 16-20
- Annotation text: fontSize 14-16
- Central/important nodes: 1.5x standard size

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
