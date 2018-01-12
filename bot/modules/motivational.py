#!/bin/python

def trigger(message):
    keywords = ['sad', 'pensa', 'love']
    for W in range(len(keywords)):
        if keywords[W] in message:
            return psicologo(W)

timerfailmessage = "calem a boca, vocês me contaminam com essa depressão"

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

