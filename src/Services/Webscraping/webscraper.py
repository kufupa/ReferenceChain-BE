import requests
from bs4 import BeautifulSoup
from newspaper import Article as NewsArticle
from newspaper.article import ArticleException
import os
from urllib.parse import quote_plus
from datetime import datetime

url_base = r"https://www.news.google.com/"
url_search = url_base + r"search?q="

seid = "65b91f9076f514217"
seapi = os.environ.get("SEAPI_KEY")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}


def getTimeStamp(title):
    url = url_search + title.replace(" ", "+")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    time = soup.find("time", {"class": "hvbAAd"})

    if not time:
        return datetime.today()

    return time["datetime"]


def parse(url):
    try:
        article = NewsArticle(url, headers=headers)
        article.download()
        article.parse()
    except ArticleException as e:
        print(e)
        return None, None, None

    title = article.title
    text = article.text
    timestamp = getTimeStamp(title)

    return title, text, timestamp


def make_datetime_month_year(time):
    time = time.split("T")[0].split("-")
    time = time[1] + "-" + time[0]
    return time


def find_volume_articles(soup):
    time_volume = {}

    for article in soup.find_all("time", {"class": "hvbAAd"}):
        # Get the month of publish
        time = make_datetime_month_year(article["datetime"])

        if time in time_volume:
            time_volume[time] += 1
        else:
            time_volume[time] = 1

    return time_volume


def find_articles(topic):
    url = url_search + quote_plus(topic)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    time_volume = find_volume_articles(soup)

    if len(time_volume) == 0:
        return None

    event_time = max(time_volume, key=time_volume.get)

    articles = soup.find_all("article")

    ret_articles = [articles[0]]

    for article in articles:
        if make_datetime_month_year(article.find("time")["datetime"]) == event_time:
            if article not in ret_articles:
                ret_articles.append(article)
                break

    ret = []

    for article in ret_articles:

        title = quote_plus(article.find("button")["aria-label"][7:])

        url = f'https://www.googleapis.com/customsearch/v1?q={title}&cx={seid}&key={seapi}'

        response = requests.get(url, headers=headers)
        data = response.json()

        try:
            for item in data["items"]:
                url = item["link"]
                break
        except KeyError:
            pass

        ret.append(url)

    return ret