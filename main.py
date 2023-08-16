from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains
import requests
import lxml
import time


GOOGLE_FORMS_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSe_JY3jbLYgdxoVz9vCWXV2sUjBrpSU3V_QL9q2gnjDgMPBOw/viewform?usp=sf_link"
ZILLOW_SEARCH_LINK = "https://www.zillow.com/houston-tx/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A30.300177589327454%2C%22east%22%3A-94.62097225585939%2C%22south%22%3A29.332699738543873%2C%22west%22%3A-96.22772274414064%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A39051%2C%22regionType%22%3A6%7D%5D%7D"

addresses_list = []
links_list = []
prices_list = []
# ---------------- Get data from Zillow ----------------- #

# ---- with bs4 only ---- #
# ACCEPT_LANGUAGE = "en-US,en;q=0.5"
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"
#
# header = {
#     "User-Agent": USER_AGENT,
#     "Accept-Language": ACCEPT_LANGUAGE,
# }
#
# response = requests.get(ZILLOW_SEARCH_LINK, headers=header)
# soup = BeautifulSoup(response.text, "lxml")


# ---- with selenium ---- #
options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get(ZILLOW_SEARCH_LINK)
driver.maximize_window()

# -- start scrolling -- #
time.sleep(5)

scroll_origin_ref = driver.find_element(By.CSS_SELECTOR, 'span[data-test="property-card-price"]')

y = 500
for _ in range(12):
    scroll_origin = ScrollOrigin.from_element(scroll_origin_ref)
    ActionChains(driver) \
        .scroll_from_origin(scroll_origin, 0, y) \
        .perform()
    time.sleep(2)
    y += 500

source_code = driver.page_source

soup = BeautifulSoup(source_code, "lxml")
# ---------- data one page --------- #
cards = soup.select("address")

for card in cards:
    print(card.text)
    addresses_list.append(card)

links = soup.select(".property-card-link")

url_prefix = "https://www.zillow.com"
for link in links:
    href = link.get("href")
    if href.find("https://") == -1:   # "https:" not found
        href = url_prefix + href
    print(href)
    links_list.append(href)

prices = soup.select(".property-card-data div div span")

for price in prices:
    print(price.text)
    prices_list.append(prices)


# ---------------- fill data into Google Form ----------------- #

# options = Options()
# options.add_experimental_option("detach", True)
#
# driver = webdriver.Chrome(options=options)
driver.get(GOOGLE_FORMS_LINK)
time.sleep(3)

for i in range(len(addresses_list)):
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(prices_list[i])

    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(addresses_list[i])

    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(links_list[i])
    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()
    time.sleep(2)

driver.quit()