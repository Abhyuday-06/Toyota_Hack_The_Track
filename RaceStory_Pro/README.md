# 🏁 RaceStory Pro

**The Ultimate Post-Race Intelligence Dashboard for GR Cup Series**

> *Go beyond the final standings - understand the story behind every position, every decision, every moment that defined the race.*

## 🎯 Project Overview

RaceStory Pro is a comprehensive post-event analysis platform that transforms raw race data into actionable insights. By analyzing race results, weather conditions, pit strategies, and driver performance across multiple circuits and seasons, we reveal the hidden narratives that determine race outcomes.

### Category: Post-Event Analysis

## 🌟 Key Features

### 1. **Race Narrative Dashboard**
- Visual race progression from grid to finish
- Key overtaking moments identification
- Pit stop strategy impact analysis
- Weather condition tracking

### 2. **Strategic Decision Analyzer**
- Pit stop timing effectiveness
- Weather-adjusted pace analysis
- Sector-by-sector competitive comparison
- "What if" strategy scenarios

### 3. **Multi-Circuit Performance Insights**
- Driver performance trends (2024 vs 2025)
- Track-specific strengths/weaknesses
- Team strategy patterns per circuit
- Season progression analysis

### 4. **Weather Impact Assessment**
- Temperature vs lap time correlation
- Track conditions vs pit strategy
- Weather windows that changed outcomes

### 5. **Driver Performance Report Cards**
- Consistency analysis
- Sector time heatmaps
- Head-to-head comparisons
- Season-over-season improvement

## 📊 Data Sources

- **6 Racing Circuits**: Barber, COTA, Road America, Sebring, Sonoma, VIR
- **2 Seasons**: 2024 and 2025 GR Cup Series
- **Data Types**: 
  - Race results (official, provisional, unofficial)
  - Lap times and sector analysis
  - Pit stop data and time cards
  - Weather conditions
  - Grid positions and progressions
  - Driver performance metrics

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
pip
```

### Installation

1. Clone or navigate to the project directory
```bash
cd RaceStory_Pro
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the dashboard
```bash
streamlit run dashboard/app.py
```

## 📁 Project Structure

```
RaceStory_Pro/
├── data/                          # Processed data storage
├── src/
│   ├── data_processing/          # Data extraction & cleaning
│   │   ├── csv_parser.py        # CSV data processing
│   │   ├── pdf_extractor.py     # PDF data extraction
│   │   └── data_cleaner.py      # Data validation & cleaning
│   ├── analysis/                 # Core analytics engine
│   │   ├── race_analyzer.py     # Race progression analysis
│   │   ├── strategy_analyzer.py # Pit stop & strategy analysis
│   │   ├── weather_analyzer.py  # Weather impact analysis
│   │   └── driver_analyzer.py   # Driver performance metrics
│   └── visualization/            # Chart & graph generation
│       ├── race_viz.py          # Race visualizations
│       ├── strategy_viz.py      # Strategy visualizations
│       └── performance_viz.py   # Performance dashboards
├── dashboard/                    # Streamlit web app
│   └── app.py                   # Main dashboard application
├── requirements.txt              # Python dependencies
└── README.md                    # This file
```

## 🎨 Dashboard Sections

1. **Race Overview** - Complete race summary with key statistics
2. **Race Replay** - Animated progression visualization
3. **Strategy Analysis** - Pit stop and strategic decision breakdown
4. **Weather Impact** - Condition correlation analysis
5. **Driver Insights** - Individual and comparative performance
6. **Season Comparison** - Multi-season trend analysis

## 🏆 Technical Highlights

- **Interactive Visualizations** using Plotly
- **Real-time Dashboard** with Streamlit
- **PDF Data Extraction** for comprehensive insights
- **Multi-dimensional Analysis** across circuits, seasons, and conditions
- **Export Capabilities** for reports and presentations

## 👥 Team

Built for the Toyota Gazoo Racing Hackathon 2025

## 📄 License

This project is developed for the Toyota Gazoo Racing Hackathon 2025.

---

**Let the data tell the story. 🏁**
