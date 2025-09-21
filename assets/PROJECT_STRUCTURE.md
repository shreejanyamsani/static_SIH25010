# 🌾 Agricultural Advisory Application - Complete Project Structure

## 📁 Directory Layout
```
agricultural-advisory-app/
├── app.py                          # Main Streamlit application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── PROJECT_STRUCTURE.md            # This file
├── .gitignore                      # Git ignore rules
├── modules/                        # Application modules
│   ├── __init__.py
│   ├── crop_advisory.py            # Crop recommendation module
│   ├── fertilizer_recommendation.py # Fertilizer suggestion module
│   ├── pest_detection.py           # Pest and disease detection
│   ├── weather_alerts.py           # Weather monitoring and alerts
│   ├── market_price.py             # Market price analysis
│   ├── community_alerts.py         # Community alert sharing
│   └── ar_module.py                # AR/VR learning demonstrations
├── data/                           # CSV datasets
│   ├── soil_health.csv             # Soil and fertilizer data
│   ├── crop_requirements.csv       # Crop growing requirements
│   ├── pest_disease_dataset.csv    # Pest and disease information
│   ├── weather_data.csv            # Weather forecast data
│   ├── market_prices.csv           # Market price trends
│   └── community_alerts.csv        # User-submitted alerts (auto-generated)
├── videos/                         # Tutorial videos
│   ├── soil_prep_demo.mp4          # Main demo video
│   ├── seed_sowing_demo.mp4        # Optional additional videos
│   ├── irrigation_demo.mp4
│   ├── pest_identification.mp4
│   ├── fertilizer_application.mp4
│   ├── harvesting_demo.mp4
│   └── README.md                   # Video requirements guide
├── assets/                         # Static assets
│   ├── icons/                      # Application icons
│   │   ├── crop_advisory.png
│   │   ├── fertilizer.png
│   │   ├── pest_detection.png
│   │   ├── weather.png
│   │   ├── market.png
│   │   ├── community.png
│   │   ├── ar_vr.png
│   │   └── app_logo.png
│   ├── images/                     # Application images
│   │   ├── backgrounds/
│   │   │   ├── farm_landscape.jpg
│   │   │   └── field_sunset.jpg
│   │   ├── crops/
│   │   │   ├── rice.jpg
│   │   │   ├── wheat.jpg
│   │   │   ├── maize.jpg
│   │   │   ├── cotton.jpg
│   │   │   └── vegetables.jpg
│   │   ├── pests/
│   │   │   ├── aphids.jpg
│   │   │   ├── stem_borer.jpg
│   │   │   ├── whitefly.jpg
│   │   │   └── caterpillar.jpg
│   │   └── soil_types/
│   │       ├── clay_soil.jpg
│   │       ├── sandy_soil.jpg
│   │       ├── loamy_soil.jpg
│   │       └── black_soil.jpg
│   ├── sample_uploads/             # Sample files for testing
│   │   ├── leaf_sample_1.jpg
│   │   ├── leaf_sample_2.jpg
│   │   ├── crop_disease_1.jpg
│   │   └── healthy_crop.jpg
│   └── README.md                   # Assets guide
└── utils/                          # Utility functions (optional)
    ├── __init__.py
    ├── data_loader.py              # CSV data loading functions
    ├── image_processing.py         # Image handling utilities
    └── helpers.py                  # Common helper functions
```

## 📋 File Descriptions

### Core Application Files
- **`app.py`**: Main Streamlit application with navigation sidebar
- **`requirements.txt`**: Python package dependencies
- **`README.md`**: Project setup and usage instructions

### Module Files (`modules/`)
Each module contains a `run()` function that handles its specific functionality:

1. **`crop_advisory.py`**: 
   - Input: Soil type, season selection
   - Output: Recommended crops from `crop_requirements.csv`

2. **`fertilizer_recommendation.py`**: 
   - Input: Soil nutrient levels (N, P, K, pH)
   - Output: Fertilizer recommendations from `soil_health.csv`

