# 🚀 RaceStory Pro - Quick Start Guide

## Installation & Setup

### 1. Navigate to Project Directory
```bash
cd e:\Programming\Toyota_Gazoo_Racing_Hackathon25\RaceStory_Pro
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Dashboard
```bash
streamlit run dashboard/app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## 📖 Using the Dashboard

### Step 1: Select Race Data
1. Use the sidebar to choose:
   - **Circuit**: Select from 6 available tracks
   - **Season**: Choose 2024 or 2025
   - **Session**: Pick race, qualifying, practice, or test

### Step 2: Load Data
2. Click the **"📊 Load Race Data"** button

### Step 3: Explore Analysis
3. Navigate through the tabs:
   - **📊 Race Overview**: Winner, fastest lap, key stats
   - **🏆 Results Analysis**: Detailed standings and battles
   - **🌤️ Weather Data**: Conditions throughout the race
   - **⚡ Performance Insights**: Driver consistency analysis

## 🎯 Available Analyses

### Race Overview
- Race winner and winning margin
- Fastest lap details
- Total finishers
- Close battle detection

### Results Analysis
- Complete standings with lap times
- Position-by-position breakdown
- Close battles (< 5 second gaps)
- Team performance

### Weather Analysis
- Air and track temperature
- Humidity levels
- Wind speed and direction
- Weather progression throughout race

### Performance Insights
- Driver consistency scoring
- Best lap analysis
- Comparative performance
- Season progression

## 📊 Data Coverage

### Circuits
- ✅ Barber Motorsports Park
- ✅ Circuit of the Americas (COTA)
- ✅ Road America
- ✅ Sebring International Raceway
- ✅ Sonoma Raceway
- ✅ Virginia International Raceway (VIR)

### Sessions Per Circuit
- 2024 Season: 8 sessions
- 2025 Season: 8 sessions
- **Total**: 96 session folders

## 🔧 Troubleshooting

### Error: Module not found
```bash
# Make sure you're in the RaceStory_Pro directory
cd RaceStory_Pro
pip install -r requirements.txt
```

### Error: No data found
- Verify the circuit/season/session combination has CSV files
- Check that you're in the correct directory
- Some sessions may not have all data types

### Dashboard won't load
```bash
# Try running with verbose mode
streamlit run dashboard/app.py --logger.level=debug
```

## 🎨 Next Steps

### Phase 2 Enhancements
- [ ] Add visualization charts (Plotly)
- [ ] Implement race replay animation
- [ ] Add strategy timeline
- [ ] Multi-race comparison
- [ ] Season progression tracking

### Phase 3 Advanced Features
- [ ] PDF data integration
- [ ] Pit stop analysis
- [ ] Sector time heatmaps
- [ ] Weather correlation analysis
- [ ] Predictive insights

## 📝 Development Notes

### Project Structure
```
RaceStory_Pro/
├── dashboard/          # Streamlit web app
├── src/
│   ├── data_processing/  # CSV & PDF parsers
│   ├── analysis/         # Analytics engine
│   └── visualization/    # Charts & graphs
├── data/              # Processed data storage
└── requirements.txt   # Dependencies
```

### Adding New Analysis
1. Create new analyzer in `src/analysis/`
2. Import in `dashboard/app.py`
3. Add new tab or section in dashboard
4. Test with sample data

## 🏁 Ready to Analyze!

Your RaceStory Pro dashboard is ready to reveal the stories behind every race. Select a session and start exploring! 🏎️

---
**Questions?** Check the main README.md for detailed documentation.
