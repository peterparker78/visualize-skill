#!/usr/bin/env python3
"""
Validate .excalidraw layout for overlapping elements and line-through-box collisions.
Usage: python3 validate_layout.py <input.excalidraw> [--fix] [--min-gap 20]

Returns exit code 0 if valid, 1 if issues found.
With --fix, writes a corrected version to <input>_fixed.excalidraw.

Requires: pip install Pillow (only for font metrics, optional)
"""

import json
import math
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def rect_of(el):
    """Return (x, y, w, h) bounding box for a shape element."""
    return (el["x"], el["y"], el.get("width", 0), el.get("height", 0))


def boxes_overlap(a, b, min_gap=20):
    """Check if two axis-aligned boxes overlap or are closer than min_gap."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    # Expand each box by min_gap/2 on all sides, then check intersection
    g = min_gap / 2
    a_left, a_right = ax - g, ax + aw + g
    a_top, a_bottom = ay - g, ay + ah + g
    b_left, b_right = bx - g, bx + bw + g
    b_top, b_bottom = by - g, by + bh + g

    if a_right <= b_left or b_right <= a_left:
        return False
    if a_bottom <= b_top or b_bottom <= a_top:
        return False
    return True


def overlap_depth(a, b):
    """Return (dx_overlap, dy_overlap) — how much boxes overlap."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b

    ox = min(ax + aw, bx + bw) - max(ax, bx)
    oy = min(ay + ah, by + bh) - max(ay, by)
    return (max(0, ox), max(0, oy))


def center_of(box):
    x, y, w, h = box
    return (x + w / 2, y + h / 2)


def segment_intersects_box(p1, p2, box, margin=5):
    """Check if line segment (p1→p2) passes through a box (with margin).
    Uses Liang-Barsky algorithm."""
    x, y, w, h = box
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1

    # Box edges with margin
    left = x - margin
    right = x + w + margin
    top = y - margin
    bottom = y + h + margin

    p = [-dx, dx, -dy, dy]
    q = [x1 - left, right - x1, y1 - top, bottom - y1]

    t_enter = 0.0
    t_exit = 1.0

    for i in range(4):
        if abs(p[i]) < 1e-10:
            if q[i] < 0:
                return False
        else:
            t = q[i] / p[i]
            if p[i] < 0:
                t_enter = max(t_enter, t)
            else:
                t_exit = min(t_exit, t)

    if t_enter > t_exit:
        return False

    # Exclude cases where the line only clips the very start/end (bound shapes)
    if t_enter < 0.05 or t_exit > 0.95:
        # The line touches near endpoints — likely a proper connection
        if t_enter < 0.05 and t_exit > 0.95:
            return True  # passes clean through
        return False
    return True


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(excalidraw_data, min_gap=20):
    """Validate layout, return list of issues."""
    elements = excalidraw_data.get("elements", [])
    issues = []

    # Separate by type
    shapes = [e for e in elements
              if e.get("type") in ("rectangle", "ellipse", "diamond")
              and not e.get("isDeleted")]
    texts = [e for e in elements
             if e.get("type") == "text"
             and not e.get("containerId")  # skip bound text
             and not e.get("isDeleted")]
    arrows = [e for e in elements
              if e.get("type") in ("arrow", "line")
              and not e.get("isDeleted")]

    # Build ID→element lookup
    by_id = {e["id"]: e for e in elements}

    # 1. Check shape-shape overlaps
    for i in range(len(shapes)):
        for j in range(i + 1, len(shapes)):
            a, b = shapes[i], shapes[j]
            box_a = rect_of(a)
            box_b = rect_of(b)
            if boxes_overlap(box_a, box_b, min_gap):
                dx, dy = overlap_depth(box_a, box_b)
                issues.append({
                    "type": "shape_overlap",
                    "severity": "error" if dx > 0 and dy > 0 else "warning",
                    "elements": [a["id"], b["id"]],
                    "message": f"Shapes '{a['id']}' and '{b['id']}' overlap or are too close "
                               f"(gap < {min_gap}px, overlap: {dx:.0f}x{dy:.0f})",
                    "boxes": [box_a, box_b]
                })

    # 2. Check free text overlapping shapes
    for t in texts:
        t_box = rect_of(t)
        for s in shapes:
            s_box = rect_of(s)
            if boxes_overlap(t_box, s_box, min_gap=10):
                issues.append({
                    "type": "text_shape_overlap",
                    "severity": "warning",
                    "elements": [t["id"], s["id"]],
                    "message": f"Free text '{t['id']}' overlaps shape '{s['id']}'"
                })

    # 3. Check arrows/lines passing through unrelated shapes
    for arrow in arrows:
        points = arrow.get("points", [])
        if len(points) < 2:
            continue

        # Identify connected shapes (start/end bindings)
        connected_ids = set()
        sb = arrow.get("startBinding")
        eb = arrow.get("endBinding")
        if sb:
            connected_ids.add(sb.get("elementId"))
        if eb:
            connected_ids.add(eb.get("elementId"))

        ax, ay = arrow["x"], arrow["y"]
        segments = []
        for k in range(len(points) - 1):
            p1 = (ax + points[k][0], ay + points[k][1])
            p2 = (ax + points[k + 1][0], ay + points[k + 1][1])
            segments.append((p1, p2))

        for shape in shapes:
            if shape["id"] in connected_ids:
                continue
            s_box = rect_of(shape)
            for p1, p2 in segments:
                if segment_intersects_box(p1, p2, s_box, margin=3):
                    issues.append({
                        "type": "line_through_shape",
                        "severity": "error",
                        "elements": [arrow["id"], shape["id"]],
                        "message": f"Arrow '{arrow['id']}' passes through shape '{shape['id']}'"
                    })
                    break  # one report per arrow-shape pair

    # 4. Check arrow-arrow overlaps (close parallel lines)
    for i in range(len(arrows)):
        for j in range(i + 1, len(arrows)):
            a_pts = arrows[i].get("points", [])
            b_pts = arrows[j].get("points", [])
            if len(a_pts) < 2 or len(b_pts) < 2:
                continue
            # Compare midpoints of first segment
            ax_o, ay_o = arrows[i]["x"], arrows[i]["y"]
            bx_o, by_o = arrows[j]["x"], arrows[j]["y"]
            a_mid = (ax_o + (a_pts[0][0] + a_pts[-1][0]) / 2,
                     ay_o + (a_pts[0][1] + a_pts[-1][1]) / 2)
            b_mid = (bx_o + (b_pts[0][0] + b_pts[-1][0]) / 2,
                     by_o + (b_pts[0][1] + b_pts[-1][1]) / 2)
            dist = math.sqrt((a_mid[0] - b_mid[0]) ** 2 + (a_mid[1] - b_mid[1]) ** 2)
            if dist < 8:
                issues.append({
                    "type": "overlapping_lines",
                    "severity": "warning",
                    "elements": [arrows[i]["id"], arrows[j]["id"]],
                    "message": f"Arrows '{arrows[i]['id']}' and '{arrows[j]['id']}' overlap "
                               f"(midpoint distance: {dist:.1f}px)"
                })

    return issues


