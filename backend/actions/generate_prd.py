from ..llm.prd_generator import generate_prd


def run(summary: str):
    """Generate a product requirements document using the LLM."""
    return generate_prd(summary=summary)
