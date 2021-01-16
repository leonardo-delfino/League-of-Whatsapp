from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import sys


class MessagesParser(object):
    def __init__(self, chat_name, personal_alias):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--log-level=3")

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException:
            print("ti puzza il webdriver")
            sys.exit(0)

        self.chat_name = chat_name
        self.ascii_chat_name = self.chat_name.encode('ascii', 'ignore').decode('ascii')
        self.personal_alias = personal_alias
        self.ascii_personal_alias = self.personal_alias.encode('ascii', 'ignore').decode('ascii')

        self.driver.get("https://web.whatsapp.com/")
        self.wait = WebDriverWait(self.driver, 600)
        xpath_arg = '//span[@title = "{}"]'.format(chat_name)
        contact = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_arg)))
        contact.click()

        self.messages = []
        self.replies = []

    def get_messages(self):
        time.sleep(3)
        labels = self.driver.find_elements_by_xpath(
            '//*[@class="copyable-text"]'
        )
        messages = self.driver.find_elements_by_xpath(
            '//*[@class="_1dB-m"]'
        )

        for label, message in zip(reversed(labels), reversed(messages)):
            current_msg = message.text.splitlines()[:-1]
            if self.ascii_chat_name in current_msg:
                current_msg.remove(self.ascii_chat_name)

            if self.personal_alias in label.get_attribute('data-pre-plain-text') or \
                    self.ascii_personal_alias in label.get_attribute('data-pre-plain-text'):
                print(current_msg)
                # break
            else:
                print(current_msg)
                # text message (text - timestamp)
                if len(current_msg) == 2:
                    self.messages.append(current_msg[0])
                    # self.timestamps.append(current_msg[0])
                    self.replies.append("")
                elif len(current_msg) == 4:
                    self.messages.append(current_msg[2])
                    # self.timestamps.append(current_msg[3])
                    self.replies.append(current_msg[1])

    def close(self):
        self.driver.close()
