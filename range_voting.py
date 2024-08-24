import pandas as pd
import os
import plotly.express as px

def range_voting_calculation(input_file='survey_data.json', output_folder='analytics/scriptResults', showResults=False):
    """
    This function performs a Range Voting calculation on survey data.

    Parameters:
    input_file (str): The path to the JSON file containing the survey data.
    output_folder (str): The directory where the results will be saved.

    Outputs:
    - A CSV file with the total scores for each project.
    - HTML files with a bar chart and box plot visualizing the range voting results.
    """

    # Load the data
    data = pd.read_json(input_file)

    # Filter columns that start with 'opinion_' and end with '_rating'
    rating_columns = [col for col in data.columns if col.startswith('opinion_') and col.endswith('_rating')]

    # Initialize a dictionary to hold the total scores for each project
    total_scores = {}

    # Calculate the total score for each project
    for col in rating_columns:
        project_name = col.replace('opinion_', '').replace('_rating', '')  # Extract the project name
        total_scores[project_name] = data[col].sum()  # Sum the ratings for each project

    # Convert the total_scores dictionary to a DataFrame
    total_scores_df = pd.DataFrame.from_dict(total_scores, orient='index', columns=['Total Score']).sort_values(
        by='Total Score', ascending=False)

    # Reset index to ensure the x-axis is labeled correctly
    total_scores_df = total_scores_df.reset_index()
    total_scores_df.columns = ['Project', 'Total Score']  # Rename columns for clarity

    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the results to the output folder
    total_scores_df.to_csv(os.path.join(output_folder, 'range_voting_results.csv'))

    # Plotting with Plotly - Bar Chart
    fig_bar = px.bar(total_scores_df,
                     x='Project',
                     y='Total Score',
                     labels={'Project': 'Project', 'Total Score': 'Total Score'},
                     title='Chart 15: Range Voting Results: Total Score per Project')

    # Save the bar chart as an HTML file
    fig_bar.write_html(os.path.join(output_folder, 'range_voting_results_plot.html'))

    # Plotting with Plotly - Box Plot
    # Reshape the data for the box plot
    reshaped_data = pd.melt(data[rating_columns], var_name='Project', value_name='Score')
    reshaped_data['Project'] = reshaped_data['Project'].str.replace('opinion_', '').str.replace('_rating', '')

    fig_box = px.box(reshaped_data,
                     x='Project',
                     y='Score',
                     labels={'Project': 'Project', 'Score': 'Score'},
                     title='Chart 16: Range Voting Results: Score Distribution per Project')

    # Save the box plot as an HTML file
    fig_box.write_html(os.path.join(output_folder, 'range_voting_results_box_plot.html'))

    # Display the plots (Optional for local testing)
    if showResults:
        fig_bar.show()
        fig_box.show()

# Example usage:
# range_voting_calculation()