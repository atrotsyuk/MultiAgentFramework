from pydantic import BaseModel
from typing import List

from fastapi import APIRouter, HTTPException, Request, Query
import os
from fastapi.responses import FileResponse

# from app.backend.source.tools.conversation_results_manager import ConversationResultExtractor
from backend.source.tools.conversation_results_manager import ConversationResultExtractor


# from source import get_results
# from source.agent_conversation import 

# client = MongoClient("mongodb://localhost:27017/")
# db = client["mydb"]
# collection = db["items"]


class AgentParam(BaseModel):
    agent_name: str
    agent_description: str

class ConversationRequest(BaseModel):
    turns: str
    topic: str
    agent_params: List[AgentParam]



router = APIRouter()
# Serve index.html on root path
@router.get("/")
async def serve_index():
    index_path = os.path.join("frontend", "dist", "index.html")
    return FileResponse(index_path)

@router.post("/run")
async def run(request: ConversationRequest):
    try:
        agent_params = [
            {
                "agent_name": agent.agent_name,
                "agent_description": agent.agent_description
            }
            for agent in request.agent_params
        ]

        extractor = ConversationResultExtractor(
            agent_params=agent_params,
            topic=request.topic,
            max_turns=int(request.turns)
        )

        extractor.run_conversation()
        extractor.fetch_and_parse_results()
        extractor.save_to_csv()

        results_dict = extractor.get_results_df()

        agent1 = agent_params[0]['agent_name']
        agent2 = agent_params[1]['agent_name']
        filename = f"output-{agent1}_{agent2}_{request.turns}.csv"

        return {
            "message": f"Conversation complete. Saved to {filename}",
            "file": filename,
            "conversation": results_dict
        }


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversation failed: {str(e)}")

@router.get("/download")
async def download_csv(filename: str = Query(...)):
    file_path = os.path.join("backend", "static", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=filename, media_type='text/csv')

