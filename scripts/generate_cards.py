import os
import math
import html

try:
    from PIL import ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

PALETTES = {
    'AI/ML': {'bg': '49316B', 'text': 'D8B4FE'},
    'WEB PLATFORM': {'bg': '193B63', 'text': '93C5FD'},
    'ALGORITHMS': {'bg': '164B3A', 'text': '6EE7B7'},
    'CREATIVE': {'bg': '55401D', 'text': 'FCD34D'},
}

PROJECTS = [
    {
        'filename': 'HomelanderAI.svg',
        'name': 'HomelanderAI',
        'url': 'https://github.com/Cord1ess/HomelanderAI',
        'type': 'AI/ML',
        'desc': 'Multi-modal AI decision support platform for life, health, and critical-illness underwriting fusing 6 model arms, clinical NLP, and 13 deterministic history rules.',
        'chips': ['Python 3.12', 'FastAPI', 'React 19', 'TypeScript', 'PyTorch', 'BioBERT', 'PostgreSQL 17']
    },
    {
        'filename': 'bn-drug-safety-rag.svg',
        'name': 'bn-drug-safety-rag',
        'url': 'https://github.com/akibmehedi666/bn-drug-safety-rag',
        'type': 'AI/ML',
        'desc': 'Clinical safety verification and hallucination detection system for maternal healthcare in Bengali across 302 drug monographs.',
        'chips': ['Python', 'PyTorch', 'SentenceTransformers', 'Scikit-learn', 'Gemini API']
    },
    {
        'filename': 'RPS-Semi-Arm.svg',
        'name': 'RPS-Semi-Arm',
        'url': 'https://github.com/akibmehedi666/RPS-Semi-Arm',
        'type': 'AI/ML',
        'desc': 'Real-time computer vision system predicting hand gestures from standard laptop webcams via frame differencing and a custom 115K-parameter CNN with ~0.60ms CPU inference.',
        'chips': ['Python', 'PyTorch', 'OpenCV', 'NumPy', 'Edge AI']
    },
    {
        'filename': 'CompeteX.svg',
        'name': 'CompeteX',
        'url': 'https://github.com/akibmehedi666/CompeteX',
        'type': 'WEB PLATFORM',
        'desc': 'Interactive web portal for university competitions and tech hackathons featuring Leaflet campus mapping, live leaderboards, and automated matchmaking.',
        'chips': ['Next.js 16', 'React 19', 'TypeScript', 'Leaflet', 'Tailwind CSS']
    },
    {
        'filename': 'OPERATION-ME.svg',
        'name': 'OPERATION-ME',
        'url': 'https://github.com/akibmehedi666/OPERATION-ME',
        'type': 'WEB PLATFORM',
        'desc': 'Tactical mission control, academic planner, and CP tracker with offline-first storage and Supabase PostgreSQL Row Level Security (RLS).',
        'chips': ['Next.js 14', 'TypeScript', 'Supabase (PostgreSQL & Auth)', 'Playwright', 'Vitest']
    },
    {
        'filename': 'Eureka.svg',
        'name': 'Eureka',
        'url': 'https://github.com/akibmehedi666/Eureka',
        'type': 'WEB PLATFORM',
        'desc': 'Collaborative academic research paper library and literature review notebook featuring automated arXiv/DOI metadata extraction and PDF ingestion.',
        'chips': ['Next.js 15', 'React 19', 'TypeScript', 'Prisma ORM', 'Supabase']
    },
    {
        'filename': 'uiu-routine-builder.svg',
        'name': 'uiu-routine-builder',
        'url': 'https://github.com/akibmehedi666/uiu-routine-builder',
        'type': 'ALGORITHMS',
        'desc': 'High-performance academic schedule generator executing a 64-bit bitmask backtracking algorithm inside a dedicated background Web Worker at 60 FPS.',
        'chips': ['Next.js 14', 'TypeScript', 'Web Workers', 'Tailwind CSS', 'Vitest']
    },
    {
        'filename': 'Team-Karasuno.svg',
        'name': 'Team-Karasuno',
        'url': 'https://github.com/akibmehedi666/Team-Karasuno',
        'type': 'CREATIVE',
        'desc': 'Interactive generative art and ambient audio experience running a 500-particle Perlin noise flow field synchronized with Tone.js audio synthesis.',
        'chips': ['Next.js 16', 'React 19', 'p5.js', 'Tone.js', 'Tailwind CSS']
    }
]

def get_font(size, bold=False):
    if HAS_PIL:
        fontname = 'segoeuib.ttf' if bold else 'segoeui.ttf'
        try:
            return ImageFont.truetype(fontname, size)
        except Exception:
            try:
                fontname = 'arialbd.ttf' if bold else 'arial.ttf'
                return ImageFont.truetype(fontname, size)
            except Exception:
                pass
    return None

def text_length(text, size, bold=False):
    f = get_font(size, bold)
    if f:
        return f.getlength(text)
    # Fallback estimate
    char_w = 0.58 if bold else 0.52
    return len(text) * size * char_w

