PATH = 'data_text/*.txt'

from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import Word2Vec
import re
import string
import datetime


def find_synonyms(elements, model, spark_session, count=5):
    result = []
    for element in elements:
        try:
            elementDF = spark_session.createDataFrame(
                [(element[0].lower().split(" "),)], 
                ["words"])
            transform_elem = model.transform(elementDF)
            synonyms = model.findSynonyms(transform_elem.collect()[0][1], count).collect()
            result.append(synonyms)
        except Exception:
            result.append([])

    return result


def remove_punctuation(text):
    """
    Удаление пунктуации из текста
    """
    return text.translate(str.maketrans('', '', string.punctuation))


def get_only_words(tokens):
    """
    Получение списка токенов, содержащих только слова
    """
    return list(filter(lambda x: re.match('[а-яА-Я]+', x), tokens))


def create_w2v_model():
    spark = SparkSession \
        .builder \
        .appName("SimpleApplication") \
        .config("spark.executor.memory", "2g") \
        .config("spark.driver.memory", "2g") \
        .config("spark.memory.offHeap.enabled", True) \
        .config("spark.memory.offHeap.size", "2g") \
        .getOrCreate()

    input_file = spark.sparkContext.wholeTextFiles(PATH)

    print("""
    
    Подготовка данных (1)...
    
    """)
    prepared_data = input_file.map(lambda x: (x[0], remove_punctuation(x[1])))

    print("""
    
    Подготовка данных (2)...
    
    """)
    df = prepared_data.toDF()

    print("""
    
    Подготовка данных (3)...
    
    """)
    prepared_df = df.selectExpr('_2 as text')

    print("""
    
    Разбитие на токены...
    
    """)
    tokenizer = Tokenizer(inputCol='text', outputCol='words')
    words = tokenizer.transform(prepared_df)

    print("""
    
    Очистка от стоп-слов...
    
    """)
    stop_words = StopWordsRemover.loadDefaultStopWords('russian')
    remover = StopWordsRemover(inputCol="words", outputCol="filtered", stopWords=stop_words)

    print("""
    
    Построение модели...
    
    """)
    word2Vec = Word2Vec(vectorSize=50, inputCol='words', outputCol='result', minCount=2)
    model = word2Vec.fit(words)

    print("""
    
    Сохранение модели...
    
    """)
    today = datetime.datetime.today()
    model_name = today.strftime("model/kurs_model")
    print("""
    
    Model  """ + model_name + """  saved
    
    """)
    model.save(model_name)

    spark.stop()
