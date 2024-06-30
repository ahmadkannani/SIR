import os
import re
from .Read import read_doc_file

def load_files():
    file_list = ['1.doc', '2.doc', '3.doc', '4.doc', '5.doc', '6.doc', '7.doc', '8.doc', '9.doc', 'M0.doc', 'M1.doc', 'M2.doc', 'M3.doc', 'M4.doc', 'M5.doc', 'M6.doc', 'M7.doc', 'M8.doc', 'M9.doc', 'M10.doc', 'M11.doc', 'M12.doc']
    docs = {}
    for filename in file_list:
        docs[filename] = read_doc_file(filename)
    return docs

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return set(text.split())

def build_inverted_index(docs):
    inverted_index = {}
    for doc_id, content in docs.items():
        words = clean_text(content)
        for word in words:
            if word not in inverted_index:
                inverted_index[word] = []
            inverted_index[word].append(doc_id)
    return inverted_index

def process_query(query):
    query_terms = clean_text(query)
    output_stack = []
    operator_precedence = {"not": 3, "and": 2, "or": 1}
    
    for term in query_terms:
        if term in operator_precedence:
            while output_stack and output_stack[-1] in operator_precedence and operator_precedence[term] <= operator_precedence[output_stack[-1]]:
                yield output_stack.pop()
            output_stack.append(term)
        else:
            yield term
    
    while output_stack:
        yield output_stack.pop()

def execute_query(parsed_query, inverted_index):
    results_stack = []
    for term in parsed_query:
        if term in {"not", "and", "or"}:
            operand_b = results_stack.pop() if results_stack else set()
            operand_a = results_stack.pop() if results_stack else set()
            if term == "not":
                results_stack.append(operand_a - operand_b)
            elif term == "and":
                results_stack.append(operand_a & operand_b)
            elif term == "or":
                results_stack.append(operand_a | operand_b)
        else:
            results_stack.append(set(inverted_index.get(term, [])))
    
    return results_stack.pop() if results_stack else set()

# Load documents
documents = load_files()

# Create inverted index
inverted_index = build_inverted_index(documents)

def search(query):
    parsed_query = process_query(query)
    result_docs = execute_query(parsed_query, inverted_index)
    return ', '.join(result_docs) if result_docs else 'None'
