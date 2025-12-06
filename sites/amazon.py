import time
import random
from bs4 import BeautifulSoup
from utils.retry import retry


@retry()
def amazon_search(query, pages, driver):
    urls = []
    for page in range(1, pages + 1):
        link = f"https://www.amazon.in/s?k={query}&page={page}"
        driver.get(link)
        time.sleep(random.uniform(5, 9))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.select("div.s-result-item[data-asin]")

        for item in items:
            asin = item.get("data-asin")
            if asin:
                urls.append(f"https://www.amazon.in/dp/{asin}")

    return urls


@retry()
def amazon_product(url, driver):
    driver.get(url)
    time.sleep(random.uniform(4, 7))
    soup = BeautifulSoup(driver.page_source, "html.parser")

    def clean(t):
        if not t:
            return t
        t = t.replace("\u200e", "").replace("\u200f", "").strip()
        return t.lstrip(":").strip()

    result = {}

    # BASIC FIELDS
    title = soup.select_one("#productTitle")
    price = soup.select_one("span.a-offscreen")
    rating = soup.select_one("span.a-icon-alt")
    availability = soup.select_one("#availability span")

    result["title"] = clean(title.get_text()) if title else None
    result["price"] = clean(price.get_text()) if price else None
    result["rating"] = clean(rating.get_text()) if rating else None
    result["availability"] = clean(availability.get_text()) if availability else None
    result["link"] = url

    # ABOUT THIS ITEM
    about_items = soup.select("#feature-bullets li span.a-list-item")
    if about_items:
        result["about"] = [clean(li.get_text()) for li in about_items]

    # DETAIL BULLETS SECTION
    # (works for shoes, watches, fashion)
    bullets = soup.select("#detailBullets_feature_div li")
    for li in bullets:
        parts = li.get_text(":", strip=True).split(":", 1)
        if len(parts) == 2:
            key, value = clean(parts[0]), clean(parts[1])
            result[key] = value

    # TECH DETAILS 1 (table)
    tech1 = soup.select("#productDetails_techSpec_section_1 tr")
    for tr in tech1:
        th, td = tr.find("th"), tr.find("td")
        if th and td:
            result[clean(th.get_text())] = clean(td.get_text())

    # TECH DETAILS 2 (table)
    tech2 = soup.select("#productDetails_detailBullets_sections1 tr")
    for tr in tech2:
        th, td = tr.find("th"), tr.find("td")
        if th and td:
            result[clean(th.get_text())] = clean(td.get_text())

    # MOBILE LAYOUT TABLE
    rows_mobile = soup.select("table.a-normal.a-spacing-micro tr")
    for tr in rows_mobile:
        th, td = tr.find("td", class_="a-span3"), tr.find("td", class_="a-span9")
        if th and td:
            result[clean(th.get_text())] = clean(td.get_text())

    # A+ CONTENT SPEC LIST
    aplus = soup.select("div.aplus-module-wrapper p")
    for p in aplus:
        text = clean(p.get_text())
        if ":" in text:
            k, v = text.split(":", 1)
            result[clean(k)] = clean(v)

    return result
