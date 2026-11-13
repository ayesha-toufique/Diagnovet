"""Test session reset, assessment restart, and theme preservation."""
from components.layout import reset_assessment


def test_reset_assessment_logic_preserves_theme():
    """Verify reset_assessment clears all clinical state while keeping theme."""
    import streamlit as st

    # Simulate dirty session state
    st.session_state["page"] = "summary"
    st.session_state["theme"] = "aurora"
    st.session_state["sp"] = "Cat"
    st.session_state["breed"] = "Siamese"
    st.session_state["age"] = "2"
    st.session_state["gen"] = "Male"
    st.session_state["wt"] = "4.2"
    st.session_state["bg"] = "None"
    st.session_state["syms"] = ["Sneezing"]
    st.session_state["ans"] = {"Sneezing|0": "Yes"}
    st.session_state["dur"] = "1–3 days"
    st.session_state["sev"] = "Mild"
    st.session_state["frq"] = "Sometimes"
    st.session_state["em"] = {0: "No", 1: "No", 2: "No"}
    st.session_state["qs"] = 5
    st.session_state["qdone"] = 1
    st.session_state["sub"] = 1
    st.session_state["errors"] = {"q": "old err"}

    reset_assessment()

    # Verify all clinical data reset
    assert st.session_state["page"] == "home"
    assert st.session_state["sp"] == ""
    assert st.session_state["breed"] == ""
    assert st.session_state["age"] == ""
    assert st.session_state["gen"] == ""
    assert st.session_state["wt"] == ""
    assert st.session_state["bg"] == ""
    assert st.session_state["syms"] == []
    assert st.session_state["ans"] == {}
    assert st.session_state["dur"] == ""
    assert st.session_state["sev"] == ""
    assert st.session_state["frq"] == ""
    assert st.session_state["em"] == {}
    assert st.session_state["qs"] == 2
    assert st.session_state["qdone"] == 0
    assert st.session_state["sub"] == 0
    assert st.session_state["errors"] == {}

    # Verify theme was preserved
    assert st.session_state["theme"] == "aurora"
