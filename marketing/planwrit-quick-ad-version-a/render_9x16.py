#!/usr/bin/env python3
"""
Planwrit Quick Ad Version A -- 9:16 render.
Real Pexels stock photos (from client's Google Drive) + real Planwrit logo +
2 personal Toronto landmark photos, composited with brand-color overlays,
Ken Burns motion, and animated bold text. No external network calls at
render time -- all assets are local files already on disk.
"""
import math
import os
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

W, H = 1080, 1920
FPS = 30
DURATION = 30.0
N_FRAMES = int(DURATION * FPS)

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(REPO_DIR, "assets")
PEXELS = os.path.join(REPO_DIR, "source-photos", "pexels")
PERSONAL = os.path.join(REPO_DIR, "source-photos", "personal")

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

BRAND_GREEN = (28, 61, 46)
WARM_DARK = (42, 34, 26)
WARM_GOLD_TINT = (54, 48, 24)
WHITE = (255, 255, 255)
GOLD = (201, 168, 76)
CREAM = (250, 247, 242)

def ease_out_cubic(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3

_font_cache = {}
def get_font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]

def draw_text_alpha(base_img, pos, text, font, fill, alpha):
    if alpha <= 0:
        return
    txt_layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(txt_layer)
    r, g, b = fill
    d.text(pos, text, font=font, fill=(r, g, b, int(alpha)))
    base_img.alpha_composite(txt_layer)

def measure(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

# ------------------------------------------------------------ photo layer ---

_photo_cache = {}
def load_cover(path, w, h, zoom_pad=1.22):
    key = (path, w, h, zoom_pad)
    if key in _photo_cache:
        return _photo_cache[key]
    im = Image.open(path).convert("RGB")
    target_w, target_h = int(w * zoom_pad), int(h * zoom_pad)
    scale = max(target_w / im.width, target_h / im.height)
    new_size = (max(1, int(im.width * scale)), max(1, int(im.height * scale)))
    im = im.resize(new_size, Image.LANCZOS)
    left = (im.width - target_w) // 2
    top = (im.height - target_h) // 2
    im = im.crop((left, top, left + target_w, top + target_h))
    _photo_cache[key] = im
    return im

_vignette_cache = None
def vignette_layer():
    global _vignette_cache
    if _vignette_cache is not None:
        return _vignette_cache
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy = W / 2, H / 2
    dist = np.sqrt(((xx - cx) / (W / 2)) ** 2 + ((yy - cy) / (H / 2)) ** 2)
    strength = np.clip((dist - 0.55) / 0.65, 0, 1) * 0.5
    alpha = (strength * 255).astype(np.uint8)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    black = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    mask = Image.fromarray(alpha, mode="L")
    layer = Image.composite(black, layer, mask)
    _vignette_cache = layer
    return layer

def animated_photo_bg(path, t_norm, overlay_color=BRAND_GREEN, overlay_alpha=150,
                       zoom_start=1.0, zoom_end=1.13, pan_dir=(1, 0.4)):
    cover = load_cover(path, W, H)
    gw, gh = cover.size
    zoom = zoom_start + (zoom_end - zoom_start) * t_norm
    cw, ch = int(W * zoom), int(H * zoom)
    cw = min(cw, gw)
    ch = min(ch, gh)
    max_px = gw - cw
    max_py = gh - ch
    px = int(max_px * (0.5 + 0.5 * pan_dir[0] * (t_norm - 0.5)))
    py = int(max_py * (0.5 + 0.5 * pan_dir[1] * (t_norm - 0.5)))
    px = max(0, min(px, max_px))
    py = max(0, min(py, max_py))
    crop = cover.crop((px, py, px + cw, py + ch)).resize((W, H), Image.LANCZOS).convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (*overlay_color, overlay_alpha))
    out = Image.alpha_composite(crop, overlay)
    out = Image.alpha_composite(out, vignette_layer())
    return out.convert("RGB")

# --------------------------------------------------------------- logo ------

_logo_rgba = None
def get_logo_rgba():
    global _logo_rgba
    if _logo_rgba is not None:
        return _logo_rgba
    im = Image.open(os.path.join(PERSONAL, "planwrit-logo.jpg")).convert("RGB")
    arr = np.array(im).astype(np.int16)
    diff = 255 - arr.min(axis=2)
    alpha = np.clip(diff * 3, 0, 255).astype(np.uint8)
    rgba = np.dstack([arr.astype(np.uint8), alpha])
    _logo_rgba = Image.fromarray(rgba, mode="RGBA")
    return _logo_rgba

