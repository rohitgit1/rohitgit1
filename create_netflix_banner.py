import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Configuration
WIDTH = 1000
HEIGHT = 380
TOTAL_FRAMES = 42
OUTPUT_GIF = "rohit_netflix_intro.gif"

# Load fonts
try:
    title_font = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 72)
    sub_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
    code_font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
except Exception:
    title_font = ImageFont.load_default()
    sub_font = ImageFont.load_default()
    code_font = ImageFont.load_default()

frames = []

for frame_idx in range(TOTAL_FRAMES):
    progress = frame_idx / float(TOTAL_FRAMES - 1)
    
    # 1. Base Image - Deep Dark Cosmic Background
    img = Image.new("RGBA", (WIDTH, HEIGHT), (9, 10, 16, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw dark gradient background
    for y in range(HEIGHT):
        r = int(9 + (y / HEIGHT) * 15)
        g = int(10 + (y / HEIGHT) * 8)
        b = int(16 + (y / HEIGHT) * 25)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # Draw neural grid lines & particles
    num_particles = 35
    for i in range(num_particles):
        px = (int(i * 37 + frame_idx * 3) % (WIDTH - 40)) + 20
        py = (int(i * 53 + math.sin(frame_idx * 0.2 + i) * 15) % (HEIGHT - 40)) + 20
        size = 2 + (i % 3)
        alpha = int(100 + 155 * math.sin(frame_idx * 0.3 + i))
        
        # Color shifting particles
        if i % 3 == 0:
            color = (147, 51, 234, alpha) # Purple
        elif i % 3 == 1:
            color = (16, 185, 129, alpha) # Emerald
        else:
            color = (245, 158, 11, alpha) # Gold
            
        draw.ellipse([px, py, px + size, py + size], fill=color)
        
        # Draw floating neural connections
        if i > 0:
            prev_px = (int((i - 1) * 37 + frame_idx * 3) % (WIDTH - 40)) + 20
            prev_py = (int((i - 1) * 53 + math.sin(frame_idx * 0.2 + i - 1) * 15) % (HEIGHT - 40)) + 20
            dist = math.hypot(px - prev_px, py - prev_py)
            if dist < 120:
                line_alpha = int(40 * (1 - dist / 120))
                draw.line([(px, py), (prev_px, prev_py)], fill=(139, 92, 246, line_alpha), width=1)

    # 2. Phase 1: Netflix-style Initial Light Beam Blast (Frames 0 to 14)
    beam_progress = min(1.0, frame_idx / 12.0)
    if beam_progress > 0:
        beam_width = int(beam_progress * WIDTH * 0.8)
        beam_x1 = (WIDTH - beam_width) // 2
        beam_x2 = beam_x1 + beam_width
        beam_y = HEIGHT // 2 - 20
        
        # Expanding laser beam flare
        beam_alpha = int(255 * (1 - min(1.0, max(0, (frame_idx - 8) / 10.0))))
        if beam_alpha > 0:
            draw.line([(beam_x1, beam_y), (beam_x2, beam_y)], fill=(236, 72, 153, beam_alpha), width=6)
            draw.line([(beam_x1, beam_y), (beam_x2, beam_y)], fill=(16, 185, 129, beam_alpha // 2), width=18)
            draw.line([(beam_x1, beam_y), (beam_x2, beam_y)], fill=(255, 255, 255, beam_alpha), width=2)

    # 3. Phase 2: Title Zoom & Reveal "ROHIT SINGH" (Starts at frame 6)
    title_text = "ROHIT SINGH"
    if frame_idx >= 6:
        t_progress = min(1.0, (frame_idx - 6) / 14.0)
        # Easing scale effect (Netflix intro zoom)
        scale = 1.6 - 0.6 * math.sin(t_progress * math.pi / 2)
        
        title_bbox = title_font.getbbox(title_text)
        t_w = title_bbox[2] - title_bbox[0]
        t_h = title_bbox[3] - title_bbox[1]
        
        cx = WIDTH // 2
        cy = HEIGHT // 2 - 30
        
        # Create separate layer for text glow & zoom
        txt_img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        txt_draw = ImageDraw.Draw(txt_img)
        
        # Color shifting gradient for title
        # Transitioning through Purple -> Crimson -> Emerald -> Gold
        c_r = int(147 + (236 - 147) * math.sin(t_progress * math.pi))
        c_g = int(51 + (185 - 51) * t_progress)
        c_b = int(234 + (129 - 234) * t_progress)
        
        # Draw multiple outer glow layers
        glow_alpha = int(200 * t_progress)
        for offset in range(8, 0, -2):
            txt_draw.text((cx - t_w // 2, cy - t_h // 2), title_text, font=title_font, fill=(c_r, c_g, c_b, glow_alpha // offset))
            
        # Draw sharp core text
        txt_draw.text((cx - t_w // 2, cy - t_h // 2), title_text, font=title_font, fill=(255, 255, 255, int(255 * t_progress)))
        
        # Composite text layer onto main image
        img = Image.alpha_composite(img, txt_img)
        draw = ImageDraw.Draw(img)

    # 4. Phase 3: Subtitle Reveal "DATA & AI ENGINEER" (Starts at frame 18)
    sub_text = "⚡ DATA & AI ENGINEER ⚡"
    if frame_idx >= 18:
        s_progress = min(1.0, (frame_idx - 18) / 12.0)
        
        sub_bbox = sub_font.getbbox(sub_text)
        s_w = sub_bbox[2] - sub_bbox[0]
        s_h = sub_bbox[3] - sub_bbox[1]
        
        scx = WIDTH // 2
        scy = HEIGHT // 2 + 50
        
        # Laser sweep effect revealing subtitle from left to right
        clip_x = int(scx - s_w // 2 + s_w * s_progress)
        
        sub_img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        sub_draw = ImageDraw.Draw(sub_img)
        
        # Neon Emerald & Cyber Gold theme
        sub_draw.text((scx - s_w // 2, scy - s_h // 2), sub_text, font=sub_font, fill=(16, 185, 129, int(255 * s_progress)))
        
        # Scanning laser line at clip edge
        if s_progress < 1.0:
            sub_draw.line([(clip_x, scy - 20), (clip_x, scy + 20)], fill=(245, 158, 11, 255), width=3)
            sub_draw.line([(clip_x, scy - 25), (clip_x, scy + 25)], fill=(255, 255, 255, 255), width=1)
            
        img = Image.alpha_composite(img, sub_img)
        draw = ImageDraw.Draw(img)

    # 5. Bottom Sci-Fi Border & Status Tag
    border_draw = ImageDraw.Draw(img)
    b_y = HEIGHT - 25
    border_draw.line([(40, b_y), (WIDTH - 40, b_y)], fill=(139, 92, 246, 120), width=1)
    
    # Active laser pulse moving across bottom border
    pulse_x = int(40 + ((frame_idx * 25) % (WIDTH - 80)))
    border_draw.line([(pulse_x, b_y), (pulse_x + 60, b_y)], fill=(16, 185, 129, 255), width=2)
    
    tag_text = "SYS.ONLINE // NEURAL PIPELINES ACTIVE // HYPER-SCALE DATA LAKES"
    t_bbox = code_font.getbbox(tag_text)
    tw = t_bbox[2] - t_bbox[0]
    border_draw.text(((WIDTH - tw) // 2, b_y + 4), tag_text, font=code_font, fill=(148, 163, 184, 180))

    # Convert to P mode for GIF saving
    rgb_img = img.convert("RGB")
    frames.append(rgb_img)

# Save as optimized GIF
frames[0].save(
    OUTPUT_GIF,
    save_all=True,
    append_images=frames[1:],
    duration=70,  # 70ms per frame = ~14 fps
    loop=0,       # infinite loop
    optimize=True
)

print(f"Successfully generated Netflix intro GIF: {OUTPUT_GIF} ({os.path.getsize(OUTPUT_GIF)} bytes)")
