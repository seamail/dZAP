from layer import YowsupCliLayer
from yowsup.layers                             import YowParallelLayer
from yowsup.layers.auth                        import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.protocol_groups             import YowGroupsProtocolLayer
from yowsup.layers.protocol_profiles           import YowProfilesProtocolLayer
from yowsup.layers.protocol_chatstate          import YowChatstateProtocolLayer
from yowsup.layers.protocol_notifications      import YowNotificationsProtocolLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.protocol_presence           import YowPresenceProtocolLayer
from yowsup.layers.protocol_media              import YowMediaProtocolLayer
from yowsup.layers.protocol_media.mediauploader import MediaUploader


from yowsup.stacks import YowStack
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup import env

import datetime

from tkinter import *
from threading import * 
from time import *

import re

from d_bot import *





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


class displayed_message(Frame):
    def __init__(self, FROM, DATE, text_content,master=None):
        Frame.__init__(self, master=master, height = 50)


        self.F_=Label(master=self, text=FROM)
        self.F_.grid(column = 1, row = 0)
        self.D_=Label(master=self,text=DATE)
        self.D_.grid(column = 0, row = 0, sticky=W)

        self.C_=Label(master=self,text=text_content)
        self.C_.grid(column = 0, row = 1, columnspan=2,sticky=W)
        self.S_=Label(master=self,text="            ")
        self.S_.grid(column = 0, row = 2)
        
    
