import sys

from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import AuthError
from yowsup.stacks import  YowStackBuilder
from yowsup.layers.auth import YowAuthenticationProtocolLayer

from layer import YowsupCliLayer


class YowsupCliStack(object):
    def __init__(self, credentials, encryptionEnabled = True):
        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder \
            .pushDefaultLayers(encryptionEnabled) \
            .push(YowsupCliLayer) \
            .build()

        self.stack.setCredentials(credentials)

    def start(self):
        print("Yowsup Cli client\n==================\nType /help for available commands\n")
        self.stack.broadcastEvent(YowLayerEvent(YowsupCliLayer.EVENT_START))

        try:
            self.stack.loop(timeout = 6666, discrete = 30*24*60*60)
        except AuthError as e:
            print("Auth Error, reason %s" % e)
        except KeyboardInterrupt:
            print("\nYowsdown")
            sys.exit(0)