3. **`pest_detection.py`**: 
   - Input: Image upload
   - Output: Pest/disease identification from `pest_disease_dataset.csv`

4. **`weather_alerts.py`**: 
   - Input: Location selection
   - Output: Weather forecast and farming advice from `weather_data.csv`

5. **`market_price.py`**: 
   - Display: Price trends and market analysis from `market_prices.csv`

6. **`community_alerts.py`**: 
   - Input: User-submitted alerts
   - Output: Community alert dashboard

7. **`ar_module.py`**: 
   - Feature: Video tutorial player using files from `videos/`

### Dataset Files (`data/`)
- **`soil_health.csv`**: 10 rows of soil types with fertilizer recommendations
- **`crop_requirements.csv`**: 15 crops with growing requirements
- **`pest_disease_dataset.csv`**: 12 common pests/diseases with treatments
- **`weather_data.csv`**: 21 weather records across Indian cities
- **`market_prices.csv`**: 22 crop price records from various markets

## 🚀 Quick Start

### 1. Setup
```bash
# Clone/create project directory
mkdir agricultural-advisory-app
cd agricultural-advisory-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install streamlit pandas numpy pillow
```

### 2. Create Directory Structure
```bash
# Create directories
mkdir -p modules data videos assets/{icons,images/{backgrounds,crops,pests,soil_types},sample_uploads} utils

# Create __init__.py files
touch modules/__init__.py utils/__init__.py
```

### 3. Add Dataset Files
Copy the provided CSV files to the `data/` directory:
- `soil_health.csv`
- `crop_requirements.csv`
- `pest_disease_dataset.csv`
- `weather_data.csv`
- `market_prices.csv`

### 4. Add Sample Assets
Follow the guides in `assets/README.md` and `videos/README.md` to add:
- Icons for each module (64x64px PNG)
- Sample crop/pest images
- Demo video file (`soil_prep_demo.mp4`)

### 5. Run Application
```bash
streamlit run app.py
```

## 📊 Dataset Schema Reference

### `soil_health.csv` (10 records)
| Column | Type | Description |
|--------|------|-------------|
| soil_type | string | Clay, Sandy, Loamy, etc. |
| nitrogen_level | string | Low, Medium, High |
| phosphorus_level | string | Low, Medium, High |
| potassium_level | string | Low, Medium, High |
| ph_level | float | 5.5 - 7.5 range |
| organic_matter | float | Percentage content |
| recommended_fertilizer | string | Fertilizer type |
| fertilizer_quantity_kg_per_hectare | int | Application rate |
| application_method | string | Broadcasting, drilling, etc. |
| best_application_time | string | Timing recommendation |

### `crop_requirements.csv` (15 records)
| Column | Type | Description |
|--------|------|-------------|
| crop_name | string | Rice, Wheat, Maize, etc. |
| soil_type | string | Preferred soil type |
| season | string | Kharif, Rabi, Summer |
| temperature_min | int | Minimum temperature (°C) |
| temperature_max | int | Maximum temperature (°C) |
| rainfall_mm | int | Required rainfall |
| growing_period_days | int | Days to harvest |
| yield_potential_tonnes_per_hectare | float | Expected yield |
| water_requirement | string | Low, Medium, High, Very High |
| sunlight_hours | string | Required sunlight |
| sowing_method | string | Broadcasting, drilling, etc. |

### `pest_disease_dataset.csv` (12 records)
| Column | Type | Description |
|--------|------|-------------|
| pest_disease_name | string | Name of pest/disease |
| crop_affected | string | Affected crop |
| type | string | Pest or Disease |
| symptoms | string | Visible symptoms |
| image_keywords | string | Keywords for image matching |
| treatment | string | General treatment |
| organic_solution | string | Organic treatment option |
| chemical_solution | string | Chemical treatment option |
| prevention_method | string | Preventive measures |
| severity_level | string | Low, Medium, High |

