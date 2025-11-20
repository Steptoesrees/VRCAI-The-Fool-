# VRChat AI Bot - TTS/STT System

~~A sophisticated AI companion bot for VRChat that provides real-time speech-to-text and text-to-speech capabilities with intelligent conversation management and memory systems.~~
yea as if, this ai readme is a bit wrong there, this is EXTREMELY EARLY IN DEVELOPMENT

## 🚀 Overview

This project creates an AI companion that can engage in natural conversations within VRChat environments. The system combines real-time speech processing with large language models to create an immersive, interactive experience. :3

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- Voicemeeter Banana
- OpenRouter API key

### Setup

1: **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "tts stt ai"
   ```

1.2: **Or Download from releases and extract from the zip folder**

2: **run run.py**


## 🎮 Usage

### Basic Operation

1. **Open VRCHAT**

2. **Set up your audio cables to have audio from VRC sent into the app via a (virtual)microphone**

3. **Start the application**:
   Run run.py


## 🔧 Configuration

### AI Personality

Customize the bot's behavior in the personality tab:

- change personality traits
- Adjust communication style and interaction guidelines
- Set VRChat-specific knowledge and social boundaries

### AI voice
The TTS currently only uses pipertts

Add new TTS voices by saving the voice .onnx and .json file in the Models folde

voices can be found here: 
https://huggingface.co/rhasspy/piper-voices
https://www.nexusmods.com/skyrimspecialedition/mods/98631?tab=files

etc, there are loads on the internet

### Common Issues

**API Connection Problems**
- Check OpenRouter API key
- Check internet connectivity
- Monitor API rate limits and quotas

## 🤝 Contributing

This project is actively developed with a modular architecture approach. Contributions are welcome in areas such as:

- Enhanced error handling and recovery
- Additional TTS voice models
- VRChat OSC integration features
- Performance optimizations

## 🙏 Acknowledgments

- **RealtimeSTT**: For real-time speech-to-text capabilities
- **Piper TTS**: For high-quality text-to-speech synthesis
- **OpenRouter**: For LLM API access
- **ChromaDB**: For vector memory storage 
- **VRChat Community**: For inspiration and use cases
- **AIcom**: I'm getting half these ideas from this


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.
---
