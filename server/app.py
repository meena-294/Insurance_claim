from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from env.healthcare_env import HealthcareEnv

app = FastAPI()

# Initialize environment
env = HealthcareEnv()


# Root endpoint (for health check)
@app.get("/")
def root():
    return {"status": "running"}


# ✅ RESET (MUST BE POST)
@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs.dict()
    }


# Action schema (if not already imported)
class Action(BaseModel):
    action_type: str
    value: Optional[str] = None


# ✅ STEP (MUST BE POST)
@app.post("/step")
def step(action: Action):
    result = env.step(action)

    return {
        "observation": result.observation.dict(),
        "reward": float(result.reward),
        "done": bool(result.done),
        "info": result.info if result.info else {}
    }


# State endpoint (GET is fine)
@app.get("/state")
def state():
    return env.state_view()
