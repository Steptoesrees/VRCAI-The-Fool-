# VRChat AI Bot - TTS/STT System

A sophisticated AI companion bot for VRChat that provides real-time speech-to-text and text-to-speech capabilities with intelligent conversation management and memory systems.

## 🚀 Overview

This project creates an AI companion that can engage in natural conversations within VRChat environments. The system combines real-time speech processing with large language models to create an immersive, interactive experience.

### Key Features

- **Real-time Speech-to-Text**: Continuous audio transcription using RealtimeSTT
- **High-Quality Text-to-Speech**: Natural voice synthesis with Piper TTS
- **Intelligent Conversation**: Context-aware responses using LLMs via OpenRouter
- **Memory Systems**: Both short-term conversation memory and long-term vector storage
- **VRChat Integration**: Designed specifically for virtual reality social interactions
- **Modular Architecture**: Clean separation of concerns with planned enhancements


### Core Components

- **Main Application** ([`Core/Main.py`](Core/Main.py:1)): Orchestrates the conversation flow
- **Speech Processing** ([`Core/Speech_To_Text.py`](Core/Speech_To_Text.py:1), [`Core/Text_To_Speech.py`](Core/Text_To_Speech.py:1)): Handles audio input/output
- **Memory Management** ([`Core/Chat_Memory.py`](Core/Chat_Memory.py:1)): Short-term and long-term memory systems
- **LLM Integration** ([`Core/callLLM.py`](Core/callLLM.py:1)): Communication with language models
- **Configuration** ([`Core/Config_Manager.py`](Core/Config_Manager.py:1)): Centralized settings management

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- Voicemeeter Banana
- OpenRouter API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "tts stt ai"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Voicemeeter Banana**
    https://vb-audio.com/Voicemeeter/banana.htm

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

5. **Configure audio devices**
   Run Device_Helper.py (and follow the instructions)
   or
   Edit [`Core/config/config.yaml`](Core/config/config.yaml:1) to set your audio input/output device indices:
   


## 🎮 Usage

### Basic Operation

1. **Open VRCHAT**
   (make sure you have the audio set up correctly)

2. **Start the application**:
   ```bash
   python Core/Main.py
   ```
he config file for different voice characteristics


## 🔧 Configuration

### Audio Settings

Configure audio devices in [`Core/config/config.yaml`](Core/config/config.yaml:1):

```yaml
audio:
  input_device: 6      # Microphone device index
  output_device: 11    # Speaker device index  
  volume: 1            # TTS volume (0.0 - 1.0)
  length_scale: 1      # Speech speed (lower = faster)
  noise_scale: 0       # Voice variation
  noise_w_scale: 0     # Additional voice variation
  normalize_audio: false
```

### AI Personality

Customize the bot's behavior in [`Core/config/vrchat_bot_prompt.md`](Core/config/vrchat_bot_prompt.md:1):

- Modify the system prompt to change personality traits
- Adjust communication style and interaction guidelines
- Set VRChat-specific knowledge and social boundaries


### Common Issues

**API Connection Problems**
- Verify OpenRouter API key in .env file
- Check internet connectivity
- Monitor API rate limits and quotas

## 🤝 Contributing

This project is actively developed with a modular architecture approach. Contributions are welcome in areas such as:

- Enhanced error handling and recovery
- Additional TTS voice models
- Improved memory management algorithms
- VRChat OSC integration features
- Performance optimizations

## 🙏 Acknowledgments

- **RealtimeSTT**: For real-time speech-to-text capabilities
- **Piper TTS**: For high-quality text-to-speech synthesis
- **OpenRouter**: For LLM API access
- **ChromaDB**: For vector memory storage
- **VRChat Community**: For inspiration and use cases
- **AIcom**: im getting half these ideas from this
---
