import pytest

from src.genai.prompts import get_template, PromptTemplate


def test_prompt_render_classify():
    template = get_template("classify")
    rendered = template.render(labels="billing,support", input="Please resend my invoice")
    assert "billing,support" in rendered
    assert "Please resend my invoice" in rendered


def test_prompt_missing_var():
    template = PromptTemplate(name="t", template="Hello {name}", input_vars=["name"])
    with pytest.raises(ValueError):
        template.render()
