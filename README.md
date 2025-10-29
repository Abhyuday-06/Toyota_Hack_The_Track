# Toyota Gazoo Racing Hackathon 2025 Project

Welcome to the repository for the Toyota Gazoo Racing Hackathon 2025! This project contains the `RaceStory Pro` application, a post-event analysis dashboard, as well as the raw data used for the hackathon.

## Project Overview

This project is a submission for the "Post-Event Analysis" category of the hackathon. The goal is to go beyond the final standings and tell the story of the race, revealing key moments and strategic decisions that led to the outcome.

The centerpiece of this project is the `RaceStory Pro` application, a powerful tool for analyzing and visualizing race data from the GR Cup Series.

## Data

The repository is organized into directories for each race track, containing raw data from the 2024 and 2025 seasons. The data includes:

*   **Race Results**: Official, provisional, and unofficial results.
*   **Lap Times**: Detailed lap time data for each driver.
*   **Pit Stop Data**: Information on pit stops and strategies.
*   **Weather Conditions**: Track and air temperature, humidity, and wind speed.
*   **Telemetry Data**: Vehicle telemetry parameters as described in `Vehicle_Telemetry_Parameters.txt`.

### Race Tracks

*   Barber Motorsports Park
*   Circuit of the Americas (COTA)
*   Road America
*   Sebring International Raceway
*   Sonoma Raceway
*   Virginia International Raceway (VIR)

## RaceStory Pro Application

`RaceStory Pro` is a Streamlit dashboard that provides a comprehensive post-event analysis platform. It transforms raw race data into actionable insights, revealing the hidden narratives that determine race outcomes.

### Key Features

*   **Race Narrative Dashboard**: Visual race progression, key overtaking moments, and pit stop strategy impact analysis.
*   **Strategic Decision Analyzer**: "What if" scenarios, pit stop timing effectiveness, and weather-adjusted pace analysis.
*   **Multi-Circuit Performance Insights**: Driver and team performance trends across different tracks and seasons.
*   **Weather Impact Assessment**: Correlation between weather conditions and lap times.
*   **Driver Performance Report Cards**: Consistency analysis, sector time heatmaps, and head-to-head comparisons.

### Getting Started with RaceStory Pro

To get started with the `RaceStory Pro` application, please refer to the detailed instructions in the `RaceStory_Pro` directory.

1.  **Navigate to the application directory:**
    ```bash
    cd RaceStory_Pro
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit dashboard:**
    ```bash
    streamlit run dashboard/app.py
    ```

For more detailed information, please see the `RaceStory_Pro/README.md` and `RaceStory_Pro/QUICKSTART.md` files.

## Hackathon Context

This project was developed for the Toyota Gazoo Racing Hackathon 2025. The following files provide additional context:

*   `hackathon-requirements.txt`: The hackathon's goals and categories.
*   `judgement-criteria.txt`: The criteria used to evaluate the projects.
*   `notes1.txt`: Notes and known issues about the telemetry and lap data.
*   `Vehicle_Telemetry_Parameters.txt`: A description of the vehicle telemetry parameters.

---

