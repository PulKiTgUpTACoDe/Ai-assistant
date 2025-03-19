import asyncio
import json
import logging
import os
import sys
from typing import Dict, List, Set
import websockets
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("websocket-service")

# Active WebSocket connections
connected_clients: Set[websockets.WebSocketServerProtocol] = set()

async def register(websocket: websockets.WebSocketServerProtocol):
    """Register a new client websocket connection."""
    connected_clients.add(websocket)
    logger.info(f"New client connected. Total clients: {len(connected_clients)}")
    
async def unregister(websocket: websockets.WebSocketServerProtocol):
    """Unregister a client websocket connection."""
    connected_clients.remove(websocket)
    logger.info(f"Client disconnected. Total clients: {len(connected_clients)}")

async def send_to_all(message: str):
    """Send a message to all connected clients."""
    if connected_clients:
        await asyncio.gather(
            *[client.send(message) for client in connected_clients]
        )

async def ws_handler(websocket: websockets.WebSocketServerProtocol, path: str):
    """Handle websocket connections and messages."""
    await register(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                logger.info(f"Received message: {data}")
                
                # Process message (will be implemented)
                if "type" in data:
                    if data["type"] == "chat":
                        # This will be implemented to call the actual AI agent
                        response = {
                            "type": "chat_response",
                            "message": "This is a placeholder response.",
                            "timestamp": asyncio.get_event_loop().time()
                        }
                        await websocket.send(json.dumps(response))
                    
                    # Broadcast messages to all clients if needed
                    # await send_to_all(json.dumps(response))
            
            except json.JSONDecodeError:
                logger.error("Invalid JSON message received")
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))
    except websockets.exceptions.ConnectionClosed:
        logger.info("Connection closed")
    finally:
        await unregister(websocket)

async def main():
    """Start the WebSocket server."""
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("WEBSOCKET_PORT", 8001))
    
    logger.info(f"Starting WebSocket server on {host}:{port}")
    async with websockets.serve(ws_handler, host, port):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
