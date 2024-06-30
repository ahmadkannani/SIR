import os
import re
import math
from collections import defaultdict
from .Read import read_doc_file

def load_docs():
    doc_files = [f'{i}.doc' for i in range(1, 13)] + [f'M{i}.doc' for i in range(13)]
    return {doc: read_doc_file(doc) for doc in doc_files}

def tokenize(text):
    return re.findall(r'\w+', text.lower())

def term_frequency(term, doc):
    return doc.split().count(term)

def inverse_doc_frequency(term, all_docs):
    doc_occurrences = sum(1 for doc in all_docs.values() if term in doc)
    return math.log(len(all_docs) / (1 + doc_occurrences))

def build_vector(doc, terms):
    return {term: term_frequency(term, doc) * inverse_doc_frequency(term, {doc}) for term in terms if term_frequency(term, doc) > 0}

def cos_similarity(vec1, vec2):
    common_terms = set(vec1.keys()).intersection(set(vec2.keys()))
    dot_prod = sum(vec1[term] * vec2[term] for term in common_terms)
    magnitude1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    magnitude2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
    return dot_prod / (magnitude1 * magnitude2 + 1e-10)

def rank_docs(query_vec, doc_vecs):
    scored_docs = [(doc, cos_similarity(query_vec, doc_vec)) for doc, doc_vec in doc_vecs.items()]
    return sorted(scored_docs, key=lambda item: item[1], reverse=True)

def search_docs(query):
    docs = load_docs()
    terms = tokenize(query)
    doc_vectors = {doc: build_vector(content, terms) for doc, content in docs.items() if any(term in content for term in terms)}

    if not doc_vectors:
        return "None"

    query_vector = build_vector(" ".join(docs.values()), terms)
    ranked_docs = rank_docs(query_vector, doc_vectors)

    return ", ".join(doc for doc, _ in ranked_docs) if ranked_docs else "None"
