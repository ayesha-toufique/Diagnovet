"""Page 6: Decision Making & Explanation Facility View for Diagnovet matching diagnovet.html."""

import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.cards import render_demo_badge, render_decision_card
from components.theme import render_html
from services.mock_repository import DiagnovetRepository


def render_decision_making_view(repo: DiagnovetRepository):
    """Renders the 4-outcome decision framework and academic explanation facility matching diagnovet.html."""
    render_header(
        title="Decision Making",
        subtitle="Veterinary action determination, clinical rationale, and explanation facility.",
        show_back=True,
    )

    # Mandatory Demo Badge matching diagnovet.html
    render_demo_badge("DEMO DECISION — BACKEND DECISION ENGINE NOT CONNECTED")

    pet_ctx = st.session_state.get("selected_pet", repo.get_all_pets()[0])
    dec_data = repo.get_decision(consultation_context=pet_ctx)

    # Four Outcomes Grid matching diagnovet.html
    render_html(
        '<div class="sec" style="margin-top: 0;">Four Veterinary Urgency Outcomes</div>'
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_decision_card(
            outcome_title="Get Help Now",
            priority_level="Critical",
            description="Emergency signs detected requiring immediate transport.",
            is_active=(dec_data["decision"] == "Get Help Now"),
        )
    with c2:
        render_decision_card(
            outcome_title="Visit Vet Today",
            priority_level="High",
            description="Concerning symptoms need urgent same-day review.",
            is_active=(dec_data["decision"] == "Visit Vet Today"),
        )
    with c3:
        render_decision_card(
            outcome_title="Book a Vet Visit",
            priority_level="Medium",
            description="Non-urgent but persistent symptoms needing appointment.",
            is_active=(dec_data["decision"] == "Book a Vet Visit"),
        )
    with c4:
        render_decision_card(
            outcome_title="Home Care & Monitor",
            priority_level="Low",
            description="Mild signs; observe closely and re-check if worsening.",
            is_active=(dec_data["decision"] == "Home Care & Monitor"),
        )

    # Active Decision Card matching diagnovet.html
    render_html(f"""
        <div class="card" style="border-left: 6px solid var(--amb); margin-top: 14px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <h3 style="margin: 0; font-size: 20px;">🏥 {dec_data['decision']}</h3>
            <span class="badge amb">Priority: {dec_data['priority']}</span>
          </div>
          <p class="m" style="margin: 0; font-size: 14px;">
            <b>Primary Rationale:</b> {dec_data['why_selected']}
          </p>
        </div>
        """)

    # Academic Explanation Facility Details matching diagnovet.html
    render_html('<div class="sec">Academic Explanation Facility</div>')
    explanation_sections = [
        ("Why this decision was selected", dec_data["why_selected"]),
        (
            "Symptoms influencing the decision",
            ", ".join(dec_data["symptoms_influencing"]),
        ),
        ("Severity & duration considerations", dec_data["severity_duration"]),
        ("Risk factors identified", ", ".join(dec_data["risk_factors"])),
        ("Rules fired (Working Memory)", "<br>".join(dec_data["rules_influenced"])),
        ("Emergency override check", dec_data["emergency_override"]),
        (
            "Alternatives considered & exclusion reasoning",
            "<br>".join(
                [
                    f"&bull; <b>{a['decision']}:</b> {a['why_not']}"
                    for a in dec_data["alternatives_considered"]
                ]
            ),
        ),
        (
            "Recommended next steps",
            "<br>".join(
                [
                    f"{i + 1}. {act}"
                    for i, act in enumerate(dec_data["recommended_actions"])
                ]
            ),
        ),
    ]

    for title, content in explanation_sections:
        with st.expander(title):
            render_html(
                f'<p class="m" style="margin-top: 4px; line-height: 1.6;">{content}</p>'
            )

    render_html('<div style="height: 18px;"></div>')
    c_btn1, c_btn2 = st.columns([1, 1])
    with c_btn2:
        if st.button(
            "📊 Open Decision Support System (DSS) Report →",
            key="dec_to_dss",
            use_container_width=True,
        ):
            st.session_state["page"] = "Decision Support System"
            st.rerun()

    render_footer()
