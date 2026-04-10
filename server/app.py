from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from env.healthcare_env import HealthcareEnv

app = FastAPI()

env = HealthcareEnv()


# Health check
@app.get("/")
def root():
    return {"status": "running"}


# ✅ MUST accept POST (no params)
@app.post("/reset")
async def reset():
    obs = env.reset()

    return {
        "observation": obs.dict()
    }


# Action schema
class Action(BaseModel):
    action_type: str
    value: Optional[str] = None


# ✅ MUST accept JSON body
@app.post("/step")
async def step(action: Action):
    result = env.step(action)

    return {
        "observation": result.observation.dict(),
        "reward": float(result.reward),
        "done": bool(result.done),
        "info": result.info if result.info else {}
    }


# State endpoint
@app.get("/state")
def state():
    return env.state_view()
