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
    


