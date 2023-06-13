import math
from collections import Counter
from typing import Dict , List , Any
from typing import Tuple
from whoosh.analysis import StopFilter, StemmingAnalyzer
from whoosh.lang.porter import stem
from whoosh.lang.stopwords import stoplists
import heapq
class Searcher:
    
    def __init__(self):
        pass
        
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


s = Searcher()
print(s.preprocessed_text("hello world was and"))