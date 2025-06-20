import random
from collections import defaultdict

class PollGenerator:
    def __init__(self, options_per_poll=3):
        self.options_per_poll = options_per_poll

    def generate_poll_question(self, label, summaries):
        template = random.choice([
            f"What are your thoughts on {label}?",
            f"Do you support recent updates in {label}?",
            f"Which aspect of {label} concerns you the most?",
            f"What should be prioritized in {label}?"
        ])
        return template

    def summarize_snippets(self, summaries, max_len=120):
        seen = set()
        options = []
        for s in summaries:
            text = s['summary']
            if text not in seen:
                seen.add(text)
                options.append(text[:max_len].rstrip(".") + "...")
            if len(options) >= self.options_per_poll:
                break
        return options

    def generate_polls(self, labeled_data):
        cluster_map = defaultdict(list)
        for item in labeled_data:
            cluster_map[item["cluster_id"]].append(item)

        polls = []
        for cluster_id, items in cluster_map.items():
            label = items[0]["cluster_label"]
            question = self.generate_poll_question(label, items)
            options = self.summarize_snippets(items)
            polls.append({
                "cluster_id": cluster_id,
                "topic": label,
                "question": question,
                "options": options,
            })

        return polls


if __name__ == "__main__":

    generator = PollGenerator(options_per_poll=3)
    polls = generator.generate_polls(labeled_data)

    for poll in polls:
        print(f"\nQ: {poll['question']}")
        for i, opt in enumerate(poll["options"]):
            print(f"  {chr(65+i)}. {opt}")
