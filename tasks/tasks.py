TASKS = [
    {
        "name": "easy_claim",
        "objective": "Fix incorrect billing code",
        "success_condition": "code_correct"
    },
    {
        "name": "medium_claim",
        "objective": "Fix code and add required document",
        "success_condition": "ready_for_resubmit"
    },
    {
        "name": "hard_claim",
        "objective": "Fully resolve claim",
        "success_condition": "approved"
    }
]