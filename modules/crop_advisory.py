import streamlit as st
import pandas as pd
from pathlib import Path

def load_crop_data():
    """Load crop requirements data"""
    data_path = Path(__file__).parent.parent / "data" / "crop_requirements.csv"
    if data_path.exists():
        return pd.read_csv(data_path)
    else:
        # Sample data if file doesn't exist
        return pd.DataFrame({
            'crop_name': ['Rice', 'Wheat', 'Cotton', 'Tomato', 'Potato', 'Sugarcane', 'Maize', 'Soybean'],
            'soil_type': ['Clay', 'Loamy', 'Sandy', 'Loamy', 'Sandy Loam', 'Clay', 'Loamy', 'Clay Loam'],
            'season': ['Kharif', 'Rabi', 'Kharif', 'Summer', 'Winter', 'Annual', 'Kharif', 'Kharif'],
            'water_requirement': ['High', 'Medium', 'Medium', 'High', 'Medium', 'Very High', 'Medium', 'Low'],
            'temperature_range': ['25-35°C', '15-25°C', '20-30°C', '18-29°C', '15-20°C', '26-32°C', '21-27°C', '20-30°C'],
            'yield_per_acre': [25, 30, 8, 40, 35, 80, 28, 15],
            'profitability_score': [7.5, 8.2, 6.8, 9.1, 7.8, 8.5, 7.9, 6.9],
            'growth_duration_days': [120, 150, 180, 90, 100, 365, 110, 120]
        })

def get_crop_recommendations(soil_type, season, water_availability):
    """Get crop recommendations based on input parameters"""
    df = load_crop_data()
    
    # Filter based on inputs
    recommendations = df.copy()
    
    if soil_type != "Any":
        recommendations = recommendations[recommendations['soil_type'].str.contains(soil_type, case=False, na=False)]
    
    if season != "Any":
        recommendations = recommendations[recommendations['season'].str.contains(season, case=False, na=False)]
    
    # Filter by water requirement based on availability
    water_map = {
        "Low": ["Low"],
        "Medium": ["Low", "Medium"], 
        "High": ["Low", "Medium", "High"],
        "Very High": ["Low", "Medium", "High", "Very High"]
    }
    
    if water_availability in water_map:
        recommendations = recommendations[recommendations['water_requirement'].isin(water_map[water_availability])]
    
    # Sort by profitability score
    recommendations = recommendations.sort_values('profitability_score', ascending=False)
    
    return recommendations

