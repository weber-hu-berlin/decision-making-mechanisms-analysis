import pandas as pd
import os
import plotly.express as px

def preference_approval_voting_calculation(input_file='survey_data.json', output_folder='analytics/scriptResults', showResults=False):
    """
    This function performs a Preference Approval Voting calculation on survey data using project ratings.

    Parameters:
    input_file (str): The path to the JSON file containing the survey data.
    output_folder (str): The directory where the results will be saved.

    Outputs:
    - A CSV file with the approval scores for each project.
    - HTML files with a bar chart and stacked bar chart visualizing the approval scores.
    """

    # Load the data
    data = pd.read_json(input_file)

    # Filter columns for preferences and ratings
    preference_columns = [col for col in data.columns if col.startswith('project_preference_')]
    rating_columns = [col for col in data.columns if col.startswith('project_rating_')]

    # Initialize a dictionary to hold the approval scores for each project
    approval_scores = {}
    approval_breakdown = []
    average_ranks = {}

    # Translate ratings to approvals
    rating_to_approval = {
        "Exzellent.": "Yes",
        "Akzeptabel.": "Yes",
        "Inakzeptabel.": "No"
    }

    # Calculate the approval score and average rank for each project
    for pref_col in preference_columns:
        project_name = pref_col.replace('project_preference_', '')  # Extract project name from the preference column
        rating_col = f'project_rating_{project_name}'  # Corresponding rating column

        if rating_col in rating_columns:
            # Map ratings to approvals
            approvals = data[rating_col].map(rating_to_approval)

            # Count approvals only where approval is 'Yes'
            valid_approvals = data.loc[approvals == 'Yes', pref_col].value_counts()

            total_ranks = 0
            total_approvals = 0

            for rank, count in valid_approvals.items():
                points = len(preference_columns) - int(rank) + 1  # Higher rank (closer to 1) gets more points
                if project_name not in approval_scores:
                    approval_scores[project_name] = 0
                approval_scores[project_name] += points * count

                # Calculate total rank and count for average rank calculation
                total_ranks += int(rank) * count
                total_approvals += count

                approval_breakdown.append({'Project': project_name, 'Rank': rank, 'Count': count})

            # Calculate the average rank for the project
            if total_approvals > 0:
                average_ranks[project_name] = total_ranks / total_approvals
            else:
                average_ranks[project_name] = None

    # Convert the approval_scores dictionary to a DataFrame
    approval_scores_df = pd.DataFrame.from_dict(approval_scores, orient='index',
                                                columns=['Approval Score']).sort_values(by='Approval Score',
                                                                                        ascending=False)

    # Add average ranks to the DataFrame
    approval_scores_df['Average Rank'] = approval_scores_df.index.map(average_ranks)

    # Reset index to ensure the x-axis is labeled correctly
    approval_scores_df = approval_scores_df.reset_index()
    approval_scores_df.columns = ['Project', 'Approval Score', 'Average Rank']  # Rename columns for clarity

    # Convert approval breakdown to a DataFrame for the stacked bar chart
    approval_breakdown_df = pd.DataFrame(approval_breakdown)

    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the results to the output folder
    approval_scores_df.to_csv(os.path.join(output_folder, 'preference_approval_voting_results.csv'))

    # Plotting with Plotly - Bar Chart
    fig_bar = px.bar(approval_scores_df,
                     x='Project',
                     y='Approval Score',
                     labels={'Project': 'Project', 'Approval Score': 'Approval Score'},
                     title='Chart 9: Preference Approval Voting Results: Approval Score per Project')

    # Save the bar chart as an HTML file
    fig_bar.write_html(os.path.join(output_folder, 'preference_approval_voting_results_plot.html'))

    # Plotting with Plotly - Stacked Bar Chart with Average Rank Annotations
    fig_stacked_bar = px.bar(approval_breakdown_df,
                             x='Project',
                             y='Count',
                             color='Rank',
                             labels={'Project': 'Project', 'Count': 'Number of Approvals', 'Rank': 'Preference Rank'},
                             title='Chart 10: Preference Approval Voting Results: Approval Breakdown by Rank')

    fig_stacked_bar.update_layout(barmode='stack')

    # Add average rank annotations above each bar
    for project in approval_scores_df['Project']:
        avg_rank = approval_scores_df.loc[approval_scores_df['Project'] == project, 'Average Rank'].values[0]
        total_count = approval_breakdown_df[approval_breakdown_df['Project'] == project]['Count'].sum()
        fig_stacked_bar.add_annotation(x=project, y=total_count, text=f'Avg Rank: {avg_rank:.2f}',
                                       showarrow=False, yshift=10, xanchor='center')

    # Save the stacked bar chart as an HTML file
    fig_stacked_bar.write_html(os.path.join(output_folder, 'preference_approval_voting_results_stacked_bar_plot.html'))

    # Display the plots (Optional for local testing)
    if showResults:
        fig_bar.show()
        fig_stacked_bar.show()

# Example usage:
# preference_approval_voting_calculation()