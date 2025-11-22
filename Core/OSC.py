from pythonosc import udp_client
from time import sleep

class OSCsender():

    def __init__(self):
        # VRChat IP and incoming prot
        self.chat_len = 8
        self.client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    
    def sendChat(self, message):
        try:
            self.client.send_message("/chatbox/input", (message, True, False))
            return True
        except:
            return False
    
    def sendResponse(self, message):
        while len(message) > 144:
            message1 = message[:144]
            message = message[144:]
            self.sendChat(message1)
            sleep(self.chat_len)
        self.sendChat(message)
        sleep(self.chat_len)
        self.sendChat("")



if __name__ == '__main__':
    osc = OSCsender()
    osc.sendChat("")
    osc.sendResponse("""You're welcome to make your own programs that communicate with VRChat over OSC. This takes some programming knowledge or learning - it's not too complicated, but it does deal with network connections and asynchronous messaging so it may not be a great first project.

We currently have two APIs available for interaction: Input and Avatar Parameters. Those pages will describe the messages available to send & receive and some other details.""")