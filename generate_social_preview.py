"""
Generate a custom social preview image for the Enterprise AI Agent repository.
Creates a 1280x640px image suitable for GitHub social previews.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Constants
WIDTH = 1280
HEIGHT = 640
OUTPUT_PATH = ".github/social-preview.png"

# Color scheme - modern, professional
BACKGROUND_COLOR = "#0A0E27"  # Dark blue
PRIMARY_COLOR = "#00D4FF"     # Cyan/blue
ACCENT_COLOR = "#FFFFFF"       # White
TEXT_SECONDARY = "#B0B8C3"     # Light gray

def create_social_preview():
    """Create the social preview image"""
    
    # Create image with background
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Try to use system fonts, fallback to default if not available
    try:
        # Title font - large and bold
        title_font = ImageFont.truetype("arial.ttf", 72)
        subtitle_font = ImageFont.truetype("arial.ttf", 32)
        tag_font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            title_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 72)
            subtitle_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 32)
            tag_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            tag_font = ImageFont.load_default()
    
    # Draw decorative elements
    # Top gradient line
    for i in range(50):
        alpha = 255 - (i * 5)
        draw.rectangle([(0, i), (WIDTH, i + 1)], fill=(0, 212, 255, min(alpha, 255)))
    
    # Bottom accent line
    draw.rectangle([(0, HEIGHT - 8), (WIDTH, HEIGHT)], fill=PRIMARY_COLOR)
    
    # Main title
    title = "Enterprise AI Agent"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    title_x = (WIDTH - title_width) // 2
    title_y = 180
    draw.text((title_x, title_y), title, fill=ACCENT_COLOR, font=title_font)
    
    # Subtitle
    subtitle = "Production-Grade RAG • Tool Integration • Autonomous Reasoning"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (WIDTH - subtitle_width) // 2
    subtitle_y = title_y + title_height + 30
    draw.text((subtitle_x, subtitle_y), subtitle, fill=TEXT_SECONDARY, font=subtitle_font)
    
    # Technology tags (bottom section)
    tags = ["RAG", "LangChain", "ChromaDB", "Streamlit", "FastAPI", "Docker"]
    tag_start_y = 420
    tag_spacing = 140
    start_x = (WIDTH - (len(tags) * tag_spacing - 20)) // 2
    
    for i, tag in enumerate(tags):
        tag_x = start_x + (i * tag_spacing)
        tag_y = tag_start_y
        
        # Draw tag background
        tag_bbox = draw.textbbox((0, 0), tag, font=tag_font)
        tag_width = tag_bbox[2] - tag_bbox[0] + 40
        tag_height = tag_bbox[3] - tag_bbox[1] + 20
        
        # Rounded rectangle effect (simplified)
        padding = 10
        draw.rectangle(
            [(tag_x - padding, tag_y - padding), 
             (tag_x + tag_width - padding, tag_y + tag_height - padding)],
            fill=PRIMARY_COLOR,
            outline=None
        )
        
        # Tag text
        text_x = tag_x + (tag_width - (tag_bbox[2] - tag_bbox[0])) // 2 - padding
        text_y = tag_y + (tag_height - (tag_bbox[3] - tag_bbox[1])) // 2 - padding
        draw.text((text_x, text_y), tag, fill=BACKGROUND_COLOR, font=tag_font)
    
    # Create .github directory if it doesn't exist
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Save image
    img.save(OUTPUT_PATH)
    print(f"✓ Social preview image created: {OUTPUT_PATH}")
    print(f"  Dimensions: {WIDTH}x{HEIGHT}px")
    print(f"  Ready to upload to GitHub!")

if __name__ == "__main__":
    create_social_preview()

