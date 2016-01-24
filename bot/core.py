#!/usr/bin/python

import os.path
from urllib.request import urlopen
from random import *
import re
from time import *
from subprocess import call

import unicodedata

import urllib
from urllib.parse import quote

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Bot():
    def __init__(self):
        current_time = time()
        self.timer_p = current_time - 13.0
        self.timer_s = current_time - 13.0
        self.timer_n = current_time - 13.0

        self.rep_p = 1
        self.rep_s = 1
        self.rep_n = 1

        self.ban_words = []
        self.load_ban_word()

        self.on_vestibular = 0

        self.window = None

    def load_ban_word(self):
        if not os.path.isfile('banword.txt'):
            return
        ban_word_file = open('banword.txt', 'r')

        for line in ban_word_file.readlines():
            line = line.split('=')
            if len(line) > 1:
                if line[1][-1] == '\n':
                    line[1] = line[1][:-1]
                self.ban_words.append([line[0], line[1]])

    def read_output(self, output, sender, participant):
        output = output.lower()
        current_time = time()

        for BWK in self.ban_words:
            if BWK[1] in output:
                return ["essezin disse a palavra banida, se fodeo."]
        if '@kkk' in output:
            if 13.0 < float(current_time) - self.timer_p:
                self.timer_p = current_time
                self.rep_p = 1
                return retrieve_joke()
            elif self.rep_p:
                self.rep_p = 0
                self.timer_p = current_time
                return "por que você não conta uma aí agora, fdp?"
        elif ('@sad' in output) or ('@pensa' in output) or ('@love' in output):
            if float(current_time) - self.timer_s > 13.0:
                self._log_command('sad', True)

                self.timer_s = current_time
                self.rep_s = 1
                kind = ['@sad', '@pensa', '@love']
                for Ki in range(len(kind)):
                    if kind[Ki] in output:
                        if '!' in output:
                            return create_voice(psicologo(Ki))
                        else:
                            return psicologo(Ki)
            elif self.rep_s:
                self._log_command('sad', False)

                self.rep_s = 0
                self.timer_s = current_time
                return "calem essa boca, voces me contaminam com essa " \
                       "depressão."
        elif '@nerd' in output:
            if float(current_time) - self.timer_n > 13.0:
                self._log_command('nerd', True)

                self.timer_n = current_time
                self.rep_n = 1
                return wikipedia()
            elif self.rep_n:
                self._log_command('nerd', False)

                self.rep_n = 0
                self.timer_n = current_time
                return "vai pegar um livro, seu mongolão."
        elif '@xinga ' in output:
            x = output.find('@xinga')
            word = output[x + 7:]
            if " " in word:
                word = word.split(" ")
                word = word[0]

            if len(word) > 4:
                user_has_ban_word = 0

                for bw in self.ban_words:
                    if bw[0] == sender:
                        bw[1] = word.lower()
                        user_has_ban_word = 1

                if user_has_ban_word == 0:
                    self.ban_words.append([sender, word])

                ban_word_file = open('banword.txt', 'w')
                for ban_word in self.ban_words:
                    ban_word_file.write(ban_word[0] + "=" + ban_word[1] + '\n')
                ban_word_file.close()

                return word + " agora é uma palavra banida."
            else:
                return word + " é uma palavra muito curta, seu fela."

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
            msg = """koeh.. sou o adolfo gomes, seu novo amiguinho. Digite @kkk para rir um pouquinho;\n
            @sad se voce estiver se sentindo um lixo.\n
            @nerd pra estudar uns skemas.\n
            @porn pra receber umas pornografias estranhas.\n
            @nerd para obter um pedaço inútil de informação útil.\n
            @dict [palavra] ou @indict [palavra] pra consultar um desses dois dicionários poderosos da língua portuguesa.
            @jesus pra ouvir um pouco da palavra de DEUS.\n
            @diz [frase] q eu te mando um áudio falando tal frase;\n
            @enema pra se inscrever no meu vestibular lixo.\n
            E é só isso mermo seus troxa."""
            return msg
        elif '@diz' in output:
            x = output.find('@diz') + 4
            word = output[x + 5:]
            return create_voice(word)
        elif ('@jesus' in output) or ('@god' in output):
            return retrieve_salmo()
        elif '@drugs' in output:
            pass
        elif '@enema' in output:
            if self.on_vestibular == 0:
                print('going vestibular.')
                self.govestibular(sender)
        elif '#' in output:
            if self.on_vestibular:
                self.on_vestibular.getanswer(output, participant)
        elif '@roleta' in output:
            self.roleta_russa(sender)
            return
        for auto in AUTO_RETRIEVE:
            out = auto.trigger(output)
            if auto.trigger(output):
                return out

    def getCliLayer(self, layer):
        self.CliLayer = layer

    def sendmessage(self, to, msg):
        self.CliLayer.message_send(to, msg)

    def govestibular(self, group):
        party = None
        if not self.window:
            print('no window.')
            return

        print(group)
        for G in self.window.GROUPS:
            print('>' + G.address)
            if G.address in group:
                party = G.PARTICIPANTS

        if party:
            self.on_vestibular = Vestibular(group, party, self.CliLayer, self)

    def roleta_russa(self, group):
        party = None
        print(group)
        for g in self.window.GROUPS:
            if g.address in group:
                print('>' + g.address)
                party = list(g.PARTICIPANTS.items())
                addr = g.address
                break

        if party:
            print(party)
            x = randrange(len(party))
            print('len %i, x=%i' % (len(party), x))
            if randrange(100) == 1:
                self.CliLayer.group_promote(addr, party[x][0])
            else:
                print(str(party[x]))
                self.CliLayer.group_kick(addr, party[x][0])

    def _log_command(self, command_name, was_granted):
        current_time = time()
        if was_granted:
            status_text = 'granted'
        else:
            status_text = 'denied'
        print(
            '@{} {}. current current_time is {} and buffer current_time is {}'
                .format(
                command_name,
                status_text,
                str(current_time),
                str(self.timer_s),
            ),
        )


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

    chosen_cat = category[randrange(0, len(category))].decode("UTF-8")

    cat_content = urlopen(url + chosen_cat).readlines()
    joke = []

    for line in cat_content:
        if b'Continuar Lendo' in line:
            z = line.find(b'<a href="')
            if z >= 0:
                k = line.find(b'">', z)
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
    WIKIP = "https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria"

    content = urlopen(WIKIP).read()
    TAG_RE = re.compile(r'<[^>]+>')

    z = content.find(b'<p>')
    k = content.find(b'</p>')

    paragraph = content[z + 3:k].decode("UTF-8")
    print(paragraph)

    paragraph = TAG_RE.sub('', paragraph)

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

    porn_src = url + categories[category]

    content = urlopen(porn_src).read().decode("UTF-8")

    if os.path.isfile('USEDporn'):
        used = open('USEDporn', 'r').read()
    else:
        used = ''

    photosarray = [
        m.start() for m in re.finditer('http://content.pornpics.com', content)
        ]

    picurl = ""
    x = 0
    while picurl in used:
        number = randrange(len(photosarray))
        z = photosarray[number]

        picurl = content[z:z + 120]

        k = picurl.find('.jpg') + 4

        picurl = picurl[:k]

        filename = 'porncache.jpg'

        print('>>>>' + picurl)
        x += 1
        if x > 30:
            return

    used = open('USEDporn', 'a+')

    used.write(picurl + '\n')
    file_ = urlopen(picurl)
    fo = open(filename, 'wb')
    fo.write(file_.read())
    fo.close()
    used.close()
    return filename


