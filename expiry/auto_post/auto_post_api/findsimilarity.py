from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from functions import dealsmagnet_fetch_deals, desidime_fetch_deals, indiadesire_fetch_deals
import json

def find_unique_entries(deals, threshold):
    """Find unique entries in the deals based on title similarity using cosine similarity."""
    titles = [entry['title'] for entry in deals]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(titles)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    seen_indices = set()
    unique_entries = []
    
    for i in range(len(titles)):
        if i in seen_indices:
            continue

        unique_entries.append(deals[i])
        seen_indices.add(i)
        # print(deals[i]['title'])

        for j in range(i + 1, len(titles)):
            if similarity_matrix[i][j] > threshold:
                seen_indices.add(j)
    
    return unique_entries


def process_deals(all_data):
    """Process the deals and find unique entries and first deal titles."""
    if all_data:
        unique_entries_list = find_unique_entries(all_data, threshold=0.5)
    else:
        unique_entries_list = []
        
    unique_list = json.dumps(unique_entries_list, indent=4)
    # exit()
    
    return unique_list