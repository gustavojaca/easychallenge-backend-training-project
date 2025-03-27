from pydantic import BaseModel

class Challenge(BaseModel):
    challenge: str
    solution: str = None