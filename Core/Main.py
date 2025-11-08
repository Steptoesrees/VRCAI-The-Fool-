import callLLM as LLM
from RealtimeSTT import AudioToTextRecorder
from Text_To_Speech import TTS
import onnxruntime as ort
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

        while True:
            print (self.TTS.isTalking)
            self.recorder.text(self.talk_to_ai)
            


    def clean_text(self,text):
        return text.replace("*","").replace("#","").replace("^","").replace("|","")


    def talk_to_ai(self, text):
        print(text)

        if self.TTS.isTalking == False:
            print ('llm')

            self.TTS.isTalking = True
            self.memory.add_user_message(text)
            self.messages = self.memory.memory

            ai_response = LLM.call(self.messages)
            self.memory.add_ai_message(ai_response)

            speech = self.clean_text(ai_response)

            print(coloured('='*30,'magenta'))
            print(coloured(speech,'red'))
            print(coloured('='*30,'magenta'))

            print('\n')
            print(coloured('tts start','green'))
            self.TTS.readAloud(speech)

            print('\n')
            print(coloured('tts end','green'))
            


            
            self.TTS.isTalking = False
        else:
            print('interrupt')
            self.TTS.stop_Phrase(text)

    def run(self, text):
        self.TTS.isTalking = True
        self.memory.add_user_message(text)

        self.messages = self.memory.memory
        print(text)

        if "exit chat" in text.lower():
            ai__response = LLM.call(self.messages, max_tokens=50)
            speech = ai__response[0]
            print(speech)
            self.TTS.readAloud(speech)
            quit()
        
        #ai_response = LLM.call(self.messages)
        ai_response = 'test message'
        self.memory.add_ai_message(ai_response)
        
        speech = ai_response
        print(speech)
        self.TTS.readAloud(speech)
        self.TTS.isTalking = False
        return

if __name__ == '__main__':
    config = Config_Manager()
    recorder = AudioToTextRecorder(input_device_index=config.get('audio.input_device'))
    main = main(recorder, config)
    