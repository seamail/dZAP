#!/usr/bin/python

import os.path
from urllib.request import urlopen
from random import *
import re
from time import *
from subprocess import call
import unicodedata
import urllib

import json

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def retrieve_joke():
    url = "http://www.piadas.com.br"
    content = urlopen(url + "/piadas-engracadas").readlines()
    category = []
    for line in content:
        if b'views-field views-field-name' in line:

            z = line.find(b'<a href="')
            if z >= 0:
                k = line.find(b'">', z)
                category.append(line[z + 9:k])
    #print(category)

    chosen_cat = category[randrange(len(category))].decode("UTF-8")

    cat_content = urlopen(url + chosen_cat).readlines()
    joke = []

    for line in cat_content:
        if b'Continuar Lendo' in line:
            z = line.find(b'<a href="')
            if z >= 0:
                k = line.find(b'" class=', z)
                joke.append(line[z + 9:k])

        if b'No momento, ' in line:
            retrieve_joke()
            return

    chosen_joke = joke[randrange(0, len(joke))].decode("UTF-8")

    print(url + chosen_joke)

    try:
        joke_content = urlopen(url + chosen_joke).read().decode("UTF-8")
    except UnicodeDecodeError:
        print("decoding failed.")
        return retrieve_joke()
    except urllib.error.HTTPError:
        print("failed to reach %s" % url+chosen_joke)
        return ""

    z = joke_content.find('<div class="field-items" id="md4">')
    k = joke_content.find(
        '<div class="field field-name-gostei field-type-ds field-label-hidden')

    joke_text = re.compile(r'<[^>]+>').sub('', joke_content[z:k])

    if ("iframe" in joke_text) or (len(joke_text) < 60):
        print("failed.")
        return retrieve_joke()

    return joke_text


def psicologo(kind):
    url = 'http://pensador.uol.com.br/blog.php?t='

    kinds = ['fm', 'fa', 'fs']

    MOTIVACIONAL = urlopen(url + kinds[kind]).read().decode("UTF-8")

    z = MOTIVACIONAL.find('"')
    k = MOTIVACIONAL.find('<br/>')

    MOTIVACIONAL = re.compile(r'<[^>]+>').sub('', MOTIVACIONAL[z + 1:k])

    MOTIVACIONAL = MOTIVACIONAL.replace(')', '').replace('\n', '').replace(
        '&quot;', '').replace('"', '')

    return MOTIVACIONAL


def wikipedia():
    url = "https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria"

    content = urlopen(url).read()
    tag_re = re.compile(r'<[^>]+>')

    z = content.find(b'<p>')
    k = content.find(b'</p>')

    paragraph = content[z + 3:k].decode("UTF-8")
    print(paragraph)

    paragraph = tag_re.sub('', paragraph)

    if len(paragraph) < 8:
        return wikipedia()
    else:
        return paragraph


def retrieve_porn(category):
    url = 'http://www.pornpics.com/recent'

    categories = {
        'normal': '',
        'ruiva': '/redhead/',
        'soft': '/stripper/',
        'lesbian': '/lesbian/',
        'ebony': '/ebony/',
    }

    url = url + categories[category]

    content = urlopen(url).read().decode("UTF-8")

    if os.path.isfile('USEDporn'):
        used = open('USEDporn', 'r').read()
    else:
        used = ''

    photos_array = [
        m.start() for m in re.finditer('http://content.pornpics.com', content)
        ]

    pic_url = ""
    x = 0
    while pic_url in used:
        number = randrange(len(photos_array))
        z = photos_array[number]

        pic_url = content[z:z + 120]

        k = pic_url.find('.jpg') + 4

        pic_url = pic_url[:k]

        filename = 'porncache.jpg'

        print('>>>>' + pic_url)
        x += 1
        if x > 30:
            return

    used = open('USEDporn', 'a+')

    used.write(pic_url + '\n')
    file_ = urlopen(pic_url)
    fo = open(filename, 'wb')
    fo.write(file_.read())
    fo.close()
    used.close()
    return filename


def create_voice(text):
    filepath = 'sound.wav'

    text = text.replace('ç', 'ss').replace('á', 'ah')[:-1]
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if
                   unicodedata.category(c) != 'Mn')
    text = str(text.encode('ascii', 'ignore'))

    print('>>>>>>>>' + text)

    e = 'echo "' + text + '" | espeak -v brazil -w "' + filepath + '"'
    call(e, shell=True)
    sleep(3)

    return filepath


def retrieve_salmo():
    index = randrange(1, 150)
    url = 'http://salmos.a77.com.br/salmos/salmo_%i.php' % index

    page = urlopen(url).read()

    z = page.find(b'<img src="salmo-da-biblia-sagrada.gif"')

    k = page.find(b'<a href="index.php">+Salmos</a>')

    page = page[z:k].decode('utf-8', 'ignore')

    salmo = re.compile(r'<[^>]+>').sub('', page[z:k])

    return salmo

