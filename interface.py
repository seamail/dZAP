from tkinter import *

def setupInterface(frontend, BOT):
    # this function is started on __init___,
    frontend.root = Tk()
    # because the window is a Thread. Initialize GUI and its widgets and menus.
    frontend.root.protocol("WM_DELETE_WINDOW", frontend.callback)
    frontend.root.resizable(width=FALSE, height=FALSE)
    
    frontend.VISOR = Frame(frontend.root, height = 600, width=500,borderwidth=3,relief=GROOVE)
    frontend.VISOR.grid(column=2,row=0,columnspan=4,)
    frontend.VISOR.grid_propagate(False)
    '''for I in range(10):
    frontend.SHOWNMESSAGE.append(displayed_message(" ", " ", " ", master=frontend.VISOR))
    frontend.SHOWNMESSAGE[I].grid(column=0, row=I)'''
    
    frontend.TEXTIN = Text(frontend.root, height=2, width=73)
    frontend.TEXTIN.grid(column=0,row=1,columnspan=6, sticky=W+E)
    
    frontend.SEND = Button(frontend.root, text = 'SEND', command = lambda: frontend.sendtext()).grid(column=0,row=2,columnspan=6, sticky=W+E)
    frontend.SENDVOICE = Button(frontend.root, text= 'SENDVOICE', command = frontend.send_voice).grid(column=2,row=3)
    frontend.REFRESH = Button(frontend.root, text = 'REFRESH', command = frontend.getinfo).grid(column=3,row=4)
    frontend.LOADMSG = Button(frontend.root, text = 'load MSG', command = frontend.refresh_message).grid(column=3,row=3)
    frontend.ADM = Button(frontend.root, text = 'toADM')
    frontend.ADM["command"] = lambda: frontend.YOWCLI.group_promote(frontend.GROUPS[2].address, frontend.TEXTIN.get("1.0",END)[:-1])
    frontend.ADM.grid(column=4,row=3)
    frontend.BROWSE = Button(frontend.root, text= 'browse file')
    frontend.BROWSE["command"] = lambda: frontend.browsefiles(frontend.TEXTIN)
    frontend.BROWSE.grid(column=2, row=4)

    frontend.QUIT = Button(frontend.root, text = 'EXIT')
    frontend.QUIT["command"] = lambda: frontend.root.destroy()
    frontend.QUIT.grid(column=4, row=4)
    
    frontend.BOTRESPONSE = Scale(frontend.root, from_=100, to=0)
    frontend.BOTRESPONSE.grid(column=0, row=3, rowspan=2)
    
    frontend.contactlist = Frame(frontend.root,borderwidth=3,relief=GROOVE)
    frontend.contactlist.grid(column=0,row=0,sticky=NS)
    
    frontend.root.wm_title(frontend.NAME)
    frontend.menubar = Menu(frontend.root)
    
    frontend.AUTOMATE = Menu(frontend.menubar)
    frontend.AUTOMATE.add_command(label="Turn ON/OFF", background="red")
    frontend.AUTOMATE.add_command(label="MANAGE", command = lambda: frontend.automate_window())
    frontend.AUTOMATE.add_separator()
    frontend.AUTOMATE.add_command(label ="@dict", command = lambda: frontend.sendtext(event='@dict'))
    frontend.AUTOMATE.add_command(label ="@indict", command = lambda: frontend.sendtext(event='@indict'))
    frontend.AUTOMATE.add_command(label ="@wiki", command = lambda: frontend.sendtext(event='@wiki'))
    frontend.AUTOMATE.add_command(label ="@kkk", command = lambda: frontend.sendtext(event='@kkk'))
    frontend.AUTOMATE.add_command(label ='Vestibular',
                                  command = lambda: BOT.govestibular(frontend.GROUPS[frontend.highlighted_group()].address))
    
    frontend.PROFILE = Menu(frontend.menubar)
    frontend.PROFILE.add_command(label="SET NICK", command = lambda: frontend.edit_profile('nick'))
    frontend.PROFILE.add_command(label="SET STATUS",  command = lambda: frontend.edit_profile('status'))
    frontend.PROFILE.add_command(label="SET IMAGE", command = lambda: frontend.edit_profile('image'))
    
    frontend.GROUP = Menu(frontend.menubar)
    frontend.GROUP.add_command(label="SET GROUP NAME", command = lambda: frontend.edit_profile('group name'))
    frontend.GROUP.add_command(label="SET GROUP IMAGE", command = lambda: frontend.edit_profile('group image'))
    frontend.GROUP.add_separator()
    frontend.GROUP.add_command(label="BAN")
    frontend.GROUP.add_command(label="demote ALL", command = lambda: frontend.admin_toall(0))
    frontend.GROUP.add_command(label="promote ALL", command = lambda: frontend.admin_toall(1))
    
    frontend.FILES = Menu(frontend.menubar)
    frontend.FILES.add_command(label="SEND IMAGE", command = lambda: frontend.YOWCLI.image_send(frontend.highlighted_group().address,
                                                                                                frontend.TEXTIN.get('1.0',END)[:-1]))
    
    frontend.NETWORK = Menu(frontend.menubar)
    #frontend.NETWORK.add_command((label="Send ACK", command = lambda: frontend.YOWCLI.      
    frontend.menubar.add_cascade(label = "PROFILE", menu = frontend.PROFILE)
    frontend.menubar.add_cascade(label = "GROUP", menu = frontend.GROUP)
    frontend.menubar.add_cascade(label = "AUTOMATE", menu = frontend.AUTOMATE)
    frontend.menubar.add_cascade(label = 'FILES', menu = frontend.FILES)
    
    frontend.root.config(menu=frontend.menubar)
    
