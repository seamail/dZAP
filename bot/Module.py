#/bin/python

from time import time

class BotModule():
    def __init__(self, module, hastimer=False):
        self.hastimer=hastimer
        if hastimer:
            self.Timer = time() - 13
            self.LastCall = 0

        self.module = module
        self._trigger = self.module.trigger

    def trigger(self, message):
        if not self.hastimer or self.weightTimer():
            R = self._trigger(message)
            if R:
                self.Timer = time()
            return R
        elif self.hastimer:
            return self.module.timerfailmessage
    def weightTimer():
        if time() - self.Timer > self.hastimer:
            return True
