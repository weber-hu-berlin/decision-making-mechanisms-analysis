import pandas as pd
import os
import plotly.express as px

def majority_judgment_calculation(input_file='survey_data.json', output_folder='analytics/scriptResults', showResults=False):
    """
    This function performs a Majority Judgment calculation on survey data.

    Parameters:
    input_file (str): The path to the JSON file containing the survey data.
    output_folder (str): The directory where the results will be saved.

    Outputs:
    - A CSV file with the median rating for each project.
    - An HTML file with a bar chart visualizing the median ratings.
    """

    # Load the data
    data = pd.read_json(input_file)

    # Filter columns that start with 'project_rating_'
    rating_columns = [col for col in data.columns if col.startswith('project_rating_')]

    # Initialize a dictionary to hold the median rating for each project
    median_ratings = {}

    # Calculate the median rating for each project
    for col in rating_columns:
        project_name = col.replace('project_rating_', '')  # Extract the project name
        median_ratings[project_name] = data[col].mode()[0]  # Calculate the mode (most frequent rating)

    # Convert the median_ratings dictionary to a DataFrame
    median_ratings_df = pd.DataFrame.from_dict(median_ratings, orient='index', columns=['Median Rating']).sort_values(
        by='Median Rating', ascending=False)

    # Reset index to ensure the x-axis is labeled correctly
    median_ratings_df = median_ratings_df.reset_index()
    median_ratings_df.columns = ['Project', 'Median Rating']  # Rename columns for clarity

    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the results to the output folder
    median_ratings_df.to_csv(os.path.join(output_folder, 'majority_judgment_results.csv'))

    # Plotting with Plotly
    fig = px.bar(median_ratings_df,
                 x='Project',
                 y='Median Rating',
                 labels={'Project': 'Project', 'Median Rating': 'Median Rating'},
                 title='Chart 8: Majority Judgment Results: Median Rating per Project')

    # Save the plot as an HTML file
    fig.write_html(os.path.join(output_folder, 'majority_judgment_results_plot.html'))

    # Display the plot (Optional for local testing)
    if showResults:
        fig.show()

# Example usage:
# majority_judgment_calculation()