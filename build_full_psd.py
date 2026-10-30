import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pytoshop
from pytoshop.user import nested_layers
from pytoshop.enums import ColorMode, Compression

OUTPUT_DIR = r"C:\Users\Yanserd\Desktop\Entender\TechStore_Photoshop_Mockup"
os.makedirs(OUTPUT_DIR, exist_ok=True)

WIDTH = 1000
HEIGHT = 2000

# Color Palette
C_BG_DEEP = (10, 14, 23, 255)
C_BG_CARD = (18, 26, 43, 255)
C_BG_CARD_LIGHT = (26, 38, 62, 255)
C_BORDER = (38, 52, 80, 255)
C_BORDER_BRIGHT = (0, 210, 255, 180)
C_BLUE = (0, 102, 255, 255)
C_CYAN = (0, 210, 255, 255)
C_WHITE = (255, 255, 255, 255)
C_SLATE = (148, 163, 184, 255)
C_DARK_SLATE = (71, 85, 105, 255)
C_GREEN = (16, 185, 129, 255)
C_CORAL = (255, 71, 87, 255)
C_YELLOW = (250, 204, 21, 255)

def get_font(size, bold=False):
    names = ["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]
    for n in names:
        p = os.path.join(r"C:\Windows\Fonts", n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def new_layer():
    return Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))

def pil_to_layer(im, name):
    bbox = im.getbbox()
    if bbox is None:
        cropped = im.crop((0, 0, 1, 1))
        top, left = 0, 0
    else:
        cropped = im.crop(bbox)
        left, top, right, bottom = bbox
    arr = np.array(cropped)
    return nested_layers.Image(
        name=name,
        top=top,
        left=left,
        channels={
            0: np.ascontiguousarray(arr[:, :, 0]),
            1: np.ascontiguousarray(arr[:, :, 1]),
            2: np.ascontiguousarray(arr[:, :, 2]),
            -1: np.ascontiguousarray(arr[:, :, 3])
        }
    )

def draw_gradient_rect(target, bbox, radius, c1, c2, horizontal=True, border=None, border_w=1):
    x0, y0, x1, y1 = bbox
    w = max(1, x1 - x0)
    h = max(1, y1 - y0)
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            f = (x / (w - 1)) if horizontal else (y / (h - 1)) if h > 1 else 0
            arr[y, x, 0] = int(c1[0] * (1 - f) + c2[0] * f)
            arr[y, x, 1] = int(c1[1] * (1 - f) + c2[1] * f)
            arr[y, x, 2] = int(c1[2] * (1 - f) + c2[2] * f)
            a1 = c1[3] if len(c1) == 4 else 255
            a2 = c2[3] if len(c2) == 4 else 255
            arr[y, x, 3] = int(a1 * (1 - f) + a2 * f)
    grad = Image.fromarray(arr)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    target.paste(grad, (x0, y0), mask)
    if border:
        ImageDraw.Draw(target).rounded_rectangle([x0, y0, x1 - 1, y1 - 1], radius=radius, outline=border, width=border_w)

def draw_radial_glow(target, cx, cy, radius, color):
    w, h = radius * 2, radius * 2
    glow_arr = np.zeros((h, w, 4), dtype=np.uint8)
    y_idx, x_idx = np.ogrid[:h, :w]
    dist = np.hypot(x_idx - radius, y_idx - radius)
    f = np.clip(1.0 - (dist / radius), 0.0, 1.0)
    f = np.power(f, 2.0)
    glow_arr[:, :, 0] = color[0]
    glow_arr[:, :, 1] = color[1]
    glow_arr[:, :, 2] = color[2]
    max_a = color[3] if len(color) == 4 else 255
    glow_arr[:, :, 3] = (f * max_a).astype(np.uint8)
    glow_img = Image.fromarray(glow_arr)
    target.paste(glow_img, (cx - radius, cy - radius), glow_img)

def draw_stars(draw, x, y, count=5, size=14, color=C_YELLOW):
    for i in range(count):
        sx = x + i * (size + 4)
        draw.text((sx, y), "★", fill=color, font=get_font(size, bold=True))

# ----------------- VECTOR DRAWING HELPERS -----------------

def draw_tech_logo(target, x, y, size=38):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # Hexagonal / Diamond isometric tech box
    cx, cy = size / 2, size / 2
    pts = [
        (cx, 2),
        (size - 4, cy - 8),
        (size - 4, cy + 10),
        (cx, size - 2),
        (4, cy + 10),
        (4, cy - 8)
    ]
    d.polygon(pts, fill=(0, 102, 255, 180), outline=C_CYAN)
    d.line([(cx, 2), (cx, size - 2)], fill=C_CYAN, width=2)
    d.line([(4, cy - 8), (cx, cy)], fill=C_WHITE, width=2)
    d.line([(size - 4, cy - 8), (cx, cy)], fill=C_WHITE, width=2)
    target.paste(im, (x, y), im)

def draw_truck_icon(target, x, y):
    d = ImageDraw.Draw(target)
    # Delivery truck vector
    d.rounded_rectangle([x, y + 8, x + 24, y + 26], radius=2, fill=(0, 210, 255, 60), outline=C_CYAN, width=2)
    d.polygon([(x + 24, y + 14), (x + 32, y + 14), (x + 36, y + 20), (x + 36, y + 26), (x + 24, y + 26)], fill=(0, 210, 255, 100), outline=C_CYAN)
    # Wheels
    d.ellipse([x + 6, y + 24, x + 12, y + 30], fill=C_WHITE, outline=C_CYAN, width=1)
    d.ellipse([x + 24, y + 24, x + 30, y + 30], fill=C_WHITE, outline=C_CYAN, width=1)
    # Speed lines
    d.line([(x - 8, y + 12), (x - 2, y + 12)], fill=C_CYAN, width=2)
    d.line([(x - 12, y + 18), (x - 3, y + 18)], fill=C_CYAN, width=2)
    d.line([(x - 6, y + 24), (x - 2, y + 24)], fill=C_CYAN, width=2)

