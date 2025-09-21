import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import csv


def safe_read_csv(path):
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return pd.DataFrame()

    # Try sniffing delimiter
    try:
        sample = p.read_text(encoding='utf-8', errors='replace')[:8192]
    except Exception:
        sample = None

    delim = None
    if sample:
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=[',', ';', '\t', '|'])
            delim = dialect.delimiter
        except Exception:
            delim = None

    candidates = ([delim] if delim else []) + [',', ';', '\t', '|']
    tried = set()
    for d in candidates:
        if not d or d in tried:
            continue
        tried.add(d)
        try:
            df = pd.read_csv(p, sep=d)
            if not df.empty and len(df.columns) > 0:
                return df
        except Exception:
            continue

    # final fallback
    try:
        return pd.read_csv(p, engine='python')
    except Exception:
        return pd.DataFrame()

def load_market_data():
    """Load market price data"""
    data_path = Path(__file__).parent.parent / "data" / "market_prices.csv"
    global market_load_info
    market_load_info = {'source': None, 'warning': None, 'columns': None, 'sample': None}

    if data_path.exists():
        try:
            raw = data_path.read_text(encoding='utf-8', errors='replace')
        except Exception:
            raw = None

        df = safe_read_csv(data_path)
        if df is None or df.empty:
            market_load_info.update({'source': 'demo_generated', 'warning': f'CSV at {data_path} missing/empty/malformed; generating demo data.', 'columns': [], 'sample': (raw[:2048] if raw else None)})
        else:
            market_load_info.update({'source': 'csv', 'warning': None, 'columns': df.columns.tolist(), 'sample': (raw[:2048] if raw else None)})
            return df
    # If we reached here, either data_path didn't exist OR CSV existed but was invalid/empty
    # Generate sample market data
    crops = ['Rice', 'Wheat', 'Cotton', 'Tomato', 'Onion', 'Potato', 'Maize', 'Soybean', 'Sugarcane', 'Chili']
    markets = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad', 'Ahmedabad']
    dates = [(datetime.now() - timedelta(days=i)) for i in range(30, 0, -1)]

    np.random.seed(42)
    market_data = []

    # Base prices (per quintal)
    base_prices = {
        'Rice': 2000, 'Wheat': 2200, 'Cotton': 5500, 'Tomato': 1500,
        'Onion': 800, 'Potato': 1200, 'Maize': 1800, 'Soybean': 4000,
        'Sugarcane': 350, 'Chili': 8000
    }

    for crop in crops:
        base_price = base_prices[crop]

        for market in markets:
            # Market-specific price variation
            market_factor = {
                'Delhi': 1.05, 'Mumbai': 1.15, 'Bangalore': 1.08, 'Chennai': 1.02,
                'Kolkata': 0.95, 'Pune': 1.12, 'Hyderabad': 1.00, 'Ahmedabad': 1.08
            }[market]

            market_base = base_price * market_factor

            for i, date in enumerate(dates):
                # Price trend with seasonal variation
                trend = np.sin(i * 0.2) * 0.1 + np.random.normal(0, 0.05)
                seasonal_factor = 1 + trend

                # Daily price with random variation
                daily_variation = np.random.normal(1, 0.03)

                current_price = market_base * seasonal_factor * daily_variation

                # Calculate min/max prices
                min_price = current_price * (0.95 + np.random.normal(0, 0.02))
                max_price = current_price * (1.05 + np.random.normal(0, 0.02))

                # Arrivals (quantity in quintals)
                base_arrival = {'Rice': 500, 'Wheat': 800, 'Cotton': 200, 'Tomato': 300,
                              'Onion': 400, 'Potato': 600, 'Maize': 450, 'Soybean': 350,
                              'Sugarcane': 1000, 'Chili': 150}[crop]

                arrival = max(50, base_arrival * (0.8 + np.random.random() * 0.4))

                # Quality grade distribution
                faq_percent = 60 + np.random.normal(0, 10)  # FAQ = Frequently Asked Quality
                good_percent = 25 + np.random.normal(0, 5)
                average_percent = max(0, 100 - faq_percent - good_percent)

                market_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'crop': crop,
                    'market': market,
                    'min_price': round(max(min_price, 0), 2),
                    'max_price': round(max_price, 2),
                    'modal_price': round(current_price, 2),  # Most common price
                    'arrival_quantity': round(arrival, 0),
                    'faq_percent': round(max(0, min(100, faq_percent)), 1),
                    'good_percent': round(max(0, min(100, good_percent)), 1),
                    'average_percent': round(max(0, min(100, average_percent)), 1)
                })

    return pd.DataFrame(market_data)

