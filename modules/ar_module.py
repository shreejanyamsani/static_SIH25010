import streamlit as st
from pathlib import Path

def get_video_tutorials():
    """Get available video tutorials"""
    return {
        'soil_preparation': {
            'title': '🌱 Soil Preparation Techniques',
            'description': 'Learn proper soil preparation methods for different crops',
            'duration': '5:30',
            'difficulty': 'Beginner',
            'file': 'soil_prep_demo.mp4',
            'topics': ['Land leveling', 'Soil testing', 'Organic matter', 'pH adjustment'],
            'crops': ['Rice', 'Wheat', 'Cotton', 'Vegetables']
        },
        'seed_treatment': {
            'title': '🌾 Seed Treatment Methods',
            'description': 'Proper seed treatment for better germination and disease resistance',
            'duration': '4:15',
            'difficulty': 'Beginner',
            'file': 'seed_treatment_demo.mp4',
            'topics': ['Fungicide treatment', 'Bio-agent coating', 'Priming techniques'],
            'crops': ['Wheat', 'Rice', 'Pulses', 'Oilseeds']
        },
        'irrigation_systems': {
            'title': '💧 Modern Irrigation Systems',
            'description': 'Installation and maintenance of drip and sprinkler systems',
            'duration': '7:45',
            'difficulty': 'Intermediate',
            'file': 'irrigation_demo.mp4',
            'topics': ['Drip installation', 'Sprinkler setup', 'Water scheduling', 'Maintenance'],
            'crops': ['Cotton', 'Tomato', 'Fruits', 'Vegetables']
        },
        'pest_identification': {
            'title': '🐛 Pest Identification Guide',
            'description': 'Identify common pests and their damage symptoms',
            'duration': '6:20',
            'difficulty': 'Intermediate',
            'file': 'pest_id_demo.mp4',
            'topics': ['Visual identification', 'Damage patterns', 'Life cycles', 'Monitoring'],
            'crops': ['Rice', 'Cotton', 'Tomato', 'Chili']
        },
        'organic_farming': {
            'title': '🌿 Organic Farming Practices',
            'description': 'Sustainable and organic farming techniques',
            'duration': '8:10',
            'difficulty': 'Advanced',
            'file': 'organic_demo.mp4',
            'topics': ['Composting', 'Bio-pesticides', 'Crop rotation', 'Companion planting'],
            'crops': ['Vegetables', 'Fruits', 'Herbs', 'Pulses']
        },
        'harvesting_techniques': {
            'title': '✂️ Harvesting & Post-Harvest',
            'description': 'Proper harvesting timing and post-harvest handling',
            'duration': '5:55',
            'difficulty': 'Intermediate',
            'file': 'harvest_demo.mp4',
            'topics': ['Maturity indicators', 'Harvesting tools', 'Drying techniques', 'Storage'],
            'crops': ['Wheat', 'Rice', 'Maize', 'Pulses']
        }
    }

def create_ar_experience_demo():
    """Create a simulated AR experience"""
    
    st.markdown("### 🥽 Virtual Reality Learning Experience")
    st.markdown("*Note: This is a demo simulation of AR/VR functionality*")
    
    # AR experience selector
    ar_experiences = {
        '3D Crop Growth Simulation': {
            'description': 'Watch crops grow from seed to harvest in 3D',
            'icon': '🌱➡️🌾',
            'features': ['Time-lapse growth', 'Nutrient effects', 'Pest damage visualization']
        },
        'Virtual Farm Tour': {
            'description': 'Explore different farming techniques in virtual environment',
            'icon': '🚜🏞️',
            'features': ['Modern machinery', 'Sustainable practices', 'Crop diversity']
        },
        'Pest Detection Training': {
            'description': 'Interactive pest identification in realistic farm settings',
            'icon': '🔍🐛',
            'features': ['Real-time scanning', 'Symptom analysis', 'Treatment recommendations']
        },
        'Soil Analysis Simulator': {
            'description': 'Visualize soil composition and nutrient levels',
            'icon': '🔬🌍',
            'features': ['Layer visualization', 'Nutrient mapping', 'pH indicators']
        }
    }
    
    selected_experience = st.selectbox(
        "🎯 Choose AR Experience:",
        list(ar_experiences.keys())
    )
    
    experience_info = ar_experiences[selected_experience]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"#### {experience_info['icon']} {selected_experience}")
        st.markdown(experience_info['description'])
        
        st.markdown("**Features:**")
        for feature in experience_info['features']:
            st.write(f"• {feature}")
        
        # Simulate AR experience
        if st.button(f"🚀 Start {selected_experience}", type="primary"):
            with st.spinner("Loading AR experience..."):
                import time
                time.sleep(2)  # Simulate loading
                
                st.success("🥽 AR Experience Started!")
                
                # Create a placeholder for AR content
                ar_placeholder = st.empty()
                
                if selected_experience == '3D Crop Growth Simulation':
                    simulate_crop_growth(ar_placeholder)
                elif selected_experience == 'Virtual Farm Tour':
                    simulate_farm_tour(ar_placeholder)
                elif selected_experience == 'Pest Detection Training':
                    simulate_pest_detection(ar_placeholder)
                elif selected_experience == 'Soil Analysis Simulator':
                    simulate_soil_analysis(ar_placeholder)
    
    with col2:
        st.markdown("#### 📱 AR Requirements")
        st.info("""
        **Device Requirements:**
        - Smartphone with camera
        - AR-capable device
        - Good lighting conditions
        - Stable internet connection
        
        **Supported Devices:**
        - Android 7.0+ (ARCore)
        - iOS 11+ (ARKit)
        - VR Headsets (optional)
        """)
        
        st.markdown("#### 🎓 Learning Benefits")
        st.success("""
        **Enhanced Learning:**
        - Visual understanding
        - Interactive experience
        - Better retention
        - Practical application
        
        **Accessibility:**
        - Multiple languages
        - Offline capability
        - Voice instructions
        - Text alternatives
        """)

