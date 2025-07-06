# text2srt_tts

[![Version](https://img.shields.io/badge/Version-v1.1.3-blue.svg)](https://github.com/sheng1111/text2srt_tts)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit)](https://text2tts.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/sheng1111/text2srt_tts)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue?style=flat-square&logo=docker)](https://docker.com/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sheng1111/text2srt_tts/blob/main/colab_run.ipynb)

One-click conversion of text to high-quality speech (WAV & MP3) and accurate subtitles (SRT), with real-time preview and download functionality in a modern single-page Streamlit UI. Features intelligent text segmentation, bilingual support, and enhanced user experience with sidebar controls.

## 🆕 What's New in v1.1.3

- **🎨 Single-Page Interface**: Modern sidebar-based layout that adapts to dark/light themes
- **🧠 Enhanced SRT Generation**: Advanced punctuation handling and intelligent text segmentation
- **🌐 Bilingual Support**: Seamless switching between Traditional Chinese and English
- **📊 Real-time Feedback**: Live character count, progress tracking, and status indicators
- **🔧 Improved Docker**: Optimized containerization with health checks and persistent storage
- **💡 Smart Spacing**: Automatic spacing correction and punctuation preservation options
- **🎛️ Sidebar Controls**: All settings organized in an expandable sidebar for better workflow

## ✨ Core Features

### 🎤 Text-to-Speech (TTS) Engine

- **Default Engine (Free)**: `Edge TTS` - Microsoft Edge's built-in speech synthesis, no API key required
- **Premium Engine (Optional)**: `Azure Speech Service` - Professional-grade natural speech synthesis
- **Automatic Fallback**: Seamless fallback to Edge TTS if Azure fails
- **Voice Customization**: Adjustable speed (-50% to +50%), pitch, and volume parameters
- **Word Boundary Extraction**: Precise timing information for perfect subtitle synchronization

### 📜 Intelligent Subtitle Generation

- **Smart Text Segmentation**: Advanced algorithm that considers natural language breaks and punctuation
- **Punctuation Control**: Option to preserve or remove punctuation marks in subtitles
- **Spacing Optimization**: Automatic correction of spacing issues around punctuation and quotes
- **Flexible Line Length**: Configurable character limits per subtitle line (20-80 characters)
- **Natural Break Points**: Detection of sentence endings, transition words, and speech pauses
- **Multi-language Support**: Optimized for both English and Chinese text processing

### 🖥️ Modern Single-Page Interface

- **Sidebar Layout**: All settings organized in an expandable sidebar for clean workflow
- **Theme Adaptive**: Automatically adapts to Streamlit's dark/light theme modes
- **Real-time Status**: Live character count, generation progress, and status indicators
- **Bilingual Interface**: Toggle between Traditional Chinese and English in the sidebar
- **Quick Tips**: Expandable help section with usage recommendations
- **Responsive Design**: Optimized for various screen sizes and devices

### 🚀 Deployment Options

- **Streamlit Web App**: Interactive single-page interface with sidebar controls
- **Enhanced Docker**: Optimized containerization with health checks and persistent volumes
- **Docker Compose**: Complete orchestration with networking and environment management
- **Command-Line Interface**: Batch processing capabilities for automation
- **Google Colab**: Cloud-based execution without local setup requirements

## 📸 Interface Preview

### Single-Page Layout with Sidebar Controls

![Modern Interface](docs/img/setting.png)

### Generation Results and Downloads

![Results Interface](docs/img/result.png)

## 🏗️ Project Architecture

```
text2srt_tts/
├── app/
│   ├── services/              # Core business logic
│   │   ├── voice.py          # TTS synthesis (Azure & Edge)
│   │   └── subtitle.py       # Enhanced subtitle generation
│   ├── ui/                   # User interface components
│   │   └── gui.py           # Single-page Streamlit application
│   ├── utils/               # Utility functions
│   │   └── text_to_srt.py   # SRT formatting utilities
│   └── cli/                 # Command-line interface
│       └── __main__.py      # CLI entry point
├── locales/                 # Internationalization
│   ├── zh_TW.toml          # Traditional Chinese
│   └── en.toml             # English
├── docker/                  # Docker configuration
├── docs/                    # Documentation assets
│   └── img/                # Screenshots and images
├── task/                    # Generated output files
│   └── {task_id}/          # Individual task results
├── tests/                   # Unit tests
├── Dockerfile              # Optimized Docker configuration
├── docker-compose.yml      # Complete orchestration setup
├── .dockerignore           # Docker build optimization
├── config.example.toml      # Configuration template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Local Installation

    ```bash

# Clone the repository

    git clone https://github.com/sheng1111/text2srt_tts.git
    cd text2srt_tts

# Create virtual environment

    python3 -m venv .venv
    source .venv/bin/activate  # Linux/macOS

# .venv\Scripts\activate # Windows

# Install dependencies

    pip install -r requirements.txt

# Launch the application

streamlit run app/ui/gui.py

```

### 2. Docker Deployment (Recommended)

#### Quick Setup with Docker Compose

    ```bash

# Clone and navigate to project

git clone https://github.com/sheng1111/text2srt_tts.git
cd text2srt_tts

# Start with Docker Compose

docker-compose up --build

# Access application at http://localhost:8501

```

#### Manual Docker Build

```bash
# Build the image
docker build -t text2srt_tts .

# Run the container
docker run -p 8501:8501 -v ./task:/app/task text2srt_tts

# With environment variables
docker run -p 8501:8501 \
  -e AZURE_KEY="your-key" \
  -e AZURE_REGION="your-region" \
  -v ./task:/app/task \
  text2srt_tts
```

### 3. Configuration (Optional)

```bash
# Copy configuration template
cp config.example.toml config.toml

# Edit configuration file
# - Add Azure credentials for premium TTS (optional)
# - Configure voice options and preferences
# - Set FFmpeg path if needed for MP3 output
```

## 🔧 Configuration Options

### Voice Settings

Configure available voices in `config.toml`:

```toml
[voices]
"Chinese Female" = { name = "zh-CN-XiaoxiaoNeural" }
"Chinese Male" = { name = "zh-CN-YunxiNeural" }
"English Female" = { name = "en-US-AriaNeural" }
"English Male" = { name = "en-US-GuyNeural" }
"Japanese Female" = { name = "ja-JP-NanamiNeural" }
"Japanese Male" = { name = "ja-JP-KeitaNeural" }
```

### Azure TTS Setup (Optional)

For premium quality speech synthesis:

```toml
AZURE_KEY = "your-azure-key"
AZURE_REGION = "your-region"
```

### Docker Environment Variables

Set these in a `.env` file for Docker deployment:

```bash
# Azure TTS (optional)
AZURE_KEY=your-azure-key
AZURE_REGION=your-region

# Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 💡 Usage Tips

### Single-Page Interface

- **Sidebar Controls**: All settings are organized in the left sidebar
- **Theme Adaptation**: Interface automatically adapts to your Streamlit theme preference
- **Language Switching**: Use the language selector in the sidebar top section
- **Progress Tracking**: Watch real-time progress during generation in the main area

### Text Input Best Practices

- Use proper punctuation for natural speech pauses
- Keep sentences clear and concise for better segmentation
- Avoid excessive special characters
- Test with shorter texts first for optimal results

### Subtitle Optimization

- **Punctuation Preservation**: Toggle in sidebar to keep or remove punctuation marks
- **Line Length**: Adjust based on content type (20-40 for mobile, 40-80 for desktop)
- **Natural Breaks**: Algorithm automatically detects sentence endings and transition words
- **Spacing Control**: Automatic correction of spacing around punctuation and quotes

### Voice Parameter Tuning

- **Rate**: -50% to +50% (negative slows down, positive speeds up)
- **Pitch**: -50% to +50% (negative lowers, positive raises)
- **Volume**: -50% to +50% (negative decreases, positive increases)

## 🌐 Multi-Language Support

The application supports:

- **Interface Languages**: Traditional Chinese (zh_TW), English (en)
- **Text Processing**: Optimized for Chinese and English content with proper punctuation handling
- **Voice Options**: Multiple language-specific voices available through sidebar selection

Switch languages using the dropdown in the sidebar's language section.

## 🐳 Docker Features

### Enhanced Containerization

- **Multi-stage Build**: Optimized for smaller image size and faster builds
- **Health Checks**: Automatic monitoring of application health
- **Non-root User**: Enhanced security with dedicated application user
- **Persistent Storage**: Volume mounting for generated files
- **Environment Management**: Complete configuration through environment variables

### Production Ready

- **Resource Optimization**: Efficient memory and CPU usage
- **Automatic Restart**: Container restarts on failure unless manually stopped
- **Network Isolation**: Dedicated Docker network for security
- **Log Management**: Structured logging for monitoring and debugging

## 📊 Performance & Limitations

### Performance Characteristics

- **Processing Speed**: ~5-10 seconds per minute of speech
- **Memory Usage**: ~100-500MB depending on text length
- **Storage**: ~1-5MB per minute of generated content
- **Container Size**: ~800MB Docker image with all dependencies

### Current Limitations

- Maximum text length: ~10,000 characters per generation
- Supported audio formats: WAV (default), MP3 (with FFmpeg)
- Internet connection required for TTS synthesis
- Sidebar requires minimum screen width for optimal display

## 🧪 Testing

Run the test suite:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest

# Run specific test modules
pytest tests/test_subtitle.py
pytest tests/test_voice.py

# Run with coverage
pytest --cov=app tests/
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 app/
black app/

# Run type checking
mypy app/

# Test Docker build locally
docker build -t text2srt_tts:dev .
docker run -p 8501:8501 text2srt_tts:dev
```

## 📝 Changelog

### v1.1.3 (Current)

- Single-page interface with sidebar controls
- Enhanced SRT generation with punctuation handling
- Theme-adaptive design (dark/light mode support)
- Improved Docker deployment with health checks
- Real-time progress tracking and status indicators
- Better error handling and user feedback
- Optimized spacing and text processing algorithms

### v1.0.1

- Initial release with basic TTS and subtitle generation
- Tabbed Streamlit interface
- Azure and Edge TTS support
- Basic Docker deployment

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Microsoft Edge TTS**: Free speech synthesis service
- **Azure Cognitive Services**: Premium TTS capabilities
- **Streamlit**: Modern web application framework
- **Docker**: Containerization platform
- **Python Community**: Excellent libraries and tools

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/sheng1111/text2srt_tts/wiki)
- **Issues**: [GitHub Issues](https://github.com/sheng1111/text2srt_tts/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sheng1111/text2srt_tts/discussions)

---

**⭐ Star this project** if it helped you create better subtitles and speech content!
