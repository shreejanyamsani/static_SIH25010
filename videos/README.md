# Videos Directory

This directory contains tutorial videos for the AR/VR learning module.

## Required Video Files:

### `soil_prep_demo.mp4`
- **Purpose**: Soil preparation tutorial for farmers
- **Duration**: 5-10 minutes recommended
- **Content**: Step-by-step soil preparation techniques
- **Format**: MP4 (H.264 codec recommended for web compatibility)
- **Resolution**: 720p or 1080p
- **Size**: Keep under 50MB for faster loading

### Additional Video Files (Optional):
- `seed_sowing_demo.mp4` - Seed sowing techniques
- `irrigation_demo.mp4` - Proper irrigation methods
- `pest_identification.mp4` - Common pest identification
- `fertilizer_application.mp4` - Fertilizer application techniques
- `harvesting_demo.mp4` - Harvesting best practices

## Video File Placeholder Structure:
```
videos/
├── soil_prep_demo.mp4          # Main demo video (required)
├── seed_sowing_demo.mp4        # Optional
├── irrigation_demo.mp4         # Optional
├── pest_identification.mp4     # Optional
├── fertilizer_application.mp4  # Optional
├── harvesting_demo.mp4         # Optional
└── README.md                   # This file
```

## Usage in Application:
Videos are played through the AR/VR learning module (`ar_module.py`) using Streamlit's `st.video()` component.

## File Preparation Notes:
1. **Format**: Use MP4 with H.264 codec for best compatibility
2. **Compression**: Balance quality vs file size for web streaming
3. **Captions**: Consider adding subtitles for accessibility
4. **Thumbnail**: First frame should be representative of content
5. **Audio**: Clear narration with background music (optional)

## Sample Video Content Outline for `soil_prep_demo.mp4`:
1. **Introduction** (30 seconds)
   - Welcome and overview
   
2. **Soil Testing** (2 minutes)
   - pH testing demonstration
   - Nutrient level checking
   
3. **Land Preparation** (3 minutes)
   - Plowing techniques
   - Leveling methods
   
4. **Organic Matter Addition** (2 minutes)
   - Compost application
   - Green manure incorporation
   
5. **Final Preparation** (1.5 minutes)
   - Final leveling
   - Ready-to-sow condition check
   
6. **Conclusion** (30 seconds)
   - Summary and next steps

## Placeholder Video Creation:
For development/testing purposes, you can:
1. Create a simple video with text slides
2. Use screen recording tools to create demo content
3. Download royalty-free agricultural videos from platforms like Pixabay or Pexels
4. Create animated slides using tools like Canva or PowerPoint