def create_voice(text):
    FILEPATH = 'sound.wav'

    text = text.replace('ç', 'ss').replace('á', 'ah')[:-1]
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if
                   unicodedata.category(c) != 'Mn')
    text = str(text.encode('ascii', 'ignore'))

    print('>>>>>>>>' + text)

    e = 'echo "' + text + '" | espeak -v brazil -w "' + FILEPATH + '"'
    call(e, shell=True)
    sleep(3)

    return FILEPATH


def retrieve_salmo():
    index = randrange(1, 150)
    src = 'http://salmos.a77.com.br/salmos/salmo_%i.php' % index

    page = urlopen(src).read()

    z = page.find(b'<img src="salmo-da-biblia-sagrada.gif"')

    k = page.find(b'<a href="index.php">+Salmos</a>')

    page = page[z:k].decode('utf-8', 'ignore')

    salmo = re.compile(r'<[^>]+>').sub('', page[z:k])

    return salmo


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

    def sendpic(self, picurl):
        filename = 'questioncache.jpg'
        file_ = urlopen(picurl)
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

    questions = [m.start() for m in re.finditer('pergunta:', source)]

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

    pergunta = re.compile(r'<[^>]+>').sub('', source[z:k].replace('<br>', '\n'))

    if pergunta.find('e)') == -1: return vestibular_questao()

    alterns = []
    alterns.append(pergunta[pergunta.find('a)'):pergunta.find('b)')])
    alterns.append(pergunta[pergunta.find('b)'):pergunta.find('c)')])
    alterns.append(pergunta[pergunta.find('c)'):pergunta.find('d)')])
    alterns.append(pergunta[pergunta.find('d)'):pergunta.find('e)')])
    alterns.append(pergunta[pergunta.find('e)'):])

    pergunta = pergunta[:pergunta.find('a)')]

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

    question = [pergunta]
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


