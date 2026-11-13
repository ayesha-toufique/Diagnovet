"""Decision Support view matching design_reference/diagnovet_flow.html."""
import html
import streamlit as st
from services.mock_repository import calculate_results
from components.widgets import render_head, render_demo_badge, render_html
from components.layout import navigate_to, navigate_back


def render_decision_support_view():
    """Renders Decision Support page."""
    render_head("Decision Support", "Compare the possibilities in plain language.")
    render_demo_badge()

    r = calculate_results(st.session_state)
    sev = st.session_state.get("sev", "")
    dec = r["decision"]

    # 1. How well each fits
    fit_bars = []
    for c_name, score in zip(r["conditions"], r["scores"]):
        fit_bars.append(
            f'<p class="m">{html.escape(c_name)} — {score}%</p>'
            f'<div class="bar"><i style="width:{score}%"></i></div>'
        )

    render_html(
        f'<div class="card">'
        f'<h3>How well each fits</h3>'
        f'{"".join(fit_bars)}'
        f'</div><br>'
    )

    # 2. Severity and Urgency
    sev_badge_tone = "red" if sev == "Severe" else "amb" if sev == "Moderate" else "grn"
    render_html(
        f'<div class="grid" style="grid-template-columns: 1fr 1fr">'
        f'<div class="card">'
        f'<h3>Severity</h3>'
        f'<span class="badge {sev_badge_tone}">{html.escape(sev)}</span>'
        f'</div>'
        f'<div class="card">'
        f'<h3>Urgency</h3>'
        f'<span class="badge {dec["tone"]}">{html.escape(dec["level"])}</span>'
        f'</div>'
        f'</div>'
    )

    # 3. Possibilities table
    table_rows = []
    for row in r["table_rows"]:
        table_rows.append(
            f'<tr>'
            f'<td style="padding:9px 0;border-top:1px solid var(--line)">{html.escape(str(row["condition"]))}</td>'
            f'<td style="border-top:1px solid var(--line)">{row["fits"]}</td>'
            f'<td style="border-top:1px solid var(--line)">{row["not_confirmed"]}</td>'
            f'</tr>'
        )

    render_html(
        f'<div class="card" style="overflow:auto">'
        f'<table style="width:100%;font-size:13.5px;border-collapse:collapse">'
        f'<tr style="color:var(--muted);text-align:left">'
        f'<th>Possibility</th>'
        f'<th>Fits</th>'
        f'<th>Not confirmed</th>'
        f'</tr>'
        f'{"".join(table_rows)}'
        f'</table>'
        f'</div>'
        f'<p class="m" style="margin-top:12px">Other possibilities stay on the list because some signs are still unconfirmed.</p>'
    )

    # 4. Navigation buttons
    st.markdown('<div class="nav2">', unsafe_allow_html=True)
    c_b, _, c_next = st.columns([2, 5, 3])
    with c_b:
        if st.button("← Back", key="supp_back_btn", type="secondary", use_container_width=True):
            navigate_back()
    with c_next:
        if st.button("Final summary →", key="supp_next_btn", use_container_width=True):
            navigate_to("summary")
    st.markdown('</div>', unsafe_allow_html=True)
