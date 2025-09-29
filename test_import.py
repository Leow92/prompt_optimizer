from dotenv import load_dotenv
load_dotenv()

from leo_prompt_optimizer import (
    optimize_prompt,
    set_client,
    set_groq_api_key,
    set_openai_api_key,
)

# Optionally: set API key manually
# set_groq_api_key("[YOUR GROQ KEY]")
# or
# set_openai_api_key("[YOUR OPEN AI KEY]")

# Mandatory: configure the client
set_client(provider="groq")

# Example draft prompt
draft = """
<role>
  You are an experienced curriculum designer and communication specialist for AI education.
</role>

<task>
  Create a comprehensive plan for a Generative AI (GenAI) course, including a clearly itemized agenda and tailored communication materials for the enrolled members.
</task>

<instructions>
  • Begin with an **Agenda**: list each session with its title, key topic, and duration.  
  • For every agenda item, write a brief paragraph (≈3–4 sentences) that explains:  
    – the learning objectives,  
    – the core content to be covered, and  
    – the suggested teaching method (e.g., lecture, workshop, hands‑on exercise).  
  • After the agenda, add a **Communication Strategy** paragraph that describes how to keep participants engaged, the main messages, and the communication channels (e.g., email, Slack, live chat).  
  • Conclude with a concise **Course Summary** paragraph highlighting the overall value proposition and expected outcomes.  
  • Use plain text; avoid markdown or special formatting unless requested.
</instructions>

<context>
  The course is designed for:  
  • **Target Audience**: [PLACEHOLDER: e.g., mid‑level professionals, graduate students, hobbyists]  
  • **Duration**: [PLACEHOLDER: e.g., 6 weeks, 12 hours total]  
  • **Core Topics**: [PLACEHOLDER: e.g., GPT‑style models, prompt engineering, ethics, real‑world applications]  
  • **Prerequisites**: [PLACEHOLDER: e.g., basic programming, familiarity with machine learning]  
  • **Learning Environment**: [PLACEHOLDER: e.g., online synchronous, blended, self‑paced]  
</context>

<examples>
  <example>
    <input>
      Target Audience: Marketing professionals  
      Duration: 4 weeks  
      Core Topics: Prompt creation, content generation, audience analysis
    </input>
    <output>
      1. Agenda  
        • Week 1 – Introduction to GenAI: Overview & Use Cases (2 hrs)  
        • Week 2 – Prompt Engineering Basics (3 hrs)  
        • Week 3 – Content Generation & Personalization (3 hrs)  
        • Week 4 – Ethics, Governance, & Course Wrap‑up (2 hrs)  

      2. Session Descriptions  
        • Week 1: Students will learn the fundamentals of generative models, explore real‑world marketing applications, and set expectations for the course.  
        • Week 2: Participants will craft effective prompts, experiment with different styles, and receive immediate feedback in a hands‑on lab.  
        • Week 3: Learners will apply prompt techniques to generate targeted ad copy, social‑media posts, and product descriptions, then assess quality against key performance metrics.  
        • Week 4: Attendees will discuss ethical considerations, establish governance policies, and outline next steps for integrating GenAI into their workflow.  

      3. Communication Strategy  
        • Weekly email newsletters summarizing key takeaways; Slack channel for Q&A; live chat during sessions for real‑time support.  

      4. Course Summary  
        • By completing this course, participants will confidently design and deploy GenAI solutions to enhance marketing effectiveness while adhering to ethical best practices.
    </output>
  </example>
</examples>

<output-format>
Plain‑text document with the following sections in order:  
1. **Agenda** (bullet list)  
2. **Session Descriptions** (paragraph per agenda item)  
3. **Communication Strategy** (paragraph)  
4. **Course Summary** (paragraph)
</output-format>

<user-input>
[PLACEHOLDER: Insert the specific audience, duration, core topics, prerequisites, and learning environment]
</user-input>
"""

context = """
The audience of the training is employees of a bank in Belgium. The language of the training is French.
"""

# Optional: context
user_input = None
llm_output = None

# Optimize
optimized = optimize_prompt(
    prompt_draft=draft,
    top_instruction=context
)

print("\n✅ --- Optimized Prompt ---\n")
print(optimized)
