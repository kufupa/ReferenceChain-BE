import requests

def get_sources():
    query = r"https://newsapi.org/v2/top-headlines/sources?apiKey=c6b6ad1b7b3541138043e3f9f72750e7"

    response = requests.get(query)

    if response.status_code == 200:
        data = response.json()
        sources = data["sources"]
        string = ""
        for source in sources:
            if source["language"] == 'en':
                string += source["id"] + ","

        return string[:-1]
    else:
        return ""