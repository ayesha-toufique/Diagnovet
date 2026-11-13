"""Page 9: About Diagnovet Academic Architecture View matching diagnovet.html."""

import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.cards import render_hero, render_feature_card
from components.theme import render_html
from services.mock_repository import DiagnovetRepository


def render_about_view(repo: DiagnovetRepository):
    """Renders academic context, system architecture, methodology, and limitations matching diagnovet.html."""
    render_header(
        title="About Diagnovet",
        subtitle="Architecture, methodology, and academic objectives for the IAI CCP Expert System project.",
        show_back=True,
    )

    render_hero(
        title="Intelligent Companion Animal Health Support",
        subtitle="Diagnovet bridges the gap between pet owner observations and timely professional veterinary intervention through structured rule-based knowledge engineering.",
        badge_text="IAI CCP Project Overview",
    )

    # Core Principles matching diagnovet.html
    about_points = [
        (
            "🐶 Companion Health Support",
            "Diagnovet is a veterinary decision-support tool designed specifically for cat and dog guardians.",
        ),
        (
            "🎯 Clear Academic Objectives",
            "Structured symptom consultations, explainable possible condition matching, and clear four-tier urgency decisions.",
        ),
        (
            "🧠 Expert System Architecture",
            "Expert System inference, Decision Making algorithms, and DSS multi-attribute evaluations are previewed here in the frontend design.",
        ),
        (
            "🛡️ Clinical Safety Limitation",
            "Diagnovet is an educational decision-support aid and never replaces a licensed veterinary surgeon's physical clinical examination.",
        ),
    ]

    for title, desc in about_points:
        render_html(f"""
            <div class="card" style="margin-bottom: 12px;">
              <h3 style="margin: 0 0 4px 0; font-size: 16px;">{title}</h3>
              <p class="m" style="margin: 0; font-size: 13.5px;">{desc}</p>
            </div>
            """)

    render_html('<div class="sec">Technical Pillars</div>')
    arch_c1, arch_c2, arch_c3 = st.columns(3)
    with arch_c1:
        render_feature_card(
            icon="📚",
            title="Knowledge Base",
            description="Veterinary consensus covering canine and feline clinical presentations.",
        )
    with arch_c2:
        render_feature_card(
            icon="⚡",
            title="Inference Engine",
            description="Forward chaining matcher evaluating facts from Working Memory against premise rules.",
        )
    with arch_c3:
        render_feature_card(
            icon="📊",
            title="Decision Support",
            description="Multi-attribute utility balancing symptom overlap, clinical severity, and patient timeline.",
        )

    render_footer()
