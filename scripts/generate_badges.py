import os
import math

try:
    from PIL import ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

PALETTES = {
    "PROGRAMMING": {"bg": "164B3A", "text": "6EE7B7"},
    "HACKATHON": {"bg": "193B63", "text": "93C5FD"},
    "ROBOTICS": {"bg": "49316B", "text": "D8B4FE"},
    "PROJECT SHOWS": {"bg": "55401D", "text": "FCD34D"},
    "CYBERSECURITY": {"bg": "633044", "text": "FDA4AF"},
}

CATEGORY_BADGES = [
    ("category-programming.svg", "PROGRAMMING", "PROGRAMMING"),
    ("category-hackathon.svg", "HACKATHON", "HACKATHON"),
    ("category-robotics.svg", "ROBOTICS", "ROBOTICS"),
    ("category-project-shows.svg", "PROJECT SHOWS", "PROJECT SHOWS"),
    ("category-cybersecurity.svg", "CYBERSECURITY", "CYBERSECURITY"),
]

RESULT_BADGES = [
    ("result-1st-runner-up-robotics.svg", "1ST RUNNER UP", "ROBOTICS"),
    ("result-top10-robotics.svg", "TOP 10", "ROBOTICS"),
    ("result-top15-robotics.svg", "TOP 15", "ROBOTICS"),
    ("result-top30-hackathon.svg", "TOP 30", "HACKATHON"),
    ("result-onsite-programming.svg", "ONSITE", "PROGRAMMING"),
    ("result-3rd-project-shows.svg", "3RD", "PROJECT SHOWS"),
    ("result-4th-project-shows.svg", "4TH", "PROJECT SHOWS"),
    ("result-10th-cybersecurity.svg", "10TH", "CYBERSECURITY"),
]

def get_text_width(text, font_size):
    if HAS_PIL:
        for fontname in ["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"]:
            try:
                font = ImageFont.truetype(fontname, font_size)
                base_len = font.getlength(text)
                letter_spacing = (len(text) - 1) * 0.5
                return base_len + letter_spacing
            except Exception:
                continue
    # Accurate fallback based on Segoe UI Bold metrics
    char_widths_12 = {
        ' ': 4.0, '0': 7.5, '1': 6.0, '3': 7.5, '4': 7.5, '5': 7.5,
        'A': 8.5, 'B': 8.0, 'C': 8.5, 'D': 8.5, 'E': 7.5, 'G': 9.0,
        'H': 8.5, 'I': 3.5, 'K': 8.0, 'M': 10.5, 'N': 8.5, 'O': 9.0,
        'P': 8.0, 'R': 8.0, 'S': 7.5, 'T': 7.5, 'U': 8.5, 'W': 11.5, 'Y': 7.5
    }
    ratio = font_size / 12.0
    base_len = sum(char_widths_12.get(c, 8.0) * ratio for c in text)
    letter_spacing = (len(text) - 1) * 0.5
    return base_len + letter_spacing

def generate_svg(text, palette_name, height, font_size, rx=6, padding=12):
    palette = PALETTES[palette_name]
    bg = palette["bg"]
    text_color = palette["text"]
    text_width = get_text_width(text, font_size)
    total_width = math.ceil(text_width + (padding * 2))
    
    rect_w = total_width - 1
    rect_h = height - 1
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{height}" viewBox="0 0 {total_width} {height}">
  <rect x="0.5" y="0.5" width="{rect_w}" height="{rect_h}" rx="{rx}" fill="#{bg}" stroke="#{text_color}" stroke-width="1" stroke-opacity="0.35"/>
  <text x="50%" y="50%" text-anchor="middle" dominant-baseline="central" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="{font_size}" font-weight="bold" letter-spacing="0.5" fill="#{text_color}">{text}</text>
</svg>"""
    return svg, total_width

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(repo_root, "assets", "badges")
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"Generating badges into {out_dir}")
    
    print("\n-- Category Badges (h=26, font=12) --")
    for filename, text, pal in CATEGORY_BADGES:
        svg_content, w = generate_svg(text, pal, height=26, font_size=12, rx=6, padding=12)
        filepath = os.path.join(out_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Created {filename} (width={w}, height=26)")
        
    print("\n-- Result Badges (h=30, font=13) --")
    for filename, text, pal in RESULT_BADGES:
        svg_content, w = generate_svg(text, pal, height=30, font_size=13, rx=6, padding=12)
        filepath = os.path.join(out_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Created {filename} (width={w}, height=30)")

if __name__ == "__main__":
    main()
