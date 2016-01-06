#!/usr/bin/python

from urllib.request import urlopen
from random import randrange

import re
from time import *

from subprocess import call

import unicodedata

import urllib
from urllib.parse import quote


import os.path

class Bot():
    def __init__(self):
        self.TIMERp=time()-13.0
        self.TIMERs=time()-13.0
        self.TIMERn=time()-13.0

        self.REPp = 1
        self.REPs = 1
        self.REPn = 1

        
        self.BANWORD = []#[['55','@porn']]
        self.load_banword()

        self.ONvestibular=0
        
        
    def load_banword(self):
        if not os.path.isfile('banword.txt'):
            return
        BANW = open('banword.txt', 'r')

        for line in BANW.readlines():
            line = line.split('=')
            if len(line) > 1:
                if line[1][-1] == '\n':
                    line[1]=line[1][:-1]
                self.BANWORD.append([line[0],line[1]])


                
    def read_output(self, output, sender, participant):

        output = output.lower()
        
        for BWK in self.BANWORD:        
            if BWK[1] in output:
                
                return ["essezin disse a palavra banida, se fodeo."]

                


        if '@kkk' in output:
            if float(time()) - self.TIMERp > 13.0:
                
                self.TIMERp = time()
                self.REPp = 1
                return retrieve_joke()

            
            elif self.REPp:
                
                self.REPp = 0
                self.TIMERp = time()
                return "por que você não conta uma aí agora, fdp?"

                
        elif ('@sad' in output) or ('@pensa' in output) or ('@love' in output):
            if float(time()) - self.TIMERs > 13.0:
                
                print('@sad granted. current time is ' + str(time()) + ' and buffer time is ' + str(self.TIMERs))
                self.TIMERs = time()
                self.REPs = 1
                KIND = ['@sad', '@pensa', '@love']
                for Ki in range(len(KIND)):
                    if KIND[Ki] in output:
                        
                        if '!' in output:
                            return create_voice(psicologo(Ki))
                        else:                                                
                            return psicologo(Ki)
                    
            elif self.REPs:
                print('@sad denied. current time is ' + str(time()) + ' and buffer time is ' + str(self.TIMERs))
                
                self.REPs = 0
                self.TIMERs=time()
                return "calem essa boca, voces me contaminam com essa depressão."

        elif '@nerd' in output:
            if float(time()) - self.TIMERn > 13.0:
                
                print('@nerd granted. current time is ' + str(time()) + ' and buffer time is ' + str(self.TIMERn))
                self.TIMERn = time()
                self.REPn=1
                return wikipedia()

            
            elif self.REPn:
                print('@nerd denied. current time is ' + str(time()) + ' and buffer time is ' + str(self.TIMERn))
                
                self.REPn = 0
                self.TIMERn=time()                
                return "vai pegar um livro, seu mongolão."

            
        elif '@xinga ' in output:
            X = output.find('@xinga')
            word = output[X+7:]
            if " " in word:
                word = word.split(" ")
                word = word[0]

            if len(word) > 4:
                usrhasbw = 0
                
                for BW in self.BANWORD:
                    if BW[0] == sender:
                        BW[1] = word.lower()
                        usrhasbw = 1
                            
                if usrhasbw ==0:
                    self.BANWORD.append([sender,word])
                    
                BW = open('banword.txt', 'w')
                for BANW in self.BANWORD:
                    BW.write(BANW[0]+"="+BANW[1]+'\n')
                BW.close()                    
                    
                return (word + " agora é uma palavra banida.")
            else:
                return(word + " é uma palavra muito curta, seu fela.")                



        elif ('@' in output) and ('porn' in output):
            if 'ruiva' in output:
                return retrieve_porn('ruiva')

            elif 'soft' in output:
                return retrieve_porn('soft')

            elif 'sapa' in output:
                return retrieve_porn('lesbian')

            elif 'afro' in output:
                return retrieve_porn('ebony')
            
            else:
                return retrieve_porn('normal')               
                
                                      
        elif 'koeh!' in output:
            msg = "koeh.. sou o adolfo gomes, seu novo amiguinho. Digite @kkk para rir um pouquinho ou digite @sad se voce estiver se sentindo um lixo. @nerd pra estudar uns skemas." #Se quiser sacanear seus amigo fpd, digite @xinga exemplo .. quem disser exemplo será banido (se eu for adm)."
            return msg


        


        elif '@diz' in output:
            X = output.find('@diz')+4
            word = output[X+5:]
            return create_voice(word)


        elif ('@jesus' in output) or ('@god' in output):
            return (retrieve_salmo())


        elif '@drugs' in output:
            return retrieve_drugs()


        elif '@enema' in output:
            return vestibular_questao()[0]


        #elif '@vestibular' in output:
        #    if self.ONvestibular == 0: self.ONvestibular = Vestibular(sender, sender.getParticipants, self.CliLayer, self)

        elif '#' in output:
            if self.ONvestibular:
                self.ONvestibular.getanswer(output, participant)


        

        for AUTO in AUTO_RETRIEVE:
            OUT = AUTO.trigger(output)
            if AUTO.trigger(output):
                return OUT




    def getCliLayer(self, layer):
        self.CliLayer = layer

    def sendmessage(self, TO, MSG):
        self.CliLayer.message_send(TO, MSG)



    def govestibular(self, group, party):
        self.ONvestibular = Vestibular(group,party,self.CliLayer,self)



