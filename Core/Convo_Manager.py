


class Convo_Manager():
    def __init__(self):
        self._is_talking = False

    def isTalking(self):
        return self._is_talking
    
    def stopTalking(self):
        self._is_talking = False
    
    def startTalking(self):
        self._is_talking = True