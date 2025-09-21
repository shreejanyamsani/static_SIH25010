import streamlit as st
import pandas as pd
from pathlib import Path
import numpy as np
from PIL import Image

def load_pest_disease_data():
    """Load pest and disease data"""
    data_path = Path(__file__).parent.parent / "data" / "pest_disease_dataset.csv"
    if data_path.exists():
        return pd.read_csv(data_path)
    else:
        # Sample data if file doesn't exist
        return pd.DataFrame({
            'pest_disease_id': ['PD001', 'PD002', 'PD003', 'PD004', 'PD005', 'PD006', 'PD007', 'PD008', 'PD009', 'PD010'],
            'name': ['Aphids', 'Leaf Blight', 'Stem Borer', 'Powdery Mildew', 'Bollworm', 'Root Rot', 'Thrips', 'Bacterial Wilt', 'Whitefly', 'Rust Disease'],
            'type': ['Pest', 'Disease', 'Pest', 'Disease', 'Pest', 'Disease', 'Pest', 'Disease', 'Pest', 'Disease'],
            'affected_crops': ['Wheat,Rice,Cotton', 'Rice,Wheat', 'Rice,Maize', 'Tomato,Cucumber,Grapes', 'Cotton,Tomato', 'Tomato,Potato', 'Cotton,Onion', 'Tomato,Potato,Chili', 'Cotton,Tomato,Cabbage', 'Wheat,Barley'],
            'symptoms': ['Small green/black insects on leaves', 'Brown spots on leaves, yellowing', 'Holes in stem, white larvae inside', 'White powdery coating on leaves', 'Caterpillars eating fruits/bolls', 'Wilting, brown roots, stunted growth', 'Tiny insects, silver streaks on leaves', 'Wilting, brown vascular bundles', 'Tiny white flying insects under leaves', 'Orange/brown pustules on leaves'],
            'severity_level': ['Medium', 'High', 'High', 'Medium', 'High', 'Very High', 'Medium', 'Very High', 'Medium', 'High'],
            'season': ['Winter,Spring', 'Monsoon', 'Monsoon,Post-Monsoon', 'Winter,Spring', 'Monsoon,Post-Monsoon', 'Monsoon', 'Summer,Winter', 'Summer,Monsoon', 'All Year', 'Winter,Spring'],
            'organic_treatment': ['Neem oil spray, ladybird release', 'Copper fungicide, crop rotation', 'Bt spray, remove affected stems', 'Milk spray, sulfur dusting', 'Bt spray, pheromone traps', 'Improve drainage, copper spray', 'Blue sticky traps, neem oil', 'Copper spray, remove affected plants', 'Yellow sticky traps, neem oil', 'Sulfur spray, resistant varieties'],
            'chemical_treatment': ['Imidacloprid, Dimethoate', 'Mancozeb, Propiconazole', 'Chlorantraniliprole, Fipronil', 'Myclobutanil, Tebuconazole', 'Cypermethrin, Spinosad', 'Metalaxyl, Fosetyl-Al', 'Spinosad, Thiamethoxam', 'Streptomycin, Copper Oxychloride', 'Thiamethoxam, Spiromesifen', 'Propiconazole, Tebuconazole'],
            'prevention': ['Regular monitoring, balanced nutrition', 'Proper spacing, avoid overhead irrigation', 'Clean cultivation, remove crop residues', 'Good air circulation, avoid overcrowding', 'Regular monitoring, destroy egg masses', 'Well-drained soil, avoid waterlogging', 'Remove weeds, use reflective mulch', 'Certified seeds, crop rotation', 'Remove weeds, use reflective mulch', 'Resistant varieties, proper nutrition'],
            'economic_threshold': ['5-10 per plant', '10% leaf area affected', '2-5% stems damaged', '5% leaf area covered', '1-2 larvae per plant', 'First symptoms appear', '5-10 per leaf', 'First wilting symptoms', '5-10 per leaf', '10% leaf area affected']
        })

def analyze_image_simple(image, crop_type):
    """Simple image analysis - placeholder for actual ML model"""
    # This is a simplified version - in production, you'd use ML models
    
    # Convert image to array for basic analysis
    img_array = np.array(image)
    
    # Basic color analysis
    avg_color = np.mean(img_array, axis=(0, 1))
    
    # Simple heuristics based on color
    possible_issues = []
    
    # Check for yellowing (high yellow component)
    if len(avg_color) >= 3:
        yellow_ratio = avg_color[1] / (avg_color[2] + 1)  # Green/Blue ratio
        if yellow_ratio > 1.2:
            possible_issues.append("Nutrient deficiency or disease causing yellowing")
    
    # Check for brown spots (low overall brightness with brown tint)
    brightness = np.mean(avg_color)
    if brightness < 100:
        possible_issues.append("Possible fungal infection or blight")
    
    # Check for white patches (high brightness in localized areas)
    if brightness > 200:
        possible_issues.append("Possible powdery mildew or pest damage")
    
    return possible_issues

