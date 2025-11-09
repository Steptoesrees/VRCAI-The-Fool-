


class Convo_Manager():
    def __init__(self):
        self._is_talking = False
        self._is_convo = False

        self._interrupt_words = ["shut up", "wait", "listen to me", "stop"]

    def isTalking(self):
        return self._is_talking
    
    def stopTalking(self):
        self._is_talking = False
    
    def startTalking(self):
        self._is_talking = True
    
    def isConvo(self):
        return self._is_convo
    
    def stopConvo(self):
        self._is_convo = False
    
    def startConvo(self):
        self._is_convo = True

    def talkingInterrupt(self, text):
        for word in self._interrupt_words:
            if word in text.lower():
                self.stopTalking()
                return True
        return False