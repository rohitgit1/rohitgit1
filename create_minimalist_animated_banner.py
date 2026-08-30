import math
import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1000
HEIGHT = 300
TOTAL_FRAMES = 40
OUTPUT_GIF = "rohit_minimalist_intro.gif"

try:
    title_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 52)
    sub_font = ImageFont.truetype("C:/Windows/Fonts/seguisb.ttf", 20)
    mono_font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
except Exception:
    title_font = ImageFont.load_default()
    sub_font = ImageFont.load_default()
    mono_font = ImageFont.load_default()

frames = []

for frame_idx in range(TOTAL_FRAMES):
    progress = frame_idx / float(TOTAL_FRAMES)
    
    # Base Slate Dark Background (#0B0F17)
    img = Image.new("RGBA", (WIDTH, HEIGHT), (11, 15, 23, 255))
    draw = ImageDraw.Draw(img)

    # Subtle Dot Matrix Grid
    dot_spacing = 30
    for x in range(dot_spacing, WIDTH, dot_spacing):
        for y in range(dot_spacing, HEIGHT, dot_spacing):
            dist = math.sin((x * 0.005 + y * 0.005) - progress * 2 * math.pi)
            alpha = int(20 + 25 * dist)
            draw.rectangle([x, y, x + 1, y + 1], fill=(226, 232, 240, alpha))

    # Crisp Title "ROHIT SINGH"
    title_text = "ROHIT SINGH"
    title_bbox = title_font.getbbox(title_text)
    t_w = title_bbox[2] - title_bbox[0]
    t_h = title_bbox[3] - title_bbox[1]
    
    cx = WIDTH // 2
    cy = HEIGHT // 2 - 25

    draw.text((cx - t_w // 2 + 1, cy - t_h // 2 + 1), title_text, font=title_font, fill=(0, 0, 0, 100))
    draw.text((cx - t_w // 2, cy - t_h // 2), title_text, font=title_font, fill=(248, 250, 252, 255))

    # Minimalist Accent Pulse Line
    line_y = cy + t_h // 2 + 15
    line_width = 320
    line_x1 = cx - line_width // 2
    line_x2 = cx + line_width // 2
    
    draw.line([(line_x1, line_y), (line_x2, line_y)], fill=(51, 65, 85, 180), width=1)
    
    pulse_length = 80
    pulse_pos = line_x1 + int((progress * (line_width + pulse_length))) - pulse_length
    
    p_x1 = max(line_x1, min(line_x2, pulse_pos))
    p_x2 = max(line_x1, min(line_x2, pulse_pos + pulse_length))
    
    if p_x2 > p_x1:
        draw.line([(p_x1, line_y), (p_x2, line_y)], fill=(16, 185, 129, 255), width=2)

    # Subtitle
    sub_text = "DATA, AI & APPLICATION ENGINEER"
    sub_bbox = sub_font.getbbox(sub_text)
    s_w = sub_bbox[2] - sub_bbox[0]
    s_h = sub_bbox[3] - sub_bbox[1]
    
    scx = WIDTH // 2
    scy = line_y + 30
    draw.text((scx - s_w // 2, scy - s_h // 2), sub_text, font=sub_font, fill=(148, 163, 184, 255))

    # Monospace Skill Header Tag
    top_tag = "// DATABRICKS • SNOWFLAKE • APACHE SPARK • AI / GEN-AI • APP DEV"
    tag_bbox = mono_font.getbbox(top_tag)
    tag_w = tag_bbox[2] - tag_bbox[0]
    draw.text(((WIDTH - tag_w) // 2, 20), top_tag, font=mono_font, fill=(100, 116, 139, 220))

    rgb_img = img.convert("RGB")
    p_img = rgb_img.quantize(colors=64, method=Image.Quantize.MEDIANCUT)
    frames.append(p_img)

frames[0].save(
    OUTPUT_GIF,
    save_all=True,
    append_images=frames[1:],
    duration=60,
    loop=0,
    optimize=True
)

print(f"Updated GIF with new skillset: {OUTPUT_GIF}")