def retrieve_joke():
    URL ="http://www.piadas.com.br"
    content = urlopen(URL+"/piadas-engracadas").readlines()
    #print (content)
    CATEGORY = []
    for line in content:
        if b'views-field views-field-name' in line:

            Z = line.find(b'<a href="')
            if Z >=0:
                K = line.find(b'">',Z)
                CATEGORY.append(line[Z+9:K])

    #print(CATEGORY)

    chosenCAT = CATEGORY[randrange(0,len(CATEGORY))].decode("UTF-8")


    
    CATcontent = urlopen(URL + chosenCAT).readlines()
    #print(URL + chosenCAT)
    JOKE = []

    for line in CATcontent:
        #print(line)
        if b'Continuar Lendo' in line:

            #print(line)
            Z = line.find(b'<a href="')
            if Z >= 0:
                K = line.find(b'">',Z)
                JOKE.append(line[Z+9:K])

        if b'No momento, ' in line:
            retrieve_joke()
            return




    #print(JOKE)
        

    chosenJOKE = JOKE[randrange(0,len(JOKE))].decode("UTF-8")


    print(URL+chosenJOKE)


    try:
        JOKEcontent = urlopen(URL + chosenJOKE).read().decode("UTF-8")
    except UnicodeDecodeError:
        print("decoding failed.")
        return retrieve_joke()


    


    #Z = JOKEcontent.find('<div class="field field-name-title field-type-ds field-label-hidden">')
    Z = JOKEcontent.find('<div class="field-items" id="md4">')
    K = JOKEcontent.find('<div class="field field-name-gostei field-type-ds field-label-hidden')



            

    JOKETEXT = re.compile(r'<[^>]+>').sub('', JOKEcontent[Z:K])




    if ("iframe" in JOKETEXT) or (len(JOKETEXT) < 60):
        print("failed.")
        return retrieve_joke()
            
    
    return JOKETEXT
    
def psicologo(kind):
    #MOTIVACIONAL= ["Calma, vai dar tudo certo", "Não fique assim, o mundo está sendo muito injusto com você", "Você não eh burrx! As pessoas k não te entendem",
    #               "Você não é uma vadia! Não importa o que o patriarcado te diz.", "Não fique tristi... voce pode ser chato, ignorante, feio, idiota, mas   "]

    URL = 'http://pensador.uol.com.br/blog.php?t='

    KIND = ['fm', 'fa', 'fs']


    MOTIVACIONAL = urlopen(URL+KIND[kind]).read().decode("UTF-8")

    Z = MOTIVACIONAL.find('"')
    K = MOTIVACIONAL.find('<br/>')

    


    MOTIVACIONAL = re.compile(r'<[^>]+>').sub('', MOTIVACIONAL[Z+1:K])

    MOTIVACIONAL = MOTIVACIONAL.replace(')','').replace('\n','').replace('&quot;','').replace('"','')
    
    return MOTIVACIONAL


