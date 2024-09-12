import streamlit as st
import pandas as pd
import ast
import plotly.express as px
import base64
import numpy as np
import plotly.graph_objects as go

matches = r"SSCNapoliAnalysis\Sources\matches_napoli_filtered.csv"
performances = r"SSCNapoliAnalysis\Sources\napoli_performances.csv"
passes = r"SSCNapoliAnalysis\Sources\passes_napoli.csv"
shots = r"SSCNapoliAnalysis\Sources\shots_napoli_filtered.csv"
carries = r"SSCNapoliAnalysis\Sources\carries_filtered.csv"
players_stats = r"SSCNapoliAnalysis\Sources\players_stats.csv"
model_path = r"SSCNapoliAnalysis\Sources\matches_napoli_filtered.csv"
image_field_path = r"SSCNapoliAnalysis\Sources\Football-field-football-soccer-field-clipart.png"

st.cache_data.clear()

@st.cache_data
def load_csv(path, nrows=None, first_column_indexes=True):
    if first_column_indexes:
        df = pd.read_csv(path, nrows=nrows, index_col=0)
    else:
        df = pd.read_csv(path, nrows=nrows)
    return df

def get_base64_image(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"

image_base64 = get_base64_image(image_field_path)

st.set_page_config(layout="wide")

st.title('SSC Napoli 2015/2016 Season Analysis')

st.write('This dashboard is a data-driven analysis of SSC Napoli\'s 2015/2016 season. The data used in this analysis is sourced from the StatsBomb open-data repository.')

st.write('The analysis is divided into three sections:')

st.write('1. **Team Performance Analysis**: This section provides an overview of SSC Napoli\'s performance in the 2015/2016 season. It includes metrics such as goals scored, goals conceded, and goal difference.')

st.write('2. **Match Analysis**: This section provides an overview of SSC Napoli\'s performance in individual matches. It includes metrics such as goals scored, goals conceded, and expected goals (xG) for each match.')

st.write('3. **Player Performance Analysis**: This section provides an overview of the top players in SSC Napoli\'s squad based on various performance metrics such as shots made, goals scored, assists, expected goals (xG), expected assist(xA), Dangerous Carries Index(DCI).')

with st.spinner("Loading dataframe.."):

    napoli_performances = load_csv(performances)
    matches_napoli = load_csv(matches).drop(columns=['match_id'])
    passes_napoli = load_csv(passes)
    shots_napoli = load_csv(shots)
    carries_napoli = load_csv(carries)
    players_stats = load_csv(players_stats, first_column_indexes=False)
# Display Key Performance Indicators (KPIs)
st.markdown('# Team Performance Analysis')

st.subheader("Key Performance Indicators (KPIs)")

col1, col2, col3 = st.columns(3)
col1.metric("Total Wins", napoli_performances['total_wins'])
col2.metric("Total Losses", napoli_performances['total_losses'])
col3.metric("Total Draws", napoli_performances['total_draws'])

col4, col5, col6 = st.columns(3)
col4.metric("Goals Made", napoli_performances['goals_made'])
col5.metric("Goals Conceded", napoli_performances['goals_conceded'])
col6.metric("Goal Difference", napoli_performances['goal_difference'])


st.markdown('# Matches Analysis')
# Get the list of available match weeks
# Get the list of available match weeks
match_weeks = matches_napoli['match_week'].unique()

# Dropdown to select match week
selected_week = st.selectbox("Select Match Week", match_weeks)

# Filter matches for the selected match week
filtered_matches = matches_napoli[matches_napoli['match_week'] == selected_week]

# Display information for each match
for i, row in filtered_matches.iterrows():
    # Set the color of the result based on match outcome
    if row['result'] == 'Win':
        result_color = 'green'
    elif row['result'] == 'Lose':
        result_color = 'red'
    else:
        result_color = 'blue'  # Draw

    # Columns for the logos and score at the center
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column sizes (1:2:1 ratio for symmetry)
    
    # Add home team logo
    with col1:
        home_team_image = f"SSCNapoliAnalysis\Sources\Images\SquadLogos\{row['home_team']}.png"  # Replace with actual logo paths or URLs
        st.image(home_team_image, caption=row['home_team'], width=150)

    # Add the score at the center with larger size and dynamic color
    with col2:
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 72px; font-weight: bold; color: {result_color};">
                {row['home_score']} - {row['away_score']}
            </div>
            """,
            unsafe_allow_html=True
        )

    # Add away team logo
    with col3:
        away_team_image = f"SSCNapoliAnalysis\Sources\Images\SquadLogos\{row['away_team']}.png"  # Replace with actual logo paths or URLs
        st.image(away_team_image, caption=row['away_team'], width=150)

    # Centering the match info below the logos and result
    st.markdown(
        f"""
        <div style="text-align: center;">
            <p><strong>Date:</strong> {row['match_date']}, <strong>Kick-off:</strong> {row['kick_off']}</p>
            <p><strong>Stadium:</strong> {row['stadium']}</p>
            <p><strong>Referee:</strong> {row['referee']}</p>
            <p><strong>Home Manager:</strong> {row['home_managers']}, <strong>Away Manager:</strong> {row['away_managers']}</p>
            <p><strong>Result:</strong> {row['result']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )



st.markdown('# Player Performance Analysis')

players = passes_napoli['player'].unique()

# Multiselect widget to filter passes by player
selected_players = st.multiselect("Select Player(s) to filter passes, shots and carries:", options=players, default=players)
# Title
st.title('Interactive Passes Heatmap')

# Extract the pass locations
passes_napoli['location'] = passes_napoli['location'].apply(lambda x: ast.literal_eval(x))  # Convert string to list
passes_napoli['x'] = passes_napoli['location'].apply(lambda loc: loc[0])
passes_napoli['y'] = passes_napoli['location'].apply(lambda loc: loc[1])
passes_napoli['under_pressure'] = passes_napoli['under_pressure'].fillna(False)
passes_napoli['pass_body_part'] = passes_napoli['pass_body_part'].fillna('Not Detected')
passes_napoli['pass_type'] = passes_napoli['pass_type'].fillna('Not Detected')
passes_napoli['pass_goal_assist'] = passes_napoli['pass_goal_assist'].fillna(False)
# Select relevant columns to show on click
info_columns = ['pass_body_part', 'pass_type', 'under_pressure', 'player', 'xA', 'pass_goal_assist']

# Create a string that summarizes the relevant information for each pass
passes_napoli['info'] = passes_napoli[info_columns].apply(lambda row: f"Body Part: {row['pass_body_part']}, "
                                                f"Type: {row['pass_type']}, "
                                                f"Under Pressure: {row['under_pressure']}, "
                                                f"Player: {row['player']}, "
                                                f"xA: {row['xA']}, "
                                                f"Is Assist: {row['pass_goal_assist']}"
                                                , axis=1)

min_xa, max_xa = st.slider(
    'Select xA Range',
    min_value=float(passes_napoli['xA'].min()), max_value=float(passes_napoli['xA'].max()), 
    value=(float(passes_napoli['xA'].min()), float(passes_napoli['xA'].max()))  # Default to full range
)

filtered_df = passes_napoli[passes_napoli['player'].isin(selected_players) &
                            (passes_napoli['xA'] >= min_xa) & (passes_napoli['xA'] <= max_xa)
                            ]

# Create the scatter plot with Plotly
fig = px.scatter(filtered_df, x='x', y='y', hover_name='info', 
                 labels={'x': 'Field Length', 'y': 'Field Width'}, 
                 title="Clickable Passes", 
                 width=800, height=600)

# Customize layout to fit football field dimensions
fig.update_layout(
    images=[dict(
        source=image_base64,  # Football field image URL
        xref="x", yref="y",
        x=0, y=80,  # Coordinates to place the image (adjust for scaling)
        sizex=120, sizey=80,
        sizing="stretch",
        opacity=0.5,
        layer="below"
    )],
    xaxis=dict(range=[0, 120], showgrid=False, zeroline=False),
    yaxis=dict(range=[0, 80], showgrid=False, zeroline=False),
    width=1000, height=750,
    xaxis_title="Field Length (x)",
    yaxis_title="Field Width (y)",
    title="Clickable Passes"
)

filtered_df['xA_log'] = np.log10(filtered_df['xA'] + 1e-5)

fig.update_traces(marker=dict(size=5, color=filtered_df['xA_log'], colorscale='Viridis', colorbar=dict(title="xA (Log-Scaled)")), textposition='top center')

# Display the interactive plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Add a note explaining how to interact with the plot
st.write("Hover on a pass to see detailed information.")

# Extract the shot locations
shots_napoli['location'] = shots_napoli['location'].apply(lambda x: ast.literal_eval(x))  # Convert string to list
shots_napoli['x'] = shots_napoli['location'].apply(lambda loc: loc[0])
shots_napoli['y'] = shots_napoli['location'].apply(lambda loc: loc[1])
shots_napoli['under_pressure'] = shots_napoli['under_pressure'].fillna(False)
shots_napoli['shot_body_part'] = shots_napoli['shot_body_part'].fillna('Not Detected')
shots_napoli['shot_type'] = shots_napoli['shot_type'].fillna('Not Detected')

# Select relevant columns to show on hover
info_columns_shots = ['shot_body_part', 'shot_type', 'under_pressure', 'player', 'xG', 'shot_outcome']

# Create a string that summarizes the relevant information for each shot
shots_napoli['info'] = shots_napoli[info_columns_shots].apply(lambda row: f"Body Part: {row['shot_body_part']}, "
                                                f"Type: {row['shot_type']}, "
                                                f"Under Pressure: {row['under_pressure']}, "
                                                f"Player: {row['player']}, "
                                                f"xG: {row['xG']}, "
                                                f"Outcome: {row['shot_outcome']}"
                                                , axis=1)

# Title
st.title('Interactive Shots Heatmap')

# Slider for xG range
min_xg, max_xg = st.slider(
    'Select xG Range',
    min_value=float(shots_napoli['xG'].min()), max_value=float(shots_napoli['xG'].max()), 
    value=(float(shots_napoli['xG'].min()), float(shots_napoli['xG'].max()))  # Default to full range
)

# Filter the DataFrame by selected players and xG range
filtered_shots_napoli = shots_napoli[shots_napoli['player'].isin(selected_players) &
                             (shots_napoli['xG'] >= min_xg) & (shots_napoli['xG'] <= max_xg)]

# Create the scatter plot with Plotly for shots
fig_shots = px.scatter(filtered_shots_napoli, x='x', y='y', hover_name='info', 
                       labels={'x': 'Field Length', 'y': 'Field Width'}, 
                       title="Clickable Shots", 
                       width=800, height=600)

# Customize layout to fit football field dimensions
fig_shots.update_layout(
    images=[dict(
        source=image_base64,  # Football field image URL
        xref="x", yref="y",
        x=0, y=80,  # Coordinates to place the image (adjust for scaling)
        sizex=120, sizey=80,
        sizing="stretch",
        opacity=0.5,
        layer="below"
    )],
    xaxis=dict(range=[0, 120], showgrid=False, zeroline=False),
    yaxis=dict(range=[0, 80], showgrid=False, zeroline=False),
    width=1000, height=750,
    xaxis_title="Field Length (x)",
    yaxis_title="Field Width (y)",
    title="Clickable Shots"
)

# Update the marker color based on xG
fig_shots.update_traces(marker=dict(size=5, color=filtered_shots_napoli['xG'], colorscale='Viridis', colorbar=dict(title="xG")), textposition='top center')

# Display the interactive plot in Streamlit for shots
st.plotly_chart(fig_shots, use_container_width=True)

# Add a note explaining how to interact with the plot
st.write("Hover on a shot to see detailed information.")

# Select relevant columns to show on hover
info_columns_carries = ['player', 'length', 'progressive_length', 'dangerousness_carries_index']

# Create a string that summarizes the relevant information for each carry
carries_napoli['info'] = carries_napoli[info_columns_carries].apply(lambda row: f"Player: {row['player']}, "
                                                                       f"Length: {row['length']:.2f}, "
                                                                       f"Progressive Length: {row['progressive_length']:.2f}, "
                                                                       f"Dangerousness: {row['dangerousness_carries_index']:.2f}"
                                                                       , axis=1)

# Title
st.title('Interactive Carries Heatmap')

# Slider for carry length
min_length, max_length = st.slider(
    'Select Carry Length Range',
    min_value=float(carries_napoli['length'].min()), max_value=float(carries_napoli['length'].max()), 
    value=(float(carries_napoli['length'].min()), float(carries_napoli['length'].max()))  # Default to full range
)

# Filter the DataFrame by selected players and length range
filtered_carries_napoli = carries_napoli[carries_napoli['player'].isin(selected_players) &
                                 (carries_napoli['length'] >= min_length) & (carries_napoli['length'] <= max_length)]

# Create the scatter plot with Plotly for carries
fig_carries = px.scatter(filtered_carries_napoli, x='x_start', y='y_start', hover_name='info', 
                         labels={'x_start': 'Field Length Start', 'y_start': 'Field Width Start'}, 
                         title="Clickable Carries", 
                         width=800, height=600)

# Customize layout to fit football field dimensions
fig_carries.update_layout(
    images=[dict(
        source=image_base64,  # Football field image URL
        xref="x", yref="y",
        x=0, y=80,  # Coordinates to place the image (adjust for scaling)
        sizex=120, sizey=80,
        sizing="stretch",
        opacity=0.5,
        layer="below"
    )],
    xaxis=dict(range=[0, 120], showgrid=False, zeroline=False),
    yaxis=dict(range=[0, 80], showgrid=False, zeroline=False),
    width=1000, height=750,
    xaxis_title="Field Length (x)",
    yaxis_title="Field Width (y)",
    title="Clickable Carries"
)

# Update the marker color based on dangerousness index
fig_carries.update_traces(marker=dict(size=5, color=filtered_carries_napoli['dangerousness_carries_index'], colorscale='Viridis', colorbar=dict(title="Dangerousness")), textposition='top center')

# Display the interactive plot in Streamlit for carries
st.plotly_chart(fig_carries, use_container_width=True)

# Add a note explaining how to interact with the plot
st.write("Hover on a carry to see detailed information.")

# Title
st.title('Players Comparison Dashboard')

col1, col2 = st.columns(2)

# Select two players for comparison
with col1:
    player_1 = st.selectbox("Select First Player", players_stats['player'], key="player1")

with col2:
    player_2 = st.selectbox("Select Second Player", players_stats['player'], key="player2")

# Filter the player data for comparison
player_1_data = players_stats[players_stats['player'] == player_1].iloc[0]
player_2_data = players_stats[players_stats['player'] == player_2].iloc[0]

# Display player images (Assume you have the images available)
# Replace "player_image_path" with actual .webp image file paths or URLs for each player
player_1_image_path = f"SSCNapoliAnalysis\Sources\Images\PlayerImages\{player_1}.webp"
player_2_image_path = f"SSCNapoliAnalysis\Sources\Images\PlayerImages\{player_2}.webp"

# Columns for displaying player images and the horizontal bar chart in the center
col1, col2, col3 = st.columns([0.5, 2, 0.5])

with col1:
    st.image(player_1_image_path, caption=player_1, width=150)

with col3:
    st.image(player_2_image_path, caption=player_2, width=150)

# Prepare data for comparison (Player 1 vs Player 2)
comparison_data = pd.DataFrame({
    'Stat': ['xA', 'xG', 'DCI', 'Assists (A)', 'Goals (G)', 'Shots', 'Passes to Shot', 'Total Contribution'],
    'Player 1': [player_1_data['xA'], player_1_data['xG'], player_1_data['DCI'], player_1_data['A'], player_1_data['G'], player_1_data['Shots'], player_1_data['Passes_to_Shot'], player_1_data['Total_contribution']],
    'Player 2': [player_2_data['xA'], player_2_data['xG'], player_2_data['DCI'], player_2_data['A'], player_2_data['G'], player_2_data['Shots'], player_2_data['Passes_to_Shot'], player_2_data['Total_contribution']]
})

# Plot the comparison as a horizontal bar chart
fig = px.bar(comparison_data, y='Stat', x=['Player 1', 'Player 2'],
             orientation='h', barmode='group', labels={'value': 'Stat Value', 'Stat': 'Statistic'},
             title=f'Comparison: {player_1} vs {player_2}')

st.plotly_chart(fig)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**{player_1} Offensive Performance Cluster:** {player_1_data['Cluster_Label']}")

with col2:
    st.markdown(f"**{player_2} Offensive Performance Cluster:** {player_2_data['Cluster_Label']}")