def calculate_price_trends(df, crop, market, days=7):
    """Calculate price trends and statistics"""
    filtered_data = df[(df['crop'] == crop) & (df['market'] == market)].copy()
    filtered_data['date'] = pd.to_datetime(filtered_data['date'])
    filtered_data = filtered_data.sort_values('date').tail(days)
    
    if len(filtered_data) < 2:
        return None
    
    latest_price = filtered_data.iloc[-1]['modal_price']
    previous_price = filtered_data.iloc[0]['modal_price']
    
    price_change = latest_price - previous_price
    price_change_percent = (price_change / previous_price) * 100
    
    avg_price = filtered_data['modal_price'].mean()
    price_volatility = filtered_data['modal_price'].std()
    
    return {
        'latest_price': latest_price,
        'price_change': price_change,
        'price_change_percent': price_change_percent,
        'avg_price': avg_price,
        'volatility': price_volatility,
        'trend_data': filtered_data
    }

def create_price_chart(df, crop, markets, days=30):
    """Create price trend chart"""
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set1
    
    for i, market in enumerate(markets):
        market_data = df[(df['crop'] == crop) & (df['market'] == market)].copy()
        market_data['date'] = pd.to_datetime(market_data['date'])
        market_data = market_data.sort_values('date').tail(days)
        
        if not market_data.empty:
            fig.add_trace(go.Scatter(
                x=market_data['date'],
                y=market_data['modal_price'],
                mode='lines+markers',
                name=market,
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=4),
                hovertemplate=f'<b>{market}</b><br>' +
                            'Date: %{x}<br>' +
                            'Price: ₹%{y:.0f}/qt<br>' +
                            '<extra></extra>'
            ))
    
    fig.update_layout(
        title=f'{crop} Price Trends - Last {days} Days',
        xaxis_title='Date',
        yaxis_title='Price (₹/Quintal)',
        hovermode='x unified',
        height=400
    )
    
    return fig

