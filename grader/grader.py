def grade(state):
    if state["status"] == "approved":
        return 1.0

    if state["submitted_code"] == state["correct_code"]:
        return 0.5

    return 0.0