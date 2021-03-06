#!/usr/bin/python
import warnings
warnings.filterwarnings("ignore")

import os
from threading import *
from time import *
import datetime

from tkinter import *
from yowsup import env
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YOWSUP_CORE_LAYERS
from yowsup.stacks import YOWSUP_FULL_STACK
from yowsup.stacks import YowStack
from yowsup.stacks import YowStackBuilder

from layer import YowsupCliLayer
from yowsup.layers import YowParallelLayer
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.layers.protocol_chatstate import YowChatstateProtocolLayer
from yowsup.layers.protocol_groups import YowGroupsProtocolLayer
from yowsup.layers.protocol_media import YowMediaProtocolLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.protocol_notifications import YowNotificationsProtocolLayer
from yowsup.layers.protocol_presence import YowPresenceProtocolLayer
from yowsup.layers.protocol_profiles import YowProfilesProtocolLayer
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
from yowsup.layers.axolotl import AxolotlSendLayer, AxolotlControlLayer, AxolotlReceivelayer
from yowsup.env import YowsupEnv



from interface import setupInterface
'''
 load credentials from the CREDENTIALS file in working folder.. template:
phone=*************
password=**********
'''
def retrieve_credentials():
    if os.path.isfile('CREDENTIALS'):
        _CRED = open('CREDENTIALS', 'r').readlines()
        PH = None
        PASS = None
        for line in _CRED:
            if 'phone' in line:
                PH = line.split('=')
                PH = PH[1].split('\n')[0]
            elif 'password' in line:
                PASS = line.split('=',1)
                PASS = PASS[1].split('\n')[0]

        if (PH) and (PASS):
            return (PH,PASS)

    return ('','')


CREDENTIALS = retrieve_credentials()


#if credentials are not provided by file, this window asks for them.
class auth_window():
    def __init__(self):
        self.run()

    def run (self):
        self.root = Tk()

        self.label_phone = Label(self.root, text='Phone:')
        self.label_phone.grid(column=0, row=0)
        self.label_pass = Label(self.root, text= 'Password:')
        self.label_pass.grid(column=0,row=1)
        self.txt_phone = Text(self.root, width=32, height=1)
        self.txt_phone.grid(column=1,row=0)
        self.txt_pass = Text(self.root, width= 32, height=1)
        self.txt_pass.grid(column=1,row=1)

        self.OK = Button(self.root, text='OK', command=self.auth)
        self.OK.grid(column=0,row=2, columnspan=2, sticky=E+W)

        self.root.wm_title('Authentication')
        self.root.mainloop()

    def auth (self):
        print((self.txt_phone.get('1.0',END),self.txt_pass.get('1.0',END)))
        global CREDENTIALS
        CREDENTIALS = (self.txt_phone.get('1.0',END)[:-1],self.txt_pass.get('1.0',END)[:-1])
        self.root.destroy()


#class for messages to be displayed on the GUI window.
class displayed_message(Frame):

    def __init__(self, FROM, DATE, text_content,master=None):
        Frame.__init__(self, master=master, height = 50)

        self.From=Label(master=self, text=FROM)
        self.From.grid(column = 2, row = 0)
        self.divisor=Label(master=self, text= " ||| ")
        self.divisor.grid(column = 1, row = 0)
        self.Date=Label(master=self,text=DATE)
        self.Date.grid(column = 0, row = 0, sticky=W)

        self.Content=Label(master=self,text=text_content)
        self.Content.grid(column = 0, row = 1, columnspan=2,sticky=W)
        self.spacer=Label(master=self,text="            ")
        self.spacer.grid(column = 0, row = 2)


