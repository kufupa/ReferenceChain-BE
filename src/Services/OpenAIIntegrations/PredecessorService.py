# from src.Services.OpenAIIntegrations.OpenAIQueryService import OpenAIGetArticlePredecessors
# from src.Services.OpenAIIntegrations.OpenAIAdapter import parseJson
# from src.Services.OpenAIIntegrations.ArticleToOAIJsonAdapter import ArticleToJsonAdapter
# from src.Models.articlenode import ArticleNode

# def query(article: ArticleNode):
#     jsonArticle = ArticleToJsonAdapter(article)
#     jsonData = OpenAIGetArticlePredecessors(str(jsonArticle))
#     queryResults = parseJson(jsonData)
#     return queryResults


# def main():

#     newArti = ArticleNode("Putin declares war on Ukraine",
#                       'Since the invasion began on 24 February 2022, the Russian government and media outlets have consistently used the term “special military operation” to refer to the attacks on its neighbour’s territory. Russia made extensive efforts to refrain from labelling the military conflict in Ukraine a war.',
#                       "2025-02-01T12:28:31Z",
#                       "stub",
#                           0,
#                           10)
#     print(query(newArti))

# if __name__ == '__main__':
#     main()
