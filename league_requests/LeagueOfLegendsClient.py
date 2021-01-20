import time
from base64 import b64encode
import requests
import urllib3
import os


class LeagueOfLegendsClient(object):
    __session = None

    __username = None
    __password = None

    def __init__(self, path, account_name):
        # disable the InsecureRequestWarning
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.league_path = path
        self.account_name = account_name

        self.__username = "riot"

        self.host = '127.0.0.1'
        self.headers = None

        self.process_name = None
        self.process_pid = None
        self.port = None
        self.protocol = None

        self.messages = []
        self.last_message = None

    def __request(self, method, path, query='', data=''):
        if not query:
            url = '%s://%s:%s%s' % (self.protocol, self.host, self.port, path)
        else:
            url = '%s://%s:%s%s?%s' % (self.protocol, self.host, self.port, path, query)

        print('%s %s %s' % (method.upper().ljust(7, ' '), url, data))

        if not data:
            return getattr(self.__session, method)(url, verify=False, headers=self.headers)
        else:
            return getattr(self.__session, method)(url, verify=False, headers=self.headers, json=data)

    def parse_lockfile(self):
        lockfile = None
        lockfile_exists = False
        # check if the client is running
        lockfile_path = self.league_path + "\lockfile"

        print("[*] Waiting for the client to start")
        while not lockfile_exists:
            if os.path.isfile(lockfile_path):
                lockfile = open(lockfile_path, "r")
                lockfile_exists = True
        # read the lockfile data
        lockfile_data = lockfile.read()
        lockfile.close()
        lockfile_list = lockfile_data.split(":")
        # wait for the client (if the user has just logged in, for example, there is a bit delay)
        time.sleep(1)
        self.process_name, self.process_pid, self.port, self.__password, self.protocol = lockfile_list

        username_password = b64encode(bytes('%s:%s' % (self.__username, self.__password), 'utf-8')).decode('ascii')
        self.headers = {'Authorization': 'Basic %s' % username_password}

        self.__session = requests.session()

    """
    :returns summoner ID once the login session has been established
    """
    def __wait_login_session(self):
        while True:
            r = self.__request('get', '/lol-login/v1/session')
            if r.status_code != 200:
                print("[-] Error -- {}".format(r.status_code))
                continue

            # login completed
            if r.json()['state'] == 'SUCCEEDED':
                return r.json()['summonerId']

    def send_message(self, message):
        summoner_id = self.__wait_login_session()

        r = self.__request('get', '/lol-chat/v1/conversations')
        if r.status_code != 200:
            print(r.status_code)
            print("[-] Error while parsing the conversations")

        data = r.json()

        tmp_summoner_id = None
        for entry in data:
            if entry['gameName'] == self.account_name:
                tmp_summoner_id = entry['id']
                break

        if tmp_summoner_id is None:
            print("[-] You don't have a conversation with {}".format(self.account_name))
            # maybe restart? or maybe exit, idk
            exit(0)

        r = self.__request('get', '/lol-chat/v1/conversations/{}/messages'.format(tmp_summoner_id))
        if r.status_code != 200:
            print(r.status_code)
            print("[-] Error while getting the messages")

        data = r.json()

        for entry in data:
            if entry['body'] == 'joined_room':
                continue
            else:
                # TODO: maybe I should create a list containing all the messages. Think about a way to manage the
                #       messages and to understand when / how to send / receive all the messages.
                if entry['fromSummonerId'] == summoner_id:
                    print("debug")
                print(entry['body'])

        print(data)

        request_body = {'body': message}
        r = self.__request(
            'post', '/lol-chat/v1/conversations/{}/messages'.format(tmp_summoner_id), '', request_body
        )

        if r.status_code != 200:
            print(r.status_code)
            print("[-] Error --- message {}".format(message))
