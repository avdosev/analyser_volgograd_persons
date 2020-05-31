import json
import os
from datetime import datetime

def writeJSON(dirname, jsonObject):
    print(f"Пишем в файл {dirname}")
    path = os.path.join(dirname, f"{datetime.now().strftime('%Y-%m-%H %H-%M-%S')}")
    os.mkdir(path)

    for news in jsonObject:
        filepath = os.path.join(path, news['title'].replace(":", " -") + ".json")
        fixedFilepath = filepath
        with open(fixedFilepath, 'w') as f:
            json.dump(news, f, indent=4, ensure_ascii=False)
            print(f"Сохраняем новость: {news['title']}")
            f.close()