def createLike(text):

    if len(text) > 40:
        return "Texto gigante demais, não será possivel."
    textsplit = text.split(" ")

    s0 = []
    s = ["","","",""]
    for k in range(4):
        s0.append("")
    I=0
    for word in textsplit:
        if len(s0[I] + word) > 9:
            I += 1
        s0[I] += " " + word

    if len(s0) == 4:
        for l in range(len(s0)):
            s[l] = s0[l]
    elif len(s0) < 4:
        for l in range(len(s0)):
            s[l + 1] = s0[l]


    for i in range(len(s)):
        x = 10 - len(s[i])
        x //= 2
        s[i] = "░"*x + s[i] + "░"*x
        if len(s[i]) < 10:
            s[i] += "░"
    like = """
            ▄▄
           █░░█
           █░░█
          █░░░█
         █░░░░█
███████▄▄█░░░░░██████▄
▓▓▓▓▓▓█░░░░░░░░░░░░░█
▓▓▓▓▓▓█░░%s░░█
▓▓▓▓▓▓█░░%s░░█
▓▓▓▓▓▓█░░%s░░█
▓▓▓▓▓▓█░░%s░░█
▓▓▓▓▓▓█████░░░░░░░░░█
██████▀░░░░▀▀██████▀""" % (s[0],s[1],s[2],s[3])


    return like

def markovAdd(text):
    Fo = open('../markovData.txt', 'a+')
    Fo.write(text)
    Fo.close()
class Vestibular():
    def __init__(self, group, participants, cli, bot):
        self.scores = []
        self.group = group
        self.participants = participants
        self.cli = cli

        self.bot = bot
        self.resposta = ''

        self.questoesN = 0
        for participant in participants:
            self.scores.append([participant, 0])

        self.mandar_questao()

    def sendmessage(self, to, msg):
        self.cli.message_send(to, msg)

    def mandar_questao(self):
        self.questoesN += 1

        self.ONvestibular = 1

        questao = vestibular_questao()
        print(questao)
        self.cli.image_send(self.group, questao[0])

        if len(questao) > 7:
            self.sendpic(questao[7])

        self.resposta = questao[1]

    def getanswer(self, tentativa, sender):
        if len(tentativa) < 2: return
        resp = tentativa[1]

        print('tentaram responder. %s' % self.resposta)
        print(resp)
        print(sender)
        print(self.scores)

        for I in range(len(self.scores)):
            if sender in self.scores[I][0]:

                if resp in self.resposta.lower()[:2]:
                    self.scores[I][1] += 1

                    msg = '%s acertou e já soma %i pontos.. sapoha eh meu ' \
                          'orgulho.' % (sender, self.scores[I][1])
                    self.sendmessage(
                        self.group,
                        msg,
                    )
                    if self.scores[I][1] == 5:
                        self.fim(sender)
                    self.mandar_questao()
                    return

                else:
                    self.sendmessage(
                        self.group,
                        '%s errou!, está eliminado, ke pena... sintam o cheiro '
                        'do fracasso.' % sender,
                    )
                    self.scores.pop(I)
                    return
                break

    def fim(self, won):
        self.sendmessage(
            self.group,
            'fim do vestiba... me entrega o envelope dos vencedores, darlene.',
        )
        if won == 0:
            self.sendmessage(
                self.group,
                'voces todos perderam, são burros pra krl! não vo zoar pq '
                'devem ter tido alguma doença grave na infância.',
            )

        else:
            self.sendmessage(
                self.group,
                '%s ganhou! meus parabens seu retardado!' % won,
            )
        self.bot.ONvestibular = 0

    def sendpic(self, pic_url):
        filename = 'questioncache.jpg'
        file_ = urlopen(pic_url)
        fo = open(filename, 'wb')
        fo.write(file_.read())
        fo.close()

        self.cli.image_send(self.group, filename)