def draw_logo(canvas, center_x, top_y, target_w, alpha_mult):
    if alpha_mult <= 0:
        return
    logo = get_logo_rgba()
    ratio = target_w / logo.width
    target_h = int(logo.height * ratio)
    resized = logo.resize((target_w, target_h), Image.LANCZOS)
    r, g, b, a = resized.split()
    a = a.point(lambda v: int(v * alpha_mult))
    resized = Image.merge("RGBA", (r, g, b, a))
    canvas.alpha_composite(resized, (int(center_x - target_w / 2), int(top_y)))
    return target_h

# ---------------------------------------------------------------- scenes ---

PHOTO_HOOK = os.path.join(PEXELS, "pexels-sora-shimazaki-5668869.jpg")
PHOTO_AGITATE = os.path.join(PEXELS, "pexels-nicola-barts-7927347.jpg")
PHOTO_SOLUTION_A = os.path.join(PEXELS, "pexels-roberto-hund-5357803.jpg")
PHOTO_SOLUTION_B = os.path.join(PERSONAL, "cn-tower-vertical.jpg")
PHOTO_TRUST = os.path.join(PEXELS, "pexels-silverkblack-36733404.jpg")

SERVICE_CUTS = [
    (os.path.join(PEXELS, "pexels-rdne-7845366.jpg"), "C11 Owner-Operator Plans"),
    (os.path.join(PEXELS, "pexels-harrun-muhammad-116282236-37198881.jpg"), "PNP Entrepreneur Streams"),
    (os.path.join(PEXELS, "pexels-kampus-8441809.jpg"), "E2 Investor Visa (USA)"),
    (os.path.join(PEXELS, "pexels-rdne-9034760.jpg"), "Pitch Decks"),
    (os.path.join(PERSONAL, "toronto-front-st-tower.jpg"), "Canadian Grants"),
]

def render_hook(t, dur):
    tn = t / dur
    img = animated_photo_bg(PHOTO_HOOK, tn, BRAND_GREEN, 165, pan_dir=(0.6, 0.3))
    canvas = img.convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    f = get_font(FONT_BOLD, 76)
    l1_alpha = 255 * ease_out_cubic((t - 0.0) / 0.6) * (1 if t < 3.5 else max(0, 1 - (t - 3.5) / 0.5))
    l2_alpha = 255 * ease_out_cubic((t - 0.5) / 0.6) * (1 if t < 3.5 else max(0, 1 - (t - 3.5) / 0.5))
    cx, cy = W / 2, H / 2 + 120
    line_h = f.size * 1.3
    w1, _ = measure(draw, "Most business plans answer", f)
    w2, _ = measure(draw, "the wrong question.", f)
    draw_text_alpha(canvas, (cx - w1 / 2, cy - line_h / 2), "Most business plans answer", f, WHITE, l1_alpha)
    draw_text_alpha(canvas, (cx - w2 / 2, cy + line_h / 2), "the wrong question.", f, GOLD, l2_alpha)
    return canvas.convert("RGB")

def render_agitate(t, dur):
    tn = t / dur
    img = animated_photo_bg(PHOTO_AGITATE, tn, WARM_DARK, 150, pan_dir=(-0.7, 0.2))
    canvas = img.convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    f1 = get_font(FONT_BOLD, 58)
    f3 = get_font(FONT_BOLD, 64)
    lines = [
        (0.0, "The person reading your plan", f1, WHITE),
        (0.15, "has one question.", f1, WHITE),
        (1.3, "Most plans never answer it.", f1, WHITE),
        (2.5, "We build plans that do.", f3, GOLD),
    ]
    cx = W / 2
    line_h = 84
    total_h = line_h * len(lines)
    start_y = H / 2 + 250 - total_h / 2
    for i, (appear_t, text, font, color) in enumerate(lines):
        alpha = 255 * ease_out_cubic((t - appear_t) / 0.5)
        if t > dur - 0.4:
            alpha *= max(0, 1 - (t - (dur - 0.4)) / 0.4)
        w, _ = measure(draw, text, font)
        y = start_y + i * line_h
        draw_text_alpha(canvas, (cx - w / 2, y), text, font, color, alpha)
    return canvas.convert("RGB")

