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
        
        self.style = ttk.Style()
        self.styles = self.style.theme_names()

        self.config = Config_Manager()
        self.convoManager = Convo_Manager()


      
        self.build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def build_ui(self):

        self.tabbook = ttk.Notebook(self)
        self.tabbook.pack(fill='both', expand=True)

        

        self.main_frame = ttk.Frame(self.tabbook)
        self.vision_frame = ttk.Frame(self.tabbook)
        self.settings_frame = ttk.Frame(self.tabbook)
        self.personality_frame = ttk.Frame(self.tabbook)
        self.tabbook.add(self.main_frame, text='Main')
        #self.tabbook.add(self.vision_frame, text='Vision')
        self.tabbook.add(self.settings_frame, text='Settings')
        self.tabbook.add(self.personality_frame, text='Personality')
        self.build_main_tab()
        self.build_vision_tab()
        self.build_settings_tab()
        self.build_personality_tab()
        self.populate_devices()
        self.populate_styles()
        self.load_config()
        self.get_prompt()
      

    def build_main_tab(self):
        self.status_label = ttk.Label(self.main_frame, text="Idle", font=('Segoe UI', 16))
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
        self.chat_log.pack(fill='both', expand=True)

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
        model_label = ttk.Label(AI_frame, text="Model url", font=('Segoe UI', 10))
        self.model_input = ttk.Entry(AI_frame, font=('Segoe UI', 12))
        key_label = ttk.Label(AI_frame, text="Openrouter key", font=('Segoe UI', 10))
        self.key_input = ttk.Entry(AI_frame, font=('Segoe UI', 12), show="*")


        #draws lables and input boxes
        model_label.pack(anchor='w', pady=(10, 0), padx=10)
        self.model_input.pack(anchor='w', fill='x', pady=(0,5), padx=10)
        
        key_label.pack(anchor='w', pady=(10, 0), padx=10)
        self.key_input.pack(anchor='w', fill='x', pady=(0,10), padx=10)




        """TTS SETTINGS"""
        TTS_frame = ttk.LabelFrame(self.settings_frame, text='TTS settings')
        TTS_frame.pack(fill='x', padx=10, pady=(0,10))


        #creates the labels, buttons, input boxes etc
        auto_button = ttk.Button(TTS_frame, text='Auto Device Setup', command=self.auto_audio_setup)
        
        input_label = ttk.Label(TTS_frame, text="Input Devices", font=('Segoe UI', 10))
        self.input_dropdown = ttk.Combobox(TTS_frame, state='readonly', width=32)

        output_label = ttk.Label(TTS_frame, text="Output Devices", font=('Segoe UI', 10))
        self.output_dropdown = ttk.Combobox(TTS_frame, state='readonly', width=32)

        #draws elements
        auto_button.pack(anchor='w', pady=10, padx=10)

        input_label.pack(anchor='w', pady=(10, 0), padx=10)
        self.input_dropdown.pack(anchor='w',pady=(0,5), padx=10)
        
        output_label.pack(anchor='w', pady=(10, 0), padx=10)
        self.output_dropdown.pack(anchor='w', pady=(0,10), padx=10)

        


        """UI SETTINGS"""
        UI_settings_frame = ttk.LabelFrame(self.settings_frame, text='UI settings')
        UI_settings_frame.pack(fill='x', padx=10, pady=(0,10))


        #creates the labels, buttons, input boxes etc
        style_label = ttk.Label(UI_settings_frame, text="UI Theme", font=('Segoe UI', 10))
        self.style_dropdown = ttk.Combobox(UI_settings_frame, state='readonly', width=32)

        style_label.pack(anchor='w', pady=(10, 0), padx=10)
        self.style_dropdown.pack(anchor='w',pady=(0,5), padx=10)


        confirm_button = ttk.Button(self.settings_frame, text='Confirm', command=self.set_config).pack()

    def build_personality_tab(self):
        prompt_frame = ttk.Frame(self.personality_frame)
        prompt_frame.pack(fill='both', expand=True, padx=5, pady=5)


        AI_name_label = ttk.Label(prompt_frame, text="AI Name", font=('Segoe UI', 10))
        self.AI_name_entry = ttk.Entry(prompt_frame, font=('Segoe UI', 12))


        prompt_label = ttk.Label(prompt_frame, text="Main Prompt", font=('Segoe UI', 10))
        self.prompt_entry = scrolledtext.ScrolledText(
            prompt_frame, 
            wrap=tk.WORD, 
            height=10, 
            font=('Segoe UI', 12),
            undo=True
        )

        AI_name_label.pack(anchor='w', pady=(10,0), padx=10)
        self.AI_name_entry.pack(fill='x', padx=10)
        prompt_label.pack(anchor='w', pady=(10,0), padx=10)
        self.prompt_entry.pack(fill='both', expand=True, padx=5,pady=(0,10))

        save_button = ttk.Button(prompt_frame, text='Confirm', command=self.set_prompt).pack(side='left',padx=5,pady=(0,5))
        save_button = ttk.Button(prompt_frame, text='Load Previous Prompt', command=self.load_previous_prompt).pack(side='right', padx=5,pady=(0,10))

    
    def populate_styles(self):
        self.style_dropdown['values'] = [f"{str(name)}"for i, name in enumerate(self.styles)]


    def populate_devices(self):
        devices = sd.query_devices()
        inp_temp = []
        out_temp = []

        self.input_devices = [(int(d['index']), d['name']) for d in devices if d['max_input_channels'] > 0]
        for idx,name in self.input_devices:
            if name in inp_temp:
                continue
            else:
                self.input_dropdown['values'] = (f"{str(name)}")

        self.output_devices = [(int(d['index']), d['name']) for d in devices if d['max_output_channels'] > 0]
        self.output_dropdown['values'] = [f"{str(name)[:40]}" for idx, name in self.output_devices if len(str(name)) < 40]




    def load_config(self):
        model = self.config.get('AI.model')
        voice = self.config.get('TTS.voice')
        inp_index = self.config.get('audio.input_device')
        out_index = self.config.get('audio.output_device')
        style = self.config.get('UI.style')
        key = self.config.get('API.openrouter_key')
        

        for i, name in enumerate(self.styles):
            if name == style:
                self.style_dropdown.current(i)

        for i, (d_idx, name) in enumerate(self.input_devices):
            if i == inp_index:
                self.input_dropdown.current(i)

        for i, (d_idx, name) in enumerate(self.output_devices):
            if d_idx == out_index:
                self.output_dropdown.current(i)
        
        self.style.theme_use(style)
        


        self.model_input.delete(0, tk.END)  # Delete all existing text
        self.model_input.insert(0, model)
        self.key_input.delete(0, tk.END)  # Delete all existing text
        self.key_input.insert(0, key)
        

    
    def set_config(self):
        newkey = self.key_input.get()
        self.config.set('API.openrouter_key', newkey)

        self.config.set('AI.model', self.model_input.get())
        self.config.set('UI.style', self.style_dropdown.get())

        for i, name in self.input_devices:
            if name == self.input_dropdown.get():
                inp_index = i

        for i, name in self.output_devices:
            if name == self.output_dropdown.get():
                out_index = i

        self.config.set('audio.input_device', inp_index)
        self.config.set('audio.output_device', out_index)
        

        self.load_config()
        




    def set_prompt(self):
        with open("Core/config/vrchat_bot_prompt.txt", "r") as rfile:
                with open("Core/config/vrchat_bot_prompt_backup.txt", "w") as wfile:
                    wfile.write(rfile.read())  

        with open("Core/config/vrchat_bot_prompt.txt", "w") as file:
            file.write(self.prompt_entry.get(1.0, tk.END))
        
        self.config.set('AI.name', self.AI_name_entry.get())
                
                
    def get_prompt(self):
        try:
            with open("Core/config/vrchat_bot_prompt.txt", "r") as file:
                content = file.read()
                self.prompt_entry.delete("1.0", tk.END)
                self.prompt_entry.insert(tk.INSERT, content)
        except:
            content = 'Load Failed'                
            self.prompt_entry.delete("1.0", tk.END)
            self.prompt_entry.insert(tk.INSERT, content)
        
        self.AI_name_entry.delete(0,tk.END)
        self.AI_name_entry.insert(0,self.config.get('AI.name'))
        

        


    def load_previous_prompt(self):
        try:
            with open("Core/config/vrchat_bot_prompt_backup.txt", "r") as file:
                content = file.read()
                self.prompt_entry.delete("1.0", tk.END)
                self.prompt_entry.insert(tk.INSERT, content)
        except:
            content = 'Load Failed'                
            self.prompt_entry.delete("1.0", tk.END)
            self.prompt_entry.insert(tk.INSERT, content)
        
        self.AI_name_entry.delete(0,tk.END)
        self.AI_name_entry.insert(0,self.config.get('AI.name'))






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


    def toggle_listen(self):
        if self.convoManager.isListening():
            self.listen_button.config(text='Start Listening')
            self.status_label.config(text="Idle")
            self.convoManager.stopListening()

        else: 
            self.listen_button.config(text='Stop Listening')
            self.status_label.config(text="Listening")
            self.convoManager.startListening()


    def remove_last_message(self):
        pass





    def on_closing(self):
        self.destroy()
        exit()
        close()



if __name__ == '__main__':
    app = UI()
    app.mainloop()
