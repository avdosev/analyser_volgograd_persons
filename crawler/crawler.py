import aiohttp
import asyncio
from bs4 import BeautifulSoup as BS
from safe_get import fetch_html


async def download_news(queue):
    url_form = "https://v102.ru/center_line_dorabotka_ajax.php?page={num}&category={category}"
    category = 0  # maybe need other
    async with aiohttp.ClientSession() as session:
        for i in range(1, 5):
            url = str.format(url_form, num=i, category=category)
            html = await fetch_html(url, session)
            news = await parse_news(html)
            await queue.put(news)


# выдает статьи
async def parse_news(news_html):
    html = BS(news_html, 'html.parser')
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
            'count_comments': count_comments
        })

    return articles


# Возвращшает распаршенную статью
async def parse_article(html_article):
    pass
