import subprocess
from crawler import config as cfg
import os


path = cfg.DATA_PATH
# рекурсивно обходим все подкаталоги папки дата
# загружаем с каждого json text
# для каждого из них создаем output

tree = os.walk('test')
print(tree)

print(subprocess.check_output(["ls"]))