# ---------------------------------------------------------------------------
# Auto-fix: spread overlapping shapes apart
# ---------------------------------------------------------------------------

def fix_overlaps(excalidraw_data, min_gap=20, max_iterations=50):
    """Iteratively push overlapping shapes apart. Returns (fixed_data, changes_made)."""
    import copy
    data = copy.deepcopy(excalidraw_data)
    elements = data.get("elements", [])

    shapes = [e for e in elements
              if e.get("type") in ("rectangle", "ellipse", "diamond")
              and not e.get("isDeleted")]
    by_id = {e["id"]: e for e in elements}

    # Build parent→children map (for bound text)
    bound_texts = [e for e in elements if e.get("type") == "text" and e.get("containerId")]
    parent_children = {}
    for t in bound_texts:
        pid = t["containerId"]
        parent_children.setdefault(pid, []).append(t)

    # Build branch group maps (shapes in the same group should move together)
    group_shapes = {}
    for s in shapes:
        for gid in s.get("groupIds", []):
            group_shapes.setdefault(gid, []).append(s)

    changes = 0
    for iteration in range(max_iterations):
        moved = False
        for i in range(len(shapes)):
            for j in range(i + 1, len(shapes)):
                a, b = shapes[i], shapes[j]
                box_a = rect_of(a)
                box_b = rect_of(b)
                if not boxes_overlap(box_a, box_b, min_gap):
                    continue

                # Calculate push vector
                ca = center_of(box_a)
                cb = center_of(box_b)
                dx = cb[0] - ca[0]
                dy = cb[1] - ca[1]
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < 1:
                    dx, dy = 1, 0
                    dist = 1

                # How much overlap to resolve
                ox, oy = overlap_depth(box_a, box_b)
                push = max(ox, oy, min_gap) / 2 + min_gap / 2

                # Normalize and apply
                nx, ny = dx / dist, dy / dist
                move_x = nx * push
                move_y = ny * push

                # Move b away from a (and its bound text)
                _move_element(b, move_x, move_y, parent_children)
                # Move a in opposite direction
                _move_element(a, -move_x, -move_y, parent_children)

                moved = True
                changes += 1

        if not moved:
            break

    # Also fix arrow waypoints that pass through shapes
    arrows = [e for e in elements if e.get("type") in ("arrow", "line") and not e.get("isDeleted")]
    for arrow in arrows:
        connected_ids = set()
        sb = arrow.get("startBinding")
        eb = arrow.get("endBinding")
        if sb:
            connected_ids.add(sb.get("elementId"))
        if eb:
            connected_ids.add(eb.get("elementId"))

        points = arrow.get("points", [])
        if len(points) < 2:
            continue

        ax, ay = arrow["x"], arrow["y"]
        for shape in shapes:
            if shape["id"] in connected_ids:
                continue
            s_box = rect_of(shape)
            for k in range(len(points) - 1):
                p1 = (ax + points[k][0], ay + points[k][1])
                p2 = (ax + points[k + 1][0], ay + points[k + 1][1])
                if segment_intersects_box(p1, p2, s_box, margin=3):
                    # Add a waypoint to route around the shape
                    sc = center_of(s_box)
                    mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
                    # Push waypoint perpendicular to the line, away from shape center
                    ldx = p2[0] - p1[0]
                    ldy = p2[1] - p1[1]
                    length = math.sqrt(ldx * ldx + ldy * ldy)
                    if length < 1:
                        continue
                    # Perpendicular direction
                    perp_x = -ldy / length
                    perp_y = ldx / length
                    # Choose direction away from shape center
                    to_shape = (sc[0] - mid[0], sc[1] - mid[1])
                    dot = perp_x * to_shape[0] + perp_y * to_shape[1]
                    if dot > 0:
                        perp_x, perp_y = -perp_x, -perp_y

                    offset = max(s_box[2], s_box[3]) / 2 + min_gap
                    wp = [mid[0] + perp_x * offset - ax, mid[1] + perp_y * offset - ay]
                    points.insert(k + 1, wp)
                    changes += 1
                    break  # re-check from start

    return data, changes


