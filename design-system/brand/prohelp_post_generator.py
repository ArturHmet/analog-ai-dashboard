#!/usr/bin/env python3
"""
ProHelp Storyboard Post Generator
Adapted from Master Prompt — cinematic storyboard for ProHelp service marketplace.
Stored on server: 195.201.171.95 /opt/prohelp/workspace/brand/

Usage:
  python3 prohelp_post_generator.py --type provider --service plumber --name "Marco"
  python3 prohelp_post_generator.py --type customer --service cleaning --setting apartment
  python3 prohelp_post_generator.py --batch  # generates all 8 service categories
"""

import argparse, json, datetime, os, pathlib

_SERVER_PATH = pathlib.Path("/opt/prohelp/workspace/brand/generated_prompts")
_LOCAL_PATH  = pathlib.Path(__file__).parent.parent / "brand" / "generated_prompts"
OUTPUT_DIR   = _SERVER_PATH if _SERVER_PATH.parent.parent.exists() else _LOCAL_PATH
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── ProHelp Brand Constants ───────────────────────────────────────────────
BRAND = {
    "primary_dark":  "#371F2C",   # Logo plum — dominant dark ink
    "gold":          "#D97706",   # CTA / accent / ratings
    "white":         "#FFFFFF",
    "bg_paper":      "beige parchment",   # storyboard bg per master prompt
    "tagline":       "YOUR PROFESSIONAL ASSISTANT",
    "name":          "PRO HELP",
}

# ─── ProHelp service categories ────────────────────────────────────────────
SERVICES = {
    "plumber":     {"emoji": "🔧", "props": "pipe wrench / plumber's tape / toolbox", "mood": "reliable, expert, calm", "locations": "apartment bathroom / burst pipe scene / kitchen under-sink"},
    "electrician": {"emoji": "⚡", "props": "voltage tester / cable reel / helmet", "mood": "precise, safety-focused, professional", "locations": "fuse box panel / construction site / smart home setup"},
    "cleaner":     {"emoji": "🧹", "props": "mop / eco spray bottle / microfiber cloth", "mood": "energetic, thorough, cheerful", "locations": "luxury apartment / office space / Maltese balcony terrace"},
    "tutor":       {"emoji": "📚", "props": "tablet / textbooks / whiteboard marker", "mood": "inspiring, patient, knowledgeable", "locations": "home study room / café / online video call setup"},
    "chef":        {"emoji": "🍳", "props": "chef's knife / apron / spice rack", "mood": "creative, passionate, artisan", "locations": "home kitchen / open-air terrace / meal-prep studio"},
    "mover":       {"emoji": "📦", "props": "moving boxes / dolly cart / tape gun", "mood": "strong, organized, efficient", "locations": "apartment hallway / moving truck / new home entrance"},
    "gardener":    {"emoji": "🌿", "props": "pruning shears / watering can / gloves", "mood": "nurturing, outdoorsy, zen", "locations": "Maltese garden / rooftop terrace / private villa grounds"},
    "nanny":       {"emoji": "👶", "props": "storybook / playmat / backpack", "mood": "warm, playful, trustworthy", "locations": "children's playroom / park / kitchen baking together"},
}

