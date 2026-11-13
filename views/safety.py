"""Safety & Disclaimer view matching design_reference/diagnovet_flow.html."""
import streamlit as st
from components.widgets import render_head


def render_safety_view():
    """Renders Safety & Disclaimer page."""
    render_head("Safety & Disclaimer")

    items = [
        "Results are possible conditions, not confirmed diagnoses.",
        "Emergency signs need immediate professional help.",
        "No medicines, doses or home remedies are given.",
        "Your answers are not saved after the assessment.",
    ]

    cards_html = [
        f'<div class="card" style="margin-top:12px"><p>{item}</p></div>'
        for item in items
    ]

    st.markdown("".join(cards_html), unsafe_allow_html=True)
