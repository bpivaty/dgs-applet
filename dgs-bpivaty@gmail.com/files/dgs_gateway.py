#!/usr/bin/env python3

try:
    import json
except:
    print("Python can't import json. Should be builtin in python. Go search the web or create a issue on git")
    exit()

try:
    import urllib.request
    from requests import Request, Session
except:
    print(json.dumps({"error":"Python can't import FancyURLopener from urllib.request","info":"Search the web or create issue on git"}))
    exit()

import sys

session = Session()

def dgs_login(user, password):
    try:
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

            return json.dumps(
                {"status_code": "Ok",
                 "id": user_info["id"],
                  "handle": user_info["handle"],
                   "list_result": game_list
                })

        else:
            return json.dumps({"status_code": "#Error"})
    except:
        return json.dumps({"status_code": "#Error"})
    

def main():
    response = ''
    
    # no need to check as argv[] is alsways fed with
    # the correct arguments from applet.js
    response = dgs_login(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
