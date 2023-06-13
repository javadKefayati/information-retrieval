import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import json
import uuid

# init the colorama module
colorama.init()

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()
main_data = set()

total_urls_visited = 0
url_id = 1


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if 'team' in str(href):
            continue
        if 'java' not in str(href):
            continue
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        try:
            get_all_website_text(href)
        except:
            pass
        internal_urls.add(href)
    return urls


def get_all_website_text(url):
    """
    Returns all text data that is found on `url` in which it belongs to the same website
    """
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    result = {}
    for tag in soup.find_all():
        if not tag.string or not tag.name:
            continue
        if tag.name not in result:
            result[tag.name] = []
        result[tag.name].append(tag.string.strip())

    global url_id

    with open(f"lang_docs/java/{url_id}.json", "w") as f:
        json.dump(result, f)

    url_id += 1


def crawl(url, max_urls=5):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")

    args = parser.parse_args()
    url = args.url
    max_urls = 5
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    crawl(url, max_urls=max_urls)

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))
    print("[+] Total crawled URLs:", max_urls)

    # save the internal links to a file
    with open(f"docs/{domain_name}_internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    # save the external links to a file
    with open(f"docs/{domain_name}_external_links.txt", "w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)
