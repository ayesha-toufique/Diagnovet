"""Test startup and imports for Diagnovet."""
import importlib
from streamlit.testing.v1 import AppTest


def test_core_imports():
    """Verify that all core modules and views can be imported without error."""
    modules = [
        "app",
        "components.layout",
        "components.widgets",
        "data.question_bank",
        "services.mock_repository",
        "views.home",
        "views.pet_information",
        "views.assessment",
        "views.review",
        "views.conditions",
        "views.care_guidance",
        "views.decision_support",
        "views.summary",
        "views.safety",
    ]
    for mod in modules:
        m = importlib.import_module(mod)
        assert m is not None


def test_app_startup_initial_state():
    """Verify that app launches in headless AppTest and establishes home page state."""
    at = AppTest.from_file("D:/Diagnovet/app.py").run()
    assert not at.exception
    assert at.session_state["page"] == "home"
    assert at.session_state["theme"] in ["lagoon", "aurora"]
    assert at.session_state["qs"] == 2
    assert at.session_state["qdone"] == 0
    assert at.session_state["sub"] == 0
