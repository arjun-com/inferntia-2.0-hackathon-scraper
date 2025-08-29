from .scraper import PESURedditScraper
from pprint import pprint
import dotenv
import os

dotenv.load_dotenv()

def print_divider():
    pprint(f"\n\n {'*' * 80} \n\n")

prs = PESURedditScraper(os.getenv("client_id"), os.getenv("client_secret"), os.getenv("user_agent"))

pprint(prs.scrape(3, "hot"))
print_divider()

pprint(prs.scrape(3, "new"))
print_divider()

pprint(prs.scrape(3, "top"))
print_divider()

pprint(prs.scrape(3, "rising"))
print_divider()

pprint(prs.scrape(3, "controversial"))