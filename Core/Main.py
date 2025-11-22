import callLLM as LLM
from RealtimeSTT import AudioToTextRecorder
from Text_To_Speech import TTS
from Config_Manager import Config_Manager
from Chat_Memory import short_memory
from Convo_Manager import Convo_Manager
from termcolor import colored as coloured
from OSC import OSCsender
import threading



class main():
    def __init__(self, recorder, convo, UI, memory, callback=None):
        self.UI = UI
        self.osc = OSCsender()
        self.config = Config_Manager()
        self.convo = convo
        self.input_device = self.config.get('audio.input_device')
        self.output_device = self.config.get('audio.output_device')
        self._is_running = True
        self.memory = memory
        self.messages = self.memory.memory
        self.TTS = TTS(self.config.get('TTS.voice'), self.convo)
        self.recorder = recorder
        self.callback = callback

        
        
    def exit_thread(self):
        self._is_running = False
        self.recorder.abort()
    
    def call(self):
        while self._is_running:
            self.recorder.text(self.talk_to_ai)
        return
    
    def clean_text(self,text):
        return text.replace("*","").replace("#","").replace("^","").replace("|","")


    def talk_to_ai(self, text):
        if self.convo.isListening():
        # QOL PRINTS INPUT TO SCREEN   
            
            print(coloured(f"Is Responding Toggle: {self.convo.isResponding()}", 'cyan'))
            
            if not self.convo.isResponding():
                
                self.convo.startResponding()
                self.memory.add_user_message(text)
                self.messages = self.memory.memory
                
                self.memory.save_memory()
                if self.callback:
                    self.callback()

                self.UI.set_thinking(True)

                if self.config.get('TTS.chatbox'): #if toggle to send messages to the chatbox in game, call function to do so
                    self.osc.sendChat('Thinking') #

                ai_response = LLM.call(self.messages)
                
                if ai_response[0] != False:
                    self.memory.add_ai_message(ai_response)
                    speech = self.clean_text(ai_response)
                    
                    if self.callback:
                        self.callback()

                    self.UI.set_talking(True)
                    self.osc.sendChat('')

                    if self.config.get('TTS.chatbox'):
                        speechthread = threading.Thread(target=self.TTS.readAloud, args=(speech,))
                        chatthread = threading.Thread(target=self.osc.sendResponse, args=(speech,))

                        speechthread.start()
                        chatthread.start()

                        speechthread.join()
                        chatthread.join()
                        
                    else:
                        self.TTS.readAloud(speech)
                    
                    
                    # QOL PRINTS WHEN TTS STOPS
                else:
                    self.UI.add_message(ai_response[1], 'system')
                
                self.UI.set_talking(False)
                self.convo.stopResponding()

            else:
                if self.convo.respondingInterrupt(text):
                    print(coloured('INTERRUPT TRIGGERED','yellow'))
                    return
                
        else: 
            return



