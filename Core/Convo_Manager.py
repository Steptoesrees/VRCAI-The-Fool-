
class Convo_Manager():
    def __init__(self):
        self._is_responding = False
        self._is_convo = False
        self._is_listening = False
        self._interrupt_words = ["shut up", "wait", "listen to me", "stop"]




    def isListening(self):
        return self._is_listening
    
    def stopListening(self):
        self._is_listening = False

    def startListening(self):
        self._is_listening = True


    def isResponding(self):
        return self._is_responding
    
    def stopResponding(self):
        self._is_responding = False
    
    def startResponding(self):
        self._is_responding = True


    def isConvo(self):
        return self._is_convo
    
    def stopConvo(self):
        self._is_convo = False
    
    def startConvo(self):
        self._is_convo = True


    def respondingInterrupt(self, text):
        for word in self._interrupt_words:
            if word in text.lower():
                self.stopResponding()
                return True
        return False
    