# from whoosh.index import open_dir

# # Open the existing index directory
# ix = open_dir("index")

# # Get the term and document lists for the "content" field
# with ix.searcher() as searcher:
#     content_terms = tuple(searcher.lexicon("content"))
#     # print(content_terms)
#     # for term in content_terms:
#         # doc_list = tuple(searcher.documents(content=term))
#         # posting_list=searcher.postings("content",term)
        
#         # print(term, list(posting_list.all_ids()))
#         # print(list(posting_list.))
#         # print(f"Doc frequency: {posting_list.doc_frequency()}\n")
#     # for term in content_terms:
#     #     postings = searcher.postings("content", term)
#     #     if postings is not None:
#     #         while postings.is_active():
#     #             doc_id = postings.id()
#     #             # freq = postings.frequency()
#     #             # print(f"term '{term}' appears {list(postings)} times in document {doc_id}")
#     #             postings.advance()




# # دریافت تمامی ترم‌های موجود در فیلد "text"
# # all_terms = reader.field_terms("content")

# # # چاپ فرکانس تمامی ترم‌ها
# # for term in all_terms:
# #     term_info = reader.term_info(fieldname="text", text=term)
# #     frequency = term_info.weight()
# #     print(f"Term: {term}, Frequency: {frequency}")


# with ix.searcher() as searcher:
#     content_terms = tuple(searcher.lexicon("content"))
    
#     # Iterate through each term in the content field
#     for term in content_terms:
        
#         # Get the posting list for the current term
#         posting_list = searcher.postings("content", term)
        
#         # Create a dictionary to store term frequency information
#         term_freqs = {}
        
#         # Iterate through each document in the posting list
#         while posting_list.is_active():
            
#             # Get the document number for the current document
#             docnum = posting_list.id()
            
#             # Get the number of times the term appears in the current document
#             freq = posting_list.weight()
            
#             # Update the term frequency information in the dictionary
#             term_freqs[docnum] = freq
            
#             # Move to the next document in the posting list
#             posting_list.next()
#             print(term_freqs)
        
#         # Print the term and its frequency information
#         print(f"Term: {term}")
#         for docnum, freq in term_freqs.items():
#             print(f"  Docnum: {docnum}, Freq: {freq}")


import math
from collections import Counter
from typing import Dict , List
from typing import Tuple

class CosineSimilarity:
    def __init__(self, documents: List[Tuple[str, str]]) -> None:
        self.doc_freqs : Dict[str, int]   = Counter()
        self.create_doc_frequency(documents)

        self.idf: Dict[str, float]  = {}
        self.create_inverse_term_frequency(documents)

        self.doc_vectors:Dict[int,Tuple[str,List[float]]] = {}
        self.create_document_vectors(documents)

    def create_doc_frequency(self, documents : List[Tuple[str, str]]) -> None:
        for ـ, doc in documents:
            self.doc_freqs.update(Counter(doc.split()))

    def create_inverse_term_frequency(self, documents : List[Tuple[str, str]]) -> None:
        num_docs = len(documents)
        for word, freq in self.doc_freqs.items():
            self.idf[word] = math.log(num_docs / freq)

    def create_document_vectors(self, documents: List[Tuple[str, str]]) -> None:
        for i, (title, doc) in enumerate(documents):
            tf = Counter(doc.split())
            vec = [tf[w] * self.idf[w] for w in self.doc_freqs.keys()]
            self.doc_vectors[i] = (title, vec)
            

    def cosine_similarity(self, query :str ="query") -> List[Tuple[str, float]]:
        tf: Dict[str, int] = Counter(query.split())
        q_vec:List[float] = [tf[w] * self.idf[w] if w in tf else 0 for w in self.doc_freqs.keys()]

        sims:List[Tuple[str, float]] = []
        for i, (title, d_vec) in self.doc_vectors.items():
            dot_product:float = sum([a*b for a,b in zip(d_vec, q_vec)])
            norm_d:float = math.sqrt(sum([a*a for a in d_vec]))
            norm_q:float = math.sqrt(sum([a*a for a in q_vec]))
            sim:float = dot_product / (norm_d * norm_q)
            sims.append((title, sim))

        return sims

doc1 = ("Document 1", "The quick brown fox jumps over the lazy dog")
doc2 = ("Document 2", "A quick brown dog outpaces a quick brown fox")
cs = CosineSimilarity([doc1, doc2])
similarity = cs.cosine_similarity("The ")
print(similarity)
