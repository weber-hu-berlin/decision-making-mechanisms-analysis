from analytics.range_voting import range_voting_calculation
from analytics.borda_count import borda_count_calculation
from analytics.clarke_groves import clark_groves_mechanism_calculation
from analytics.majority_judgment_calculation import majority_judgment_calculation
from analytics.majority_judgment_calculation_adjusted import majority_judgment_calculation as majority_judgment_calculation_adjusted
from analytics.preferred_project import preferred_project_votes_calculation
from analytics.knapsack_voting import knapsack_voting_calculation
from analytics.preference_approval import preference_approval_voting_calculation

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    showResults = False

    borda_count_calculation(showResults=showResults)
    clark_groves_mechanism_calculation(showResults=showResults)
    range_voting_calculation(showResults=showResults)
    majority_judgment_calculation(showResults=showResults)
    majority_judgment_calculation_adjusted(showResults=showResults)
    preferred_project_votes_calculation(showResults=showResults)
    knapsack_voting_calculation(showResults=showResults)
    preference_approval_voting_calculation(showResults=showResults)
