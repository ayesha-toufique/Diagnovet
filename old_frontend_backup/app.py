"""Diagnovet — Smart Pet Health Diagnosis & Decision Support System.

Main application entrypoint and clean routing layer.
Phase 1: Complete Frontend Architecture.
"""

import streamlit as st

# Streamlit Page Configuration - Must be very first Streamlit call
st.set_page_config(
    page_title="Diagnovet — Smart Pet Health DSS",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.theme import inject_custom_styles
from components.sidebar import render_sidebar
from services.mock_repository import DiagnovetRepository

# View Imports
from views.home import render_home_view
from views.pet_profile import render_pet_profile_view
from views.consultation import render_consultation_view
from views.symptom_assessment import render_symptom_assessment_view
from views.diagnosis_results import render_diagnosis_results_view
from views.decision_making import render_decision_making_view
from views.decision_support import render_decision_support_view
from views.consultation_history import render_consultation_history_view
from views.about import render_about_view
from views.safety import render_safety_view


def init_session_state():
    """Initializes global session state attributes."""
    if "repo" not in st.session_state:
        st.session_state["repo"] = DiagnovetRepository()

    if "page" not in st.session_state:
        st.session_state["page"] = "Home Dashboard"

    if "theme" not in st.session_state:
        st.session_state["theme"] = "Lagoon"

    if "selected_pet" not in st.session_state:
        pets = st.session_state["repo"].get_all_pets()
        st.session_state["selected_pet"] = pets[0] if pets else None


def main():
    # Initialize application state
    init_session_state()

    # Inject Lagoon theme & optional Aurora dark mode override
    inject_custom_styles()

    # Render custom navigation sidebar
    render_sidebar()

    # Route Dictionary
    routes = {
        "Home Dashboard": render_home_view,
        "Pet Profile": render_pet_profile_view,
        "Start Consultation": render_consultation_view,
        "Symptom Assessment": render_symptom_assessment_view,
        "Diagnosis Results": render_diagnosis_results_view,
        "Decision Making": render_decision_making_view,
        "Decision Support System": render_decision_support_view,
        "Consultation History": render_consultation_history_view,
        "About Diagnovet": render_about_view,
        "Safety & Disclaimer": render_safety_view,
    }

    current_page = st.session_state.get("page", "Home Dashboard")
    view_func = routes.get(current_page, render_home_view)
    repo = st.session_state["repo"]

    # Render target view
    view_func(repo)


if __name__ == "__main__":
    main()