def simulate_crop_growth(placeholder):
    """Simulate 3D crop growth visualization"""
    
    growth_stages = [
        "🌰 Seed planted in soil",
        "🌱 Germination begins",
        "🌿 Seedling emerges",
        "🌾 Vegetative growth",
        "🌻 Flowering stage",
        "🌾 Fruit/grain development",
        "🌾 Maturation complete"
    ]
    
    with placeholder.container():
        st.markdown("### 🌱 3D Crop Growth Simulation")
        
        progress_bar = st.progress(0)
        stage_display = st.empty()
        
        import time
        for i, stage in enumerate(growth_stages):
            progress = (i + 1) / len(growth_stages)
            progress_bar.progress(progress)
            stage_display.markdown(f"**Current Stage:** {stage}")
            time.sleep(1)
        
        st.success("🎉 Crop growth simulation complete!")
        st.markdown("**Key Learnings:**")
        st.write("• Proper spacing prevents competition")
        st.write("• Adequate nutrition at each stage is crucial")
        st.write("• Water requirements vary by growth stage")

def simulate_farm_tour(placeholder):
    """Simulate virtual farm tour"""
    
    farm_areas = [
        {"name": "🌾 Crop Fields", "description": "Modern farming techniques in action"},
        {"name": "🚜 Machinery Shed", "description": "Latest agricultural equipment"},
        {"name": "💧 Irrigation System", "description": "Water-efficient irrigation setup"},
        {"name": "🏪 Storage Facility", "description": "Proper grain storage methods"},
        {"name": "🐄 Livestock Area", "description": "Integrated farming approach"},
        {"name": "🌿 Organic Section", "description": "Chemical-free farming practices"}
    ]
    
    with placeholder.container():
        st.markdown("### 🏞️ Virtual Farm Tour")
        
        for i, area in enumerate(farm_areas):
            st.markdown(f"**Stop {i+1}: {area['name']}**")
            st.write(area['description'])
            
            # Simulate tour progress
            tour_progress = st.progress((i + 1) / len(farm_areas))
            
            import time
            time.sleep(0.8)
        
        st.success("🏁 Farm tour completed!")
        st.markdown("**Tour Highlights:**")
        st.write("• Saw precision agriculture in action")
        st.write("• Learned about sustainable practices")
        st.write("• Understood integrated farming approach")

