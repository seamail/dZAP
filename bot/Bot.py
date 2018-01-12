#!/bin/python
import os.path
from random import *
from time import *

from .core import create_voice, \
    wikipedia, retrieve_porn, retrieve_salmo, createLike, \
    markovAdd


from .Module import BotModule

from .modules import hippie
from .modules import joke
from .modules import quiz
from .modules import retrieve
from .modules import autochat
from .modules import helpmessage
from .modules import motivational

from urllib.request import urlopen


LOAD_CONVERSATION_BOT = True

class Bot:
    def __init__(self):
        current_time = time()

        self.Modules = [BotModule(joke, 13),
                        BotModule(motivational, 13)]

        self.ban_words = []
        self.load_ban_word()

        self.on_vestibular = 0

        self.window = None
        self.chat = None

        if LOAD_CONVERSATION_BOT:
            try:
                from bot.chat import Chatbrain
                self.chat = Chatbrain()
            except ImportError:
                self.chat = None
                print("Can't find Chatterbot module. Automatic conversation disabled.")

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
        if not self.window: return
        else:
            if not self.window.LOADED: return
        output = output.lower()
        current_time = time()

        #print(output[0])
        #print(output[1])


        for BWK in self.ban_words:
            if BWK[1] in output:
                return ["essezin disse a palavra banida, se fodeo."]
        if output.startswith('@'):
            for module in self.Modules:
                module.trigger(output)
        '''
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
            return helpmessage

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
        elif '@like' in output:
            return createLike(output[6:])
        elif '@art' in output:
            return retrieve_codigoPenal(output.split(" ")[1])
        for auto in AUTO_RETRIEVE:
            out = auto.trigger(output)
            if out:
                return out
        if self.chat and len(output):
            if output[0] == '>':
                self.chat.read(output[1:0])
                return self.chat.respond(output[1:])

            else:
                if len(output) < 46:
                    self.chat.read(output)
                    markovAdd(output)
                    rep = self.chat.respond(output)
                    if randrange(100) < self.window.BOTRESPONSE.get(): return rep
                    return
        '''

    def getCliLayer(self, layer):
        self.CliLayer = layer

    def sendmessage(self, to, msg):

        print(to)
        # send fragmented message as recommended yowsup version
        # cant send group messages bigger than 128 chars.
        while len(msg) > 127:
            self.CliLayer.message_send(to, msg[:127])
            msg = msg[128:]

        self.CliLayer.message_send(to, msg)

    def sendimage(self, to, url):
        filename = 'cache.jpg'
        file_ = urlopen(url)
        Fo = open(filename, 'wb')
        Fo.write(file_.read())
        Fo.close()

        self.CliLayer.image_send(to, filename)

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
                address = g.address
                break

        if party:
            print(party)
            x = randrange(len(party))
            print('len %i, x=%i' % (len(party), x))
            if randrange(100) == 1:
                self.CliLayer.group_promote(address, party[x][0])
            else:
                print(str(party[x]))
                self.CliLayer.group_kick(address, party[x][0])

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

