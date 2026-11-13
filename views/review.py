"""Review Answers view (Step 6 of 6) matching design_reference/diagnovet_flow.html."""
import html
import streamlit as st
from data.question_bank import FOLLOW_UPS
from components.widgets import render_head, render_prog, render_kv, render_html
from components.layout import navigate_to


def render_review_view():
    """Renders Step 6: Review Answers."""
    render_head("Review Your Answers", "Check everything, or tap Edit to fix an answer.")
    render_prog(6)

    sp = st.session_state.get("sp", "")
    breed = st.session_state.get("breed", "")
    gen = st.session_state.get("gen", "")
    age = st.session_state.get("age", "")
    syms = st.session_state.get("syms", [])
    ans = st.session_state.get("ans", {})
    dur = st.session_state.get("dur", "")
    sev = st.session_state.get("sev", "")
    frq = st.session_state.get("frq", "")

    # Card 1: Pet
    with st.container(border=True):
        c_h1, c_ed1 = st.columns([5, 1])
        with c_h1:
            render_html('<h3>Pet</h3>')
        with c_ed1:
            if st.button("Edit", key="rev_edit_pet", type="secondary"):
                navigate_to("pet")
        render_html(
            f"""
            {render_kv("Species", html.escape(str(sp)))}
            {render_kv("Breed", html.escape(str(breed)))}
            {render_kv("Gender · Age", f"{html.escape(str(gen))} · {html.escape(str(age))} yrs")}
            """
        )

    render_html('<div style="height: 12px;"></div>')

    # Card 2: Signs noticed
    with st.container(border=True):
        c_h2, c_ed2 = st.columns([5, 1])
        with c_h2:
            render_html('<h3>Signs noticed</h3>')
        with c_ed2:
            if st.button("Edit", key="rev_edit_signs", type="secondary"):
                st.session_state["qs"] = 2
                navigate_to("q")
        render_html(
            f"""
            <p class="m">{html.escape(", ".join(syms))}</p>
            """
        )

    render_html('<div style="height: 12px;"></div>')

    # Card 3: Follow-up answers
    with st.container(border=True):
        c_h3, c_ed3 = st.columns([5, 1])
        with c_h3:
            render_html('<h3>Follow-up answers</h3>')
        with c_ed3:
            if st.button("Edit", key="rev_edit_fu", type="secondary"):
                st.session_state["qs"] = 3
                navigate_to("q")
        fu_rows = []
        for s in syms:
            for j, q_text in enumerate(FOLLOW_UPS.get(s, [])):
                a_val = ans.get(f"{s}|{j}", "")
                fu_rows.append(render_kv(html.escape(q_text), html.escape(str(a_val))))
        render_html(
            f"""
            {"".join(fu_rows)}
            """
        )

    render_html('<div style="height: 12px;"></div>')

    # Card 4: Timing
    with st.container(border=True):
        c_h4, c_ed4 = st.columns([5, 1])
        with c_h4:
            render_html('<h3>Timing</h3>')
        with c_ed4:
            if st.button("Edit", key="rev_edit_timing", type="secondary"):
                st.session_state["qs"] = 4
                navigate_to("q")
        render_html(
            f"""
            {render_kv("Duration", html.escape(str(dur)))}
            {render_kv("Severity", html.escape(str(sev)))}
            {render_kv("Frequency", html.escape(str(frq)))}
            """
        )

    # Navigation buttons
    render_html('<div class="nav2">')
    c_back, _, c_show = st.columns([2, 4, 4])
    with c_back:
        if st.button("← Previous", key="rev_prev_btn", type="secondary", use_container_width=True):
            st.session_state["qs"] = 5
            navigate_to("q", is_back=True)
    with c_show:
        if st.button("Show possible conditions →", key="rev_show_cond_btn", use_container_width=True):
            st.session_state["sub"] = 1
            navigate_to("cond")
    render_html('</div>')
