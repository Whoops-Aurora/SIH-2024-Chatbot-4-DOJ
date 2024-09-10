import os
import requests
from bs4 import BeautifulSoup
import pdfkit

# Set the base website URL
base_url = 'https://doj.gov.in/'
visited_links = set()
all_text_content = []

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def clean_html(soup):
    # Remove scripts, styles, and other unwanted elements
    for script in soup(["script", "style", "header", "footer", "nav", "aside"]):
        script.extract()
    # Extract text
    return soup.get_text(separator='\n').strip()

def save_pdf(content, filename):
    # Convert the list of text content into a single string
    full_content = "\n\n".join(content)
    options = {
        'encoding': 'UTF-8',
    }
    pdfkit.from_string(full_content, filename, options=options)

def scrape_site(url, base_url):
    # Only scrape if the link hasn't been visited
    if url not in visited_links:
        visited_links.add(url)
        print(f'Scraping {url}')
        
        # Fetch the page content
        html_content = fetch_page(url)
        soup = BeautifulSoup(html_content, 'html.parser')

        # Clean and extract text content
        text_content = clean_html(soup)
        all_text_content.append(text_content)

        # Find all internal links and scrape them
        for link in soup.find_all('a', href=True):
            link_url = link['href']
            if link_url.startswith('/') or link_url.startswith(base_url):
                # Construct full URL
                if link_url.startswith('/'):
                    link_url = base_url + link_url
                scrape_site(link_url, base_url)

def main():
    # Start scraping from the base URL
    scrape_site(base_url, base_url)
    
    # Save the entire content into a single PDF
    save_pdf(all_text_content, 'website_content.pdf')
    print('PDF generated successfully.')

if __name__ == '__main__':
    main()