def simulate_pest_detection(placeholder):
    """Simulate interactive pest detection training"""
    
    pests = [
        {"name": "🐛 Aphids", "symptoms": "Curled leaves, sticky honeydew", "action": "Neem oil spray"},
        {"name": "🐛 Stem Borer", "symptoms": "Holes in stem, dead heart", "action": "Pheromone traps"},
        {"name": "🐛 Bollworm", "symptoms": "Damaged bolls, caterpillars", "action": "Bt spray"},
        {"name": "🦠 Leaf Blight", "symptoms": "Brown spots on leaves", "action": "Copper fungicide"}
    ]
    
    with placeholder.container():
        st.markdown("### 🔍 Interactive Pest Detection")
        
        for i, pest in enumerate(pests):
            st.markdown(f"**Detection {i+1}: {pest['name']}**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Pest:** {pest['name']}")
            
            with col2:
                st.write(f"**Symptoms:** {pest['symptoms']}")
            
            with col3:
                st.write(f"**Action:** {pest['action']}")
            
            # Simulate scanning
            scan_progress = st.progress((i + 1) / len(pests))
            
            import time
            time.sleep(1)
        
        st.success("🎯 Pest detection training completed!")
        st.markdown("**Skills Acquired:**")
        st.write("• Visual pest identification")
        st.write("• Symptom-based diagnosis")
        st.write("• Appropriate treatment selection")

def simulate_soil_analysis(placeholder):
    """Simulate soil analysis visualization"""
    
    with placeholder.container():
        st.markdown("### 🔬 Interactive Soil Analysis")
        
        # Simulate soil layers
        layers = [
            {"depth": "0-6 inches", "type": "Topsoil", "nutrients": "High organic matter"},
            {"depth": "6-18 inches", "type": "Subsoil", "nutrients": "Moderate nutrients"},
            {"depth": "18+ inches", "type": "Parent material", "nutrients": "Low organic content"}
        ]
        
        st.markdown("**Soil Profile Visualization:**")
        
        for layer in layers:
            st.markdown(f"**{layer['depth']}** - {layer['type']}: {layer['nutrients']}")
        
        # Nutrient analysis
        st.markdown("**Nutrient Analysis:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Nitrogen (N)", "180 ppm", "15 ppm ↑")
        
        with col2:
            st.metric("Phosphorus (P)", "25 ppm", "2 ppm ↑")
        
        with col3:
            st.metric("Potassium (K)", "200 ppm", "5 ppm ↓")
        
        import time
        time.sleep(2)
        
        st.success("🧪 Soil analysis visualization complete!")
        st.markdown("**Analysis Insights:**")
        st.write("• Soil pH is optimal for most crops")
        st.write("• Organic matter content is good")
        st.write("• Slight potassium deficiency detected")

def run():
    """Main function for AR/VR module"""
    
    st.markdown("## 🎥 AR/VR Learning Hub")
    st.markdown("Interactive agricultural learning through videos, simulations, and virtual experiences.")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📹 Video Tutorials", "🥽 AR Experiences", "📚 Learning Paths", "🎯 Interactive Tools"])
    
    with tab1:
        show_video_tutorials()
    
    with tab2:
        create_ar_experience_demo()
    
    with tab3:
        show_learning_paths()
    
    with tab4:
        show_interactive_tools()

