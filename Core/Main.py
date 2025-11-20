import callLLM as LLM
from RealtimeSTT import AudioToTextRecorder
from Text_To_Speech import TTS
from Config_Manager import Config_Manager
from Chat_Memory import short_memory
from Convo_Manager import Convo_Manager
from termcolor import colored as coloured




class main():
    def __init__(self, recorder, convo, UI, memory, callback=None):
        self.UI = UI
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
            
            print(coloured(f"Is Talking Toggle: {self.convo.isTalking()}", 'cyan'))
            print(coloured('='*30,'magenta'))
            print(coloured(text,'green'))
            print(coloured('='*30,'magenta'))
            
            if not self.convo.isTalking():
                
                self.convo.startTalking()
                self.memory.add_user_message(text)
                self.messages = self.memory.memory
                
                self.memory.save_memory()
                if self.callback:
                    self.callback()

                self.UI.set_thinking(True)
                ai_response = LLM.call(self.messages)
                
                if ai_response[0] != False:
                    self.memory.add_ai_message(ai_response)
                    speech = self.clean_text(ai_response)


                    # QOL PRINTS AI RESPONSE TO SCREEN
                    print("\n")
                    print(coloured('='*30,'magenta'))
                    print(coloured(speech,'red'))
                    print(coloured('='*30,'magenta'))

                    # QOL PRINTS WHEN TTS STarts
                    print('\n')
                    print(coloured('tts start','green'))
                    
                    if self.callback:
                        self.callback()

                    self.UI.set_talking(True)

                    self.TTS.readAloud(speech)
                    
                    
                    # QOL PRINTS WHEN TTS STOPS
                    print('\n')
                    print(coloured('tts end','green'))
                else:
                    self.UI.add_message(ai_response[1], 'system')
                
                self.UI.set_talking(False)
                self.convo.stopTalking()

            else:
                if self.convo.talkingInterrupt(text):
                    print(coloured('INTERRUPT TRIGGERED','yellow'))
                    return
                
        else: 
            return



