import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go


def majority_judgment_calculation(input_file='survey_data.json', output_folder='analytics/scriptResults', showResults=False):
    """
    This function performs a Majority Judgment calculation on survey data and visualizes the results
    using both a Diverging Bar Chart and a Box Plot.

    Parameters:
    input_file (str): The path to the JSON file containing the survey data.
    output_folder (str): The directory where the results will be saved.

    Outputs:
    - A CSV file with the count of each rating category for each project.
    - An HTML file with a Diverging Bar Chart visualizing the ratings distribution.
    - An HTML file with a Box Plot visualizing the ratings spread for each project.
    """

    # Load the data
    data = pd.read_json(input_file)

    # Filter columns that start with 'project_rating_'
    rating_columns = [col for col in data.columns if col.startswith('project_rating_')]

    # Initialize a DataFrame to hold the rating counts for each project
    rating_counts = pd.DataFrame()

    # Define the expected rating categories
    expected_ratings = ['Inakzeptabel.', 'Akzeptabel.', 'Exzellent.']

    # Calculate the count of each rating for each project
    for col in rating_columns:
        project_name = col.replace('project_rating_', '')  # Extract the project name
        counts = data[col].value_counts(dropna=True)  # Count the occurrences of each rating, ignoring nulls
        # Filter out any unexpected rating values
        counts = counts[counts.index.isin(expected_ratings)]
        # Ensure all expected ratings are present
        for rating in expected_ratings:
            if rating not in counts:
                counts[rating] = 0
        rating_counts[project_name] = counts

    # Transpose the DataFrame for easier plotting
    rating_counts = rating_counts.T

    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the results to the output folder
    rating_counts.to_csv(os.path.join(output_folder, 'majority_judgment_results.csv'))

    # Prepare data for Diverging Bar Chart
    rating_counts = rating_counts.fillna(0)  # Fill any remaining NaNs with 0
    rating_counts['Positive'] = rating_counts['Exzellent.'] + rating_counts['Akzeptabel.']
    rating_counts['Negative'] = -rating_counts['Inakzeptabel.']  # Negative values for diverging bars

    # Create a DataFrame suitable for Plotly (Diverging Bar Chart)
    diverging_data = pd.DataFrame({
        'Project': rating_counts.index,
        'Positive': rating_counts['Positive'],
        'Negative': rating_counts['Negative']
    }).melt(id_vars='Project', value_vars=['Positive', 'Negative'], var_name='Rating', value_name='Count')

    # Plotting Diverging Bar Chart with Plotly
    fig1 = px.bar(diverging_data,
                  x='Count',
                  y='Project',
                  color='Rating',
                  orientation='h',
                  labels={'Count': 'Number of Ratings', 'Project': 'Project'},
                  title='Chart 8: Majority Judgment Results: Diverging Bar Chart of Ratings',
                  color_discrete_map={'Positive': 'green', 'Negative': 'red'})

    # Save the Diverging Bar Chart as an HTML file
    fig1.write_html(os.path.join(output_folder, 'majority_judgment_diverging_bar_chart.html'))

    # Display the plots (Optional for local testing)
    if showResults:
        fig1.show()

# Example usage:
# majority_judgment_calculation()