def run():
    """Main function for crop advisory module"""
    
    st.markdown("## 🌱 Crop Advisory System")
    st.markdown("Get personalized crop recommendations based on your soil, season, and water availability.")
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Farm Details")
        
        soil_type = st.selectbox(
            "🏞️ Select Soil Type:",
            ["Any", "Clay", "Loamy", "Sandy", "Sandy Loam", "Clay Loam", "Silty"],
            help="Choose your predominant soil type"
        )
        
        season = st.selectbox(
            "🗓️ Select Season:",
            ["Any", "Kharif", "Rabi", "Summer", "Winter", "Annual"],
            help="Kharif: Jun-Oct, Rabi: Nov-Apr"
        )
        
        water_availability = st.selectbox(
            "💧 Water Availability:",
            ["Low", "Medium", "High", "Very High"],
            help="Assess your irrigation capacity"
        )
        
        farm_size = st.number_input(
            "🌾 Farm Size (acres):",
            min_value=0.1,
            max_value=1000.0,
            value=5.0,
            step=0.5
        )
    
    with col2:
        st.markdown("### 🎯 Additional Preferences")
        
        investment_budget = st.selectbox(
            "💰 Investment Budget:",
            ["Low (< ₹25,000/acre)", "Medium (₹25,000-50,000/acre)", "High (> ₹50,000/acre)"]
        )
        
        experience_level = st.selectbox(
            "👨‍🌾 Farming Experience:",
            ["Beginner", "Intermediate", "Advanced"]
        )
        
        market_preference = st.selectbox(
            "🏪 Market Preference:",
            ["Local Market", "Export Market", "Both"]
        )
        
        risk_tolerance = st.selectbox(
            "⚖️ Risk Tolerance:",
            ["Conservative", "Moderate", "Aggressive"]
        )
    
    # Get recommendations button
    if st.button("🔍 Get Crop Recommendations", type="primary"):
        
        recommendations = get_crop_recommendations(soil_type, season, water_availability)
        
        if not recommendations.empty:
            st.markdown("---")
            st.markdown("## 🎯 Recommended Crops for Your Farm")
            
            # Top 3 recommendations
            top_crops = recommendations.head(3)
            
            for idx, (_, crop) in enumerate(top_crops.iterrows()):
                with st.expander(f"🥇 #{idx+1}: {crop['crop_name']} (Score: {crop['profitability_score']}/10)", expanded=idx==0):
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**🌡️ Growing Conditions**")
                        st.write(f"Temperature: {crop['temperature_range']}")
                        st.write(f"Water Need: {crop['water_requirement']}")
                        st.write(f"Growth Period: {crop['growth_duration_days']} days")
                    
                    with col2:
                        st.markdown("**📊 Yield & Profitability**")
                        st.write(f"Expected Yield: {crop['yield_per_acre']} qt/acre")
                        estimated_production = crop['yield_per_acre'] * farm_size
                        st.write(f"Your Production: {estimated_production:.1f} qt")
                        st.write(f"Profitability: {crop['profitability_score']}/10")
                    
                    with col3:
                        st.markdown("**💡 Quick Stats**")
                        # Estimated revenue (sample calculation)
                        avg_price = {
                            'Rice': 2000, 'Wheat': 2200, 'Cotton': 5500,
                            'Tomato': 1500, 'Potato': 1200, 'Sugarcane': 350,
                            'Maize': 1800, 'Soybean': 4000
                        }
                        
                        price = avg_price.get(crop['crop_name'], 2000)
                        estimated_revenue = estimated_production * price
                        
                        st.metric("Est. Revenue", f"₹{estimated_revenue:,.0f}")
                        st.write(f"Per qt: ₹{price}")
            
            # Additional insights
            st.markdown("---")
            st.markdown("## 💡 Additional Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🌟 Pro Tips")
                if soil_type == "Clay":
                    st.info("💧 Clay soil retains water well - consider crops that need consistent moisture")
                elif soil_type == "Sandy":
                    st.info("🏃‍♂️ Sandy soil drains quickly - choose drought-resistant crops")
                elif soil_type == "Loamy":
                    st.success("🎯 Loamy soil is ideal for most crops - you have great flexibility!")
                
                if season == "Kharif":
                    st.info("🌧️ Kharif season benefits from monsoon rains - rice and cotton are excellent choices")
                elif season == "Rabi":
                    st.info("❄️ Rabi season has cooler weather - wheat and mustard perform well")
            
            with col2:
                st.markdown("### ⚠️ Risk Factors")
                st.warning("🦗 Monitor for seasonal pests specific to your chosen crops")
                st.warning("🌡️ Climate change may affect traditional growing patterns")
                st.info("📊 Consider crop insurance for high-value crops")
                st.info("🤝 Join farmer groups for collective bargaining power")
            
            # Detailed comparison table
            st.markdown("---")
            st.markdown("## 📋 Detailed Crop Comparison")
            
            # Display formatted dataframe
            display_df = recommendations[['crop_name', 'season', 'water_requirement', 
                                       'yield_per_acre', 'profitability_score', 'growth_duration_days']].copy()
            display_df.columns = ['Crop', 'Season', 'Water Need', 'Yield (qt/acre)', 'Profit Score', 'Days to Harvest']
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
            
        else:
            st.warning("⚠️ No crops found matching your criteria. Try adjusting your filters.")
            st.markdown("### 💡 Suggestions:")
            st.markdown("- Try selecting 'Any' for soil type or season")
            st.markdown("- Consider improving water availability through irrigation")
            st.markdown("- Contact local agricultural extension officers for advice")
    
    # Information section
    st.markdown("---")
    st.markdown("## 📚 Learn More")
    
    with st.expander("🌱 Soil Types Guide"):
        st.markdown("""
        **Clay Soil**: Heavy, water-retaining, rich in nutrients. Good for rice, wheat.
        
        **Sandy Soil**: Light, fast-draining, warms up quickly. Good for root vegetables.
        
        **Loamy Soil**: Perfect mix of sand, silt, clay. Ideal for most crops.
        
        **Silty Soil**: Smooth, retains moisture, fertile. Good for grasses and grains.
        """)
    
    with st.expander("📅 Cropping Seasons in India"):
        st.markdown("""
        **Kharif Season**: June to October (Monsoon crops)
        - Rice, Cotton, Sugarcane, Maize, Pulses
        
        **Rabi Season**: November to April (Winter crops)  
        - Wheat, Barley, Mustard, Gram, Peas
        
        **Summer Season**: March to June
        - Fodder crops, vegetables, fruits
        """)
    
    with st.expander("💧 Water Management Tips"):
        st.markdown("""
        **Drip Irrigation**: 30-50% water savings, better for high-value crops
        
        **Sprinkler Systems**: Good for field crops, uniform water distribution
        
        **Rainwater Harvesting**: Store monsoon water for dry periods
        
        **Mulching**: Reduces evaporation, maintains soil moisture
        """)

if __name__ == "__main__":
    run()