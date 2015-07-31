#Our chatsystem Everything will be included in this file for now, once it starts growing we will seperate into modules
# Important this diaglog system is still in development, it comes no where near human processing intelligence
import nltk
import sqlite3
import os

#For now the NLU will be in this file, if it grows we will need to put it elsewhere
def preprocess(raw):
    raw = raw.lower()
    tokens = nltk.word_tokenize(raw)
    tags = nltk.pos_tag(tokens)
    return NounPhrase(tags)

#getting noun phrase
def NounPhrase(tags):
    grammar = 'NP: {<DT>?<JJ>*<NN>}'
    cp = nltk.RegexpParser(grammar)
    return cp.parse(tags)

#TODO: calculate verb phrase?? 
  

def question(Q):
    return nltk.help.upenn_tagset(Q)


# makes inserting into DB easier
def insertDB(word,statement):
    conn = sqlite3.connect('dialogknowledge.db')
    c = conn.cursor()
    c.execute("insert into greetings (word,statement) values (?,?)",(word,statement))
    conn.commit()
    conn.close()

def printTable():
    conn = sqlite3.connect('dialogknowledge.db')
    c = conn.cursor()
    c.execute("SELECT * FROM greeting")

#Dialog Manager
class DialogManager:
    #Current topic string form
    topic = None
    #database representation of topic
    topicKnowledge = None;
    person = None
    #Noun phrase
    NP = None
    #The word list which will stay in memory
    wordlist = None

    def __init__(self):
        #Folders chatbotIQ/topics & chatbotIQ/wordlist must exist in cwd
        if(os.name == "nt"):
            dir = os.getcwd() + "\\chatbotIQ\\wordlist\\vocab"
        else:
            dir = os.getcwd() + "/chatbotIQ/wordlist/vocab"
        DialogManager.wordlist = self.searchAid(dir)

        
    #This is our parser that will parse any of our database files
    def searchAid(self, dir):
        dataset = []
        text1 = None
        text2 = None
        f = open(dir, 'r')
        fileText = f.readline()
        while (fileText != ''):
            templist = []
            temp = nltk.word_tokenize(fileText)
            text1 = temp[0]
            text2 = " ".join(temp[2:])
            templist.append(text1)
            templist.append(text2)
            dataset.append(templist)
            fileText = f.readline()

        return dataset

    def loadTopic(self,topic):
        if(os.name == "nt"):
            dir = []
            dir.append(os.getcwd() + "\\chatbotIQ\\topics")
        else:
            dir = []
            dir.append(os.getcwd() + "/chatbotIQ/topics")

        files = os.listdir(dir)
        for i in range(0, len(files)-1):
            if files[i] == topic:
                dir.append(files[i])
                break
        ''.join(dir)
        DialogSystem.topicKnowledge = self.searchAid(self,dir)

        
        
        
            
        
        
    #looks for topic in wordlist
    def topicSearch(self,word):
        print word
        topicSet = False
        for i in DialogManager.wordlist:
            if word == i[0]:
                DialogManager.topic = i[1]
                topicSet = True
                break

        
        if(topicSet == False):
            DialogManager.topic = word


    #searching for the key tag
    def findKey(self,sentence):
        topicSet = False
        tree = sentence[0:]
        for i in tree:
            for j in DialogManager.wordlist:
                if i[0].lower() == j[0]:
                    DialogManager.topic = j[1]
                    topicSet = True
                    break

        #If topic not in wordlist assume first noun is the topic
        if(topicSet == False):
            for i in tree:
                if(i[1] == "NN" or i[1] == "NNS"):
                    DialogManager.topic = i[0]
                    topicSet = True
                    break

            if(topicSet == False):
                DialogManager.topic = None


    
    
    def checkTopic(self,sentence):
        if len(sentence) == 1:
            self.topicSearch(sentence[0][0])
        else:
            self.findKey(sentence)
        
    
    def Analyze(self,text):
        self.checkTopic(text.flatten())
                

    def getNLUdata(self,NLUtext):
        #pass of to analyze
        self.Analyze(NLUtext)

    

# Where the user chats with the system
def chat():
    while True:
        manager = DialogManager()
        raw = raw_input()
        if raw == "qqq":
            sys.exit()
        manager.getNLUdata(preprocess(raw))
        print manager.topic
        print manager.topicKnowledge

