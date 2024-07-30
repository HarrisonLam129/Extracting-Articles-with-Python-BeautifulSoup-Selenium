import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd


def get_page(url):
    response = requests.get(url)
    if not response.ok:
        print('Status code:', response.status_code)
        raise Exception('Failed to load page {}'.format(url))
    page_content = response.text
    doc = BeautifulSoup(page_content, 'html.parser')
    return doc


def import_data():
    ft_email = ""
    ft_pw = ""
    for p in range(1,51):
        print(p)
        if p == 1:
            driver = webdriver.Chrome()
            main_page = get_page('https://www.ft.com/hong-kong')
        else:
            main_page = get_page('https://www.ft.com/hong-kong?page=' + str(p))
        a_tags = main_page.find_all('a', {'class': "js-teaser-heading-link"})
        time_tags = main_page.find_all('time', {'class': "o-date"})
        article_text_list = []
        for i in range(len(a_tags)):
            href_tag = a_tags[i].get('href')
            if href_tag.startswith('http'):
                url = href_tag
            else:
                url = 'http://ft.com'+href_tag
            if i == 0 and p == 1:
                login_url = 'https://accounts.ft.com/login?location=https%3A%2F%2Fwww.ft.com%2Fcontent%2F'+href_tag[9:]
                driver.get(login_url)
                time.sleep(1)
                while not driver.find_element(By.NAME, "email"):
                    time.sleep(1)
                driver.find_element(By.NAME, "email").send_keys(ft_email)
                driver.find_element(By.ID, "enter-email-next").click()
                time.sleep(5)
                while not driver.find_element(By.ID, "sso-redirect-button"):
                    time.sleep(1)
                driver.find_element(By.ID, "sso-redirect-button").click()
                time.sleep(5)
                while not driver.find_element(By.NAME, "loginfmt"):
                    time.sleep(1)
                driver.find_element(By.NAME, "loginfmt").send_keys(ft_email)
                driver.find_element(By.ID, "idSIButton9").click()
                time.sleep(5)
                while not driver.find_element(By.NAME, "passwd"):
                    time.sleep(1)
                driver.find_element(By.NAME, "passwd").send_keys(ft_pw)
                driver.find_element(By.ID, "idSIButton9").click()
                input("Press the Enter key to continue: ")
                driver.find_element(By.ID, "KmsiCheckboxField").click()
                driver.find_element(By.ID, "idSIButton9").click()
                driver.find_element(By.ID, "_shib_idp_rememberConsent").click()
                driver.find_element(By.NAME, "_eventId_proceed").click()
                time.sleep(5)
                driver.find_element(By.CLASS_NAME, "o-cookie-message__button").click()
                time.sleep(5)
            driver.get(url)
            article = BeautifulSoup(driver.page_source, 'html.parser')
            paragraphs = article.find_all('p', {'class': None})
            article_text = ''
            for j in range(len(paragraphs)):
                article_text += paragraphs[j].text + ' '
            print(article_text)
            article_text_list.append(article_text)
        return time_tags, a_tags, article_text_list

    """
    doc = get_page('https://www.scmp.com/news/hong-kong/hong-kong-economy')
    a_tags = doc.find_all(['a','a'], {'class': ["article__link","article-title__article-link article-hover-link"]})
    time_tags = doc.find_all('span', {'class': "author__status-left-time"})

    driver = webdriver.Chrome()
    url = 'https://www.techinasia.com/tag/hong-kong'
    driver.get(url)
    for i in range(30):
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(3)
        doc = BeautifulSoup(driver.page_source, 'html.parser')
    a_tags = doc.find_all('h2', {'class': "jsx-2737968273"})
    for i in range(len(a_tags)):
        a_tags[i] = a_tags[i].findChildren('a', recursive=False).pop()
    time_tags = doc.find_all('time', {'class': "jsx-3825207150 time inline-block"})

    driver = webdriver.Chrome()
    url = 'https://www.thestandard.com.hk/section-news-list/section/finance/'
    driver.get(url)
    for i in range(50):
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        driver.find_element(By.CLASS_NAME, "show-more").click()
        time.sleep(3)
        doc = BeautifulSoup(driver.page_source, 'html.parser')
    a_tags = doc.find_all('li', {'class': "caption"})
    for i in range(len(a_tags)):
        a_tags[i] = a_tags[i].findChildren('h1', recursive=False).pop()
        a_tags[i] = a_tags[i].findChildren('a', recursive=False).pop()
    time_tags = doc.find_all('li', {'class': "caption"})
    for i in range(len(time_tags)):
        time_tags[i] = time_tags[i].findChildren('span', recursive=False).pop()
    """


def import_data2():
    driver = webdriver.Chrome()
    driver.get('https://www.cnbc.com/search/?query=tencent&qsearchterm=tencent')
    time.sleep(5)
    driver.find_element(By.ID, "sortdate").click()
    time.sleep(3)
    for i in range(40):
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(3)
        doc = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(3)
    a_tags = doc.find_all('div', class_="SearchResult-searchResultTitle")
    print(len(a_tags))
    titleList = []
    dateList = []
    article_text_list = []
    for i in range(1,len(a_tags)):
        print(i)
        driver.get(a_tags[i].findChild('a').get('href'))
        try:
            title = driver.find_element(By.XPATH, '//*[@id="main-article-header"]/div/div[1]/div[1]/h1')
            date = driver.find_element(By.XPATH, '//*[@id="main-article-header"]/div/div[1]/div[2]/time[1]')
        except NoSuchElementException:
            print('No title/date')
            continue
        try:
            text_group = driver.find_element(By.CLASS_NAME, 'group')
            text = ''
            for para in text_group.find_elements(By.XPATH, '*'):
                text += para.text + ' '
        except NoSuchElementException:
            print('No content')
            continue
        titleList.append(title.text)
        date = date.get_attribute("datetime")
        dateList.append(date.split('T')[0])
        article_text_list.append(text)
    return dateList, titleList, article_text_list


def store_data(date, title, text, name):
    data = pd.DataFrame(
        {'Date': date,
         'Title': title,
         'Text': text})
    data.to_csv(name, index=False)


"""
dates, titles, texts = import_data()
store_data(dates, titles, texts, 'FTnews.csv')

dates, titles, texts = import_data2()
store_data(dates, titles, texts, 'aastocks.csv')
"""
