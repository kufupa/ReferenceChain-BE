#OpenAIJsonAdapter
import datetime
import json
from typing import *

DTF = "%d-%m-%Y"

def parseJson(jsonString):

    data = json.loads(jsonString)
    data["predecessors"] = list(map(lambda x: (x[0], x[1]), data["predecessors"]))

    return data


# if second arg is null, this means datetime is present/unfinished as of now
def parseEventTimeline(timeString) -> Tuple[datetime, Optional[datetime]]:
    t1, t2 = timeString.split(':')

    dt2 = None
    if t2 != "Present":
        dt2 = datetime.datetime.strptime(t2, DTF)

    return datetime.datetime.strptime(t1, DTF), dt2