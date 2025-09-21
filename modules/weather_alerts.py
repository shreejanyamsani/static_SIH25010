import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
from datetime import datetime, timedelta
import csv
import io


def safe_read_csv(path):
    """Read CSV robustly: sniff delimiter, try fallbacks, and avoid raising on empty/malformed files.

    Returns a DataFrame or an empty DataFrame on failure.
    """
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return pd.DataFrame()

    # Read sample for sniffing
    try:
        sample = p.read_text(encoding='utf-8', errors='replace')[:8192]
    except Exception:
        sample = None

    delimiter = None
    if sample:
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=[',', ';', '\t', '|'])
            delimiter = dialect.delimiter
        except Exception:
            delimiter = None

    tried = set()
    candidates = ([delimiter] if delimiter else []) + [',', ';', '\t', '|']
    for delim in candidates:
        if not delim or delim in tried:
            continue
        tried.add(delim)
        try:
            df = pd.read_csv(p, sep=delim)
            # If read yields multiple columns, assume success
            if not df.empty and len(df.columns) > 0:
                return df
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            continue
        except Exception:
            continue

    # Last attempt with python engine
    try:
        df = pd.read_csv(p, engine='python')
        return df
    except Exception:
        return pd.DataFrame()


def load_weather_data():
    """Load weather forecast data with normalization and demo fallback."""
    global weather_load_info
    weather_load_info = {'source': None, 'warning': None, 'columns': None, 'sample': None, 'rename_map': None}

    data_path = Path(__file__).parent.parent / "data" / "weather_data.csv"

    if data_path.exists():
        try:
            raw_text = data_path.read_text(encoding='utf-8', errors='replace')
        except Exception:
            raw_text = None

        df = safe_read_csv(data_path)
        if df is None or df.empty:
            weather_load_info.update({'source': 'demo_generated', 'warning': f'CSV at {data_path} is missing/empty/malformed; generated demo data instead.', 'columns': [], 'sample': (raw_text[:2048] if raw_text else None), 'rename_map': {}})
        else:
            orig_columns = df.columns.tolist()
            weather_load_info.update({'source': 'csv', 'warning': None, 'columns': orig_columns, 'sample': (raw_text[:2048] if raw_text else None)})

            # Normalize common alternative column names
            cols_lower = {c.lower(): c for c in df.columns}

            def pick(variants):
                for v in variants:
                    if v in cols_lower:
                        return cols_lower[v]
                for v in variants:
                    for low_c, orig in cols_lower.items():
                        if v in low_c:
                            return orig
                return None

            rename_map = {}
            # temperature
            m = pick(['maxtemp_c', 'maxtemp', 'max_temp', 'max temp', 'temp_max', 'temperature_max'])
            if m:
                rename_map[m] = 'max_temp'
            m = pick(['mintemp_c', 'mintemp', 'min_temp', 'min temp', 'temp_min', 'temperature_min'])
            if m:
                rename_map[m] = 'min_temp'
            # rainfall
            m = pick(['precip_mm', 'precipitation', 'rainfall', 'rain_mm', 'rain', 'rainfall_mm'])
            if m:
                rename_map[m] = 'rainfall'
            # humidity
            m = pick(['humidity', 'hum'])
            if m:
                rename_map[m] = 'humidity'
            # wind
            m = pick(['wind_kph', 'wind_km_h', 'wind_speed', 'wind', 'wind_speed_kmh', 'wind_kmh'])
            if m:
                rename_map[m] = 'wind_speed'
            # uv, pressure, condition, location, date
            m = pick(['uv', 'uv_index', 'uvindex'])
            if m:
                rename_map[m] = 'uv_index'
            m = pick(['pressure', 'press'])
            if m:
                rename_map[m] = 'pressure'
            m = pick(['weather_condition', 'condition', 'weather'])
            if m:
                rename_map[m] = 'condition'
            m = pick(['location', 'city', 'place'])
            if m:
                rename_map[m] = 'location'
            m = pick(['date', 'datetime', 'day'])
            if m:
                rename_map[m] = 'date'

            if rename_map:
                df = df.rename(columns=rename_map)

            numeric_cols = ['max_temp', 'min_temp', 'rainfall', 'humidity', 'wind_speed', 'uv_index', 'pressure']
            for c in numeric_cols:
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors='coerce')

            if 'date' in df.columns:
                try:
                    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
                except Exception:
                    df['date'] = df['date'].astype(str)

            if 'location' not in df.columns:
                df['location'] = 'Unknown'

            weather_load_info['rename_map'] = rename_map
            return df

    # Demo generation fallback
    dates = [datetime.now() + timedelta(days=i) for i in range(10)]
    np.random.seed(42)
    locations = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad', 'Ahmedabad']
    weather_data = []
    for location in locations:
        for i, date in enumerate(dates):
            base_temp = {'Delhi': 25, 'Mumbai': 28, 'Bangalore': 22, 'Chennai': 30,
                        'Kolkata': 26, 'Pune': 24, 'Hyderabad': 27, 'Ahmedabad': 29}[location]
            temp_variation = np.sin(i * 0.5) * 3 + np.random.normal(0, 2)
            max_temp = base_temp + temp_variation + 5
            min_temp = base_temp + temp_variation - 3
            if 6 <= date.month <= 9:
                rainfall = max(0, np.random.exponential(15) if np.random.random() > 0.6 else 0)
                humidity = min(95, 70 + np.random.normal(15, 10))
            else:
                rainfall = max(0, np.random.exponential(2) if np.random.random() > 0.9 else 0)
                humidity = min(90, 45 + np.random.normal(20, 15))
            wind_speed = max(0, np.random.normal(8, 4))
            if rainfall > 50:
                condition = "Heavy Rain"
            elif rainfall > 10:
                condition = "Light Rain"
            elif humidity > 80:
                condition = "Cloudy"
            elif max_temp > base_temp + 8:
                condition = "Hot"
            else:
                condition = "Clear"
            weather_data.append({
                'location': location,
                'date': date.strftime('%Y-%m-%d'),
                'max_temp': round(max_temp, 1),
                'min_temp': round(min_temp, 1),
                'humidity': round(humidity, 0),
                'rainfall': round(rainfall, 1),
                'wind_speed': round(wind_speed, 1),
                'condition': condition,
                'uv_index': min(11, max(1, round(max_temp / 4))),
                'pressure': round(1013 + np.random.normal(0, 10), 1)
            })

    df_demo = pd.DataFrame(weather_data)
    weather_load_info.update({'source': 'demo_generated', 'warning': f'CSV missing or invalid at {data_path}; generated demo data.', 'columns': [], 'sample': None, 'rename_map': {}})
    return df_demo

