PATH = 'model/kurs_model/'

from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2VecModel
from pprint import pprint

test_words = ["дом", "бочаров", "документ", "деньги", "гараж", "волга", "дума", "закон", "полиция", "врач"]

spark = SparkSession \
    .builder \
    .appName("SimpleApplication") \
    .getOrCreate()

model = Word2VecModel.load(PATH)

pprint("Контекстные синонимы слов, полученные из модели, обученной на статьях:")

for test_word in test_words:
    pprint("-"*20)
    pprint(test_word)
    result = model.findSynonyms(test_word, 5).collect()
    for el in result:
        pprint(el[0])

spark.stop()