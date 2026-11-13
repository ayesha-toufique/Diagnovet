"""Test symptom selection, dynamic follow-ups, and answer preservation."""
from streamlit.testing.v1 import AppTest
from data.question_bank import SYMPTOMS


def test_species_symptom_lists():
    """Verify Dog and Cat have distinct, designated symptoms in question bank."""
    assert "Coughing" in SYMPTOMS["Dog"]
    assert "Sneezing" in SYMPTOMS["Cat"]
    assert "Limping" in SYMPTOMS["Dog"]
    assert "Hiding more" in SYMPTOMS["Cat"]


def test_symptom_toggling_and_answer_removal():
    """Verify that removing a symptom removes its follow-up answers but preserves others."""
    at = AppTest.from_file("D:/Diagnovet/app.py").run()
    at.session_state["page"] = "q"
    at.session_state["sp"] = "Dog"
    at.session_state["qs"] = 2
    at.session_state["syms"] = ["Vomiting", "Itching"]
    at.session_state["ans"] = {
        "Vomiting|0": "Yes",
        "Vomiting|1": "No",
        "Itching|0": "Yes",
        "Itching|1": "Not Sure",
    }
    at.run()

    # Toggle Vomiting off by clicking its chip
    for b in at.button:
        if b.key == "sym_chip_Vomiting":
            b.click().run()
            break

    assert "Vomiting" not in at.session_state["syms"]
    assert "Itching" in at.session_state["syms"]

    ans = at.session_state["ans"]
    assert "Vomiting|0" not in ans
    assert "Vomiting|1" not in ans
    assert ans["Itching|0"] == "Yes"
    assert ans["Itching|1"] == "Not Sure"


def test_validation_requires_at_least_one_symptom():
    """Verify user cannot advance from Step 2 without selecting a symptom."""
    at = AppTest.from_file("D:/Diagnovet/app.py").run()
    at.session_state["page"] = "q"
    at.session_state["sp"] = "Dog"
    at.session_state["qs"] = 2
    at.session_state["syms"] = []
    at.run()

    for b in at.button:
        if b.key == "q_next_btn":
            b.click().run()
            break

    err = at.session_state.get("errors", {}).get("q", "")
    assert err == "Choose at least one sign to continue."
    assert at.session_state["qs"] == 2
