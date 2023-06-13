import os
import requests
from bs4 import BeautifulSoup
# from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
# from urllib.parse import urljoin, urlparse



def bayes_scoring(html_file):
    """
    Perform sentiment analysis using Bayes theorem and NLTK.
    """
    soup = BeautifulSoup(html_file, "html.parser")
    text = soup.get_text()
    words = word_tokenize(text)

    header_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
    header_words = []
    for tag_name in header_tags:
        for tag in soup.find_all(tag_name):
            header_words.extend(word_tokenize(tag.get_text()))

    header_weight = 2
    total_words = words + header_words * (header_weight - 1)
    sentiment = sia.polarity_scores(" ".join(total_words))
    return sentiment["compound"]

def search_html_files(query, directory="html_files"):
    """
    Search for relevant HTML files within the directory.
    """
    matching_files = []

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        with open(file_path, "r") as f:
            content = f.read()
            if query in content:
                matching_files.append((file_name, file_path))

    return matching_files

def main():
    url = "https://stackoverflow.com/"  # Replace with the desired URL
    html_files = crawl_url(url)
    save_html_files(html_files)

    scores = {}
    for url, content in html_files:
        file_name = urlparse(url).path.split("/")[-1] or "index.html"
        scores[file_name] = bayes_scoring(content)

    # Example query
    query = "python"  # Replace with the desired query
    matching_files = search_html_files(query)
    for file_name, file_path in matching_files:
        print(f"File: {file_name} (score: {scores[file_name]})\nPath: {file_path}")

if __name__ == "__main__":
    # main()
    print(word_tokenize("hello guys and were none"))