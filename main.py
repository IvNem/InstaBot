from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random


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

            time.sleep(3)

            # browser.close()
            # browser.quit()
        except Exception as ex:
            print(ex)
            self.close_browser()

    def hashtag_search(self, hashtag):
        browser = self.browser
        self.login()
        try:
            browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            time.sleep(5)

            for i in range(1, 8):
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(random.randrange(3, 5))

            hrefs = browser.find_elements_by_tag_name('a')
            posts_url = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
            print(len(posts_url))

            for url in posts_url:
                browser.get(url)
                time.sleep(3)
                like_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(80, 100))
            # browser.close()
            # browser.quit()
        except Exception as ex:
            print(ex)
            self.close_browser()


# hashtag_search(username, password, "Спб")
bot = InstagramBot(username, password)
bot.hashtag_search("молодаямама")
