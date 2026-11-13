"""Shared Sidebar Navigation Component for Diagnovet."""

import streamlit as st
from components.theme import render_html

PAGES = [
    ("Home Dashboard", "🏠", "Home"),
    ("Pet Profile", "🐶", "Pet Profile"),
    ("Start Consultation", "🩺", "Consultation"),
    ("Symptom Assessment", "📋", "Assessment"),
    ("Diagnosis Results", "🧪", "Results"),
    ("Decision Making", "⚖️", "Decision"),
    ("Decision Support System", "📊", "DSS Report"),
    ("Consultation History", "🕘", "History"),
    ("About Diagnovet", "ℹ️", "About"),
    ("Safety & Disclaimer", "🛡️", "Safety"),
]


def render_sidebar():
    """Renders the custom sidebar with logo, navigation links, pet badge, and theme toggle."""
    with st.sidebar:
        # App Branding Header matching diagnovet.html
        brand_html = """
        <div style="padding: 6px 0 14px 0; text-align: center;">
          <div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 4px;">
            <div class="ico" style="margin: 0; width: 38px; height: 38px; font-size: 20px; border-radius: 12px;">🐾</div>
            <span class="dv-wordmark" style="font-size: 23px; font-weight: 800;">Diagnovet</span>
          </div>
          <div style="font-size: 11.5px; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
            Smart Pet Health DSS
          </div>
        </div>
        <div style="height: 1px; background: var(--line); margin-bottom: 14px;"></div>
        """
        render_html(brand_html)

        # Active Pet Pill
        active_pet = st.session_state.get("selected_pet", None)
        if active_pet:
            icon = "🐱" if active_pet.get("species") == "Cat" else "🐶"
            pet_html = f"""
            <div style="background: rgba(46,125,255,0.08); border: 1.5px solid var(--a); border-radius: 14px; padding: 10px 14px; margin-bottom: 16px;">
              <div style="font-size: 11px; text-transform: uppercase; color: var(--muted); font-weight: 700;">Active Patient</div>
              <div style="font-size: 15px; font-weight: 800; color: var(--text); display: flex; align-items: center; gap: 6px; margin-top: 2px;">
                <span>{icon}</span> {active_pet.get('name', 'Unknown')}
                <span style="font-size: 12px; font-weight: 500; color: var(--muted);">({active_pet.get('breed', '')})</span>
              </div>
            </div>
            """
            render_html(pet_html)
        else:
            no_pet_html = """
            <div style="background: var(--card); border: 1px dashed var(--line); border-radius: 14px; padding: 10px 14px; margin-bottom: 16px; text-align: center;">
              <span style="font-size: 12.5px; color: var(--muted);">No active pet selected</span>
            </div>
            """
            render_html(no_pet_html)

        # Navigation Menu
        render_html(
            '<div style="font-size: 11px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 8px;">Navigation</div>'
        )

        current_page = st.session_state.get("page", "Home Dashboard")

        for page_name, icon, short_label in PAGES:
            is_active = current_page == page_name
            button_label = f"{icon}  {page_name}"
            if st.button(
                button_label,
                key=f"nav_{page_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state["page"] = page_name
                st.rerun()

        # Theme Selector at Bottom
        render_html(
            '<div style="height: 1px; background: var(--line); margin: 20px 0 14px 0;"></div>'
            '<div style="font-size: 11px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 8px;">Theme</div>'
        )

        theme_choice = st.radio(
            "Select UI Theme",
            options=["Lagoon (Mint)", "Aurora (Dark)"],
            index=0 if st.session_state.get("theme", "Lagoon") == "Lagoon" else 1,
            label_visibility="collapsed",
            key="sidebar_theme_radio",
        )
        selected_theme = "Lagoon" if "Lagoon" in theme_choice else "Aurora"
        if selected_theme != st.session_state.get("theme", "Lagoon"):
            st.session_state["theme"] = selected_theme
            st.rerun()
