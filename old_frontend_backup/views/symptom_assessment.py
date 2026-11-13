"""Page 4: Symptom Assessment Interactive Interface for Diagnovet matching diagnovet.html."""

import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.cards import render_emergency_alert, render_pet_card
from components.theme import render_html
from services.mock_repository import DiagnovetRepository


def render_symptom_assessment_view(repo: DiagnovetRepository):
    """Renders the comprehensive symptom assessment matching diagnovet.html."""
    render_header(
        title="Symptom Assessment",
        subtitle="Detailed clinical observations, duration, severity, and risk factors.",
        show_back=True,
    )

    pets = repo.get_all_pets()
    active_pet = st.session_state.get("selected_pet", pets[0] if pets else None)
    categories = repo.get_health_categories()

    col_pet, col_cat = st.columns([1, 1])
    with col_pet:
        render_html('<div class="sec" style="margin-top: 0;">Patient</div>')
        render_pet_card(active_pet, is_selected=True)

    with col_cat:
        render_html('<div class="sec" style="margin-top: 0;">Category</div>')
        cat_names = [c["name"] for c in categories]
        chosen_cat_name = st.selectbox(
            "Health System Assessment", options=cat_names, index=0
        )
        selected_cat = next(c for c in categories if c["name"] == chosen_cat_name)

        render_html(f"""
            <div class="card" style="padding: 14px 18px; margin-bottom: 12px;">
              <div style="display: flex; align-items: center; gap: 12px;">
                <div class="ico" style="margin: 0; width: 40px; height: 40px; font-size: 18px;">{selected_cat['icon']}</div>
                <div>
                  <h3 style="margin: 0 0 2px 0; font-size: 16px;">{selected_cat['name']}</h3>
                  <p class="m" style="margin: 0; font-size: 12.5px;">{selected_cat['desc']}</p>
                </div>
              </div>
            </div>
            """)

    # Symptom Parameters Form matching diagnovet.html
    render_html('<div class="sec">Clinical Parameters & Triage</div>')
    with st.form("assessment_form"):
        c1, c2 = st.columns(2)
        with c1:
            duration = st.selectbox(
                "Duration",
                options=[
                    "Less than 1 day",
                    "1–3 days",
                    "More than 3 days",
                    "Recurring over weeks",
                ],
                index=1,
            )
            severity = st.radio(
                "Severity",
                options=["Mild", "Moderate", "Severe"],
                index=1,
                horizontal=True,
            )

        with c2:
            appetite = st.selectbox(
                "Appetite & Drinking",
                ["Normal", "Reduced appetite", "Complete refusal of food/water"],
            )
            energy = st.selectbox(
                "Lethargy & Demeanor",
                [
                    "Alert & Active",
                    "Mildly lethargic",
                    "Severe weakness / Reluctant to move",
                ],
            )

        st.markdown("**Risk Factors** (Select any that apply):")
        r_cols = st.columns(4)
        with r_cols[0]:
            rf_senior = st.checkbox("Senior pet")
        with r_cols[1]:
            rf_diet = st.checkbox("Recent diet change")
        with r_cols[2]:
            rf_vax = st.checkbox("Not vaccinated")
        with r_cols[3]:
            rf_chronic = st.checkbox("Chronic illness")

        st.markdown("**Emergency Warning Signs** (Immediate veterinary care required):")
        e_cols = st.columns(4)
        with e_cols[0]:
            em_collapse = st.checkbox("Collapse / Syncope")
        with e_cols[1]:
            em_seizure = st.checkbox("Active Seizure")
        with e_cols[2]:
            em_gums = st.checkbox("Pale or blue gums")
        with e_cols[3]:
            em_poison = st.checkbox("Suspected poison")

        notes = st.text_area(
            "Additional Observations",
            placeholder="Note any specific behaviors, stool consistency, or unusual events...",
        )

        submit_btn = st.form_submit_button("Run Assessment & View Possible Conditions")
        if submit_btn:
            has_em = any([em_collapse, em_seizure, em_gums, em_poison])
            risk_factors = []
            if rf_senior:
                risk_factors.append("Senior pet")
            if rf_diet:
                risk_factors.append("Recent diet change")
            if rf_vax:
                risk_factors.append("Not vaccinated")
            if rf_chronic:
                risk_factors.append("Chronic illness")

            st.session_state["assessment_data"] = {
                "duration": duration,
                "severity": severity,
                "appetite": appetite,
                "energy": energy,
                "risk_factors": risk_factors,
                "has_emergency": has_em,
                "notes": notes,
            }
            st.session_state["page"] = "Diagnosis Results"
            st.rerun()

    # Emergency check display if any emergency sign was flagged
    assess_data = st.session_state.get("assessment_data", {})
    if assess_data.get("has_emergency"):
        render_emergency_alert(
            "Emergency warning sign selected! Collapse, seizures, cyanotic gums, or toxin ingestion require immediate veterinary hospital transport.",
            title="CRITICAL WARNING:",
        )

    render_footer()
