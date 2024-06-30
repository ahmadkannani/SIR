import os
import re
import math
from collections import defaultdict
from .Read import read_doc_file

def load_documents():
    filenames = [
        '1.doc', '2.doc', '3.doc', '4.doc', '5.doc', '6.doc', '7.doc', '8.doc', 
        '9.doc', 'M0.doc', 'M1.doc', 'M2.doc', 'M3.doc', 'M4.doc', 'M5.doc', 
        'M6.doc', 'M7.doc', 'M8.doc', 'M9.doc', 'M10.doc', 'M11.doc', 'M12.doc'
    ]
    docs = {}
    for filename in filenames:
        docs[filename] = read_doc_file(filename)
    return docs

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def compute_tfidf(term, doc, all_docs):
    term_freq = doc.count(term)
    inv_doc_freq = math.log(len(all_docs) / (sum(term in d for d in all_docs.values()) + 1e-10))
    return term_freq * inv_doc_freq

def build_inverted_index(docs):
    inverted_index = defaultdict(dict)
    for doc_name, content in docs.items():
        terms = set(tokenize(content))
        for term in terms:
            inverted_index[term][doc_name] = compute_tfidf(term, content, docs)
    return inverted_index

def parse_boolean_query(query):
    precedence = {'or': 0, 'and': 1, 'not': 2}
    stack = []
    output = []
    for token in query.split():
        if token not in precedence:
            output.append(token)
        else:
            while stack and stack[-1] in precedence and precedence[token] <= precedence[stack[-1]]:
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())
    return output

def process_query(query_terms, index, all_documents):
    stack = []
    for term in query_terms:
        if term in {'and', 'or', 'not'}:
            if not stack:
                print(f"Error: operator '{term}' without sufficient operands.")
                return
            operand_b = stack.pop()
            if term == 'not':
                stack.append(apply_not(operand_b, all_documents))
            else:
                if not stack:
                    print(f"Error: operator '{term}' without sufficient operands.")
                    return
                operand_a = stack.pop()
                stack.append(apply_boolean(operand_a, operand_b, term))
        else:
            stack.append(index.get(term, {}))
    return sorted(stack[0], key=stack[0].get, reverse=True) if stack else []

def apply_not(docs, all_docs):
    return {doc: weight for doc, weight in all_docs.items() if doc not in docs}

def apply_boolean(docs1, docs2, operator):
    if operator == 'and':
        return {doc: min(docs1.get(doc, 0), docs2.get(doc, 0)) for doc in docs1.keys() & docs2.keys()}
    elif operator == 'or':
        return {doc: max(docs1.get(doc, 0), docs2.get(doc, 0)) for doc in docs1.keys() | docs2.keys()}

def search_documents(query):
    docs = load_documents()
    index = build_inverted_index(docs)
    all_docs = {doc: 1 for doc in docs}
    parsed_query = parse_boolean_query(query)
    result_docs = process_query(parsed_query, index, all_docs)
    result_str = ", ".join(result_docs) if result_docs else "None"
    return result_str.encode("utf-8", "replace").decode("utf-8")
