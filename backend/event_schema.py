from pydantic import BaseModel
from typing import Optional, Literal, Dict

class Metadata(BaseModel):
    file: Optional[str] = None
    status: Optional[Literal["success", "failure"]] = "success"

class Event(BaseModel):
    session_id: str
    timestamp: float
    step: int
    action: Literal["read_file", "write_file", "run_command", "llm_call"]
    input: Optional[str] = ""
    output: Optional[str] = ""
    metadata: Optional[Metadata] = Metadata()