from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    prompt: str = Field(..., title="Prompt", description="The user prompt to run the agent with.", min_length=1)
    verbose: bool = Field(default=False, title="Verbose", description="Enable verbose output.")

class AgentResponse(BaseModel):
    status: str = Field(..., title="Status", description="The status of the response, usually 'success' or 'error'.")
    message: str = Field(..., title="Message", description="The result message or error description.")
    code: int = Field(..., title="HTTP Code", description="The corresponding HTTP status code.")
