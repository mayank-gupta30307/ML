from bs4 import BeautifulSoup
import requests
import os
import json
from tqdm import tqdm


curr_loc = os.path.dirname(__file__)
url_having_links = "https://www.who.int/news-room/fact-sheets" 
target_url = "/news-room/fact-sheets/detail/"  
base_url = "https://www.who.int/"
class_id = "sf-detail-body-wrapper"


def fetch_urls(from_url , target_url):
    r = requests.get(from_url)
    soup = BeautifulSoup(r.text , "html.parser")

    scraping_urls = []
    for links in soup.find_all('a'):
        link = links.get("href")
        if link[0:len(target_url)] == target_url:
            scraping_urls.append(link)
    return scraping_urls


def save_data(scraping_urls , base_url , class_id):
    for url in tqdm(scraping_urls):
        r = requests.get(base_url+url)
        current_heading = None
        article_data = {}
        soup = BeautifulSoup(r.text , "html.parser")
        article = soup.find("article" , class_=class_id)
        for tag in article.find_all(["h2", "h3", "p", "ul"]):
            if tag.name in ["h2", "h3"]:
                current_heading = tag.get_text(strip=True)
                article_data[current_heading] = ""
            elif current_heading is not None:
                if tag.name == "p":
                    text = tag.get_text(" ", strip=True)
                    if text:
                        article_data[current_heading] += text + "\n"
                elif tag.name == "ul":
                    items = [li.get_text(" ", strip=True) for li in tag.find_all("li")]
                    article_data[current_heading] += "\n".join(f"- {item}" for item in items) + "\n"
        # Remove trailing newlines
        article_data = {k: v.strip() for k, v in article_data.items()}
        article_data["link"] = base_url+url
        field = url.split("/")[-1]
        if "WHO" not in os.listdir(os.path.join(curr_loc , "Data")):
            os.mkdir(os.path.join(curr_loc , "Data" , "WHO"))
        with open(os.path.join(curr_loc,f"Data/WHO/{field}.json") , "w") as f:
            json.dump(article_data , f , indent=4)


scraping_urls = fetch_urls(from_url = url_having_links , target_url = target_url)
save_data(scraping_urls = scraping_urls , base_url = base_url , class_id = class_id)


if __name__=="__main__":
    print(*scraping_urls , sep="\n")
    print(len(scraping_urls))