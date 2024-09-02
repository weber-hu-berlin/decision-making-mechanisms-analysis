import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from common_fields import common_fields  # Importing common_fields from common_fields.py

def preferred_project_votes_calculation(input_file='survey_data.json', output_folder='analytics/scriptResults', showResults=False):
    """
    This function calculates the vote counts for each preferred project from the survey data.

    Parameters:
    input_file (str): The path to the JSON file containing the survey data.
    output_folder (str): The directory where the results will be saved.

    Outputs:
    - A CSV file with the vote counts for each project.
    - An HTML file with a bar chart visualizing the vote counts.
    - An HTML file with a radar chart visualizing the vote distribution.
    """

    # Load the data
    data = pd.read_json(input_file)

    # Count the votes for each preferred project
    preferred_project_votes = data['preferred_project'].value_counts()

    # Map indices to project names using common_fields['projects']
    project_names = common_fields['projects']
    preferred_project_votes.index = [project_names[i - 1] for i in preferred_project_votes.index]

    # Sort the results in descending order
    preferred_project_votes = preferred_project_votes.sort_values(ascending=False)

    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the results to the output folder
    preferred_project_votes.to_csv(os.path.join(output_folder, 'preferred_project_votes.csv'))

    # Convert the Series to a DataFrame for better handling in Plotly
    preferred_project_votes_df = preferred_project_votes.reset_index()
    preferred_project_votes_df.columns = ['Project', 'Votes']  # Rename columns for clarity

    # Plotting Bar Chart with Plotly
    fig_bar = px.bar(preferred_project_votes_df,
                     x='Project',
                     y='Votes',
                     title='Chart 11: Votes by Preferred Project')

    # Save the bar chart as an HTML file
    fig_bar.write_html(os.path.join(output_folder, 'preferred_project_votes_plot.html'))

    # Prepare data for Radar Chart
    radar_chart_data = pd.concat([preferred_project_votes_df, preferred_project_votes_df.iloc[[0]]], ignore_index=True)

    # Plotting Radar Chart with Plotly
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=radar_chart_data['Votes'],
        theta=radar_chart_data['Project'],
        fill='toself',
        name='Project Votes'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        showlegend=False,
        title='Chart 12: Votes by Preferred Project (Radar Chart)'
    )

    # Save the radar chart as an HTML file
    fig_radar.write_html(os.path.join(output_folder, 'preferred_project_votes_radar_plot.html'))

    # Display the plots (Optional for local testing)
    if showResults:
        fig_bar.show()
        fig_radar.show()

# Example usage:
# preferred_project_votes_calculation()