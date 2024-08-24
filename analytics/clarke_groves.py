import pandas as pd
import os
import plotly.express as px

def clark_groves_mechanism_calculation(input_file='survey_data.json', output_folder='analytics/scriptResults', showResults=False):
    """
    This function performs a Clark-Groves Mechanism calculation on survey data.

    Parameters:
    input_file (str): The path to the JSON file containing the survey data.
    output_folder (str): The directory where the results will be saved.

    Outputs:
    - A CSV file with the total support for each project.
    - An HTML file with a bar chart visualizing the total support results.
    - An HTML file with a box plot visualizing the distribution of support for each project.
    - An HTML file with a bubble chart visualizing the relationship between average income, points from opinion columns, and average support.
    - A CSV file containing all the data used for the bubble chart.
    """

    # Load the data
    data = pd.read_json(input_file)

    # Filter columns that end with '_support'
    support_columns = [col for col in data.columns if col.endswith('_support')]

    # Initialize a dictionary to hold the total support for each project
    total_support = {}

    # Calculate the total support for each project
    for col in support_columns:
        project_name = col.replace('_support', '')  # Extract the project name from the column
        total_support[project_name] = data[col].sum()  # Sum the support values for each project

    # Convert the total_support dictionary to a DataFrame
    total_support_df = pd.DataFrame.from_dict(total_support, orient='index', columns=['Total Support (€)']).sort_values(
        by='Total Support (€)', ascending=False)

    # Reset index to ensure the x-axis is labeled correctly
    total_support_df = total_support_df.reset_index()
    total_support_df.columns = ['Project', 'Total Support (€)']  # Rename columns for clarity

    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the results to the output folder
    total_support_df.to_csv(os.path.join(output_folder, 'clark_groves_mechanism_results.csv'), index=False)

    # Plotting Bar Chart with Plotly
    fig_bar = px.bar(total_support_df,
                     x='Project',
                     y='Total Support (€)',
                     labels={'Project': 'Project', 'Total Support (€)': 'Total Support (€)'},
                     title='Chart 4: Clark-Groves Mechanism: Total Support per Project')

    # Save the bar chart as an HTML file
    fig_bar.write_html(os.path.join(output_folder, 'clark_groves_mechanism_results_plot.html'))

    # Prepare data for Box Plot
    box_plot_data = pd.melt(data[support_columns], var_name='Project', value_name='Support (€)')
    box_plot_data['Project'] = box_plot_data['Project'].str.replace('_support', '')

    # Plotting Box Plot with Plotly
    fig_box = px.box(box_plot_data,
                     x='Project',
                     y='Support (€)',
                     labels={'Project': 'Project', 'Support (€)': 'Support (€)'},
                     title='Chart 5: Clark-Groves Mechanism: Distribution of Support per Project')

    # Save the box plot as an HTML file
    fig_box.write_html(os.path.join(output_folder, 'clark_groves_mechanism_box_plot.html'))

    # Calculate average income, points from opinion columns, and average support
    income_column = 'annual_income'  # Assuming this is the column for income
    opinion_columns = [col for col in data.columns if col.startswith('opinion_') and col.endswith('_rating')]

    # Convert income to numeric, assuming it's in a recognizable format
    income_mapping = {
        "• < 20.000 €": 10000,
        "• 20.000 - 39.999 €": 30000,
        "• 40.000 - 59.999 €": 50000,
        "• 60.000 - 79.999 €": 70000,
        "• 80.000 - 99.999 €": 90000,
        "• 100.000 € oder mehr": 110000,
        "• Bevorzuge keine Angabe": None
    }
    data['income_numeric'] = data[income_column].map(income_mapping)

    bubble_data = []

    for col in support_columns:
        project_name = col.replace('_support', '')
        rating_col = f'project_rating_{project_name}'
        supporting_data = data[data[rating_col] != 'Inakzeptabel.']  # Filter supporters
        avg_income = supporting_data['income_numeric'].mean()  # Calculate average income of supporters
        opinion_col = f'opinion_{project_name}_rating'
        if opinion_col in data.columns:
            total_opinion_points = data[opinion_col].sum()  # Total points from the relevant opinion column
        else:
            total_opinion_points = 0
        avg_support = data[col].mean()

        bubble_data.append({
            'Project': project_name,
            'Avg Income (€)': avg_income,
            'Total Opinion Points': total_opinion_points,
            'Avg Support (€)': avg_support,
            'Bubble Size': abs(avg_support)  # Use absolute value for bubble size
        })

    bubble_data_df = pd.DataFrame(bubble_data)

    # Save the bubble data to a CSV file
    bubble_data_df.to_csv(os.path.join(output_folder, 'clark_groves_mechanism_bubble_data.csv'), index=False)

    # Plotting Bubble Chart with Plotly
    fig_bubble = px.scatter(bubble_data_df,
                            x='Avg Income (€)',
                            y='Total Opinion Points',
                            size='Bubble Size',
                            color='Project',
                            hover_name='Project',
                            hover_data={'Avg Support (€)': True, 'Bubble Size': False},  # Display actual Avg Support in hover
                            size_max=60,
                            labels={'Avg Income (€)': 'Average Income (€)', 'Total Opinion Points': 'Total Opinion Points'},
                            title='Chart 6: Clark-Groves Mechanism: Bubble Chart of Average Income vs. Opinion Points')

    # Save the bubble chart as an HTML file
    fig_bubble.write_html(os.path.join(output_folder, 'clark_groves_mechanism_bubble_chart.html'))

    # Display the plots (Optional for local testing)
    if showResults:
        fig_bar.show()
        fig_box.show()
        fig_bubble.show()

# Example usage:
# clark_groves_mechanism_calculation()