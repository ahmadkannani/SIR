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

def calculate_weight(term, document, documents):
    tf = document.count(term)
    idf = math.log(len(documents) / (sum(term in d for d in documents.values()) + 1e-10))
    return tf * idf


def create_index(documents):
    index = defaultdict(dict)
    for filename, content in documents.items():
        for term in set(preprocess(content)):
            index[term][filename] = calculate_weight(term, content, documents)
    return index

def parse_query(query):
    operators = {'or': 0, 'and': 1, 'not': 2}
    stack = []
    output = []
    for term in query.split():
        if term not in operators:
            output.append(term)
        else:
            while stack and stack[-1] in operators and operators[term] <= operators[stack[-1]]:
                output.append(stack.pop())
            stack.append(term)
    while stack:
        output.append(stack.pop())
    return output


def evaluate_query(expression, index, all_docs):
    stack = []
    for term in expression:
        if term in {'and', 'or', 'not'}:
            if not stack:
                print(f"Error: operator '{term}' without sufficient operands.")
                return
            b = stack.pop()
            if term == 'not':
                stack.append(not_operation(b, all_docs))
            else:
                if not stack:
                    print(f"Error: operator '{term}' without sufficient operands.")
                    return
                a = stack.pop()
                stack.append(boolean_operation(a, b, term))
        else:
            stack.append(index.get(term, {}))
    return sorted(stack[0], key=stack[0].get, reverse=True) if stack else []



def not_operation(docs, all_docs):
    return {doc: weight for doc, weight in all_docs.items() if doc not in docs}


def boolean_operation(docs1, docs2, op):
    if op == 'and':
        return {doc: min(docs1.get(doc, 0), docs2.get(doc, 0)) for doc in set(docs1) & set(docs2)}
    elif op == 'or':
        return {doc: max(docs1.get(doc, 0), docs2.get(doc, 0)) for doc in set(docs1) | set(docs2)}

def show_a( query ):
    documents = read_documents()
    index = create_index(documents)
    all_docs = {doc: 1 for doc in documents}
    while True:
       
        if query.lower() == 'exit':
            break
        expression = parse_query(query)
        result = evaluate_query(expression, index, all_docs)
        result_text = ", ".join(result) if result else "None"
        return result_text.encode("utf-8", "replace").decode("utf-8")
        
       

