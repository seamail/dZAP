#!/bin/python
'''
        if '@kkk' in output:
            if 13.0 < float(current_time) - self.timer_p:
                self.timer_p = current_time
                self.rep_p = 1
                return retrieve_joke()
            elif self.rep_p:
                self.rep_p = 0
                self.timer_p = current_time
                return "por que você não conta uma aí agora, fdp?"
'''
def trigger(message):
    if '@kkk' in message:
        return retrieve_joke()

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

