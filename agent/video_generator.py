"""
Video Generator — creates real MP4 promotional videos using Pillow + moviepy.
Generates text-based animated videos for YouTube, TikTok, Instagram Reels, and Shorts.
"""
import os
import json
import math
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'videos')
FONT_DIR = os.path.join(BASE_DIR, 'assets', 'fonts')


def _ensure_dirs():
    for d in [OUTPUT_DIR, os.path.join(OUTPUT_DIR, 'youtube'), 
              os.path.join(OUTPUT_DIR, 'shorts'), os.path.join(OUTPUT_DIR, 'thumbnails'),
              FONT_DIR]:
        os.makedirs(d, exist_ok=True)


def _get_font(size=60, bold=False):
    """Get a font - try system fonts, fall back to default."""
    font_names = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for fn in font_names:
        if os.path.exists(fn):
            return ImageFont.truetype(fn, size)
    return ImageFont.load_default()


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def _create_gradient_bg(width, height, color1='#0a0a0a', color2='#1a1a2e'):
    """Create a gradient background image."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    r1, g1, b1 = _hex_to_rgb(color1)
    r2, g2, b2 = _hex_to_rgb(color2)
    for y in range(height):
        ratio = y / height
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img


def _draw_text_centered(draw, text, y, width, font, fill=(255, 255, 255)):
    """Draw centered text on image."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def _draw_text_wrapped(draw, text, x, y, max_width, font, fill=(255, 255, 255), line_spacing=10):
    """Draw wrapped text, returns total height used."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    total_height = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        line_h = bbox[3] - bbox[1]
        cx = x + (max_width - text_w) // 2
        draw.text((cx, y + total_height), line, font=font, fill=fill)
        total_height += line_h + line_spacing
    return total_height


def _add_glow(img, cx, cy, radius, color, alpha=80):
    """Add a circular glow effect."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    r, g, b = _hex_to_rgb(color)
    for i in range(radius, 0, -2):
        a = int(alpha * (i / radius))
        draw.ellipse([cx - i, cy - i, cx + i, cy + i], fill=(r, g, b, a))
    img_rgba = img.convert('RGBA')
    result = Image.alpha_composite(img_rgba, overlay)
    return result.convert('RGB')


