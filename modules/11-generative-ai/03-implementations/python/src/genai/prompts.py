from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PromptTemplate:
    name: str
    template: str
    input_vars: Iterable[str]

    def render(self, **kwargs: str) -> str:
        missing = [var for var in self.input_vars if var not in kwargs]
        if missing:
            raise ValueError(f"Missing input vars: {', '.join(missing)}")
        return self.template.format(**kwargs)


BUILTIN_TEMPLATES = {
    "classify": PromptTemplate(
        name="classify",
        template=(
            "System: You are a strict classifier.\n"
            "Task: Classify the input into one label from: {labels}.\n"
            "Rules:\n"
            "- Output JSON only: {{\"label\": \"...\", \"confidence\": 0-1}}\n"
            "- If unsure, choose the closest label and set confidence < 0.6\n"
            "Input:\n"
            "\"\"\"\n{input}\n\"\"\"\n"
        ),
        input_vars=["labels", "input"],
    ),
    "extract": PromptTemplate(
        name="extract",
        template=(
            "System: Extract structured fields from the input.\n"
            "Output JSON schema:\n"
            "{{\n"
            "  \"items\": [{{\"type\": \"\", \"value\": \"\"}}]\n"
            "}}\n"
            "Input:\n"
            "\"\"\"\n{input}\n\"\"\"\n"
        ),
        input_vars=["input"],
    ),
    "summarize": PromptTemplate(
        name="summarize",
        template=(
            "System: Summarize for {audience}.\n"
            "Constraints:\n"
            "- Max 5 bullets\n"
            "- Keep facts only, no speculation\n"
            "Input:\n"
            "\"\"\"\n{input}\n\"\"\"\n"
        ),
        input_vars=["audience", "input"],
    ),
    "plan": PromptTemplate(
        name="plan",
        template=(
            "System: You are a planner.\n"
            "Return JSON:\n"
            "{{\"goal\": \"...\", \"steps\": [{{\"id\": 1, \"task\": \"...\", \"needs_tool\": true}}]}}\n"
            "Input:\n"
            "\"\"\"\n{input}\n\"\"\"\n"
        ),
        input_vars=["input"],
    ),
}


def get_template(name: str) -> PromptTemplate:
    if name not in BUILTIN_TEMPLATES:
        raise KeyError(f"Unknown template: {name}")
    return BUILTIN_TEMPLATES[name]
