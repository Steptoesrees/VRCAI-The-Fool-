import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import sounddevice as sd


from RealtimeSTT import AudioToTextRecorder
from Config_Manager import Config_Manager
from Convo_Manager import Convo_Manager
from Chat_Memory import short_memory
from Text_To_Speech import TTS
import callLLM as LLM

class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Fool TTS UI")
        self.geometry("900x700")

        style = ttk.Style()
        style.theme_use('clam')

        self.config = Config_Manager()
        self.convoManager = Convo_Manager()


      
        self.build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def build_ui(self):

        self.tabbook = ttk.Notebook(self)
        self.tabbook.pack(fill='both', expand=True, padx=10, pady=10)

        self.main_frame = ttk.Frame(self.tabbook)
        self.vision_frame = ttk.Frame(self.tabbook)
        self.settings_frame = ttk.Frame(self.tabbook)
        self.tabbook.add(self.main_frame, text='Main')
        self.tabbook.add(self.vision_frame, text='Vision')
        self.tabbook.add(self.settings_frame, text='Settings')
        self.build_main_tab()
        self.build_vision_tab()
        self.build_settings_tab()
        self.populate_devices()
      



    def build_main_tab(self):
        self.status_label = ttk.Label(self.main_frame, text="⚫ | Idle🔴", font=('Segoe UI', 16))
        self.status_label.pack(anchor='center', pady=(10, 5), padx=10)

        # Chat log frame
        self.chat_frame = ttk.Frame(self.main_frame)
        self.chat_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.chat_log = scrolledtext.ScrolledText(
            self.chat_frame, 
            wrap=tk.WORD, 
            state=tk.DISABLED, 
            height=10, 
            font=('Consolas', 12)
        )

        lorem_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in 
culpa qui officia deserunt mollit anim id est laborum."""

        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.pack(fill='both', expand='true')

        self.add_message("Click 'Start listening' to start the AI", "System")

        self.bottom_frame = ttk.Frame(self.main_frame)
        self.listen_button = ttk.Button(self.bottom_frame, text='Start Listening', command=self.toggle_listen)
        self.listen_button.pack(side='left',padx=5)
        self.undo_button = ttk.Button(self.bottom_frame, text='Remove Last Request', command=self.remove_last_message)
        self.undo_button.pack(side='left',padx=5)
        self.bottom_frame.pack(pady=5, padx=5)


    def build_vision_tab(self):
        temp_label = ttk.Label(self.vision_frame, text="PlaceHolder", font=('impact', 120))
        temp_label.pack(anchor='center', pady=(10, 5), padx=10)

    def build_settings_tab(self):
        
        """AI SETTINGS"""
        AI_frame = ttk.LabelFrame(self.settings_frame, text='AI settings')
        AI_frame.pack(fill='x', padx=10, pady=10)

        #creates the lables and input boxes for model and openrouter key
        model_label = ttk.Label(AI_frame, text="Model", font=('Segoe UI', 10))
        model_input = ttk.Entry(AI_frame, font=('Segoe UI', 12))
        key_label = ttk.Label(AI_frame, text="Openrouter key", font=('Segoe UI', 10))
        key_input = ttk.Entry(AI_frame, font=('Segoe UI', 12), show="*")

        #draws lables and input boxes
        model_label.pack(anchor='w', pady=(10, 0), padx=10)
        model_input.pack(anchor='w', fill='x', pady=(0,5), padx=10)
        
        key_label.pack(anchor='w', pady=(10, 0), padx=10)
        key_input.pack(anchor='w', fill='x', pady=(0,10), padx=10)

        """TTS SETTINGS"""
        TTS_frame = ttk.LabelFrame(self.settings_frame, text='TTS settings')
        TTS_frame.pack(fill='x', padx=10, pady=(0,10))


        #creates the labels, buttons, input boxes etc
        auto_button = ttk.Button(TTS_frame, text='Auto Device Setup', command=self.auto_audio_setup)
        
        input_label = ttk.Label(TTS_frame, text="Input Devices", font=('Segoe UI', 10))
        self.input_dropdown = ttk.Combobox(TTS_frame, state='readonly', width=32)

        output_label = ttk.Label(TTS_frame, text="Output Devices", font=('Segoe UI', 10))
        self.output_dropdown = ttk.Combobox(TTS_frame, state='readonly', width=32)

        self.volume_var = 0
        ttk.Label(TTS_frame, text='Volume:').pack(anchor='w')
        self.volume_var = tk.DoubleVar(value=1.0)
        self.volume_scale = ttk.Scale(TTS_frame, from_=0.0, to=2.0, orient='horizontal', variable=self.volume_var)

        #draws elements
        auto_button.pack(anchor='w', pady=10, padx=10)

        input_label.pack(anchor='w', pady=(10, 0), padx=10)
        self.input_dropdown.pack(anchor='w',pady=(0,5), padx=10)
        
        output_label.pack(anchor='w', pady=(10, 0), padx=10)
        self.output_dropdown.pack(anchor='w', pady=(0,10), padx=10)

        self.volume_scale.pack(fill='x', pady=(0, 10))


    def populate_devices(self):
        devices = sd.query_devices()
        self.input_devices = [(int(d['index']), d['name']) for d in devices if d['max_input_channels'] > 0]
        self.input_dropdown['values'] = [f"{idx} - {str(name)[:40]}{'...' if len(str(name)) > 40 else ''}" for idx, name in self.input_devices]

        self.output_devices = [(int(d['index']), d['name']) for d in devices if d['max_output_channels'] > 0]
        self.output_dropdown['values'] = [f"{idx} - {str(name)[:40]}{'...' if len(str(name)) > 40 else ''}" for idx, name in self.output_devices]


    def toggle_listen(self):
        if self.convoManager.isListening():
            self.listen_button.config(text='Start Listening')
            self.status_label.config(text="⚫ | Idle")
            self.convoManager.stopListening()

        else: 
            self.listen_button.config(text='Stop Listening')
            self.status_label.config(text="🟡 | Listening")
            self.convoManager.startListening()

    
    def remove_last_message(self):
        pass


    def on_closing(self):
        self.destroy()
        exit()
        close()


    def auto_audio_setup(self):
        pass

    def add_message(self, message, sender):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.INSERT, "\n")
        self.chat_log.insert(tk.INSERT, f"{sender}:")
        self.chat_log.insert(tk.INSERT, "\n")
        self.chat_log.insert(tk.INSERT, message)
        self.chat_log.insert(tk.INSERT, "\n")
        self.chat_log.config(state=tk.DISABLED)

if __name__ == '__main__':
    app = UI()
    app.mainloop()
