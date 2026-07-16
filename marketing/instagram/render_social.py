#!/usr/bin/env python3
"""Render Haunt's reusable Instagram launch kit from content.json."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
MARKETING = ROOT.parent
SOURCE = MARKETING / "source"
SCREENSHOTS = MARKETING / "screenshots" / "iphone-6.9"
EXPORTS = ROOT / "exports"
POSTS = EXPORTS / "posts"
HIGHLIGHTS = EXPORTS / "highlights"
STORIES = EXPORTS / "stories"

W = 1080
H = 1080
STORY_H = 1920

# Keep these in sync with the canonical brand tokens in public/index.html.
INK = "#0A0A0F"
INK_2 = "#13131A"
ELEVATED = "#1C1C28"
BORDER = "#2A2A38"
AMBER = "#E8A847"
CREAM = "#E8E6E1"
MUTED = "#8A8A96"
GREEN = "#43D17B"


def font(size: int, serif: bool = False, bold: bool = False) -> ImageFont.FreeTypeFont:
    if serif:
        candidates = [
            ("/System/Library/Fonts/Supplemental/Georgia Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Georgia.ttf", 0),
            ("/System/Library/Fonts/NewYork.ttf", 0),
        ]
    else:
        # Avenir Next is a TTC. Index 2 is Demi Bold and index 7 is Regular.
        # Loading the default face (index 0) silently makes every label Bold.
        candidates = [
            ("/System/Library/Fonts/Avenir Next.ttc", 2 if bold else 7),
            ("/Library/Fonts/Montserrat-SemiBold.ttf" if bold else "/Library/Fonts/Montserrat-Regular.ttf", 0),
            ("/System/Library/Fonts/Helvetica.ttc", 0),
        ]
    for candidate, index in candidates:
        try:
            return ImageFont.truetype(candidate, size=size, index=index)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, start_size: int, *, serif=False, bold=False):
    size = start_size
    while size > 18:
        selected = font(size, serif=serif, bold=bold)
        if draw.textbbox((0, 0), text, font=selected)[2] <= max_width:
            return selected
        size -= 2
    return font(size, serif=serif, bold=bold)


def rounded_screen(path: Path, width: int, height: int, radius: int = 42) -> Image.Image:
    source = Image.open(path).convert("RGB")
    source.thumbnail((width, height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    x = (width - source.width) // 2
    y = (height - source.height) // 2
    canvas.alpha_composite(source.convert("RGBA"), (x, y))
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius=radius, fill=255)
    canvas.putalpha(mask)
    return canvas


def brand_mark(width: int, color: str = AMBER) -> Image.Image:
    """Extract and recolor the exact production ghost mark from the app icon."""
    source = Image.open(SOURCE / "AppIcon-1024.png").convert("RGB")
    background = Image.new("RGB", source.size, source.getpixel((0, 0)))
    difference = ImageChops.difference(source, background).convert("L")
    mask = difference.point(lambda value: max(0, min(255, (value - 2) * 3)))
    bounds = mask.getbbox()
    if bounds is None:
        raise RuntimeError("Could not extract the Haunt mark from AppIcon-1024.png")
    mask = mask.crop(bounds)
    height = round(width * mask.height / mask.width)
    mask = mask.resize((width, height), Image.Resampling.LANCZOS)
    mark = Image.new("RGBA", (width, height), color)
    mark.putalpha(mask)
    return mark


def place_brand_mark(image: Image.Image, box: tuple[int, int, int, int], color: str = AMBER) -> None:
    """Center the exact mark in a layout box without distorting its proportions."""
    x0, y0, x1, y1 = box
    max_width = x1 - x0
    max_height = y1 - y0
    mark = brand_mark(max_width, color)
    if mark.height > max_height:
        target_width = round(max_width * max_height / mark.height)
        mark = brand_mark(target_width, color)
    x = x0 + (max_width - mark.width) // 2
    y = y0 + (max_height - mark.height) // 2
    image.paste(mark, (x, y), mark)


def render_profile(inverted: bool = False) -> Image.Image:
    """Create a circle-safe Instagram avatar using only the production mark."""
    background = AMBER if inverted else INK
    mark_color = INK if inverted else AMBER
    image = Image.new("RGB", (W, H), background)
    draw = ImageDraw.Draw(image)
    if not inverted:
        draw.ellipse((54, 54, W - 54, H - 54), fill=INK_2, outline=AMBER, width=20)
    place_brand_mark(image, (245, 155, 835, 925), mark_color)
    return image


def eyebrow(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], color=AMBER) -> None:
    draw.text(xy, text.upper(), fill=color, font=font(25, bold=True))


def card(draw: ImageDraw.ImageDraw, box, title, detail=None):
    draw.rounded_rectangle(box, radius=26, fill=INK_2, outline=BORDER, width=2)
    x0, y0, x1, _ = box
    draw.text((x0 + 28, y0 + 22), title, fill=CREAM, font=font(34, bold=True))
    if detail:
        draw.text((x0 + 28, y0 + 70), detail, fill=MUTED, font=font(22))


def render_launch(copy: dict) -> Image.Image:
    image = Image.new("RGB", (W, H), INK)
    draw = ImageDraw.Draw(image)

    # Warm atmospheric glow without inventing a fake place or venue.
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((-330, 90, 780, 1200), fill=(238, 173, 66, 44))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    image = Image.alpha_composite(image.convert("RGBA"), glow)
    draw = ImageDraw.Draw(image)

    eyebrow(draw, copy["launch"]["eyebrow"], (70, 64))
    draw.multiline_text((65, 115), copy["launch"]["headline"], fill=CREAM, font=font(106, serif=True, bold=True), spacing=2)
    draw.text((72, 405), copy["launch"]["subhead"], fill=AMBER, font=fit_text(draw, copy["launch"]["subhead"], 465, 34, bold=True))

    icon = Image.open(SOURCE / "AppIcon-1024.png").convert("RGB").resize((92, 92), Image.Resampling.LANCZOS)
    image.alpha_composite(icon.convert("RGBA"), (70, 528))
    draw = ImageDraw.Draw(image)
    draw.text((184, 540), "SELF-GUIDED\nGPS GHOST TOURS", fill=CREAM, font=font(24, bold=True), spacing=4)

    screen = rounded_screen(SCREENSHOTS / "03-active-tour-narration.png", 430, 930, radius=48)
    shadow = Image.new("RGBA", (470, 970), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((20, 20, 450, 950), radius=52, fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    image.alpha_composite(shadow, (590, 122))
    image.alpha_composite(screen, (610, 105))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((607, 102, 1043, 1040), radius=54, outline=AMBER, width=3)

    draw.text((72, 690), copy["launch"]["body"], fill=CREAM, font=font(36, serif=True), spacing=9)
    draw.rounded_rectangle((70, 938, 488, 1007), radius=34, fill=AMBER)
    draw.text((103, 954), copy["launch"]["cta"], fill=INK, font=font(27, bold=True))
    return image.convert("RGB")


def render_cities(copy: dict) -> Image.Image:
    image = Image.new("RGB", (W, H), AMBER)
    draw = ImageDraw.Draw(image)
    eyebrow(draw, copy["cities"]["eyebrow"], (72, 64), color=INK)
    draw.text((62, 108), copy["cities"]["headline"], fill=INK, font=font(106, serif=True, bold=True))
    place_brand_mark(image, (850, 55, 1000, 230), INK)
    draw.line((72, 275, 1008, 275), fill=INK, width=3)

    cities = copy["cities"]["items"]
    columns = [cities[:6], cities[6:]]
    for col, values in enumerate(columns):
        x = 74 + col * 505
        for row, city in enumerate(values):
            y = 325 + row * 94
            draw.ellipse((x, y + 18, x + 16, y + 34), fill=INK)
            draw.text((x + 36, y), city, fill=INK, font=fit_text(draw, city, 420, 42, serif=True))

    draw.line((72, 908, 1008, 908), fill=INK, width=3)
    draw.text((72, 942), copy["cities"]["footer"], fill=INK, font=font(31, bold=True))
    return image


def render_trust(copy: dict) -> Image.Image:
    image = Image.new("RGB", (W, H), INK)
    draw = ImageDraw.Draw(image)
    eyebrow(draw, copy["trust"]["eyebrow"], (70, 62))
    draw.multiline_text((65, 112), copy["trust"]["headline"], fill=CREAM, font=font(92, serif=True, bold=True), spacing=2)
    place_brand_mark(image, (845, 55, 998, 235), AMBER)

    y = 395
    for item in copy["trust"]["items"]:
        detail = item.get("detail")
        height = 112 if detail else 90
        card(draw, (70, y, 1010, y + height), item["title"], detail)
        y += height + 22

    draw.rounded_rectangle((70, 871, 1010, 1008), radius=28, fill=AMBER)
    draw.text((103, 897), copy["trust"]["safety_title"], fill=INK, font=font(28, bold=True))
    safety_font = fit_text(draw, copy["trust"]["safety_body"], 874, 24)
    draw.text((103, 950), copy["trust"]["safety_body"], fill=INK, font=safety_font)
    return image


def render_highlight(label: str, glyph: str) -> Image.Image:
    image = Image.new("RGB", (W, STORY_H), INK)
    draw = ImageDraw.Draw(image)
    center_y = STORY_H // 2
    draw.ellipse((240, center_y - 300, 840, center_y + 300), fill=AMBER)
    place_brand_mark(image, (410, center_y - 200, 670, center_y + 90), INK)
    selected = fit_text(draw, glyph, 490, 54, bold=True)
    glyph_box = draw.textbbox((0, 0), glyph, font=selected)
    draw.text(((W - (glyph_box[2] - glyph_box[0])) // 2, center_y + 135), glyph, fill=INK, font=selected)
    draw.text((50, STORY_H - 90), f"HAUNT • {label.upper()}", fill=ELEVATED, font=font(19, bold=True))
    return image


def render_story(copy: dict) -> Image.Image:
    image = Image.new("RGB", (W, STORY_H), INK)
    draw = ImageDraw.Draw(image)
    eyebrow(draw, copy["launch"]["eyebrow"], (72, 105))
    draw.multiline_text((65, 170), copy["launch"]["headline"], fill=CREAM, font=font(132, serif=True, bold=True), spacing=4)
    draw.text((72, 530), copy["launch"]["subhead"], fill=AMBER, font=fit_text(draw, copy["launch"]["subhead"], 900, 44, bold=True))
    screen = rounded_screen(SCREENSHOTS / "03-active-tour-narration.png", 575, 1248, radius=64)
    image.paste(screen, (445, 640), screen)
    draw = ImageDraw.Draw(image)
    draw.multiline_text((72, 760), copy["launch"]["body"], fill=CREAM, font=font(55, serif=True), spacing=12)
    draw.rounded_rectangle((70, 1575, 430, 1658), radius=41, fill=AMBER)
    draw.text((111, 1596), copy["launch"]["cta"], fill=INK, font=font(31, bold=True))
    draw.text((72, 1730), "@hauntghosttours", fill=MUTED, font=font(28, bold=True))
    return image


def main() -> None:
    copy = json.loads((ROOT / "content.json").read_text())
    POSTS.mkdir(parents=True, exist_ok=True)
    HIGHLIGHTS.mkdir(parents=True, exist_ok=True)
    STORIES.mkdir(parents=True, exist_ok=True)

    render_profile().save(EXPORTS / "profile-photo-primary.png", quality=95)
    render_profile(inverted=True).save(EXPORTS / "profile-photo-inverted.png", quality=95)

    launch = render_launch(copy)
    cities = render_cities(copy)
    trust = render_trust(copy)
    launch.save(POSTS / "01-launch-how-it-works.png", quality=95)
    cities.save(POSTS / "02-twelve-cities.png", quality=95)
    trust.save(POSTS / "03-trust-privacy.png", quality=95)

    preview = Image.new("RGB", (W * 3 + 16, H), "white")
    preview.paste(launch, (0, 0))
    preview.paste(cities, (W + 8, 0))
    preview.paste(trust, (W * 2 + 16, 0))
    preview.save(EXPORTS / "grid-preview.png", quality=94)

    for item in copy["highlights"]:
        render_highlight(item["label"], item["glyph"]).save(HIGHLIGHTS / item["filename"], quality=95)

    render_story(copy).save(STORIES / "launch-story.png", quality=95)
    print("Rendered 2 profile photos, 3 posts, 4 highlight covers, launch story, and grid preview.")


if __name__ == "__main__":
    main()
