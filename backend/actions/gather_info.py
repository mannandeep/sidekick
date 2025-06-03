
def run(questions: list[str]):
    """Prompt the user for more information."""
    print("\n🤔 Sidekick needs more information before proceeding:")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")
    return {"status": "follow_up_needed", "questions": questions}
