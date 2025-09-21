# Assets Directory

This directory contains icons, images, and other static assets for the agricultural advisory application.

## Directory Structure:
```
assets/
├── icons/
│   ├── crop_advisory.png        # 🌾 Crop advisory icon
│   ├── fertilizer.png           # 🧪 Fertilizer recommendation icon
│   ├── pest_detection.png       # 🐛 Pest detection icon
│   ├── weather.png              # 🌤️ Weather alerts icon
│   ├── market.png               # 📊 Market prices icon
│   ├── community.png            # 👥 Community alerts icon
│   ├── ar_vr.png               # 🥽 AR/VR learning icon
│   └── app_logo.png            # Main app logo
├── images/
│   ├── backgrounds/
│   │   ├── farm_landscape.jpg   # App background
│   │   └── field_sunset.jpg     # Alternative background
│   ├── crops/
│   │   ├── rice.jpg
│   │   ├── wheat.jpg
│   │   ├── maize.jpg
│   │   ├── cotton.jpg
│   │   └── vegetables.jpg
│   ├── pests/
│   │   ├── aphids.jpg
│   │   ├── stem_borer.jpg
│   │   ├── whitefly.jpg
│   │   └── caterpillar.jpg
│   └── soil_types/
│       ├── clay_soil.jpg
│       ├── sandy_soil.jpg
│       ├── loamy_soil.jpg
│       └── black_soil.jpg
├── sample_uploads/
│   ├── leaf_sample_1.jpg        # Sample pest detection images
│   ├── leaf_sample_2.jpg
│   ├── crop_disease_1.jpg
│   └── healthy_crop.jpg
└── README.md                    # This file
```

## Icon Requirements:
- **Format**: PNG with transparent background
- **Size**: 64x64px for sidebar icons, 128x128px for headers
- **Style**: Consistent flat design or outline style
- **Colors**: Earth tones (greens, browns, blues) for agricultural theme

## Image Requirements:
- **Format**: JPG for photos, PNG for graphics
- **Size**: Max 1920px width for backgrounds, 512px for thumbnails
- **Quality**: High quality but optimized for web (< 1MB per image)
- **Content**: Agricultural, farming, and rural themes

## Icon Sources (Free/Royalty-free):
1. **Feather Icons**: https://feathericons.com/
2. **Heroicons**: https://heroicons.com/
3. **Lucide Icons**: https://lucide.dev/
4. **Font Awesome**: https://fontawesome.com/
5. **Flaticon**: https://www.flaticon.com/

## Image Sources (Free/Royalty-free):
1. **Unsplash**: https://unsplash.com/ (search: agriculture, farming, crops)
2. **Pexels**: https://www.pexels.com/ (search: farm, soil, plants)
3. **Pixabay**: https://pixabay.com/ (search: agriculture, farming)
4. **Freepik**: https://www.freepik.com/ (agricultural illustrations)

## Sample Asset Creation Guide:

### App Logo (`app_logo.png`):
- Combine agriculture symbols (leaf, tractor, sun)
- Include app name if desired
- Use green/brown color palette
- 256x256px minimum resolution

### Module Icons:
- **Crop Advisory**: Wheat/grain icon
- **Fertilizer**: Chemical beaker or soil with nutrients
- **Pest Detection**: Bug or magnifying glass with leaf
- **Weather**: Sun/cloud/rain combination
- **Market**: Graph/chart or money symbol
- **Community**: People or speech bubble
- **AR/VR**: VR headset or play button

### Crop Images:
- High-quality photos of healthy crops
- Clear, well-lit images
- Different growth stages if possible
- Consistent lighting and background

### Pest/Disease Images:
- Clear symptoms visible
- Good contrast for identification
- Multiple angles if available
- Before/after treatment comparisons

## Color Palette Recommendations:
- **Primary Green**: #2E7D32 (agricultural green)
- **Secondary Brown**: #5D4037 (soil brown)
- **Accent Blue**: #1976D2 (sky blue)
- **Warning Orange**: #F57C00 (alert color)
- **Success Green**: #388E3C (healthy crop)
- **Background**: #F1F8E9 (light green tint)

## Usage in Streamlit:
```python
# Load and display images
from PIL import Image
import streamlit as st

# Load icon
icon = Image.open("assets/icons/crop_advisory.png")
st.image(icon, width=64)

# Load background
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_image}");
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
```

## File Naming Convention:
- Use lowercase with underscores
- Be descriptive but concise
- Include category prefix where appropriate
- Examples: `icon_crop.png`, `bg_farm_sunset.jpg`, `pest_aphids.jpg`