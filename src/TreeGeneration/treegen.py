from src.Models.articlenode import ArticleNode
from src.Services.Webscraping.webscraper import parse, find_articles
import threading


def build_reg_tree(root: str, roots: list[ArticleNode]):
    title, text, timestamp = parse(root)
    rootNode = ArticleNode(title, text, timestamp, root, 0, 0)

    roots.append(rootNode)

    # generate 1 generations of predecessors
    node = rootNode
    for i in range(1):

        print("Generating predecessors")

        if not node.find_predecessors(3):
            break
        node = node.predecessors[0]
    
    # print(rootNode.get_potential_future())


def explore_new_node(root: str, roots: list[ArticleNode]):
    title, text, timestamp = parse(root)
    rootNode = ArticleNode(title, text, timestamp, root, 0, 0)

    print("Checking includes with ", root)
    for node in roots:
        if node.includes(rootNode):
            print("we are so back")
            node.explore_further(root)
            break
    else:
        roots.append(rootNode)
        build_reg_tree(root, roots)
    
# roots = []
# build_reg_tree("https://www.bbc.co.uk/news/articles/cdrye506z1go", roots)

# print("Built")

# preds = roots[-1].find_predecessors_2("https://www.bbc.co.uk/news/articles/cdrye506z1go")

# combined = {"nodes": []}
# for node in preds:
#     combined["nodes"].append(node.to_client())
#     thread = threading.Thread(target=node.get_new_preds)
#     thread.start()

# print(combined)