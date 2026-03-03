# Excalidraw JSON Schema Reference

## Top-Level File Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "viewBackgroundColor": "#1e1e2e",
    "gridSize": null
  },
  "files": {}
}
```

## Universal Element Properties

Every element requires:

```json
{
  "id": "unique-string",
  "type": "rectangle|ellipse|diamond|text|arrow|line|freedraw",
  "x": 0,
  "y": 0,
  "width": 100,
  "height": 50,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": 12345,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

### Property Values

| Property | Values |
|---|---|
| `fillStyle` | `"solid"`, `"hachure"`, `"cross-hatch"` |
| `strokeStyle` | `"solid"`, `"dashed"`, `"dotted"` |
| `roughness` | `0` (architect/clean), `1` (artist/sketchy), `2` (cartoonist/very rough) |
| `roundness` | `null` (sharp), `{ "type": 3 }` (rounded corners for shapes), `{ "type": 2 }` (for lines/arrows) |
| `strokeWidth` | `1` (thin), `2` (normal), `4` (thick) |

## Element Types

### Rectangle
```json
{
  "type": "rectangle",
  "roundness": { "type": 3 },
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid"
}
```

### Ellipse
```json
{
  "type": "ellipse",
  "backgroundColor": "#b2f2bb",
  "fillStyle": "solid"
}
```

### Diamond
```json
{
  "type": "diamond",
  "backgroundColor": "#ffd8a8",
  "fillStyle": "solid"
}
```

### Text
```json
{
  "type": "text",
  "text": "Hello World",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "Hello World",
  "autoResize": true,
  "lineHeight": 1.25
}
```

**fontFamily values**: `1` = Virgil (hand-drawn), `2` = Helvetica, `3` = Cascadia (monospace), `5` = Excalifont (default hand-drawn)

**textAlign**: `"left"`, `"center"`, `"right"`

**verticalAlign**: `"top"`, `"middle"`

**Text centering**: To center text at position `(cx, cy)`, estimate `x = cx - (charCount * fontSize * 0.3)` and set `y` accordingly.

### Text Inside Shapes (Bound Text)

To put text inside a shape, create both elements and bind them:

Shape element:
```json
{
  "id": "shape1",
  "type": "rectangle",
  "boundElements": [{ "id": "text1", "type": "text" }]
}
```

Text element:
```json
{
  "id": "text1",
  "type": "text",
  "containerId": "shape1",
  "verticalAlign": "middle",
  "textAlign": "center"
}
```

The text's `x,y` should be inside the shape. Excalidraw auto-centers bound text.

### Arrow
```json
{
  "type": "arrow",
  "points": [[0, 0], [200, 0]],
  "startBinding": {
    "elementId": "source-shape-id",
    "focus": 0,
    "gap": 5,
    "fixedPoint": null
  },
  "endBinding": {
    "elementId": "target-shape-id",
    "focus": 0,
    "gap": 5,
    "fixedPoint": null
  },
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "roundness": { "type": 2 }
}
```

**Arrowhead values**: `null`, `"arrow"`, `"bar"`, `"dot"`, `"triangle"`

**Binding**: When an arrow is bound to shapes, also add the arrow to each shape's `boundElements`:
```json
{
  "id": "shape1",
  "boundElements": [{ "id": "arrow1", "type": "arrow" }]
}
```

**Points**: Array of `[dx, dy]` relative offsets from the arrow's `x,y` origin. First point is always `[0,0]`.

### Line
Same as arrow but `type: "line"` and typically no arrowheads.

## Color Palette

### Dark theme stroke colors
- White: `#ffffff`
- Light gray: `#ced4da`
- Blue: `#4a9eed` or `#a5d8ff`
- Green: `#22c55e` or `#b2f2bb`
- Red: `#ef4444` or `#ffc9c9`
- Amber: `#f59e0b` or `#ffd8a8`
- Purple: `#8b5cf6` or `#d0bfff`
- Pink: `#ec4899` or `#eebefa`
- Cyan: `#06b6d4`
- Teal: `#c3fae8`
- Yellow: `#fff3bf`

### Light fill colors (for backgrounds)
- `#a5d8ff` (blue), `#b2f2bb` (green), `#ffd8a8` (orange)
- `#d0bfff` (purple), `#ffc9c9` (red), `#fff3bf` (yellow)
- `#c3fae8` (teal), `#eebefa` (pink)

## Grouping Elements

To group elements, give them the same group ID in `groupIds`:
```json
{ "id": "el1", "groupIds": ["group1"] },
{ "id": "el2", "groupIds": ["group1"] }
```

## Z-Order

Elements render in array order: first element = back layer, last = front. Place backgrounds first, then shapes, then text, then arrows on top.

## ID Generation

Use short random strings: `"id": "rect_1"`, `"id": "arrow_a2b"`, etc. Each must be unique. Use `seed` with any random integer for consistent hand-drawn rendering.
