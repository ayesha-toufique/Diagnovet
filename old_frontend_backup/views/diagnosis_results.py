"""Page 5: Diagnosis Results View for Diagnovet matching diagnovet.html."""

import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.cards import render_demo_badge
from components.charts import render_confidence_bar_chart
from components.theme import render_html
from services.mock_repository import DiagnovetRepository


def render_diagnosis_results_view(repo: DiagnovetRepository):
    """Renders the diagnosis results interface matching diagnovet.html."""
    render_header(
        title="Diagnosis Results",
        subtitle="Ranked condition concordance based on observed symptoms.",
        show_back=True,
    )

    # Mandatory Demonstration Warning Badge
    render_demo_badge("DEMO RESULT — NOT A REAL VETERINARY DIAGNOSIS")

    pet_ctx = st.session_state.get("selected_pet", repo.get_all_pets()[0])
    diag_data = repo.get_diagnosis(consultation_context=pet_ctx)

    # Metadata Strip
    render_html(f"""
        <div class="card" style="padding: 14px 20px; margin-bottom: 20px;">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
              <span class="m" style="font-size: 11px; text-transform: uppercase; font-weight: 700;">Consultation</span>
              <h3 style="margin: 2px 0 0 0; font-size: 18px;">{diag_data['consultation_id']}</h3>
            </div>
            <div style="display: flex; gap: 16px; font-size: 13.5px;">
              <div><span class="m">Patient:</span> <b>{diag_data['pet_name']} ({diag_data['species']})</b></div>
              <div><span class="m">Category:</span> <b>{diag_data['category']}</b></div>
              <div><span class="m">Date:</span> <b>{diag_data['created_at'].split()[0]}</b></div>
            </div>
          </div>
        </div>
        """)

    # Plotly Overview
    conditions = [c["condition"] for c in diag_data["top_conditions"]]
    confidences = [c["confidence"] for c in diag_data["top_conditions"]]

    c_chart, c_top = st.columns([3, 2])
    with c_chart:
        render_confidence_bar_chart(
            conditions, confidences, title="Concordance Match (%)"
        )

    with c_top:
        top_cond = diag_data["top_conditions"][0]
        render_html(f"""
            <div class="card" style="height: 100%; border-color: var(--a);">
              <span class="badge blu" style="margin-bottom: 8px;">Top Match</span>
              <h3 style="margin: 0 0 6px 0; font-size: 18px;">{top_cond['condition']}</h3>
              <p class="m" style="margin: 0 0 8px 0; font-size: 13px;">Concordance Confidence: <b>{top_cond['confidence']}%</b></p>
              <div class="bar"><i style="width: {top_cond['confidence']}%;"></i></div>
              <p class="m" style="margin: 8px 0 0 0; font-size: 12.5px;">{top_cond['explanation']}</p>
            </div>
            """)

    # Details Expanders matching diagnovet.html
    render_html('<div class="sec">Candidate Conditions & Evidence</div>')
    for idx, c in enumerate(diag_data["top_conditions"]):
        with st.expander(
            f"{c['condition']} — {c['confidence']}% Match ({c['severity']} Severity)",
            expanded=(idx == 0),
        ):
            render_html(f"""
                <div class="bar"><i style="width: {c['confidence']}%;"></i></div>
                <p class="m" style="line-height: 1.6;">
                  <b>Supporting:</b> {', '.join(c['supporting_symptoms'])}.<br>
                  <b>Unconfirmed:</b> {', '.join(c['missing_symptoms'])}.<br>
                  <b>Next Steps:</b> {c['next_steps']}
                </p>
                """)

    render_html('<div style="height: 20px;"></div>')
    act_c1, act_c2 = st.columns(2)
    with act_c1:
        if st.button(
            "⚖️ Proceed to Decision Making & Explanation",
            key="res_to_dec",
            use_container_width=True,
        ):
            st.session_state["page"] = "Decision Making"
            st.rerun()
    with act_c2:
        if st.button(
            "📊 View Full Decision Support System Report",
            key="res_to_dss",
            use_container_width=True,
        ):
            st.session_state["page"] = "Decision Support System"
            st.rerun()

    render_footer()
