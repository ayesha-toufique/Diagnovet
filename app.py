"""Diagnovet — Smart Pet Health Diagnosis & Decision Support System.

Main application entrypoint and clean routing layer. Phase 1: Complete Frontend Architecture.
"""
import utils.clients
import utils.http_session
import utils.transport
import utils.session
import streamlit as st

# Streamlit Page Configuration - Must be very first Streamlit call
st.set_page_config(
    page_title="Diagnovet — Smart Pet Health DSS",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import layout components
from components.layout import init_session, render_top_bar, render_sidebar, render_footer

# View Imports (matching exact reference IDs)
from views.home import render_home_view
from views.pet_information import render_pet_information_view
from views.assessment import render_assessment_view
from views.review import render_review_view
from views.conditions import render_conditions_view
from views.care_guidance import render_care_guidance_view
from views.decision_support import render_decision_support_view
from views.summary import render_summary_view
from views.safety import render_safety_view


def main():
    # Initialize session state (creates keys if missing)
    init_session()

    # Render top bar and sidebar
    render_top_bar()
    render_sidebar()

    # Route based on session_state['page']
    page = st.session_state.get("page", "home")
    view_map = {
        "home": render_home_view,
        "pet": render_pet_information_view,
        "q": render_assessment_view,
        "review": render_review_view,
        "cond": render_conditions_view,
        "care": render_care_guidance_view,
        "support": render_decision_support_view,
        "summary": render_summary_view,
        "safety": render_safety_view,
    }
    view_func = view_map.get(page, render_home_view)
    view_func()

    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
