import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

def load_community_alerts():
    """Load community alerts data"""
    data_path = Path(__file__).parent.parent / "data" / "community_alerts.csv"
    if data_path.exists():
        return pd.read_csv(data_path)
    else:
        # Sample community alerts data
        sample_data = [
            {
                'id': 'CA001',
                'farmer_name': 'Rajesh Kumar',
                'location': 'Ludhiana, Punjab',
                'alert_type': 'Pest Outbreak',
                'crop_affected': 'Rice',
                'severity': 'High',
                'description': 'Stem borer infestation observed in 5 acres of paddy fields. Started 3 days ago.',
                'date_posted': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
                'status': 'Active',
                'contact_phone': '+91-9876543210',
                'verified': True,
                'helpful_votes': 15,
                'solution_provided': 'Applied Bt spray and pheromone traps. Seeing improvement.',
                'estimated_area': '25 acres',
                'tags': 'pest,rice,stem-borer'
            },
            {
                'id': 'CA002', 
                'farmer_name': 'Sita Devi',
                'location': 'Nashik, Maharashtra',
                'alert_type': 'Disease Warning',
                'crop_affected': 'Tomato',
                'severity': 'Medium',
                'description': 'Early blight disease symptoms appearing on tomato plants. Yellow spots on lower leaves.',
                'date_posted': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'status': 'Active',
                'contact_phone': '+91-9876543211',
                'verified': True,
                'helpful_votes': 8,
                'solution_provided': '',
                'estimated_area': '10 acres',
                'tags': 'disease,tomato,early-blight'
            },
            {
                'id': 'CA003',
                'farmer_name': 'Kumar Singh',
                'location': 'Meerut, Uttar Pradesh',
                'alert_type': 'Weather Alert',
                'crop_affected': 'Wheat',
                'severity': 'High',
                'description': 'Unexpected hailstorm damaged wheat crops yesterday evening. Need advice on recovery.',
                'date_posted': datetime.now().strftime('%Y-%m-%d'),
                'status': 'Active',
                'contact_phone': '+91-9876543212',
                'verified': False,
                'helpful_votes': 3,
                'solution_provided': '',
                'estimated_area': '50 acres',
                'tags': 'weather,wheat,hailstorm'
            },
            {
                'id': 'CA004',
                'farmer_name': 'Priya Patel',
                'location': 'Anand, Gujarat',
                'alert_type': 'Success Story',
                'crop_affected': 'Cotton',
                'severity': 'Low',
                'description': 'Successfully controlled bollworm using IPM approach. 40% reduction in pesticide use.',
                'date_posted': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                'status': 'Resolved',
                'contact_phone': '+91-9876543213',
                'verified': True,
                'helpful_votes': 22,
                'solution_provided': 'Used Bt cotton + refuge strategy with pheromone traps and beneficial insects.',
                'estimated_area': '20 acres',
                'tags': 'success,cotton,bollworm,ipm'
            },
            {
                'id': 'CA005',
                'farmer_name': 'Mohan Reddy',
                'location': 'Warangal, Telangana',
                'alert_type': 'Input Shortage',
                'crop_affected': 'Rice',
                'severity': 'Medium',
                'description': 'Local seed supplier out of quality paddy seeds. Need alternative sources.',
                'date_posted': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'status': 'Active',
                'contact_phone': '+91-9876543214',
                'verified': True,
                'helpful_votes': 5,
                'solution_provided': '',
                'estimated_area': '15 acres',
                'tags': 'inputs,seeds,rice'
            }
        ]
        
        return pd.DataFrame(sample_data)

def save_community_alert(alert_data):
    """Save new community alert"""
    # In a real application, this would save to database
    # For demo, we'll just show success message
    return True

def get_alert_stats(df):
    """Get community alert statistics"""
    stats = {
        'total_alerts': len(df),
        'active_alerts': len(df[df['status'] == 'Active']),
        'resolved_alerts': len(df[df['status'] == 'Resolved']),
        'verified_alerts': len(df[df['verified'] == True]),
        'avg_helpful_votes': df['helpful_votes'].mean(),
        'top_alert_type': df['alert_type'].value_counts().index[0] if len(df) > 0 else 'None'
    }
    return stats

