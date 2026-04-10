from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional
from env.healthcare_env import HealthcareEnv

app = FastAPI()

env = HealthcareEnv()


# Health check
@app.get("/")
def root():
    return {"status": "running"}


# ✅ RESET (POST, no input required)
@app.post("/reset")
async def reset():
    obs = env.reset()

    return {
        "observation": obs.dict() if hasattr(obs, "dict") else obs
    }


# Action schema
class Action(BaseModel):
    action_type: str
    value: Optional[str] = None


# ✅ STEP (POST with JSON body)
@app.post("/step")
async def step(action: Action = Body(...)):
    result = env.step(action)

    return {
        "observation": result.observation.dict() if hasattr(result.observation, "dict") else result.observation,
        "reward": float(result.reward),
        "done": bool(result.done),
        "info": result.info if result.info else {}
    }


# State endpoint
@app.get("/state")
def state():
    return env.state_view()
