"""Final Assessment Summary view matching design_reference/diagnovet_flow.html."""
import html
import streamlit as st
from services.mock_repository import calculate_results
from components.widgets import render_head, render_kv, render_html
from components.layout import reset_assessment, show_confirm_dialog


def render_summary_view():
    """Renders Final Assessment Summary page."""
    render_head("Final Assessment Summary", "For this session only.")

    r = calculate_results(st.session_state)
    d = r["decision"]
    sp = st.session_state.get("sp", "")
    breed = st.session_state.get("breed", "")
    gen = st.session_state.get("gen", "")
    age = st.session_state.get("age", "")

    # 1. Pet Card
    render_html(
        f"""
        <div class="card">
          <h3>Pet</h3>
          {render_kv("Species · Breed", f"{html.escape(str(sp))} · {html.escape(str(breed))}")}
          {render_kv("Gender · Age", f"{html.escape(str(gen))} · {html.escape(str(age))} yrs")}
        </div>
        <br>
        """
    )

    # 2. Signs and answers Card
    signs_and_ans = "; ".join(r["supporting"])
    render_html(
        f"""
        <div class="card">
          <h3>Signs and answers</h3>
          <p class="m">{html.escape(signs_and_ans)}</p>
        </div>
        <br>
        """
    )

    # 3. Possible conditions Card
    conditions_str = " · ".join(r["conditions"])
    render_html(
        f"""
        <div class="card">
          <h3>Possible conditions</h3>
          <p class="m">{html.escape(conditions_str)}</p>
        </div>
        <br>
        """
    )

    # 4. Selected Decision Card
    render_html(
        f"""
        <div class="card sel">
          <h3>{d['icon']} {html.escape(d['name'])}</h3>
          <p class="m">{html.escape(d['text'])}</p>
        </div>
        """
    )

    # 5. Alert
    render_html(
        '<div class="alert">⚠️ These are possible conditions, not a diagnosis. Do not give medicines without a vet’s advice.</div>'
    )

    # 6. Action buttons with confirmations
    st.markdown('<div class="nav2">', unsafe_allow_html=True)
    c_end, c_new = st.columns(2)

    with c_end:
        if st.button("End assessment", key="sum_end_btn", type="secondary", use_container_width=True):
            def do_end():
                reset_assessment()
                st.session_state["page"] = "home"
                st.toast("Assessment ended")
                st.rerun()

            show_confirm_dialog(
                "End this assessment? All entered information will be cleared.",
                do_end,
            )

    with c_new:
        if st.button("Start new assessment", key="sum_start_new_btn", use_container_width=True):
            def do_new():
                reset_assessment()
                st.session_state["page"] = "pet"
                st.rerun()

            show_confirm_dialog(
                "Start a new assessment? The current one will be cleared.",
                do_new,
            )

    st.markdown('</div>', unsafe_allow_html=True)