def get_crop_specific_pests(crop_type, season):
    """Get pests/diseases specific to crop and season"""
    df = load_pest_disease_data()
    
    # Filter by crop
    crop_pests = df[df['affected_crops'].str.contains(crop_type, case=False, na=False)]
    
    # Filter by season
    if season != "All Year":
        season_pests = crop_pests[crop_pests['season'].str.contains(season, case=False, na=False) | 
                                 crop_pests['season'].str.contains('All Year', case=False, na=False)]
    else:
        season_pests = crop_pests
    
    return season_pests

def run():
    """Main function for pest detection module"""
    
    st.markdown("## 🐛 Pest & Disease Detection System")
    st.markdown("Upload crop images or describe symptoms to identify potential pest and disease issues.")
    
    # Input method selection
    detection_method = st.radio(
        "🔍 Choose Detection Method:",
        ["Image Upload", "Symptom Description", "Crop-Season Analysis"],
        horizontal=True
    )
    
    if detection_method == "Image Upload":
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📸 Upload Plant Image")
            
            uploaded_image = st.file_uploader(
                "Choose an image file:",
                type=['jpg', 'jpeg', 'png'],
                help="Upload a clear image of the affected plant part"
            )
            
            crop_type = st.selectbox(
                "🌱 Crop Type:",
                ["Rice", "Wheat", "Cotton", "Tomato", "Potato", "Maize", "Onion", "Chili"],
                help="Select the crop in the image"
            )
            
            current_season = st.selectbox(
                "📅 Current Season:",
                ["Monsoon", "Post-Monsoon", "Winter", "Spring", "Summer", "All Year"]
            )
            
            if uploaded_image is not None:
                image = Image.open(uploaded_image)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                if st.button("🔍 Analyze Image", type="primary"):
                    with st.spinner("Analyzing image..."):
                        # Simple analysis
                        image_issues = analyze_image_simple(image, crop_type)
                        
                        # Get crop-specific pests for context
                        crop_pests = get_crop_specific_pests(crop_type, current_season)
                        
                        with col2:
                            st.markdown("### 📊 Analysis Results")
                            
                            if image_issues:
                                st.warning("🚨 Potential Issues Detected:")
                                for issue in image_issues:
                                    st.write(f"• {issue}")
                            else:
                                st.success("✅ No obvious issues detected in the image")
                            
                            st.markdown("### 🎯 Common Issues for Your Crop")
                            
                            if not crop_pests.empty:
                                # Show top 3 most likely pests/diseases
                                priority_order = {'Very High': 4, 'High': 3, 'Medium': 2, 'Low': 1}
                                crop_pests['severity_score'] = crop_pests['severity_level'].map(priority_order)
                                top_pests = crop_pests.nlargest(3, 'severity_score')
                                
                                for idx, (_, pest) in enumerate(top_pests.iterrows()):
                                    with st.expander(f"🔍 {pest['name']} ({pest['type']})", expanded=idx==0):
                                        
                                        col_a, col_b = st.columns(2)
                                        
                                        with col_a:
                                            st.markdown("**🔍 Symptoms:**")
                                            st.write(pest['symptoms'])
                                            st.markdown(f"**⚠️ Severity:** {pest['severity_level']}")
                                            st.markdown(f"**📅 Season:** {pest['season']}")
                                        
                                        with col_b:
                                            st.markdown("**🌿 Organic Treatment:**")
                                            st.success(pest['organic_treatment'])
                                            st.markdown("**⚗️ Chemical Treatment:**")
                                            st.info(pest['chemical_treatment'])
    
    elif detection_method == "Symptom Description":
        st.markdown("### 📝 Describe the Symptoms")
        
        col1, col2 = st.columns(2)
        
        with col1:
            crop_type = st.selectbox(
                "🌱 Affected Crop:",
                ["Rice", "Wheat", "Cotton", "Tomato", "Potato", "Maize", "Onion", "Chili"]
            )
            
            plant_part = st.selectbox(
                "🌿 Affected Plant Part:",
                ["Leaves", "Stem", "Fruits/Bolls", "Roots", "Flowers", "Entire Plant"]
            )
            
            symptoms = st.multiselect(
                "🔍 Select Observed Symptoms:",
                [
                    "Yellowing leaves", "Brown spots", "White patches", "Holes in leaves",
                    "Wilting", "Stunted growth", "Insects visible", "Sticky honeydew",
                    "Caterpillars present", "Flying insects", "Root damage", "Fruit damage"
                ]
            )
        
        with col2:
            severity = st.selectbox(
                "📊 Severity Level:",
                ["Just started", "Moderate spread", "Severe damage", "Crop failure threat"]
            )
            
            duration = st.selectbox(
                "⏰ How long noticed:",
                ["1-2 days", "3-7 days", "1-2 weeks", "More than 2 weeks"]
            )
            
            weather_conditions = st.multiselect(
                "🌤️ Recent Weather:",
                ["Heavy rain", "Drought", "High humidity", "Temperature fluctuation", "Normal weather"]
            )
        
        symptom_text = st.text_area(
            "📋 Additional Details:",
            placeholder="Describe any other symptoms, patterns, or observations..."
        )
        
        if st.button("🔍 Find Matching Issues", type="primary"):
            st.markdown("---")
            st.markdown("### 🎯 Possible Matches")
            
            df = load_pest_disease_data()
            
            # Simple keyword matching
            matches = []
            for _, row in df.iterrows():
                if crop_type.lower() in row['affected_crops'].lower():
                    score = 0
                    symptom_keywords = row['symptoms'].lower()
                    
                    # Check symptom matches
                    for symptom in symptoms:
                        if any(word in symptom_keywords for word in symptom.lower().split()):
                            score += 1
                    
                    if score > 0:
                        matches.append((row, score))
            
            # Sort by match score
            matches.sort(key=lambda x: x[1], reverse=True)
            
            if matches:
                for i, (pest, score) in enumerate(matches[:3]):
                    confidence = min(score * 30, 95)  # Simple confidence calculation
                    
                    with st.expander(f"🎯 Match #{i+1}: {pest['name']} ({confidence}% match)", expanded=i==0):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown("**🔍 Full Symptom Description:**")
                            st.write(pest['symptoms'])
                            st.markdown(f"**⚠️ Severity:** {pest['severity_level']}")
                            st.markdown(f"**📊 Economic Threshold:** {pest['economic_threshold']}")
                        
                        with col_b:
                            st.markdown("**🌿 Organic Treatment:**")
                            st.success(pest['organic_treatment'])
                            st.markdown("**⚗️ Chemical Treatment:**")
                            st.info(pest['chemical_treatment'])
                            st.markdown("**🛡️ Prevention:**")
                            st.warning(pest['prevention'])
            else:
                st.warning("No direct matches found. Please try the Crop-Season Analysis or consult with local experts.")
    
    elif detection_method == "Crop-Season Analysis":
        st.markdown("### 📊 Crop-Season Pest Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            crop_type = st.selectbox(
                "🌱 Your Crop:",
                ["Rice", "Wheat", "Cotton", "Tomato", "Potato", "Maize", "Onion", "Chili"]
            )
        
        with col2:
            current_season = st.selectbox(
                "📅 Current Season:",
                ["Monsoon", "Post-Monsoon", "Winter", "Spring", "Summer", "All Year"]
            )
        
        with col3:
            growth_stage = st.selectbox(
                "🌿 Growth Stage:",
                ["Seedling", "Vegetative", "Flowering", "Fruiting", "Maturity"]
            )
        
        if st.button("📋 Get Seasonal Pest Report", type="primary"):
            crop_pests = get_crop_specific_pests(crop_type, current_season)
            
            if not crop_pests.empty:
                st.markdown("---")
                st.markdown(f"## 🎯 Common Pests & Diseases for {crop_type} in {current_season}")
                
                # Separate pests and diseases
                pests = crop_pests[crop_pests['type'] == 'Pest']
                diseases = crop_pests[crop_pests['type'] == 'Disease']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if not pests.empty:
                        st.markdown("### 🐛 Common Pests")
                        for _, pest in pests.iterrows():
                            severity_color = {
                                'Low': '🟢', 'Medium': '🟡', 
                                'High': '🟠', 'Very High': '🔴'
                            }
                            
                            st.markdown(f"**{severity_color.get(pest['severity_level'], '⚪')} {pest['name']}**")
                            st.caption(pest['symptoms'])
                            st.caption(f"Economic Threshold: {pest['economic_threshold']}")
                            st.markdown("---")
                
                with col2:
                    if not diseases.empty:
                        st.markdown("### 🦠 Common Diseases")
                        for _, disease in diseases.iterrows():
                            severity_color = {
                                'Low': '🟢', 'Medium': '🟡', 
                                'High': '🟠', 'Very High': '🔴'
                            }
                            
                            st.markdown(f"**{severity_color.get(disease['severity_level'], '⚪')} {disease['name']}**")
                            st.caption(disease['symptoms'])
                            st.caption(f"Economic Threshold: {disease['economic_threshold']}")
                            st.markdown("---")
                
                # Treatment recommendations
                st.markdown("### 💊 Treatment Options")
                
                priority_order = {'Very High': 4, 'High': 3, 'Medium': 2, 'Low': 1}
                crop_pests['severity_score'] = crop_pests['severity_level'].map(priority_order)
                top_threats = crop_pests.nlargest(3, 'severity_score')
                
                for _, threat in top_threats.iterrows():
                    with st.expander(f"🎯 {threat['name']} - Treatment Guide"):
                        
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            st.markdown("**🌿 Organic Approach**")
                            st.success(threat['organic_treatment'])
                            st.caption("✅ Safe for environment")
                            st.caption("✅ No chemical residues")
                        
                        with col_b:
                            st.markdown("**⚗️ Chemical Control**")
                            st.info(threat['chemical_treatment'])
                            st.caption("⚡ Fast acting")
                            st.caption("⚠️ Follow safety guidelines")
                        
                        with col_c:
                            st.markdown("**🛡️ Prevention**")
                            st.warning(threat['prevention'])
                            st.caption("🎯 Best long-term strategy")
                            st.caption("💰 Cost effective")
    
    # Information panels
    st.markdown("---")
    st.markdown("## 📚 Pest Management Guide")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.expander("🔍 Early Detection Tips"):
            st.markdown("""
            **Daily Monitoring:**
            - Check plants early morning
            - Look under leaves for eggs/insects
            - Monitor new growth areas
            - Check soil around plants
            
            **Weekly Scouting:**
            - Count pests per plant
            - Record damage levels
            - Check neighboring fields
            - Document weather conditions
            
            **Use Tools:**
            - Magnifying glass
            - Yellow/blue sticky traps
            - Pheromone traps
            - Beat sheet sampling
            """)
    
    with col2:
        with st.expander("🌿 Integrated Pest Management (IPM)"):
            st.markdown("""
            **IPM Pyramid:**
            1. **Prevention** (Base)
               - Resistant varieties
               - Crop rotation
               - Proper nutrition
            
            2. **Cultural Controls**
               - Timely planting
               - Field sanitation
               - Water management
            
            3. **Biological Controls**
               - Natural predators
               - Beneficial insects
               - Bio-pesticides
            
            4. **Chemical Controls** (Last resort)
               - Selective pesticides
               - Rotation of chemicals
               - Follow economic thresholds
            """)
    
    with col3:
        with st.expander("📊 Economic Thresholds"):
            st.markdown("""
            **Key Concepts:**
            - **Economic Injury Level (EIL):** Pest density causing economic loss
            - **Economic Threshold (ET):** When to start treatment
            - **Action Threshold:** Pest level requiring immediate action
            
            **Benefits:**
            - Reduces unnecessary spraying
            - Saves money on pesticides
            - Preserves beneficial insects
            - Prevents resistance development
            
            **Monitoring Schedule:**
            - Vegetative: Weekly
            - Reproductive: 2-3 times/week
            - Critical stages: Daily
            """)
    
    # Emergency contacts and resources
    st.markdown("---")
    st.markdown("## 🆘 Emergency Support")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📞 Emergency Contacts")
        st.info("""
        **Pest Outbreak Hotline:**
        📱 1800-180-1551
        
        **State Agriculture Dept:**
        🏛️ Contact local KVK
        
        **Plant Protection Officer:**
        👨‍🌾 District collector office
        
        **Pesticide Poisoning:**
        🚑 102 (Medical emergency)
        """)
    
    with col2:
        st.markdown("### 🌐 Online Resources")
        st.success("""
        **Government Portals:**
        - plantix.net/en/library
        - farmer.gov.in
        - mkisan.gov.in
        
        **Mobile Apps:**
        - CropIn
        - AgriApp
        - Kisan Suvidha
        
        **Weather & Alerts:**
        - IMD Agromet
        - Meghdoot App
        """)
    
    with col3:
        st.markdown("### 🧪 Diagnostic Labs")
        st.warning("""
        **Send samples to:**
        - State Agricultural Universities
        - ICAR institutes
        - Private diagnostic labs
        
        **Sample Guidelines:**
        - Fresh specimens preferred
        - Multiple affected parts
        - Include healthy tissue
        - Proper packaging
        
        **Turn-around time:**
        - Visual diagnosis: Same day
        - Lab tests: 2-5 days
        - Molecular tests: 7-10 days
        """)
    
    # Seasonal calendar
    st.markdown("---")
    st.markdown("## 📅 Seasonal Pest Calendar")
    
    # Create a simple seasonal calendar
    calendar_data = {
        'Season': ['Summer', 'Monsoon', 'Post-Monsoon', 'Winter', 'Spring'],
        'Common Pests': [
            'Thrips, Whitefly, Spider mites',
            'Stem borer, Leaf folder, BPH',
            'Bollworm, Aphids, Jassids', 
            'Aphids, Thrips, Cut worms',
            'Thrips, Aphids, Early shoot borer'
        ],
        'Common Diseases': [
            'Powdery mildew, Leaf curl',
            'Blast, Blight, Root rot',
            'Late blight, Downy mildew',
            'Rust, Smut, Wilt',
            'Early blight, Anthracnose'
        ],
        'Management Focus': [
            'Water stress monitoring',
            'Drainage, fungicide sprays',
            'Harvest timing, storage',
            'Soil preparation, seed treatment',
            'Early detection, preventive sprays'
        ]
    }
    
    calendar_df = pd.DataFrame(calendar_data)
    st.dataframe(calendar_df, hide_index=True, use_container_width=True)
    
    # Cost calculator
    st.markdown("---")
    st.markdown("## 💰 Treatment Cost Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        treatment_type = st.selectbox("Treatment Type:", ["Organic", "Chemical", "Biological"])
        farm_area = st.number_input("Farm Area (acres):", 1.0, 1000.0, 5.0, 0.5)
    
    with col2:
        severity = st.selectbox("Infestation Level:", ["Low", "Medium", "High", "Severe"])
        application_method = st.selectbox("Application:", ["Manual spray", "Tractor spray", "Drone spray"])
    
    with col3:
        if st.button("💰 Calculate Cost"):
            # Simple cost calculation
            base_costs = {
                'Organic': {'Low': 200, 'Medium': 350, 'High': 500, 'Severe': 700},
                'Chemical': {'Low': 300, 'Medium': 500, 'High': 800, 'Severe': 1200},
                'Biological': {'Low': 400, 'Medium': 600, 'High': 900, 'Severe': 1300}
            }
            
            method_multiplier = {'Manual spray': 1.0, 'Tractor spray': 1.2, 'Drone spray': 1.5}
            
            base_cost = base_costs[treatment_type][severity]
            total_cost = base_cost * farm_area * method_multiplier[application_method]
            
            st.metric("Estimated Cost", f"₹{total_cost:,.0f}")
            st.caption(f"₹{total_cost/farm_area:.0f} per acre")
    
    # Success stories
    st.markdown("---")
    st.markdown("## 🏆 Success Stories")
    
    success_stories = [
        {
            'farmer': 'Raj Kumar, Punjab',
            'crop': 'Rice',
            'problem': 'Stem borer infestation',
            'solution': 'IPM approach with pheromone traps',
            'result': '40% reduction in pesticide use, 15% yield increase'
        },
        {
            'farmer': 'Sita Devi, Maharashtra',
            'crop': 'Cotton',
            'problem': 'Bollworm resistance',
            'solution': 'Bt cotton + refuge strategy',
            'result': 'Sustainable pest control, ₹25,000/acre profit'
        },
        {
            'farmer': 'Kumar Singh, Uttar Pradesh',
            'crop': 'Tomato',
            'problem': 'Early blight disease',
            'solution': 'Copper spray + resistant variety',
            'result': '80% disease reduction, quality improvement'
        }
    ]
    
    for story in success_stories:
        with st.expander(f"🌟 {story['farmer']} - {story['crop']} Success"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Problem:** {story['problem']}")
                st.markdown(f"**Solution:** {story['solution']}")
            with col_b:
                st.success(f"**Result:** {story['result']}")

if __name__ == "__main__":
    run()