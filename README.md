# AI Agent

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
GEMINI_API_KEY=your_gemini_api_key
WEATHER_API_KEY=your_weather_api_key
```

## Usage

1. Run the assistant:

```bash
python -m ai-agent.main
```

2. Voice Commands:

- "Open [application name]" - Opens specified application
- "Search for [query]" - Performs web search
- "Play [song name]" - Plays music
- "What's the time" - Tells current time
- "Weather in [city]" - Provides weather information
- "Take screenshot" - Captures screen
- "Set volume to [number]" - Adjusts system volume
- "Increase/Decrease volume" - Adjusts volume
- "Reset chat" - Clears chat history
- "Exit" - Closes the assistant

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
- Various Python libraries used in this project
