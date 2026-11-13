"""Possible Conditions view matching design_reference/diagnovet_flow.html."""
import html
import streamlit as st
from services.mock_repository import calculate_results
from components.widgets import render_head, render_demo_badge, render_html
from components.layout import navigate_to, navigate_back


def render_conditions_view():
    """Renders Possible Conditions page."""
    render_head("Possible Health Conditions", "These are possibilities, not a diagnosis.")
    render_demo_badge()

    r = calculate_results(st.session_state)

    if r["emergency"]:
        st.markdown(
            '<div class="alert">🚨 Emergency signs were reported. Please contact a vet immediately.</div>',
            unsafe_allow_html=True,
        )

    for i, c_name in enumerate(r["conditions"]):
        badge_cls = "amb" if i == 0 else "grn"
        badge_lbl = "Most likely" if i == 0 else "Possible"
        is_open = "open" if i == 0 else ""
        pct = r["scores"][i]

        matches_str = "; ".join(r["supporting"][:3]) + "."
        if r["missing"]:
            not_conf_str = "; ".join(r["missing"][:2])
        else:
            not_conf_str = "Signs only a vet can check."

        # Verified Source Citations
        sources_html = ""
        if "matches" in r and i < len(r["matches"]):
            match_cond = r["matches"][i].condition
            if match_cond.sources:
                src_items = []
                for s in match_cond.sources:
                    claims = "; ".join(s.claims_supported[:2]) if s.claims_supported else ""
                    src_items.append(
                        f'• <b>{html.escape(s.organization)}</b>: '
                        f'<a href="{html.escape(s.url)}" target="_blank" rel="noopener noreferrer" style="color: var(--a); text-decoration: underline;">{html.escape(s.title)}</a> '
                        f'({html.escape(s.publication_date or "Verified")})<br>'
                        f'<span style="font-size:12px; opacity:0.85;">{html.escape(claims)}</span>'
                    )
                sources_html = (
                    f'<div style="margin-top:8px; padding-top:6px; border-top: 1px dashed var(--line); font-size:12.5px;">'
                    f'<b>Medical Sources:</b><br>{"<br>".join(src_items)}</div>'
                )

        render_html(
            f"""
            <details {is_open}>
              <summary>
                {html.escape(c_name)} <span class="badge {badge_cls}" style="float:right">{badge_lbl}</span>
              </summary>
              <div class="bar"><i style="width:{pct}%"></i></div>
              <p class="m">
                <b>Matches:</b> {html.escape(matches_str)}<br>
                <b>Not confirmed:</b> {html.escape(not_conf_str)}
              </p>
              {sources_html}
            </details>
            """
        )

    st.markdown('<p class="m">Only a qualified veterinarian can diagnose your pet.</p>', unsafe_allow_html=True)

    # Navigation buttons
    st.markdown('<div class="nav2">', unsafe_allow_html=True)
    c_b, _, c_next = st.columns([2, 5, 3])
    with c_b:
        if st.button("← Back", key="cond_back_btn", type="secondary", use_container_width=True):
            navigate_back()
    with c_next:
        if st.button("See care guidance →", key="cond_next_btn", use_container_width=True):
            navigate_to("care")
    st.markdown('</div>', unsafe_allow_html=True)
