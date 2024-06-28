
import os
import re
import math
from collections import defaultdict
from .Read import read_doc_file
def read_documents():
    list_files=['1.doc','2.doc','3.doc','4.doc','5.doc','6.doc','7.doc','8.doc','9.doc','M0.doc','M1.doc','M2.doc','M3.doc','M4.doc','M5.doc','M6.doc','M7.doc','M8.doc','M9.doc','M10.doc','M11.doc','M12.doc',]
    documents = {}
    for file in list_files:
             
            documents[file] = read_doc_file(file)
    return documents

def preprocess(text):
    return re.findall(r'\b\w+\b', text.lower())

def calculate_tf(term, document):
    return document.split().count(term)

def calculate_idf(term, documents):
    if isinstance(documents, set):
        document_count = 1 if term in documents else 0
    else:
        document_count = sum(1 for doc in documents.values() if term in doc)
    return math.log(len(documents) / (document_count + 1e-10))

def create_vector(document, query_terms):
    vector = {}
    for term in query_terms:
        tf = calculate_tf(term, document)
        idf = calculate_idf(term, {document})  # Pass a set containing the current document
        vector[term] = tf * idf
    
    # Remove terms with zero vector values
    vector = {term: value for term, value in vector.items() if value != 0}
    
    return vector


def cosine_similarity(vector1, vector2):
    dot_product = sum(vector1.get(term, 0) * vector2.get(term, 0) for term in set(vector1) & set(vector2))
    magnitude1 = math.sqrt(sum(value ** 2 for value in vector1.values()))
    magnitude2 = math.sqrt(sum(value ** 2 for value in vector2.values()))
    return dot_product / (magnitude1 * magnitude2 + 1e-10)

def rank_documents(query_vector, document_vectors):
    rankings = [(doc, cosine_similarity(query_vector, doc_vector)) for doc, doc_vector in document_vectors.items()]
    rankings.sort(key=lambda x: x[1], reverse=True)
    return rankings
def show_b(query):
    all_documents = read_documents()
    query_terms = preprocess(query)
    
    # Create vectors only for documents containing the query terms
    document_vectors = {doc: create_vector(content, query_terms) for doc, content in all_documents.items() if any(term in content for term in query_terms)}
    
    # If no documents contain the query terms, return "None"
    if not document_vectors:
        return "None"
    
    query_vector = create_vector(" ".join(all_documents.values()), query_terms)

    rankings = rank_documents(query_vector, document_vectors)

    result_text = ", ".join(doc for doc, _ in rankings) if rankings else "None"
    return result_text.encode("utf-8", "replace").decode("utf-8")