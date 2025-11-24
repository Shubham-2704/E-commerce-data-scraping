import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_driver(headless=True):
    options = Options()

    # if headless:
    #     options.add_argument("--headless=new")

    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")

    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1 Safari/605.1.15",
    ]
    options.add_argument(f"user-agent={random.choice(agents)}")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
