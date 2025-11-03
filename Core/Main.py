import callLLM as LLM
from RealtimeSTT import AudioToTextRecorder
from Text_To_Speech import TTS
import onnxruntime as ort
from Config_Manager import Config_Manager
from Chat_Memory import short_memory



class main():
    def __init__(self, recorder, config):
        self.config = config
        self.input_device = self.config.get('audio.input_device')
        self.output_device = self.config.get('audio.output_device')
        self.text = input("enter 'yes' to type instead of talk").lower()



        self.memory = short_memory()
        self.messages = self.memory.memory
        self.GLAD0S = TTS()
        self.recorder = recorder
        self.recorder.text(self.run)
            


    def run(self, text):
        print('='*60)
        print(self.memory.memory)
        print('='*60)
        self.memory.add_user_message(text)

        self.messages = self.memory.memory
        print(text)

        if "exit chat" in text.lower():
            self.memory.add_user_message(text)

            self.messages = self.memory.memory
            ai__response = LLM.call(self.messages, max_tokens=50)
            speech = ai__response[0]
            print(speech)
            self.GLAD0S.readAloud(speech)
            quit()
        
        ai_response = LLM.call(self.messages)
        
        self.memory.add_ai_message(ai_response)
        
        speech = ai_response
        print(speech)
        self.GLAD0S.readAloud(speech)

if __name__ == '__main__':
    config = Config_Manager()
    recorder = AudioToTextRecorder(input_device_index=config.get('audio.input_device'))
    main = main(recorder, config)
    