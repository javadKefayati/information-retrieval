import glob


def create_inverted_index(files):
    inverted_index = {}
    for i, file in enumerate(files):
        with open(file, 'r') as f:
            contents = f.read()
            words = contents.split()
            for word in set(words):
                if word not in inverted_index:
                    inverted_index[word] = []
                inverted_index[word].append(i + 1)
    for word in inverted_index:
        inverted_index[word].sort()
    return inverted_index


files = glob.glob('./docs/*.txt')
inverted_index = create_inverted_index(files)
# print(inverted_index)


def search_query(inverted_index, query):
    query_tokens = query.split()
    result_docs = set(range(1, len(files) + 1))
    
    # Loop through each token in the query
    for i in range(len(query_tokens)):
        token = query_tokens[i]
        
        # If the token is "and"
        if token == "and":
            # Get the intersection of the current result document set and the next token's document set
            next_token = query_tokens[i+1]
            if next_token not in inverted_index:
                return []
            next_docs = set(inverted_index[next_token])
            result_docs = result_docs.intersection(next_docs)
            
        # If the token is "or"
        elif token == "or":
            # Get the union of the current result document set and the next token's document set
            next_token = query_tokens[i+1]
            if next_token not in inverted_index:
                continue
            next_docs = set(inverted_index[next_token])
            print(result_docs)
            result_docs = result_docs.union(next_docs)
            print(result_docs)
            
        # If the token is "not"
        elif token == "not":
            # Remove the documents from the current result document set that are also in the next token's document set
            next_token = query_tokens[i+1]
            if next_token not in inverted_index:
                continue
            next_docs = set(inverted_index[next_token])
            result_docs = result_docs.difference(next_docs)
            
        # If the token is not an operator, it must be a search term
        else:
            # Get the document set for the current token and update the result document set accordingly
            if i - 1 >= 0 and (query_tokens[i - 1] == 'not' or query_tokens[i - 1] == 'or'):
                continue
            if token not in inverted_index:
                return []
            docs = set(inverted_index[token])
            result_docs = result_docs.intersection(docs)
    
    # Convert the final result document set to a sorted list and return it
    result_list = sorted(list(result_docs))
    return result_list


query = input("Please enter query : ")
print(search_query(inverted_index, query))
