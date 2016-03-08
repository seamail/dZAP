from urllib.request import urlopen
import re

import urllib
from urllib.parse import quote

from random import randrange

class _Retrieve:

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
            Mftrim = None,
            Mbtrim = '"'
    ):
        self.url = url
        self.trigger_word = callword

        self.front_trim = ftrim
        self.back_trim = btrim
        self.front_rebound_trim = frtrim
        self.back_rebound_trim = brtrim

        self.menu_trim = Mftrim
        self.menu_back_trim = Mbtrim

        self.charset = charset

        self.error_key = error_key

    def trigger(self, IN):
        if self.trigger_word in IN:
            word = IN.split(' ')
            print('Processing call %s %s' % (self.trigger_word, word[1]))
            return self.retrieve(word[1])

    def submenu(self):
        source = self.url

        table = [m.start() for m in re.finditer(self.menu_front_trim, source)]
        results = []
        
        for Z in table:
            K = source.find(self.menu_back_trim, Z)
            results.append(source[Z:K])

        X = randrange(len(results))

        self.retrieve('x')#,url=self.url+results[X])
                


    
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
            source_to = url.encode('UTF-8', 'ignore')
            source = source_to.decode('unicode_escape', 'ignore') + \
                     quote(source[z:k])

            source = urlopen(source, timeout=20).read()
        z = source.find(self.front_trim)
        k = source.find(self.back_trim, z)

        content = re.compile(r'<[^>]+>') \
            .sub('', source[z:k].decode(self.charset, 'ignore'))

        return content


_RETRIEVER_DICIO = _Retrieve(
    '@dict',
    'http://www.dicio.com.br/pesquisa.php?q=',
    ftrim=b'</h2>',
    btrim=b'<h2 class="tit-section">',
    frtrim=b'href="',
    brtrim=b'">',
    error_key=b'o foram encontradas'
)


_RETRIEVER_DICIONARIO_INFORMAL = _Retrieve(
    '@indict',
    'http://www.dicionarioinformal.com.br/',
    ftrim=b'<p class="text-justify">',
    btrim=b'</p>',
    frtrim=b'<div class="di-blue-link" style="font-size:20px;"><a href="',
    brtrim=b'"',
)


_RETRIEVER_WIKI = _Retrieve(
    '@wiki',
    'https://pt.wikipedia.org/wiki/',
    ftrim=b'<p>',
    btrim=b'</p>',
    frtrim=b'<span class="searchmatch>',
    brtrim=b'</span>',
    error_key=b'o produziu resultados.',
    charset='UTF-8',
)

_RETRIEVER_JOKE = _Retrieve(
    '@kkk',
    'https://www.piadas.com.br',
    
)

AUTO_RETRIEVE = (
    _RETRIEVER_DICIO,
    _RETRIEVER_DICIONARIO_INFORMAL,
    _RETRIEVER_WIKI,
)