def generate_thumbnail(title, subtitle="", filename="thumbnail.png", width=1280, height=720):
    """Generate a YouTube thumbnail image."""
    _ensure_dirs()
    img = _create_gradient_bg(width, height, '#0a0a0a', '#16213e')
    img = _add_glow(img, width - 150, 100, 300, '#7b2ff7', 60)
    img = _add_glow(img, 150, height - 100, 250, '#00d4ff', 50)
    
    draw = ImageDraw.Draw(img)
    title_font = _get_font(72, bold=True)
    sub_font = _get_font(36)
    brand_font = _get_font(48, bold=True)
    
    # Title
    _draw_text_wrapped(draw, title, 60, height // 2 - 120, width - 120, title_font, (255, 255, 255))
    
    # Subtitle
    if subtitle:
        _draw_text_wrapped(draw, subtitle, 60, height // 2 + 60, width - 120, sub_font, (160, 160, 160))
    
    # Brand
    draw.text((width - 180, height - 70), "myAI", font=brand_font, fill=_hex_to_rgb('#00d4ff'))
    
    # Accent bar
    draw.rectangle([0, 0, width, 6], fill=_hex_to_rgb('#7b2ff7'))
    draw.rectangle([0, height - 6, width, height], fill=_hex_to_rgb('#00d4ff'))
    
    path = os.path.join(OUTPUT_DIR, 'thumbnails', filename)
    img.save(path, quality=95)
    return path


def _create_frame(width, height, texts, bg_colors=('#0a0a0a', '#1a1a2e'), 
                  accent_color='#00d4ff', glow_pos=None):
    """Create a single video frame with text overlays."""
    img = _create_gradient_bg(width, height, *bg_colors)
    
    if glow_pos:
        for gx, gy, gr, gc in glow_pos:
            img = _add_glow(img, gx, gy, gr, gc, 50)
    
    draw = ImageDraw.Draw(img)
    
    y_offset = 80
    for text_item in texts:
        text = text_item.get('text', '')
        size = text_item.get('size', 48)
        color = text_item.get('color', '#ffffff')
        bold = text_item.get('bold', False)
        y_pos = text_item.get('y', y_offset)
        
        font = _get_font(size, bold)
        fill = _hex_to_rgb(color) if isinstance(color, str) else color
        h = _draw_text_wrapped(draw, text, 60, y_pos, width - 120, font, fill)
        y_offset = y_pos + h + 20
    
    # Brand watermark
    brand_font = _get_font(28, bold=True)
    draw.text((width - 120, height - 50), "myAI", font=brand_font, fill=_hex_to_rgb('#00d4ff'))
    
    return img


def generate_promo_video(title="AI Runs Your Business", scenes=None, 
                         output_name="promo.mp4", fps=12, duration_per_scene=4,
                         video_type="youtube"):
    """Generate a promotional MP4 video with animated text scenes using imageio."""
    _ensure_dirs()
    import numpy as np
    import imageio.v2 as iio
    
    if video_type == "youtube":
        width, height = 1280, 720
        subdir = "youtube"
    else:  # shorts / reels
        width, height = 720, 1280
        subdir = "shorts"
    
    if scenes is None:
        scenes = _get_default_scenes(video_type)
    
    output_path = os.path.join(OUTPUT_DIR, subdir, output_name)
    
    writer = iio.get_writer(output_path, fps=fps, codec='libx264',
                            quality=8, macro_block_size=8)
    
    for i, scene in enumerate(scenes):
        glow_pos = [
            (width - 120, 90, 180, '#7b2ff7'),
            (120, height - 120, 150, '#00d4ff'),
        ]
        
        frame_img = _create_frame(width, height, scene['texts'], 
                              scene.get('bg', ('#0a0a0a', '#1a1a2e')),
                              glow_pos=glow_pos)
        
        frame_array = np.array(frame_img)
        dur = scene.get('duration', duration_per_scene)
        num_frames = int(dur * fps)
        
        fade_frames = min(6, num_frames)
        for f in range(num_frames):
            if f < fade_frames:
                alpha = f / fade_frames
                faded = (frame_array * alpha).astype(np.uint8)
                writer.append_data(faded)
            else:
                writer.append_data(frame_array)
    
    writer.close()
    return output_path


def _get_default_scenes(video_type="youtube"):
    """Default promotional video scenes."""
    if video_type == "shorts":
        return [
            {"texts": [
                {"text": "Your Business", "size": 72, "bold": True, "y": 400},
                {"text": "On Autopilot", "size": 72, "bold": True, "y": 500, "color": "#00d4ff"},
                {"text": "Powered by AI", "size": 36, "y": 650, "color": "#888888"},
            ], "duration": 3},
            {"texts": [
                {"text": "AI Builds Your Website", "size": 56, "bold": True, "y": 350},
                {"text": "Writes Your Content", "size": 56, "bold": True, "y": 450, "color": "#00d4ff"},
                {"text": "Manages Your Marketing", "size": 56, "bold": True, "y": 550, "color": "#7b2ff7"},
            ], "duration": 4},
            {"texts": [
                {"text": "Results:", "size": 48, "y": 300},
                {"text": "347% More Leads", "size": 64, "bold": True, "y": 400, "color": "#00ff88"},
                {"text": "40% Lower Costs", "size": 64, "bold": True, "y": 500, "color": "#00d4ff"},
                {"text": "60 Hours/Week Saved", "size": 64, "bold": True, "y": 600, "color": "#7b2ff7"},
            ], "duration": 4},
            {"texts": [
                {"text": "Start Free Trial", "size": 72, "bold": True, "y": 450, "color": "#00d4ff"},
                {"text": "No Credit Card Required", "size": 36, "y": 580, "color": "#888888"},
                {"text": "myAI", "size": 96, "bold": True, "y": 700, "color": "#ffffff"},
            ], "duration": 3},
        ]
    else:  # youtube landscape
        return [
            {"texts": [
                {"text": "What If AI Could Run", "size": 72, "bold": True, "y": 250},
                {"text": "Your Entire Business?", "size": 72, "bold": True, "y": 350, "color": "#00d4ff"},
            ], "duration": 4},
            {"texts": [
                {"text": "Website Building", "size": 56, "bold": True, "y": 200, "color": "#00d4ff"},
                {"text": "Content Creation", "size": 56, "bold": True, "y": 300, "color": "#7b2ff7"},
                {"text": "Email Campaigns", "size": 56, "bold": True, "y": 400, "color": "#00ff88"},
                {"text": "Social Media Management", "size": 56, "bold": True, "y": 500, "color": "#ff6b6b"},
                {"text": "All Automated. 24/7.", "size": 48, "y": 650, "color": "#888888"},
            ], "duration": 5},
            {"texts": [
                {"text": "Real Results", "size": 64, "bold": True, "y": 200},
                {"text": "347% Increase in Leads", "size": 52, "y": 340, "color": "#00ff88"},
                {"text": "40% Cost Reduction", "size": 52, "y": 430, "color": "#00d4ff"},
                {"text": "10x Faster Content Production", "size": 52, "y": 520, "color": "#7b2ff7"},
                {"text": "60+ Hours/Week Saved", "size": 52, "y": 610, "color": "#ff6b6b"},
            ], "duration": 5},
            {"texts": [
                {"text": "Start Your Free 14-Day Trial", "size": 64, "bold": True, "y": 300, "color": "#00d4ff"},
                {"text": "No Credit Card Required", "size": 40, "y": 420, "color": "#888888"},
                {"text": "aoeua.com", "size": 36, "y": 520, "color": "#ffffff"},
                {"text": "myAI — Your Business on Autopilot", "size": 48, "bold": True, "y": 650, "color": "#7b2ff7"},
            ], "duration": 4},
        ]


def generate_all_videos():
    """Generate all promotional videos and thumbnails."""
    _ensure_dirs()
    results = []
    
    print("[VIDEO] Generating YouTube promo video...")
    path = generate_promo_video(
        title="AI Runs Your Business",
        output_name="myai_promo_youtube.mp4",
        video_type="youtube"
    )
    results.append({"type": "youtube", "path": path})
    print(f"  Created: {path}")
    
    print("[VIDEO] Generating Shorts/Reels video...")
    path = generate_promo_video(
        title="Business on Autopilot",
        output_name="myai_promo_shorts.mp4",
        video_type="shorts"
    )
    results.append({"type": "shorts", "path": path})
    print(f"  Created: {path}")
    
    # Generate niche-specific shorts
    niche_scenes = {
        "restaurants": [
            {"texts": [
                {"text": "Restaurant Owners", "size": 64, "bold": True, "y": 350},
                {"text": "Stop Losing Money", "size": 64, "bold": True, "y": 450, "color": "#ff6b6b"},
                {"text": "On Manual Work", "size": 64, "bold": True, "y": 550, "color": "#ff6b6b"},
            ], "duration": 3},
            {"texts": [
                {"text": "AI Handles:", "size": 48, "y": 300},
                {"text": "Reservations", "size": 56, "bold": True, "y": 400, "color": "#00d4ff"},
                {"text": "Inventory Tracking", "size": 56, "bold": True, "y": 500, "color": "#00ff88"},
                {"text": "Customer Service 24/7", "size": 56, "bold": True, "y": 600, "color": "#7b2ff7"},
            ], "duration": 4},
            {"texts": [
                {"text": "Starting at $299/mo", "size": 56, "bold": True, "y": 400, "color": "#00d4ff"},
                {"text": "Free 14-Day Trial", "size": 48, "y": 520},
                {"text": "Link in Bio", "size": 40, "y": 650, "color": "#888888"},
            ], "duration": 3},
        ],
        "dental": [
            {"texts": [
                {"text": "Dental Practices", "size": 64, "bold": True, "y": 350},
                {"text": "Tired of No-Shows?", "size": 64, "bold": True, "y": 450, "color": "#ff6b6b"},
            ], "duration": 3},
            {"texts": [
                {"text": "AI Powered:", "size": 48, "y": 300},
                {"text": "Smart Scheduling", "size": 56, "bold": True, "y": 400, "color": "#00d4ff"},
                {"text": "Auto Reminders", "size": 56, "bold": True, "y": 500, "color": "#00ff88"},
                {"text": "Patient Follow-up", "size": 56, "bold": True, "y": 600, "color": "#7b2ff7"},
            ], "duration": 4},
            {"texts": [
                {"text": "Starting at $349/mo", "size": 56, "bold": True, "y": 400, "color": "#00d4ff"},
                {"text": "Free 14-Day Trial", "size": 48, "y": 520},
                {"text": "Link in Bio", "size": 40, "y": 650, "color": "#888888"},
            ], "duration": 3},
        ],
        "legal": [
            {"texts": [
                {"text": "Law Firms", "size": 64, "bold": True, "y": 350},
                {"text": "Stop Drowning in Paperwork", "size": 56, "bold": True, "y": 450, "color": "#ff6b6b"},
            ], "duration": 3},
            {"texts": [
                {"text": "AI Handles:", "size": 48, "y": 300},
                {"text": "Document Processing", "size": 56, "bold": True, "y": 400, "color": "#00d4ff"},
                {"text": "Deadline Tracking", "size": 56, "bold": True, "y": 500, "color": "#00ff88"},
                {"text": "Time Capture", "size": 56, "bold": True, "y": 600, "color": "#7b2ff7"},
            ], "duration": 4},
            {"texts": [
                {"text": "Starting at $499/mo", "size": 56, "bold": True, "y": 400, "color": "#00d4ff"},
                {"text": "Free 14-Day Trial", "size": 48, "y": 520},
                {"text": "Link in Bio", "size": 40, "y": 650, "color": "#888888"},
            ], "duration": 3},
        ],
    }
    
    for niche, scenes in niche_scenes.items():
        print(f"[VIDEO] Generating {niche} promo short...")
        path = generate_promo_video(
            title=f"AI for {niche}",
            scenes=scenes,
            output_name=f"myai_{niche}_short.mp4",
            video_type="shorts"
        )
        results.append({"type": f"shorts_{niche}", "path": path})
        print(f"  Created: {path}")
    
    # Generate thumbnails
    thumbnail_configs = [
        ("AI RUNS MY BUSINESS 24/7", "See How It Works", "thumb_main.png"),
        ("I Let AI Handle Marketing for 30 Days", "The Results Were INSANE", "thumb_30days.png"),
        ("5 Tasks You Should NEVER Do Manually", "AI Does Them Better", "thumb_5tasks.png"),
        ("Restaurant AI: Cut Costs by 40%", "Automation for Food Business", "thumb_restaurants.png"),
        ("Dental Practice AI Automation", "No More No-Shows", "thumb_dental.png"),
        ("Law Firm AI: Save 60 Hours/Week", "Document Processing on Autopilot", "thumb_legal.png"),
    ]
    
    for title, subtitle, fname in thumbnail_configs:
        print(f"[VIDEO] Generating thumbnail: {fname}")
        path = generate_thumbnail(title, subtitle, fname)
        results.append({"type": "thumbnail", "path": path})
    
    # Save index
    index_path = os.path.join(OUTPUT_DIR, 'videos_index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump({
            "generated": datetime.now().isoformat(),
            "total": len(results),
            "videos": results
        }, f, indent=2)
    
    print(f"\n[VIDEO] Generated {len(results)} assets total")
    return results


if __name__ == "__main__":
    generate_all_videos()