def wikipedia():

    WIKIP = "https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria"

    content = urlopen(WIKIP).read()
    TAG_RE = re.compile(r'<[^>]+>')


    Z = content.find(b'<p>')
    K = content.find(b'</p>')

    paragraph = content[Z+3:K].decode("UTF-8")
    print(paragraph)
    
    paragraph = TAG_RE.sub('', paragraph)


                     
    if len(paragraph) < 8: return wikipedia()
    else: return paragraph



def retrieve_porn(category):

    URL = 'http://www.pornpics.com/recent'
    CATEGORIES={'normal': '', 'ruiva': '/redhead/' , 'soft': '/stripper/', 'lesbian': '/lesbian/', 'ebony': '/ebony/'}
    
    PORNSRC = URL + CATEGORIES[category]

    content = urlopen(PORNSRC).read().decode("UTF-8")

    number = randrange(0,12)

    
    if os.path.isfile('USEDporn'):
        USED = open('USEDporn', 'r').read()
    else:
        USED = ''
    

    
    PHOTOSARRAY = [m.start() for m in re.finditer('http://content.pornpics.com', content)]

    
    picurl = ""
    X=0
    while picurl in USED:
        number = randrange(len(PHOTOSARRAY))
        Z = PHOTOSARRAY[number]

        picurl = content[Z:Z+120]

        K = picurl.find('.jpg') + 4

        picurl = picurl[:K]

        
        filename = 'porncache.jpg'

        print('>>>>' + picurl)
        X+=1
        if X > 30:
            return

    
    USED = open('USEDporn', 'a+')
        
    USED.write(picurl+'\n')
    FILE = urlopen(picurl)
    Fo = open(filename, 'wb')
    Fo.write(FILE.read())
    Fo.close()
    USED.close()
    return filename

def create_voice(text):
    FILEPATH = '/home/gabs/Desktop/max_steel/sound.wav'

    text = text.replace('ç','ss').replace('á','ah')
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = str(text.encode('ascii', 'ignore'))

    print('>>>>>>>>'+text)
    
    #e = 'echo "'+text+'" | text2wave -scale 10 -o "'+FILEPATH+'"'
    e = 'echo "'+text+'" | espeak -v brazil -w "'+FILEPATH+'"'
    call(e, shell=True)
    sleep(3)

    return FILEPATH
    
def retrieve_salmo():
    INDEX = randrange(1,150)
    SRC = 'http://salmos.a77.com.br/salmos/salmo_%i.php' % INDEX

    PAGE = urlopen(SRC).read()

    Z= PAGE.find(b'<img src="salmo-da-biblia-sagrada.gif"')

    K = PAGE.find(b'<a href="index.php">+Salmos</a>')

    PAGE = PAGE[Z:K].decode('utf-8','ignore')
    SALMO = ''.join(c for c in unicodedata.normalize('NFD', PAGE) if unicodedata.category(c) != 'Mn')

    SALMO = re.compile(r'<[^>]+>').sub('', PAGE[Z:K])

    return SALMO








