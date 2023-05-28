import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.analysis import StemmingAnalyzer
from whoosh import query
from whoosh.analysis import StopFilter, StemmingAnalyzer
from whoosh.lang.porter import stem
from whoosh.lang.stopwords import stoplists
import glob

def create_index_directory(path="" , name="index"):
  if not os.path.exists(path+"index"):
      os.mkdir(path+"index")
  return  create_in("index", schema)
  
def create_schema():
  stopwords = frozenset(stoplists["en"])

  analyzer = StemmingAnalyzer(stemfn=stem, stoplist=stopwords) | StopFilter(stoplist=stopwords)

  return  Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(analyzer=analyzer))


def indexing_docs(docs_addresses):
  writer = ix.writer()
  
  for i, file in enumerate(files):
      with open(file, 'r') as f:
        contents = f.read()

      writer.add_document(title=file, path= file , content=contents)

  writer.commit()


def searcher(boolean_query):
  #for create parser and return docs number 
  with ix.searcher() as searcher:
      parser = QueryParser("content",  termclass=query.Variations ,schema=schema)
      q = parser.parse(boolean_query)
      results = searcher.search(q)
      for i , r in  enumerate(results):
        title = r["title"]
        print(f"score: {i+1}          -----       doc name: {title}")
    
global schema , ix
files = glob.glob('./docs/*.txt')
schema = create_schema()
ix = create_index_directory()
indexing_docs(files)

query_input = input("Enter query : ")
searcher(query_input)

from whoosh.analysis import StandardAnalyzer, StopFilter, StemmingAnalyzer

def preprocess_text(text):
    # Define the analyzer for removing stop words and stemming
    analyzer = StemmingAnalyzer() | StopFilter()

    # Tokenize and analyze the text using the defined analyzer
    tokens = [token.text for token in analyzer(text)]

    # Join the tokens back together to form a preprocessed string
    preprocessed_text = " ".join(tokens)

    return preprocessed_text

a = preprocess_text("HEllo eveRy one schools and very Good was were")
