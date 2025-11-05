import sounddevice as sd
from Config_Manager import Config_Manager

#test

"""
audio line:
default speakers = voicemeeter input
voicemeeter input -> B2
B2 -> input_device (for the ai to hear)
    (optional, B2 !-> input_device)
    B2 -> Nvidia Broadcast
    Nvidia Broadcast -> input_device
    
tts -> voicemeeter AUX
voicemeeter AUX -> B1
B1 -> Vrc

"""

class Device_Helper():
    def __init__(self):
        self.devices = sd.query_devices()
        self.inp = False
        self.aux = False
        self.nvd = False
        self.B2 = False
        self.config = Config_Manager()
        

    def Update_Audio_Device_Config(self):
        print('='*60)
        print('downlaod voicemeeter Banana: https://vb-audio.com/Voicemeeter/banana.htm')
        print("Set VRCHAT mic to Voicemeeter B1")
        print("Set sound output device to Voicemeeter input")
        print("in voicemeeter, in virtual inputs, set voicemeeter input to B2")
        print("in voicemeeter, in virtual inputs, set voicemeeter AUX input to B1")
        print('='*60)
        for device in self.devices:
            if 'Voicemeeter Input' in device['name'] and not self.inp:
                print(f"{device['index']} : {device['name']}")
                self.inp = True

            if 'Voicemeeter AUX Input' in device['name'] and not self.aux:
                print(f"{device['index']} : {device['name']}")
                self.config.set("audio.output_device",device['index'])
                self.aux = True

            if 'Voicemeeter Out B2' in device['name'] and not self.B2:
                print(f"{device['index']} : {device['name']}")
                if not self.nvd:
                    self.config.set("audio.input_device",device['index'])
                self.B2 = True
            
            if 'Microphone (NVIDIA Broadcast)' in device['name'] and not self.nvd:
                print(f"{device['index']} : {device['name']}")
                self.config.set("audio.input_device",device['index'])
                self.nvd = True

        print('='*60)


if __name__ == '__main__':
    Device_Helper = Device_Helper()
    Device_Helper.Update_Audio_Device_Config()