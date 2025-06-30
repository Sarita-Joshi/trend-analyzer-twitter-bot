import random
from typing import List
from src.schemas.article_schema import ArticleSchema
from src.llm.llm_client import LLMClient

EXAMPLES = [
    {
        "context": "Electric car sales surged 40% globally last year, but supply chain issues are causing long wait times. Meanwhile, governments in Europe are pushing stricter emission regulations.",
        "poll": "EVs are booming with sales surged by 40%, but not able to feed the demand due to restriction and bottlenecks. Should governments ease regulations to speed up production?",
        "options": ["Yes, prioritize availability", "Keep strict rules", "Offer subsidies instead", "Not sure"]
    },
    {
        "context": "The UN just released a report warning of record-breaking heatwaves and wildfires this summer. Some cities are already imposing water restrictions and curfews to manage the crisis.",
        "poll": "With heatwaves worsening, should cities enforce stricter water and energy curbs during summer emergencies?",
        "options": ["Absolutely, save resources", "No, it's too extreme", "Only voluntary limits", "Depends on severity"]
    },
    {
        "context": "A blockbuster video game sequel broke launch day sales records but sparked backlash over heavy microtransactions and loot boxes. Consumer groups are calling for tighter regulations on in-game purchases.",
        "poll": "A blockbuster video game sequel broke launch day sales records but sparked backlash over heavy microtransactions and loot boxes. Consumer groups are calling for tighter regulations on in-game purchases. Should regulators clamp down on microtransactions and loot boxes in popular video games?",
        "options": ["Yes, protect players", "No, let the market decide", "Only for kids' games", "Not sure"]
    }
]

class PollGenerator:
    def __init__(self, topic: str):
        self.topic = topic
        self.llm_client = LLMClient(provider='gemini')

    def generate_prompt(self, summary: List[str]) -> str:
        bullet_points = [f"- {a.strip()}" for a in summary]
        context = "\n".join(bullet_points)
        few_shot_examples = "\n\n".join([
            f"Context:\n{e['context']}\nPoll Question: {e['poll']}\nOptions: {', '.join(e['options'])}"
            for e in EXAMPLES
        ])

        return f"""
You are a social media strategist who crafts viral polls for X (formerly Twitter) based on current news and trending topics.
Given a context with recent article headlines or developments, generate a sharp, engaging poll that:
- Summarizes with references to at least 2 specific developments or examples from the context to ground it in real current events.
- Provide a specific insight, why the poll, topic and context is important; why you selected the particular options for poll.
- Uses a conversational, slightly provocative tone as if written by a savvy human social media strategist.
- Is brief and clear, optimized for X's fast-scrolling audience — keep the poll question under 280 characters (2-4 sentences).
- Produces 4 or fewer concise options that cover a range of opinions or possible answers.
- Limit Question to 280 chars.


Format your response as:
Poll Question: <Your question here>
Options: <option1> | <option2> | ... (MAX 4)

{few_shot_examples}

Context:
{context}
"""

    def generate_poll(self, articles: List[ArticleSchema]) -> dict:
        prompt = self.generate_prompt(articles)
        response = self.llm_client.complete(prompt)

        try:
            poll_line = next(line for line in response.split("\n") if line.startswith("Poll Question:"))
            options_line = next(line for line in response.split("\n") if line.startswith("Options:"))
            poll = poll_line.replace("Poll Question:", "").strip()
            options = [opt.strip() for opt in options_line.replace("Options:", "").split("|") if opt.strip()]
            return {"question": poll, "options": options}
        except Exception as e:
            print("Failed to parse poll:", e)
            return {"question": "What’s your take on this week’s tech headlines?", "options": ["Exciting", "Worrying", "Confusing", "Overhyped"]}
