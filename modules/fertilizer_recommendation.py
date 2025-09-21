import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

def load_soil_health_data():
    """Load soil health data"""
    data_path = Path(__file__).parent.parent / "data" / "soil_health.csv"
    if data_path.exists():
        return pd.read_csv(data_path)
    else:
        # Sample data if file doesn't exist
        return pd.DataFrame({
            'soil_id': ['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008'],
            'region': ['Punjab', 'Haryana', 'UP', 'Bihar', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Gujarat'],
            'soil_type': ['Alluvial', 'Sandy Loam', 'Clay', 'Silt Loam', 'Black Soil', 'Red Soil', 'Laterite', 'Desert'],
            'ph_level': [7.2, 6.8, 7.5, 6.9, 7.8, 6.2, 5.8, 8.1],
            'nitrogen_ppm': [240, 180, 320, 200, 280, 150, 120, 90],
            'phosphorus_ppm': [25, 18, 35, 22, 30, 15, 12, 8],
            'potassium_ppm': [180, 150, 220, 160, 200, 130, 110, 80],
            'organic_matter_percent': [2.1, 1.8, 2.5, 2.2, 3.2, 1.5, 1.2, 0.8],
            'calcium_ppm': [400, 350, 450, 380, 520, 300, 250, 200],
            'magnesium_ppm': [80, 70, 90, 75, 100, 60, 50, 40],
            'sulfur_ppm': [15, 12, 18, 14, 20, 10, 8, 6]
        })

def get_optimal_ranges():
    """Get optimal nutrient ranges for different crops"""
    return {
        'rice': {'ph': (5.5, 6.5), 'n': (200, 300), 'p': (20, 30), 'k': (150, 200)},
        'wheat': {'ph': (6.0, 7.5), 'n': (180, 250), 'p': (18, 25), 'k': (140, 180)},
        'cotton': {'ph': (5.8, 8.0), 'n': (150, 220), 'p': (15, 25), 'k': (120, 160)},
        'tomato': {'ph': (6.0, 6.8), 'n': (200, 280), 'p': (25, 35), 'k': (180, 240)},
        'potato': {'ph': (5.2, 6.4), 'n': (160, 240), 'p': (20, 30), 'k': (200, 280)},
        'maize': {'ph': (6.0, 6.8), 'n': (180, 260), 'p': (20, 28), 'k': (160, 220)},
        'sugarcane': {'ph': (6.5, 7.5), 'n': (250, 350), 'p': (30, 40), 'k': (200, 280)},
        'soybean': {'ph': (6.0, 7.0), 'n': (100, 150), 'p': (20, 30), 'k': (150, 200)}
    }

def analyze_soil_deficiency(ph, n, p, k, crop):
    """Analyze soil deficiency and recommend fertilizers"""
    optimal = get_optimal_ranges()
    crop_req = optimal.get(crop.lower(), optimal['wheat'])  # Default to wheat
    
    deficiencies = []
    recommendations = []
    
    # pH analysis
    if ph < crop_req['ph'][0]:
        deficiencies.append(f"pH too low ({ph:.1f}, need {crop_req['ph'][0]}-{crop_req['ph'][1]})")
        recommendations.append({
            'nutrient': 'pH (Alkalinity)',
            'product': 'Lime (CaCO3)',
            'quantity': f"{2-4} kg per acre",
            'reason': 'Increase soil pH',
            'cost_estimate': '₹200-400'
        })
    elif ph > crop_req['ph'][1]:
        deficiencies.append(f"pH too high ({ph:.1f}, need {crop_req['ph'][0]}-{crop_req['ph'][1]})")
        recommendations.append({
            'nutrient': 'pH (Acidity)',
            'product': 'Sulfur/Gypsum',
            'quantity': f"{3-5} kg per acre",
            'reason': 'Decrease soil pH',
            'cost_estimate': '₹300-500'
        })
    
    # Nitrogen analysis
    if n < crop_req['n'][0]:
        deficit = crop_req['n'][0] - n
        deficiencies.append(f"Nitrogen deficient (Current: {n} ppm, Need: {crop_req['n'][0]}-{crop_req['n'][1]} ppm)")
        recommendations.append({
            'nutrient': 'Nitrogen (N)',
            'product': 'Urea (46% N)',
            'quantity': f"{deficit*0.2:.1f} kg per acre",
            'reason': 'Promote vegetative growth',
            'cost_estimate': f"₹{deficit*0.2*6:.0f}-{deficit*0.2*8:.0f}"
        })
    
    # Phosphorus analysis
    if p < crop_req['p'][0]:
        deficit = crop_req['p'][0] - p
        deficiencies.append(f"Phosphorus deficient (Current: {p} ppm, Need: {crop_req['p'][0]}-{crop_req['p'][1]} ppm)")
        recommendations.append({
            'nutrient': 'Phosphorus (P)',
            'product': 'DAP (18-46-0)',
            'quantity': f"{deficit*1.5:.1f} kg per acre",
            'reason': 'Root development & flowering',
            'cost_estimate': f"₹{deficit*1.5*25:.0f}-{deficit*1.5*30:.0f}"
        })
    
    # Potassium analysis
    if k < crop_req['k'][0]:
        deficit = crop_req['k'][0] - k
        deficiencies.append(f"Potassium deficient (Current: {k} ppm, Need: {crop_req['k'][0]}-{crop_req['k'][1]} ppm)")
        recommendations.append({
            'nutrient': 'Potassium (K)',
            'product': 'MOP (60% K2O)',
            'quantity': f"{deficit*0.3:.1f} kg per acre",
            'reason': 'Disease resistance & fruit quality',
            'cost_estimate': f"₹{deficit*0.3*20:.0f}-{deficit*0.3*25:.0f}"
        })
    
    return deficiencies, recommendations

def create_nutrient_chart(ph, n, p, k, crop):
    """Create a radar chart showing nutrient levels"""
    optimal = get_optimal_ranges()
    crop_req = optimal.get(crop.lower(), optimal['wheat'])
    
    # Calculate percentage of optimal levels
    ph_optimal = (crop_req['ph'][0] + crop_req['ph'][1]) / 2
    n_optimal = (crop_req['n'][0] + crop_req['n'][1]) / 2
    p_optimal = (crop_req['p'][0] + crop_req['p'][1]) / 2
    k_optimal = (crop_req['k'][0] + crop_req['k'][1]) / 2
    
    current_levels = [
        min((ph / ph_optimal) * 100, 150),
        min((n / n_optimal) * 100, 150),
        min((p / p_optimal) * 100, 150),
        min((k / k_optimal) * 100, 150)
    ]
    
    categories = ['pH Level', 'Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)']
    
    fig = go.Figure()
    
    # Add optimal range (100%)
    fig.add_trace(go.Scatterpolar(
        r=[100, 100, 100, 100],
        theta=categories,
        fill='toself',
        name='Optimal Range',
        fillcolor='rgba(0,255,0,0.2)',
        line_color='green'
    ))
    
    # Add current levels
    fig.add_trace(go.Scatterpolar(
        r=current_levels,
        theta=categories,
        fill='toself',
        name='Current Levels',
        fillcolor='rgba(255,0,0,0.3)',
        line_color='red'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 150]
            )),
        showlegend=True,
        title=f"Soil Nutrient Analysis for {crop.title()}"
    )
    
    return fig

