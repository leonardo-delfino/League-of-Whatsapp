from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import sys


class WhatsAppParser(object):
    def __init__(self, chat_name, personal_alias):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--log-level=3")

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException:
            flag = input("[-] Make sure that you have Google Chrome installed. Is it? [yes/no] ")
            if flag == "yes" or flag == "y":
                print("[-] Check your Google Chrome's version and download the correct chromedriver manually from"
                      " https://chromedriver.chromium.org/downloads and make sure that the chrome driver is in the"
                      " same directory of the executable.")
                sys.exit(0)
            else:
                print("[-] this script can't run without Google Chrome")
                sys.exit(0)

        self.chat_name = chat_name
        self.ascii_chat_name = self.chat_name.encode('ascii', 'ignore').decode('ascii')
        self.personal_alias = personal_alias
        self.ascii_personal_alias = self.personal_alias.encode('ascii', 'ignore').decode('ascii')

        self.driver.get("https://web.whatsapp.com/")
        xpath_arg = '//span[@title = "{}"]'.format(chat_name)
        contact = None
        try:
            contact = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, xpath_arg)))
        except TimeoutException:
            print("[-] The username can't be found.")
            exit(-1)
        contact.click()

        self.messages = []
        self.last_message = None
        self.replies = []

    """
    Possible messages:
        length 0:
            - image
        length 1:
            - text message
            - video (length)
            - sticker (if the text is empty)
        length 2:
            - vocal message (index 0 = length)
        length 3:
            - index 0 = sender of the message he / she is replying to (should be me)
            - index 1 = message he / she is replying to
            - index 2 = text (if the text is empty, it's an image)
        length 4:
            - index 0 = sender of the message he / she is replying to (should be the contact)
            - index 1 = message he / she is replying to
            - index 2 = text
            - index 3 = name
        length n:
            - if index 0 =/= 'You' or ascii_chat_name or is not a length (or 2nd index is not ''), then it's a message
              with emojis
    """
    def get_messages(self):
        time.sleep(3)
        # TODO: sometimes this does not work (maybe now it's working, do more tests)
        messages_list = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/div[4]/div/div[3]/div/div'
        )
        # every first layer sub elements
        tmp_messages = reversed(
            messages_list.find_elements_by_xpath('//*[@class="tSmQ1"]')[0].find_elements_by_xpath("./*")
        )
        # get only the received messages before the last sent message
        for message in tmp_messages:
            if "message-out" in message.get_attribute("class"):
                break
            # empty = image or sticker or video
            emoji = None
            for el in message.find_elements_by_xpath(".//*"):
                try:
                    emoji = str(el.find_element_by_tag_name('img').get_attribute("alt"))
                    break
                except NoSuchElementException:
                    continue
            tmp_list = message.text.splitlines()[:-1]
            if emoji is not None:
                tmp_list.append(emoji)
                self.messages.append(tmp_list)
            else:
                self.messages.append(tmp_list)

        return self.messages

    def close(self):
        self.driver.close()
