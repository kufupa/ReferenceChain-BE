import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta



def get_bbc_publish_date(article_url):
    search_url = f"https://www.google.com/search?q={article_url}&tbm=nws"  # Google News search
    print(search_url)

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return f"Failed to fetch search results (Status Code: {response.status_code})"

    soup = BeautifulSoup(response.text, "html.parser")
    
    # print(soup)

    # Find the first search result with a time label (e.g., "5 hours ago", "2 days ago")
    # OSrXXb rbYSKb LfVVr
    time_element = soup.find("div", class_="OSrXXb rbYSKb LfVVr")
    print(time_element)
    if not time_element:
        return "Publish date not found in Google News results"

    time_text = time_element.text.strip()
    
    # Convert "X days ago" into an actual date
    today = datetime.today()
    if "hour" in time_text:
        hours_ago = int(time_text.split()[0])
        publish_date = today - timedelta(hours=hours_ago)
    elif "day" in time_text:
        days_ago = int(time_text.split()[0])
        publish_date = today - timedelta(days=days_ago)
    else:
        return f"Could not parse date: {time_text}"

    return publish_date.strftime("%Y-%m-%d")

# Example Usage
article_url = "https://www.bbc.co.uk/news/live/cn4z119e5xxt"  # Replace with a real BBC article URL
publish_date = get_bbc_publish_date(article_url)
print("Publish Date:", publish_date)
