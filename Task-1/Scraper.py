# Imports
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import os


class AmazonLaptopScraper:

    def __init__(self):

        self.url = "https://www.amazon.in/s?k=laptops&page={}"
        self.products = []

        self.headers = {
            "User-Agent": "Mozilla/5.0 Chrome/124.0"
        }

    def fetch_page(self, page):

        response = requests.get(
            self.url.format(page),
            headers=self.headers
        )

        if response.status_code == 200:
            return response.text

        return None

    def parse_products(self, html):

        soup = BeautifulSoup(html, "lxml")

        products = soup.find_all(
            "div",
            {"data-component-type": "s-search-result"}
        )

        for product in products:

            try:

                title = product.find("h2").text.strip()

                price_tag = product.find(
                    "span",
                    class_="a-price-whole"
                )

                rating_tag = product.find(
                    "span",
                    class_="a-icon-alt"
                )

                image_tag = product.find(
                    "img",
                    class_="s-image"
                )

                link_tag = product.find(
                    "a",
                    class_="a-link-normal s-no-outline"
                )

                sponsored = product.find(
                    string=lambda text: text and "Sponsored" in text
                )

                self.products.append({
                    "Title": title,
                    "Price": price_tag.text if price_tag else "N/A",
                    "Rating": rating_tag.text if rating_tag else "N/A",
                    "Image_URL": image_tag["src"] if image_tag else "N/A",
                    "Product_URL": (
                        "https://www.amazon.in" + link_tag["href"]
                    ) if link_tag else "N/A",
                    "Result_Type": "Ad" if sponsored else "Organic"
                })

                print(f"Scraped -> {title[:50]}")

            except:
                pass

    def save_csv(self):

        os.makedirs("output", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        file_name = f"output/amazon_laptops_{timestamp}.csv"

        pd.DataFrame(self.products).to_csv(
            file_name,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"\nCSV Saved -> {file_name}")

    def run(self, pages=3):

        print("\nAmazon Laptop Scraper Started\n")

        for page in range(1, pages + 1):

            html = self.fetch_page(page)

            if html:
                self.parse_products(html)

            time.sleep(2)

        self.save_csv()

        print("\nScraping Completed")


if __name__ == "__main__":

    scraper = AmazonLaptopScraper()

    scraper.run(pages=3)