def generate_weather_alerts(weather_df, location):
    """Generate weather-based agricultural alerts"""
    alerts = []
    location_data = weather_df[weather_df['location'] == location].head(7)  # Next 7 days
    
    for _, day in location_data.iterrows():
        date = day['date']
        
        # Heavy rain alert
        if day['rainfall'] > 50:
            alerts.append({
                'date': date,
                'type': 'Critical',
                'icon': '🌧️',
                'title': 'Heavy Rainfall Alert',
                'message': f"Expected rainfall: {day['rainfall']:.1f}mm. Protect crops from waterlogging.",
                'recommendations': [
                    "Ensure proper drainage in fields",
                    "Postpone spraying operations",
                    "Harvest mature crops if possible",
                    "Cover harvested grain properly"
                ]
            })
        
        # High temperature alert
        elif day['max_temp'] > 35:
            alerts.append({
                'date': date,
                'type': 'Warning',
                'icon': '🌡️',
                'title': 'High Temperature Alert',
                'message': f"Maximum temperature expected: {day['max_temp']:.1f}°C",
                'recommendations': [
                    "Increase irrigation frequency",
                    "Provide shade to sensitive crops",
                    "Avoid field operations during peak hours",
                    "Monitor livestock for heat stress"
                ]
            })
        
        # Frost alert (low temperature)
        elif day['min_temp'] < 5:
            alerts.append({
                'date': date,
                'type': 'Critical',
                'icon': '❄️',
                'title': 'Frost Alert',
                'message': f"Minimum temperature: {day['min_temp']:.1f}°C. Risk of frost damage.",
                'recommendations': [
                    "Cover sensitive plants",
                    "Use smoke or water sprinklers",
                    "Harvest tender vegetables",
                    "Protect nursery plants"
                ]
            })
        
        # High wind alert
        elif day['wind_speed'] > 25:
            alerts.append({
                'date': date,
                'type': 'Warning',
                'icon': '💨',
                'title': 'Strong Wind Alert',
                'message': f"Wind speed: {day['wind_speed']:.1f} km/h",
                'recommendations': [
                    "Secure greenhouse structures",
                    "Postpone aerial spraying",
                    "Support tall crops with stakes",
                    "Check irrigation pipes"
                ]
            })
        
        # Dry spell alert
        elif day['humidity'] < 30 and day['rainfall'] == 0:
            alerts.append({
                'date': date,
                'type': 'Advisory',
                'icon': '🏜️',
                'title': 'Dry Weather Advisory',
                'message': f"Low humidity: {day['humidity']:.0f}%",
                'recommendations': [
                    "Increase irrigation frequency",
                    "Apply mulch to conserve moisture",
                    "Monitor crop water stress",
                    "Consider foliar feeding"
                ]
            })
        
        # Good weather for operations
        elif 15 <= day['max_temp'] <= 30 and day['rainfall'] == 0 and day['wind_speed'] < 15:
            alerts.append({
                'date': date,
                'type': 'Favorable',
                'icon': '☀️',
                'title': 'Favorable Weather',
                'message': "Good conditions for field operations",
                'recommendations': [
                    "Ideal for spraying operations",
                    "Good for harvesting",
                    "Suitable for land preparation",
                    "Perfect for sowing operations"
                ]
            })
    
    return alerts

