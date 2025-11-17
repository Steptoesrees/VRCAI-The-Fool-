import callLLM as LLM
from RealtimeSTT import AudioToTextRecorder
from Text_To_Speech import TTS
from Config_Manager import Config_Manager
from Chat_Memory import short_memory
from Convo_Manager import Convo_Manager
from termcolor import colored as coloured




class main():
    def __init__(self, recorder, config):
        self.config = config
        self.convo = Convo_Manager()
        self.input_device = self.config.get('audio.input_device')
        self.output_device = self.config.get('audio.output_device')

        self.memory = short_memory()
        self.messages = self.memory.memory
        self.TTS = TTS(self.config.get('TTS.voice'), self.convo)
        self.recorder = recorder
        
      
    
    def call(self):
        self.recorder.text(self.talk_to_ai)
    
    def clean_text(self,text):
        return text.replace("*","").replace("#","").replace("^","").replace("|","")


    def talk_to_ai(self, text):
        
        # QOL PRINTS INPUT TO SCREEN   
        print(coloured(f"Is Talking Toggle: {self.convo.isTalking()}", 'cyan'))
        print(coloured('='*30,'magenta'))
        print(coloured(text,'green'))
        print(coloured('='*30,'magenta'))
        
        if not self.convo.isTalking():

            self.convo.startTalking()
            self.memory.add_user_message(text)
            self.messages = self.memory.memory


            ai_response = LLM.call(self.messages)
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
            


            self.TTS.readAloud(speech)

            # QOL PRINTS WHEN TTS STOPS
            print('\n')
            print(coloured('tts end','green'))
            
            self.convo.stopTalking()

        else:
            if self.convo.talkingInterrupt(text):
                print(coloured('INTERRUPT TRIGGERED','yellow'))
                return

if __name__ == '__main__':
    config = Config_Manager()
    recorder = AudioToTextRecorder(input_device_index=config.get('audio.input_device'))
    main = main(recorder, config)
    while True:
        main.call()