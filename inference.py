import os
from openai import OpenAI
from models.schemas import Action
from env.healthcare_env import HealthcareEnv

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)


def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done, error):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error}",
        flush=True
    )


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)


def main():
    env = HealthcareEnv()
    rewards = []

    log_start("healthcare_claim", "openenv", MODEL_NAME)

    obs = env.reset()

    for step in range(1, 7):

        # Simple rule-based agent
        if obs.submitted_code != "X456":
            action = Action(action_type="fix_code", value="X456")
        elif "authorization" not in obs.documents:
            action = Action(action_type="add_document", value="authorization")
        else:
            action = Action(action_type="resubmit")

        result = env.step(action)

        rewards.append(result.reward)

        log_step(step, action.action_type, result.reward, result.done, "null")

        obs = result.observation

        if result.done:
            break

    score = min(max(sum(rewards), 0.0), 1.0)
    success = score > 0.5

    env.close()

    log_end(success, step, score, rewards)


if __name__ == "__main__":
    main()