### `weather_data.csv` (21 records)
| Column | Type | Description |
|--------|------|-------------|
| location | string | City name |
| date | string | YYYY-MM-DD format |
| temperature_min | int | Minimum temperature |
| temperature_max | int | Maximum temperature |
| humidity | int | Humidity percentage |
| rainfall_mm | int | Rainfall amount |
| wind_speed_kmh | int | Wind speed |
| weather_condition | string | Weather description |
| alert_type | string | Alert level |
| farming_advice | string | Specific farming advice |

### `market_prices.csv` (22 records)
| Column | Type | Description |
|--------|------|-------------|
| crop_name | string | Crop name |
| market | string | Market location |
| date | string | Price date |
| price_per_quintal_inr | int | Price in INR |
| price_trend | string | Rising, Falling, Stable |
| demand_level | string | Low, Medium, High |
| quality_grade | string | Grade A, B, etc. |
| storage_advice | string | Storage recommendations |
| transportation_cost_per_quintal | int | Transport cost |
| market_arrival_tonnes | int | Market arrival quantity |

## 🎨 UI/UX Guidelines

### Color Scheme
- **Primary**: #2E7D32 (Agricultural Green)
- **Secondary**: #5D4037 (Soil Brown)
- **Accent**: #1976D2 (Sky Blue)
- **Warning**: #F57C00 (Alert Orange)
- **Success**: #388E3C (Healthy Green)
- **Background**: #F1F8E9 (Light Green)

### Navigation Structure
```
🌾 Agricultural Advisory Dashboard
├── 🌱 Crop Advisory
├── 🧪 Fertilizer Recommendation
├── 🐛 Pest & Disease Detection
├── 🌤️ Weather Alerts
├── 📊 Market Prices
├── 👥 Community Alerts
└── 🥽 AR/VR Learning
```

### Module Layout Pattern
Each module follows this structure:
1. **Header**: Icon + Module name
2. **Input Section**: User inputs/selections
3. **Processing**: Data analysis/lookup
4. **Results**: Formatted output with recommendations
5. **Additional Info**: Tips, warnings, or related data

## 🔧 Technical Requirements

### Dependencies (`requirements.txt`)
```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.21.0
pillow>=9.0.0
plotly>=5.0.0
opencv-python>=4.5.0
```

### Python Version
- Python 3.8 or higher recommended

### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```
Access at: `http://localhost:8501`

### Streamlit Cloud
1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy from main branch

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Heroku Deployment
Required files:
- `Procfile`: `web: sh setup.sh && streamlit run app.py`
- `setup.sh`: Streamlit configuration script

## 📝 Development Notes

### Module Development Pattern
Each module in `modules/` should follow this pattern:
```python
import streamlit as st
import pandas as pd

def run():
    st.header("🌱 Module Name")
    
    # Input section
    with st.container():
        # User inputs
        pass
    
    # Processing section
    if st.button("Process"):
        # Data analysis
        # Display results
        pass
```

### Data Loading Pattern
```python
@st.cache_data
def load_data(filename):
    return pd.read_csv(f"data/{filename}")
```

### Error Handling
- Validate user inputs
- Handle missing CSV files gracefully
- Provide fallback options for missing assets
- Display user-friendly error messages

## 🎯 Feature Extensions (Future)

### Phase 2 Enhancements
- **Real API Integration**: Weather, market prices
- **Machine Learning**: Advanced pest detection
- **Database**: SQLite/PostgreSQL for persistence
- **User Authentication**: Login/registration system
- **Mobile App**: React Native companion
- **Multilingual Support**: Local language options

### Advanced Features
- **IoT Integration**: Sensor data collection
- **Satellite Imagery**: Crop monitoring
- **AI Chatbot**: Farming assistant
- **Supply Chain**: Farm-to-market tracking
- **Financial Tools**: Loan and insurance calculators

This structure provides a complete foundation for building a comprehensive agricultural advisory application with dataset-driven recommendations and modern web UI/UX.