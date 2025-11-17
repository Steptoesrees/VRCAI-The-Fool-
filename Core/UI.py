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

        self.config = Config_Manager()
        self.convo = Convo_Manager()
        self.memory = short_memory()
        voice_path = self.config.get('TTS.voice')
        self.TTS = TTS(voice_path, self.convo)
        self.listening = False
        self.recorder = None

        self.build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Welcome message
        self.chat_log.config(state='normal')
        self.chat_log.insert('end', 'Welcome to The Fool TTS Chat. Press "Start Listening" to begin.\n\n')
        self.chat_log.config(state='disabled')

    def build_ui(self):
        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Usage Tab
        self.usage_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.usage_frame, text='Usage')
        self.build_usage_tab()

        # Settings Tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text='Settings')
        self.build_settings_tab()

        self.populate_devices()
        self.load_config_to_ui()

    def build_usage_tab(self):
        # Top frame: title and status
        top_frame = ttk.Frame(self.usage_frame)
        top_frame.pack(fill='x', padx=10, pady=5)

        self.title_label = ttk.Label(top_frame, text="The Fool TTS Chat", font=('Arial', 16, 'bold'))
        self.title_label.pack()

        self.status_var = tk.StringVar(value="Idle")
        self.status_label = ttk.Label(top_frame, textvariable=self.status_var, font=('Arial', 12))
        self.status_label.pack()

        # Chat log frame
        chat_frame = ttk.Frame(self.usage_frame)
        chat_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.chat_log = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            height=15,
            font=('Consolas', 10)
        )
        self.chat_log.pack(fill='both', expand=True)

        # Configure tags
        self.chat_log.tag_config('user', foreground='green', font=('Consolas', 10, 'bold'))
        self.chat_log.tag_config('ai', foreground='red')

        # Bottom frame: buttons
        bottom_frame = ttk.Frame(self.usage_frame)
        bottom_frame.pack(fill='x', padx=10, pady=5)

        self.listen_button = ttk.Button(bottom_frame, text='Start Listening', command=self.toggle_listen)
        self.listen_button.pack(side='left', padx=5)

        clear_button = ttk.Button(bottom_frame, text='Clear Chat', command=self.clear_chat)
        clear_button.pack(side='left', padx=5)

    def build_settings_tab(self):
        # Audio frame
        audio_frame = ttk.LabelFrame(self.settings_frame, text='Audio Settings')
        audio_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(audio_frame, text='Input Device:').pack(anchor='w')
        self.input_combo = ttk.Combobox(audio_frame, state='readonly', width=60)
        self.input_combo.pack(fill='x', pady=(0, 10))

        ttk.Label(audio_frame, text='Output Device:').pack(anchor='w')
        self.output_combo = ttk.Combobox(audio_frame, state='readonly', width=60)
        self.output_combo.pack(fill='x', pady=(0, 10))

        ttk.Label(audio_frame, text='Volume:').pack(anchor='w')
        self.volume_var = tk.DoubleVar(value=1.0)
        self.volume_scale = ttk.Scale(audio_frame, from_=0.0, to=2.0, orient='horizontal', variable=self.volume_var)
        self.volume_scale.pack(fill='x', pady=(0, 10))

        ttk.Label(audio_frame, text='Length Scale:').pack(anchor='w')
        self.length_var = tk.DoubleVar(value=1.0)
        self.length_scale = ttk.Scale(audio_frame, from_=0.5, to=2.0, orient='horizontal', variable=self.length_var)
        self.length_scale.pack(fill='x', pady=(0, 10))

        ttk.Label(audio_frame, text='Noise Scale:').pack(anchor='w')
        self.noise_var = tk.DoubleVar(value=0.0)
        self.noise_scale = ttk.Scale(audio_frame, from_=0.0, to=1.0, orient='horizontal', variable=self.noise_var)
        self.noise_scale.pack(fill='x', pady=(0, 10))

        ttk.Label(audio_frame, text='Noise W Scale:').pack(anchor='w')
        self.noise_w_var = tk.DoubleVar(value=0.0)
        self.noise_w_scale = ttk.Scale(audio_frame, from_=0.0, to=1.0, orient='horizontal', variable=self.noise_w_var)
        self.noise_w_scale.pack(fill='x', pady=(0, 10))

        self.normalize_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(audio_frame, text='Normalize Audio', variable=self.normalize_var).pack(anchor='w', pady=(10, 0))

        # TTS frame
        tts_frame = ttk.LabelFrame(self.settings_frame, text='TTS Settings')
        tts_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(tts_frame, text='Voice:').pack(anchor='w')
        self.voice_var = tk.StringVar()
        self.voice_combo = ttk.Combobox(tts_frame, textvariable=self.voice_var, state='readonly', width=60)
        self.voice_combo.pack(fill='x', pady=(0, 20))

        # Buttons
        buttons_frame = ttk.Frame(self.settings_frame)
        buttons_frame.pack(pady=20)

        save_btn = ttk.Button(buttons_frame, text='Save Config', command=self.save_config)
        save_btn.pack(side='right', padx=5)

        reset_btn = ttk.Button(buttons_frame, text='Reset Defaults', command=self.reset_config)
        reset_btn.pack(side='right', padx=5)

    def populate_devices(self):
        devices = sd.query_devices()
        self.input_devices = [(int(d['index']), d['name']) for d in devices if d['max_input_channels'] > 0]
        self.input_combo['values'] = [f"{idx} - {str(name)[:40]}{'...' if len(str(name)) > 40 else ''}" for idx, name in self.input_devices]

        self.output_devices = [(int(d['index']), d['name']) for d in devices if d['max_output_channels'] > 0]
        self.output_combo['values'] = [f"{idx} - {str(name)[:40]}{'...' if len(str(name)) > 40 else ''}" for idx, name in self.output_devices]

        # Voices - for now, use current, add more as needed
        current_voice = self.config.get('TTS.voice')
        self.voice_combo['values'] = [current_voice] if current_voice else []

    def load_config_to_ui(self):
        # Input device
        input_idx = self.config.get('audio.input_device')
        if input_idx is not None:
            target_str = f"{input_idx} - "
            for i, val in enumerate(self.input_combo['values']):
                if val.startswith(target_str):
                    self.input_combo.current(i)
                    break

        # Output device
        output_idx = self.config.get('audio.output_device')
        if output_idx is not None:
            target_str = f"{output_idx} - "
            for i, val in enumerate(self.output_combo['values']):
                if val.startswith(target_str):
                    self.output_combo.current(i)
                    break

        self.volume_var.set(self.config.get('audio.volume') or 1.0)
        self.length_var.set(self.config.get('audio.length_scale') or 1.0)
        self.noise_var.set(self.config.get('audio.noise_scale') or 0.0)
        self.noise_w_var.set(self.config.get('audio.noise_w_scale') or 0.0)
        self.normalize_var.set(self.config.get('audio.normalize_audio') or False)
        self.voice_var.set(self.config.get('TTS.voice') or '')

    def save_config(self):
        # Audio
        sel = self.input_combo.get()
        if sel:
            self.config.set('audio.input_device', int(sel.split(' - ')[0]))

        sel = self.output_combo.get()
        if sel:
            self.config.set('audio.output_device', int(sel.split(' - ')[0]))

        self.config.set('audio.volume', float(self.volume_var.get()))
        self.config.set('audio.length_scale', float(self.length_var.get()))
        self.config.set('audio.noise_scale', float(self.noise_var.get()))
        self.config.set('audio.noise_w_scale', float(self.noise_w_var.get()))
        self.config.set('audio.normalize_audio', bool(self.normalize_var.get()))

        # TTS
        self.config.set('TTS.voice', self.voice_var.get())

        # Restart TTS for new config
        self.restart_tts()

    def reset_config(self):
        self.volume_var.set(1.0)
        self.length_var.set(1.0)
        self.noise_var.set(0.0)
        self.noise_w_var.set(0.0)
        self.normalize_var.set(False)
        # Reset combos to defaults if needed
        self.save_config()

    def restart_tts(self):
        voice = self.config.get('TTS.voice')
        if voice:
            self.TTS = TTS(voice, self.convo)

    def clean_text(self, text):
        return text.replace("*", "").replace("#", "").replace("^", "").replace("|", "")

    def toggle_listen(self):
        if self.listening:
            self.listening = False
            self.recorder = None  # Allow GC to clean up
            self.listen_button.config(text='Start Listening')
            self.status_var.set('Idle')
        else:
            self.listening = True
            input_idx = self.config.get('audio.input_device')
            if input_idx is None:
                self.status_var.set('Error: No input device')
                return
            try:
                self.recorder = AudioToTextRecorder(input_device_index=int(input_idx))
                self.recorder.text(self.handle_stt)
                self.listen_button.config(text='Stop Listening')
                self.status_var.set('Listening')
            except Exception as e:
                self.status_var.set(f'Error starting: {str(e)}')

    def handle_stt(self, text):
        if self.listening:
            threading.Thread(target=self._process_text, args=(text,), daemon=True).start()

    def _process_text(self, text):
        clean = self.clean_text(text)
        self.after(0, lambda: self.append_to_log('user', clean))
        self.after(0, lambda: self.status_var.set('Processing'))

        if not self.convo.isTalking():
            self.convo.startTalking()
            self.memory.add_user_message(text)
            ai_response = LLM.call(self.memory.memory)
            self.memory.add_ai_message(ai_response)
            speech = self.clean_text(ai_response)
            self.after(0, lambda: self.append_to_log('ai', speech))
            self.after(0, lambda: self.status_var.set('Speaking'))
            self.TTS.readAloud(speech)
            self.after(0, lambda: self.status_var.set('Idle'))
            self.convo.stopTalking()
        else:
            if self.convo.talkingInterrupt(text):
                self.after(0, lambda: self.status_var.set('Interrupted'))
                self.convo.stopTalking()

    def append_to_log(self, tag, text):
        self.chat_log.config(state='normal')
        self.chat_log.insert('end', text + '\n\n', tag)
        self.chat_log.config(state='disabled')
        self.chat_log.see('end')

    def clear_chat(self):
        self.chat_log.config(state='normal')
        self.chat_log.delete('1.0', 'end')
        self.chat_log.config(state='disabled')

    def on_closing(self):
        self.listening = False
        if hasattr(self, 'recorder') and self.recorder:
            del self.recorder
        self.memory.save_memory()
        self.destroy()


if __name__ == '__main__':
    app = UI()
    app.mainloop()