from typing import Dict , List , Any
from typing import Tuple
from whoosh.analysis import StopFilter, StemmingAnalyzer
from whoosh.lang.porter import stem
from whoosh.lang.stopwords import stoplists
import heapq
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from typing import Tuple,List
import json

class CosineSimilarity:
    def __init__(self, documents: List[Tuple[str, str]]) -> None:
        """ This function create list of vector for analyze content and scoring

        Args:
            documents (List[Tuple[str, str]]): List of document 
        """
        
        self.doc_freqs : Dict[str, int]  = Counter()
        self.create_doc_frequency(documents)

        self.idf: Dict[str, float]  = {}
        self.create_inverse_term_frequency(documents)

        self.doc_vectors:Dict[int,Tuple[str,List[float]]] = {}
        self.create_document_vectors(documents)

    def create_doc_frequency(self, documents : List[Tuple[str, str]]) -> None:
        """ This function create list of document frequency that contain word and number of
            repeat in all documents

        Args:
            documents (List[Tuple[str, str]]): list of document 
        """
        for ـ, doc in documents:
            self.doc_freqs.update(Counter(doc.split()))

    def create_inverse_term_frequency(self, documents : List[Tuple[str, str]]) -> None:
        """ Create inverse term frequency with this formula 
            idf for specified word = log(length of all documents / number of repeats in all docs)

        Args:
            documents (List[Tuple[str, str]]): List of document 
        """
        num_docs = len(documents)
        for word, freq in self.doc_freqs.items():
            self.idf[word] = math.log(num_docs / freq)

    def create_document_vectors(self, documents: List[Tuple[str, str]]) -> None:
        """ This functions create list of tuples that contain title and
            inverse term frequency each word * term frequency of each word

        Args:
            documents (List[Tuple[str, str]]): List of document 
        """
        for i, (title, doc) in enumerate(documents):
            tf = Counter(doc.split())
            vec = [tf[w] * self.idf[w] for w in self.doc_freqs.keys()]
            self.doc_vectors[i] = (title, vec)
        
            

    def cosine_similarity(self, query :str ="query") -> List[Tuple[str, float]]:
        """ This func create list of the approximate amount query with each document

        Args:
            query (str, optional): A string that the user enters to measure the similarity of the text with other texts. Defaults to "query".

        Returns:
            List[Tuple[str, float]]: List of the approximate amount query with each document
        """
        # Removed stop words and finds the root of the rest
        tf: Dict[str, int] = Counter(query.split())
        q_vec:List[float] = [tf[w] * self.idf[w] if w in tf else 0 for w in self.doc_freqs.keys()]
        sims:List[Tuple[str, float]] = []
        for _, (title, d_vec) in self.doc_vectors.items():
            dot_product:float = sum([a*b for a,b in zip(d_vec, q_vec)])
            norm_d:float = math.sqrt(sum([a*a for a in d_vec]))
            norm_q:float = math.sqrt(sum([a*a for a in q_vec]))
            try:
                sim:float = dot_product / (norm_d * norm_q)
            except ZeroDivisionError:
                sim:float = dot_product / ((norm_d * norm_q)+0.0001)
            sims.append((title, sim))

        return sims
    

class Searcher:
    header_tags = ["h1", "h2", "h3", "h4", "h5", "h6","title"]
    simple_tags = ["p","span","div","button"]
    header_weight = 4
    content_each_file = []
    files_name = []
    
    def __init__(self):
        self.processing_json_files()
        
    def preprocessed_text(self, text:str )-> str:
        """This function takes a Text and removes the stop words and finds the root of the rest

        Args:
            text (str): A string of words in a row

        Returns:
            str: A string that removed stop words and finds the root of the rest
        """
        stopwords: Any = frozenset(stoplists["en"])

        analyzer = StemmingAnalyzer(stemfn=stem, stoplist=stopwords) | StopFilter(stoplist=stopwords)
        # Tokenize and analyze the text using the defined analyzer
        tokens:List[str] = [token.text for token in analyzer(text)]

        # Join the tokens back together to form a preprocessed string
        preprocessed_text = " ".join(tokens)
        return preprocessed_text
    
    def create_str_from_tags_content(self,json_address, tags_list):
        tags_str = ""
        with open(json_address, 'r') as f:
            # Load the contents of the file into a dictionary
            html_content = json.load(f)
            #get headers of json file
            for tag in tags_list:
                if tag in html_content:
                    tags_str += " ".join(html_content[tag]) 
        return tags_str
    
    def name_of_files(self, dic_address):
        self.files_name  = os.listdir(dic_address)
        return self.files_name
        
    def processing_json_files(self, dic_address="./docs/"):
        files = self.name_of_files(dic_address)
        headers_str = ""
        
        for file in files:
            headers_text = self.create_str_from_tags_content(dic_address+file,self.header_tags)
            simple_text = self.create_str_from_tags_content(dic_address+file,self.simple_tags)
            total_content = self.preprocessed_text(simple_text) +self.preprocessed_text(headers_str) * self.header_weight
            
            self.content_each_file.append(total_content)
            
    # for this func please change result of func to number nearly score or prediction 
    def get_nlargest_similarity_doc(self, n_first:int ) ->List[Tuple[str,float]]:
        """ Return a list of nearly result for query and documents

        Args:
            n_first (int): Number of nearly results

        Returns:
            List[Tuple[str,float]]: A list contain score and document number
        """
        return heapq.nlargest(n_first,self.scores_details, key=lambda x: x[1])
    def query_with_bayes_algo(self, query:str= "query")->None:
        """calculating rank

        Args:
            query (str, optional): a string that for search in json files. Defaults to "query".
        """

        # Create a vectorizer to convert text into numerical features
        vectorizer = CountVectorizer()
        
        # Vectorize the documents
        X = vectorizer.fit_transform(self.content_each_file)
        
        # Train a Naive Bayes classifier on the vectorized documents
        clf = MultinomialNB()
        
        clf.fit(X, self.files_name)
        new_vec = vectorizer.transform([query])
        # print(new_vec)
        scores = clf.predict_proba(new_vec)
        self.scores_details = tuple(zip(self.files_name, scores[0]))
    
    def query_with_cos_algo(self,query=""):
        self.cosineSimilarity = CosineSimilarity(self.information)
        query = self.preprocessed_text(query)
        self.scores_details = self.cosineSimilarity.cosine_similarity(query)
        
    def print_results(self, n_first:int = 10)-> None:
        """ Print all ranked score 

        Args:
            n_first (int, optional): Number of nearly results. Defaults to 10.
        """
        
        if len(self.scores_details) != 0  :
            n_first_similarly_doc = self.get_nlargest_similarity_doc(n_first)
            print('----------------- RESULTS ---------------------')
            print("      SCORE         ***     DOCUMENT NAME")
            print('-----------------------------------------------')

            for index,result in enumerate(n_first_similarly_doc):
                
                document_number = result[0].split(".")[0]
                score = index + 1
                print(f"        {score:<20}{document_number}")

        else :
            print("Please First call search query function")
                


s = Searcher()
s.query("chat")
s.print_results(n_first = 2)

