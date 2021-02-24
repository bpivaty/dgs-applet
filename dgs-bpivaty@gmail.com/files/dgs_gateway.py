#!/usr/bin/env python3

try:
    import json
    import logging
    # 
except:
    print("Python can't import json. Should be builtin in python. Go search the web or create a issue on git")
    exit()

try:
    import urllib.request
    from requests import Request, Session
except:
    print(json.dumps({"error":"Python can't import FancyURLopener from urllib.request","info":"Search the web or create issue on git"}))
    exit()

try:
    import keyring
except:
    print(json.dumps({"error":"Python can't import keyring libary","info":"'pip3 install keyring' and 'pip3 install keyrings-alt' to fix"}))
    exit()

import sys
import time

session = Session()

def dgs_login(user, password):

    dgs_url = "http://dragongoserver.net/"
    url = dgs_url + "login.php?quick_mode=1&userid=" + user + "&passwd=" + password

    req = urllib.request.Request(url)

    user_info = ""
    games = ""

    if '#Error' not in session.get(url):
        url = dgs_url + "quick_do.php?obj=user&cmd=info&uid=" + user
        result = session.get(url)
        user_info = json.loads(result.text)

        url = dgs_url + "quick_do.php?obj=game&cmd=list&view=running&uid=" + user
        result = session.get(url)
        games = json.loads(result.text)

        game_list = []
        for game in games["list_result"]:
            if game[29] == user_info["id"]:
                url = dgs_url + "quick_do.php?obj=user&cmd=info&uid=" + str(game[34])
                opponent_info = json.loads(session.get(url).text)
                game_list.append([game[0], game[25], user, opponent_info["handle"]])
            else:
                url = dgs_url + "quick_do.php?obj=user&cmd=info&uid=" + str(game[29])
                opponent_info = json.loads(session.get(url).text)
                game_list.append([game[0], game[25], opponent_info["handle"], user])

        result = session.get(url)

        print(json.dumps(
            {"status_code": "Ok",
             "id": user_info["id"],
              "handle": user_info["handle"],
               "list_result": game_list
            }))

        return json.dumps(
            {"status_code": "Ok",
             "id": user_info["id"],
              "handle": user_info["handle"],
               "list_result": game_list
            })

    else:
        return json.dumps({"status_code": "#Error"})
    

def main():
    logging.basicConfig(filename='/tmp/getHttpData.log', level=logging.INFO)

    response = ''

    user = sys.argv[1]
    passwd = sys.argv[2]

    response = dgs_login(user, passwd)


if __name__ == "__main__":
    main()