def draw_shield_icon(target, x, y):
    d = ImageDraw.Draw(target)
    pts = [
        (x + 16, y + 4),
        (x + 30, y + 9),
        (x + 28, y + 23),
        (x + 16, y + 32),
        (x + 4, y + 23),
        (x + 2, y + 9)
    ]
    d.polygon(pts, fill=(0, 210, 255, 50), outline=C_CYAN, width=2)
    # Checkmark inside
    d.line([(x + 9, y + 16), (x + 14, y + 21)], fill=C_WHITE, width=2)
    d.line([(x + 14, y + 21), (x + 23, y + 12)], fill=C_WHITE, width=2)

def draw_lock_icon(target, x, y):
    d = ImageDraw.Draw(target)
    # Shackle
    d.arc([x + 8, y + 4, x + 24, y + 20], start=180, end=0, fill=C_CYAN, width=2)
    # Body
    d.rounded_rectangle([x + 6, y + 14, x + 26, y + 30], radius=3, fill=(0, 210, 255, 60), outline=C_CYAN, width=2)
    # Keyhole
    d.ellipse([x + 14, y + 19, x + 18, y + 23], fill=C_WHITE)
    d.line([(x + 16, y + 23), (x + 16, y + 26)], fill=C_WHITE, width=2)

def draw_headset_icon(target, x, y):
    d = ImageDraw.Draw(target)
    d.arc([x + 6, y + 4, x + 26, y + 26], start=170, end=10, fill=C_CYAN, width=2)
    d.rounded_rectangle([x + 3, y + 14, x + 8, y + 25], radius=2, fill=C_WHITE)
    d.rounded_rectangle([x + 24, y + 14, x + 29, y + 25], radius=2, fill=C_WHITE)
    d.arc([x + 12, y + 14, x + 26, y + 29], start=20, end=90, fill=C_CYAN, width=2)
    d.ellipse([x + 10, y + 27, x + 14, y + 31], fill=C_CYAN)

def draw_cart_icon(target, x, y):
    d = ImageDraw.Draw(target)
    # Handle & basket
    d.line([(x, y + 4), (x + 5, y + 4), (x + 9, y + 18), (x + 23, y + 18)], fill=C_WHITE, width=2)
    d.polygon([(x + 5, y + 4), (x + 25, y + 6), (x + 22, y + 16), (x + 8, y + 16)], fill=(0, 210, 255, 80), outline=C_WHITE)
    # Wheels
    d.ellipse([x + 10, y + 20, x + 13, y + 23], fill=C_CYAN)
    d.ellipse([x + 20, y + 20, x + 23, y + 23], fill=C_CYAN)

def draw_search_icon(target, x, y):
    d = ImageDraw.Draw(target)
    d.ellipse([x, y, x + 14, y + 14], outline=C_SLATE, width=2)
    d.line([(x + 11, y + 11), (x + 18, y + 18)], fill=C_SLATE, width=2)

def draw_user_icon(target, x, y):
    d = ImageDraw.Draw(target)
    d.ellipse([x + 4, y, x + 14, y + 10], outline=C_SLATE, width=2)
    d.arc([x, y + 9, x + 18, y + 23], start=180, end=0, fill=C_SLATE, width=2)

# ----------------- GADGET RENDERERS -----------------

