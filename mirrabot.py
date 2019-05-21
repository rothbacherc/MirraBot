#Version 2.0 Dev: Charles Rothbacher

import random
import requests
from requests.exceptions import HTTPError

#there are built in functions and libraries that do similar things possibly
#better, but this is a really simple funtion that takes only the punctuations
#that I want out
def textFormatter(text):
    punct = ['!','$','%','*','(',')','-',',','.','[',']','{','}','?','@']
    for i in punct:
        text = text.replace(i,' ')
    return text

def sendText(chat_id, text):
    sendURL = baseURL 
    sendURL += 'sendMessage'
    PARAMS = {'chat_id': chat_id, 'text': text}
    try:
        requests.post(url = sendURL, params = PARAMS)
        print("Send Worked")
    except:
        print("Send Broke")

def getPatchNotes(allNotes,chat_id):
    outFile = open('mirrabotPatchNotes.txt','r')
    #make a new string that will be combined with each line in the file
    #and allow them to be printed out all as is
    notesString = '*'
    for line in outFile:
        notesString = notesString + line
    #finds the last * which denotes the beginning of a specific version
    if allNotes == False: 
        start = notesString.rfind('*')
    else:
        start = 1
    sendText(chat_id, notesString[int(start):])      #fix here
    outFile.close()

def writeIn(chat_id,text):
    inFile = open('mirraism.txt','a+')
    inFile.write(text + '\n')
    mList.append(text)
    length = len(mList) + 1
    inFile.close()
    print(length)
    #find out how long inFile is, have to open it again specifically for reading
    #inFile = open('mirraism.txt','r')
    #i = 0
    #for line in inFile:
    #    i += 1
    if length % 100 == 0:
        #used double quotes to get around the apostrophe
        sendText(chat_id, "Sham bakkala! I've learned "+ str(length) +" phrases!")      #fix here


def mirraSays(chat_id):
    #outFile = open('mirraism.txt','r')
    #length = 0
    #mList = []
    #for strLine in outFile:
    #    mList.append(strLine[:-1])
    #    length += 1
    ranNum = random.randint(0,mLength-1)
    #print(length)
    sendText(chat_id, mList[ranNum]) #bot.sendMessage(chat_id, mList[ranNum])      #fix here
    #outFile.close()
    
def handleMe(msg):
    user_name = msg['from']['username']
    user_id = msg['from']['id']
    text = msg['text']
    chat_id = msg['chat']['id']
    dice = random.randint(1,6)
    wordTest = []
    inFlag = False
    outFlag = False
    patchFlag = False
    hasLearned = False
    allNotes = False

    #pprint.pprint(msg)

    #checks if this is a reply or not to use with teaching mirrabot phrases    
    if 'reply_to_message' in msg:
        replyText = msg['reply_to_message']['text']
        replyName = msg['reply_to_message']['from']['username']

    replaced = textFormatter(text)
    wordTest = replaced.split(' ')

    for i in wordTest:
        if user_name == mirra and (i == 'chicken' or i == 'apple'):
            inFlag = True
        elif i == '/mirrasays':
            outFlag = True
        
    #if text  == '/update' and user_name == admin:       #fix here
    #    bot.getUpdates
    if text == '/patchnotes' and user_name == admin:
        getPatchNotes(allNotes,chat_id)
    elif text == '/allpatchnotes' and user_name == admin:
        allNotes = True
        getPatchNotes(allNotes,chat_id)
    elif text == '/mirrasays' or outFlag == True:
        mirraSays(chat_id)
    elif text == '/mirralearns' and user_name != mirra and replyName == mirra:
        inFile = open('mirraism.txt','r')
        for strLine in inFile:
            if strLine[:-1] == replyText:
                hasLearned = True
        inFile.close()
        if hasLearned == True:
            sendText(chat_id, 'I already knew that you butthead!')               #fix here
        else:
            writeIn(chat_id,replyText)
            sendText(chat_id,replyText)                                 #fix here
    else:
        if inFlag == True:
            writeIn(chat_id,text)
        elif user_name == 'mirracles' and dice > 3 and len(text) > 10:
            writeIn(chat_id,text)

offset = 0
inFile = open('botKey.txt', 'r')
key = inFile.readline()
admin = inFile.readline()
mirra = inFile.readline()
inFile.close()

outFile = open('mirraism.txt','r')
mLength = 0
mList = []
for strLine in outFile:
    mList.append(strLine[:-1])
    mLength += 1
outFile.close()

baseURL = 'https://api.telegram.org/bot'
baseURL += key + '/'
print("I'm on!")

while 1:
    try:
        result = requests.post(url = baseURL + 'getUpdates', data={"offset": offset})
        result.raise_for_status()
        msgList = result.json()["result"]
        if len(msgList) > 0:
            offset = msgList[-1]["update_id"] + 1
            for msg in msgList:
                print(msg)
                handleMe(msg['message'])
    except HTTPError as http_err:
        print("It broke")
    except KeyboardInterrupt as e:
        print("End")
        break