class Vestibular():
    def __init__(self, group, participants, CLI, BOT):
        self.SCORES = []
        self.group = group
        self.participants = participants
        self.CLI = CLI

        self.BOT = BOT
        self.resposta = ''

        self.questoesN = 0
        for PARTICIPANT in participants:
            self.SCORES.append([PARTICIPANT, 0])


        self.sendmessage(self.group, 'hora do vestibular rapaziada bora garantir sua vaga no mercado de escravos..... digite #a, #b, #c etc.. para responder. Lembrando, eu não boto fé em vocês.')
        self.mandar_questao()
    def sendmessage(self, TO, MSG):
        self.CLI.message_send(TO,MSG)

        
    def mandar_questao(self):
        self.questoesN += 1

        self.ONvestibular=1

        
            
        
        
        
        QUESTAO = vestibular_questao()
        print(QUESTAO)
        self.sendmessage(self.group, QUESTAO[0])
        if len(QUESTAO)>7:
            self.sendpic(QUESTAO[7])
        for i in range(len(QUESTAO)-2):
            self.sendmessage(self.group, QUESTAO[i+1])
            sleep(1)

        self.resposta = QUESTAO[6]



    def getanswer(self, tentativa, sender):
        resp = tentativa[1]
        
        print('tentaram responder. %s' % self.resposta)
        print(resp)
        print(sender)
        print(self.SCORES)
        for I in range(len(self.SCORES)):
            if sender in self.SCORES[I][0]:
                        
                if resp in self.resposta.lower()[:2]:
                    self.sendmessage(self.group, '%s acertou mlk' % sender)
                    self.SCORES[I][1]+=1

                    self.sendmessage(self.group, '%s já soma %i pontos.. sapoha eh meu orgulho.' % (sender, self.SCORES[I][1]))
                    if self.SCORES[I][1] == 5:
                        self.fim(sender)
                            
                    
                else:
                    self.sendmessage(self.group, '%s errou!, está eliminado, ke pena... sintam o cheiro do fracasso.' % sender)
                    self.SCORES.pop(I)
                    
                if (self.questoesN > 20) or (self.SCORES==1):
                    self.fim(0)
                    return
                self.mandar_questao()       
                break
    def fim(self, won):
        self.sendmessage(self.group, 'fim do vestiba... me entrega o envelope dos vencedores, darlene.')
        if won == 0:
            self.sendmessage(self.group, 'voces todos perderam, são burros pra krl! não vo zoar pq devem ter tido alguma doença grave na infância.')

        else:
            self.sendmessage(self.group, '%s ganhou! meus parabens seu retardado!' % won)
        self.BOT.ONvestibular = 0

    def sendpic(self, picurl):
        
        filename = 'vestibacache.jpg'
        FILE = urlopen(picurl)
        Fo = open(filename, 'wb')
        Fo.write(FILE.read())
        Fo.close()
        
        self.CLI.image_send(group, filename)
        
def vestibular_questao():

    URL = 'http://www.professor.bio.br/'

    CATEGORY = ['portugues', '', 'geografia', 'quimica']

    SEARCH = ['bicho', 'inseto', 'pedra', 'molecula']

    _C=randrange(len(CATEGORY))


    URL += CATEGORY[_C]
    URL += '/search.asp?search='+ SEARCH[_C]

    #print(URL)

    SOURCE = urlopen(URL).read().decode('latin-1', 'ignore')

    questions = [m.start() for m in re.finditer('pergunta:', SOURCE)]

    Z = questions[randrange(len(questions))]
    Z+=9

    K = SOURCE.find('<strong>', Z)


    Zr = SOURCE.find('resposta:',K)
    Zr+=9

    Kr = SOURCE.find('<br>', Zr)

    IMG = SOURCE[Z:K].find('img src=')
    if IMG >-1:
        IMGe = SOURCE[Z:K].find('>', IMG)
        IMG = SOURCE[IMG:IMGe]
        try:
            openurl(IMG)
        except ValueError:
            return vestibular_questao()
    

    PERGUNTA = re.compile(r'<[^>]+>').sub('', SOURCE[Z:K].replace('<br>','\n'))

    if PERGUNTA.find('e)') == -1: return vestibular_questao()

    rA = PERGUNTA[PERGUNTA.find('a)'):PERGUNTA.find('b)')]
    rB = PERGUNTA[PERGUNTA.find('b)'):PERGUNTA.find('c)')]
    rC = PERGUNTA[PERGUNTA.find('c)'):PERGUNTA.find('d)')]
    rD = PERGUNTA[PERGUNTA.find('d)'):PERGUNTA.find('e)')]
    rE = PERGUNTA[PERGUNTA.find('e)'):]

    PERGUNTA = PERGUNTA[:PERGUNTA.find('a)')]

    RESPOSTA = re.compile(r'<[^>]+>').sub('', SOURCE[Zr:Kr])



    QUESTION = [PERGUNTA,rA,rB,rC,rD,rE,RESPOSTA]   

    for T in range(len(QUESTION)):
        QUESTION[T]=QUESTION[T].replace('&quot', '').replace('\r','').strip()
        QUESTION[T] =" ".join(QUESTION[T].split())
        
        if ('e)' in QUESTION[T]) and ('.' in QUESTION[T]):
            X = QUESTION[T].find('.')
            QUESTION[T] = QUESTION[T][:X]

    if not IMG == -1:
        QUESTION.append(IMG)

    return QUESTION            
            
