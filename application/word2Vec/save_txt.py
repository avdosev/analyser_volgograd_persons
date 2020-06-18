def save_text_db_to_txt(con, save_to_one_file=False, filename_base = "./data_text/main_text"):
    with con:
        cur = con.cursor()
        # Берем тексты статей из БД
        cur.execute("SELECT text FROM storage WHERE text IS NOT NULL")

        # Сохраняем в файлы для обучения модели
        for i, el in enumerate(cur.fetchall()):
            if save_to_one_file:
                filename = f'{filename_base}.txt'
                output_file = open(filename, 'a', encoding="utf-8")
            else:
                filename = f'{filename_base}_{i}.txt'
                output_file = open(filename, 'w')
            output_file.write(el[0])
            output_file.close()
