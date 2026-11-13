"""Care Guidance view matching design_reference/diagnovet_flow.html."""
import html
import streamlit as st
from data.question_bank import DECISIONS
from services.mock_repository import calculate_results
from components.widgets import render_head, render_demo_badge, render_html
from components.layout import navigate_to, navigate_back


def render_care_guidance_view():
    """Renders Care Guidance page."""
    render_head("Care Guidance", "What we suggest you do next.")
    render_demo_badge()

    r = calculate_results(st.session_state)
    d = r["decision"]
    d_idx = r["decision_index"]
    sev = st.session_state.get("sev", "")
    dur = st.session_state.get("dur", "")
    frq = st.session_state.get("frq", "")
    syms = st.session_state.get("syms", [])
    guidance = r.get("guidance", {})

    # 4 outcome cards
    cards_html = []
    for i, dec in enumerate(DECISIONS):
        is_sel = i == d_idx
        card_cls = "card sel" if is_sel else "card"
        style_attr = "" if is_sel else 'style="opacity:.55"'
        cards_html.append(
            f'<div class="{card_cls}" {style_attr}>'
            f'<div class="ico">{dec["icon"]}</div>'
            f'<h3>{html.escape(dec["name"])}</h3>'
            f'<span class="badge {dec["tone"]}">{html.escape(dec["level"])}</span>'
            f'</div>'
        )

    render_html(f'<div class="grid">{"".join(cards_html)}</div>')

    # Active decision summary card
    render_html(
        f'<div class="card sel">'
        f'<h3>{d["icon"]} {html.escape(d["name"])}</h3>'
        f'<p class="m">{html.escape(d["text"])}</p>'
        f'</div><br>'
    )

    # Why this was suggested
    if r["emergency"]:
        why_text = f"You reported an emergency sign. Main signs: {', '.join(syms)}."
    else:
        why_text = f"You reported {sev.lower()} signs lasting {dur.lower()}, happening {frq.lower()}. Main signs: {', '.join(syms)}."

    render_html(
        f'<details open>'
        f'<summary>Why this was suggested</summary>'
        f'<p class="m" style="margin-top:8px">{html.escape(why_text)}</p>'
        f'</details>'
    )

    # What to do next
    steps_html = "<br>".join([f"• {html.escape(s)}" for s in d["steps"]])
    render_html(
        f'<details open>'
        f'<summary>What to do next</summary>'
        f'<p class="m" style="margin-top:8px">{steps_html}</p>'
        f'</details>'
    )

    # Unsafe actions to avoid
    if guidance and "unsafe_actions" in guidance:
        unsafe_html = "<br>".join([f"• {html.escape(a)}" for a in guidance["unsafe_actions"]])
        render_html(
            f'<details>'
            f'<summary>Critical precautions & actions to avoid</summary>'
            f'<p class="m" style="margin-top:8px; color:#E5484D !important;">{unsafe_html}</p>'
            f'</details>'
        )

    # Veterinary preparation checklist
    if guidance and "preparation_checklist" in guidance:
        prep_html = "<br>".join([f"• {html.escape(p)}" for p in guidance["preparation_checklist"]])
        render_html(
            f'<details>'
            f'<summary>What to prepare for the veterinary clinic</summary>'
            f'<p class="m" style="margin-top:8px">{prep_html}</p>'
            f'</details>'
        )

    # Navigation buttons
    st.markdown('<div class="nav2">', unsafe_allow_html=True)
    c_b, _, c_next = st.columns([2, 5, 3])
    with c_b:
        if st.button("← Back", key="care_back_btn", type="secondary", use_container_width=True):
            navigate_back()
    with c_next:
        if st.button("Compare options →", key="care_next_btn", use_container_width=True):
            navigate_to("support")
    st.markdown('</div>', unsafe_allow_html=True)
