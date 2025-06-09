# AI Voice Agent

![image](https://github.com/user-attachments/assets/aadac9d8-d439-4d24-bd35-ce85552b4835)

A powerful Python-based AI voice agent that combines natural language processing, computer vision, and various tools to provide an intelligent voice assistant experience.

## 🌟 Key Features

### Voice & Speech

- Real-time voice recognition and speech synthesis
- Natural conversation flow with context awareness
- Multi-language support

### AI & Machine Learning

- Powered by Google Gemini AI for advanced language understanding
- Real-time object detection using YOLOv8
- Contextual image analysis with Gemini Vision Pro
- Vector-based memory using ChromaDB

### System Integration

- System control commands (shutdown, restart, volume)
- Application management
- Screenshot capture and analysis
- File system operations

### Information & Media

- Web search integration using Serper API
- YouTube music playback
- Weather information via WeatherAPI
- Latest news retrieval using NewsAPI
- Wikipedia knowledge base access
- Math calculations using Wolfram Alpha

### Automation & Tools

- WhatsApp automation
- Document reading and analysis
- Web scraping capabilities
- Image generation and recognition

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Windows OS (for system commands)
- Internet connection
- Microphone and speakers
- Git

### Step-by-Step Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ai-voice-assistant.git
   cd ai-voice-assistant
   ```

2. **Set Up Virtual Environment**

   ```bash
   # Create virtual environment
   python -m venv .mlvenv

   # Activate virtual environment
   # On Windows
   .mlvenv\Scripts\activate
   # On Unix or MacOS
   source .mlvenv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   # Upgrade pip
   python -m pip install --upgrade pip

   # Install requirements
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   ```bash
   # Copy example environment file
   cp .env.example .env
   ```

5. **Set Up API Keys**
   Edit the `.env` file and add your API keys:

   ```
   # AI Services
   GOOGLE_API_KEY=your_gemini_api_key

   # Weather and News
   WEATHER_API_KEY=your_weather_api_key
   NEWS_API_KEY=your_news_api_key

   # Search and Knowledge
   SERPAPI_API_KEY=your_serpapi_key
   WOLFRAM_ALPHA_APPID=your_wolfram_key

   # Voice Services
   PICOVOICE_ACCESS_KEY=your_picovoice_key

   # News API Credentials
   asknews_client_secret='your_secret'
   asknews_client_id='your_client_id'

   # Configuration
   DEBUG=True
   LOG_LEVEL=INFO

   # Database
   VECTOR_DB_PATH=ai-agent/database

   # Services
   API_HOST=0.0.0.0
   API_PORT=8000
   WEBSOCKET_PORT=8001

   # Langsmith Configuration
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
   LANGSMITH_API_KEY=your_langsmith_key
   LANGSMITH_PROJECT="Your project name"
   ```

6. **Initialize the Database**
   ```bash
   # The database will be automatically initialized on first run
   ```

### Running the Assistant

1. **Start the Assistant**

   ```bash
   python -m ai-agent.main
   ```

2. **Using Voice Commands**

   - Wait for the "Listening..." prompt
   - Speak your command clearly
   - The assistant will respond through voice and text

3. **Example Commands**
   - "What's the weather like today?"
   - "Play some music from YouTube"
   - "Take a screenshot and analyze it"
   - "Search Wikipedia for artificial intelligence"
   - "What's the latest news?"

## 📁 Project Structure

```
ai-agent/
├── config/             # Configuration files
├── core/              # Core functionality
│   ├── agents/        # AI Agents (LLM, RAG)
│   ├── memory/        # Context storage
│   ├── retrieval/     # Information retrieval
│   ├── tools/         # External API tools
│   └── utils/         # Helper functions
├── models/            # ML models
├── services/          # API services
├── database/          # Data storage
├── web/              # Frontend UI
├── tests/            # Test suite
├── scripts/          # Utility scripts
├── .env              # Environment variables
├── requirements.txt  # Dependencies
├── Dockerfile        # Container config
└── main.py          # Entry point
```

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI
- YOLOv8
- ChromaDB
- WeatherAPI
- Serper API
- Wolfram Alpha
- Wikipedia API
- NewsAPI
- All contributors and users
