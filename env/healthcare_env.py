import uuid
from typing import List
from models.schemas import Observation, Action, StepResult
from reward.reward import calculate_reward
from grader.grader import grade


class HealthcareEnv:

    def __init__(self, max_steps=6):
        self.max_steps = max_steps
        self.current_step = 0
        self.done = False
        self.state = None

    def reset(self):
        self.current_step = 0
        self.done = False

        self.state = {
            "claim_id": str(uuid.uuid4()),
            "procedure": "MRI Scan",
            "submitted_code": "X123",
            "correct_code": "X456",
            "documents": [],
            "required_docs": ["authorization"],
            "status": "denied",
            "denial_reasons": ["Incorrect code", "Missing document"]
        }

        return self._get_obs()

    def _get_obs(self):
        return Observation(
            claim_id=self.state["claim_id"],
            procedure=self.state["procedure"],
            submitted_code=self.state["submitted_code"],
            denial_reasons=self.state["denial_reasons"],
            documents=self.state["documents"],
            status=self.state["status"]
        )

    def step(self, action: Action):
        if self.done:
            return StepResult(
                observation=self._get_obs(),
                reward=0.0,
                done=True,
                info={"error": "Episode finished"}
            )

        self.current_step += 1
        info = {"error": None}

        # Apply action
        if action.action_type == "fix_code":
            self.state["submitted_code"] = action.value

        elif action.action_type == "add_document":
            self.state["documents"].append(action.value)

        elif action.action_type == "resubmit":
            if (
                self.state["submitted_code"] == self.state["correct_code"]
                and all(doc in self.state["documents"] for doc in self.state["required_docs"])
            ):
                self.state["status"] = "approved"
                self.done = True
            else:
                self.state["status"] = "denied"

        # Calculate reward
        reward = calculate_reward(self.state, action)

        # Done condition
        if self.current_step >= self.max_steps:
            self.done = True

        return StepResult(
            observation=self._get_obs(),
            reward=reward,
            done=self.done,
            info=info
        )

    def state_view(self):
        return self.state

    def close(self):
        pass