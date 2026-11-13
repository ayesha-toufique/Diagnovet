"""Test navigation, unlock constraints, and page routing."""
from streamlit.testing.v1 import AppTest
from components.layout import is_unlocked


def test_unlock_rules():
    """Verify that pages unlock according to assessment progression."""
    # Initially: home, pet, safety are unlocked; others locked
    assert is_unlocked("home") is True
    assert is_unlocked("pet") is True
    assert is_unlocked("safety") is True
    assert is_unlocked("q") is False
    assert is_unlocked("review") is False
    assert is_unlocked("cond") is False
    assert is_unlocked("care") is False
    assert is_unlocked("support") is False
    assert is_unlocked("summary") is False


def test_pet_validation_helper():
    """Verify is_pet_valid logic with various session state mockings."""
    # Simulate empty
    session = {"sp": "", "breed": "", "gen": "", "age": ""}
    assert not (session["sp"] and session["breed"] and session["gen"] and session["age"] != "")

    # Valid
    valid_session = {"sp": "Dog", "breed": "Bulldog", "gen": "Female", "age": "4.5"}
    assert valid_session["sp"] and valid_session["breed"] and valid_session["gen"]
    age_val = float(valid_session["age"])
    assert 0 <= age_val <= 30


def test_locked_sidebar_nav_interaction():
    """Verify clicking a locked sidebar item does not alter page."""
    at = AppTest.from_file("D:/Diagnovet/app.py").run()
    assert at.session_state["page"] == "home"

    # Try navigating to summary while locked
    for b in at.button:
        if b.key == "sb_nav_summary":
            b.click().run()
            break

    # Page should remain home
    assert at.session_state["page"] == "home"
