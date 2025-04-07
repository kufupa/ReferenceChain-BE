import datetime
import uuid
from src.Services.OpenAIIntegrations.OpenAIQueryService import OpenAIGetArticlePredecessors, OpenAIGetArticleSucessors, OpenAIGetFuture
from src.Services.Webscraping.webscraper import parse, find_articles

class ArticleNode:

    def __init__(self, title: str, content: str, timestamp: datetime.datetime, link: str, depth: int, significance: int):
        self.title = title
        self.id = uuid.uuid4()
        self.content = content
        self.timestamp = timestamp
        self.link = link
        self.predecessors = []
        self.successors = []
        self.depth = depth
        self.significance = significance
        self.future = None

        print(self)

        # TODO: tell client about new node

    def toJson(self):
        return {
            "title": self.title,
            "content": self.content,
            "publish_date": self.timestamp
        }

    def find_predecessors(self, num_preds=1):
        preds = OpenAIGetArticlePredecessors(self.toJson())

        if preds is None:
            return False

        for i in range(min(num_preds, len(preds))):
            urls = find_articles(preds[i])

            if not urls:
                continue

            time_url = urls[min(1, len(urls) - 1)]
            title, content, publishDate = parse(time_url)
            if title is not None:
                article = ArticleNode(title, content, publishDate, time_url, 0, 0)

                if article != self and article not in self.successors and article not in self.predecessors:
                    article.successors.append(self)
                    self.predecessors.append(article)
        
        return len(self.predecessors) > 0

    def find_sucessors(self, num_sucs=1):
        sucs = OpenAIGetArticleSucessors(self.toJson())
        if sucs is None:
            return False

        sucs.sort(key=lambda x: x[1], reverse=True)
        for i in range(min(num_sucs, len(sucs))):
            urls = find_articles(sucs[i][0])

            if not urls:
                continue

            time_url = urls[min(1, len(urls) - 1)]
            title, content, publishDate = parse(time_url)
            if title is not None:
                article = ArticleNode(title, content, publishDate, time_url, 0, sucs[i][1])

                if article != self and article not in self.successors and article not in self.predecessors:
                    article.predecessors.append(self)
                    self.successors.append(article)
        
        return len(self.successors) > 0

    def get_potential_future(self):
        return OpenAIGetFuture(self.url_list())

    def includes(self, other):
        print("Checking includes for ", self.link)
        if self.link == other.link:
            return True
        for p in self.predecessors:
            if p.includes(other):
                return True
        
        return False
    
    def explore_further(self, link, path=False):
        if self.link == link:
            if len(self.predecessors) >= 3:
                self.predecessors[1].explore_further(self.predecessors[1].link, path=True)
            else:
                self.find_predecessors(3 - len(self.predecessors))
                self.predecessors[-1].find_predecessors(2)
        else:
            if path:
                self.find_predecessors(3 - len(self.predecessors))
            else:
                for node in self.predecessors:
                    node.explore_further(link)

    def to_client(self):
        baseJson = self.toJson()
        baseJson["id"] = self.id
        baseJson["url"] = self.link
        preds_list = [p.id for p in self.predecessors]
        baseJson["predecessors"] = preds_list
        if len(self.successors) > 0:
            baseJson["parent"] = self.successors[0].id
        return baseJson
    
    def find_predecessors_2(self, link: str):
        if self.link == link:
            return self.predecessors
        for p in self.predecessors:
            v = p.find_predecessors_2(link)
            if v is not None:
                return v
        return None
    
    def get_new_preds(self):
        self.find_predecessors(3 - len(self.predecessors))
        for p in self.predecessors:
            p.find_predecessors(1 - len(p.predecessors))

    def url_list(self):
        curList = [self.link]
        for node in self.predecessors:
            curList.extend(node.url_list())

        return curList


    def __repr__(self):
        string = "\n--------------\n"
        string += f"Headline: {self.title}\n"
        string += f"Published: {self.timestamp}\n"
        string += f"Link: {self.link}\n"
        string += "\n--------------\n"

        return string
    
    def __eq__(self, other):
        if other is not ArticleNode:
            return False
        return self.link == other.link
    
    def __hash__(self):
        return hash(self.link)
    