def show_video_tutorials():
    """Display video tutorial section"""
    
    st.markdown("### 📹 Agricultural Video Tutorials")
    
    tutorials = get_video_tutorials()
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        difficulty_filter = st.selectbox(
            "🎯 Difficulty Level:",
            ["All", "Beginner", "Intermediate", "Advanced"]
        )
    
    with col2:
        crop_filter = st.selectbox(
            "🌾 Crop Focus:",
            ["All", "Rice", "Wheat", "Cotton", "Vegetables", "Fruits", "Pulses"]
        )
    
    with col3:
        topic_filter = st.selectbox(
            "📖 Topic:",
            ["All", "Soil", "Seeds", "Irrigation", "Pests", "Organic", "Harvest"]
        )
    
    # Filter tutorials
    filtered_tutorials = {}
    
    for key, tutorial in tutorials.items():
        include = True
        
        if difficulty_filter != "All" and tutorial['difficulty'] != difficulty_filter:
            include = False
        
        if crop_filter != "All" and crop_filter not in tutorial['crops']:
            include = False
        
        if topic_filter != "All":
            topic_match = any(topic_filter.lower() in topic.lower() for topic in tutorial['topics'])
            if not topic_match:
                include = False
        
        if include:
            filtered_tutorials[key] = tutorial
    
    # Display tutorials
    if not filtered_tutorials:
        st.info("No tutorials match your filter criteria. Try adjusting the filters.")
        return
    
    st.markdown(f"### 🎬 Available Tutorials ({len(filtered_tutorials)} found)")
    
    for tutorial_id, tutorial in filtered_tutorials.items():
        
        with st.expander(f"{tutorial['title']} - {tutorial['duration']}", expanded=False):
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**📝 Description:** {tutorial['description']}")
                
                st.markdown("**📚 Topics Covered:**")
                for topic in tutorial['topics']:
                    st.write(f"• {topic}")
                
                st.markdown(f"**🌾 Suitable for Crops:** {', '.join(tutorial['crops'])}")
                
                # Video player placeholder
                video_path = Path(__file__).parent.parent / "videos" / tutorial['file']
                
                if video_path.exists():
                    # In a real app, this would embed the actual video
                    st.info("📼 Video player would be embedded here")
                    
                    if st.button(f"▶️ Play {tutorial['title']}", key=f"play_{tutorial_id}"):
                        st.success("🎬 Video is now playing!")
                        st.markdown("*Note: In a real application, the video would play here*")
                else:
                    st.warning(f"📁 Video file not found: {tutorial['file']}")
                    st.markdown("**📋 Video Content Preview:**")
                    
                    # Show what the video would contain
                    if 'soil_preparation' in tutorial_id:
                        st.markdown("""
                        **Video would show:**
                        - Land leveling techniques
                        - Soil testing procedures
                        - Adding organic matter
                        - pH adjustment methods
                        """)
                    elif 'seed_treatment' in tutorial_id:
                        st.markdown("""
                        **Video would show:**
                        - Fungicide application
                        - Bio-agent coating process
                        - Seed priming techniques
                        - Storage after treatment
                        """)
                    elif 'irrigation' in tutorial_id:
                        st.markdown("""
                        **Video would show:**
                        - Drip system installation
                        - Sprinkler setup guide
                        - Water scheduling tips
                        - System maintenance
                        """)
                    else:
                        st.markdown(f"**Video demonstrates:** {tutorial['description']}")
            
            with col2:
                difficulty_colors = {
                    'Beginner': '🟢',
                    'Intermediate': '🟡',
                    'Advanced': '🔴'
                }
                
                st.markdown(f"**⏱️ Duration:** {tutorial['duration']}")
                st.markdown(f"**📊 Level:** {difficulty_colors[tutorial['difficulty']]} {tutorial['difficulty']}")
                
                # Progress tracking
                st.markdown("**📈 Your Progress:**")
                progress = st.slider("Completion %", 0, 100, 0, key=f"progress_{tutorial_id}")
                
                if progress == 100:
                    st.success("✅ Completed!")
                elif progress > 0:
                    st.info(f"🔄 {progress}% watched")
                else:
                    st.info("▶️ Not started")
                
                # Actions
                if st.button("📚 Add to Playlist", key=f"playlist_{tutorial_id}"):
                    st.success("Added to your learning playlist!")
                
                if st.button("📤 Share Tutorial", key=f"share_{tutorial_id}"):
                    st.info("Share link copied to clipboard!")

