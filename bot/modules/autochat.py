from chatterbot import ChatBot
import codecs

class Chatbrain ():
    def __init__(self):

        self.brain = ChatBot("Adolfo",
                storage_adapter = "chatterbot.adapters.storage.MongoDatabaseAdapter",
                   logic_adapters=["chatterbot.adapters.logic.EvaluateMathematically",
                                  #"chatterbot.adapters.logic.TimeLogicAdapter"])
                                  "chatterbot.adapters.logic.ClosestMatchAdapter"],
                    io_adapter="chatterbot.adapters.io.SelectiveAdapter")

        self.brain.train("chatterbot.corpus.Portuguese.conversations_pt-BR")

    def respond(self, textin):
        return self.brain.get_response(textin)
    def read(self, inputc):
        self.brain.io.process_input(statement=inputc)