class Retrieve():
    def __init__(
            self,
            callword,
            url,
            ftrim='',
            btrim='',
            frtrim='',
            brtrim='',
            error_key=b'koytr1we0ewrt',
            charset='latin-1',
    ):
        self.url = url
        self.trigger_word = callword

        self.front_trim = ftrim
        self.back_trim = btrim
        self.front_rebound_trim = frtrim
        self.back_rebound_trim = brtrim

        self.charset = charset

        self.error_key = error_key

    def trigger(self, IN):
        if self.trigger_word in IN:
            word = IN.split(' ')
            print('Processing call %s %s' % (self.trigger_word, word[1]))
            return self.retrieve(word[1])

    def retrieve(self, word):
        try:
            source = urlopen(
                self.url + quote(word)).read()  # .decode('latin-1', 'ignore')
        except urllib.error.HTTPError:
            return 'Non ecsiste.'

        if self.error_key in source:
            z = source.find(self.front_rebound_trim)
            z += len(self.front_rebound_trim)
            k = source.find(self.back_rebound_trim, z)

            print(source[z:k])
            print(source[z:k].decode('UTF-8', 'ignore'))
            print(source[z:k].decode('latin-1', 'ignore'))
            source_to = self.url.encode('UTF-8', 'ignore')
            source = source_to.decode('unicode_escape', 'ignore') + \
                 quote(source[z:k])

            source = urlopen(source, timeout=20).read()
        z = source.find(self.front_trim)
        k = source.find(self.back_trim, z)

        content = re.compile(r'<[^>]+>') \
            .sub('', source[z:k].decode(self.charset, 'ignore'))

        return content


AUTO_RETRIEVE = []

AUTO_RETRIEVE.append(
    Retrieve(
        '@dict',
        'http://www.dicio.com.br/pesquisa.php?q=',
        ftrim=b'</h2>',
        btrim=b'<h2 class="tit-section">',
        frtrim=b'href="',
        brtrim=b'">',
        error_key=b'o foram encontradas'
    ),
)

AUTO_RETRIEVE.append(
    Retrieve(
        '@indict',
        'http://www.dicionarioinformal.com.br/',
        ftrim=b'<p class="text-justify">',
        btrim=b'</p>',
        frtrim=b'<div class="di-blue-link" style="font-size:20px;"><a href="',
        brtrim=b'"',
    ),
)

AUTO_RETRIEVE.append(
    Retrieve(
        '@wiki',
        'https://pt.wikipedia.org/wiki/',
        ftrim=b'<p>',
        btrim=b'</p>',
        frtrim=b'<span class="searchmatch>',
        brtrim=b'</span>',
        error_key=b'o produziu resultados.',
        charset='UTF-8',
    ),
)
