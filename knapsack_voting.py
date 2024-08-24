import pandas as pd
import os
import plotly.graph_objects as go

def knapsack_voting_calculation(input_file='survey_data.json', output_folder='analytics/scriptResults', showResults=False):
    """
    This function performs a Knapsack-Voting calculation and overlays the Clark-Groves Mechanism contributions
    as a line chart on a secondary y-axis.

    Parameters:
    input_file (str): The path to the JSON file containing the survey data.
    output_folder (str): The directory where the results will be saved.

    Outputs:
    - A CSV file with the total votes each project received.
    - A CSV file with the total support each project received from the Clark-Groves Mechanism.
    - An HTML file with a bar chart and line chart visualizing the results.
    """

    # Load the data
    data = pd.read_json(input_file)

    # Filter columns that start with 'votes_for_'
    vote_columns = [col for col in data.columns if col.startswith('votes_for_')]

    # Initialize a dictionary to hold the total votes for each project
    total_votes = {}

    # Calculate the total votes for each project
    for col in vote_columns:
        project_name = col.replace('votes_for_', '')  # Extract the project name from the column name
        total_votes[project_name] = data[col].apply(lambda x: str(x).count('Stimme')).sum()

    # Convert the total_votes dictionary to a DataFrame
    total_votes_df = pd.DataFrame.from_dict(total_votes, orient='index', columns=['Total Votes']).sort_values(
        by='Total Votes', ascending=False)

    # Reset index to ensure the x-axis is labeled correctly
    total_votes_df = total_votes_df.reset_index()
    total_votes_df.columns = ['Project', 'Total Votes']  # Rename columns for clarity

    # Filter columns that end with '_support' for Clark-Groves Mechanism
    support_columns = [col for col in data.columns if col.endswith('_support')]

    # Initialize a dictionary to hold the total support for each project (Clark-Groves Mechanism)
    total_support = {}

    # Calculate the total support for each project
    for col in support_columns:
        project_name = col.replace('_support', '')  # Extract the project name from the column
        total_support[project_name] = data[col].sum()  # Sum the support values for each project

    # Convert the total_support dictionary to a DataFrame
    total_support_df = pd.DataFrame.from_dict(total_support, orient='index', columns=['Total Support (€)'])

    # Align the project order to match that of the total_votes_df
    total_support_df = total_support_df.loc[total_votes_df['Project']].reset_index(drop=True)
    total_support_df['Project'] = total_votes_df['Project']

    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the results to the output folder
    total_votes_df.to_csv(os.path.join(output_folder, 'knapsack_voting_results.csv'))
    total_support_df.to_csv(os.path.join(output_folder, 'clark_groves_mechanism_results.csv'))

    # Plotting with Plotly (Bar for Knapsack Voting, Line for Clark-Groves)
    fig = go.Figure()

    # Add bar chart for Knapsack Voting results
    fig.add_trace(go.Bar(
        x=total_votes_df['Project'],
        y=total_votes_df['Total Votes'],
        name='Knapsack Voting: Total Votes',
        marker_color='blue',
        yaxis='y1'
    ))

    # Add line chart for Clark-Groves Mechanism results
    fig.add_trace(go.Scatter(
        x=total_support_df['Project'],
        y=total_support_df['Total Support (€)'],
        mode='lines+markers',
        name='Clark-Groves Mechanism: Total Support (€)',
        line=dict(color='red', width=2),
        yaxis='y2'
    ))

    # Update layout with secondary y-axis
    fig.update_layout(
        title='Chart 7: Knapsack Voting Results with Clark-Groves Mechanism Overlay',
        xaxis=dict(title='Project'),
        yaxis=dict(
            title='Total Votes',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue'),
            side='left'
        ),
        yaxis2=dict(
            title='Total Support (€)',
            titlefont=dict(color='red'),
            tickfont=dict(color='red'),
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.02, y=0.98),
        margin=dict(l=40, r=40, t=80, b=40)
    )

    # Save the combined plot as an HTML file
    fig.write_html(os.path.join(output_folder, 'knapsack_voting_and_clark_groves_results_plot.html'))

    # Display the plot (Optional for local testing)
    if showResults:
        fig.show()

# Example usage:
# knapsack_voting_calculation()