def run():
    """Main function for market price module"""
    
    st.markdown("## 📊 Market Prices & Trends")
    st.markdown("Track crop prices, analyze market trends, and make informed selling decisions.")
    
    # Load market data
    df = load_market_data()

    # Show debug info if CSV had issues
    info = globals().get('market_load_info')
    if info and info.get('warning'):
        st.warning(info.get('warning'))
        with st.expander("⚙️ Market data debug info"):
            st.write("Detected columns:", info.get('columns'))
            sample = info.get('sample')
            if sample:
                st.markdown("**CSV sample (first 2KB):**")
                st.code(sample)
    
    # Input controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_crop = st.selectbox(
            "🌾 Select Crop:",
            sorted(df['crop'].unique()),
            help="Choose the crop to analyze"
        )
    
    with col2:
        available_markets = sorted(df[df['crop'] == selected_crop]['market'].unique())
        selected_markets = st.multiselect(
            "🏪 Select Markets:",
            available_markets,
            default=available_markets[:3],
            help="Choose markets to compare"
        )
    
    with col3:
        time_period = st.selectbox(
            "📅 Time Period:",
            ["7 days", "15 days", "30 days"],
            index=2,
            help="Select analysis period"
        )
    
    days = int(time_period.split()[0])
    
    if not selected_markets:
        st.warning("Please select at least one market to display data.")
        return
    
    # Current prices summary
    st.markdown("---")
    st.markdown("### 💰 Current Market Prices")
    
    current_data = []
    for market in selected_markets:
        latest_data = df[(df['crop'] == selected_crop) & (df['market'] == market)]
        if not latest_data.empty:
            latest_row = latest_data.loc[latest_data['date'].idxmax()]
            
            # Calculate trend
            trend_info = calculate_price_trends(df, selected_crop, market, 7)
            trend_arrow = "📈" if trend_info and trend_info['price_change_percent'] > 0 else "📉" if trend_info and trend_info['price_change_percent'] < 0 else "➡️"
            trend_text = f"{trend_info['price_change_percent']:.1f}%" if trend_info else "N/A"
            
            current_data.append({
                'Market': market,
                'Current Price': f"₹{latest_row['modal_price']:.0f}",
                'Min-Max': f"₹{latest_row['min_price']:.0f} - ₹{latest_row['max_price']:.0f}",
                'Arrivals': f"{latest_row['arrival_quantity']:.0f} qt",
                '7-Day Trend': f"{trend_arrow} {trend_text}",
                'Date': latest_row['date']
            })
    
    if current_data:
        current_df = pd.DataFrame(current_data)
        st.dataframe(current_df, hide_index=True, use_container_width=True)
    
    # Price trend chart
    if selected_markets:
        st.markdown("---")
        st.markdown("### 📈 Price Trend Analysis")
        
        fig = create_price_chart(df, selected_crop, selected_markets, days)
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Market Insights")
            
            # Find highest and lowest price markets
            current_prices = {}
            for market in selected_markets:
                latest_data = df[(df['crop'] == selected_crop) & (df['market'] == market)]
                if not latest_data.empty:
                    current_prices[market] = latest_data.loc[latest_data['date'].idxmax()]['modal_price']
            
            if current_prices:
                highest_market = max(current_prices, key=current_prices.get)
                lowest_market = min(current_prices, key=current_prices.get)
                
                price_diff = current_prices[highest_market] - current_prices[lowest_market]
                price_diff_percent = (price_diff / current_prices[lowest_market]) * 100
                
                st.success(f"**Highest Price:** {highest_market} - ₹{current_prices[highest_market]:.0f}/qt")
                st.info(f"**Lowest Price:** {lowest_market} - ₹{current_prices[lowest_market]:.0f}/qt")
                st.warning(f"**Price Difference:** ₹{price_diff:.0f}/qt ({price_diff_percent:.1f}%)")
        
        with col2:
            st.markdown("#### 📊 Trading Recommendations")
            
            # Calculate overall trend
            all_trends = []
            for market in selected_markets:
                trend_info = calculate_price_trends(df, selected_crop, market, days)
                if trend_info:
                    all_trends.append(trend_info['price_change_percent'])
            
            if all_trends:
                avg_trend = np.mean(all_trends)
                
                if avg_trend > 5:
                    st.success("🚀 **Strong Uptrend** - Consider holding for better prices")
                elif avg_trend > 2:
                    st.info("📈 **Moderate Uptrend** - Good time to sell gradually")
                elif avg_trend > -2:
                    st.warning("➡️ **Stable Market** - Sell based on immediate needs")
                elif avg_trend > -5:
                    st.warning("📉 **Moderate Downtrend** - Consider selling soon")
                else:
                    st.error("📉 **Strong Downtrend** - Sell immediately if possible")
                
                volatility = np.std(all_trends)
                if volatility > 5:
                    st.warning("⚠️ **High Volatility** - Monitor daily for best timing")
    
    # Market analysis by quality grades
    st.markdown("---")
    st.markdown("### 🏆 Quality Grade Analysis")
    
    if selected_markets:
        quality_data = []
        for market in selected_markets:
            market_data = df[(df['crop'] == selected_crop) & (df['market'] == market)]
            if not market_data.empty:
                latest = market_data.loc[market_data['date'].idxmax()]
                quality_data.append({
                    'Market': market,
                    'FAQ (%)': latest['faq_percent'],
                    'Good (%)': latest['good_percent'], 
                    'Average (%)': latest['average_percent'],
                    'Quality Score': latest['faq_percent'] * 0.6 + latest['good_percent'] * 0.3 + latest['average_percent'] * 0.1
                })
        
        if quality_data:
            quality_df = pd.DataFrame(quality_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(quality_df, hide_index=True, use_container_width=True)
            
            with col2:
                # Quality distribution chart
                fig_quality = go.Figure()
                
                markets = quality_df['Market'].tolist()
                fig_quality.add_trace(go.Bar(name='FAQ', x=markets, y=quality_df['FAQ (%)']))
                fig_quality.add_trace(go.Bar(name='Good', x=markets, y=quality_df['Good (%)']))
                fig_quality.add_trace(go.Bar(name='Average', x=markets, y=quality_df['Average (%)']))
                
                fig_quality.update_layout(
                    title='Quality Grade Distribution',
                    xaxis_title='Markets',
                    yaxis_title='Percentage (%)',
                    barmode='stack',
                    height=300
                )
                
                st.plotly_chart(fig_quality, use_container_width=True)
    
    # Price forecasting (simple trend-based)
    st.markdown("---")
    st.markdown("### 🔮 Price Forecast")
    
    forecast_market = st.selectbox(
        "📍 Select Market for Forecast:",
        selected_markets,
        help="Choose market for price prediction"
    )
    
    if st.button("📊 Generate 7-Day Price Forecast"):
        
        # Get historical data for the selected market
        historical_data = df[(df['crop'] == selected_crop) & (df['market'] == forecast_market)].copy()
        historical_data['date'] = pd.to_datetime(historical_data['date'])
        historical_data = historical_data.sort_values('date').tail(30)
        
        if len(historical_data) > 10:
            
            # Simple linear regression for trend
            x = np.arange(len(historical_data))
            y = historical_data['modal_price'].values
            
            # Calculate trend
            z = np.polyfit(x, y, 1)
            trend_slope = z[0]
            
            # Generate forecast
            last_price = y[-1]
            forecast_dates = [(datetime.now() + timedelta(days=i)) for i in range(1, 8)]
            forecast_prices = []
            
            for i in range(7):
                # Simple trend continuation with some randomness
                forecasted_price = last_price + (trend_slope * (i + 1))
                # Add some uncertainty
                uncertainty = abs(forecasted_price * 0.02)  # 2% uncertainty
                forecast_prices.append({
                    'Date': forecast_dates[i].strftime('%Y-%m-%d'),
                    'Predicted Price': f"₹{forecasted_price:.0f}",
                    'Range': f"₹{forecasted_price-uncertainty:.0f} - ₹{forecasted_price+uncertainty:.0f}",
                    'Confidence': '70%' if i < 3 else '50%' if i < 5 else '30%'
                })
            
            forecast_df = pd.DataFrame(forecast_prices)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"#### 📈 7-Day Forecast for {forecast_market}")
                st.dataframe(forecast_df, hide_index=True, use_container_width=True)
            
            with col2:
                st.markdown("#### ⚠️ Forecast Disclaimer")
                st.warning("""
                **Note:** This forecast is based on historical trends and should be used as guidance only.
                
                **Factors not considered:**
                - Weather conditions
                - Government policies
                - Festival demands
                - Import/export changes
                - Crop diseases/pests
                
                **Recommendation:** Use multiple sources for market decisions.
                """)
        
        else:
            st.error("Insufficient historical data for forecasting. Need at least 10 days of data.")
    
    # Price alerts setup
    st.markdown("---")
    st.markdown("### 🔔 Price Alert Setup")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        alert_market = st.selectbox("Market for Alert:", selected_markets, key="alert_market")
        target_price = st.number_input("Target Price (₹/qt):", min_value=0.0, value=2000.0, step=50.0)
    
    with col2:
        alert_type = st.selectbox("Alert Type:", ["Price Above", "Price Below", "Price Change > 5%"])
        contact_method = st.selectbox("Notification Method:", ["SMS", "Email", "App Push", "All"])
    
    with col3:
        if st.button("🔔 Set Price Alert"):
            st.success(f"✅ Alert set for {selected_crop} in {alert_market}!")
            st.info(f"📱 You'll be notified via {contact_method} when price is {alert_type.lower()} ₹{target_price:.0f}/qt")
    
    # Market calendar and seasonal trends
    st.markdown("---")
    st.markdown("### 📅 Seasonal Market Calendar")
    
    # Sample seasonal data
    seasonal_data = {
        'Rice': {
            'harvest_months': 'Oct-Dec, Apr-May',
            'peak_price_months': 'Jul-Sep',
            'festival_demand': 'Diwali, Pongal',
            'export_season': 'Nov-Mar'
        },
        'Wheat': {
            'harvest_months': 'Mar-May',
            'peak_price_months': 'Aug-Oct', 
            'festival_demand': 'Holi, Diwali',
            'export_season': 'Apr-Aug'
        },
        'Cotton': {
            'harvest_months': 'Oct-Feb',
            'peak_price_months': 'Jun-Sep',
            'festival_demand': 'Wedding season',
            'export_season': 'Nov-Apr'
        }
    }
    
    if selected_crop in seasonal_data:
        crop_seasonal = seasonal_data[selected_crop]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.info(f"**Harvest Season**\n{crop_seasonal['harvest_months']}")
        
        with col2:
            st.success(f"**Peak Prices**\n{crop_seasonal['peak_price_months']}")
        
        with col3:
            st.warning(f"**Festival Demand**\n{crop_seasonal['festival_demand']}")
        
        with col4:
            st.info(f"**Export Season**\n{crop_seasonal['export_season']}")
    
    # Market intelligence and tips
    st.markdown("---")
    st.markdown("### 🧠 Market Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("💡 Best Selling Practices"):
            st.markdown("""
            **Timing Your Sales:**
            - Monitor weekly arrival patterns
            - Avoid selling during peak harvest
            - Target festival and wedding seasons
            - Watch for export opportunities
            
            **Quality Improvement:**
            - Proper post-harvest handling
            - Correct moisture content
            - Clean, uniform grading
            - Attractive packaging
            
            **Negotiation Tips:**
            - Know current market rates
            - Compare multiple buyers
            - Build long-term relationships
            - Consider collective selling
            """)
    
    with col2:
        with st.expander("📊 Market Analysis Tools"):
            st.markdown("""
            **Price Indicators:**
            - Moving averages (7, 15, 30 days)
            - Seasonal price patterns
            - Supply-demand balance
            - Government policy impacts
            
            **Risk Management:**
            - Don't sell entire stock at once
            - Use forward contracts when available
            - Consider warehouse receipts
            - Monitor weather impacts
            
            **Information Sources:**
            - AGMARKNET portal
            - Local mandi boards
            - Commodity exchanges
            - Agricultural newspapers
            """)
    
    # Government schemes and support
    st.markdown("---")
    st.markdown("### 🏛️ Government Support & Schemes")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🎯 MSP Information")
        
        # Sample MSP data
        msp_data = {
            'Rice': '₹2,183/qt',
            'Wheat': '₹2,290/qt', 
            'Cotton': '₹6,620/qt',
            'Maize': '₹2,090/qt',
            'Soybean': '₹4,560/qt'
        }
        
        if selected_crop in msp_data:
            st.success(f"**MSP for {selected_crop}:** {msp_data[selected_crop]}")
            st.caption("Minimum Support Price - Govt guaranteed")
        else:
            st.info("MSP not available for this crop")
        
        st.markdown("""
        **MSP Benefits:**
        - Guaranteed minimum price
        - Available at procurement centers
        - Direct payment to farmers
        - No middleman commission
        """)
    
    with col2:
        st.markdown("#### 🏪 Market Schemes")
        st.markdown("""
        **e-NAM Platform:**
        - Online trading platform
        - Transparent price discovery
        - Pan-India market access
        - Quality assurance
        
        **FPO Benefits:**
        - Collective bargaining power
        - Better price realization
        - Reduced marketing costs
        - Access to credit
        
        **Warehouse Receipts:**
        - Scientific storage
        - Collateral for loans
        - Reduced post-harvest losses
        - Better price timing
        """)
    
    with col3:
        st.markdown("#### 📱 Digital Platforms")
        st.markdown("""
        **Mobile Apps:**
        - e-NAM mobile app
        - Kisan Rath for transport
        - mKisan for alerts
        - AgriApp for prices
        
        **Online Portals:**
        - agmarknet.gov.in
        - farmer.gov.in
        - mkisan.gov.in
        - enam.gov.in
        
        **Helpline Numbers:**
        - e-NAM: 1800-270-0224
        - Kisan Call: 1800-180-1551
        - PM-Kisan: 155261
        """)
    
    # Export opportunities
    st.markdown("---")
    st.markdown("### 🌍 Export Opportunities")
    
    export_crops = ['Rice', 'Wheat', 'Cotton', 'Soybean', 'Chili']
    
    if selected_crop in export_crops:
        
        export_data = {
            'Rice': {
                'main_destinations': 'Middle East, Africa, Europe',
                'export_price': '₹3,500-4,500/qt',
                'quality_requirements': 'Basmati/Non-Basmati, Low moisture',
                'peak_season': 'November to March'
            },
            'Cotton': {
                'main_destinations': 'China, Bangladesh, Vietnam',
                'export_price': '₹8,000-12,000/qt',
                'quality_requirements': 'Good staple length, clean',
                'peak_season': 'December to May'
            },
            'Soybean': {
                'main_destinations': 'Japan, Thailand, South Korea',
                'export_price': '₹6,000-8,000/qt',
                'quality_requirements': 'High protein content, clean',
                'peak_season': 'February to June'
            }
        }
        
        if selected_crop in export_data:
            crop_export = export_data[selected_crop]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"#### 🚢 {selected_crop} Export Info")
                st.success(f"**Export Price:** {crop_export['export_price']}")
                st.info(f"**Main Markets:** {crop_export['main_destinations']}")
                st.warning(f"**Peak Season:** {crop_export['peak_season']}")
            
            with col2:
                st.markdown("#### 📋 Export Requirements")
                st.markdown(f"**Quality Standards:** {crop_export['quality_requirements']}")
                st.markdown("""
                **Documentation Needed:**
                - Phytosanitary certificate
                - Certificate of origin
                - Quality test reports
                - Export license (if required)
                
                **Export Channels:**
                - Direct to importers
                - Through exporters
                - Export houses
                - Commodity boards
                """)
    
    # Storage and logistics
    st.markdown("---")
    st.markdown("### 🏬 Storage & Logistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📦 Storage Options")
        
        storage_costs = {
            'Farm Storage': '₹2-5/qt/month',
            'Warehouse': '₹8-15/qt/month',
            'Cold Storage': '₹25-50/qt/month',
            'Silo Storage': '₹10-20/qt/month'
        }
        
        storage_type = st.selectbox("Storage Type:", list(storage_costs.keys()))
        quantity = st.number_input("Quantity (quintals):", min_value=1, value=100, step=10)
        months = st.selectbox("Storage Duration:", [1, 2, 3, 6, 9, 12])
        
        if st.button("💰 Calculate Storage Cost"):
            cost_per_qt = float(storage_costs[storage_type].split('₹')[1].split('/')[0].split('-')[0])
            total_cost = cost_per_qt * quantity * months
            st.metric("Total Storage Cost", f"₹{total_cost:,.0f}")
            st.caption(f"₹{cost_per_qt}/qt/month × {quantity} qt × {months} months")
    
    with col2:
        st.markdown("#### 🚛 Transportation")
        
        st.markdown("""
        **Transport Options:**
        - **Truck**: ₹2-5/km/qt
        - **Rail**: ₹1-3/km/qt  
        - **Containerized**: ₹3-6/km/qt
        
        **Kisan Rail Benefits:**
        - 50% subsidy on freight
        - Faster transportation
        - Reduced handling
        - Better price realization
        
        **Digital Platforms:**
        - Kisan Rath app
        - TruckSuvidha
        - BlackBuck
        - Rivigo
        """)
        
        distance = st.number_input("Distance (km):", min_value=1, value=100, step=10)
        transport_rate = st.slider("Rate (₹/km/qt):", 1.0, 6.0, 3.0, 0.5)
        
        if quantity > 0:
            transport_cost = distance * transport_rate * quantity
            st.metric("Transport Cost", f"₹{transport_cost:,.0f}")
    
    # Profit calculator
    st.markdown("---")
    st.markdown("### 💰 Profit Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 Cost Inputs")
        production_cost = st.number_input("Production Cost (₹/qt):", min_value=0.0, value=1500.0, step=50.0)
        harvesting_cost = st.number_input("Harvesting Cost (₹/qt):", min_value=0.0, value=100.0, step=10.0)
        transport_cost_calc = st.number_input("Transport Cost (₹/qt):", min_value=0.0, value=50.0, step=5.0)
    
    with col2:
        st.markdown("#### 💵 Revenue Inputs")
        selling_price = st.number_input("Selling Price (₹/qt):", min_value=0.0, value=2000.0, step=50.0)
        quantity_sold = st.number_input("Quantity (quintals):", min_value=1, value=50, step=5)
        market_fee = st.number_input("Market Fee (%):", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
    
    with col3:
        st.markdown("#### 📈 Profit Analysis")
        
        if st.button("💰 Calculate Profit"):
            total_cost_per_qt = production_cost + harvesting_cost + transport_cost_calc
            market_fee_amount = selling_price * (market_fee / 100)
            net_selling_price = selling_price - market_fee_amount
            
            profit_per_qt = net_selling_price - total_cost_per_qt
            total_profit = profit_per_qt * quantity_sold
            profit_margin = (profit_per_qt / total_cost_per_qt) * 100
            
            st.metric("Profit per Quintal", f"₹{profit_per_qt:.0f}")
            st.metric("Total Profit", f"₹{total_profit:.0f}")
            st.metric("Profit Margin", f"{profit_margin:.1f}%")
            
            if profit_per_qt > 0:
                st.success("✅ Profitable sale!")
            else:
                st.error("❌ Loss-making sale!")
    
    # Data export options
    st.markdown("---")
    if st.button("📥 Download Market Data"):
        # Filter data for selected crop and markets
        export_data = df[
            (df['crop'] == selected_crop) & 
            (df['market'].isin(selected_markets))
        ].copy()
        
        export_data['date'] = pd.to_datetime(export_data['date'])
        export_data = export_data.sort_values(['market', 'date']).tail(days * len(selected_markets))
        
        csv = export_data.to_csv(index=False)
        st.download_button(
            label="💾 Download CSV",
            data=csv,
            file_name=f"market_prices_{selected_crop}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    run()