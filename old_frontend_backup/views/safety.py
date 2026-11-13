"""Page 10: Safety & Clinical Disclaimer View for Diagnovet matching diagnovet.html."""

import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.cards import render_emergency_alert
from components.theme import render_html
from services.mock_repository import DiagnovetRepository


def render_safety_view(repo: DiagnovetRepository):
    """Renders clinical safety mandates, emergency guidelines, and disclaimers matching diagnovet.html."""
    render_header(
        title="Safety & Disclaimer",
        subtitle="Important clinical policies, emergency warning protocols, and user boundaries.",
        show_back=True,
    )

    # Top Emergency Warning Alert matching diagnovet.html
    render_emergency_alert(
        "Diagnovet does not manage active medical emergencies. If your pet is unresponsive, choking, having persistent seizures, or bleeding profusely, seek emergency veterinary hospital care immediately.",
        title="EMERGENCY SAFETY MANDATE:",
    )

    # Core Safety Principles matching diagnovet.html
    safety_cards = [
        (
            "🚫 Not a Replacement for a Veterinarian",
            "Diagnovet does not establish a legally or clinically binding veterinary diagnosis. It is strictly an educational decision-support aid.",
        ),
        (
            "⚠️ Possible Conditions, Not Confirmed Diagnoses",
            "All findings are probabilistic concordance matches based solely on owner-reported observations, subject to physical examination by a licensed veterinarian.",
        ),
        (
            "🚨 Emergency Signs Require Immediate Care",
            "Acute signs such as severe dyspnea, blue/pale gums, collapse, or suspected toxin ingestion require instant emergency clinical intervention.",
        ),
        (
            "💊 No Medication Prescriptions or Dosages",
            "Diagnovet strictly forbids generating drug prescriptions, calculating pharmaceutical dosages, or recommending unverified human home remedies (e.g. acetaminophen is fatal to felines).",
        ),
    ]

    for title, desc in safety_cards:
        render_html(f"""
            <div class="card" style="margin-bottom: 12px;">
              <h3 style="margin: 0 0 4px 0; font-size: 16px;">{title}</h3>
              <p class="m" style="margin: 0; font-size: 13.5px;">{desc}</p>
            </div>
            """)

    render_html('<div class="sec">Critical Red-Flag Clinical Signs</div>')
    signs = repo.get_emergency_signs()
    for s in signs:
        render_html(f"""
            <div style="display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: var(--card); border: 1px solid var(--line); border-left: 4px solid var(--emergency); border-radius: 10px; margin-bottom: 8px; font-size: 13px;">
              <span style="color: var(--emergency); font-weight: 800;">!</span>
              <span>{s}</span>
            </div>
            """)

    render_html('<div style="height: 16px;"></div>')
    agree = st.checkbox(
        "I acknowledge that Diagnovet is an educational decision-support tool and agree to consult a licensed veterinarian for medical concerns."
    )
    if agree:
        st.success(
            "Acknowledgement recorded. Thank you for prioritizing your companion's health and safety."
        )

    render_footer()
