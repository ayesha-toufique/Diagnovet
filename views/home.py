"""Home view matching design_reference/diagnovet_flow.html."""
import streamlit as st
from components.layout import navigate_to
from components.widgets import render_html


def render_home_view():
    """Renders Home view with exact text, cards, and navigation."""
    # 1. Hero
    render_html(
        """
        <div class="hero">
          <span class="badge" style="background:#fff3;margin-bottom:14px">✨ Guided Pet Health Assessment</span>
          <h1>Smarter Pet Health Decisions, One Consultation at a Time.</h1>
          <p>Tell us about your cat or dog, answer a few simple questions, and get possible conditions with clear advice on what to do next.</p>
        </div>
        """
    )

    if st.button("Start Health Assessment →", key="hero_start_btn"):
        navigate_to("pet")

    # 2. Who is this assessment for?
    render_html('<div class="sec">Who is this assessment for?</div>')

    c_dog, c_cat = st.columns(2)
    with c_dog:
        render_html(
            """
            <div class="card-overlay-container">
              <div class="card h">
                <div class="ico">🐶</div>
                <h3>Dog</h3>
                <p class="m">Stomach, skin, cough and mobility concerns.</p>
              </div>
            </div>
            """
        )
        if st.button("Dog", key="home_card_dog", help="Choose Dog"):
            st.session_state["sp"] = "Dog"
            st.session_state["breed"] = ""
            navigate_to("pet")

    with c_cat:
        render_html(
            """
            <div class="card-overlay-container">
              <div class="card h">
                <div class="ico">🐱</div>
                <h3>Cat</h3>
                <p class="m">Urinary, sneezing, coat and behaviour concerns.</p>
              </div>
            </div>
            """
        )
        if st.button("Cat", key="home_card_cat", help="Choose Cat"):
            st.session_state["sp"] = "Cat"
            st.session_state["breed"] = ""
            navigate_to("pet")

    # 3. How it works
    render_html('<div class="sec">How it works</div>')
    render_html(
        """
        <div class="grid">
          <div class="card"><div class="ico">🐾</div><h3>1. Tell us about your pet</h3></div>
          <div class="card"><div class="ico">🩺</div><h3>2. Answer simple questions</h3></div>
          <div class="card"><div class="ico">🧪</div><h3>3. See possible conditions</h3></div>
          <div class="card"><div class="ico">⚖️</div><h3>4. Get care guidance</h3></div>
        </div>
        """
    )

    # 4. Emergency alert
    render_html(
        """
        <div class="alert">🚨 <b>Emergency?</b> Trouble breathing, collapse, seizures or suspected poison — contact a vet immediately.</div>
        <p class="m">Diagnovet shows <i>possible</i> conditions only. It is not a diagnosis and does not replace a vet.</p>
        """
    )
