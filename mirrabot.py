#Version 1.2 Dev: Charles Rothbacher

import random
import datetime
import telepot
import time
import pprint

#telepot github: https://github.com/nickoala/telepot
#thank you for providing this library and the example I built 
#this project off of.

#there are built in functions and libraries that do similar things possibly
#better, but this is a really simple funtion that takes only the punctuations
#that I want out
def textFormatter(text):
    punct = ['!','$','%','*','(',')','-',',','.','[',']','{','}','?','@']
    for i in punct:
	text = text.replace(i,' ')
    return text

def getPatchNotes(allNotes,chat_id):
    outFile = open('####################.txt','r')
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
    bot.sendMessage(chat_id, notesString[int(start):])
    outFile.close()

def writeIn(chat_id,text):
    inFile = open('############################.txt','a+')
    inFile.write(text + '\n')
    inFile.close()
    #find out how long inFile is, have to open it again specifically for reading
    inFile = open('################################.txt','r')
    i = 0
    for line in inFile:
        i += 1
    if i == 100 or i == 200 or i == 300 or i == 400 or i == 500:
	#used double quotes to get around the apostrophe
        bot.sendMessage(chat_id, "Sham bakkala! I've learned "+ str(i) +" phrases!")


def mirraSays(chat_id):
    outFile = open('################################.txt','r')
    length = 0
    mList = []
    for strLine in outFile:
        mList.append(strLine[:-1])
        length += 1
    ranNum = random.randint(0,length-1)
    bot.sendMessage(chat_id, mList[ranNum])      #fix here
    outFile.close()
    
def handle(msg):
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

    pprint.pprint(msg)
    print '\n'

    #checks if this is a reply or not to use with teaching mirrabot phrases    
    if 'reply_to_message' in msg:
	print 'in the if'
        replyText = msg['reply_to_message']['text']
	replyName = msg['reply_to_message']['from']['username']

    replaced = textFormatter(text)
    wordTest = replaced.split(' ')

    for i in wordTest:
        if user_name == '#################' and (i == 'chicken' or i == 'apple'):
            inFlag = True
	elif i == '/mirrasays':
	    outFlag = True
    
    if text  == '/update' and user_name == '#####################':
        bot.getUpdates
    elif text == '/patchnotes' and user_name == '##################':
	getPatchNotes(allNotes,chat_id)
    elif text == '/allpatchnotes' and user_name == '###################':
	allNotes = True
	getPatchNotes(allNotes,chat_id)
    elif text == '/mirrasays' or outFlag == True:
        mirraSays(chat_id)
    elif text == '/mirralearns' and user_name != '##########' and replyName == '########':
	inFile = open('######################.txt','r')
	for strLine in inFile:
	    print strLine[:-1]
	    if strLine[:-1] == replyText:
		hasLearned = True
	inFile.close()
	if hasLearned == True:
	    bot.sendMessage(chat_id, 'I already knew that you butthead!')  #fix here
	else:
	    writeIn(chat_id,replyText)
	    bot.sendMessage(chat_id,replyText)   #fix here
    else:
        if inFlag == True:
            writeIn(chat_id,text)
        elif user_name == '#########################' and dice == 6 and len(text) > 10:
            writeIn(chat_id,text)

bot = telepot.Bot('##################################################')
bot.notifyOnMessage(handle)

while 1:
    time.sleep(10)
