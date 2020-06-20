PATH = 'model/kurs_model/'

from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2VecModel
from pprint import pprint
import word2vec
import os
import sys
sys.path.append("..")
from dbconfig import TABLE_NAME, DATABASE_NAME
from dbmodel import Connection, Mongo


conn = Connection().getConnection()
mongo = Mongo(conn, DATABASE_NAME)


def save_text_db_to_txt(save_to_one_file=False, filename_base = "./data_text/main_text"):
    if (not os.path.exists('data_text')):
        os.mkdir('data_text')
        print("Папка создана")
    with conn:
        # Сохраняем в файлы для обучения модели
        for i, el in enumerate(mongo.fetchall()):
            if save_to_one_file:
                filename = f'{filename_base}.txt'
                output_file = open(filename, 'a', encoding="utf-8")
            else:
                filename = f'{filename_base}_{i}.txt'
                output_file = open(filename, 'w')
            output_file.write(el[0])
            output_file.close()


def main():
    if not os.path.exists('model'):
        save_txt.save_text_db_to_txt()
        word2vec.create_w2v_model()


    with SparkSession.builder.appName("SimpleApplication").getOrCreate() as spark_session:
        model = Word2VecModel.load(PATH)

        persons = mongo.selectAll('persons')
        places = mongo.selectAll('places')

        pprint("Поиск контекстных синонимов персон:")
        persons_synonyms = word2vec.find_synonyms(persons, model, spark_session)
        pprint(persons_synonyms)

        pprint("Поиск контекстных синонимов достопримечательностей:")
        places_synonyms = word2vec.find_synonyms(places, model, spark_session)
        pprint(places_synonyms)


if __name__ == '__main__':
    main()