def show_learning_paths():
    """Show structured learning paths"""
    
    st.markdown("### 📚 Structured Learning Paths")
    st.markdown("Follow guided learning journeys based on your farming interests and experience level.")
    
    learning_paths = {
        'beginner_farmer': {
            'title': '🌱 New Farmer Journey',
            'description': 'Complete guide for beginners starting their farming career',
            'duration': '6-8 weeks',
            'modules': [
                'Understanding Soil Types',
                'Crop Selection Basics', 
                'Basic Irrigation Methods',
                'Pest Identification 101',
                'Harvest & Storage Fundamentals'
            ],
            'prerequisites': 'None',
            'certification': 'Beginner Farmer Certificate'
        },
        'organic_farming': {
            'title': '🌿 Organic Farming Mastery',
            'description': 'Comprehensive organic and sustainable farming practices',
            'duration': '8-10 weeks',
            'modules': [
                'Organic Soil Management',
                'Composting Techniques',
                'Natural Pest Control',
                'Crop Rotation & Companion Planting',
                'Organic Certification Process'
            ],
            'prerequisites': 'Basic farming knowledge',
            'certification': 'Organic Farming Specialist'
        },
        'precision_agriculture': {
            'title': '🤖 Precision Agriculture',
            'description': 'Modern technology-driven farming techniques',
            'duration': '10-12 weeks',
            'modules': [
                'GPS and GIS in Agriculture',
                'Drone Applications',
                'Soil Sensors & IoT',
                'Data Analytics for Farming',
                'Automated Irrigation Systems'
            ],
            'prerequisites': 'Intermediate farming experience',
            'certification': 'Precision Agriculture Expert'
        },
        'crop_specific': {
            'title': '🌾 Crop-Specific Expertise',
            'description': 'Deep dive into specific crop cultivation',
            'duration': '4-6 weeks per crop',
            'modules': [
                'Rice Cultivation Mastery',
                'Wheat Production Excellence',
                'Cotton Farming Techniques',
                'Vegetable Production Systems',
                'Fruit Orchard Management'
            ],
            'prerequisites': 'Basic crop knowledge',
            'certification': 'Crop Specialist Certificate'
        }
    }
    
    # Path selection
    selected_path = st.selectbox(
        "🎯 Choose Learning Path:",
        list(learning_paths.keys()),
        format_func=lambda x: learning_paths[x]['title']
    )
    
    path_info = learning_paths[selected_path]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"## {path_info['title']}")
        st.markdown(f"**📖 Description:** {path_info['description']}")
        
        st.markdown("### 📋 Learning Modules")
        
        for i, module in enumerate(path_info['modules'], 1):
            with st.expander(f"Module {i}: {module}"):
                # Module content placeholder
                if 'soil' in module.lower():
                    st.markdown("""
                    **Learning Objectives:**
                    - Identify different soil types
                    - Understand soil composition
                    - Learn soil testing methods
                    - Practice soil improvement techniques
                    
                    **Activities:**
                    - Video: Soil analysis demonstration
                    - Interactive: Soil type identification
                    - Assignment: Test your farm soil
                    - Quiz: Soil basics assessment
                    """)
                elif 'pest' in module.lower():
                    st.markdown("""
                    **Learning Objectives:**
                    - Recognize common pests
                    - Understand pest life cycles
                    - Learn identification techniques
                    - Practice monitoring methods
                    
                    **Activities:**
                    - AR: Pest identification simulation
                    - Video: Field scouting techniques
                    - Assignment: Create pest monitoring log
                    - Quiz: Pest identification test
                    """)
                else:
                    st.markdown(f"""
                    **Learning Objectives:**
                    - Master {module.lower()} fundamentals
                    - Apply practical techniques
                    - Understand best practices
                    - Develop implementation skills
                    
                    **Activities:**
                    - Interactive tutorials
                    - Practical demonstrations
                    - Hands-on assignments
                    - Progress assessments
                    """)
                
                # Module progress
                module_progress = st.progress(0)
                if st.button(f"🚀 Start Module {i}", key=f"start_{i}"):
                    st.success(f"Module {i} started! Check your learning dashboard.")
        
        # Enroll button
        if st.button(f"📝 Enroll in {path_info['title']}", type="primary"):
            st.balloons()
            st.success("🎉 Successfully enrolled!")
            st.info("Check your dashboard for learning schedule and materials.")
    
    with col2:
        st.markdown("### ℹ️ Path Information")
        st.info(f"""
        **⏰ Duration:** {path_info['duration']}
        
        **📚 Prerequisites:** {path_info['prerequisites']}
        
        **🏆 Certification:** {path_info['certification']}
        
        **📊 Format:**
        - Video tutorials
        - Interactive simulations
        - Hands-on assignments
        - Progress quizzes
        - Final assessment
        """)
        
        st.markdown("### 🎓 Learning Benefits")
        st.success("""
        **Skills You'll Gain:**
        - Practical farming knowledge
        - Problem-solving abilities
        - Modern technique adoption
        - Decision-making skills
        
        **Career Benefits:**
        - Improved crop yields
        - Reduced farming costs
        - Enhanced sustainability
        - Professional recognition
        """)
        
        st.markdown("### 👥 Community")
        st.markdown("""
        **Connect with:**
        - Fellow learners
        - Expert instructors
        - Local mentors
        - Success alumni
        
        **Support Available:**
        - Discussion forums
        - Live Q&A sessions
        - Peer study groups
        - Expert consultations
        """)

def show_interactive_tools():
    """Show interactive learning tools"""
    
    st.markdown("### 🎯 Interactive Learning Tools")
    st.markdown("Hands-on tools to practice and apply agricultural concepts.")
    
    tools_tab1, tools_tab2, tools_tab3, tools_tab4 = st.tabs([
        "🧮 Calculators", "🎮 Simulations", "🔬 Virtual Labs", "📊 Assessments"
    ])
    
    with tools_tab1:
        show_agricultural_calculators()
    
    with tools_tab2:
        show_farming_simulations()
    
    with tools_tab3:
        show_virtual_labs()
    
    with tools_tab4:
        show_knowledge_assessments()

