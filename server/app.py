from fastapi import FastAPI
from pydantic import BaseModel
from env.healthcare_env import HealthcareEnv
from models.schemas import Action

app = FastAPI()

env = HealthcareEnv()


class ActionRequest(BaseModel):
    action_type: str
    value: str | None = None


@app.post("/reset")
def reset():
    obs = env.reset()
    return {"observation": obs.dict()}


@app.post("/step")
def step(action_req: ActionRequest):
    action = Action(**action_req.dict())
    result = env.step(action)

    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done,
        "info": result.info,
    }


@app.get("/state")
def state():
    return env.state_view()