def run():
    """Main function for community alerts module"""
    
    st.markdown("## 👥 Community Alert System")
    st.markdown("Share and discover agricultural alerts from fellow farmers in your region.")
    
    # Load community data
    alerts_df = load_community_alerts()
    
    # Sidebar for actions
    with st.sidebar:
        st.markdown("### 🚀 Quick Actions")
        action = st.radio(
            "What would you like to do?",
            ["📋 View Alerts", "📝 Post Alert", "🔍 Search Alerts", "📊 Analytics"],
            key="community_action"
        )
        
        st.markdown("---")
        st.markdown("### 🏷️ Filter Options")
        
        # Filter controls
        alert_type_filter = st.multiselect(
            "Alert Type:",
            alerts_df['alert_type'].unique(),
            default=alerts_df['alert_type'].unique()
        )
        
        severity_filter = st.multiselect(
            "Severity Level:",
            ['Low', 'Medium', 'High'],
            default=['Medium', 'High']
        )
        
        status_filter = st.multiselect(
            "Status:",
            ['Active', 'Resolved'],
            default=['Active']
        )
        
        location_filter = st.text_input("📍 Location (optional):", placeholder="e.g., Punjab, Maharashtra")
    
    # Apply filters
    filtered_df = alerts_df.copy()
    
    if alert_type_filter:
        filtered_df = filtered_df[filtered_df['alert_type'].isin(alert_type_filter)]
    
    if severity_filter:
        filtered_df = filtered_df[filtered_df['severity'].isin(severity_filter)]
    
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    
    if location_filter:
        filtered_df = filtered_df[filtered_df['location'].str.contains(location_filter, case=False, na=False)]
    
    # Main content based on selected action
    if action == "📋 View Alerts":
        show_alerts_view(filtered_df)
    
    elif action == "📝 Post Alert":
        show_post_alert_form()
    
    elif action == "🔍 Search Alerts":
        show_search_alerts(alerts_df)
    
    elif action == "📊 Analytics":
        show_community_analytics(alerts_df)

def show_alerts_view(filtered_df):
    """Show alerts view with filtering and sorting"""
    
    # Community stats overview
    stats = get_alert_stats(filtered_df)
    
    st.markdown("### 📊 Community Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Alerts", stats['total_alerts'])
    
    with col2:
        st.metric("Active Issues", stats['active_alerts'])
    
    with col3:
        st.metric("Resolved", stats['resolved_alerts'])
    
    with col4:
        st.metric("Verified Alerts", stats['verified_alerts'])
    
    st.markdown("---")
    
    # Sort options
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox(
            "📋 Sort by:",
            ["Date Posted", "Helpful Votes", "Severity", "Location"],
            key="sort_alerts"
        )
    
    with col2:
        sort_order = st.selectbox(
            "🔄 Order:",
            ["Newest First", "Oldest First"] if sort_by == "Date Posted" else ["Descending", "Ascending"]
        )
    
    # Apply sorting
    sort_mapping = {
        "Date Posted": "date_posted",
        "Helpful Votes": "helpful_votes",
        "Severity": "severity",
        "Location": "location"
    }
    
    sort_col = sort_mapping[sort_by]
    ascending = sort_order in ["Oldest First", "Ascending"]
    
    if sort_by == "Severity":
        # Custom severity sorting
        severity_order = {'High': 3, 'Medium': 2, 'Low': 1}
        filtered_df['severity_rank'] = filtered_df['severity'].map(severity_order)
        filtered_df = filtered_df.sort_values('severity_rank', ascending=ascending)
    else:
        filtered_df = filtered_df.sort_values(sort_col, ascending=ascending)
    
    # Display alerts
    st.markdown(f"### 🚨 Community Alerts ({len(filtered_df)} found)")
    
    if filtered_df.empty:
        st.info("No alerts match your current filters. Try adjusting the filter options.")
        return
    
    for idx, (_, alert) in enumerate(filtered_df.iterrows()):
        
        # Alert severity color coding
        severity_colors = {
            'High': '🔴',
            'Medium': '🟡', 
            'Low': '🟢'
        }
        
        status_colors = {
            'Active': '🔥',
            'Resolved': '✅'
        }
        
        verified_badge = '✅ Verified' if alert['verified'] else '⚠️ Unverified'
        
        with st.expander(
            f"{severity_colors[alert['severity']]} {alert['alert_type']} - {alert['crop_affected']} | {alert['location']} {status_colors[alert['status']]}",
            expanded=idx < 3  # Expand first 3 alerts
        ):
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**📝 Description:** {alert['description']}")
                
                if alert['solution_provided']:
                    st.success(f"**💡 Solution:** {alert['solution_provided']}")
                
                st.markdown(f"**👨‍🌾 Reported by:** {alert['farmer_name']}")
                st.markdown(f"**📍 Location:** {alert['location']}")
                st.markdown(f"**🌾 Crop:** {alert['crop_affected']}")
                st.markdown(f"**📏 Affected Area:** {alert['estimated_area']}")
                st.caption(f"**🏷️ Tags:** {alert['tags']}")
            
            with col2:
                st.markdown(f"**📅 Posted:** {alert['date_posted']}")
                st.markdown(f"**⚡ Severity:** {alert['severity']}")
                st.markdown(f"**📊 Status:** {alert['status']}")
                st.markdown(f"**👍 Helpful Votes:** {alert['helpful_votes']}")
                st.markdown(f"**🔒 Status:** {verified_badge}")
                
                # Action buttons
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("👍", key=f"helpful_{alert['id']}"):
                        st.success("Marked as helpful!")
                
                with col_b:
                    if st.button("📞", key=f"contact_{alert['id']}"):
                        st.info(f"Contact: {alert['contact_phone']}")
                
                with col_c:
                    if st.button("💬", key=f"comment_{alert['id']}"):
                        st.text_area("Add your comment:", key=f"comment_text_{alert['id']}")

