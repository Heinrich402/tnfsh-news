import requests
from bs4 import BeautifulSoup
import datetime

def news():
    url = 'https://www.tnfsh.tn.edu.tw/latestevent/index.aspx?Parser=9,3,19'
    response = requests.get(url)
    news_links = []
    whole_news = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        list_items = soup.find_all('li')

        today = datetime.date.today()

        for item in list_items[1:]:
            date_elements = item.find_all('span', class_='w15 hidden-xs')
            if len(date_elements) > 1:
                date_str = date_elements[1].text.strip()
                try:
                    news_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    if news_date == today:
                        news_link = item.find('a')['href']
                        news_links.append(news_link)
                except ValueError:
                    pass
        for i in news_links:
            today_url = 'https://www.tnfsh.tn.edu.tw/latestevent/' + i
            response = requests.get(today_url)
            if response.status_code == 200:
                tnfsh = BeautifulSoup(response.text, 'html.parser')
                findtitle = tnfsh.find('div', class_='content_title')
                finddate = tnfsh.find('span', class_="content_date")
                findunit = tnfsh.find('label', string='公布單位')
                title = findtitle.text if findtitle else "未找到標題"
                date = finddate.text if finddate else "未找到時間"
                unit = findunit.next_sibling.strip().replace('：', '') if findunit else "未找到單位"
                p = tnfsh.find('div', class_='content_txt').find_all('p')
                paragraphs = '\n'.join([paragraph.text for paragraph in p]) if p else "未找到內文"

                news = title + '\n公布單位：　' + unit + '\n發布時間：　' + date + '\n' + paragraphs + '\n文章網址：' + today_url + '\n\n=====文章分割線=====\n\n'
                whole_news += news
    else:
        print(f'無法取得網頁內容，錯誤代碼：{response.status_code}')

    return ''.join(whole_news)[:-19] if whole_news else "沒有新通知"