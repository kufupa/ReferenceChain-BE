import os
from source_gen import get_sources
import datetime
import requests, urllib.parse
from article import Article
from sentiment import Sentiment
from newspaper import Article as NewsArticle


# run "export NEWS_API_KEY=''" in terminal (and for ci will work automatically)

sources = get_sources()
language = 'en'

# Init
key = os.getenv('NEWS_API')

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

# Given a query, return articles relevant to it
def getArticleFromApi(query, dateFrom=None, dateTo=None):
  
  if dateFrom is not None or dateTo is None:
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    if dateFrom is None:
      dateFrom = "2025-01-01"
    if dateTo is None:
      dateTo = today

  # con = http.client.HTTPSConnection('api.thenewsapi.com')

  query_base = "https://api.thenewsapi.com/v1/news/all?"

  params = urllib.parse.urlencode({
      'api_token': key,
      'search': query,
  })

  # print(params)
  print(query_base + params)

  response = requests.get(query_base + params)

  if response.status_code != 200:
    print(f"Failed to fetch the page, status code: {response.status_code}")
    return None
  else:
    data = response.json()
    content = data["data"]

    articles = []

    for article in content:
      title = article["title"]
      url = article["url"]
      keywords = article["keywords"]
      time = article["published_at"]
      if "similar" in article:
        similar = article["similar"]

      # convert time to datetime
      time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")

      # get article text using newspaper
      newspaper_article = NewsArticle(url)
      newspaper_article.download()
      newspaper_article.parse()
      text = newspaper_article.text


      new_article = Article(text, keywords, Sentiment.POSITIVE, time, url, title)
      articles.append(new_article)
    
    return articles