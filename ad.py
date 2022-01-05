"""Discord Rich Presence advertisement for my Bot"""
import time
import pypresence as rpc
import re

CLIENT_ID = 872705737430827069
MYPY_NO_ERR_MSG = "Success: no issues found in "

RPC = rpc.Presence(client_id=CLIENT_ID)
RPC.connect()

RPC.update(
    details="Check out my new Discord Bot",
    state="Made with Hikari",
    large_image="lmao",
    large_text="xd",
    buttons=[
        # {"label": "Invite my Bot", "url": ""},
        {"label": "Soruce Code", "url": "https://github.com/AlexanderHOtt/ottbot_v4/"},
    ],
)


class OttRPC(object):
    def __init__(self, RPC):
        self.RPC = RPC

    def update(self):
        with open("mypy.log", "r") as f:
            log = f.read()

        if MYPY_NO_ERR_MSG in log:
            details = "0 mypy errors"
        else:
            details = re.search()

        self.RPC.update(details=details)
        # self.RPC.update(data)


o = OttRPC(RPC)

while True:
    o.update()
    time.sleep(60)
