import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
import time

# Set up logging
logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s %(message)s')

# Set the base URL and start URLs
BASE_URL = "https://cloud.google.com/looker/docs"
START_URLS = [
    BASE_URL,
    "https://cloud.google.com/looker/docs/intro",
    "https://cloud.google.com/looker/docs/best-practices/home",
    "https://cloud.google.com/looker/docs/reference/lookml-quick-reference",
    "https://cloud.google.com/looker/docs/reference/available-apis"
]

# URLs to skip
SKIP_URLS = {"https://cloud.google.com/looker/docs/historical-releases"}

# Initialize sets for visited URLs and broken links
visited_urls = set()
broken_links = set()

# Function to save content
def save_content(url, content):
    with open("lookerdocs.html", "a", encoding="utf-8") as html_file, open("lookerdocs.txt", "a", encoding="utf-8") as text_file:
        html_file.write(f"<h2>Source: {url}</h2>\n")
        html_file.write(content + "\n")
        soup = BeautifulSoup(content, 'html.parser')
        text_file.write(f"\nSource: {url}\n")
        text_file.write(soup.get_text(separator="\n", strip=True) + "\n")

# Function to crawl a URL
def crawl(url):
    # Remove the anchor part from the URL
    core_url = url.split('#')[0]

    if core_url in visited_urls or core_url in SKIP_URLS or "/docs/23" in core_url or "hl=" in core_url:
        return
    visited_urls.add(core_url)

    try:
        response = requests.get(core_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('article', class_='devsite-article')
        if article:
            save_content(core_url, str(article))

            # Logging the current URL and number of links found
            links = article.find_all('a', href=True)
            logging.info(f"Visited {core_url} - Found {len(links)} links")

            # Crawling the found links
            for link in links:
                href = link['href']
                next_url = urljoin(core_url, href)
                if next_url.startswith(BASE_URL):
                    crawl(next_url)

        # Pause to mitigate rate limiting
        time.sleep(0.15)

    except requests.RequestException as e:
        logging.error(f"Error crawling {core_url}: {e}")
        broken_links.add(core_url)

# Start crawling from the start URLs
for start_url in START_URLS:
    crawl(start_url.split('#')[0])

# Save the list of broken links
with open("brokenlinks.txt", "w", encoding="utf-8") as file:
    for link in broken_links:
        file.write(link + "\n")

print("Crawling complete.")
