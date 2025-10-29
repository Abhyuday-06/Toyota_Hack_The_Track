"""
RaceStory Pro - Main Dashboard
Post-Event Race Analysis Platform for GR Cup Series
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data_processing.csv_parser import CSVParser
from data_processing.pdf_extractor import PDFExtractor
from analysis.race_analyzer import RaceAnalyzer

# Page configuration
st.set_page_config(
    page_title="RaceStory Pro",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #FF0000, #000000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF0000;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🏁 RaceStory Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">The Ultimate Post-Race Intelligence Dashboard for GR Cup Series</p>', 
            unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/FF0000/FFFFFF?text=GR+Cup", 
             use_container_width=True)
    
    st.markdown("## 🏎️ Race Selection")
    
    # Circuit selection
    circuits = {
        'Barber Motorsports Park': 'barber',
        'Circuit of the Americas (COTA)': 'cota',
        'Road America': 'road-america',
        'Sebring International Raceway': 'sebring',
        'Sonoma Raceway': 'sonoma',
        'Virginia International Raceway (VIR)': 'vir'
    }
    
    selected_circuit = st.selectbox(
        "Select Circuit",
        options=list(circuits.keys())
    )
    
    # Season selection
    selected_season = st.selectbox(
        "Select Season",
        options=['2025 season', '2024 season']
    )
    
    # Session selection
    sessions = [
        'race 1', 'race 2',
        'qualifying 1', 'qualifying 2',
        'practice 1', 'practice 2',
        'test session 1', 'test session 2'
    ]
    
    selected_session = st.selectbox(
        "Select Session",
        options=sessions
    )
    
    st.markdown("---")
    
    load_data = st.button("📊 Load Race Data", type="primary", use_container_width=True)

# Main content
if load_data:
    with st.spinner("Loading race data..."):
        try:
            # Initialize parsers
            # Go up 3 levels: app.py -> dashboard -> RaceStory_Pro -> Toyota_Gazoo_Racing_Hackathon25
            base_path = str(Path(__file__).resolve().parent.parent.parent)
            csv_parser = CSVParser(base_path)
            analyzer = RaceAnalyzer()
            
            # Load data
            circuit_key = circuits[selected_circuit]
            race_data = csv_parser.load_race_data(circuit_key, selected_season, selected_session)
            
            if not race_data:
                st.error("❌ No data found for the selected race session.")
            else:
                st.success(f"✅ Successfully loaded data for {selected_circuit} - {selected_season} - {selected_session}")
                
                # Tabs for different analyses
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📊 Race Overview",
                    "🏆 Results Analysis", 
                    "🌤️ Weather Data",
                    "⚡ Performance Insights"
                ])
                
                with tab1:
                    st.markdown("### 🏁 Race Overview")
                    
                    # Generate race summary
                    if 'results' in race_data and not race_data['results'].empty:
                        try:
                            summary = analyzer.generate_race_summary(race_data)
                        except Exception as e:
                            st.error(f"Error generating race summary: {str(e)}")
                            st.write("Available columns in results:", list(race_data['results'].columns))
                            summary = None
                        
                        if summary:
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown("#### 🥇 Race Winner")
                                if summary.get('winner'):
                                    st.metric("Driver", summary['winner']['driver'])
                                    st.metric("Car #", summary['winner']['car_number'])
                                    st.metric("Team", summary['winner']['team'])
                        
                        with col2:
                            st.markdown("#### ⚡ Fastest Lap")
                            if summary['fastest_lap']:
                                st.metric("Driver", summary['fastest_lap']['driver'])
                                st.metric("Time", summary['fastest_lap']['time'])
                                st.metric("Speed", f"{summary['fastest_lap']['speed']} km/h")
                        
                        with col3:
                            st.markdown("#### 📈 Race Stats")
                            st.metric("Total Finishers", summary['total_finishers'])
                            st.metric("Close Battles", len(summary['close_battles']))
                    else:
                        st.info("No race results data available for this session.")
                
                with tab2:
                    st.markdown("### 🏆 Detailed Results")
                    
                    if 'results' in race_data and not race_data['results'].empty:
                        results_df = race_data['results']
                        
                        # Display key columns
                        display_cols = ['POSITION', 'NUMBER', 'DRIVER_FIRSTNAME', 
                                       'DRIVER_SECONDNAME', 'TEAM', 'LAPS', 
                                       'TOTAL_TIME', 'FL_TIME', 'STATUS']
                        
                        available_cols = [col for col in display_cols if col in results_df.columns]
                        st.dataframe(results_df[available_cols], use_container_width=True, height=400)
                        
                        # Close battles
                        st.markdown("### ⚔️ Close Battles")
                        battles = analyzer.identify_key_battles(results_df)
                        
                        if battles:
                            for battle in battles[:5]:  # Show top 5
                                st.markdown(f"**Position {battle['position']}**: {battle['driver']} "
                                          f"(#{battle['car_number']}) - Gap: {battle['gap']:.3f}s")
                        else:
                            st.info("No close battles detected (gap > 5 seconds)")
                    else:
                        st.info("No results data available.")
                
                with tab3:
                    st.markdown("### 🌤️ Weather Conditions")
                    
                    if 'weather' in race_data and not race_data['weather'].empty:
                        weather_df = race_data['weather']
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            avg_air_temp = weather_df['AIR_TEMP'].mean() if 'AIR_TEMP' in weather_df else 0
                            st.metric("Avg Air Temp", f"{avg_air_temp:.1f}°C")
                        
                        with col2:
                            avg_track_temp = weather_df['TRACK_TEMP'].mean() if 'TRACK_TEMP' in weather_df else 0
                            st.metric("Avg Track Temp", f"{avg_track_temp:.1f}°C")
                        
                        with col3:
                            avg_humidity = weather_df['HUMIDITY'].mean() if 'HUMIDITY' in weather_df else 0
                            st.metric("Avg Humidity", f"{avg_humidity:.1f}%")
                        
                        with col4:
                            avg_wind = weather_df['WIND_SPEED'].mean() if 'WIND_SPEED' in weather_df else 0
                            st.metric("Avg Wind Speed", f"{avg_wind:.1f} m/s")
                        
                        # Weather data table
                        st.markdown("### 📊 Weather Throughout Race")
                        display_weather = weather_df[['TIME_UTC_STR', 'AIR_TEMP', 'TRACK_TEMP', 
                                                       'HUMIDITY', 'WIND_SPEED']]
                        st.dataframe(display_weather, use_container_width=True, height=300)
                    else:
                        st.info("No weather data available for this session.")
                
                with tab4:
                    st.markdown("### ⚡ Performance Insights")
                    
                    if 'best_laps' in race_data and not race_data['best_laps'].empty:
                        consistency_df = analyzer.calculate_consistency(race_data['best_laps'])
                        
                        if not consistency_df.empty:
                            st.markdown("### 🎯 Driver Consistency Analysis")
                            st.markdown("*Based on standard deviation of best 10 laps*")
                            
                            top_consistent = consistency_df.head(10)
                            
                            for idx, row in top_consistent.iterrows():
                                col1, col2, col3 = st.columns([2, 1, 1])
                                with col1:
                                    st.markdown(f"**{row['driver']}** (#{row['car_number']})")
                                with col2:
                                    st.metric("Best Lap", f"{row['best_lap']:.3f}s")
                                with col3:
                                    st.metric("Consistency", f"{row['consistency_score']:.2f}")
                        else:
                            st.info("Insufficient lap data for consistency analysis.")
                    else:
                        st.info("No performance data available.")
        
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            st.exception(e)
else:
    # Welcome screen
    st.markdown("## 👈 Select a race session from the sidebar to begin analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Race Overview")
        st.markdown("""
        - Complete race summary
        - Winner & fastest lap
        - Key race statistics
        - Close battle identification
        """)
    
    with col2:
        st.markdown("### 🌤️ Weather Impact")
        st.markdown("""
        - Air & track temperatures
        - Humidity levels
        - Wind conditions
        - Weather progression
        """)
    
    with col3:
        st.markdown("### ⚡ Performance")
        st.markdown("""
        - Driver consistency analysis
        - Lap time breakdowns
        - Comparative insights
        - Season progression
        """)
    
    st.markdown("---")
    st.markdown("### 🏎️ Available Data")
    st.markdown("""
    **6 Racing Circuits**: Barber, COTA, Road America, Sebring, Sonoma, VIR  
    **2 Seasons**: 2024 & 2025  
    **8 Session Types**: Races, Qualifying, Practice, Test Sessions
    """)

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666;">🏁 RaceStory Pro - Toyota Gazoo Racing Hackathon 2025</p>',
    unsafe_allow_html=True
)
