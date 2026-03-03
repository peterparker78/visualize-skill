# Color Palette Reference

Semantic color system — every color has a purpose. To brand-customize, edit only this file.

## Shape Colors (stroke / fill pairs)

| Role | Stroke | Fill | Use for |
|------|--------|------|---------|
| Primary | `#4a9eed` | `#a5d8ff` | Main flow, core concepts, default shapes |
| Success | `#22c55e` | `#b2f2bb` | Completion, output, end states, results |
| Processing | `#f59e0b` | `#ffd8a8` | Transforms, in-progress, warnings |
| Error | `#ef4444` | `#ffc9c9` | Failures, critical paths, blockers |
| Decision | `#8b5cf6` | `#d0bfff` | Branch points, logic, conditionals |
| Data/Input | `#06b6d4` | `#c3fae8` | External data, inputs, APIs, systems |
| Highlight | `#ec4899` | `#eebefa` | Emphasis, callouts, annotations |
| Neutral | `#868e96` | `#e9ecef` | Backgrounds, disabled, secondary |

## Text Colors

| Context | Color | Use for |
|---------|-------|---------|
| Dark theme text | `#ffffff` | All text on dark backgrounds |
| On light fills | `#1e1e1e` | Text inside filled shapes |
| Annotations | `#ced4da` | Subtitles, labels, secondary info |
| Muted | `#868e96` | Legend text, optional info |

## Arrow/Line Colors

| Context | Color |
|---------|-------|
| Default arrows | `#ced4da` |
| Branch-colored lines | Match parent shape stroke color |
| Hub-to-branch connections | Match branch stroke at 60% opacity |

## Background Colors

| Theme | Color |
|-------|-------|
| Dark (default) | `#1e1e2e` |
| Light | `#ffffff` |

## Mind Map Branch Assignment

Assign in order for up to 6 branches:
1. Blue: `#4a9eed` / `#a5d8ff`
2. Purple: `#8b5cf6` / `#d0bfff`
3. Teal: `#06b6d4` / `#c3fae8`
4. Amber: `#f59e0b` / `#ffd8a8`
5. Green: `#22c55e` / `#b2f2bb`
6. Red: `#ef4444` / `#ffc9c9`

Sub-nodes inherit parent branch stroke color with transparent fill.

## Evidence Artifact Colors

For code snippets, JSON payloads, or technical detail blocks:

| Element | Color |
|---------|-------|
| Background fill | `#1e293b` (dark slate) |
| Stroke | `#334155` |
| Code text | `#22c55e` (green monospace) |
| JSON keys | `#4a9eed` (blue) |
| Values | `#f59e0b` (amber) |
