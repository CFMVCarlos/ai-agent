from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models.agent import AgentRequest, AgentResponse
from src.services.agent import AgentService

router = APIRouter()
agent_service = AgentService()


@router.post("/run", response_model=AgentResponse)
async def run_agent_endpoint(request: AgentRequest):
    """
    Run the AI agent with the given prompt.
    """
    try:
        result = agent_service.run_agent(user_prompt=request.prompt, verbose=request.verbose)
        return AgentResponse(status="success", message=result, code=200)
    except Exception as e:  # noqa: BLE001
        # Global exception handler should catch it, but here we can return 500 cleanly
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "code": 500}
        )
