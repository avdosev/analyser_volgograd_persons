PATH = 'model/kurs_model/'

from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2VecModel
from pprint import pprint
import save_txt
import word2vec
import os
import sys
sys.path.append("..")
from dbconfig import TABLE_NAME, DATABASE_NAME
from dbmodel import Connection, Mongo



def get_synonyms(elements, count, model, spark_session):
    result = []
    for element in elements:
        try:
            elementDF = spark_session.createDataFrame([
                (element[0].lower().split(" "),)], ["words"])
            transform_elem = model.transform(elementDF)
            synonyms = model.findSynonyms(transform_elem.collect()[0][1], count).collect()
            result.append(synonyms)
        except Exception:
            result.append("Синонимы не найдены")

    return result


def print_elem(elements, elements_synonyms):
    for i in range(len(elements_synonyms)):
        pprint("-" * 30)
        pprint(elements[i][0])
        for el in elements_synonyms[i]:
            print(el[0])




def main():
    conn = Connection().getConnection()
    mongo = Mongo(conn, DATABASE_NAME)

    if (not os.path.exists('model')):
        if (not os.path.exists('data_text')):
            os.mkdir('data_text')
            print("Папка создана")
        save_txt.save_text_db_to_txt(mongo)

        word2vec.create_w2v_model()


    spark = SparkSession.builder.appName("SimpleApplication").getOrCreate()
    model = Word2VecModel.load(PATH)

    pprint("Поиск контекстных синонимов персон:")
    persons_synonyms = get_synonyms(persons, 5, model, spark)

    pprint("Поиск контекстных синонимов достопримечательностей:")
    places_synonyms = get_synonyms(places, 5, model, spark)

    spark.stop()


if __name__ == '__main__':
    main()
