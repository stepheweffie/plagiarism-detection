from pandas import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
    return top_74, non_zero_counts


def syntactic_visuals():
    top_74, non_zero_counts = sorted_syntactic(syntactic_csv)

    # Set a default style
    sns.set_style("whitegrid")

    # 1. Bar Plot of Group Counts
    plt.figure(figsize=(10, 6))
    non_zero_counts.plot(kind='bar')
    plt.title("Videos Occur in Top 74 Records")
    plt.ylabel("Count")
    plt.xlabel("Wolfe Video")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # 2. Box Plots for Similarity Scores
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=top_74, x='Wolfe URL Video 2', y='Similarity Score', order=non_zero_counts.index)
    plt.title("Distribution of Similarity Scores by Video")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # 3. Histogram of Similarity Scores
    plt.figure(figsize=(10, 6))
    for group in non_zero_counts.index[:10]:
        group_data = top_74[top_74['Wolfe URL Video 2'] == group]
        # Select only the first 10 records for this group
        first_10 = group_data.head(10)
        # Plot the histogram for this group
        sns.histplot(first_10['Similarity Score'],
                     label=group, kde=False, element="step", common_norm=False, alpha=0.66)

    plt.title("Distribution of Similarity Scores for First 10 of the 15 Videos")
    plt.xlabel("Similarity Score")
    plt.ylabel("Frequency")
    plt.legend()

    # Adjusting the x-axis limits to focus on the region between 0.8 and 1.0
    plt.xlim(0.899, .94)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    syntactic_visuals()