def vestibular_questao():
    url = 'http://www.professor.bio.br/'

    category = ['portugues', '', 'geografia', 'quimica']

    search = ['bicho', 'inseto', 'pedra', 'molecula']

    _c = randrange(len(category))

    url += category[_c]
    url += '/search.asp?search=' + search[_c]

    source = urlopen(url).read().decode('latin-1', 'ignore')

    questions = [m.start() for m in re.finditer('question:', source)]

    z = questions[randrange(len(questions))]
    z += 9

    k = source.find('<strong>', z)

    zr = source.find('resposta:', k)
    zr += 9

    kr = source.find('<br>', zr)

    img = source[z:k].find('img src=')
    if img > -1:
        imge = source[z:k].find('>', img)
        img = source[img:imge]
        try:
            urlopen(img)
        except ValueError:
            return vestibular_questao()
        except urllib.error.URLError:
            return vestibular_questao()

    question = re.compile(r'<[^>]+>').sub('', source[z:k].replace('<br>', '\n'))

    if question.find('e)') == -1: return vestibular_questao()

    alterns = [
        question[question.find('a)'):question.find('b)')],
        question[question.find('b)'):question.find('c)')],
        question[question.find('c)'):question.find('d)')],
        question[question.find('d)'):question.find('e)')],
        question[question.find('e)'):]]

    question = question[:question.find('a)')]

    resposta = re.compile(r'<[^>]+>').sub('', source[zr:kr])

    shuffle(alterns)
    letters = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e'}

    ra = 0
    for A in range(len(alterns)):

        if (alterns[A][0] in resposta[:3].lower()) and (ra == 0):
            ra = 1

        alterns[A] = letters[A] + alterns[A][1:]
        if ra == 1:
            print('mudando resposta de %s para %s.' % (resposta, letters[A]))
            resposta = '[' + letters[A] + ']]'
            ra = -1

    question = [question]
    for alt in alterns:
        question.append(alt)
    question.append(resposta)

    for T in range(len(question)):
        question[T] = question[T].replace('&quot', '').replace('\r', '').strip()
        question[T] = " ".join(question[T].split())

        if ('e)' in question[T]) and ('.' in question[T]):
            x = question[T].find('.')
            question[T] = question[T][:x]

    if not img == -1:
        question.append(img)

    text = ''

    for q in range(6):
        marker = 0
        breaks = []
        for I in range(len(question[q])):
            marker += 1
            if marker > 36:
                if (question[q][I] == ',') or (question[q][I] == '.'):
                    breaks.append(I + 1)
                    marker = 0

        breaks = list(reversed(breaks))
        for b in breaks:
            question[q] = question[q][:b] + '\n' + question[q][b + 1:]

    for x in range(6):
        text += question[x] + '\n \n'

    font = ImageFont.truetype('arial.ttf', 16)
    draw = ImageDraw.Draw(Image.new("RGBA", (800, 600), (255, 255, 255)))
    img = Image.new("RGBA", draw.textsize(text, font=font), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.text((0, 0), text, (0, 0, 0), font=font)

    draw = ImageDraw.Draw(img)
    img.save("questioncache.jpg")

    return ['questioncache.jpg', resposta]

def retrieve_locality(Ilat,Ilng):
    mult = [-1,1]
    V = randrange(0,1)
    lat = Ilat + uniform(0,2)*mult[V]
    V = randrange(0,1)
    lng = Ilng + uniform(0,2)*mult[V]

    URL = "http://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+','+str(lng)+"&sensor=false"
    Content = urllib.request.urlopen(URL).read().decode('utf-8')
    jsondata = json.loads(Content)

    Result = []
    
    if len(jsondata["results"]) ==0:
        return retrieve_locality(Ilat,Ilng)
    
    result = jsondata["results"][0]

    if len(result["address_components"]) < 2:
        return retrieve_locality(Ilat,Ilng)        
        
    for component in result["address_components"]:
        #if 'administrative_area_level_2' in component["types"]:
            #print('>>> %s' % component['short_name'])
            #Result.append(component['short_name'])
        if 'administrative_area_level_1' in component["types"]:
            #print('>>> %s' % component['short_name'])
            Result.append(component['short_name'])
        if 'locality' in component["types"]:
            #print('>> %s' % component['short_name'])
            Result.append(component['short_name'])
    if len(Result) < 2:
        return retrieve_locality(Ilat,Ilng)
    Result.append([lat,lng])

    middlelat = (Ilat - lat)/2
    middlelat = middlelat + lat
    middlelng = (Ilng - lng)/2
    middlelng = middlelng + lng

    print("Coord Origin: %f,%f   Middle: %f,%f   Destination: %f,%f" %
          (Ilat,Ilng,middlelat,middlelng,lat,lng))
    
    Result.append([middlelat,middlelng])
    
    return Result


def retrieve_codigoPenal(art):
    URL = "http://www.planalto.gov.br/ccivil_03/decreto-lei/Del2848compilado.htm"
    print("searching for art %s" % art)
    if art[-1] == '\n':
        art=art[:-1]
    try:
        source = urlopen(URL).read()
    except:
        return "Fail."

    R = "Art. %s" % art
    K = "</font>"

    Rx = source.find(R)
    Kx = source.find(K, beg=Rx)

    txtArt = source[Rx + len(R):Kx]
    
    print(">%s" % txtArt)
    return txtArt
        
