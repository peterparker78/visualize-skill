#!/usr/bin/env python3
"""
Render .excalidraw JSON files to PNG using Pillow.
Usage: python3 render_excalidraw.py <input.excalidraw> [output.png]

Requires: pip install Pillow
"""

import json
import math
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Installing Pillow...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"], check=True)
    from PIL import Image, ImageDraw, ImageFont


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def hex_to_rgba(hex_color: str, opacity: int = 100) -> tuple:
    """Convert hex color + opacity (0-100) to RGBA tuple."""
    r, g, b = hex_to_rgb(hex_color)
    a = int(opacity * 255 / 100)
    return (r, g, b, a)


def get_font(size: int, monospace: bool = False):
    """Try to load a good font, fall back to default."""
    font_paths = [
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/Library/Fonts/Arial.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    mono_paths = [
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/Library/Fonts/Courier New.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    paths = mono_paths if monospace else font_paths
    for fp in paths:
        try:
            return ImageFont.truetype(fp, size)
        except (OSError, IOError):
            continue
    # Fall back to default bitmap font
    try:
        return ImageFont.truetype("arial.ttf", size)
    except (OSError, IOError):
        return ImageFont.load_default()


def draw_dashed_line(draw, x1, y1, x2, y2, fill, width, dash_len=10, gap_len=6):
    """Draw a dashed line."""
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    pos = 0
    while pos < length:
        sx = x1 + ux * pos
        sy = y1 + uy * pos
        end = min(pos + dash_len, length)
        ex = x1 + ux * end
        ey = y1 + uy * end
        draw.line([(sx, sy), (ex, ey)], fill=fill, width=width)
        pos = end + gap_len


def draw_arrowhead(draw, x1, y1, x2, y2, fill, size=12):
    """Draw an arrowhead at (x2, y2) pointing from (x1, y1)."""
    angle = math.atan2(y2 - y1, x2 - x1)
    a1 = angle + math.pi * 0.85
    a2 = angle - math.pi * 0.85
    p1 = (x2 + size * math.cos(a1), y2 + size * math.sin(a1))
    p2 = (x2 + size * math.cos(a2), y2 + size * math.sin(a2))
    draw.polygon([(x2, y2), p1, p2], fill=fill)


def render(input_path: str, output_path: str = None):
    """Render .excalidraw to PNG using Pillow."""
    input_file = Path(input_path)
    if not input_file.exists():
        print(f"Error: {input_file} not found")
        sys.exit(1)

    if output_path is None:
        output_path = str(input_file.with_suffix(".png"))

    with open(input_file, "r") as f:
        scene_data = json.load(f)

    elements = scene_data.get("elements", [])
    app_state = scene_data.get("appState", {})
    bg_color = app_state.get("viewBackgroundColor", "#ffffff")

    if not elements:
        print("Error: No elements in file")
        sys.exit(1)

    # Calculate bounding box
    min_x = min(e["x"] for e in elements)
    min_y = min(e["y"] for e in elements)
    max_x = max(e["x"] + e.get("width", 0) for e in elements)
    max_y = max(e["y"] + e.get("height", 0) for e in elements)

    # Account for arrow points that extend beyond element bounds
    for el in elements:
        if el.get("type") in ("arrow", "line"):
            for pt in el.get("points", []):
                px = el["x"] + pt[0]
                py = el["y"] + pt[1]
                min_x = min(min_x, px)
                min_y = min(min_y, py)
                max_x = max(max_x, px)
                max_y = max(max_y, py)

    padding = 50
    scale = 2  # Retina-quality
    canvas_w = int((max_x - min_x + padding * 2) * scale)
    canvas_h = int((max_y - min_y + padding * 2) * scale)
    ox = (-min_x + padding) * scale
    oy = (-min_y + padding) * scale

    img = Image.new("RGBA", (canvas_w, canvas_h), hex_to_rgba(bg_color))
    draw = ImageDraw.Draw(img)

    # Separate elements by type for z-order: shapes first, then text, then arrows
    shapes = [e for e in elements if e.get("type") in ("rectangle", "ellipse", "diamond")]
    texts = [e for e in elements if e.get("type") == "text"]
    arrows = [e for e in elements if e.get("type") in ("arrow", "line")]

    # Draw shapes
    for el in shapes:
        x = el["x"] * scale + ox
        y = el["y"] * scale + oy
        w = el.get("width", 0) * scale
        h = el.get("height", 0) * scale
        stroke = el.get("strokeColor", "#1e1e1e")
        bg = el.get("backgroundColor", "transparent")
        sw = el.get("strokeWidth", 2) * scale
        opacity = el.get("opacity", 100)
        t = el["type"]

        fill_color = hex_to_rgba(bg, opacity) if bg != "transparent" else None
        stroke_color = hex_to_rgba(stroke, opacity)

        if t == "rectangle":
            r = int(12 * scale) if el.get("roundness") else 0
            if fill_color:
                draw.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill_color)
            draw.rounded_rectangle([x, y, x + w, y + h], radius=r, outline=stroke_color, width=int(sw))
        elif t == "ellipse":
            if fill_color:
                draw.ellipse([x, y, x + w, y + h], fill=fill_color)
            draw.ellipse([x, y, x + w, y + h], outline=stroke_color, width=int(sw))
        elif t == "diamond":
            cx, cy = x + w / 2, y + h / 2
            pts = [(cx, y), (x + w, cy), (cx, y + h), (x, cy)]
            if fill_color:
                draw.polygon(pts, fill=fill_color)
            draw.polygon(pts, outline=stroke_color)
            # Redraw outline with proper width
            for i in range(len(pts)):
                p1 = pts[i]
                p2 = pts[(i + 1) % len(pts)]
                draw.line([p1, p2], fill=stroke_color, width=int(sw))

    # Draw arrows/lines
    for el in arrows:
        x = el["x"] * scale + ox
        y = el["y"] * scale + oy
        stroke = el.get("strokeColor", "#ced4da")
        sw = max(el.get("strokeWidth", 2) * scale, 2)
        opacity = el.get("opacity", 100)
        points = el.get("points", [])
        style = el.get("strokeStyle", "solid")

        if len(points) < 2:
            continue

        stroke_color = hex_to_rgba(stroke, opacity)

        for i in range(len(points) - 1):
            x1 = x + points[i][0] * scale
            y1 = y + points[i][1] * scale
            x2 = x + points[i + 1][0] * scale
            y2 = y + points[i + 1][1] * scale

            if style == "dashed":
                draw_dashed_line(draw, x1, y1, x2, y2, stroke_color, int(sw),
                                 dash_len=int(14 * scale), gap_len=int(8 * scale))
            elif style == "dotted":
                draw_dashed_line(draw, x1, y1, x2, y2, stroke_color, int(sw),
                                 dash_len=int(4 * scale), gap_len=int(6 * scale))
            else:
                draw.line([(x1, y1), (x2, y2)], fill=stroke_color, width=int(sw))

        # Draw arrowhead
        if el.get("type") == "arrow" and el.get("endArrowhead", "arrow"):
            last = points[-1]
            prev = points[-2]
            ax2 = x + last[0] * scale
            ay2 = y + last[1] * scale
            ax1 = x + prev[0] * scale
            ay1 = y + prev[1] * scale
            draw_arrowhead(draw, ax1, ay1, ax2, ay2, stroke_color, size=int(14 * scale))

    # Draw text
    for el in texts:
        text = el.get("text", "")
        if not text:
            continue
        x = el["x"] * scale + ox
        y = el["y"] * scale + oy
        fs = int(el.get("fontSize", 20) * scale)
        stroke = el.get("strokeColor", "#1e1e1e")
        opacity = el.get("opacity", 100)
        align = el.get("textAlign", "left")
        color = hex_to_rgba(stroke, opacity)
        font_family = el.get("fontFamily", 1)
        monospace = font_family == 3

        font = get_font(fs, monospace=monospace)

        lines = text.split("\n")
        line_height = fs * 1.3
        w = el.get("width", 0) * scale

        for i, line in enumerate(lines):
            ly = y + i * line_height

            # Calculate text width for alignment
            bbox = font.getbbox(line)
            tw = bbox[2] - bbox[0]

            if align == "center" and w > 0:
                tx = x + (w - tw) / 2
            elif align == "right" and w > 0:
                tx = x + w - tw
            else:
                tx = x

            # For bound text (containerId), center vertically in parent
            if el.get("containerId"):
                # Find parent element to get its dimensions
                parent_id = el["containerId"]
                parent = next((e for e in elements if e.get("id") == parent_id), None)
                if parent:
                    px = parent["x"] * scale + ox
                    py = parent["y"] * scale + oy
                    pw = parent.get("width", 0) * scale
                    ph = parent.get("height", 0) * scale
                    total_text_h = len(lines) * line_height
                    tx = px + (pw - tw) / 2
                    ly = py + (ph - total_text_h) / 2 + i * line_height

            draw.text((tx, ly), line, fill=color, font=font)

    # Save
    img.save(output_path, "PNG")
    print(f"Rendered: {output_path} ({canvas_w}x{canvas_h}px)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 render_excalidraw.py <input.excalidraw> [output.png]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    render(input_path, output_path)
