from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
import json

# Import from the correct structure
from ..core.engine import SelfingEngine

app = FastAPI(
    title="SelfingAI-v2",
    version="2.0.0",
    description="Cognitive Organism Engine with Existential, Boredom & Survival modules"
)

# Initialize the engine
engine = SelfingEngine(agent_id="main_agent")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "alive", 
        "version": "2.0.0",
        "message": "SelfingAI-v2 is running"
    }

@app.post("/process")
async def process_input(data: Dict):
    """Main endpoint to send input to the cognitive engine"""
    user_input = data.get("input", "")
    context_length = data.get("context_length", 0)
    complexity = data.get("complexity", 0.5)
    
    # Process the input through the full cognitive engine
    result = engine.process_input(
        user_input=user_input,
        context_length=context_length,
        complexity=complexity
    )
    
    # Get response style modifiers based on internal state
    modifiers = engine.get_response_modifier()
    
    return {
        "cognitive_state": result,
        "response_modifiers": modifiers,
        "message": "Cognitive state updated successfully"
    }

@app.get("/state")
async def get_state():
    """Get the current full cognitive state"""
    return engine.get_full_state()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time applications (Unity, web, games, etc.)"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                user_input = message.get("input", data)
                
                result = engine.process_input(user_input)
                
                await websocket.send_json({
                    "type": "cognitive_update",
                    "state": result,
                    "modifiers": engine.get_response_modifier()
                })
            except json.JSONDecodeError:
                # If not JSON, treat as plain text
                result = engine.process_input(data)
                await websocket.send_json({
                    "type": "cognitive_update",
                    "state": result
                })
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.close()

# For running directly: python -m app.api.routes
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
