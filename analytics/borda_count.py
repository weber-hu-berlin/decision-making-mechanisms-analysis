import pandas as pd
import os
import plotly.express as px

def borda_count_calculation(input_file='survey_data.json', output_folder='analytics/scriptResults', showResults=False):
    """
    This function performs a Borda Count calculation on survey data.

    Parameters:
    input_file (str): The path to the JSON file containing the survey data.
    output_folder (str): The directory where the results will be saved.

    Outputs:
    - A CSV file with the total Borda points for each project.
    - HTML files with a bar chart, dot plot, heatmap, and box plot visualizing the Borda Count results.
    """

    # Load the data
    data = pd.read_json(input_file)

    # Filter columns that start with 'project_preference_'
    preference_columns = [col for col in data.columns if col.startswith('project_preference_')]

    # Initialize a dictionary to hold the Borda count scores
    borda_scores = {}

    # Maximum points calculation (in Borda, lower rank gets more points)
    max_points = len(preference_columns)

    # Iterate through each row to calculate Borda points
    for _, row in data[preference_columns].iterrows():
        for col in preference_columns:
            project_name = col.replace('project_preference_', '')  # Extract the project name from the column
            rank = int(row[col])  # The rank is the value in the cell

            if project_name not in borda_scores:
                borda_scores[project_name] = 0

            # Calculate the points based on the rank (inversely proportional)
            borda_scores[project_name] += (max_points - rank + 1)

    # Convert the borda_scores dictionary to a DataFrame
    borda_scores_df = pd.DataFrame.from_dict(borda_scores, orient='index', columns=['Total Points']).sort_values(
        by='Total Points', ascending=False)

    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Reset index to ensure the x-axis is labeled correctly
    borda_scores_df = borda_scores_df.reset_index()
    borda_scores_df.columns = ['Project', 'Total Points']  # Rename columns for clarity

    # Save the results to the output folder
    borda_scores_df.to_csv(os.path.join(output_folder, 'borda_count_results.csv'))

    # Plotting with Plotly - Bar Chart
    fig_bar = px.bar(borda_scores_df,
                     x='Project',
                     y='Total Points',
                     labels={'Project': 'Project', 'Total Points': 'Total Points'},
                     title='Chart 1: Borda Count Results')

    # Save the bar chart as an HTML file
    fig_bar.write_html(os.path.join(output_folder, 'borda_count_results_bar_plot.html'))

    # Plotting with Plotly - Dot Plot
    # We need to reshape the data to show ranks across projects
    rank_data = []
    for _, row in data[preference_columns].iterrows():
        for col in preference_columns:
            project_name = col.replace('project_preference_', '')
            rank = int(row[col])
            rank_data.append({'Project': project_name, 'Rank': rank})

    rank_df = pd.DataFrame(rank_data)

    # Adding a small random noise to the Rank to create a jitter effect manually
    rank_df['Jittered Rank'] = rank_df['Rank'] + (pd.Series(rank_df.index).mod(2) * 0.1)

    fig_dot = px.scatter(rank_df,
                         x='Project',
                         y='Jittered Rank',
                         labels={'Project': 'Project', 'Jittered Rank': 'Rank'},
                         title='Chart 2: Distribution of Ranks for Each Project',
                         )

    # Save the dot plot as an HTML file
    fig_dot.write_html(os.path.join(output_folder, 'borda_count_results_dot_plot.html'))

    # Plotting with Plotly - Heatmap
    heatmap_data = rank_df.pivot_table(index='Project', columns='Rank', aggfunc='size', fill_value=0)

    fig_heatmap = px.imshow(
        heatmap_data,
        labels=dict(x="Rank", y="Project", color="Frequency"),
        title='Chart 3: Heatmap of Ranks for Each Project'
    )

    # Save the heatmap as an HTML file
    fig_heatmap.write_html(os.path.join(output_folder, 'borda_count_results_heatmap.html'))

    # Prepare data for the box plot
    # Assign numeric values to sentiment levels
    data['sentiment_category'] = data['opinion_on_tesla_factory_presence'].apply(
        lambda x: 'Positive' if x in ["Sehr positiv.", "Eher positiv.", "Neutral."] else 'Negative')

    # Prepare data for the box plot
    box_plot_data = pd.DataFrame()

    for col in preference_columns:
        project_name = col.replace('project_preference_', '')
        data.loc[:, f'{project_name}_Contribution'] = data[col].apply(lambda rank: max_points - int(rank) + 1)

        # Add the contribution and sentiment category to the box plot data
        project_data = data[[f'{project_name}_Contribution', 'sentiment_category']].copy()
        project_data.columns = ['Contribution', 'Sentiment']
        project_data['Project'] = project_name

        box_plot_data = pd.concat([box_plot_data, project_data], axis=0)

    # Create the box plot
    fig_box = px.box(box_plot_data,
                     x='Project',
                     y='Contribution',
                     color='Sentiment',
                     labels={'Contribution': 'Contribution', 'Project': 'Project'},
                     title='Chart 17: Contribution Comparison by Sentiment for Each Project'
                     )

    # Save the box plot as an HTML file
    fig_box.write_html(os.path.join(output_folder, 'borda_count_results_box_plot.html'))

    # Display the plots (Optional for local testing)
    if showResults:
        fig_bar.show()
        fig_dot.show()
        fig_heatmap.show()
        fig_box.show()

# Example usage:
# borda_count_calculation()