from bs4 import BeautifulSoup
import selenium
import requests



GOOGLE_FORMS_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSe_JY3jbLYgdxoVz9vCWXV2sUjBrpSU3V_QL9q2gnjDgMPBOw/viewform?usp=sf_link"
ZILLOW_SEARCH_LINK = "https://www.zillow.com/houston-tx/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A30.300177589327454%2C%22east%22%3A-94.62097225585939%2C%22south%22%3A29.332699738543873%2C%22west%22%3A-96.22772274414064%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A39051%2C%22regionType%22%3A6%7D%5D%7D"


ACCEPT_LANGUAGE = "en-US,en;q=0.5"
USER_AGENT = ""

header = {
    "User-Agent": USER_AGENT,
    "Accept-Language": ACCEPT_LANGUAGE,
}

response = requests.get(ZILLOW_SEARCH_LINK, headers=header)

soup = BeautifulSoup(response.text, "html.parser")

cards = soup.select("address")

for card in cards:
    print(card.text)

links = soup.select(".property-card-link")

for link in links:
    print(link.get("href"))


prices = soup.select(".property-card-data div div span")

for price in prices:
    print(price.text)