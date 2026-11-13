"""Regression and unit tests for HTML rendering without Markdown code-block escaping."""
import html
import textwrap
from unittest.mock import patch
import pytest

from components.widgets import render_html
from views.care_guidance import render_care_guidance_view
from views.decision_support import render_decision_support_view


def test_render_html_strips_indentation_completely():
    """Verify render_html removes 4+ space leading indentation from all lines."""
    captured = []

    def mock_markdown(content, unsafe_allow_html=False):
        assert unsafe_allow_html is True
        captured.append(content)

    test_input = """
        <div class="grid">
            <div class="card">
              <h3>Title</h3>
            </div>
        </div>
    """
    with patch("streamlit.markdown", side_effect=mock_markdown):
        render_html(test_input)

    assert len(captured) == 1
    rendered = captured[0]
    # No line should begin with 4 spaces (which triggers Markdown code block)
    for line in rendered.splitlines():
        assert not line.startswith("    "), f"Indented line found: {repr(line)}"
    assert rendered.startswith('<div class="grid">')
    assert rendered.endswith("</div>")


def test_render_html_preserves_html_tags_without_escaping():
    """Verify render_html does not escape structural HTML tags into &lt; or &gt;."""
    captured = []

    def mock_markdown(content, unsafe_allow_html=False):
        captured.append(content)

    test_input = '<div class="card"><p class="m">Hello</p></div>'
    with patch("streamlit.markdown", side_effect=mock_markdown):
        render_html(test_input)

    assert len(captured) == 1
    assert "<div class=\"card\">" in captured[0]
    assert "&lt;div" not in captured[0]


def test_dynamic_content_is_escaped_while_tags_remain_raw():
    """Verify dynamic content is sanitized with html.escape without breaking HTML tags."""
    user_malicious_input = '<script>alert("xss")</script> & "quotes"'
    escaped = html.escape(user_malicious_input)

    constructed_html = f'<p class="m">{escaped}</p>'
    captured = []

    with patch("streamlit.markdown", side_effect=lambda c, unsafe_allow_html=False: captured.append(c)):
        render_html(constructed_html)

    assert '<p class="m">' in captured[0]
    assert "&lt;script&gt;" in captured[0]
    assert "<script>" not in captured[0]


def test_care_guidance_and_decision_support_views_render_without_code_blocks():
    """Verify Care Guidance and Decision Support views generate zero 4-space indented lines."""
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file("D:/Diagnovet/app.py", default_timeout=15)
    at.run()
    at.session_state["sp"] = "Dog"
    at.session_state["breed"] = "Labrador"
    at.session_state["gen"] = "Male"
    at.session_state["age"] = "3"
    at.session_state["wt"] = "20"
    at.session_state["bg"] = ""
    at.session_state["syms"] = ["Vomiting", "Diarrhoea"]
    at.session_state["ans"] = {"Vomiting|0": "Yes"}
    at.session_state["dur"] = "1-3 days"
    at.session_state["sev"] = "Moderate"
    at.session_state["frq"] = "Often"
    at.session_state["em"] = {0: "No", 1: "No", 2: "No"}
    at.session_state["qdone"] = 1
    at.session_state["sub"] = 1

    # Test Care Guidance
    at.session_state["page"] = "care"
    at.run()
    # Check all markdown outputs on the page (excluding header <style> block)
    for m in at.markdown:
        if m.value.strip().startswith("<style>"):
            continue
        for line in m.value.splitlines():
            assert not line.startswith("    "), f"Code block indentation detected on Care page: {repr(line)}"

    # Test Decision Support
    at.session_state["page"] = "support"
    at.run()
    for m in at.markdown:
        if m.value.strip().startswith("<style>"):
            continue
        for line in m.value.splitlines():
            assert not line.startswith("    "), f"Code block indentation detected on Support page: {repr(line)}"
