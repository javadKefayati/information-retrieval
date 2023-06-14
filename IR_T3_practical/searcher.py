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
    def query(self, query:str= "query")->None:
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

