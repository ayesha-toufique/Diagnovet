"""Test validation logic on the Pet Information view."""
from streamlit.testing.v1 import AppTest


def test_pet_information_empty_submission():
    """Verify that submitting an empty Pet Information form sets validation errors."""
    at = AppTest.from_file("D:/Diagnovet/app.py").run()
    # Go to pet page
    at.session_state["page"] = "pet"
    at.run()

    # Click Next
    for b in at.button:
        if b.key == "pet_next_btn":
            b.click().run()
            break

    errors = at.session_state.get("errors", {})
    assert "sp" in errors
    assert errors["sp"] == "Please choose Dog or Cat."
    assert "breed" in errors
    assert "gen" in errors
    assert "age" in errors
    # Page must stay on pet
    assert at.session_state["page"] == "pet"


def test_pet_information_invalid_age_and_weight():
    """Verify that invalid numeric ranges produce explicit error strings."""
    at = AppTest.from_file("D:/Diagnovet/app.py").run()
    at.session_state["page"] = "pet"
    at.session_state["sp"] = "Cat"
    at.session_state["breed"] = "Persian"
    at.session_state["gen"] = "Female"
    at.session_state["age"] = "45"  # Out of range 0-30
    at.session_state["wt"] = "150"  # Out of range 0.5-90
    at.run()

    for b in at.button:
        if b.key == "pet_next_btn":
            b.click().run()
            break

    errors = at.session_state.get("errors", {})
    assert errors.get("age") == "Enter an age from 0 to 30."
    assert errors.get("wt") == "Enter a weight from 0.5 to 90 kg."
    assert at.session_state["page"] == "pet"


def test_pet_information_valid_submission():
    """Verify that valid inputs clear errors and navigate to assessment step 2."""
    at = AppTest.from_file("D:/Diagnovet/app.py").run()
    at.session_state["page"] = "pet"
    at.session_state["sp"] = "Dog"
    at.session_state["breed"] = "German Shepherd"
    at.session_state["gen"] = "Male"
    at.session_state["age"] = "5"
    at.session_state["wt"] = "32"
    at.run()

    for b in at.button:
        if b.key == "pet_next_btn":
            b.click().run()
            break

    assert not at.session_state.get("errors")
    assert at.session_state["page"] == "q"
    assert at.session_state["qs"] == 2