def render_solution(t, dur):
    split = dur * 0.42
    if t < split + 0.4:
        tn = t / split if split else 0
        img = animated_photo_bg(PHOTO_SOLUTION_A, min(tn, 1.0), BRAND_GREEN, 120, pan_dir=(0.5, 0.2))
    if t > split - 0.4:
        tn2 = (t - split) / (dur - split) if dur > split else 0
        img_b = animated_photo_bg(PHOTO_SOLUTION_B, min(max(tn2, 0), 1.0), BRAND_GREEN, 120, pan_dir=(0.2, 0.5))
        if t < split + 0.4:
            blend = (t - (split - 0.4)) / 0.8
            blend = min(max(blend, 0), 1)
            img = Image.blend(img, img_b, blend)
        else:
            img = img_b
    canvas = img.convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    logo_alpha = 255 * ease_out_cubic(t / 0.7)
    if t > dur - 0.5:
        logo_alpha *= max(0, 1 - (t - (dur - 0.5)) / 0.5)
    logo_h = draw_logo(canvas, W / 2, H / 2 - 340, 340, logo_alpha / 255)

    f_brand = get_font(FONT_BOLD, 84)
    f_sub = get_font(FONT_REG, 40)
    brand_alpha = 255 * ease_out_cubic((t - 0.3) / 0.6)
    if t > dur - 0.5:
        brand_alpha *= max(0, 1 - (t - (dur - 0.5)) / 0.5)
    sub_alpha = 255 * ease_out_cubic((t - 1.1) / 0.7)
    if t > dur - 0.5:
        sub_alpha *= max(0, 1 - (t - (dur - 0.5)) / 0.5)
    cx = W / 2
    w_brand, h_brand = measure(draw, "Planwrit.com", f_brand)
    brand_y = H / 2 - 340 + (logo_h or 200) + 60
    w_sub, h_sub = measure(draw, "We write plans that get approved.", f_sub)
    sub_y = brand_y + h_brand + 40
    draw_text_alpha(canvas, (cx - w_brand / 2, brand_y), "Planwrit.com", f_brand, GOLD, brand_alpha)
    draw_text_alpha(canvas, (cx - w_sub / 2, sub_y), "We write plans that get approved.", f_sub, WHITE, sub_alpha)
    return canvas.convert("RGB")

def render_services(t, dur):
    cut_dur = dur / len(SERVICE_CUTS)
    idx = min(int(t / cut_dur), len(SERVICE_CUTS) - 1)
    local_t = t - idx * cut_dur
    photo_path, label = SERVICE_CUTS[idx]
    tn = local_t / cut_dur
    img = animated_photo_bg(photo_path, tn, BRAND_GREEN, 160, pan_dir=(0.8 if idx % 2 == 0 else -0.8, 0.3))
    canvas = img.convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    f = get_font(FONT_BOLD, 66)
    in_a = ease_out_cubic(local_t / 0.3)
    out_a = 1.0 if local_t < cut_dur - 0.3 else max(0, 1 - (local_t - (cut_dur - 0.3)) / 0.3)
    alpha = 255 * min(in_a, out_a)
    slide = (1 - in_a) * 40
    w, h = measure(draw, label, f)
    cx, cy = W / 2, H - 340
    bar_w, bar_h = 90, 6
    if alpha > 0:
        overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(overlay).rectangle(
            [cx - bar_w / 2, cy - h / 2 - 50 + slide, cx + bar_w / 2, cy - h / 2 - 50 + bar_h + slide],
            fill=(*GOLD, int(alpha)),
        )
        canvas.alpha_composite(overlay)
    draw_text_alpha(canvas, (cx - w / 2, cy - h / 2 + slide), label, f, WHITE, alpha)
    idx_text = f"{idx + 1} / {len(SERVICE_CUTS)}"
    f_small = get_font(FONT_REG, 30)
    w2, h2 = measure(draw, idx_text, f_small)
    draw_text_alpha(canvas, (cx - w2 / 2, cy + h / 2 + 60), idx_text, f_small, GOLD, alpha * 0.8)
    return canvas.convert("RGB")