def render_hero_headphones():
    im = Image.new("RGBA", (450, 420), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 225, 200
    
    # Floor drop shadow
    shadow = Image.new("RGBA", (450, 420), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse([cx - 150, cy + 130, cx + 150, cy + 180], fill=(0, 0, 0, 180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))
    im.paste(shadow, (0, 0), shadow)
    
    # Soundwaves / Equalizer arcs
    for r_arc in [170, 195, 220]:
        d.arc([cx - r_arc, cy - r_arc, cx + r_arc, cy + r_arc], start=210, end=250, fill=(0, 210, 255, 80), width=2)
        d.arc([cx - r_arc, cy - r_arc, cx + r_arc, cy + r_arc], start=290, end=330, fill=(0, 210, 255, 80), width=2)
        d.arc([cx - r_arc, cy - r_arc, cx + r_arc, cy + r_arc], start=30, end=70, fill=(0, 210, 255, 60), width=2)
        d.arc([cx - r_arc, cy - r_arc, cx + r_arc, cy + r_arc], start=110, end=150, fill=(0, 210, 255, 60), width=2)
    
    # Headband outer metallic arch
    d.arc([cx - 110, cy - 170, cx + 110, cy + 50], start=190, end=350, fill=(160, 180, 210, 255), width=18)
    # Headband inner cushion
    d.arc([cx - 100, cy - 160, cx + 100, cy + 40], start=195, end=345, fill=(20, 28, 45, 255), width=12)
    
    # Earcups (Left and Right)
    # Left Earcup
    lx, ly = cx - 110, cy + 30
    d.rounded_rectangle([lx - 25, ly - 50, lx + 25, ly + 50], radius=22, fill=(15, 22, 35, 255), outline=(50, 70, 100, 255), width=3)
    d.rounded_rectangle([lx - 16, ly - 38, lx + 16, ly + 38], radius=16, fill=(25, 36, 56, 255))
    # Glowing cyan LED ring on left cup
    d.ellipse([lx - 10, ly - 15, lx + 10, ly + 15], outline=C_CYAN, width=3)
    d.text((lx - 5, ly - 8), "X", fill=C_WHITE, font=get_font(12, bold=True))
    
    # Right Earcup
    rx, ry = cx + 110, cy + 30
    d.rounded_rectangle([rx - 25, ry - 50, rx + 25, ry + 50], radius=22, fill=(15, 22, 35, 255), outline=(50, 70, 100, 255), width=3)
    d.rounded_rectangle([rx - 16, ry - 38, rx + 16, ry + 38], radius=16, fill=(25, 36, 56, 255))
    # Glowing cyan LED ring on right cup
    d.ellipse([rx - 10, ry - 15, rx + 10, ry + 15], outline=C_CYAN, width=3)
    d.text((rx - 5, ry - 8), "X", fill=C_WHITE, font=get_font(12, bold=True))
    
    # Glow blur effect
    glow = Image.new("RGBA", (450, 420), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([lx - 18, ly - 23, lx + 18, ly + 23], fill=(0, 210, 255, 120))
    ImageDraw.Draw(glow).ellipse([rx - 18, ry - 23, rx + 18, ry + 23], fill=(0, 210, 255, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(8))
    im.paste(glow, (0, 0), glow)
    
    return im

def render_smartwatch():
    im = Image.new("RGBA", (240, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 120, 100
    # Strap
    d.rounded_rectangle([cx - 26, 10, cx + 26, 190], radius=8, fill=(30, 41, 59, 255), outline=(51, 65, 85, 255), width=2)
    # Shadow
    shadow = Image.new("RGBA", (240, 200), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse([cx - 45, cy + 30, cx + 45, cy + 65], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    im.paste(shadow, (0, 0), shadow)
    # Watch Case
    d.rounded_rectangle([cx - 42, cy - 50, cx + 42, cy + 50], radius=18, fill=(15, 23, 42, 255), outline=(71, 85, 105, 255), width=3)
    # Dial Glass
    d.rounded_rectangle([cx - 36, cy - 44, cx + 36, cy + 44], radius=14, fill=(5, 10, 20, 255), outline=C_BORDER_BRIGHT, width=1)
    # Screen UI Rings
    d.arc([cx - 24, cy - 30, cx + 24, cy + 18], start=120, end=40, fill=C_CORAL, width=3)
    d.arc([cx - 19, cy - 25, cx + 19, cy + 13], start=160, end=80, fill=C_CYAN, width=3)
    d.arc([cx - 14, cy - 20, cx + 14, cy + 8], start=200, end=140, fill=C_GREEN, width=3)
    # Time
    d.text((cx - 20, cy + 8), "10:42", fill=C_WHITE, font=get_font(13, bold=True))
    d.text((cx - 15, cy + 24), "78 bpm", fill=C_CORAL, font=get_font(9, bold=True))
    # Button Crown
    d.rounded_rectangle([cx + 42, cy - 14, cx + 46, cy + 2], radius=2, fill=(148, 163, 184, 255))
    return im

def render_earbuds():
    im = Image.new("RGBA", (240, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 120, 105
    # Shadow
    shadow = Image.new("RGBA", (240, 200), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse([cx - 50, cy + 30, cx + 50, cy + 60], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    im.paste(shadow, (0, 0), shadow)
    # Open Charging Case Base
    d.rounded_rectangle([cx - 46, cy - 20, cx + 46, cy + 42], radius=20, fill=(15, 23, 42, 255), outline=(71, 85, 105, 255), width=2)
    # Open Lid behind
    d.rounded_rectangle([cx - 44, cy - 50, cx + 44, cy - 16], radius=16, fill=(20, 30, 50, 255), outline=(56, 189, 248, 120), width=2)
    # Inner wells glowing cyan
    d.ellipse([cx - 30, cy - 15, cx - 10, cy + 12], fill=(0, 210, 255, 60), outline=C_CYAN)
    d.ellipse([cx + 10, cy - 15, cx + 30, cy + 12], fill=(0, 210, 255, 60), outline=C_CYAN)
    # Earbuds stems
    d.rounded_rectangle([cx - 24, cy - 30, cx - 16, cy + 10], radius=4, fill=C_WHITE)
    d.rounded_rectangle([cx + 16, cy - 30, cx + 24, cy + 10], radius=4, fill=C_WHITE)
    # LED status dot
    d.ellipse([cx - 3, cy + 12, cx + 3, cy + 18], fill=C_GREEN)
    return im

def render_keyboard():
    im = Image.new("RGBA", (240, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 120, 105
    # Shadow
    shadow = Image.new("RGBA", (240, 200), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse([cx - 70, cy + 30, cx + 70, cy + 55], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    im.paste(shadow, (0, 0), shadow)
    # Keyboard Aluminum Body
    d.rounded_rectangle([cx - 72, cy - 40, cx + 72, cy + 35], radius=8, fill=(15, 23, 42, 255), outline=(71, 85, 105, 255), width=2)
    # Key matrix rows with RGB neon
    colors = [C_CYAN, (0, 160, 255, 255), (140, 60, 255, 255), C_CORAL]
    for row in range(4):
        ky = cy - 32 + row * 15
        kc = colors[row]
        for col in range(8):
            kx = cx - 64 + col * 16
            d.rectangle([kx, ky, kx + 13, ky + 11], fill=(25, 35, 55, 255), outline=kc, width=1)
    # Rotary knob
    d.ellipse([cx + 52, cy - 34, cx + 64, cy - 22], fill=(160, 180, 210, 255), outline=C_CYAN, width=1)
    return im

print("Gadget models compiled.")

def build_all_layers():
    groups = []
    
    # ----------------------------------------------------
    # 00_FONDO_GLOBAL
    # ----------------------------------------------------
    im_bg = new_layer()
    draw_bg = ImageDraw.Draw(im_bg)
    # Background mesh & gradient
    for y in range(HEIGHT):
        factor = y / HEIGHT
        # Gradient from #070B14 to #0E1726 to #090D18
        r = int(7 * (1 - factor) + 14 * factor)
        g = int(11 * (1 - factor) + 23 * factor)
        b = int(20 * (1 - factor) + 38 * factor)
        draw_bg.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))
    
    # Subtle ambient radial spots
    draw_radial_glow(im_bg, 800, 300, 450, (0, 102, 255, 35))
    draw_radial_glow(im_bg, 200, 900, 400, (0, 210, 255, 20))
    draw_radial_glow(im_bg, 750, 1400, 450, (121, 40, 202, 25))
    draw_radial_glow(im_bg, 300, 1850, 350, (0, 102, 255, 25))
    
    layer_bg = pil_to_layer(im_bg, "Malla_Fondo_Oscura_Tech")
    grp_bg = nested_layers.Group(name="00_FONDO_GLOBAL", layers=[layer_bg], closed=False)
    
    # ----------------------------------------------------
    # 01_HEADER
    # ----------------------------------------------------
    # Background header
    im_h_bg = new_layer()
    draw_gradient_rect(im_h_bg, [0, 0, WIDTH, 80], radius=0, c1=(10, 15, 28, 240), c2=(15, 22, 40, 240), border=(56, 189, 248, 70), border_w=1)
    l_h_bg = pil_to_layer(im_h_bg, "Fondo_Header_Glassmorphism")
    
    # Logo
    im_h_logo = new_layer()
    draw_tech_logo(im_h_logo, 50, 21, size=38)
    d_logo = ImageDraw.Draw(im_h_logo)
    d_logo.text((98, 24), "DBA", fill=C_WHITE, font=get_font(20, bold=True))
    d_logo.text((144, 24), "TECHSTORE", fill=C_CYAN, font=get_font(20, bold=True))
    d_logo.text((98, 48), "INNOVACIÓN DIGITAL Y GADGETS", fill=C_SLATE, font=get_font(9, bold=False))
    l_h_logo = pil_to_layer(im_h_logo, "Logo_DBA_TechStore")
    
    # Menu Navigation
    im_h_menu = new_layer()
    d_menu = ImageDraw.Draw(im_h_menu)
    menu_items = [
        ("INICIO", True, False),
        ("PRODUCTOS", False, False),
        ("OFERTAS", False, True),
        ("BENEFICIOS", False, False),
        ("SOPORTE", False, False),
        ("CONTACTO", False, False)
    ]
    mx = 360
    for label, is_active, is_hot in menu_items:
        col = C_CYAN if is_active else C_WHITE
        f = get_font(13, bold=is_active)
        d_menu.text((mx, 32), label, fill=col, font=f)
        if is_active:
            # Active indicator bar
            d_menu.rounded_rectangle([mx - 4, 54, mx + 48, 57], radius=2, fill=C_CYAN)
        if is_hot:
            # HOT badge
            draw_gradient_rect(im_h_menu, [mx + 60, 26, mx + 92, 40], radius=4, c1=C_CORAL, c2=(255, 100, 50, 255))
            ImageDraw.Draw(im_h_menu).text((mx + 64, 28), "HOT", fill=C_WHITE, font=get_font(8, bold=True))
        mx += 78 if not is_hot else 105
    l_h_menu = pil_to_layer(im_h_menu, "Menu_Navegacion_Interactivo")
    
    # Header Actions (Search, Cart, User)
    im_h_act = new_layer()
    draw_search_icon(im_h_act, 830, 31)
    draw_cart_icon(im_h_act, 875, 29)
    # Cart badge (3)
    d_act = ImageDraw.Draw(im_h_act)
    d_act.ellipse([894, 22, 908, 36], fill=C_CORAL)
    d_act.text((898, 23), "3", fill=C_WHITE, font=get_font(9, bold=True))
    draw_user_icon(im_h_act, 935, 29)
    l_h_act = pil_to_layer(im_h_act, "Iconos_Acciones_Usuario")
    
    grp_header = nested_layers.Group(name="01_HEADER", layers=[l_h_act, l_h_menu, l_h_logo, l_h_bg], closed=False)
    
    # ----------------------------------------------------
    # 02_BANNER_HERO
    # ----------------------------------------------------
    # Background Glow
    im_b_glow = new_layer()
    draw_radial_glow(im_b_glow, 720, 280, 280, (0, 102, 255, 90))
    draw_radial_glow(im_b_glow, 720, 280, 180, (0, 210, 255, 110))
    l_b_glow = pil_to_layer(im_b_glow, "Resplandor_Neon_Hero")
    
    # Headphone Gadget
    im_b_gadget = new_layer()
    hp = render_hero_headphones()
    im_b_gadget.paste(hp, (520, 110), hp)
    l_b_gadget = pil_to_layer(im_b_gadget, "Ilustracion_Gadget_Headphones")
    
    # Hero Texts
    im_b_text = new_layer()
    d_b_text = ImageDraw.Draw(im_b_text)
    # Tag
    draw_gradient_rect(im_b_text, [50, 125, 245, 155], radius=6, c1=(0, 102, 255, 120), c2=(0, 210, 255, 120), border=C_CYAN, border_w=1)
    ImageDraw.Draw(im_b_text).text((62, 132), "⚡ NUEVA GENERACIÓN 2026", fill=C_WHITE, font=get_font(10, bold=True))
    
    # H1 Title
    d_b_text.text((50, 175), "AUDIO PRO ULTRA", fill=C_WHITE, font=get_font(38, bold=True))
    d_b_text.text((50, 222), "SONIDO INMERSIVO 8D", fill=C_CYAN, font=get_font(34, bold=True))
    
    # Subtitle Paragraph
    sub_lines = [
        "Experimenta cancelación activa de ruido adaptativa con IA,",
        "drivers de titanio de 50mm y audio espacial de 360 grados.",
        "Hasta 48 horas de reproducción continua con carga ultra rápida."
    ]
    for i, line in enumerate(sub_lines):
        d_b_text.text((50, 285 + i * 22), line, fill=C_SLATE, font=get_font(14))
    
    # Spec Pills
    specs = ["ANC Inteligente", "Titanio 50mm", "48h Batería", "Bluetooth 5.4"]
    sp_x = 50
    for s in specs:
        draw_gradient_rect(im_b_text, [sp_x, 360, sp_x + 95, 385], radius=4, c1=C_BG_CARD, c2=C_BG_CARD_LIGHT, border=C_BORDER)
        ImageDraw.Draw(im_b_text).text((sp_x + 10, 366), s, fill=C_WHITE, font=get_font(10, bold=True))
        sp_x += 105
        
    l_b_text = pil_to_layer(im_b_text, "Textos_Titulos_Hero")
    
    # Buttons (Interactive Zones)
    im_b_btn = new_layer()
    # Primary CTA with electric gradient and shadow
    draw_gradient_rect(im_b_btn, [50, 415, 290, 470], radius=8, c1=C_BLUE, c2=C_CYAN, border=C_WHITE, border_w=1)
    d_btn = ImageDraw.Draw(im_b_btn)
    d_btn.text((72, 431), "COMPRAR AHORA", fill=C_WHITE, font=get_font(15, bold=True))
    d_btn.text((215, 432), "$249.99", fill=(10, 25, 45, 255), font=get_font(14, bold=True))
    d_btn.text((270, 431), "➔", fill=(10, 25, 45, 255), font=get_font(15, bold=True))
    
    # Secondary Button
    draw_gradient_rect(im_b_btn, [310, 415, 490, 470], radius=8, c1=(20, 30, 50, 255), c2=(30, 45, 75, 255), border=C_BORDER)
    ImageDraw.Draw(im_b_btn).text((332, 432), "VER ESPECIFICACIONES", fill=C_WHITE, font=get_font(12, bold=True))
    
    l_b_btn = pil_to_layer(im_b_btn, "Botones_CTA_Hero_Interactivo")
    
    grp_hero = nested_layers.Group(name="02_BANNER_HERO", layers=[l_b_btn, l_b_text, l_b_gadget, l_b_glow], closed=False)
    
    # ----------------------------------------------------
    # 03_BENEFICIOS_VECTORES
    # ----------------------------------------------------
    im_ben_cards = new_layer()
    im_ben_icons = new_layer()
    im_ben_text = new_layer()
    d_ben_text = ImageDraw.Draw(im_ben_text)
    
    # Section Header
    d_ben_text.text((50, 515), "VENTAJAS EXCLUSIVAS DE COMPRA", fill=C_CYAN, font=get_font(12, bold=True))
    d_ben_text.text((50, 535), "¿POR QUÉ MILES ELIGEN TECHSTORE?", fill=C_WHITE, font=get_font(22, bold=True))
    
    cards_data = [
        ("Envíos Express Gratis", "Entregas prioritarias en 24/48h sin costo a nivel nacional.", draw_truck_icon),
        ("Garantía Oficial 2 Años", "Cobertura completa y reemplazo inmediato sin trámites.", draw_shield_icon),
        ("Pago Cifrado 256-bit", "Transacciones blindadas con protección antifraude total.", draw_lock_icon),
        ("Soporte Técnico 24/7", "Asesoría especializada de ingenieros en vivo los 365 días.", draw_headset_icon)
    ]
    
    cx_start = 50
    cw = 212
    gap = 17
    for i, (title, desc, icon_func) in enumerate(cards_data):
        bx = cx_start + i * (cw + gap)
        by = 575
        bh = 120
        # Card base
        draw_gradient_rect(im_ben_cards, [bx, by, bx + cw, by + bh], radius=10, c1=C_BG_CARD, c2=C_BG_CARD_LIGHT, border=C_BORDER, border_w=1)
        # Vector Icon Badge
        draw_gradient_rect(im_ben_icons, [bx + 14, by + 16, bx + 54, by + 56], radius=8, c1=(0, 102, 255, 60), c2=(0, 210, 255, 60), border=C_BORDER_BRIGHT)
        icon_func(im_ben_icons, bx + 16, by + 19)
        # Texts
        d_ben_text.text((bx + 14, by + 68), title, fill=C_WHITE, font=get_font(13, bold=True))
        # 2 lines desc
        words = desc.split()
        l1 = " ".join(words[:4])
        l2 = " ".join(words[4:])
        d_ben_text.text((bx + 14, by + 86), l1, fill=C_SLATE, font=get_font(10))
        d_ben_text.text((bx + 14, by + 99), l2, fill=C_SLATE, font=get_font(10))
        
    l_ben_cards = pil_to_layer(im_ben_cards, "Tarjetas_Base_Beneficios")
    l_ben_icons = pil_to_layer(im_ben_icons, "Iconos_Vectores_Hexagonos")
    l_ben_text = pil_to_layer(im_ben_text, "Textos_Beneficios")
    
    grp_beneficios = nested_layers.Group(name="03_BENEFICIOS_VECTORES", layers=[l_ben_icons, l_ben_text, l_ben_cards], closed=False)
    
    # ----------------------------------------------------
    # 04_PRODUCTOS_DESTACADOS
    # ----------------------------------------------------
    im_prod_head = new_layer()
    d_prod_head = ImageDraw.Draw(im_prod_head)
    d_prod_head.text((50, 725), "CATÁLOGO PREMIUM", fill=C_CYAN, font=get_font(12, bold=True))
    d_prod_head.text((50, 745), "GADGETS MÁS VENDIDOS DE LA SEMANA", fill=C_WHITE, font=get_font(24, bold=True))
    
    # Category Filter Pills
    filters = [("TODOS", True), ("AUDIO", False), ("SMARTWATCHES", False), ("GAMING", False), ("ACCESORIOS", False)]
    fx = 50
    for fname, factive in filters:
        bg1 = C_BLUE if factive else C_BG_CARD
        bg2 = C_CYAN if factive else C_BG_CARD_LIGHT
        txt_col = C_WHITE if factive else C_SLATE
        bdr = C_WHITE if factive else C_BORDER
        draw_gradient_rect(im_prod_head, [fx, 790, fx + 90, 818], radius=6, c1=bg1, c2=bg2, border=bdr)
        ImageDraw.Draw(im_prod_head).text((fx + 16, 796), fname, fill=txt_col, font=get_font(11, bold=factive))
        fx += 102
    l_prod_head = pil_to_layer(im_prod_head, "Encabezado_y_Filtros_Productos")
    
    # Product Cards
    products = [
        {
            "tag": "-25% OFERTA",
            "tag_color": C_CORAL,
            "title": "Apex Watch Pro Gen 3",
            "desc": "Pantalla AMOLED Retina, GPS dual & SpO2.",
            "stars": 5,
            "reviews": "(142)",
            "price": "$199.99",
            "old_price": "$249.99",
            "renderer": render_smartwatch
        },
        {
            "tag": "TOP VENTAS",
            "tag_color": C_CYAN,
            "title": "Nova Wave ANC X",
            "desc": "Cancelación híbrida, estuche Qi inalámbrico.",
            "stars": 5,
            "reviews": "(389)",
            "price": "$149.99",
            "old_price": "$189.99",
            "renderer": render_earbuds
        },
        {
            "tag": "NUEVO 2026",
            "tag_color": C_GREEN,
            "title": "CyberMech RGB Pro",
            "desc": "Switches ópticos hotswap, triple conexión.",
            "stars": 5,
            "reviews": "(98)",
            "price": "$119.99",
            "old_price": "$139.99",
            "renderer": render_keyboard
        }
    ]
    
    pw = 285
    pgap = 22
    px_start = 50
    card_layers = []
    
    for idx, p in enumerate(products):
        im_card = new_layer()
        bx = px_start + idx * (pw + pgap)
        by = 840
        bh = 380
        
        # Card Background
        draw_gradient_rect(im_card, [bx, by, bx + pw, by + bh], radius=12, c1=C_BG_CARD, c2=C_BG_CARD_LIGHT, border=C_BORDER, border_w=1)
        
        # Tag Badge
        draw_gradient_rect(im_card, [bx + 14, by + 14, bx + 105, by + 36], radius=4, c1=p["tag_color"], c2=p["tag_color"])
        ImageDraw.Draw(im_card).text((bx + 20, by + 18), p["tag"], fill=C_WHITE, font=get_font(9, bold=True))
        
        # Render Gadget Graphic
        gadget_img = p["renderer"]()
        im_card.paste(gadget_img, (bx + 22, by + 45), gadget_img)
        
        # Text details
        d_c = ImageDraw.Draw(im_card)
        d_c.text((bx + 16, by + 245), p["title"], fill=C_WHITE, font=get_font(16, bold=True))
        d_c.text((bx + 16, by + 268), p["desc"], fill=C_SLATE, font=get_font(11))
        
        # Rating stars
        draw_stars(d_c, bx + 16, by + 290, count=5, size=12)
        d_c.text((bx + 105, by + 289), p["reviews"], fill=C_SLATE, font=get_font(11))
        
        # Pricing
        d_c.text((bx + 16, by + 312), p["price"], fill=C_CYAN, font=get_font(20, bold=True))
        d_c.text((bx + 115, by + 316), p["old_price"], fill=C_DARK_SLATE, font=get_font(13))
        # Strike-through line on old price
        d_c.line([(bx + 113, by + 323), (bx + 165, by + 323)], fill=C_CORAL, width=1)
        
        # Interactive Button: Añadir al carrito
        draw_gradient_rect(im_card, [bx + 16, by + 338, bx + pw - 16, by + 370], radius=6, c1=C_BLUE, c2=C_CYAN, border=C_WHITE, border_w=1)
        ImageDraw.Draw(im_card).text((bx + 85, by + 346), "Añadir al Carrito", fill=C_WHITE, font=get_font(12, bold=True))
        
        l_c = pil_to_layer(im_card, f"Tarjeta_Producto_0{idx+1}_{p['title'].split()[0]}")
        card_layers.append(l_c)
        
    grp_productos = nested_layers.Group(name="04_PRODUCTOS_DESTACADOS", layers=card_layers + [l_prod_head], closed=False)
    
    # ----------------------------------------------------
    # 05_ZONA_INTERACTIVA_PROMO
    # ----------------------------------------------------
    im_promo = new_layer()
    p_x0, p_y0, p_x1, p_y1 = 50, 1250, 950, 1490
    
    # Card Background with vibrant gradient & circuit styling
    draw_gradient_rect(im_promo, [p_x0, p_y0, p_x1, p_y1], radius=16, c1=(12, 35, 75, 255), c2=(6, 18, 42, 255), border=C_CYAN, border_w=2)
    
    # Tech angled decorative lines
    d_promo = ImageDraw.Draw(im_promo)
    for lx in range(p_x0 + 50, p_x1 - 50, 80):
        d_promo.line([(lx, p_y0 + 10), (lx + 40, p_y0 + 50)], fill=(0, 210, 255, 25), width=2)
        d_promo.line([(lx, p_y1 - 50), (lx + 40, p_y1 - 10)], fill=(0, 210, 255, 25), width=2)
        
    # Headline
    d_promo.text((p_x0 + 40, p_y0 + 25), "⚡ ZONA INTERACTIVA: OFERTA FLASH EXCLUSIVA", fill=C_CORAL, font=get_font(12, bold=True))
    d_promo.text((p_x0 + 40, p_y0 + 48), "DESCUENTO DE HASTA 40% EN TU PRIMERA COMPRA", fill=C_WHITE, font=get_font(22, bold=True))
    d_promo.text((p_x0 + 40, p_y0 + 82), "Ingresa tu email para desbloquear tu cupón interactivo. Tiempo restante:", fill=C_SLATE, font=get_font(13))
    
    # Countdown Timer Display Boxes
    time_boxes = [("08", "HORAS"), ("42", "MINUTOS"), ("19", "SEGUNDOS")]
    tx = p_x0 + 40
    ty = p_y0 + 115
    for val, unit in time_boxes:
        draw_gradient_rect(im_promo, [tx, ty, tx + 75, ty + 50], radius=8, c1=(10, 18, 32, 255), c2=(18, 28, 50, 255), border=C_BORDER_BRIGHT, border_w=1)
        ImageDraw.Draw(im_promo).text((tx + 22, ty + 10), val, fill=C_CYAN, font=get_font(20, bold=True))
        ImageDraw.Draw(im_promo).text((tx + 14, ty + 34), unit, fill=C_SLATE, font=get_font(8, bold=True))
        tx += 90
        if unit != "SEGUNDOS":
            d_promo.text((tx - 10, ty + 12), ":", fill=C_CYAN, font=get_font(20, bold=True))
            
    # Interactive Newsletter Form Field & Button
    form_y = p_y0 + 180
    # Input box
    draw_gradient_rect(im_promo, [p_x0 + 40, form_y, p_x0 + 560, form_y + 45], radius=8, c1=(8, 14, 25, 255), c2=(14, 22, 38, 255), border=(56, 189, 248, 160), border_w=1)
    ImageDraw.Draw(im_promo).text((p_x0 + 55, form_y + 14), "tunombre@correo.com", fill=C_SLATE, font=get_font(13))
    # Blinking cursor indicator
    d_promo.line([(p_x0 + 195, form_y + 12), (p_x0 + 195, form_y + 32)], fill=C_CYAN, width=2)
    
    # Action Button (Hover State / Interactive Glow)
    draw_gradient_rect(im_promo, [p_x0 + 580, form_y, p_x0 + 860, form_y + 45], radius=8, c1=C_BLUE, c2=C_CYAN, border=C_WHITE, border_w=1)
    ImageDraw.Draw(im_promo).text((p_x0 + 625, form_y + 14), "CANJEAR CUPÓN AHORA ➔", fill=C_WHITE, font=get_font(13, bold=True))
    
    l_promo = pil_to_layer(im_promo, "Caja_Oferta_Flash_y_Formulario_Interactivo")
    grp_promo = nested_layers.Group(name="05_ZONA_INTERACTIVA_PROMO", layers=[l_promo], closed=False)
    
    # ----------------------------------------------------
    # 06_TESTIMONIOS
    # ----------------------------------------------------
    im_test = new_layer()
    d_test = ImageDraw.Draw(im_test)
    
    d_test.text((50, 1515), "FEEDBACK DE LA COMUNIDAD", fill=C_CYAN, font=get_font(12, bold=True))
    d_test.text((50, 1535), "EXPERIENCIAS REALES DE NUESTROS CLIENTES", fill=C_WHITE, font=get_font(22, bold=True))
    
    testimonials = [
        {
            "name": "Carlos Mendoza",
            "role": "Comprador Verificado • Audio Pro Ultra",
            "quote": "\"Los auriculares llegaron en menos de 24 horas. La cancelación activa de ruido supera a auriculares del doble de precio. La calidad de sonido en juegos y música es insuperable.\""
        },
        {
            "name": "Valentina Rojas",
            "role": "Creadora Digital • Apex Watch Pro",
            "quote": "\"El Apex Watch Pro es perfecto para mi rutina de entrenamiento y producción digital. La pantalla AMOLED se lee con total claridad bajo el sol y la batería dura más de 5 días seguidos.\""
        }
    ]
    
    tw = 438
    t_gap = 24
    for i, t in enumerate(testimonials):
        bx = 50 + i * (tw + t_gap)
        by = 1580
        bh = 135
        # Testimonial card
        draw_gradient_rect(im_test, [bx, by, bx + tw, by + bh], radius=10, c1=C_BG_CARD, c2=C_BG_CARD_LIGHT, border=C_BORDER)
        
        # Avatar circle
        draw_radial_glow(im_test, bx + 36, by + 36, 22, (0, 210, 255, 60))
        d_test.ellipse([bx + 18, by + 18, bx + 54, by + 54], fill=(30, 45, 75, 255), outline=C_CYAN, width=2)
        # Initials
        initials = "".join([part[0] for part in t["name"].split()])
        d_test.text((bx + 26, by + 26), initials, fill=C_WHITE, font=get_font(13, bold=True))
        
        # Name and Role
        d_test.text((bx + 66, by + 20), t["name"], fill=C_WHITE, font=get_font(14, bold=True))
        d_test.text((bx + 66, by + 38), t["role"], fill=C_CYAN, font=get_font(10))
        
        # Stars
        draw_stars(d_test, bx + tw - 95, by + 22, count=5, size=11)
        
        # Quote text
        words = t["quote"].split()
        l1 = " ".join(words[:10])
        l2 = " ".join(words[10:20])
        l3 = " ".join(words[20:])
        d_test.text((bx + 20, by + 68), l1, fill=C_SLATE, font=get_font(11))
        d_test.text((bx + 20, by + 86), l2, fill=C_SLATE, font=get_font(11))
        if l3:
            d_test.text((bx + 20, by + 104), l3, fill=C_SLATE, font=get_font(11))
            
    l_test = pil_to_layer(im_test, "Tarjetas_Testimonios_Comunidad")
    grp_test = nested_layers.Group(name="06_TESTIMONIOS", layers=[l_test], closed=False)
    
    # ----------------------------------------------------
    # 07_FOOTER
    # ----------------------------------------------------
    im_footer = new_layer()
    d_foot = ImageDraw.Draw(im_footer)
    
    # Footer background
    draw_gradient_rect(im_footer, [0, 1740, WIDTH, HEIGHT], radius=0, c1=(7, 10, 18, 255), c2=(4, 6, 12, 255), border=C_BORDER_BRIGHT, border_w=1)
    
    # Logo & About
    draw_tech_logo(im_footer, 50, 1765, size=34)
    d_foot.text((94, 1768), "DBA TECHSTORE", fill=C_WHITE, font=get_font(18, bold=True))
    d_foot.text((50, 1810), "Distribuidor oficial de tecnología, periféricos", fill=C_SLATE, font=get_font(11))
    d_foot.text((50, 1826), "de alta gama y gadgets de última generación.", fill=C_SLATE, font=get_font(11))
    d_foot.text((50, 1848), "📞 +1 (800) 456-7890   •   ✉ contacto@techstore.com", fill=C_CYAN, font=get_font(10, bold=True))
    
    # Navigation Columns
    cols = [
        ("PRODUCTOS", ["Auriculares Studio", "Smartwatches", "Teclados Mecánicos", "Audio Espacial", "Ofertas Flash"], 400),
        ("SOPORTE", ["Centro de Ayuda", "Estado del Pedido", "Políticas de Garantía", "Devoluciones", "Contacto 24/7"], 580),
        ("COMPAÑÍA", ["Sobre Nosotros", "Términos del Servicio", "Privacidad", "Prensa y Blog", "Sustentabilidad"], 760)
    ]
    for c_title, c_links, c_x in cols:
        d_foot.text((c_x, 1768), c_title, fill=C_WHITE, font=get_font(12, bold=True))
        for l_idx, link in enumerate(c_links):
            d_foot.text((c_x, 1795 + l_idx * 18), link, fill=C_SLATE, font=get_font(11))
            
    # Bottom separator line
    d_foot.line([(50, 1915), (950, 1915)], fill=C_BORDER, width=1)
    
    # Payment Badges
    payments = ["VISA", "MASTERCARD", "PAYPAL", "APPLE PAY", "BITCOIN"]
    pay_x = 50
    for p_name in payments:
        draw_gradient_rect(im_footer, [pay_x, 1930, pay_x + 65, 1952], radius=4, c1=(18, 26, 42, 255), c2=(25, 36, 56, 255), border=C_BORDER)
        ImageDraw.Draw(im_footer).text((pay_x + 8, 1935), p_name, fill=C_WHITE, font=get_font(8, bold=True))
        pay_x += 72
        
    # Social Links
    socials = ["INSTAGRAM", "TWITTER / X", "YOUTUBE", "DISCORD"]
    s_x = 620
    for s_name in socials:
        d_foot.text((s_x, 1936), s_name, fill=C_CYAN, font=get_font(9, bold=True))
        s_x += 85
        
    # Copyright
    d_foot.text((50, 1970), "© 2026 DBA TechStore. Todos los derechos reservados. Archivo Mockup PSD 1000x2000 px.", fill=C_SLATE, font=get_font(10))
    d_foot.text((720, 1970), "Diseño Web Profesional con Sectores HTML", fill=C_SLATE, font=get_font(10))
    
    l_footer = pil_to_layer(im_footer, "Contenido_Footer_Completo")
    grp_footer = nested_layers.Group(name="07_FOOTER", layers=[l_footer], closed=False)
    
    # Order of groups from bottom to top:
    # 00_FONDO_GLOBAL, 07_FOOTER, 06_TESTIMONIOS, 05_ZONA_INTERACTIVA_PROMO, 04_PRODUCTOS_DESTACADOS, 03_BENEFICIOS_VECTORES, 02_BANNER_HERO, 01_HEADER
    # In Photoshop group stack, the first in the list appears at the top!
    all_groups = [
        grp_header,
        grp_hero,
        grp_beneficios,
        grp_productos,
        grp_promo,
        grp_test,
        grp_footer,
        grp_bg
    ]
    
    # Also create the composite image
    print("Generating complete composite preview image...")
    comp = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
    comp.paste(im_bg, (0, 0), im_bg)
    comp.paste(im_footer, (0, 0), im_footer)
    comp.paste(im_test, (0, 0), im_test)
    comp.paste(im_promo, (0, 0), im_promo)
    comp.paste(im_prod_head, (0, 0), im_prod_head)
    for cl in card_layers:
        pass # already in im_card pastes below
    # Re-composite product cards onto comp
    for idx, p in enumerate(products):
        bx = px_start + idx * (pw + pgap)
        by = 840
        bh = 380
        draw_gradient_rect(comp, [bx, by, bx + pw, by + bh], radius=12, c1=C_BG_CARD, c2=C_BG_CARD_LIGHT, border=C_BORDER, border_w=1)
        draw_gradient_rect(comp, [bx + 14, by + 14, bx + 105, by + 36], radius=4, c1=p["tag_color"], c2=p["tag_color"])
        ImageDraw.Draw(comp).text((bx + 20, by + 18), p["tag"], fill=C_WHITE, font=get_font(9, bold=True))
        gadget_img = p["renderer"]()
        comp.paste(gadget_img, (bx + 22, by + 45), gadget_img)
        d_c = ImageDraw.Draw(comp)
        d_c.text((bx + 16, by + 245), p["title"], fill=C_WHITE, font=get_font(16, bold=True))
        d_c.text((bx + 16, by + 268), p["desc"], fill=C_SLATE, font=get_font(11))
        draw_stars(d_c, bx + 16, by + 290, count=5, size=12)
        d_c.text((bx + 105, by + 289), p["reviews"], fill=C_SLATE, font=get_font(11))
        d_c.text((bx + 16, by + 312), p["price"], fill=C_CYAN, font=get_font(20, bold=True))
        d_c.text((bx + 115, by + 316), p["old_price"], fill=C_DARK_SLATE, font=get_font(13))
        d_c.line([(bx + 113, by + 323), (bx + 165, by + 323)], fill=C_CORAL, width=1)
        draw_gradient_rect(comp, [bx + 16, by + 338, bx + pw - 16, by + 370], radius=6, c1=C_BLUE, c2=C_CYAN, border=C_WHITE, border_w=1)
        ImageDraw.Draw(comp).text((bx + 85, by + 346), "Añadir al Carrito", fill=C_WHITE, font=get_font(12, bold=True))
        
    comp.paste(im_ben_cards, (0, 0), im_ben_cards)
    comp.paste(im_ben_text, (0, 0), im_ben_text)
    comp.paste(im_ben_icons, (0, 0), im_ben_icons)
    comp.paste(im_b_glow, (0, 0), im_b_glow)
    comp.paste(im_b_gadget, (0, 0), im_b_gadget)
    comp.paste(im_b_text, (0, 0), im_b_text)
    comp.paste(im_b_btn, (0, 0), im_b_btn)
    comp.paste(im_h_bg, (0, 0), im_h_bg)
    comp.paste(im_h_logo, (0, 0), im_h_logo)
    comp.paste(im_h_menu, (0, 0), im_h_menu)
    comp.paste(im_h_act, (0, 0), im_h_act)
    
    preview_path = os.path.join(OUTPUT_DIR, "mockup_preview_1000x2000.png")
    comp.save(preview_path, "PNG")
    print(f"Preview image saved: {preview_path} ({os.path.getsize(preview_path)} bytes)")
    
    print("Writing Photoshop PSD file...")
    psd = nested_layers.nested_layers_to_psd(
        all_groups,
        color_mode=ColorMode.rgb,
        compression=Compression.raw,
        size=(WIDTH, HEIGHT)
    )
    
    psd_path = os.path.join(OUTPUT_DIR, "TechStore_Mockup_1000x2000.psd")
    with open(psd_path, "wb") as f:
        psd.write(f)
    print(f"PSD file saved: {psd_path} ({os.path.getsize(psd_path)} bytes)")

if __name__ == "__main__":
    build_all_layers()
