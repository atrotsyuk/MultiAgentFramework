from pydantic import BaseModel
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Request, Query, UploadFile, File
import os, shutil
from fastapi.responses import FileResponse

from source.tools.conversation_results_manager import ConversationResultExtractor
from source.tools.agent_manager import agent_manager


class AgentParam(BaseModel):
    agent_name: str
    agent_description: str

class ConversationRequest(BaseModel):
    turns: str
    topic: str
    agent_uuids: List[str]



router = APIRouter()
# Serve index.html on root path
@router.get("/")
async def serve_index():
    return "App Running"


@router.post("/create-agents")
async def create_agents(req: List[AgentParam]):
    try:
        agent_params = [
            {
                "agent_name": agent.agent_name,
                "agent_description": agent.agent_description
            }
            for agent in req
        ]
        return agent_manager.build_agents(agent_params)
    except Exception as e:
        raise HTTPException(500, detail=f"Error creating agents: {e}")


@router.get("/get-agents-list")
async def get_agents_list():
    return agent_manager.get_agents_list()

@router.post("/run")
async def run(request: ConversationRequest):
    try:
        # agent_params = [
        #     {
        #         "agent_name": agent.agent_name,
        #         "agent_description": agent.agent_description
        #     }
        #     for agent in request.agent_params
        # ]

        extractor = ConversationResultExtractor(
            agent_uuids=request.agent_uuids,
            topic=request.topic,
            max_turns=int(request.turns)
        )

        extractor.run_conversation()
        extractor.fetch_and_parse_results()
        extractor.save_to_csv()

        results_dict = extractor.get_results_df()

        # agent1 = agent_params[0]['agent_name']
        # agent2 = agent_params[1]['agent_name']
        filename = f"output-{request.topic}_{request.turns}.csv"

        return {
            "message": f"Conversation complete. Saved to {filename}",
            "file": filename,
            "conversation": results_dict
        }


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversation failed: {str(e)}")

@router.get("/download")
async def download_csv(filename: str = Query(...)):
    file_path = os.path.join("static", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=filename, media_type='text/csv')


@router.post("/upload-transcripts")
async def upload_transcripts(files: List[UploadFile] = File(...)):
    saved_files = []
    upload_dir = os.path.join("static", "transcripts")
    os.makedirs(upload_dir, exist_ok=True)
    for file in files:
        file_location = os.path.join(upload_dir, file.filename)
        if not file.filename.endswith((".txt", ".vtt")):
            raise HTTPException(status_code=400, detail="Only .txt or .vtt files allowed")
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            saved_files.append(file.filename)
    
    return {"files_saved": saved_files, "status": "saved", "count": len(saved_files)}
