import re
from nltk.stem import PorterStemmer
from collections import defaultdict
stemmer = PorterStemmer()
# Preprocessing  the query
def preprocess(query):
    query = re.sub(r'[^a-zA-Z\s]', '', query).lower()
    terms = query.split()
    terms = [stemmer.stem(term) for term in terms]
    return terms

def tokenize(text):
    tokens = preprocess(text)
    index = defaultdict(list)
    for position, term in enumerate(tokens):
        index[term].append(position)
    obj = {
            "terms": [{"term": term, "positions": positions} for term, positions in index.items()]
        }
    return obj




def get_positions(docs, query):
    data = []
    query_terms = preprocess(query)
    for document in docs:
        document_terms = [term['term'] for term in document['terms']]
        # print("Document terms:", document_terms)
        
        if all(term in document_terms for term in query_terms):
            # print("Match found in document:", document['filename'])
            
            first_query_term = query_terms[0]
            first_term_positions = [term['positions'] for term in document['terms'] if term['term'] == first_query_term][0]
            
            start_positions = []
            for start_pos in first_term_positions:
                position_matched = True
                for i in range(1, len(query_terms)):
                    term_positions = [term['positions'] for term in document['terms'] if term['term'] == query_terms[i]][0]
                    if start_pos + i not in term_positions:
                        position_matched = False
                        break
                if position_matched:
                    start_positions.append(start_pos)
            
            if start_positions:

                doc = {
                    "file_name": document['filename'],
                    "start_positions": start_positions,
                    "type": document['type'],
                    "total_occurances": len(start_positions),
                    "id" : document['id']
                    # "org_document": Documents.objects.get(id = document['id'])
                }
                data.append(doc)
                print("Match found in document:", document['filename'])
                print("Start positions:", start_positions)
            else:
                print("No consecutive matches found.")
        else:
            print("No match found in document:", document['filename'])
    return data