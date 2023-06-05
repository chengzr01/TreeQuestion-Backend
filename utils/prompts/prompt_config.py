from typing import Final

PROMPT_CONFIGS: Final[dict] = {
    "instructions": {
        "ideation": "./utils/prompts/instructions/ideation.txt",
        "knowledge": "./utils/prompts/instructions/knowledge.txt",
        "graph": "./utils/prompts/instructions/graph.txt",
        "key": "./utils/prompts/instructions/key.txt",
        "heuristics": "./utils/prompts/instructions/heuristics.txt",
        "distractors": "./utils/prompts/instructions/distractors.txt",
        "distractors-part":
        "./utils/prompts/instructions/distractors-part.txt",
        "keys-part": "./utils/prompts/instructions/keys-part.txt",
        "true-false": "./utils/prompts/instructions/true-false.txt",
        "multiple-choice": "./utils/prompts/instructions/multiple-choice.txt",
    },
    "taxonomy": {
        "remember": "./utils/prompts/taxonomy/remember.txt",
        "understand": "./utils/prompts/taxonomy/understand.txt",
        "apply": "./utils/prompts/taxonomy/apply.txt",
        "analyze": "./utils/prompts/taxonomy/analyze.txt",
        "evaluate": "./utils/prompts/taxonomy/evaluate.txt",
        "create": "./utils/prompts/taxonomy/create.txt",
    }
}


def retrieve_prompt_prefix(part_name: str) -> dict:
    def open_file(data: dict):
        return {
            key: open_file(value) if isinstance(value, dict) else open(
                value, "r").read()
            for key, value in data.items()
        }

    filename_dict = PROMPT_CONFIGS[part_name]
    return open_file(filename_dict)
