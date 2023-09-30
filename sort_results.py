from pandas import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
syntactic_csv = 'syntactic_results.csv'


def sorted_syntactic(csv_file):
    # Load csv
    data = pd.read_csv(csv_file)
    # Compute the size of each group defined by 'Wolfe URL Video 2'
    data = data.drop_duplicates(subset=['Peterson URL Video 1', 'Wolfe URL Video 2'])
    # Compute the minimum rank for each 'Wolfe URL Video 2' group
    group_ranks = data.groupby('Wolfe URL Video 2')['Rank'].min()
    # Sort the groups by ranks
    sorted_groups = group_ranks.sort_values().index
    # Use the categorical data type to enforce an order on 'Wolfe URL Video 2' based on sorted_groups
    data['Wolfe URL Video 2'] = pd.Categorical(data['Wolfe URL Video 2'], categories=sorted_groups, ordered=True)
    # Sorting the dataframe solely based on the 'Similarity Score' column in descending order
    df_sorted_by_score = data.sort_values(by='Similarity Score', ascending=False)
    # Taking the top 74 rows based on the highest similarity scores
    top_74 = df_sorted_by_score.head(74)
    # top_74.to_csv('syntactic_results_top_74.csv', index=False)
    group_74 = top_74['Wolfe URL Video 2'].value_counts()
    non_zero_counts = group_74[group_74 > 0]
    print('These are the Wolfe video(s) results contained in the top 10% of TF-IDF cosine similarity scores')
    print(top_74, non_zero_counts)
    # Iterate through the unique 'Wolfe URL Video 2' values corresponding to the non-zero counts
    for group in non_zero_counts.index:
        group_data = top_74[top_74['Wolfe URL Video 2'] == group]
        print(f"\nTop 10% Statistics For Video: {group}\n{'-' * 40}")
        print(group_data.describe())

    # top_74['Re-Rank'] = top_74['Rank'].rank(method='min')
    return group_74


sorted_syntactic(syntactic_csv)