def show_agricultural_calculators():
    """Show various agricultural calculators"""
    
    st.markdown("#### 🧮 Agricultural Calculators")
    
    calc_type = st.selectbox(
        "Choose Calculator:",
        ["Seed Rate Calculator", "Fertilizer Calculator", "Irrigation Scheduler", "Yield Predictor", "Cost Analyzer"]
    )
    
    if calc_type == "Seed Rate Calculator":
        st.markdown("##### 🌰 Seed Rate Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            crop = st.selectbox("Crop:", ["Rice", "Wheat", "Maize", "Cotton", "Soybean"])
            field_area = st.number_input("Field Area (acres):", min_value=0.1, value=1.0, step=0.1)
            spacing = st.number_input("Row Spacing (inches):", min_value=6, value=12, step=1)
        
        with col2:
            plant_spacing = st.number_input("Plant Spacing (inches):", min_value=2, value=6, step=1)
            germination_rate = st.slider("Germination Rate (%):", 70, 100, 85)
            thousand_seed_weight = st.number_input("1000 Seed Weight (grams):", min_value=1.0, value=25.0, step=1.0)
        
        if st.button("💫 Calculate Seed Rate"):
            # Simplified calculation
            plants_per_sq_ft = 144 / (spacing * plant_spacing)
            total_plants = field_area * 43560 * plants_per_sq_ft  # 43560 sq ft per acre
            seeds_needed = total_plants * (100 / germination_rate)
            seed_weight_kg = (seeds_needed * thousand_seed_weight) / (1000 * 1000)  # Convert to kg
            
            st.success(f"🌰 **Recommended Seed Rate:** {seed_weight_kg:.1f} kg for {field_area} acres")
            st.info(f"📊 **Plants per acre:** {total_plants/field_area:,.0f}")
            st.info(f"🔢 **Total seeds needed:** {seeds_needed:,.0f}")
    
    elif calc_type == "Fertilizer Calculator":
        st.markdown("##### 🧪 NPK Fertilizer Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            crop_fert = st.selectbox("Crop:", ["Rice", "Wheat", "Cotton", "Tomato", "Potato"], key="fert_crop")
            area_fert = st.number_input("Area (acres):", min_value=0.1, value=1.0, step=0.1, key="fert_area")
            target_yield = st.number_input("Target Yield (qt/acre):", min_value=5, value=30, step=5)
        
        with col2:
            soil_n = st.number_input("Soil N (ppm):", min_value=0, value=200, step=10)
            soil_p = st.number_input("Soil P (ppm):", min_value=0, value=25, step=5)
            soil_k = st.number_input("Soil K (ppm):", min_value=0, value=150, step=10)
        
        if st.button("🧪 Calculate Fertilizer Need"):
            # Simplified NPK calculation
            n_requirement = target_yield * 2.5  # kg/acre
            p_requirement = target_yield * 1.2
            k_requirement = target_yield * 2.0
            
            # Adjust for soil levels
            n_needed = max(0, n_requirement - (soil_n * 0.1))
            p_needed = max(0, p_requirement - (soil_p * 0.2))
            k_needed = max(0, k_requirement - (soil_k * 0.1))
            
            st.success("🧪 **Fertilizer Recommendations:**")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("Nitrogen (N)", f"{n_needed:.1f} kg/acre")
            with col_b:
                st.metric("Phosphorus (P)", f"{p_needed:.1f} kg/acre")
            with col_c:
                st.metric("Potassium (K)", f"{k_needed:.1f} kg/acre")
            
            # Commercial fertilizer suggestions
            urea_needed = (n_needed * area_fert) / 0.46  # Urea is 46% N
            dap_needed = (p_needed * area_fert) / 0.46   # DAP is 46% P2O5
            mop_needed = (k_needed * area_fert) / 0.60   # MOP is 60% K2O
            
            st.info(f"""
            **Commercial Fertilizer Requirements:**
            - Urea: {urea_needed:.1f} kg
            - DAP: {dap_needed:.1f} kg  
            - MOP: {mop_needed:.1f} kg
            """)

def show_farming_simulations():
    """Show farming simulation games"""
    
    st.markdown("#### 🎮 Farming Simulations")
    
    simulation = st.selectbox(
        "Choose Simulation:",
        ["Crop Planning Game", "Weather Decision Maker", "Market Timing Challenge", "Pest Management Scenario"]
    )
    
    if simulation == "Crop Planning Game":
        st.markdown("##### 🌾 Virtual Crop Planning")
        
        if 'game_started' not in st.session_state:
            st.session_state.game_started = False
            st.session_state.game_score = 0
            st.session_state.game_round = 1
        
        if not st.session_state.game_started:
            st.markdown("""
            **Game Objective:** Plan the optimal crop mix for maximum profit
            
            **Rules:**
            - You have 100 acres of land
            - Choose up to 3 different crops
            - Consider soil type, season, and market prices
            - Weather events may affect your crops
            """)
            
            if st.button("🚀 Start Game"):
                st.session_state.game_started = True
                st.experimental_rerun()
        
        else:
            st.markdown(f"### 🎮 Round {st.session_state.game_round} - Crop Planning")
            st.markdown(f"**Current Score:** {st.session_state.game_score} points")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Available Land:** 100 acres")
                st.markdown("**Soil Type:** Loamy (versatile)")
                st.markdown("**Season:** Kharif")
                st.markdown("**Budget:** ₹5,00,000")
            
            with col2:
                st.markdown("**Market Prices (per quintal):**")
                st.write("• Rice: ₹2,200")
                st.write("• Cotton: ₹5,800") 
                st.write("• Maize: ₹1,900")
                st.write("• Soybean: ₹4,200")
            
            # Crop selection
            st.markdown("**🌱 Select Your Crops:**")
            
            rice_acres = st.slider("Rice (acres):", 0, 100, 0)
            cotton_acres = st.slider("Cotton (acres):", 0, 100-rice_acres, 0)
            remaining = 100 - rice_acres - cotton_acres
            maize_acres = st.slider("Maize (acres):", 0, remaining, 0)
            
            total_used = rice_acres + cotton_acres + maize_acres
            st.write(f"**Land Used:** {total_used}/100 acres")
            
            if total_used <= 100 and st.button("📊 Calculate Results"):
                # Simple scoring
                rice_profit = rice_acres * 25 * 2200 * 0.3  # yield * price * profit margin
                cotton_profit = cotton_acres * 8 * 5800 * 0.4
                maize_profit = maize_acres * 28 * 1900 * 0.25
                
                total_profit = rice_profit + cotton_profit + maize_profit
                round_score = int(total_profit / 10000)  # Convert to points
                
                st.session_state.game_score += round_score
                st.session_state.game_round += 1
                
                st.success(f"🎉 Round Complete! Earned {round_score} points")
                st.info(f"💰 Total Profit: ₹{total_profit:,.0f}")
                
                if st.session_state.game_round <= 3:
                    if st.button("➡️ Next Round"):
                        st.experimental_rerun()
                else:
                    st.balloons()
                    st.success(f"🏆 Game Complete! Final Score: {st.session_state.game_score}")
                    if st.button("🔄 Play Again"):
                        st.session_state.game_started = False
                        st.session_state.game_score = 0
                        st.session_state.game_round = 1
                        st.experimental_rerun()

def show_virtual_labs():
    """Show virtual laboratory experiences"""
    
    st.markdown("#### 🔬 Virtual Agricultural Labs")
    
    lab_type = st.selectbox(
        "Choose Virtual Lab:",
        ["Soil Testing Lab", "Plant Disease Diagnosis", "Seed Quality Testing", "Nutrient Analysis"]
    )
    
    if lab_type == "Soil Testing Lab":
        st.markdown("##### 🧪 Virtual Soil Testing Laboratory")
        
        st.markdown("**Lab Objective:** Analyze soil samples and interpret results")
        
        # Simulate lab equipment
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔬 Available Equipment:**")
            equipment = st.multiselect(
                "Select Equipment:",
                ["pH Meter", "EC Meter", "Soil Auger", "Test Tubes", "Chemical Reagents", "Microscope"],
                default=["pH Meter", "EC Meter"]
            )
        
        with col2:
            st.markdown("**🧪 Sample Information:**")
            sample_depth = st.selectbox("Sample Depth:", ["0-6 inches", "6-12 inches", "12-18 inches"])
            sample_location = st.text_input("Field Location:", "North Field Block A")
        
        if st.button("🔬 Start Analysis"):
            with st.spinner("Analyzing soil sample..."):
                import time
                time.sleep(2)
                
                # Simulate results
                results = {
                    "pH": 6.8,
                    "EC": 0.45,
                    "Organic Matter": 2.3,
                    "Nitrogen": 185,
                    "Phosphorus": 28,
                    "Potassium": 195
                }
                
                st.success("🧪 **Analysis Complete!**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("pH Level", results["pH"])
                    st.metric("EC (dS/m)", results["EC"])
                
                with col2:
                    st.metric("Organic Matter (%)", results["Organic Matter"])
                    st.metric("Nitrogen (ppm)", results["Nitrogen"])
                
                with col3:
                    st.metric("Phosphorus (ppm)", results["Phosphorus"])
                    st.metric("Potassium (ppm)", results["Potassium"])
                
                # Interpretation
                st.markdown("**🎯 Lab Report & Recommendations:**")
                st.info("""
                **Findings:**
                - Soil pH is slightly acidic but within acceptable range
                - Organic matter content is good
                - Nitrogen levels are adequate
                - Phosphorus is optimal for most crops
                - Potassium is well balanced
                
                **Recommendations:**
                - Continue current organic matter management
                - Monitor nitrogen during peak growing season
                - Soil is suitable for most field crops
                """)

def show_knowledge_assessments():
    """Show knowledge assessment tools"""
    
    st.markdown("#### 📊 Knowledge Assessment Center")
    
    assessment_type = st.selectbox(
        "Choose Assessment:",
        ["Quick Quiz", "Skill Assessment", "Scenario-Based Test", "Certification Exam"]
    )
    
    if assessment_type == "Quick Quiz":
        st.markdown("##### 🧠 Agricultural Knowledge Quiz")
        
        if 'quiz_started' not in st.session_state:
            st.session_state.quiz_started = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_question = 0
        
        quiz_questions = [
            {
                "question": "What is the ideal pH range for most crops?",
                "options": ["4.0-5.0", "6.0-7.0", "8.0-9.0", "9.0-10.0"],
                "correct": 1,
                "explanation": "Most crops grow best in slightly acidic to neutral soil (pH 6.0-7.0)"
            },
            {
                "question": "Which nutrient is primarily responsible for leaf growth?",
                "options": ["Phosphorus", "Nitrogen", "Potassium", "Calcium"],
                "correct": 1,
                "explanation": "Nitrogen is essential for vegetative growth and leaf development"
            },
            {
                "question": "What does IPM stand for in agriculture?",
                "options": ["Intensive Pest Management", "Integrated Pest Management", "Individual Plant Monitoring", "Indoor Plant Maintenance"],
                "correct": 1,
                "explanation": "IPM combines multiple pest control strategies for sustainable management"
            }
        ]
        
        if not st.session_state.quiz_started:
            st.markdown("**Quiz Instructions:**")
            st.info("""
            - 3 multiple choice questions
            - Each correct answer = 10 points
            - No time limit
            - Immediate feedback provided
            """)
            
            if st.button("📝 Start Quiz"):
                st.session_state.quiz_started = True
                st.experimental_rerun()
        
        else:
            if st.session_state.quiz_question < len(quiz_questions):
                current_q = quiz_questions[st.session_state.quiz_question]
                
                st.markdown(f"**Question {st.session_state.quiz_question + 1}/3:**")
                st.markdown(f"**{current_q['question']}**")
                
                answer = st.radio("Select your answer:", current_q['options'], key=f"q_{st.session_state.quiz_question}")
                
                if st.button("Submit Answer"):
                    selected_index = current_q['options'].index(answer)
                    
                    if selected_index == current_q['correct']:
                        st.success("✅ Correct!")
                        st.session_state.quiz_score += 10
                    else:
                        st.error("❌ Incorrect")
                        st.info(f"**Correct Answer:** {current_q['options'][current_q['correct']]}")
                    
                    st.info(f"**Explanation:** {current_q['explanation']}")
                    st.session_state.quiz_question += 1
                    
                    if st.session_state.quiz_question < len(quiz_questions):
                        if st.button("Next Question"):
                            st.experimental_rerun()
                    else:
                        st.experimental_rerun()
            
            else:
                # Quiz completed
                st.balloons()
                st.markdown("### 🎉 Quiz Complete!")
                
                score_percentage = (st.session_state.quiz_score / 30) * 100
                
                st.metric("Final Score", f"{st.session_state.quiz_score}/30 ({score_percentage:.0f}%)")
                
                if score_percentage >= 80:
                    st.success("🌟 Excellent! You have strong agricultural knowledge.")
                elif score_percentage >= 60:
                    st.info("👍 Good job! Consider reviewing some topics.")
                else:
                    st.warning("📚 Keep learning! Practice with more tutorials.")
                
                if st.button("🔄 Retake Quiz"):
                    st.session_state.quiz_started = False
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_question = 0
                    st.experimental_rerun()

if __name__ == "__main__":
    run()