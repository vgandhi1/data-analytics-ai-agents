from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import asyncio
from team.analyzer_gpt import getDataAnalyzerTeam
from config.openai_model_client import get_model_client
from config.docker_utils import getDockerCommandLineExecutor, start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage

app = FastAPI()

class AnalysisRequest(BaseModel):
    task: str
    filename: str = "data.csv"

@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    model_client = get_model_client()
    docker_executor = getDockerCommandLineExecutor()
    team = getDataAnalyzerTeam(docker_executor, model_client, request.filename)
    
    try:
        await start_docker_container(docker_executor)
        
        final_response = ""
        # Run the agent team
        async for message in team.run_stream(task=request.task):
            if isinstance(message, TextMessage):
                final_response = message.content
        
        # Read the generated code file if it exists
        generated_code = ""
        try:
            with open("temp/generated_analysis.py", "r") as f:
                generated_code = f.read()
        except FileNotFoundError:
            generated_code = "# No code file generated."

        return {
            "status": "success",
            "message": final_response,
            "output_file": "output.png", # Path relative to the shared volume
            "generated_code": generated_code
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await stop_docker_container(docker_executor)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
