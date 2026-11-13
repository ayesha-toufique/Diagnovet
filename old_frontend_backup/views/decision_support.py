"""Page 7: Decision Support System (DSS) Report View for Diagnovet matching diagnovet.html."""

import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.cards import render_demo_badge
from components.charts import render_criteria_comparison_chart
from components.theme import render_html
from services.mock_repository import DiagnovetRepository


def render_decision_support_view(repo: DiagnovetRepository):
    """Renders the comprehensive multi-criteria decision support report matching diagnovet.html."""
    render_header(
        title="Decision Support Report",
        subtitle="Multi-attribute evidence synthesis, condition comparison, and action prioritization.",
        show_back=True,
    )

    # Mandatory Demonstration Warning Badge matching diagnovet.html
    render_demo_badge("DEMONSTRATION DATA ONLY")

    pet_ctx = st.session_state.get("selected_pet", repo.get_all_pets()[0])
    dss_data = repo.get_dss_report(consultation_context=pet_ctx)

    # Top Grid: Condition comparison + Urgency card matching diagnovet.html
    col_comp, col_urg = st.columns([2, 1])

    with col_comp:
        bars_html = "".join(
            [
                f'<p class="m" style="margin-bottom: 2px;">{row["Condition"]} &mdash; <b>{row["Concordance"]}%</b></p>'
                f'<div class="bar"><i style="width: {row["Concordance"]}%;"></i></div>'
                for row in dss_data["condition_comparison"]
            ]
        )
        render_html(f"""
            <div class="card" style="height: 100%;">
              <h3 style="margin-top: 0;">Condition comparison</h3>
              {bars_html}
            </div>
            """)

    with col_urg:
        render_html(f"""
            <div class="card" style="height: 100%;">
              <h3 style="margin-top: 0;">Recommended Urgency</h3>
              <div class="ico" style="margin-top: 12px;">🏥</div>
              <b style="font-size: 16px;">{dss_data['recommended_action']}</b>
              <p class="m" style="margin-top: 6px;">{dss_data['primary_rationale']}</p>
            </div>
            """)

    # Table matching diagnovet.html
    render_html('<div class="sec">Comparative Evidence Breakdown</div>')
    table_rows = "".join([f"""
            <tr>
              <td><b>{row['Condition']}</b></td>
              <td>{len(row['Evidence For'].split(','))} identified</td>
              <td>{len(row['Evidence Against'].split(','))} missing</td>
              <td><span class="badge {'amb' if row['Severity'] == 'High' else 'grn'}">{row['Severity']}</span></td>
            </tr>
            """ for row in dss_data["condition_comparison"]])

    render_html(f"""
        <div class="card" style="overflow-x: auto; padding: 14px 18px;">
          <table style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr>
                <th style="padding: 8px 10px; border-bottom: 1px solid var(--line); text-align: left;">Condition</th>
                <th style="padding: 8px 10px; border-bottom: 1px solid var(--line); text-align: left;">Evidence</th>
                <th style="padding: 8px 10px; border-bottom: 1px solid var(--line); text-align: left;">Missing</th>
                <th style="padding: 8px 10px; border-bottom: 1px solid var(--line); text-align: left;">Severity</th>
              </tr>
            </thead>
            <tbody>
              {table_rows}
            </tbody>
          </table>
        </div>
        """)

    # Multi-Criteria Chart
    render_html('<div class="sec">Multi-Criteria Evaluation Matrix</div>')
    render_criteria_comparison_chart(
        dss_data["criteria_weights"],
        title="Decision Criteria Weights vs Evaluated Scores",
    )

    render_html('<div style="height: 18px;"></div>')
    c_hist, c_new = st.columns([1, 1])
    with c_hist:
        if st.button(
            "📜 View Past Consultation History",
            key="dss_view_hist",
            use_container_width=True,
        ):
            st.session_state["page"] = "Consultation History"
            st.rerun()
    with c_new:
        if st.button(
            "Start Consultation →", key="dss_start_new", use_container_width=True
        ):
            st.session_state["consult_step"] = 0
            st.session_state["page"] = "Start Consultation"
            st.rerun()

    render_footer()
