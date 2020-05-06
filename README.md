# Анализатор волгоградских персон
Проект разделен на три части:

## Парсер сайта и web-интерфейс.

Краулер должен считывать новостную ленту с первой 
страницы сайта. Периодичность повторения устанавливается пользователем. Данные 
заполняются в БД MongoDB. 
Обязательные поля для текста новости:
- Название новости
- Дата новости
- Ссылка на новость
- Текст новости
- Ссылка на видео (если есть)
- Количество просмотров новости (если есть)
- Количество комментариев новости (если есть)

При учередном проходе краулера для существующих в БД новостей (определяется по -
Название новости, Дата новости, Ссылка на новость) поля количества просмотров и
комментариев обновляются. \
Сайт с которого берутся все данные - https://v102.ru/

### Запуск парсера на linux

Для запуска обязательна версия python `3.7+`
```
python3.7 crawler/main.py
```

Он сохранит новости в json файлы в каталоге `data/<datetime>`


##  Программный модуль для анализа новостей из БД. 

Выделить с помощью Томита-
парсера упоминание в тексте значимых персон Волгоградской области и
достопримечательностей. Зафиксировать в БД предложения с их упоминанием для
дальнейшего анализа тональности.
Создать программный модуль для проведения с помощью Spark MlLib анализ модели
word2vec на всем объеме новостных статей из БД. Для персон Волгоградской области и
достопримечательностей определить контектные синонимы и слова, с которыми они
упоминались в тексте. 

Персоны https://global-volgograd.ru/person \
Достопримечательности https://avolgograd.com/sights?obl=vgg

### Установка tomita
Ставим софт
```
apt-get update
apt-get install build-essential cmake lua5.2 unzip
```
Собираем томиту
```
cd ~
git clone https://github.com/yandex/tomita-parser
cd tomita-parser && mkdir build && cd build
cmake ../src/ -DCMAKE_BUILD_TYPE=Release
make
    
```
Выполняем из папки build
```  
wget https://github.com/yandex/tomita-parser/releases/download/v1.0/libmystem_c_binding.so.linux_x64.zip
unzip libmystem_c_binding.so.linux_x64.zip
rm libmystem_c_binding.so.linux_x64.zip
```
Экспортируем томиту
```
export PATH="$HOME/tomita-parser/build/bin:$PATH"
source ~/.bashrc
```
Запускаем
```
python3.7 crawler/main.py
```


## Программный модуль для выявления тональности высказываний по отношению к
персонам Волгоградской области и достопримечательностям.

Можно использовать либо подход на основе правил и словарей, либо методы машинного
обучения.


### Для разработчиков

Добавим памяти, мне 10гб будет мало
```
vagrant plugin install vagrant-disksize
vagrant init ubuntu/bionic64
```
Вставляем строчку в `vagrantvile` `config.disksize.size = '50GB'`

Из стандартного репозитория питон с обвязкой весит колоссально много(около 4гб), но скачаем все же его, он отлично работает.
```
sudo apt-get install python 3.7
python3.7 -m pip install -U pip
python3.7 -m pip3 install -r requrements.txt 

sudo apt install -y mongodb
sudo systemctl status mongodb
```


