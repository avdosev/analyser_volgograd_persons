import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs
from crawler.safe_get import fetch_html


async def download_news(queue):
    site = "https://v102.ru"
    url_form = "https://v102.ru/center_line_dorabotka_ajax.php?page={num}&category={category}"
    category = 0  # maybe need other
    async with aiohttp.ClientSession() as session:
        for i in range(1, 2):
            url = str.format(url_form, num=i, category=category)
            html = await fetch_html(url, session)
            news = parse_news(html)
            articles = await asyncio.gather(
                *[fetch_html(link, session) for link in map(lambda article: site + article['link'], news)]
            )
            text_articles = map(parse_article, articles)
            for new, new_text in zip(news, text_articles):
                new['text'] = new_text
                new['link'] = site + new['link']
            await queue.put(news)


# выдает статьи
def parse_news(news_html):
    html = bs(news_html, 'html.parser')
    articles_elements = html.find_all(class_="new-article")
    articles = []
    for article in articles_elements:
        title = article.h3.get_text()
        date = article.find(class_="mobile-date").get_text()
        link = article.find(class_="detail-link")['href']
        count_comments = article.find(class_="comment-icon").get_text()
        articles.append({
            'title': title,
            'date': date,
            'link': link,
            'count_comments': count_comments,
            'sequences': '',  # предложения для 2 задания
            'tonality': ''  # тональность для 3 задания
        })

    return articles


# Возвращшает распаршенную статью
def parse_article(html_article):
    html = bs(html_article, 'html.parser')
    article_text = html.find(class_='n-text').get_text()
    return article_text
