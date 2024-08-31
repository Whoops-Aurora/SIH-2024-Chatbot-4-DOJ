import os
import requests
from bs4 import BeautifulSoup
import pdfkit

# Set the website URL
base_url = 'https://example.com'
visited_links = set()

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def clean_html(soup):
    # Remove scripts, styles, and other unwanted elements
    for script in soup(["script", "style", "header", "footer", "nav", "aside"]):
        script.extract()
    return soup.get_text()

def save_pdf(content, filename):
    options = {
        'encoding': 'UTF-8',
    }
    pdfkit.from_string(content, filename, options=options)

def scrape_site(url, base_url):
    # Only scrape if the link hasn't been visited
    if url not in visited_links:
        visited_links.add(url)
        print(f'Scraping {url}')
        
        # Fetch the page content
        html_content = fetch_page(url)
        soup = BeautifulSoup(html_content, 'html.parser')

        # Clean the content
        text_content = clean_html(soup)

        # Find all internal links
        for link in soup.find_all('a', href=True):
            link_url = link['href']
            if link_url.startswith('/') or link_url.startswith(base_url):
                # Construct full URL
                if link_url.startswith('/'):
                    link_url = base_url + link_url
                scrape_site(link_url, base_url)

        return text_content
    return ''

def main():
    site_content = scrape_site(base_url, base_url)
    # Save the entire content into a single PDF
    save_pdf(site_content, 'website_content.pdf')
    print('PDF generated successfully.')

if __name__ == '__main__':
    main()
