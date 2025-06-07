from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatLiteLLM


def run(summary: str):
    """Generate a product requirements document using the LLM."""
    print("📝 Generating PRD based on summary:", summary)

    template = """
You are Sidekick, an AI assistant that helps Product Managers create clear, structured Product Requirement Documents (PRDs).

Using the project summary below, create a PRD using Figma’s internal format.

---

Project Summary: "{summary}"

---

Respond ONLY in this format:

# Problem
[What is the user problem or opportunity?]

# Audience
[Who is affected?]

# Solution
[What are you building and why is it valuable? What’s in scope? What’s out of scope?]

# Requirements
[What functionality must be built? Bullet points preferred.]

# User Experience
[How will the user experience this feature? Can be narrative or UX goals.]

# Metrics
[What success looks like — e.g., adoption, engagement, speed.]

# Milestones
[Estimated milestones — planning, dev, review, launch.]
"""

    prompt = PromptTemplate.from_template(template)

    llm = ChatLiteLLM(
        model="mistral",
        api_base="http://localhost:1234/v1",
        api_key="not-needed",
        custom_llm_provider="openai"
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    prd = chain.run(summary=summary)

    print("\n📄 Final PRD:\n", prd)
    return prd
