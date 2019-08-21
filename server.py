import requests
from mirrabot import mirrabot
from requests.exceptions import HTTPError

if __name__ == "__main__":
    botBoi = mirrabot()
    offset = 0
    inFile = open('botKey.txt', 'r')
    line = inFile.readline().split(',')
    key = line[0]
    mirra = line[1]
    inFile.close()
    baseURL = 'https://api.telegram.org/bot'
    baseURL += key + '/'
    sendURL = baseURL + "sendMessage"
    print("I'm on!")
    while 1:
        result = None
        try:
            data = requests.post(url = baseURL + 'getUpdates', data={"offset": offset})
            data.raise_for_status()
            msgList = data.json()["result"]
            if len(msgList) > 0:
                offset = msgList[-1]["update_id"] + 1
                for msg in msgList:
                    print(msg)
                    if('message' in msg):
                        result = botBoi.handleMe(msg['message'], mirra)
                    elif('edited_message' in msg):
                        result = botBoi.handleMe(msg['edited_message'], mirra)

                    if result != None:
                        try:
                            requests.post(url = sendURL, params = result)
                        except HTTPError as http_err:
                            print("Send broke")
        except HTTPError as http_err:
            print("Update broke")
        except KeyboardInterrupt as e:
            print("Force End")
            break
        except Exception as e:
            print("Unkown error")
            print(e)