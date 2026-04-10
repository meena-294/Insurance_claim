from fastapi import FastAPI
from env.healthcare_env import HealthcareEnv
from models.schemas import Action

app = FastAPI()

env = HealthcareEnv()

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/reset")
def reset():
    obs = env.reset()
    return {"observation": obs.dict()}

@app.post("/step")
def step(action: Action):
    result = env.step(action)
    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done,
        "info": result.info
    }

@app.get("/state")
def state():
    return env.state_view()
