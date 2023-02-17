import json
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import fake_useragent


def get_first_news():
    url = 'https://www.securitylab.ru/news/'
    ua = fake_useragent.UserAgent()
    headers = {
        'User-agent': ua.random}
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    all_articles = soup.findAll('a', class_='article-card inline-card')

    news_dict= {}
    for article in all_articles:
        news_name = article.find('h2', class_='article-card-title').text
        news_description = article.find('p').text
        news_time = article.find('time').get('datetime')
        date_from_iso = datetime.fromisoformat(news_time)
        date_time =datetime.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')
        news_datetime = time.mktime(datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').timetuple())


        news_url = f'https://www.securitylab.ru{article.get("href")}'
        news_id = news_url.split('/')[-1]
        news_id = news_id[:-4]

        news_dict[news_id] = {
            'time': news_datetime,
            'name': news_name,
            'description': news_description,
            'url': news_url
         }
    with open('news.json', 'w', encoding='utf-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False, )

def check_news_update():
    with open('news.json', encoding='utf-8') as file:
        news_dict = json.load(file)

    # login = 'gLhpob'
    # password = 'F7aYVW'
    # proxies = {'https': f'http://{login}:{password}@185.184.78.198:9248'}

    url = 'https://www.securitylab.ru/news/'
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    all_articles = soup.findAll('a', class_='article-card inline-card')
    fresh_dict = {}
    for article in all_articles:
        news_url = f'https://www.securitylab.ru{article.get("href")}'
        news_id = news_url.split('/')[-1]
        news_id = news_id[:-4]

        if news_id in news_dict:
            continue
        else:
            news_name = article.find('h2', class_='article-card-title').text
            news_description = article.find('p').text
            news_time = article.find('time').get('datetime')
            date_from_iso = datetime.fromisoformat(news_time)
            date_time = datetime.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')
            news_datetime = time.mktime(datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').timetuple())


            news_dict[news_id] = {
                'time': news_datetime,
                'name': news_name,
                'description': news_description,
                'url': news_url
            }

            fresh_dict[news_id] = {
                'time': news_time,
                'name': news_name,
                'description': news_description,
                'url': news_url
            }
    with open('news.json', 'w', encoding='utf-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False, )

    return fresh_dict
def main():
    #get_first_news()
    check_news_update()
    print(check_news_update())

if __name__ == '__main__':
    main()
