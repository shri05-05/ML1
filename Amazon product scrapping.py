import requests
from bs4 import BeautifulSoup
import random
import time

def scrape_amazon_product(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to retrieve page: {e}"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract product details
    title = soup.select_one("#productTitle")
    price_whole = soup.select_one(".a-price-whole")
    price_fraction = soup.select_one(".a-price-fraction")
    rating = soup.select_one(".a-icon-alt")
    image = soup.select_one("#landingImage")

    full_price = f"{price_whole.get_text(strip=True)}.{price_fraction.get_text(strip=True)}" if price_whole and price_fraction else (price_whole.get_text(strip=True) if price_whole else "No price")

    return {
        "title": title.get_text(strip=True) if title else "No title",
        "price": full_price,
        "rating": rating.get_text(strip=True) if rating else "No rating",
        "image": image["src"] if image else "No image"
    }

# List of 10 Amazon product URLs
amazon_urls = [
    "https://amzn.in/d/7d58U3j",
    "https://amzn.in/d/1pfrHsn",
    "https://amzn.in/d/coqE283",
    "https://amzn.in/d/5IWekrH",
    "https://amzn.in/d/91XhpMB",
    "https://amzn.in/d/56Sy0Ae",
    "https://amzn.in/d/3rlwdVR",
    "https://amzn.in/d/ivufT19",
    "https://amzn.in/d/b6kgpqq",
    "https://amzn.in/d/9vKnl8O",
]

# Scrape each product and print results
if __name__ == "__main__":
    for index, url in enumerate(amazon_urls, start=1):
        print(f"\nScraping product {index}...")
        product_details = scrape_amazon_product(url)
        print(product_details)

        # Add a random delay (2-5 seconds) between requests
        time.sleep(random.uniform(2, 5))
