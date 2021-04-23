import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException


class InstagramBot():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("C:/Users/Компьютер/PycharmProjects/InstaBot/chromedriver")

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):

        try:
            browser = self.browser
            browser.get('https://www.instagram.com/')
            time.sleep(random.randrange(3, 5))

            username_input = browser.find_element_by_name('username')
            username_input.clear()
            username_input.send_keys(username)

            time.sleep(2)
            password_input = browser.find_element_by_name('password')
            password_input.clear()
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)

            time.sleep(5)

        except Exception as ex:
            print(ex)
            self.close_browser()

    def hashtag_search(self, hashtag):
        browser = self.browser
        self.login()
        try:
            browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            time.sleep(5)

            posts_url = []
            for i in range(1, 10):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
                for href in hrefs:
                    posts_url.append(href)
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(random.randrange(4, 6))
                print(f'Итерация: {i}')
            set_posts_url = set(posts_url)
            set_posts_url = list(set_posts_url)
            print(len(set_posts_url))

            for url in set_posts_url:
                browser.get(url)
                time.sleep(5)
                like_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                print(f'Лайк {url} поставлен')
                time.sleep(random.randrange(80, 100))

        except Exception as ex:
            print(ex)
            self.close_browser()

    # проверяем существует ли элемент на странице
    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # лайк по прямой ссылке
    def put_exactly_like(self, userpost):
        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print('Поста не существует')
            self.close_browser()
        else:
            print('Лойс')
            time.sleep(3)

            like_button = '/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button'
            browser.find_element_by_xpath(like_button).click()

    # ставим лайки по ссылке пользователя
    def put_random_likes(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пользователь успешно найден, ставим лайки!")
            time.sleep(2)
            post_count = '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span'
            loops_count = int(int(browser.find_element_by_xpath(post_count).text) / 12)
            if loops_count > 4:
                loops_count = 4

            posts_url = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_url.append(href)
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(random.randrange(3, 5))
                print(f'Итерация: {i}')

            set_posts_url = set(posts_url)
            set_posts_url = list(set_posts_url)
            print(len(set_posts_url))

            for post in set_posts_url[0:6]:
                try:
                    browser.get(post)
                    time.sleep(3)

                    like_button = '/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button'
                    browser.find_element_by_xpath(like_button).click()
                    time.sleep(random.randrange(80, 100))

                except Exception as ex:
                    print(ex)
                    self.close_browser()

    def get_all_followers(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(5)
        file_name = userpage.split("/")[-2]
        # создаем папку с именем пользователя
        if os.path.exists(f"{file_name}"):
            print(f"Папка {file_name} уже существует")
        else:
            print(f"Создаем папку пользователя {file_name}")
            os.mkdir(file_name)

        # проверяем существование пользователя
        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f"Пользователя {file_name} не существует, проверьте URL")
            # self.close_browser()

        else:
            print(f"Пользователь {file_name} успешно найден, начинаем скачивать подписчиков!")
            time.sleep(2)

            # смотрим количество подписчиков
            followers_button = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
            followers_count = followers_button.get_attribute('title')
            # followers_count = int(followers_count.split(' ')[0])
            # если количество подписчиков больше 999, убираем из числа запятые
            if ' ' in followers_count:
                followers_count = int(''.join(followers_count.split(' ')))
            else:
                followers_count = int(followers_count)

            print(f'Количество подписчиков: {followers_count}')
            time.sleep(2)
            loops_cont = int(followers_count / 12)
            print(f"Число итераций: {loops_cont}")

            followers_button.click()
            time.sleep(4)
            followers_ul = browser.find_element_by_xpath(
                "/html/body/div[5]/div/div/div[2]")
            try:
                followers_urls = []
                # # скроллим подписчиков
                # for i in range(1, loops_cont + 1):
                #     browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_url)
                #     time.sleep(random.randrange(3, 5))
                #     print(f'Итерация {i}')
                #all_urls_div = browser.find_elements_by_tag_name('li')

                # сохраняем ссылки на страницы в список
                all_urls_div = followers_ul.find_elements_by_tag_name("li")

                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                # сохраняем ссылки на страницы в файл
                with open(f'{file_name}/{file_name}.txt', 'a') as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

                with open(f'{file_name}/{file_name}.txt') as text_file:
                    users_urls = text_file.readlines()

                    for user in users_urls:
                        try:
                            try:
                                # файл с пролайкаными пользователями
                                with open(f'{file_name}/{file_name}_like_list.txt', 'r') as like_list_file:
                                    lines = like_list_file.readlines()
                                    # если пользователь был пролайкан, переходим к следующему
                                    if user in lines:
                                        print(f'Мы уже лайкали {user}, переходим к следующему')
                                        continue

                            except Exception as ex:
                                print('Файл со ссылками еще не создан')

                            browser = self.browser
                            browser.get(user)
                            page_owner = user.split("/")[-2]

                            if self.xpath_exists('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/a'):
                                print('Это наш профиль')
                                continue
                            elif self.xpath_exists('/html/body/div[1]/section/main/div/div/article/div[1]/div/h2'):
                                print(f'Это закрытый аккаунт {user}')
                                continue
                            else:
                                # лайкаем аккаунт
                                self.put_random_likes(user)

                            # записываем в файл аккаунт который лайкали
                            with open(f'{file_name}/{file_name}_like_list.txt', 'a') as like_list_file:
                                like_list_file.write(user)

                        except Exception as ex:
                            print(ex)

            except Exception as ex:
                print(ex)
                self.close_browser()


bot = InstagramBot(username, password)
# bot.hashtag_search("hashtag")
bot.login()
bot.get_all_followers('https://www.instagram.com/username/')
