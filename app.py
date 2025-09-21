import streamlit as st
import sys
from pathlib import Path

# Add modules directory to path
sys.path.append(str(Path(__file__).parent / "modules"))

# Import all modules
from modules.crop_advisory import run as crop_advisory_run
from modules.fertilizer_recommendation import run as fertilizer_run
from modules.pest_detection import run as pest_detection_run
from modules.weather_alerts import run as weather_alerts_run
from modules.market_price import run as market_price_run
from modules.community_alerts import run as community_alerts_run
from modules.ar_module import run as ar_module_run

def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title="🌾 AgriAdvisor Pro",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .module-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
            margin: 1rem 0;
            color: #000; /* make text black by default inside the card */
        }
        .module-card h4, .module-card p {
            color: #000 !important; /* ensure headings and paragraphs are black */
        }
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
        <div class="main-header">
            <h1>🌾 AgriAdvisor Pro - Smart Farming Solutions</h1>
            <p>Your comprehensive agricultural advisory platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 📋 Navigation Menu")
        
        # Module selection
        modules = {
            "🏠 Dashboard": "dashboard",
            "🌱 Crop Advisory": "crop_advisory",
            "💡 Fertilizer Recommendation": "fertilizer",
            "🐛 Pest & Disease Detection": "pest_detection",
            "🌤️ Weather Alerts": "weather_alerts",
            "📊 Market Prices": "market_price",
            "👥 Community Alerts": "community_alerts",
            "🎥 AR/VR Learning": "ar_module"
        }
        
        selected_module = st.selectbox(
            "Select Module:",
            list(modules.keys()),
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📱 Quick Stats")
        st.metric("Active Farmers", "1,234", "12%")
        st.metric("Crops Monitored", "567", "8%")
        st.metric("Alerts Sent", "89", "23%")
        
        st.markdown("---")
        st.markdown("### 🔗 Resources")
        st.markdown("- [Weather Updates]()")
        st.markdown("- [Market Trends]()")
        st.markdown("- [Best Practices]()")
        st.markdown("- [Contact Support]()")
    
    # Main content area
    module_key = modules[selected_module]
    
    if module_key == "dashboard":
        show_dashboard()
    elif module_key == "crop_advisory":
        crop_advisory_run()
    elif module_key == "fertilizer":
        fertilizer_run()
    elif module_key == "pest_detection":
        pest_detection_run()
    elif module_key == "weather_alerts":
        weather_alerts_run()
    elif module_key == "market_price":
        market_price_run()
    elif module_key == "community_alerts":
        community_alerts_run()
    elif module_key == "ar_module":
        ar_module_run()

def show_dashboard():
    """Display the main dashboard"""
    
    st.markdown("## 🏠 Dashboard Overview")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🌾 Total Crops",
            value="156",
            delta="12 this month"
        )
    
    with col2:
        st.metric(
            label="🧑‍🌾 Active Farmers",
            value="1,234",
            delta="45 new"
        )
    
    with col3:
        st.metric(
            label="⚠️ Active Alerts",
            value="23",
            delta="-5 from yesterday"
        )
    
    with col4:
        st.metric(
            label="💰 Avg Market Price",
            value="₹2,450/qt",
            delta="3.2%"
        )
    
    st.markdown("---")
    
    # Quick access cards
    st.markdown("## 🚀 Quick Access")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="module-card">
                <h4>🌱 Get Crop Recommendations</h4>
                <p>Find the best crops for your soil and season</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Start Crop Advisory", key="crop_btn"):
            st.query_params["module"]="crop_advisory"
    
    with col2:
        st.markdown("""
            <div class="module-card">
                <h4>🌤️ Check Weather</h4>
                <p>Get weather forecasts and alerts for your area</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("View Weather Alerts", key="weather_btn"):
            st.query_params['module']="weather_alerts"
    
    with col3:
        st.markdown("""
            <div class="module-card">
                <h4>📊 Market Prices</h4>
                <p>Track crop prices and market trends</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("View Market Data", key="market_btn"):
            st.query_params['module']="market_price"
    
    # Recent activity
    st.markdown("---")
    st.markdown("## 📈 Recent Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔔 Latest Alerts")
        st.info("🐛 Pest alert for tomatoes in Karnataka region")
        st.warning("🌧️ Heavy rain expected in Punjab - protect crops")
        st.success("💰 Good prices for wheat in Delhi mandi")
    
    with col2:
        st.markdown("### 👥 Community Updates")
        st.write("• New irrigation technique shared by Farmer Raj")
        st.write("• Disease outbreak reported in Haryana")
        st.write("• Organic farming workshop scheduled")
    
    # Footer
    st.markdown("---")
    st.markdown("### 📞 Need Help?")
    st.markdown("Contact our agricultural experts: **1800-XXX-AGRI** | **support@agriadvisor.com**")

if __name__ == "__main__":
    main()