def _move_element(el, dx, dy, parent_children):
    """Move an element and its bound text children."""
    el["x"] += dx
    el["y"] += dy
    for child in parent_children.get(el["id"], []):
        child["x"] += dx
        child["y"] += dy


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(issues):
    """Print a human-readable validation report."""
    if not issues:
        print("PASS: No layout issues found.")
        return

    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]

    print(f"FAIL: Found {len(errors)} error(s) and {len(warnings)} warning(s):\n")

    for i, issue in enumerate(issues, 1):
        icon = "ERROR" if issue["severity"] == "error" else "WARN"
        print(f"  [{icon}] {i}. {issue['message']}")

    print()
    if errors:
        print("Errors indicate elements that overlap or lines crossing through shapes.")
        print("Use --fix to auto-correct, or adjust positions manually in Excalidraw.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate Excalidraw layout")
    parser.add_argument("input", help="Path to .excalidraw file")
    parser.add_argument("--fix", action="store_true", help="Auto-fix overlaps")
    parser.add_argument("--min-gap", type=int, default=20, help="Minimum gap between shapes (px)")
    parser.add_argument("--output", "-o", help="Output path for fixed file")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)

    with open(input_path) as f:
        data = json.load(f)

    issues = validate(data, min_gap=args.min_gap)
    print_report(issues)

    if args.fix and issues:
        fixed_data, changes = fix_overlaps(data, min_gap=args.min_gap)
        out_path = args.output or str(input_path.with_suffix("")) + "_fixed.excalidraw"
        with open(out_path, "w") as f:
            json.dump(fixed_data, f, indent=2)
        print(f"\nFixed {changes} issues → {out_path}")

        # Re-validate
        remaining = validate(fixed_data, min_gap=args.min_gap)
        if remaining:
            print(f"Note: {len(remaining)} issue(s) remain after auto-fix (may need manual adjustment)")
        else:
            print("All issues resolved.")

    sys.exit(1 if any(i["severity"] == "error" for i in issues) else 0)


if __name__ == "__main__":
    main()
