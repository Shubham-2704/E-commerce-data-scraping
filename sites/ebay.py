import time
import random
import re
from bs4 import BeautifulSoup
from utils.retry import retry


def is_valid_ebay_link(url):
    # Real product links look like: /itm/165778620268
    return re.search(r"/itm/\d{9,12}", url) is not None

@retry()
def ebay_search(query, pages, driver):
    urls = []

    for page in range(1, pages + 1):
        link = f"https://www.ebay.com/sch/i.html?_nkw={query}&_pgn={page}"
        driver.get(link)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Product card <a> tags
        cards = soup.select("a.s-card__link[href], a.image-treatment[href]")

        for a in cards:
            href = a.get("href")
            if not href:
                continue

            # Normalize link
            if href.startswith("http"):
                url = href
            else:
                url = "https://www.ebay.com" + href

            # Only accept REAL product URLs
            if not is_valid_ebay_link(url):
                continue

            clean = url.split("?")[0]

            if clean not in urls:
                urls.append(clean)

    return urls

@retry()
def ebay_product(url, driver):
    driver.get(url)
    time.sleep(4)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    result = {"link": url}

    title = soup.select_one("h1.x-item-title__mainTitle")
    result["title"] = title.get_text(strip=True) if title else None

    price = soup.select_one("div.x-price-primary")
    result["price"] = price.get_text(strip=True) if price else None

    spec_rows = soup.select("dl.ux-labels-values")

    for row in spec_rows:
        label_el = row.select_one("dt.ux-labels-values__labels span")
        value_el = row.select_one("dd.ux-labels-values__values span")

        if label_el and value_el:
            key = label_el.get_text(strip=True).replace(":", "")
            val = value_el.get_text(strip=True)
            result[key] = val

    return result