class Retrieve():
    def __init__(self, CALLWORD, URL, FTRIM='',BTRIM='', FRTRIM='', BRTRIM='', REBOUND_KEY=b'032442301sda1sd', ERROR_KEY=b'koytr1we0ewrt', FUNCTYPE='keyword', CHARSET='latin-1'):
        
        self.URL = URL
        self.TRIGGER_WORD = CALLWORD
        
        self.FRONT_TRIM = FTRIM
        self.BACK_TRIM = BTRIM
        self.FRONT_REBOUND_TRIM = FRTRIM
        self.BACK_REBOUND_TRIM = BRTRIM


        self.CHARSET = CHARSET
        
        self.ERROR_KEY = ERROR_KEY
        self.TIMER = 13
        self._TIMER = 0

        self.TYPE = FUNCTYPE
    def trigger(self, IN):
        if self.TRIGGER_WORD in IN:
            word = IN.split(' ')
            print('Processing call %s %s' % (self.TRIGGER_WORD, word[1]))
            return self.retrieve(word[1])

    def retrieve(self, word):

        
        #word = ''.join(c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn')
        try:
            
            SOURCE = urlopen(self.URL + quote(word)).read()#.decode('latin-1', 'ignore')
        except urllib.error.HTTPError:
            return 'Non ecsiste.'


        if self.ERROR_KEY in SOURCE:
            Z = SOURCE.find(self.FRONT_REBOUND_TRIM)
            Z += len(self.FRONT_REBOUND_TRIM)
            K = SOURCE.find(self.BACK_REBOUND_TRIM, Z)


            print(SOURCE[Z:K])
            print(SOURCE[Z:K].decode('UTF-8', 'ignore'))
            print(SOURCE[Z:K].decode('latin-1', 'ignore'))
            SOURCETO = self.URL.encode('UTF-8', 'ignore')
            SOURCE = SOURCETO.decode('unicode_escape', 'ignore') + quote(SOURCE[Z:K])
            #print(SOURCE)
     
            SOURCE = urlopen((SOURCE),timeout=20).read()#.decode('latin-1', 'ignore')
        

        Z = SOURCE.find(self.FRONT_TRIM)

        K = SOURCE.find(self.BACK_TRIM, Z)

                                
        CONTENT = re.compile(r'<[^>]+>').sub('', SOURCE[Z:K].decode(self.CHARSET,'ignore'))

        return CONTENT




AUTO_RETRIEVE=[]

AUTO_RETRIEVE.append(Retrieve('@dict', 'http://www.dicio.com.br/pesquisa.php?q=', FTRIM=b'</h2>', BTRIM=b'<h2 class="tit-section">',
                              FRTRIM=b'href="', BRTRIM=b'">', REBOUND_KEY=b'class="resultados">', ERROR_KEY = b'o foram encontradas'))

AUTO_RETRIEVE.append(Retrieve('@indict', 'http://www.dicionarioinformal.com.br/', FTRIM=b'<p class="text-justify">', BTRIM=b'</p>',
                FRTRIM=b'<div class="di-blue-link" style="font-size:20px;"><a href="', BRTRIM=b'"', REBOUND_KEY = b'Nenhuma Defini'))

AUTO_RETRIEVE.append(Retrieve('@wiki', 'https://pt.wikipedia.org/wiki/', FTRIM=b'<p>', BTRIM=b'</p>', FRTRIM=b'<span class="searchmatch>', BRTRIM=b'</span>',
                              REBOUND_KEY= b'A mostrar resultados para', ERROR_KEY = b'o produziu resultados.', CHARSET='UTF-8'))