def show_post_alert_form():
    """Show form to post new community alert"""
    
    st.markdown("### 📝 Post a New Community Alert")
    st.markdown("Share important agricultural information with fellow farmers in your region.")
    
    with st.form("post_alert_form"):
        
        col1, col2 = st.columns(2)
        
        with col1:
            farmer_name = st.text_input(
                "👨‍🌾 Your Name *:",
                help="Your name will be displayed with the alert"
            )
            
            location = st.text_input(
                "📍 Location *:",
                placeholder="Village, District, State",
                help="Be specific about location"
            )
            
            alert_type = st.selectbox(
                "🚨 Alert Type *:",
                ["Pest Outbreak", "Disease Warning", "Weather Alert", "Success Story", 
                 "Input Shortage", "Equipment Help", "Market Information", "Other"]
            )
            
            crop_affected = st.selectbox(
                "🌾 Crop Affected:",
                ["Rice", "Wheat", "Cotton", "Tomato", "Potato", "Maize", "Onion", 
                 "Soybean", "Sugarcane", "Other"]
            )
        
        with col2:
            severity = st.selectbox(
                "⚡ Severity Level *:",
                ["Low", "Medium", "High"],
                index=1,
                help="How urgent is this alert?"
            )
            
            estimated_area = st.text_input(
                "📏 Affected Area:",
                placeholder="e.g., 10 acres, 5 hectares",
                help="Approximate area affected"
            )
            
            contact_phone = st.text_input(
                "📞 Contact Number:",
                placeholder="+91-XXXXXXXXXX",
                help="Optional - for other farmers to contact you"
            )
            
            tags = st.text_input(
                "🏷️ Tags:",
                placeholder="pest, disease, rice (comma separated)",
                help="Keywords to help others find your alert"
            )
        
        description = st.text_area(
            "📝 Detailed Description *:",
            height=100,
            placeholder="Describe the issue, symptoms, timeline, and any other relevant details...",
            help="Provide as much detail as possible"
        )
        
        solution_provided = st.text_area(
            "💡 Solution (if any):",
            height=80,
            placeholder="If you've found a solution or tried something, share it here...",
            help="Help others by sharing what worked"
        )
        
        # Image upload placeholder
        uploaded_image = st.file_uploader(
            "📸 Upload Image (optional):",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image showing the problem"
        )
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            agree_terms = st.checkbox(
                "I agree to community guidelines",
                help="By posting, you agree to provide accurate information"
            )
        
        with col2:
            allow_contact = st.checkbox(
                "Allow farmers to contact me",
                value=True,
                help="Other farmers can reach out for more details"
            )
        
        with col3:
            submit_button = st.form_submit_button(
                "📤 Post Alert",
                type="primary",
                use_container_width=True
            )
        
        # Form submission handling
        if submit_button:
            # Validation
            errors = []
            
            if not farmer_name:
                errors.append("Farmer name is required")
            if not location:
                errors.append("Location is required")
            if not description:
                errors.append("Description is required")
            if not agree_terms:
                errors.append("Must agree to community guidelines")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Create alert data
                new_alert = {
                    'id': f"CA{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'farmer_name': farmer_name,
                    'location': location,
                    'alert_type': alert_type,
                    'crop_affected': crop_affected,
                    'severity': severity,
                    'description': description,
                    'date_posted': datetime.now().strftime('%Y-%m-%d'),
                    'status': 'Active',
                    'contact_phone': contact_phone if allow_contact else '',
                    'verified': False,
                    'helpful_votes': 0,
                    'solution_provided': solution_provided,
                    'estimated_area': estimated_area,
                    'tags': tags.lower().replace(' ', '') if tags else ''
                }
                
                # Save alert (in real app, would save to database)
                if save_community_alert(new_alert):
                    st.success("✅ Alert posted successfully!")
                    st.balloons()
                    st.info("📢 Your alert will be reviewed and made visible to the community shortly.")
                    
                    # Show preview
                    st.markdown("### 👀 Preview of Your Alert")
                    
                    severity_colors = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                    
                    with st.container():
                        st.markdown(f"**{severity_colors[severity]} {alert_type} - {crop_affected} | {location} 🔥**")
                        st.markdown(f"**📝 Description:** {description}")
                        
                        if solution_provided:
                            st.success(f"**💡 Solution:** {solution_provided}")
                        
                        st.markdown(f"**👨‍🌾 Reported by:** {farmer_name}")
                        st.markdown(f"**📍 Location:** {location}")
                        st.markdown(f"**📏 Affected Area:** {estimated_area}")
                        st.caption(f"**🏷️ Tags:** {tags}")