def wrap_text(text, max_width, initial_size=12):
    size = initial_size
    while size >= 9:
        words = text.split()
        lines = []
        curr = []
        overflow = False
        for w in words:
            candidate = ' '.join(curr + [w])
            w_len = text_length(candidate, size, bold=False)
            if w_len <= max_width:
                curr.append(w)
            else:
                if curr:
                    lines.append(' '.join(curr))
                    curr = [w]
                else:
                    # Single word overflows max_width
                    overflow = True
                    break
        if curr:
            lines.append(' '.join(curr))
            
        if not overflow and len(lines) <= 4:
            # Check every line fits
            fits = all(text_length(line, size, bold=False) <= max_width for line in lines)
            if fits:
                return lines, size
        size -= 1
    return lines, size

def wrap_chips(chips, max_width, font_size=11):
    rows = []
    curr_row = []
    curr_w = 0
    for c in chips:
        w = math.ceil(text_length(c, font_size, bold=False) + 16)
        spacing = 6 if curr_row else 0
        if curr_w + w + spacing <= max_width:
            curr_row.append((c, w))
            curr_w += w + spacing
        else:
            if curr_row:
                rows.append(curr_row)
            curr_row = [(c, w)]
            curr_w = w
    if curr_row:
        rows.append(curr_row)
    return rows

def generate_card_svg(project):
    name = project['name']
    type_name = project['type']
    desc = project['desc']
    chips = project['chips']
    
    pal = PALETTES[type_name]
    tag_bg = pal['bg']
    tag_text = pal['text']
    stripe_color = tag_text  # user instruction: use text color for the stripe so it is visible on the dark card
    
    # Card size
    card_w = 400
    card_h = 200
    rx = 10
    
    # Top row
    type_tag_text_w = text_length(type_name, 10, bold=True) + (len(type_name) - 1) * 0.5
    tag_w = math.ceil(type_tag_text_w + 16)
    tag_h = 22
    tag_x = card_w - 18 - tag_w
    tag_y = 16
    
    # Description lines
    desc_max_w = card_w - 20 - 18 # 362px
    desc_lines, desc_size = wrap_text(desc, desc_max_w, initial_size=12)
    
    # Chips layout
    chip_rows = wrap_chips(chips, desc_max_w, font_size=11)
    
    # Calculate chip y positions
    chip_h = 22
    chip_gap = 6
    if len(chip_rows) == 2:
        row_y = [card_h - 14 - (chip_h * 2 + chip_gap), card_h - 14 - chip_h]
    else:
        row_y = [card_h - 14 - chip_h]
        
    # Build SVG XML
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{card_w}" height="{card_h}" viewBox="0 0 {card_w} {card_h}">',
        '  <defs>',
        f'    <clipPath id="card-clip">',
        f'      <rect width="{card_w}" height="{card_h}" rx="{rx}"/>',
        '    </clipPath>',
        '  </defs>',
        '  <g clip-path="url(#card-clip)">',
        f'    <rect width="{card_w}" height="{card_h}" fill="#161b22"/>',
        f'    <rect x="0" y="0" width="4" height="{card_h}" fill="#{stripe_color}"/>',
        '  </g>',
        f'  <rect x="0.5" y="0.5" width="{card_w - 1}" height="{card_h - 1}" rx="{rx}" fill="none" stroke="#30363d" stroke-width="1"/>',
        f'  <text x="20" y="32" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="16" font-weight="bold" fill="#22D3EE">{html.escape(name)}</text>',
        f'  <rect x="{tag_x}" y="{tag_y}" width="{tag_w}" height="{tag_h}" rx="6" fill="#{tag_bg}" stroke="#{tag_text}" stroke-width="1" stroke-opacity="0.35"/>',
        f'  <text x="{tag_x + tag_w / 2:.1f}" y="{tag_y + tag_h / 2:.1f}" text-anchor="middle" dominant-baseline="central" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="10" font-weight="bold" letter-spacing="0.5" fill="#{tag_text}">{html.escape(type_name)}</text>'
    ]
    
    # Description lines
    line_spacing = 18 if desc_size >= 12 else 16
    start_y = 56 + (desc_size - 10)
    for i, line in enumerate(desc_lines):
        ly = start_y + (i * line_spacing)
        svg_parts.append(f'  <text x="20" y="{ly}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="{desc_size}" fill="#c9d1d9">{html.escape(line)}</text>')
        
    # Chips
    for r_idx, row in enumerate(chip_rows):
        cy = row_y[r_idx]
        cx = 20
        for c_text, cw in row:
            svg_parts.append(f'  <rect x="{cx}" y="{cy}" width="{cw}" height="{chip_h}" rx="4" fill="#21262d" stroke="#30363d" stroke-width="1"/>')
            svg_parts.append(f'  <text x="{cx + cw / 2:.1f}" y="{cy + chip_h / 2:.1f}" text-anchor="middle" dominant-baseline="central" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="11" fill="#8b949e">{html.escape(c_text)}</text>')
            cx += cw + chip_gap
            
    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    out_dir = os.path.join(repo_root, 'assets', 'cards')
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"Generating project cards into {out_dir}")
    for p in PROJECTS:
        svg_content = generate_card_svg(p)
        filepath = os.path.join(out_dir, p['filename'])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"Generated {p['filename']}")

if __name__ == '__main__':
    main()
