"""Page 1: Home Dashboard View for Diagnovet matching diagnovet.html."""

import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.cards import render_hero, render_feature_card, render_emergency_alert
from components.theme import render_html
from services.mock_repository import DiagnovetRepository


def render_home_view(repo: DiagnovetRepository):
    """Renders the comprehensive landing dashboard matching diagnovet.html."""
    render_header(
        title="Diagnovet Health Portal",
        subtitle="Smarter Pet Health Decisions, One Consultation at a Time.",
        show_back=False,
    )

    # Hero Banner matching diagnovet.html
    render_hero(
        title="Smarter Pet Health Decisions, One Consultation at a Time.",
        subtitle="Guided symptom consultations for cats and dogs that explain every recommendation — clearly and safely.",
        badge_text="✨ Veterinary Decision Support",
    )

    # Primary Action Button
    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        if st.button(
            "Start Consultation →", key="home_start_consult", use_container_width=True
        ):
            st.session_state["consult_step"] = 0
            st.session_state["page"] = "Start Consultation"
            st.rerun()
    with col_c2:
        if st.button(
            "🐶 Pet Profiles & Management",
            key="home_manage_pets",
            type="secondary",
            use_container_width=True,
        ):
            st.session_state["page"] = "Pet Profile"
            st.rerun()

    # Who needs care today? section matching diagnovet.html
    render_html('<div class="sec">Who needs care today?</div>')
    col_dog, col_cat = st.columns(2)
    with col_dog:
        render_html("""
            <div class="card h" style="margin-bottom: 0;">
              <div class="ico">🐶</div>
              <h3>Dog</h3>
              <p class="m">Digestive, skin, joint and behaviour concerns.</p>
            </div>
            """)
        if st.button(
            "Consult for Dog",
            key="home_pick_dog",
            use_container_width=True,
            type="secondary",
        ):
            pets = repo.get_all_pets()
            dog_pet = next((p for p in pets if p.get("species") == "Dog"), pets[0])
            st.session_state["selected_pet"] = dog_pet
            st.session_state["consult_step"] = 1
            st.session_state["page"] = "Start Consultation"
            st.rerun()

    with col_cat:
        render_html("""
            <div class="card h" style="margin-bottom: 0;">
              <div class="ico">🐱</div>
              <h3>Cat</h3>
              <p class="m">Urinary, respiratory, dental and coat concerns.</p>
            </div>
            """)
        if st.button(
            "Consult for Cat",
            key="home_pick_cat",
            use_container_width=True,
            type="secondary",
        ):
            pets = repo.get_all_pets()
            cat_pet = next((p for p in pets if p.get("species") == "Cat"), pets[0])
            st.session_state["selected_pet"] = cat_pet
            st.session_state["consult_step"] = 1
            st.session_state["page"] = "Start Consultation"
            st.rerun()

    # How Diagnovet works matching diagnovet.html
    render_html('<div class="sec">How Diagnovet works</div>')
    how_steps = [
        ("1", "Add pet", "Select existing companion or register vital stats."),
        ("2", "Pick category", "Choose from 9 specialized health domains."),
        ("3", "Answer questions", "Interactive symptom questionnaire with follow-ups."),
        (
            "4",
            "Get explained advice",
            "Receive categorized triage action & evidence breakdown.",
        ),
    ]
    c_steps = st.columns(4)
    for idx, col in enumerate(c_steps):
        num, title, desc = how_steps[idx]
        with col:
            render_html(f"""
                <div class="card" style="height: 100%;">
                  <div class="ico" style="width: 38px; height: 38px; font-size: 18px;">{num}</div>
                  <h3 style="font-size: 15px;">{title}</h3>
                  <p class="m" style="font-size: 12.5px;">{desc}</p>
                </div>
                """)

    # Core Features matching diagnovet.html
    render_html('<div class="sec">Core features</div>')
    f_cols = st.columns(4)
    with f_cols[0]:
        render_feature_card(
            icon="🧠",
            title="Intelligent Diagnosis",
            description="Possible conditions ranked by concordance, never confirmed.",
        )
    with f_cols[1]:
        render_feature_card(
            icon="📚",
            title="Expert System",
            description="Knowledge-based veterinary reasoning and inference.",
        )
    with f_cols[2]:
        render_feature_card(
            icon="⚖️",
            title="Decision Making",
            description="Four clear clinical urgency outcomes with explanation.",
        )
    with f_cols[3]:
        render_feature_card(
            icon="📊",
            title="Decision Support",
            description="Compare options with supporting and missing evidence.",
        )

    # Health Categories Chips matching diagnovet.html
    render_html('<div class="sec">Health categories</div>')
    categories = repo.get_health_categories()
    chips_html = "".join(
        [f'<span class="chip">{c["icon"]} {c["name"]}</span>' for c in categories]
    )
    render_html(f'<div class="chips">{chips_html}</div>')

    # Emergency Alert matching diagnovet.html
    render_emergency_alert(
        "Trouble breathing, collapse, seizures or suspected poisoning &mdash; contact an emergency vet hospital immediately.",
        title="Emergency?",
    )

    render_footer()
