def calculate_reward(state, action):
    reward = 0.0

    # Correct code fix
    if action.action_type == "fix_code":
        if state["submitted_code"] == state["correct_code"]:
            reward += 0.3
        else:
            reward -= 0.2

    # Add document
    if action.action_type == "add_document":
        if action.value in state["required_docs"]:
            reward += 0.2
        else:
            reward -= 0.1

    # Resubmit
    if action.action_type == "resubmit":
        if state["status"] == "approved":
            reward += 0.5
        else:
            reward -= 0.3

    return reward