class window(Thread):
    class group():
        def __init__(self, address, party, subject, index, master):
            self.address = address
            self.subject = subject

            
            self.label = Label(master)
            self.label['text'] = self.subject
            self.label.grid(column=0, row=index+2)

            self.ACT = Button(master)
            self.ACT['text'] = ' '
            self.ACT['activebackground'] = 'grey'
            self.ACT['command'] = self.activate
            self.ACT['background'] = 'black'
            self.ACT.grid(column=1, row=index+2)


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
    
            
    def __init__(self):
        Thread.__init__(self)

        self.NAME = 'dZAP'
        self.start()
        self.connected=1
        self.contacts = {}
        
        self.GROUPS = []
        
        self.MSGREADINDEX = 0
        self.MSGABSINDEX = 0

        self.YOWCLI = stack.getLayer(6)

        self.SHOWNMESSAGE = []

                                     
    def getinfo(self):
        self.YOWCLI.group_info(self.address)

    
    def callback(self):
        self.root.quit()

    def sendtext(self,event=None):
        self.refresh_message()
        sent=0
        CONTENT = self.TEXTIN.get("1.0",END)[:-1]

        for AUTO in AUTO_RETRIEVE:
            if AUTO.TRIGGER_WORD == event:
                print('>>>>'+CONTENT)
                CONTENT = AUTO.retrieve(CONTENT)
                

        
        for GROUP in self.GROUPS:
            if GROUP.ACTIVE == 1:
                MSG = self.YOWCLI.message_send(GROUP.address, CONTENT)    
                sent=1       
        
        self.TEXTIN.delete(1.0, END)
        if sent:
            self.showmessage(MSG)

        
    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.resizable(width=FALSE, height=FALSE)

        


        self.VISOR = Frame(self.root, height = 600, width=500)
        self.VISOR.grid(column=0,row=0,columnspan=4)
        self.VISOR.grid_propagate(False)
        '''for I in range(10):
            self.SHOWNMESSAGE.append(displayed_message(" ", " ", " ", master=self.VISOR))
            self.SHOWNMESSAGE[I].grid(column=0, row=I)'''
  
        
        self.TEXTIN = Text(self.root, height=2, width=73)
        self.TEXTIN.grid(column=0,row=1,columnspan=4, sticky=W+E)

        #self.root.bind('<Return>', self.sendtext())
        
        self.SEND = Button(self.root, text = 'SEND', command = lambda: self.sendtext()).grid(column=2,row=2)

        self.SENDVOICE = Button(self.root, text= 'SENDVOICE', command = self.send_voice).grid(column=2,row=3)

        self.REFRESH = Button(self.root, text = 'REFRESH', command = self.getinfo).grid(column=3,row=4)

        self.LOADMSG = Button(self.root, text = 'load MSG', command = self.refresh_message).grid(column=3,row=3)

                              
        self.ADM = Button(self.root, text = 'toADM')
        self.ADM["command"] = lambda: stack.getLayer(6).group_promote(self.contacts['holex'], '5522998800908')
        self.ADM.grid(column=3,row=2)

        
        self.root.wm_title(self.NAME)

        self.menubar = Menu(self.root)

        self.AUTOMATE = Menu(self.menubar)
        self.AUTOMATE.add_command(label="Turn ON/OFF", background="red")
        self.AUTOMATE.add_command(label="MANAGE", command = lambda: self.automate_window())
        self.AUTOMATE.add_separator()
        self.AUTOMATE.add_command(label ="@dict", command = lambda: self.sendtext(event='@dict'))
        self.AUTOMATE.add_command(label ="@indict", command = lambda: self.sendtext(event='@indict'))
        self.AUTOMATE.add_command(label ="@wiki", command = lambda: self.sendtext(event='@wiki'))

        self.PROFILE = Menu(self.menubar)
        self.PROFILE.add_command(label="SET NICK", command = lambda: self.edit_profile('nick'))
        self.PROFILE.add_command(label="SET STATUS",  command = lambda: self.edit_profile('status'))
        self.PROFILE.add_command(label="SET IMAGE", command = lambda: self.edit_profile('image'))
                                

                                  

        self.menubar.add_cascade(label = "PROFILE", menu = self.PROFILE)
        self.menubar.add_cascade(label = "AUTOMATE", menu = self.AUTOMATE)
        
        
        self.root.config(menu=self.menubar)




        sleep(2)
        self.getinfo()

        self.root.mainloop()


    def edit_profileSAVEQUIT(self,attribute):
        if attribute == 'nick':
            self.YOWCLI.presence_name(self.editprofile.TEXT.get('1.0',END))
        elif attribute == 'status':
            self.YOWCLI.profile_setStatus(self.editprofile.TEXT.get('1.0',END))
        elif attribute == 'image':
            self.YOWCLI.profile_setPicture(self.editprofile.TEXT.get('1.0',END)[:-1])
        

        self.editprofile.destroy()

    def edit_profile(self, attribute):
            
            
        self.editprofile = Tk()

        self.editprofile.TEXT = Text(self.editprofile,height=1)
        self.editprofile.TEXT.grid(column=0,row=0)

        
        self.editprofile.OK = Button(self.editprofile, text="save", command = lambda: self.edit_profileSAVEQUIT(attribute)).grid(column=0,row=1)
        self.editprofile.wm_title('edit %s' % attribute)

        
    def refresh_message(self):

        while self.MSGREADINDEX < len(stack.getLayer(6).MESSAGES):
            self.showmessage(stack.getLayer(6).MESSAGES[self.MSGREADINDEX])
            self.MSGREADINDEX+=1


    def send_voice(self):
        for GROUP in self.GROUPS:
            if GROUP.ACTIVE == 1:
                create_voice(self.TEXTIN.get("1.0",END))
                sleep(1)
                MSG = self.YOWCLI.audio_send(GROUP.address, 'sound.wav')    
                sent=1       
        
        self.TEXTIN.delete(1.0, END)        


    def showmessage(self, message):
        INDEX = self.MSGABSINDEX*3

        try:
            text_content = message.getBody().decode('utf-8','ignore')
        except AttributeError:
            text_content = message.getBody()

        for K in range(round(len(text_content)/60)):
            text_content = text_content[:60*K] + "\n" + text_content[60*K:] 



        
        if not message.getFrom():
            FROM = 'SELF >>'

        else:
            FROM = message.getFrom()

        DATE = datetime.datetime.fromtimestamp(message.getTimestamp()).strftime('%d-%m-%Y %H:%M')

        self.SHOWNMESSAGE.append(displayed_message(FROM, DATE, text_content, master=self.VISOR))



        
        if len(self.SHOWNMESSAGE) > 10:
            self.SHOWNMESSAGE.pop(0)
                                 
        for M in range(len(self.SHOWNMESSAGE)):
            self.SHOWNMESSAGE[M].grid_forget()
        for M in range(len(self.SHOWNMESSAGE)):
            self.SHOWNMESSAGE[M].grid(column=0,row=M, sticky=W)
        

        self.MSGABSINDEX+=1


        
    def getinfo(self):  
        stack.getLayer(6).groups_list()
        sleep(2)
        self.process(stack.getLayer(6).LASTIQ)
        
    def process(self, INFO):
        try:
            if INFO.getType() == 'result':
                GROUPS = []
                I=0
                for G in INFO.groupsList:
              

                    PARTY = G.getParticipants()
                    SUBJ = G.getSubject()
                    ID = G.getId()

                    self.GROUPS.append(self.group(ID, PARTY, SUBJ, I, self.root))

                    I+=1
            
        except AttributeError:
            pass



        

if __name__==  "__main__":
    if len(CREDENTIALS[0]) < 2:
        print(CREDENTIALS[0])
        auth_w = auth_window()

    
    layers = (
        YowsupCliLayer,
        YowParallelLayer([YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer, YowGroupsProtocolLayer,
                          YowProfilesProtocolLayer, YowChatstateProtocolLayer, YowPresenceProtocolLayer, YowMediaProtocolLayer, YowNotificationsProtocolLayer])
    ) + YOWSUP_CORE_LAYERS
    
    stack = YowStack(layers)
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)         #setting credentials
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])    #whatsapp server address
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)              
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())          #info about us as WhatsApp client

    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal

    def CLIsend_message(TO, MESSAGE):
        stack.getLayer(6).message_send(TO, MESSAGE)





    app = window()
    stack.loop()