#main window (GUI) class. It runs as a thread, to function indepently of the stdout stream generated by yowsup client/stacks.
class window(Thread):
    class group():
        def __init__(self, address, party, subject, index, master):
            self.address = address
            self.subject = subject

            self.label = Label(master)
            self.label['text'] = self.subject
            self.label.grid(column=0, row=index)

            self.ACT = Button(master)
            self.ACT['text'] = ' '
            self.ACT['activebackground'] = 'grey'
            self.ACT['command'] = self.activate
            self.ACT['background'] = 'black'
            self.ACT.grid(column=1, row=index)

            self.ACTIVE = 0

            self.PARTICIPANTS = party

        def activate(self):
            if self.ACTIVE == 1:
                self.ACTIVE = 0
                self.ACT['background'] = 'black'
                self.ACT['activebackground'] = 'dim grey'
            else:
                self.ACTIVE = 1
                self.ACT['background'] = 'olive drab'
                self.ACT['activebackground'] = 'yellow green'

    class automation():
        def __init__(self, triggerTXT, action):
            self.trigger = triggerTXT
            self.action = action

    def automate_window(self):
        self.auto_window = Tk()
        self.auto_window.VIEW = Canvas(self.auto_window).grid(row=0,column=0)
        self.auto_window.OK = Button(self.auto_window, text="save & close").grid(row=1,column=0)
        self.auto_window.wm_title(self.NAME + " [manage automation]")
        self.auto_window.mainloop()

    def __init__(self, YOWCLI):
        self.LOADED=0
        Thread.__init__(self)

        self.NAME = 'dZAP'
        self.start()
        self.connected=1
        self.contacts = {}

        self.GROUPS = []

        self.MSGREADINDEX = 0
        self.MSGABSINDEX = 0

        self.YOWCLI = YOWCLI

        

        self.SHOWNMESSAGE = []

    def callback(self):
        self.root.quit()

    def sendtext(self,event=None):
        self.refresh_message()
        sent=[]
        CONTENT = self.TEXTIN.get("1.0",END)[:-1]

        if event:
            for AUTO in AUTO_RETRIEVE:
                if AUTO.trigger_word == event:
                    print('>>>>'+CONTENT)
                    CONTENT = AUTO.retrieve(CONTENT)

        for GROUP in self.GROUPS:
            if GROUP.ACTIVE == 1:
                print(GROUP.address)
                MSG = self.YOWCLI.message_send(GROUP.address, CONTENT)
                sent.append(GROUP.subject)

        self.TEXTIN.delete(1.0, END)
        if len(sent) > 0:
            self.showmessage(MSG, TO = ">>> %s" % sent)

    def run(self):
        # this function is started on __init___,
        # because the window is a Thread. Initialize GUI and its widgets and menus.

        setupInterface(self, BOT)

        sleep(2)
        self.getinfo()
        self.LOADED = 1
        self.root.mainloop()

    def edit_profileSAVEQUIT(self, attribute):
        if attribute == 'nick':
            self.YOWCLI.presence_name(self.editprofile.TEXT.get('1.0',END)[:-1])
        elif attribute == 'status':
            self.YOWCLI.profile_setStatus(self.editprofile.TEXT.get('1.0',END).encode('utf-8'))
        elif attribute == 'image':
            self.YOWCLI.profile_setPicture(self.editprofile.TEXT.get('1.0',END).replace('\n', ''))
        else:
            for G in self.GROUPS:
                if G.ACTIVE:
                    if attribute == 'group name':
                        self.YOWCLI.group_setSubject(G.address, self.editprofile.TEXT.get('1.0',END)[:-1])
                    elif attribute == 'group image':
                        self.YOWCLI.group_picture(G.address, self.editprofile.TEXT.get('1.0',END)[:-1])

        self.editprofile.destroy()

    def edit_profile(self, attribute):
        self.editprofile = Tk()

        self.editprofile.TEXT = Text(self.editprofile,height=1)
        self.editprofile.TEXT.grid(column=0,row=0)
        self.editprofile.OK = Button(self.editprofile, text="save", command = lambda: self.edit_profileSAVEQUIT(attribute)).grid(column=0,row=1)

        if 'image' in attribute:
            self.editprofile.BROWSE = Button(self.editprofile, text='Browse', command = lambda: self.browsefiles(self.editprofile.TEXT)).grid(column=1,row=0)

        self.editprofile.wm_title('edit %s' % attribute)

    def browsefiles(self, target):#open the file finder dialog.
        target.delete('1.0', END)
        target.insert('1.0', filedialog.askopenfilename(title = "escolha a imagem.",))

    def refresh_message(self):
        while self.MSGREADINDEX < len(self.YOWCLI.MESSAGES):
            self.showmessage(self.YOWCLI.MESSAGES[self.MSGREADINDEX])
            self.MSGREADINDEX+=1

        self.MSGREADINDEX=0
        self.YOWCLI.MESSAGES = []

    def send_voice(self):#convert text input to synthetized voice, and send the file.
        for GROUP in self.GROUPS:
            if GROUP.ACTIVE == 1:
                create_voice(self.TEXTIN.get("1.0",END))
                sleep(1)
        self.TEXTIN.delete(1.0, END)

    def showmessage(self, message, TO = None):#refresh message viewing visor.
        INDEX = self.MSGABSINDEX*3
        
        if not message or not message.getType() == "text": return

        if not type(message.getBody) == str: 
            text_content = message.getBody()#.decode('utf-8', 'ignore')


        #for K in range(round(len(text_content)/60)):
        #    text_content = text_content[:60*K] + b'\n' + text_content[60*K:]

        if not message.getFrom():
            FROM = TO
        else:
            FROM = message.getFrom()
            for G in self.GROUPS:
                if G.address in FROM:
                    FROM = G.subject

        DATE = datetime.datetime.fromtimestamp(message.getTimestamp()).strftime('%d-%m-%Y %H:%M')

        try:
            self.SHOWNMESSAGE.append(displayed_message(FROM, DATE, text_content, master=self.VISOR))
        except TclError:
            print('Tkinter Error!')
            pass
        if len(self.SHOWNMESSAGE) > 10:
            self.SHOWNMESSAGE.pop(0)

        for M in range(len(self.SHOWNMESSAGE)):
            self.SHOWNMESSAGE[M].grid_forget()
        for M in range(len(self.SHOWNMESSAGE)):
            self.SHOWNMESSAGE[M].grid(column=0,row=M, sticky=W)

        self.MSGABSINDEX+=1

    def getinfo(self):#send group info request.
        self.YOWCLI.groups_list()
        sleep(2)
        self.process(self.YOWCLI.LASTIQ)

    def process(self, INFO):#receive and interprete the info we asked to the server in the getinfo() function, to load the GUI with the appropriate buttons.
        #also appends any contact you got on CONTACTS file, so the contacts and groups will appear on the same list on the app.
        try:
            if INFO.getType() == 'result':
                self.GROUPS = []
                I=0

                contacts = open('CONTACTS','r').readlines()
                contacts_togetkey = []
                for line in contacts:
                    if len(line) > 3:
                        person = line[:-1].split(';')
                        self.GROUPS.append(self.group(person[1], [], person[0], I, self.contactlist))
                        contacts_togetkey.append(person[1])
                        I+=1
                        

                for G in INFO.groupsList:
                    PARTY = G.getParticipants()
                    SUBJ = G.getSubject()
                    ID = G.getId()
                    self.GROUPS.append(self.group(ID, PARTY, SUBJ, I, self.contactlist))
                    I+=1


                if len(contacts_togetkey)>0:
                    self.YOWCLI.keys_get(contacts_togetkey)
                    self.YOWCLI.keys_set()
                    
        except AttributeError:
            pass

    def highlighted_group(self):#return the group that is selected on the GUI, if there is exactly one.
        H=[]
        for G in range(len(self.GROUPS)):
            if self.GROUPS[G].ACTIVE == 1:
                H.append(self.GROUPS[G])

        if len(H) == 1:
            return H[0]

    def admin_toall(self, demotepromote):# demote all admins on a group but yourself.
        group = self.highlighted_group()
        print(group)
        if group:
            party = group.PARTICIPANTS.items()
            for person in party:
                if CREDENTIALS[0] not in person[0]:
                    if demotepromote:
                        if person[1] != 'admin':
                            self.YOWCLI.group_promote(group.address, person[0])
                    else:
                        if person[1] == 'admin':
                            self.YOWCLI.group_demote(group.address, person[0])


if __name__==  "__main__":
    #if credentials are unavailable, launch auth window.
    if len(CREDENTIALS[0]) < 2:
        #print(CREDENTIALS[0])
        auth_w = auth_window()

    #initialize yowsup stack, with the layers we need.
    StackBuilder = YowStackBuilder()
    stack = StackBuilder.getDefaultStack(layer=YowsupCliLayer, axolotl=True)
    
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS) #setting credentials
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])     #whatsapp server address
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
    stack.setProp(YowCoderLayer.PROP_RESOURCE, YowsupEnv.getCurrent().getResource())     #info about us as WhatsApp client
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))             #sending the connect signal

    
    for i in range(9):
        #print(str(i)+" = "+str(stack.getLayer(i)))
        if str(stack.getLayer(i)) == "CLI Interface Layer":
               InterfaceLayer = stack.getLayer(i)
               break
            
    #print(X)
    
    #setting bot and cli layer to know each other.
    BOT = InterfaceLayer.getBot()
    BOT.getCliLayer(InterfaceLayer)

    #print(BOT.CliLayer)

    #starting the GUI and client; set BOT to recognize the window instance.
    app = window(InterfaceLayer)
    
    BOT.window = app
    stack.loop()
