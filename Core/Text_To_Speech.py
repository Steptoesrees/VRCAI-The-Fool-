from piper import PiperVoice, SynthesisConfig
import sounddevice as sd
import numpy as np
from Config_Manager import Config_Manager


class TTS():
    def __init__ (self,voice, convo_manager):
        self.convo = convo_manager
        self.config = Config_Manager()
        self.voice = PiperVoice.load(voice)
        self.test_message = """Based on the error message, it seems like you're having trouble with the CUDA Execution Provider for ONNX Runtime, which is used by Piper. Here's how you can address the issue:"""


        self.isTalking = False
        self.inConvo = False
        self.stopPhrases = ["shut up", "wait", "listen to me"]

    
        



        self.syn_config = SynthesisConfig(
            volume=self.config.get('audio.volume'),  
            length_scale=self.config.get('audio.length_scale'),  
            noise_scale=self.config.get('audio.noise_scale'),  
            noise_w_scale=self.config.get('audio.noise_w_scale'),  
            normalize_audio=self.config.get('audio.normalize_audio'), 
        )

    def readAloud(self, message):
        self.stream = sd.OutputStream(samplerate=self.voice.config.sample_rate, channels=1, dtype='int16', device=self.config.get('audio.output_device'))
        self.stream.start()
        
        for chunk in self.voice.synthesize(message):
            if self.isTalking == True:
                int_data = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
                self.stream.write(int_data)

        self.stream.close()
        return

    def toggle_talking(self):
        self.isTalking = not self.isTalking

    def stop_Phrase(self, phrase):
        for i in self.stopPhrases:
            if i in phrase:
                if self.isTalking == True:
                    self.toggle_talking()
                    self.stream.close()
                return
        return


    