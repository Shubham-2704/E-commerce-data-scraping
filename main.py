import json
from core.logger import get_logger
from core.driver import get_driver
from core.router import get_search_function, get_product_function

logger = get_logger()

def run():
    site = input("Site (flipkart / amazon / ebay): ").strip().lower()
    query = input("Search query: ").strip().replace(" ", "+")
    pages = int(input("How many pages to scrape? ").strip())
    max_items = int(input("Max products to collect? ").strip())

    driver = get_driver()

    # get correct search + product function based on site
    search_fn = get_search_function(site)
    product_fn = get_product_function(site)

    logger.info(f"Searching {site} for '{query}' ...")

    # searching
    urls = search_fn(query, pages, driver)
    urls = urls[:max_items]

    logger.info(f"Found {len(urls)} products, scraping details...")

    results = []
    for url in urls:
        data = product_fn(url, driver)
        if data:
            results.append(data)

    driver.quit()

    # save output json
    output_file = f"{site}_{query}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    logger.info(f"Completed — saved to {output_file}")


if __name__ == "__main__":
    run()
