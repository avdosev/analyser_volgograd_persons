import subprocess as sub
import sys
sys.path.append("..")
from config import DATA_PATH
import json

path = DATA_PATH
# рекурсивно обходим все подкаталоги папки дата
# загружаем с каждого json text
# для каждого из них создаем output
# создаем файлик input.txt с новым текстом
# получаем output.txt
# сохраняем его где-то еще(надо бы в бд)
import os
print(DATA_PATH)


for address, dirs, files in os.walk(DATA_PATH):
    for file in files:
        if not file.endswith(".json"):
            continue

        with open(os.path.join(address, file)) as myjson:
            data = json.load(myjson)
            text = data['text']

            with open(os.path.join(os.getcwd(), 'input.txt'), 'w') as inputFile:
                inputFile.writelines(text)
                p = sub.Popen(["tomita-parser", "config.proto"], stdout=sub.PIPE, stderr=sub.PIPE)
                out, err = p.communicate()
                print(out)

