import time
import atexit
import getpass
import requests  # install the package via "pip install requests"
from collections import defaultdict
from Algorithm import getResponse
from Preprocess import Preprocess
# url of the speakeasy server
url = 'https://speakeasy.ifi.uzh.ch'
#url = "https://server5.speakeasy-ai.org"
listen_freq = 1

ENTRY_MSG = "Hello, I am Griot. Type HELP in chat box to understand the types of questions I can answer! Looking forward to interact with you :D"
DEFAULT_MSG = "I don't understand you. Can you rephrase it?"


class DemoBot:
    def __init__(self, username, password, prior_obj):
        self.agent_details = self.login(username, password)
        self.session_token = self.agent_details['sessionToken']
        self.chat_state = defaultdict(lambda: {'messages': defaultdict(dict), 'initiated': False, 'my_alias': None})
        self.prior_obj = prior_obj
        atexit.register(self.logout)

    def listen(self):
        while True:
            # check for all chatrooms
            current_rooms = self.check_rooms(session_token=self.session_token)['rooms']
            for room in current_rooms:
                # ignore finished conversations
                if room['remainingTime'] > 0:
                    room_id = room['uid']
                    if not self.chat_state[room_id]['initiated']:
                        # send a welcome message and get the alias of the agent in the chatroom
                        self.post_message(room_id=room_id, session_token=self.session_token, message=ENTRY_MSG.format(listen_freq))
                        self.chat_state[room_id]['initiated'] = True
                        self.chat_state[room_id]['my_alias'] = room['alias']

                    # check for all messages
                    all_messages = self.check_room_state(room_id=room_id, since=0, session_token=self.session_token)['messages']

                    # you can also use ["reactions"] to get the reactions of the messages: STAR, THUMBS_UP, THUMBS_DOWN

                    for message in all_messages:
                        if message['authorAlias'] != self.chat_state[room_id]['my_alias']:

                            # check if the message is new
                            if message['ordinal'] not in self.chat_state[room_id]['messages']:
                                self.chat_state[room_id]['messages'][message['ordinal']] = message
                                print('\t- Chatroom {} - new message #{}: \'{}\' - {}'.format(room_id, message['ordinal'], message['message'], self.get_time()))
                                try:
                                    reply = getResponse(message["message"], self.prior_obj)
                                except:
                                    reply = DEFAULT_MSG
                                self.post_message(room_id=room_id, session_token=self.session_token, message=reply)
                                # self.post_message(room_id=room_id, session_token=self.session_token, message='Got your message: \'{}\' at {}.'.format(message['message'], self.get_time()))
            time.sleep(listen_freq)

    def login(self, username: str, password: str):
        agent_details = requests.post(url=url + "/api/login", json={"username": username, "password": password}).json()
        print('- User {} successfully logged in with session \'{}\'!'.format(agent_details['userDetails']['username'], agent_details['sessionToken']))
        return agent_details

    def check_rooms(self, session_token: str):
        return requests.get(url=url + "/api/rooms", params={"session": session_token}).json()

    def check_room_state(self, room_id: str, since: int, session_token: str):
        return requests.get(url=url + "/api/room/{}/{}".format(room_id, since), params={"roomId": room_id, "since": since, "session": session_token}).json()

    def post_message(self, room_id: str, session_token: str, message: str):
        tmp_des = requests.post(url=url + "/api/room/{}".format(room_id),
                                params={"roomId": room_id, "session": session_token}, data=message).json()
        if tmp_des['description'] != 'Message received':
            print('\t\t Error: failed to post message: {}'.format(message))

    def get_time(self):
        return time.strftime("%H:%M:%S, %d-%m-%Y", time.localtime())

    def logout(self):
        if requests.get(url=url + "/api/logout", params={"session": self.session_token}).json()['description'] == 'Logged out':
            print('- Session \'{}\' successfully logged out!'.format(self.session_token))


if __name__ == '__main__':
    username = 'rupal.saxena_bot'
    #username = "panickyLeopard0_bot"
    password = "Tori3IWM-Ep-Jw"
    prior_obj = Preprocess()
    demobot = DemoBot(username, password, prior_obj)
    demobot.listen()
