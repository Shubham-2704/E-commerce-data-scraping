from sites.flipkart import flipkart_search, flipkart_product
from sites.amazon import amazon_search, amazon_product
from sites.ebay import ebay_search, ebay_product

def get_search_function(site):
    site = site.lower()

    if site == "flipkart":
        return flipkart_search

    if site == "amazon":
        return amazon_search
    
    if site == "ebay":
        return ebay_search

    raise Exception("Invalid site → " + site)


def get_product_function(site):
    site = site.lower()

    if site == "flipkart":
        return flipkart_product

    if site == "amazon":
        return amazon_product
    
    if site == "ebay":
        return ebay_product

    raise Exception("Invalid site → " + site)