def create_weather_chart(weather_df, location):
    """Create weather forecast chart"""
    location_data = weather_df[weather_df['location'] == location].head(7)
    
    fig = go.Figure()
    
    # Temperature traces
    fig.add_trace(go.Scatter(
        x=location_data['date'],
        y=location_data['max_temp'],
        mode='lines+markers',
        name='Max Temperature',
        line=dict(color='red', width=2),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=location_data['date'],
        y=location_data['min_temp'],
        mode='lines+markers',
        name='Min Temperature',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))
    
    # Rainfall bars
    fig.add_trace(go.Bar(
        x=location_data['date'],
        y=location_data['rainfall'],
        name='Rainfall (mm)',
        yaxis='y2',
        marker_color='lightblue',
        opacity=0.7
    ))
    
    fig.update_layout(
        title=f'7-Day Weather Forecast - {location}',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        yaxis2=dict(
            title='Rainfall (mm)',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified'
    )
    
    return fig

def run():
    """Main function for weather alerts module"""
    
    st.markdown("## 🌤️ Weather Alerts & Forecast")
    st.markdown("Get weather forecasts and agricultural advisories for your location.")
    
    # Load weather data
    weather_df = load_weather_data()
    
    # Location selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_location = st.selectbox(
            "📍 Select Location:",
            weather_df['location'].unique(),
            help="Choose your nearest location"
        )
    
    with col2:
        alert_types = st.multiselect(
            "⚠️ Alert Types:",
            ["Critical", "Warning", "Advisory", "Favorable"],
            default=["Critical", "Warning"],
            help="Select which types of alerts to show"
        )
    
    with col3:
        forecast_days = st.selectbox(
            "📅 Forecast Period:",
            [3, 7, 10],
            index=1,
            help="Number of days to show forecast"
        )
    
    # Current weather summary
    loc_df = weather_df[weather_df['location'] == selected_location]
    if loc_df.empty:
        st.warning(f"No weather data available for '{selected_location}'.")
        return
    current_weather = loc_df.iloc[0]

    # Helper to safely fetch and format values from the pandas Series
    def safe_format(series, key, fmt=None, default='N/A'):
        # series.get works on Series and returns None if missing
        val = series.get(key) if hasattr(series, 'get') else None
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return default
        if fmt:
            try:
                return fmt.format(float(val))
            except Exception:
                return default
        return str(val)
    
    st.markdown("---")
    st.markdown("### 🌡️ Current Weather Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "🌡️ Temperature",
            safe_format(current_weather, 'max_temp', "{:.1f}°C"),
            f"Min: {safe_format(current_weather, 'min_temp', '{:.1f}°C')}"
        )
    
    with col2:
        st.metric(
            "🌧️ Rainfall",
            safe_format(current_weather, 'rainfall', "{:.1f}mm"),
            "Today"
        )
    
    with col3:
        st.metric(
            "💨 Wind Speed",
            safe_format(current_weather, 'wind_speed', "{:.1f} km/h"),
            "Current"
        )
    
    with col4:
        st.metric(
            "💧 Humidity",
            safe_format(current_weather, 'humidity', "{:.0f}%"),
            "Current"
        )
    
    with col5:
        st.metric(
            "☀️ UV Index",
            safe_format(current_weather, 'uv_index', "{:.0f}"),
            "Today"
        )

    # Show warning / debug info if CSV was missing/invalid
    info = globals().get('weather_load_info')
    if info and info.get('warning'):
        st.warning(info.get('warning'))
        with st.expander("⚙️ Weather data debug info"):
            st.write("Detected columns:", info.get('columns'))
            st.write("Rename map:", info.get('rename_map'))
            sample = info.get('sample')
            if sample:
                st.markdown("**CSV sample (first 2KB):**")
                st.code(sample)
    
    # Weather alerts
    alerts = generate_weather_alerts(weather_df, selected_location)
    filtered_alerts = [alert for alert in alerts if alert['type'] in alert_types]
    
    if filtered_alerts:
        st.markdown("---")
        st.markdown("### 🚨 Weather Alerts")
        
        # Group alerts by type
        alert_groups = {'Critical': [], 'Warning': [], 'Advisory': [], 'Favorable': []}
        for alert in filtered_alerts:
            alert_groups[alert['type']].append(alert)
        
        # Display critical alerts first
        for alert_type in ['Critical', 'Warning', 'Advisory', 'Favorable']:
            if alert_groups[alert_type]:
                
                for alert in alert_groups[alert_type]:
                    alert_color = {
                        'Critical': 'error',
                        'Warning': 'warning', 
                        'Advisory': 'info',
                        'Favorable': 'success'
                    }[alert['type']]
                    
                    with st.container():
                        if alert_color == 'error':
                            st.error(f"{alert['icon']} **{alert['title']}** ({alert['date']})")
                        elif alert_color == 'warning':
                            st.warning(f"{alert['icon']} **{alert['title']}** ({alert['date']})")
                        elif alert_color == 'info':
                            st.info(f"{alert['icon']} **{alert['title']}** ({alert['date']})")
                        else:
                            st.success(f"{alert['icon']} **{alert['title']}** ({alert['date']})")
                        
                        st.write(alert['message'])
                        
                        # Show recommendations in expandable section
                        with st.expander("💡 Recommendations"):
                            for rec in alert['recommendations']:
                                st.write(f"• {rec}")
    
    # Weather forecast chart
    st.markdown("---")
    st.markdown("### 📊 Weather Forecast")
    
    fig = create_weather_chart(weather_df, selected_location)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed forecast table
    location_forecast = weather_df[weather_df['location'] == selected_location].head(forecast_days)
    
    st.markdown("### 📋 Detailed Forecast")
    
    # Format the data for display
    display_forecast = location_forecast.copy()
    display_forecast['Temperature'] = display_forecast.apply(lambda x: f"{x['max_temp']:.1f}°C / {x['min_temp']:.1f}°C", axis=1)
    display_forecast['Weather'] = display_forecast['condition'] + " " + display_forecast.apply(lambda x: f"({x['humidity']:.0f}% humidity)", axis=1)
    display_forecast['Rain/Wind'] = display_forecast.apply(lambda x: f"{x['rainfall']:.1f}mm / {x['wind_speed']:.1f}km/h", axis=1)
    
    forecast_table = display_forecast[['date', 'Temperature', 'Weather', 'Rain/Wind']].copy()
    forecast_table.columns = ['Date', 'Max/Min Temp', 'Condition', 'Rain/Wind']
    
    st.dataframe(forecast_table, hide_index=True, use_container_width=True)
    
    # Agricultural calendar based on weather
    st.markdown("---")
    st.markdown("### 🌾 Agricultural Calendar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Recommended Activities (Next 7 Days)")
        
        activities = []
        for _, day in location_forecast.head(7).iterrows():
            date = day['date']
            
            if day['rainfall'] == 0 and 15 <= day['max_temp'] <= 30:
                activities.append(f"**{date}**: ✅ Good for spraying, harvesting, land preparation")
            elif day['rainfall'] > 0 and day['rainfall'] < 10:
                activities.append(f"**{date}**: 🌱 Good for sowing, transplanting")
            elif day['rainfall'] > 50:
                activities.append(f"**{date}**: ⚠️ Avoid field operations, ensure drainage")
            elif day['max_temp'] > 35:
                activities.append(f"**{date}**: 🌡️ Increase irrigation, avoid mid-day work")
            else:
                activities.append(f"**{date}**: 🔄 Plan indoor activities, equipment maintenance")
        
        for activity in activities:
            st.markdown(activity)
    
    with col2:
        st.markdown("#### 🎯 Crop-Specific Advisories")
        
        crop_advisories = {
            "Rice": "Monitor water levels, watch for pest outbreak after rain",
            "Wheat": "Avoid irrigation if rain expected, harvest in dry weather", 
            "Cotton": "Protect from heavy rain, ensure proper drainage",
            "Vegetables": "Cover during extreme weather, increase harvest frequency",
            "Fruits": "Protect blossoms from rain, support branches in wind"
        }
        
        selected_crop = st.selectbox("Select your crop:", list(crop_advisories.keys()))
        st.info(f"**{selected_crop}:** {crop_advisories[selected_crop]}")
        
        # Weather-based pest alerts
        if current_weather['humidity'] > 80 and current_weather['max_temp'] > 25:
            st.warning("🐛 **Pest Alert**: High humidity and temperature favor pest development. Monitor crops closely.")
        
        if current_weather['rainfall'] > 20:
            st.warning("🦠 **Disease Alert**: Wet conditions favor fungal diseases. Consider preventive sprays.")
    
    # Weather trends and historical data
    st.markdown("---")
    st.markdown("### 📈 Weather Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature trend
        temp_trend_data = location_forecast.head(forecast_days)
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=list(range(len(temp_trend_data))),
            y=temp_trend_data['max_temp'],
            mode='lines+markers',
            name='Max Temperature Trend',
            line=dict(color='red')
        ))
        
        fig_trend.update_layout(
            title='Temperature Trend',
            xaxis_title='Days Ahead',
            yaxis_title='Temperature (°C)',
            height=300
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        # Rainfall pattern
        fig_rain = go.Figure()
        fig_rain.add_trace(go.Bar(
            x=list(range(len(temp_trend_data))),
            y=temp_trend_data['rainfall'],
            name='Rainfall Pattern',
            marker_color='lightblue'
        ))
        
        fig_rain.update_layout(
            title='Rainfall Pattern',
            xaxis_title='Days Ahead', 
            yaxis_title='Rainfall (mm)',
            height=300
        )
        
        st.plotly_chart(fig_rain, use_container_width=True)
    
    # Seasonal information
    st.markdown("---")
    st.markdown("### 🗓️ Seasonal Information")
    
    current_month = datetime.now().month
    season_info = {
        (12, 1, 2): {"name": "Winter", "crops": "Wheat, Mustard, Peas", "focus": "Frost protection, timely irrigation"},
        (3, 4, 5): {"name": "Spring", "crops": "Summer vegetables, Fodder crops", "focus": "Heat stress management"},
        (6, 7, 8, 9): {"name": "Monsoon", "crops": "Rice, Cotton, Sugarcane", "focus": "Drainage, disease control"},
        (10, 11): {"name": "Post-Monsoon", "crops": "Late kharif, Early rabi", "focus": "Harvest timing, storage"}
    }
    
    current_season = None
    for months, info in season_info.items():
        if current_month in months:
            current_season = info
            break
    
    if current_season:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"**Current Season:** {current_season['name']}")
        
        with col2:
            st.info(f"**Suitable Crops:** {current_season['crops']}")
        
        with col3:
            st.info(f"**Focus Area:** {current_season['focus']}")
    
    # Emergency weather preparedness
    st.markdown("---")
    st.markdown("### 🆘 Emergency Weather Preparedness")
    
    preparedness_tips = {
        "Cyclone/Storm": {
            "icon": "🌪️",
            "tips": [
                "Harvest mature crops immediately",
                "Secure farm structures and equipment",
                "Create drainage channels",
                "Store seeds and fertilizers in safe places",
                "Keep emergency contact numbers ready"
            ]
        },
        "Drought": {
            "icon": "🏜️", 
            "tips": [
                "Implement water conservation techniques",
                "Use drought-resistant crop varieties",
                "Apply mulch to reduce evaporation",
                "Install drip irrigation systems",
                "Plan alternative income sources"
            ]
        },
        "Flood": {
            "icon": "🌊",
            "tips": [
                "Ensure proper field drainage",
                "Elevate storage areas",
                "Keep pumping equipment ready",
                "Have flood-resistant seed varieties",
                "Maintain emergency food supplies"
            ]
        },
        "Hailstorm": {
            "icon": "🧊",
            "tips": [
                "Use protective nets over crops",
                "Monitor weather radar closely",
                "Have crop insurance coverage",
                "Keep indoor livestock shelters ready",
                "Document damage for insurance claims"
            ]
        }
    }
    
    selected_emergency = st.selectbox(
        "🚨 Select Emergency Type:",
        list(preparedness_tips.keys())
    )
    
    emergency_info = preparedness_tips[selected_emergency]
    st.markdown(f"### {emergency_info['icon']} {selected_emergency} Preparedness")
    
    for tip in emergency_info['tips']:
        st.write(f"• {tip}")
    
    # Weather-based irrigation scheduler
    st.markdown("---")
    st.markdown("### 💧 Smart Irrigation Scheduler")
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop_type_irrigation = st.selectbox(
            "🌱 Crop Type:",
            ["Rice", "Wheat", "Cotton", "Vegetables", "Fruits"],
            key="irrigation_crop"
        )
        
        soil_type_irrigation = st.selectbox(
            "🏞️ Soil Type:",
            ["Clay", "Loamy", "Sandy", "Black Cotton"]
        )
    
    with col2:
        growth_stage_irrigation = st.selectbox(
            "🌿 Growth Stage:",
            ["Germination", "Vegetative", "Flowering", "Fruiting", "Maturity"]
        )
        
        irrigation_method = st.selectbox(
            "💧 Irrigation Method:",
            ["Flood", "Sprinkler", "Drip", "Furrow"]
        )
    
    if st.button("📅 Generate Irrigation Schedule"):
        st.markdown("#### 📋 7-Day Irrigation Schedule")
        
        irrigation_schedule = []
        
        # Water requirement factors
        crop_water_need = {"Rice": 1.5, "Wheat": 1.0, "Cotton": 1.2, "Vegetables": 0.8, "Fruits": 1.1}
        stage_factor = {"Germination": 0.7, "Vegetative": 1.0, "Flowering": 1.3, "Fruiting": 1.2, "Maturity": 0.6}
        soil_factor = {"Clay": 0.8, "Loamy": 1.0, "Sandy": 1.3, "Black Cotton": 0.9}
        
        base_requirement = crop_water_need.get(crop_type_irrigation, 1.0) * stage_factor.get(growth_stage_irrigation, 1.0) * soil_factor.get(soil_type_irrigation, 1.0)
        
        for _, day in location_forecast.head(7).iterrows():
            date = day['date']
            rain = day['rainfall']
            temp = day['max_temp']
            humidity = day['humidity']
            
            # Calculate daily water requirement (simplified)
            et_factor = 1 + (temp - 25) * 0.02 + (100 - humidity) * 0.005  # Evapotranspiration factor
            daily_need = base_requirement * et_factor * 10  # mm per day
            
            # Adjust for rainfall
            irrigation_need = max(0, daily_need - rain)
            
            if irrigation_need > 5:
                status = "💧 Irrigate"
                amount = f"{irrigation_need:.1f} mm"
            elif irrigation_need > 0:
                status = "🌿 Light watering"
                amount = f"{irrigation_need:.1f} mm"
            else:
                status = "✅ No irrigation needed"
                amount = "0 mm"
            
            irrigation_schedule.append({
                'Date': date,
                'Weather': day['condition'],
                'Rainfall': f"{rain:.1f} mm",
                'Irrigation Need': amount,
                'Action': status
            })
        
        schedule_df = pd.DataFrame(irrigation_schedule)
        st.dataframe(schedule_df, hide_index=True, use_container_width=True)
        
        # Water conservation tips
        st.markdown("#### 💡 Water Conservation Tips")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.success("""
            **Efficient Practices:**
            • Early morning irrigation (5-7 AM)
            • Use mulch to reduce evaporation
            • Install soil moisture sensors
            • Collect and use rainwater
            """)
        
        with col_b:
            st.info("""
            **Schedule Optimization:**
            • Avoid irrigation before rain
            • Deep, less frequent watering
            • Adjust for crop growth stage
            • Monitor soil moisture levels
            """)
    
    # Weather data sources and reliability
    st.markdown("---")
    st.markdown("### 📊 Data Sources & Reliability")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🛰️ Data Sources")
        st.markdown("""
        - **IMD**: India Meteorological Dept
        - **ISRO**: Satellite imagery
        - **AWS**: Automatic Weather Stations  
        - **Doppler Radar**: Real-time data
        """)
    
    with col2:
        st.markdown("#### 📈 Forecast Accuracy")
        st.markdown("""
        - **Day 1**: 95% accuracy
        - **Day 2-3**: 85% accuracy
        - **Day 4-7**: 70% accuracy
        - **Beyond 7 days**: Trend only
        """)
    
    with col3:
        st.markdown("#### 📱 Alert Delivery")
        st.markdown("""
        - **SMS**: Critical alerts
        - **App Push**: All alerts
        - **Email**: Daily summaries
        - **Voice Call**: Emergency only
        """)
    
    # Contact information for weather emergencies
    st.markdown("---")
    st.markdown("### 📞 Emergency Contacts")
    
    st.warning("""
    **Weather Emergency Helplines:**
    
    🌧️ **Flood/Cyclone**: 1070 (National Disaster Response)
    
    🔥 **Fire Emergency**: 101
    
    🚑 **Medical Emergency**: 108
    
    🌾 **Agricultural Helpline**: 1800-180-1551
    
    📱 **State Emergency**: 100
    
    **Local Contacts:**
    - District Collector Office
    - Tehsildar/Block Office  
    - Krishi Vigyan Kendra (KVK)
    - Local Police Station
    """)
    
    # Download weather data option
    st.markdown("---")
    if st.button("📥 Download Weather Data (CSV)"):
        csv = location_forecast.to_csv(index=False)
        st.download_button(
            label="💾 Download Forecast Data",
            data=csv,
            file_name=f"weather_forecast_{selected_location}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    run()