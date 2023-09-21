from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import json


def load_files_from_directory(directory):
    transcripts = []
    file_paths = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # Load .pkl files
        if filename.endswith('.pkl'):
            with open(filepath, 'rb') as f:
                pkl_data = pickle.load(f)
                concatenated_text = ' '.join([entry['text'] for entry in pkl_data])
                transcripts.append(concatenated_text)

        # Load .json files and concatenate text values
        elif filename.endswith('.json'):
            with open(filepath, 'r') as f:
                json_data = json.load(f)
                concatenated_text = ' '.join([entry['text'] for entry in json_data])
                transcripts.append(concatenated_text)
        file_paths.append(filepath)

    # print(transcripts)
    return transcripts, file_paths


# load_files_from_directory('psych_wolfe/json')


def preprocess_transcript(transcript):
    for s in transcript:
        s.lower()
    return transcript


def compare_transcripts(transcripts1, file_paths1, transcripts2, file_paths2):
    results = []

    vectorizer = TfidfVectorizer()

    # Combine, vectorize, and compute similarity
    all_transcripts = transcripts1 + transcripts2
    tfidf_matrix = vectorizer.fit_transform(all_transcripts)
    similarity_scores = cosine_similarity(tfidf_matrix)

    # Extract transcript-by-transcript similarity scores
    for i in range(len(transcripts1)):
        for j in range(len(transcripts2)):
            results.append({
                "transcript1": transcripts1[i],
                "transcript2": transcripts2[j],
                "file_path1": file_paths1[i],
                "file_path2": file_paths2[j],
                "similarity_score": similarity_scores[i, len(transcripts1) + j]
            })

    return results


# Preprocess transcripts
dir1_transcripts, dir1_paths = load_files_from_directory("mom")
dir2_transcripts, dir2_paths = load_files_from_directory("psych_wolfe/json")

results = compare_transcripts(dir1_transcripts, dir1_paths, dir2_transcripts, dir2_paths)

# Sort results based on similarity scores
sorted_results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)

# Print top N results
N = 10
url_base = "https://www.youtube.com/watch?v="
for i in range(min(N, len(sorted_results))):
    print(f"Transcript from PKL: '{sorted_results[i]['transcript1'][:100]}'...")  # Displaying the first 100 characters for brevity
    print(f"File from PKL: '{sorted_results[i]['file_path1']}'")

    print(f"was most similar to Transcript from JSON: '{sorted_results[i]['transcript2'][200:300]}'...")
    print(f"was most similar to File from JSON: '{sorted_results[i]['file_path2']}'")

    print(f"with a similarity score of: {sorted_results[i]['similarity_score']}\n")

    print(f"Visit the first video at: {url_base + sorted_results[i]['file_path1'].split('/')[-1][:-4]}")
    print(f"Visit the second video at: {url_base + sorted_results[i]['file_path2'].split('/')[-1][:-5]}")