def run():
    """Main function for fertilizer recommendation module"""
    
    st.markdown("## 💡 Fertilizer Recommendation System")
    st.markdown("Get personalized fertilizer recommendations based on soil nutrient analysis.")
    
    # Input methods
    input_method = st.radio(
        "🔍 Choose Input Method:",
        ["Manual Entry", "Upload Soil Test Report", "Select from Database"],
        horizontal=True
    )
    
    if input_method == "Manual Entry":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Soil Test Results")
            
            ph_level = st.number_input(
                "🧪 pH Level:",
                min_value=3.0,
                max_value=10.0,
                value=6.8,
                step=0.1,
                help="Soil acidity/alkalinity level"
            )
            
            nitrogen = st.number_input(
                "🟢 Nitrogen (N) in ppm:",
                min_value=0,
                max_value=500,
                value=200,
                step=5,
                help="Available nitrogen in soil"
            )
            
            phosphorus = st.number_input(
                "🟡 Phosphorus (P) in ppm:",
                min_value=0,
                max_value=100,
                value=25,
                step=1,
                help="Available phosphorus in soil"
            )
            
            potassium = st.number_input(
                "🔵 Potassium (K) in ppm:",
                min_value=0,
                max_value=400,
                value=150,
                step=5,
                help="Available potassium in soil"
            )
        
        with col2:
            st.markdown("### 🌾 Crop Information")
            
            crop_type = st.selectbox(
                "🌱 Select Crop:",
                ["Rice", "Wheat", "Cotton", "Tomato", "Potato", "Maize", "Sugarcane", "Soybean"],
                help="Choose the crop you want to grow"
            )
            
            farm_area = st.number_input(
                "📏 Farm Area (acres):",
                min_value=0.1,
                max_value=1000.0,
                value=5.0,
                step=0.5
            )
            
            growth_stage = st.selectbox(
                "🌿 Growth Stage:",
                ["Pre-planting", "Vegetative", "Flowering", "Fruiting/Grain Filling"],
                help="Current stage of crop growth"
            )
            
            soil_type = st.selectbox(
                "🏞️ Soil Type:",
                ["Alluvial", "Black", "Red", "Laterite", "Sandy", "Clay", "Loamy"],
                help="Primary soil type of your field"
            )
    
    elif input_method == "Upload Soil Test Report":
        st.markdown("### 📄 Upload Soil Test Report")
        uploaded_file = st.file_uploader(
            "Choose a file (PDF/Image)",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            help="Upload your lab soil test report"
        )
        
        if uploaded_file:
            st.info("📋 File uploaded successfully! Manual extraction not implemented - please use manual entry for now.")
            st.markdown("**Expected format:** pH, N-P-K values, Organic Matter %")
        
        # Fallback to manual entry
        st.markdown("### ⚡ Quick Entry (from report)")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            ph_level = st.number_input("pH", 3.0, 10.0, 6.8, 0.1)
        with col2:
            nitrogen = st.number_input("N (ppm)", 0, 500, 200, 5)
        with col3:
            phosphorus = st.number_input("P (ppm)", 0, 100, 25, 1)
        with col4:
            potassium = st.number_input("K (ppm)", 0, 400, 150, 5)
        
        crop_type = st.selectbox("Crop:", ["Rice", "Wheat", "Cotton", "Tomato", "Potato", "Maize", "Sugarcane", "Soybean"])
        farm_area = st.number_input("Area (acres):", 0.1, 1000.0, 5.0, 0.5)
        growth_stage = "Pre-planting"
        soil_type = "Alluvial"
    
    elif input_method == "Select from Database":
        st.markdown("### 🗃️ Select from Database")
        soil_data = load_soil_health_data()
        
        selected_region = st.selectbox(
            "📍 Select Region:",
            soil_data['region'].unique(),
            help="Choose a region with similar soil conditions"
        )
        
        region_data = soil_data[soil_data['region'] == selected_region].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            ph_level = st.number_input("pH", value=float(region_data['ph_level']), step=0.1)
        with col2:
            nitrogen = st.number_input("N (ppm)", value=int(region_data['nitrogen_ppm']), step=5)
        with col3:
            phosphorus = st.number_input("P (ppm)", value=int(region_data['phosphorus_ppm']), step=1)
        with col4:
            potassium = st.number_input("K (ppm)", value=int(region_data['potassium_ppm']), step=5)
        
        st.info(f"📊 Using soil data from {selected_region} region ({region_data['soil_type']} soil)")
        
        crop_type = st.selectbox("Crop:", ["Rice", "Wheat", "Cotton", "Tomato", "Potato", "Maize", "Sugarcane", "Soybean"])
        farm_area = st.number_input("Area (acres):", 0.1, 1000.0, 5.0, 0.5)
        growth_stage = st.selectbox("Growth Stage:", ["Pre-planting", "Vegetative", "Flowering", "Fruiting/Grain Filling"])
        soil_type = region_data['soil_type']
    
    # Analysis button
    if st.button("🔬 Analyze Soil & Get Recommendations", type="primary"):
        
        # Analyze deficiencies
        deficiencies, recommendations = analyze_soil_deficiency(
            ph_level, nitrogen, phosphorus, potassium, crop_type
        )
        
        st.markdown("---")
        
        # Current soil status
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("## 📈 Soil Analysis Results")
            
            # Nutrient radar chart
            fig = create_nutrient_chart(ph_level, nitrogen, phosphorus, potassium, crop_type)
            st.plotly_chart(fig, use_container_width=True)
            
            # Current values table
            current_data = pd.DataFrame({
                'Parameter': ['pH Level', 'Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)'],
                'Current Value': [f"{ph_level:.1f}", f"{nitrogen} ppm", f"{phosphorus} ppm", f"{potassium} ppm"],
                'Status': ['✅ Optimal' if len([d for d in deficiencies if 'pH' in d]) == 0 else '⚠️ Needs Attention',
                          '✅ Adequate' if nitrogen >= 180 else '🔴 Low',
                          '✅ Adequate' if phosphorus >= 20 else '🔴 Low',
                          '✅ Adequate' if potassium >= 150 else '🔴 Low']
            })
            
            st.dataframe(current_data, hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("## 💊 Fertilizer Recommendations")
            
            if recommendations:
                total_cost_min = 0
                total_cost_max = 0
                
                for i, rec in enumerate(recommendations):
                    with st.expander(f"🧪 {rec['nutrient']} - {rec['product']}", expanded=i==0):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown(f"**Quantity per acre:** {rec['quantity']}")
                            st.markdown(f"**Total for {farm_area} acres:** {float(rec['quantity'].split()[0]) * farm_area:.1f} kg")
                            st.markdown(f"**Purpose:** {rec['reason']}")
                        
                        with col_b:
                            st.markdown(f"**Cost per acre:** {rec['cost_estimate']}")
                            
                            # Extract cost range
                            cost_str = rec['cost_estimate'].replace('₹', '').replace(',', '')
                            if '-' in cost_str:
                                cost_min, cost_max = map(int, cost_str.split('-'))
                            else:
                                cost_min = cost_max = int(cost_str)
                            
                            total_cost_min += cost_min * farm_area
                            total_cost_max += cost_max * farm_area
                            
                            st.markdown(f"**Your total cost:** ₹{cost_min * farm_area:,.0f} - ₹{cost_max * farm_area:,.0f}")
                
                # Cost summary
                st.markdown("### 💰 Total Investment Summary")
                st.success(f"**Total fertilizer cost for {farm_area} acres:** ₹{total_cost_min:,.0f} - ₹{total_cost_max:,.0f}")
                
            else:
                st.success("🎉 Your soil is well-balanced for the selected crop!")
                st.info("💡 Consider maintenance doses of balanced fertilizer during the growing season.")
        
        # Detailed recommendations
        st.markdown("---")
        st.markdown("## 📋 Detailed Application Schedule")
        
        if recommendations:
            schedule_data = []
            
            for rec in recommendations:
                if 'Nitrogen' in rec['nutrient']:
                    schedule_data.extend([
                        ['Pre-planting', 'Urea', f"{float(rec['quantity'].split()[0]) * 0.3:.1f} kg/acre", 'Basal dose'],
                        ['Vegetative stage', 'Urea', f"{float(rec['quantity'].split()[0]) * 0.4:.1f} kg/acre", 'First top-dress'],
                        ['Flowering stage', 'Urea', f"{float(rec['quantity'].split()[0]) * 0.3:.1f} kg/acre", 'Final top-dress']
                    ])
                else:
                    schedule_data.append(['Pre-planting', rec['product'], rec['quantity'], 'Full dose at planting'])
            
            if schedule_data:
                schedule_df = pd.DataFrame(schedule_data, columns=['Stage', 'Fertilizer', 'Quantity', 'Application Method'])
                st.dataframe(schedule_df, hide_index=True, use_container_width=True)
        
        # Additional recommendations
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("## 🌱 Organic Amendments")
            st.markdown("""
            **Recommended organic additions:**
            - 🐄 Farmyard manure: 5-10 tons/acre
            - 🍃 Compost: 2-3 tons/acre  
            - 🌾 Green manure crops before main crop
            - 🦠 Bio-fertilizers (Rhizobium, PSB, KSB)
            """)
            
            st.markdown("## ⚠️ Application Tips")
            st.markdown("""
            - Apply phosphorus and potassium at planting
            - Split nitrogen into 2-3 applications
            - Apply fertilizers before irrigation
            - Mix with soil immediately after application
            """)
        
        with col2:
            st.markdown("## 📊 Expected Benefits")
            
            # Yield improvement estimate
            improvement_factors = {
                'low_nutrients': 1.3,  # 30% improvement
                'medium_nutrients': 1.2,  # 20% improvement
                'adequate_nutrients': 1.1  # 10% improvement
            }
            
            nutrient_status = 'adequate_nutrients'
            if len(recommendations) >= 3:
                nutrient_status = 'low_nutrients'
            elif len(recommendations) >= 1:
                nutrient_status = 'medium_nutrients'
            
            expected_improvement = improvement_factors[nutrient_status]
            
            # Base yields (qt/acre)
            base_yields = {
                'Rice': 25, 'Wheat': 30, 'Cotton': 8, 'Tomato': 400,
                'Potato': 200, 'Maize': 28, 'Sugarcane': 800, 'Soybean': 15
            }
            
            base_yield = base_yields.get(crop_type, 25)
            improved_yield = base_yield * expected_improvement
            additional_yield = improved_yield - base_yield
            
            st.metric("Expected Yield Increase", f"{additional_yield:.1f} qt/acre", f"{(expected_improvement-1)*100:.0f}%")
            st.metric("Total Expected Yield", f"{improved_yield:.1f} qt/acre")
            
            # ROI calculation (simplified)
            crop_prices = {'Rice': 2000, 'Wheat': 2200, 'Cotton': 5500, 'Tomato': 1500, 
                          'Potato': 1200, 'Maize': 1800, 'Sugarcane': 350, 'Soybean': 4000}
            
            price = crop_prices.get(crop_type, 2000)
            additional_revenue = additional_yield * price * farm_area
            investment = (total_cost_min + total_cost_max) / 2
            
            if investment > 0:
                roi = ((additional_revenue - investment) / investment) * 100
                st.metric("Expected ROI", f"{roi:.0f}%", "Return on Investment")
        
        # Soil health monitoring
        st.markdown("---")
        st.markdown("## 🔬 Soil Health Monitoring")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📅 Testing Schedule")
            st.info("""
            **Annual:** Complete NPK + pH test
            **Bi-annual:** Quick N test during crop season
            **Every 3 years:** Micronutrient analysis
            """)
        
        with col2:
            st.markdown("### 🎯 Target Levels")
            optimal = get_optimal_ranges()
            crop_req = optimal.get(crop_type.lower(), optimal['wheat'])
            st.success(f"""
            **For {crop_type}:**
            - pH: {crop_req['ph'][0]} - {crop_req['ph'][1]}
            - N: {crop_req['n'][0]} - {crop_req['n'][1]} ppm
            - P: {crop_req['p'][0]} - {crop_req['p'][1]} ppm
            - K: {crop_req['k'][0]} - {crop_req['k'][1]} ppm
            """)
        
        with col3:
            st.markdown("### 📞 Expert Support")
            st.markdown("""
            **Need help?**
            - 📱 SMS: Send soil test to 54321
            - 🌐 Web: soilhealth.gov.in  
            - 👨‍🌾 Local agriculture officer
            - 🔬 Nearest soil testing lab
            """)

if __name__ == "__main__":
    run()