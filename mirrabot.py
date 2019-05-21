#Version 2.0 Dev: Charles Rothbacher
import random

class mirrabot:
    mLength = 0
    mList = []

    def __init__(self):
        outFile = open('mirraism.txt','r')
        for strLine in outFile:
            self.mList.append(strLine[:-1])
            self.mLength += 1
        outFile.close()

    #there are built in functions and libraries that do similar things possibly
    #better, but this is a really simple funtion that takes only the punctuations
    #that I want out
    def textFormatter(self, text):
        punct = ['!','$','%','*','(',')','-',',','.','[',']','{','}','?','@']
        for i in punct:
            text = text.replace(i,' ')
        return text

    def sendText(self, chat_id, text):
        return {'chat_id': chat_id, 'text': text}

    def writeIn(self, chat_id, text):
        inFile = open('mirraism.txt','a+')
        inFile.write(text + '\n')
        self.mList.append(text)
        self.mLength += 1
        inFile.close()
        print(self.mLength)

        #breaking for now
        #if self.mLength % 100 == 0:
            #used double quotes to get around the apostrophe
        #    return self.sendText(chat_id, "Sham bakkala! I've learned "+ str(self.mLength) +" phrases!")      #fix here


    def mirraSays(self, chat_id):
        ranNum = random.randint(0,self.mLength-1)
        return self.sendText(chat_id, self.mList[ranNum]) 

    def handleMe(self, msg, mirra):
        if 'text' in msg:
            user_name = msg['from']['username']
            text = msg['text']
            chat_id = msg['chat']['id']
            dice = random.randint(1,6)
            wordTest = []
            inFlag = False
            outFlag = False
            hasLearned = False

            #checks if this is a reply or not to use with teaching mirrabot phrases    
            if 'reply_to_message' in msg:
                replyText = msg['reply_to_message']['text']
                replyName = msg['reply_to_message']['from']['username']

            replaced = self.textFormatter(text)
            wordTest = replaced.split(' ')

            for i in wordTest:
                if user_name == mirra and (i == 'chicken' or i == 'apple'):
                    inFlag = True
                elif i == '/mirrasays':
                    outFlag = True

            if text == '/mirrasays' or outFlag == True:
                return self.mirraSays(chat_id)
            elif text == '/mirralearns' and user_name != mirra and replyName == mirra:
                inFile = open('mirraism.txt','r')
                for strLine in inFile:
                    if strLine[:-1] == replyText:
                        hasLearned = True
                inFile.close()
                if hasLearned == True:
                    return self.sendText(chat_id, 'I already knew that you butthead!')               
                else:
                    self.writeIn(chat_id,replyText)
                    return self.sendText(chat_id,replyText)                                 
            else:
                if inFlag == True:
                    self.writeIn(chat_id,text)
                elif user_name == mirra and dice > 3 and len(text) > 10:
                    self.writeIn(chat_id,text)
                return None