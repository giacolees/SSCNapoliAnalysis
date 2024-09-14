# SSC Napoli 2015/2016 Serie A Season Analysis

This repository contains two data analysis projects focused on SSC Napoli’s 2015/2016 Serie A season. The projects cover data processing, cleaning, and visualization through an interactive dashboard, allowing users to explore match and player performance data in-depth.

## Projects Overview

1. **First Project: Soccer Data Processing**
   - **Goal**: To clean and structure the raw dataset for efficient use in data visualization. This involves handling and preprocessing match data, player statistics, and event records like passes and shots from the season.
   - **Outcome**: Cleaned and transformed datasets stored as CSV files, ready for use in the second project.

2. **Second Project: Interactive Dashboard**
   - **Goal**: To build an interactive web-based dashboard using Python’s Streamlit framework, where users can dynamically explore the processed datasets. The dashboard provides real-time visualizations for team and player performances.
   - **Outcome**: An interactive dashboard for detailed analysis of Napoli’s 2015/2016 Serie A season, with filtering options and data visualization through charts, tables, and heatmaps.

---

## First Project: Soccer Data Processing

### Objective
The objective of this project is to take raw data from Napoli’s 2015/2016 season and prepare it for further analysis. This is achieved through data cleaning, transformation, and feature engineering.

### Data Sources
The dataset used in this project is sourced from StatsBomb's open-data repository. It includes:
- **Match Data**: Scores, teams involved, and match outcomes.
- **Player Data**: Statistics like goals, assists, shots, and passes.
- **Event Data**: Detailed records of passes, shots, and carries with spatial coordinates.

### Processing Steps
1. **Data Cleaning**: Remove or transform null values and inconsistent data types.
2. **Data Transformation**: Convert spatial coordinates for meaningful visualizations (e.g., heatmaps).
3. **Feature Engineering**: Create new metrics like expected goals (xG) and expected assists (xA).
4. **Data Filtering**: Focus only on relevant match events, such as passes or shots from Napoli’s games.
5. **Saving Data**: Save cleaned data as CSV files for use in the dashboard.

---

## Second Project: Interactive Dashboard

### Objective
This project focuses on developing a web-based dashboard for data visualization. The dashboard allows users to interactively explore SSC Napoli’s 2015/2016 season using the cleaned datasets from the first project.

### Technologies Used
- **Python**: Core logic for data handling and dashboard generation.
- **Streamlit**: For building the web-based interactive dashboard.
- **Plotly**: For generating interactive charts and visualizations.
- **Pandas**: For data manipulation and filtering.

### Features
- **Dynamic Filtering**: Filter data in real-time using dropdowns, sliders, checkboxes, etc.
- **Real-time Visualizations**: Line charts, bar charts, scatter plots, and heatmaps update dynamically based on user input.
- **Data Table Integration**: Users can sort, search, and download filtered data.
- **Responsive Design**: The dashboard adjusts to different screen sizes, ensuring it works well on desktops, tablets, and smartphones.

---

## How to Run the Projects

### First Project: Soccer Data Processing
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the data processing script to clean and prepare the dataset:
   ```bash
   jupyter notebook SoccerDataAnalysis.ipynb
   ```
5. The cleaned datasets will be saved as CSV files in the `Sources` folder.

### Second Project: Interactive Dashboard
1. After completing the first project.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the dashboard using Streamlit:
   ```bash
   streamlit run InteractiveDashboard.py
   ```
4. The dashboard will be available locally at `http://localhost:8501`. Open this link in your browser to explore the interactive visualizations.

---
