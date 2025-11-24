import time
import random
from bs4 import BeautifulSoup
from utils.retry import retry

@retry()
def flipkart_search(query, pages, driver):
    urls = set()   
    for page in range(1, pages + 1):
        link = f"https://www.flipkart.com/search?q={query}&page={page}"
        driver.get(link)
        time.sleep(random.uniform(5, 8))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.select("a.CGtC98[href], a.rPDeLR[href], a.WKTcLC[href], a.wjcEIp[href]")

        for a in cards:
            href = a.get("href")
            if not href:
                continue

            if href.startswith("/"):
                full_url = "https://www.flipkart.com" + href
            else:
                full_url = href

            # Add to set (prevents duplicates)
            urls.add(full_url)

    return list(urls)  # convert back to list



@retry()
def flipkart_product(url, driver):
    driver.get(url)
    time.sleep(random.uniform(4, 7))
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Basic info
    title = soup.select_one("span.VU-ZEz")
    price = soup.select_one("div.Nx9bqj")
    rating = soup.select_one("div.XQDdHH")

    result = {
        "title": title.get_text(strip=True) if title else None,
        "price": price.get_text(strip=True) if price else None,
        "rating": rating.get_text(strip=True) if rating else None,
        "link": url
    }

    highlights = soup.select("div._2418kt li, li._21Ahn-")
    if highlights:
        result["highlights"] = [li.get_text(strip=True) for li in highlights]

    # Specs table (multiple layout types)
    rows = soup.select("table._14cfVK tr")
    if not rows:
        rows = soup.select("tr.WJdYP6")

    for r in rows:
        k = r.find("td", class_="+fFi1w") or r.find("td", class_="_1hKmbr")
        v = r.find("td", class_="Izz52n") or r.find("td", class_="_21lJbe")
        if k and v:
            result[k.get_text(strip=True)] = v.get_text(strip=True)

    col_labels = soup.select("div.col.col-3-12")
    col_values = soup.select("div.col.col-9-12")

    for k, v in zip(col_labels, col_values):
        key = k.get_text(strip=True)
        val = v.get_text(strip=True)
        if key and val:
            result[key] = val

    return result
