import torch
import os
import pandas as pd
import pickle
import json
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize

# Initialize BERT
model_name = "bert-base-uncased"
model = BertModel.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)


def embed_sentence(sentence):
    tokens = tokenizer(sentence, return_tensors='pt', padding='max_length', truncation=True, max_length=128)
    with torch.no_grad():
        embedding = model(**tokens).last_hidden_state.mean(dim=1)
    return embedding.numpy()


def extract_sentences_from_dict_list(dict_list):
    # Extract texts, join them, and then split by sentences
    full_text = ' '.join([item["text"] for item in dict_list])
    return sent_tokenize(full_text)

# Load files


pkl_dir = 'mom'
json_dir = 'psych_wolfe/json'

pkl_files = [f for f in os.listdir(pkl_dir) if f.endswith('.pkl')]
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

pkl_embeddings = {}
json_embeddings = {}
results = []

# Loop through files and compute similarity
for pkl_file in pkl_files:
    with open(os.path.join(pkl_dir, pkl_file), 'rb') as f:
        pkl_content = pickle.load(f)
    pkl_sentences = extract_sentences_from_dict_list(pkl_content)
    pkl_embeddings[pkl_file] = [(sentence, embed_sentence(sentence)) for sentence in pkl_sentences]

for json_file in json_files:
    with open(os.path.join(json_dir, json_file), 'r') as f:
        json_content = json.load(f)
    json_sentences = extract_sentences_from_dict_list(json_content)
    json_embeddings[json_file] = [(sentence, embed_sentence(sentence)) for sentence in json_sentences]


# Compute similarity
for pkl_file, pkl_data in pkl_embeddings.items():
    for json_file, json_data in json_embeddings.items():
        for pkl_sentence, pkl_embed in pkl_data:
            max_similarity = 0
            best_match = ""
            for json_sentence, json_embed in json_data:
                similarity = cosine_similarity(pkl_embed.reshape(1, -1), json_embed.reshape(1, -1))[0][0]
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_match = json_sentence

            results.append({
                'PKL File': pkl_file,
                'JSON File': json_file,
                'PKL Sentence': pkl_sentence,
                'Best Matched JSON Sentence': best_match,
                'Similarity': max_similarity
            })
            print(len(results))
# Store results in a DataFrame and save
df = pd.DataFrame(results)
df.to_csv('semantic_results.csv', index=False)
