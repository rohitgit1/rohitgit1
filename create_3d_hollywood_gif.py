import os
import math
from PIL import Image, ImageEnhance, ImageDraw

# Keyframe image paths
kf1_path = r"C:\Users\rohit\.gemini\antigravity-ide\brain\799fb5e1-f5bd-4f4d-9098-1f638ddba70b\rohit_keyframe_1_ignition_1788122880866.jpg"
kf2_path = r"C:\Users\rohit\.gemini\antigravity-ide\brain\799fb5e1-f5bd-4f4d-9098-1f638ddba70b\rohit_keyframe_2_title_1788122894288.jpg"
kf3_path = r"C:\Users\rohit\.gemini\antigravity-ide\brain\799fb5e1-f5bd-4f4d-9098-1f638ddba70b\rohit_keyframe_3_masterpiece_1788122908299.jpg"

TARGET_W = 800
TARGET_H = 450

# Load & resize keyframes
img1 = Image.open(kf1_path).convert("RGBA").resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
img2 = Image.open(kf2_path).convert("RGBA").resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
img3 = Image.open(kf3_path).convert("RGBA").resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)

frames = []
TOTAL_FRAMES = 36

for i in range(TOTAL_FRAMES):
    # Phase 1: Ignition (Frames 0-8)
    if i <= 8:
        alpha = i / 8.0
        scale = 1.0 + 0.06 * (1.0 - alpha)
        w_scaled, h_scaled = int(TARGET_W * scale), int(TARGET_H * scale)
        tmp = img1.resize((w_scaled, h_scaled), Image.Resampling.BILINEAR)
        crop_x = (w_scaled - TARGET_W) // 2
        crop_y = (h_scaled - TARGET_H) // 2
        frame = tmp.crop((crop_x, crop_y, crop_x + TARGET_W, crop_y + TARGET_H))
        
        if i >= 6:
            enhancer = ImageEnhance.Brightness(frame)
            frame = enhancer.enhance(1.0 + 0.3 * ((i - 6) / 2.0))

    # Phase 2: Transition from Ignition -> Title Reveal (Frames 9-19)
    elif i <= 19:
        blend_factor = (i - 9) / 10.0
        frame = Image.blend(img1, img2, blend_factor)
        
        sweep_x = int(TARGET_W * blend_factor)
        draw = ImageDraw.Draw(frame)
        draw.line([(sweep_x - 20, 0), (sweep_x + 20, TARGET_H)], fill=(255, 255, 255, 180), width=3)
        draw.line([(sweep_x, 0), (sweep_x, TARGET_H)], fill=(245, 158, 11, 255), width=2)

    # Phase 3: Transition from Title Reveal -> Masterpiece Subtitle (Frames 20-27)
    elif i <= 27:
        blend_factor = (i - 20) / 7.0
        frame = Image.blend(img2, img3, blend_factor)
        
        scan_x = int(TARGET_W * blend_factor)
        draw = ImageDraw.Draw(frame)
        draw.line([(scan_x, TARGET_H - 100), (scan_x, TARGET_H - 15)], fill=(16, 185, 129, 255), width=3)

    # Phase 4: Masterpiece Hold with Metallic Sheen (Frames 28-35)
    else:
        shimmer_factor = (i - 28) / 7.0
        frame = img3.copy()
        draw = ImageDraw.Draw(frame)
        
        sheen_x = int(TARGET_W * shimmer_factor * 1.2)
        draw.line([(sheen_x - 40, 0), (sheen_x + 30, TARGET_H)], fill=(255, 255, 255, 50), width=18)

    # Convert to quantized P-mode image for compact fast GIF
    rgb_frame = frame.convert("RGB")
    p_frame = rgb_frame.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    frames.append(p_frame)

out_gif = "rohit_hollywood_3d_intro.gif"
frames[0].save(
    out_gif,
    save_all=True,
    append_images=frames[1:],
    duration=90,
    loop=0,
    optimize=True
)

print(f"Successfully generated optimized Hollywood 3D Intro GIF: {out_gif} ({os.path.getsize(out_gif)} bytes)")
