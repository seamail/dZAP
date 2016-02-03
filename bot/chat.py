from chatterbot import ChatBot
import codecs




class Chatbrain ():
    def __init__(self):
        
        self.brain = ChatBot("Adolfo",
                   logic_adapters=["chatterbot.adapters.logic.EvaluateMathematically",
                                  #"chatterbot.adapters.logic.TimeLogicAdapter"])
                                  "chatterbot.adapters.logic.ClosestMatchAdapter"])
        self.brain.train("chatterbot.corpus.Portuguese.conversations_pt-BR")

    def respond(self, textin):
        self.brain.get_response(textin)
