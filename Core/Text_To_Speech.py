from piper import PiperVoice, SynthesisConfig
import sounddevice as sd
import numpy as np
from Config_Manager import Config_Manager
import subprocess


class TTS():
    def __init__ (self,voice, convo_manager):
        self.convo = convo_manager
        self.config = Config_Manager()
        self.voice = PiperVoice.load(voice, use_cuda=True)
        self.test_message = """Based on the error message, it seems like you're having trouble with the CUDA Execution Provider for ONNX Runtime, which is used by Piper. Here's how you can address the issue:"""


    
        



        self.syn_config = SynthesisConfig(
            volume=self.config.get('audio.volume'),  
            length_scale=self.config.get('audio.length_scale'),  
            noise_scale=self.config.get('audio.noise_scale'),  
            noise_w_scale=self.config.get('audio.noise_w_scale'),  
            normalize_audio=self.config.get('audio.normalize_audio'), 
        )

    def update_voice(self, voice):
        self.voice = PiperVoice.load(voice, use_cuda=True)

    def readAloud(self, message):
        self.stream = sd.OutputStream(samplerate=self.voice.config.sample_rate, channels=1, dtype='int16', device=self.config.get('audio.output_device'))
        self.stream.start()
        
        for chunk in self.voice.synthesize(message):
            if self.convo.isTalking():
                int_data = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
                self.stream.write(int_data)
            else:
                self.stream.close()
                return

        self.stream.stop()
        self.stream.close()
        return
    
if __name__ == '__main__':
    subprocess.call(['espeak', 'Hello world'])


    





    