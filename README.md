# AI Voice Agent
![image](https://github.com/user-attachments/assets/aadac9d8-d439-4d24-bd35-ce85552b4835)

A Python-based AI voice agent that can perform various tasks using voice commands and natural language processing.

## Features

- Voice recognition and speech synthesis
- Natural language processing using Google's Gemini AI
- System control commands (volume, shutdown, restart)
- Weather information
- Web search capabilities
- Music playback
- Screenshot capture
- Chat history management
- Open applications
- Wikipedia search
- Math calculations
- News retrieval
- Current time retrieval

## Prerequisites

- Python 3.8 or higher
- Windows OS (for system commands)
- Internet connection
- Microphone and speakers

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ai-voice-assistant.git
cd ai-voice-assistant
```

2. Create and activate a virtual environment:

```bash
python -m venv .mlvenv
# On Windows
.mlvenv\Scripts\activate
# On Unix or MacOS
source .mlvenv/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

5. Add your API keys to the `.env` file:

```
GOOGLE_API_KEY=your_gemini_api_key
WEATHER_API_KEY=your_weather_api_key
DEEPSEEK_API_KEY=api_key
PICOVOICE_ACCESS_KEY=api_key
SERPAPI_API_KEY=api_key
WOLFRAM_ALPHA_APPID=api_id

# GOOGLE_CSE_ID=client_id

# Ask news credenials
asknews_client_secret='secret'
asknews_client_id='client_id'

# Configuration
DEBUG=True
LOG_LEVEL=INFO

# Database
VECTOR_DB_PATH=ai-agent/database/faiss_index

# Services
API_HOST=0.0.0.0
API_PORT=8000
WEBSOCKET_PORT=8001

# Langsmith congif
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=api_key
LANGSMITH_PROJECT="Your project name"
```

## Usage

1. Run the assistant:

```bash
python -m ai-agent.main
```

## Project Structure

```
ai-agent/
│── config/                  # Configuration files (YAML/JSON)
│── core/                    # Core logic
│   ├── agents/              # AI Agents (LLM, RAG, etc.)
│   ├── memory/              # Context storage (FAISS, Pinecone, etc.)
│   ├── retrieval/           # Information retrieval (RAG-based)
│   ├── tools/               # External API tools (Google, Wolfram, etc.)
│   ├── utils/               # Helper functions (file handling, logs, etc.)
│
│── models/                  # Pretrained or fine-tuned ML models
│── services/                # API services & orchestration
│   ├── api.py               # REST API (FastAPI)
│   ├── websocket.py         # Real-time communication
│
│── database/                # Long-term storage
│   ├── faiss_index/         # Vector embeddings storage
│   ├── chat_history.json    # Persistent conversation history
│
│── web/                     # Frontend UI or chatbot UI
│── tests/                   # Unit tests & integration tests
│── scripts/                 # Utility scripts for automation
│── .env                     # Environment variables
│── requirements.txt         # Dependencies
│── Dockerfile               # Containerization
│── main.py                  # Entry point
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for natural language processing
- WeatherAPI for weather information
- Serper API for web search
- Wolfram Alpha API for math calculations
- Wikipedia API for knowledge retrieval
- AskNews API for news retrieval
- Various Python libraries used in this project