# ─── Master Prompt Adapted for ProHelp ─────────────────────────────────────
PROHELP_MASTER_PROMPT = """
Create a highly detailed cinematic storyboard poster in a 4:5 vertical ratio, designed like a premium editorial character sheet and service marketplace campaign board. Use a clean beige paper background with thin dark grid lines, deep plum (#371F2C) title bars, and a refined urban-editorial aesthetic that blends film production storyboard with professional service advertising. The composition must follow this exact layout: a large vertical provider profile panel on the left, a multi-panel storyboard sequence on the right showing the service delivery journey, and a bottom information strip spanning the full width. Keep the design polished, balanced, and highly readable, with strong visual hierarchy, realistic lighting, and consistent character design across all panels. Incorporate the ProHelp brand identity: wordmark "PRO HELP" with tagline "YOUR PROFESSIONAL ASSISTANT" in a clean monolinear style.

LEFT PANEL: Show the main service provider in a confident, professional hero pose. At the top, place the stylized ProHelp wordmark "PRO HELP" in bold monolinear all-caps typography, with "YOUR PROFESSIONAL ASSISTANT" as a smaller spaced tagline beneath it. Below the branding, show a full-body or near full-body image of the provider in their work uniform, holding their signature tool or prop. Add a structured profile card with labeled fields: Name, Service, Experience (years), Rating (★★★★★), Location (Malta), Specialty, Quote, and Bio. Typography should feel hand-drawn bold meets editorial clean — confident, approachable, premium.

RIGHT SIDE: Create {num_shots} storyboard frames in a clean grid. Each frame has a deep plum (#371F2C) header bar with a numbered shot title. Every frame shows the same provider in a different action beat of their service delivery — from arrival → assessment → work in progress → problem solved → client interaction → finished result → satisfied client. Clear camera energy and scene progression throughout. Under each frame, include three small text boxes labeled Camera/Movement, Sound, and ProHelp App (showing the in-app booking/rating moment where relevant). The shots should feel like a real production storyboard: dynamic, expressive, and telling a complete service story.

BOTTOM STRIP: Three sections across the full width:
1. Uniform & Gear — small thumbnail cutouts of key tools, uniform items, safety equipment, and ProHelp-branded elements (app on phone, branded bag/vest)
2. Skills & Trust — bullet list of 5-6 key professional traits and verified credentials (background check ✓, licensed ✓, rated 4.9★ ✓)
3. Service Areas & Conditions — mini thumbnails of 3 Malta locations/settings with brief environment notes (indoor / outdoor / emergency / standard)

STYLE DIRECTION: Cinematic service advertisement, premium editorial storyboard, urban professional aesthetic, natural skin texture, realistic proportions, dramatic but clean lighting. Color palette anchored in deep plum (#371F2C) headers and gold (#D97706) accent highlights on ratings, badges, and CTA elements. High detail, sharp composition, professional print-ready finish. Make it look like a campaign board for a high-end staffing or gig-economy brand.

IMPORTANT LAYOUT RULES: Preserve the overall structure — dominant left provider profile panel, storyboard grid on right, footer band at bottom. The entire board should feel like a single unified art board for ProHelp's marketing team, not separate random panels. Include the ProHelp logo wordmark prominently in the top-left of the left panel.

FILL-IN TEMPLATE VALUES:
Subject: {provider_name} — {service_type} professional
Theme: {theme}
Setting: {setting} (Malta-based)
Hero prop: {hero_prop}
Mood: {mood}
Number of storyboard shots: {num_shots}
Output format: 4:5 vertical

NEGATIVE CONSTRAINTS: Do not make it look like a simple comic page or random collage. Avoid clutter, distorted anatomy, unreadable text, inconsistent character design across panels, or generic stock-photo aesthetics. Every panel must feel intentional, branded, and editorial. The character must look like the same real person across all panels. Do not use blue as a dominant color — plum (#371F2C) and gold (#D97706) are the brand anchors.
""".strip()

# ─── Generator ─────────────────────────────────────────────────────────────
def generate_prompt(service: str, provider_name: str = None, setting: str = None, num_shots: int = 7) -> dict:
    svc = SERVICES.get(service, SERVICES["plumber"])
    name = provider_name or f"Marco the {service.title()}"
    loc = setting or svc["locations"].split("/")[0].strip()
    theme = f"professional local services / urban Malta / trust & reliability"
    
    filled = PROHELP_MASTER_PROMPT.format(
        provider_name=name,
        service_type=service,
        theme=theme,
        setting=loc,
        hero_prop=svc["props"].split("/")[0].strip(),
        mood=svc["mood"],
        num_shots=num_shots,
    )
    
    return {
        "prompt": filled,
        "service": service,
        "provider_name": name,
        "setting": loc,
        "num_shots": num_shots,
        "brand_colors": BRAND,
        "generated_at": datetime.datetime.now().isoformat(),
        "output_format": "4:5 vertical",
        "platform": "Instagram / LinkedIn / ProHelp blog",
    }

def save_prompt(data: dict) -> str:
    slug = data["service"].replace(" ", "_")
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    fname = OUTPUT_DIR / f"prohelp_post_{slug}_{ts}.json"
    with open(fname, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    # Also save plain text version for direct copy-paste into image generators
    txt_fname = OUTPUT_DIR / f"prohelp_post_{slug}_{ts}.txt"
    txt_fname.write_text(data["prompt"])
    return str(fname)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ProHelp Storyboard Post Generator")
    parser.add_argument("--service", default="plumber", choices=list(SERVICES.keys()))
    parser.add_argument("--name", default=None)
    parser.add_argument("--setting", default=None)
    parser.add_argument("--shots", type=int, default=7)
    parser.add_argument("--batch", action="store_true", help="Generate prompts for all services")
    args = parser.parse_args()
    
    if args.batch:
        print(f"Generating prompts for all {len(SERVICES)} service categories...")
        for svc_key in SERVICES:
            data = generate_prompt(svc_key, num_shots=args.shots)
            path = save_prompt(data)
            print(f"  ✓ {svc_key:12s} → {path}")
        print(f"\nAll prompts saved to {OUTPUT_DIR}")
    else:
        data = generate_prompt(args.service, args.name, args.setting, args.shots)
        path = save_prompt(data)
        print(f"✓ Generated: {path}")
        print("\n" + "─"*60)
        print(data["prompt"])
        print("─"*60)
