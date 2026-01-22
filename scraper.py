import asyncio
import json
import os
import re
from datetime import datetime
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# List of target URLs provided for the AI Solution Accelerators project
TARGET_URLS = [
    "https://accelerators.ms/",
    "https://aka.ms/csaGoldStandards",
    "https://github.com/microsoft/Solution-Accelerators",
    "https://github.com/microsoft/Commercial-Solution-Areas-Accelerators"
]

class AzureAIScraper:
    def __init__(self, output_dir="scraped_data"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def clean_text(self, text):
        """Removes extra whitespace and boilerplate."""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    async def scrape_url(self, browser, url):
        """Navigates to a URL, waits for JS to load, and extracts content."""
        page = await browser.new_page()
        print(f"[*] Navigating to: {url}")
        
        try:
            # Navigate and wait for the network to be idle (important for JS-heavy sites)
            await page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Get the full rendered HTML
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')

            # Remove script and style elements
            for script_or_style in soup(["script", "style", "nav", "footer", "header"]):
                script_or_style.decompose()

            # Extract data
            title = soup.title.string if soup.title else "No Title"
            
            # Focus on main content areas to avoid sidebar noise
            main_content = soup.find('main') or soup.find('article') or soup.body
            text_content = self.clean_text(main_content.get_text(separator=' '))

            result = {
                "source_url": url,
                "title": title.strip(),
                "timestamp": datetime.now().isoformat(),
                "content": text_content,
                "metadata": {
                    "char_count": len(text_content),
                    "word_count": len(text_content.split())
                }
            }

            # Save as JSON for Azure Ingestion
            filename = re.sub(r'\W+', '_', url.split('//')[-1]) + ".json"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4)
            
            print(f"[+] Successfully scraped and saved: {filename}")
            return result

        except Exception as e:
            print(f"[!] Error scraping {url}: {str(e)}")
            return None
        finally:
            await page.close()

    async def run(self):
        async with async_playwright() as p:
            # Launching headless browser
            browser = await p.chromium.launch(headless=True)
            tasks = [self.scrape_url(browser, url) for url in TARGET_URLS]
            results = await asyncio.gather(*tasks)
            await browser.close()
            return results

if __name__ == "__main__":
    print("--- Starting Azure AI Solution Accelerator Scraper ---")
    scraper = AzureAIScraper()
    try:
        results = asyncio.run(scraper.run())
        print(f"--- Scraping Complete. Files saved in /{scraper.output_dir} ---")
        print(f"Total pages scraped: {len([r for r in results if r is not None])}")
    except Exception as e:
        print(f"[!] Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()