def show_search_alerts(alerts_df):
    """Show search functionality for alerts"""
    
    st.markdown("### 🔍 Search Community Alerts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_query = st.text_input(
            "🔍 Search Keywords:",
            placeholder="e.g., rice pest, tomato disease, weather damage",
            help="Search in descriptions, crops, locations, and tags"
        )
    
    with col2:
        search_in = st.multiselect(
            "🎯 Search In:",
            ["Description", "Crop", "Location", "Tags", "Solution"],
            default=["Description", "Crop", "Tags"]
        )
    
    if search_query:
        search_results = alerts_df.copy()
        query_lower = search_query.lower()
        
        # Create search conditions
        conditions = []
        
        if "Description" in search_in:
            conditions.append(search_results['description'].str.lower().str.contains(query_lower, na=False))
        
        if "Crop" in search_in:
            conditions.append(search_results['crop_affected'].str.lower().str.contains(query_lower, na=False))
        
        if "Location" in search_in:
            conditions.append(search_results['location'].str.lower().str.contains(query_lower, na=False))
        
        if "Tags" in search_in:
            conditions.append(search_results['tags'].str.lower().str.contains(query_lower, na=False))
        
        if "Solution" in search_in:
            conditions.append(search_results['solution_provided'].str.lower().str.contains(query_lower, na=False))
        
        # Combine conditions with OR
        if conditions:
            combined_condition = conditions[0]
            for condition in conditions[1:]:
                combined_condition = combined_condition | condition
            
            search_results = search_results[combined_condition]
        
        st.markdown(f"### 📋 Search Results ({len(search_results)} found)")
        
        if search_results.empty:
            st.info("No alerts found matching your search criteria.")
        else:
            # Display search results
            for _, alert in search_results.iterrows():
                with st.expander(f"🎯 {alert['alert_type']} - {alert['crop_affected']} | {alert['location']}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Highlight search terms in description
                        description = alert['description']
                        if query_lower in description.lower():
                            # Simple highlighting (would be better with regex)
                            highlighted = description.replace(
                                query_lower, f"**{query_lower}**"
                            ).replace(
                                query_lower.title(), f"**{query_lower.title()}**"
                            )
                            st.markdown(f"**📝 Description:** {highlighted}")
                        else:
                            st.markdown(f"**📝 Description:** {description}")
                        
                        if alert['solution_provided']:
                            st.success(f"**💡 Solution:** {alert['solution_provided']}")
                    
                    with col2:
                        st.markdown(f"**📅 Posted:** {alert['date_posted']}")
                        st.markdown(f"**⚡ Severity:** {alert['severity']}")
                        st.markdown(f"**👍 Helpful:** {alert['helpful_votes']}")
    
    # Popular searches
    st.markdown("---")
    st.markdown("### 🔥 Popular Searches")
    
    popular_searches = [
        "rice pest", "tomato disease", "wheat rust", "cotton bollworm", 
        "weather damage", "fertilizer shortage", "irrigation problems", "market prices"
    ]
    
    cols = st.columns(4)
    for i, search_term in enumerate(popular_searches):
        with cols[i % 4]:
            if st.button(f"🔍 {search_term}", key=f"popular_{i}"):
                st.experimental_set_query_params(search=search_term)

def show_community_analytics(alerts_df):
    """Show community analytics and insights"""
    
    st.markdown("### 📊 Community Analytics")
    
    # Overall statistics
    stats = get_alert_stats(alerts_df)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Alerts", stats['total_alerts'])
    
    with col2:
        st.metric("Active Issues", stats['active_alerts'])
    
    with col3:
        st.metric("Resolved", stats['resolved_alerts'])
    
    with col4:
        st.metric("Verified", stats['verified_alerts'])
    
    with col5:
        st.metric("Avg. Helpfulness", f"{stats['avg_helpful_votes']:.1f}")
    
    st.markdown("---")
    
    # Charts and visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Alert Types Distribution")
        alert_type_counts = alerts_df['alert_type'].value_counts()
        
        import plotly.express as px
        fig_types = px.pie(
            values=alert_type_counts.values,
            names=alert_type_counts.index,
            title="Distribution of Alert Types"
        )
        st.plotly_chart(fig_types, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Severity Levels")
        severity_counts = alerts_df['severity'].value_counts()
        
        fig_severity = px.bar(
            x=severity_counts.index,
            y=severity_counts.values,
            title="Alerts by Severity Level",
            color=severity_counts.index,
            color_discrete_map={
                'High': '#ff4444',
                'Medium': '#ffaa00', 
                'Low': '#44ff44'
            }
        )
        st.plotly_chart(fig_severity, use_container_width=True)
    
    # Geographic distribution
    st.markdown("---")
    st.markdown("#### 🗺️ Geographic Distribution")
    
    # Extract states from location
    alerts_df['state'] = alerts_df['location'].str.split(',').str[-1].str.strip()
    state_counts = alerts_df['state'].value_counts().head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_geo = px.bar(
            x=state_counts.values,
            y=state_counts.index,
            orientation='h',
            title="Top 10 States by Alert Volume",
            labels={'x': 'Number of Alerts', 'y': 'State'}
        )
        st.plotly_chart(fig_geo, use_container_width=True)
    
    with col2:
        st.markdown("#### 🌾 Crop-wise Alerts")
        crop_counts = alerts_df['crop_affected'].value_counts().head(8)
        
        fig_crops = px.bar(
            x=crop_counts.index,
            y=crop_counts.values,
            title="Most Affected Crops",
            labels={'x': 'Crops', 'y': 'Number of Alerts'}
        )
        fig_crops.update_xaxis(tickangle=45)
        st.plotly_chart(fig_crops, use_container_width=True)
    
    # Timeline analysis
    st.markdown("---")
    st.markdown("#### 📅 Alert Timeline")
    
    alerts_df['date_posted'] = pd.to_datetime(alerts_df['date_posted'])
    alerts_df['week'] = alerts_df['date_posted'].dt.to_period('W')
    weekly_counts = alerts_df.groupby('week').size()
    
    import plotly.graph_objects as go
    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Scatter(
        x=[str(week) for week in weekly_counts.index],
        y=weekly_counts.values,
        mode='lines+markers',
        name='Alerts per Week',
        line=dict(width=3)
    ))
    
    fig_timeline.update_layout(
        title='Alert Activity Over Time',
        xaxis_title='Week',
        yaxis_title='Number of Alerts'
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Top contributors and most helpful alerts
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Top Contributors")
        contributor_counts = alerts_df['farmer_name'].value_counts().head(5)
        
        for i, (farmer, count) in enumerate(contributor_counts.items()):
            st.write(f"{i+1}. **{farmer}**: {count} alerts")
    
    with col2:
        st.markdown("#### 👍 Most Helpful Alerts")
        helpful_alerts = alerts_df.nlargest(5, 'helpful_votes')[['farmer_name', 'alert_type', 'helpful_votes']]
        
        for _, alert in helpful_alerts.iterrows():
            st.write(f"• **{alert['alert_type']}** by {alert['farmer_name']} ({alert['helpful_votes']} votes)")
    
    # Community insights
    st.markdown("---")
    st.markdown("### 💡 Community Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🎯 Key Trends")
        
        # Calculate trends
        pest_alerts = len(alerts_df[alerts_df['alert_type'] == 'Pest Outbreak'])
        disease_alerts = len(alerts_df[alerts_df['alert_type'] == 'Disease Warning'])
        success_stories = len(alerts_df[alerts_df['alert_type'] == 'Success Story'])
        
        st.info(f"""
        **Current Issues:**
        - {pest_alerts} pest outbreaks reported
        - {disease_alerts} disease warnings active
        - {success_stories} success stories shared
        
        **Most Affected:** {alerts_df['crop_affected'].value_counts().index[0]}
        
        **Active Regions:** {', '.join(alerts_df['state'].value_counts().head(3).index)}
        """)
    
    with col2:
        st.markdown("#### 🚀 Community Impact")
        
        total_area = 0
        for area_str in alerts_df['estimated_area'].dropna():
            try:
                # Extract numeric value from area string
                import re
                numbers = re.findall(r'\d+', str(area_str))
                if numbers:
                    total_area += int(numbers[0])
            except:
                pass
        
        st.success(f"""
        **Community Reach:**
        - {stats['total_alerts']} farmers participated
        - ~{total_area:,} acres monitored
        - {stats['verified_alerts']} verified reports
        - {int(stats['avg_helpful_votes'] * len(alerts_df))} helpful interactions
        
        **Knowledge Sharing:**
        - {len(alerts_df[alerts_df['solution_provided'] != ''])} solutions shared
        """)
    
    with col3:
        st.markdown("#### 📈 Recommendations")
        
        # Generate recommendations based on data
        recommendations = []
        
        if pest_alerts > disease_alerts:
            recommendations.append("Focus on pest management training")
        else:
            recommendations.append("Increase disease prevention awareness")
        
        if stats['verified_alerts'] / stats['total_alerts'] < 0.7:
            recommendations.append("Improve alert verification process")
        
        if success_stories < stats['total_alerts'] * 0.2:
            recommendations.append("Encourage sharing success stories")
        
        recommendations.append("Organize regional farmer meetups")
        recommendations.append("Create mobile app for faster reporting")
        
        for rec in recommendations:
            st.write(f"• {rec}")
    
    # Export functionality
    st.markdown("---")
    if st.button("📥 Download Community Data"):
        # Prepare data for export
        export_data = alerts_df.copy()
        # Remove sensitive information
        export_data = export_data.drop(['contact_phone'], axis=1, errors='ignore')
        
        csv = export_data.to_csv(index=False)
        st.download_button(
            label="💾 Download Analytics Report (CSV)",
            data=csv,
            file_name=f"community_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    run()