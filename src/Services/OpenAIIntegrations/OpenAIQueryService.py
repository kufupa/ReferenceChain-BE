from openai import OpenAI
import os
from src.Services.OpenAIIntegrations.OpenAIAdapter import parseJson


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def OpenAIGetArticlePredecessors(content, depth=0):
    if depth > 5:
        print("crying rn")
        return None

    response = (client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "Your goal is to respond with a list of events. You will be provided"
                        "with information in the format: "

                        "{title:'...',"
                        "content:'...',"
                        "publish_date:'...'"
                        "}. '"

                        "You must then respond with a list in the format: "

                        "event1|event2|event3|... "
                        "the events should be ordered from oldest to newest. "
                        "the events should be names of important events that preceded and in some way "
                        "caused the event on which the content sent is about. For example, 'Trump innaugurated "
                        "as 47th president of United States' may have predecessor 'Trump beats Harris in 2024 election' "
                        ". Crucially, try to keep predecessors one logical level of implication "
                        "backwards, rather than several. So for example, 'Battle of the Somme' may not have 'Assasination "
                        "of Franz Ferdinand' as a predecessor, but it may be linked maybe 5-6 levels back. "
             ,
        },
            {"role": "user", "content": str(content)}
        ],
        temperature=0
    ))

    try:
        ret = response.choices[0].message.content.split("|")
    except:
        return OpenAIGetArticlePredecessors(content, depth + 1)

    return ret


def OpenAIGetArticleSucessors(content, depth=0):
    if depth > 5:
        return None


    response = (client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "Your goal is to respond with information in a Json format. You will be provided "
                        "with information in the format: "

                        "{title:'...',"
                        "content:'...',"
                        "publish_date:'...'"
                        "}. '"

                        "You must then respond with a Json of the format: "

                        "event1|event2|event3|..."

                        "sucessors must be a list of strings. "
                        "The strings should be names of important events that suceeded and in some way were "
                        "directly caused by the given event. If there exist no such sucessors (ie if the event "
                        "is too recent), then just return sucessors as an empty list. For example, Japan leaving "
                        "the League of Nations was a direct sucessor to the Manchurian Crisis, and so you would "
                        "return 'japan leaves the league of nations' if the input content is 'manchurian crisis'."

             },
            {"role": "user", "content": str(content)}
        ],
        temperature=0
    ))

    try:
        ret = parseJson(response.choices[0].message.content)["sucessors"]
    except:
        return OpenAIGetArticlePredecessors(content, depth + 1)

    return ret

def OpenAIGetFuture(content):
    response = (client.chat.completions.create(
        model="o3-mini",
        messages=[
            {"role": "system",
             "content": "Your goal is to respond with short, concise news headlines, and provide some content for this news."
                        "Give your output in this 3 section format:"
                        "Headline:,"
                        "Content:,"
                        "Evidence:,"
                        "You must also provide suitable evidence for the news headline and content that you provide."
                        "You will be given a list of news articles. These articles are in such"
                        "a way that one event is followed by the other, and therefore one is a direct cause of the other,"
                        "forming a chain (or multiple chains leading up to a main event) this way. You must read through these"
                        "articles, and the headline/content you return must be caused by and follow the latest event from these articles"
                        "Do your best to make the response as rooted in world events occuring at "
                        "the time of the latest news article as possible, and make sure the evidence you base on is from these articles."
                        "In the content you provide, clearly show where you have used the evidence provided to you."
                        "Evidence should have links that were provided to you."
             },
            {"role": "user", "content": str(content)}
        ]
    ))

    return response.choices[0].message.content