def render_trust(t, dur):
    tn = t / dur
    img = animated_photo_bg(PHOTO_TRUST, tn, WARM_GOLD_TINT, 145, pan_dir=(0.6, -0.3))
    canvas = img.convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    f1 = get_font(FONT_BOLD, 60)
    f2 = get_font(FONT_REG, 40)
    a1 = 255 * ease_out_cubic(t / 0.5)
    a2 = 255 * ease_out_cubic((t - 0.8) / 0.6)
    if t > dur - 0.4:
        fade = max(0, 1 - (t - (dur - 0.4)) / 0.4)
        a1 *= fade
        a2 *= fade
    cx = W / 2
    line1a = "Start with a FREE"
    line1b = "eligibility assessment."
    line2 = "5 minutes. Honest feedback."
    line3 = "No commitment."
    w1a, h1 = measure(draw, line1a, f1)
    w1b, _ = measure(draw, line1b, f1)
    w2, h2 = measure(draw, line2, f2)
    w3, _ = measure(draw, line3, f2)
    top = H - 620
    draw_text_alpha(canvas, (cx - w1a / 2, top), line1a, f1, GOLD, a1)
    draw_text_alpha(canvas, (cx - w1b / 2, top + h1 * 1.25), line1b, f1, WHITE, a1)
    draw_text_alpha(canvas, (cx - w2 / 2, top + h1 * 1.25 * 2 + 60), line2, f2, WHITE, a2)
    draw_text_alpha(canvas, (cx - w3 / 2, top + h1 * 1.25 * 2 + 60 + h2 * 1.4), line3, f2, WHITE, a2)
    return canvas.convert("RGB")

def render_cta(t, dur):
    canvas = Image.new("RGB", (W, H), BRAND_GREEN).convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    logo_alpha = 255 * ease_out_cubic(t / 0.6)
    logo_h = draw_logo(canvas, W / 2, H / 2 - 480, 300, logo_alpha / 255)

    f_url = get_font(FONT_BOLD, 84)
    f_sub = get_font(FONT_BOLD, 38)
    f_services = get_font(FONT_REG, 32)
    a1 = 255 * ease_out_cubic((t - 0.3) / 0.6)
    a2 = 255 * ease_out_cubic((t - 0.9) / 0.6)
    a3 = 255 * ease_out_cubic((t - 1.4) / 0.6)
    cx = W / 2
    url_text = "PLANWRIT.COM"
    w_url, h_url = measure(draw, url_text, f_url)
    url_y = H / 2 - 480 + (logo_h or 180) + 50
    draw_text_alpha(canvas, (cx - w_url / 2, url_y), url_text, f_url, CREAM, a1)
    bar_w = w_url * 0.5
    bar_y = url_y + h_url + 26
    if a1 > 0:
        overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(overlay).rectangle(
            [cx - bar_w / 2, bar_y, cx + bar_w / 2, bar_y + 5], fill=(*GOLD, int(a1))
        )
        canvas.alpha_composite(overlay)
    sub_text = "Free Assessment Available Now"
    w_sub, h_sub = measure(draw, sub_text, f_sub)
    sub_y = bar_y + 55
    draw_text_alpha(canvas, (cx - w_sub / 2, sub_y), sub_text, f_sub, GOLD, a2)
    services_text = "Immigration Plans  ·  Pitch Decks  ·  Grant Writing"
    w_serv, h_serv = measure(draw, services_text, f_services)
    serv_y = sub_y + h_sub + 36
    draw_text_alpha(canvas, (cx - w_serv / 2, serv_y), services_text, f_services, CREAM, a3)
    return canvas.convert("RGB")

SCENES = [
    (0.0, 4.0, render_hook),
    (4.0, 8.0, render_agitate),
    (8.0, 13.0, render_solution),
    (13.0, 22.0, render_services),
    (22.0, 26.0, render_trust),
    (26.0, 30.0, render_cta),
]

CROSSFADE = 0.35

def get_scene_at(global_t):
    for start, end, fn in SCENES:
        if start <= global_t < end:
            return start, end, fn
    return SCENES[-1][0], SCENES[-1][1], SCENES[-1][2]

def render_frame(global_t):
    start, end, fn = get_scene_at(global_t)
    local_t = global_t - start
    dur = end - start
    frame = fn(local_t, dur)

    idx = SCENES.index((start, end, fn))
    if idx > 0 and (global_t - start) < CROSSFADE:
        prev_start, prev_end, prev_fn = SCENES[idx - 1]
        prev_dur = prev_end - prev_start
        prev_frame = prev_fn(prev_dur, prev_dur)
        blend = (global_t - start) / CROSSFADE
        frame = Image.blend(prev_frame, frame, blend)
    return frame

def main():
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    out_path = os.path.join(OUT_DIR, "planwrit-quick-ad-version-a-9x16.mp4")
    cmd = [
        ffmpeg_bin, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
        "-movflags", "+faststart",
        out_path,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(N_FRAMES):
        t = i / FPS
        frame = render_frame(t)
        proc.stdin.write(np.asarray(frame, dtype=np.uint8).tobytes())
        if i % 90 == 0:
            print(f"frame {i}/{N_FRAMES} t={t:.1f}s", flush=True)
    proc.stdin.close()
    proc.wait()
    print("done:", out_path)

if __name__ == "__main__":
    main()
