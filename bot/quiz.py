#!/bin/python
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
        
