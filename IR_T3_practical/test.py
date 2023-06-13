import os
import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from urllib.parse import urljoin, urlparse
import time
# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

def is_valid_url(url):
    """
    Check if the URL is valid.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_links(soup):
    """
    Extract all links from the soup object.
    """
    links = []
    for a_tag in soup.find_all("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None or href.startswith("/"):
            continue
        links.append(href)
    return links

def crawl_url(url, max_pages=5):
    """
    Crawl the website and save HTML files.
    """
    visited_urls = set()
    urls_to_visit = [url]
    html_files = []

    while urls_to_visit and len(visited_urls) < max_pages:
        url = urls_to_visit.pop(0)
        if not is_valid_url(url) or url in visited_urls:
            continue
        time.sleep(0.06)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        visited_urls.add(url)

        html_files.append((url, response.content))

        for link in get_all_links(soup):
            new_url = urljoin(url, link)
            if new_url not in visited_urls:
                urls_to_visit.append(new_url)

    return html_files

def save_html_files(html_files, directory="html_files"):
    """
    Save HTML files to a directory.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    for url, content in html_files:
        file_name = urlparse(url).path.split("/")[-1] or "index.html"
        file_path = os.path.join(directory, file_name)

        with open(file_path, "wb") as f:
            f.write(content)

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
    main()