"""Shared Header Component for Diagnovet with Back Navigation and Theme Toggle."""

import streamlit as st
from components.theme import render_html


def render_header(
    title: str,
    subtitle: str = "",
    show_back: bool = True,
    back_page: str = None,
):
    """Renders the standard top header on every page.

    Includes page-level back navigation and top theme switcher matching diagnovet.html.
    """
    current_page = st.session_state.get("page", "Home Dashboard")

    # Top Control Bar (Back Button + Theme Switcher)
    col_nav, col_theme = st.columns([3, 1])

    with col_nav:
        if show_back and current_page != "Home Dashboard":
            # Default logical parent page mapping
            parent_map = {
                "Pet Profile": "Home Dashboard",
                "Start Consultation": "Home Dashboard",
                "Symptom Assessment": "Start Consultation",
                "Diagnosis Results": "Start Consultation",
                "Decision Making": "Diagnosis Results",
                "Decision Support System": "Decision Making",
                "Consultation History": "Home Dashboard",
                "About Diagnovet": "Home Dashboard",
                "Safety & Disclaimer": "Home Dashboard",
            }
            target_back = back_page or parent_map.get(current_page, "Home Dashboard")
            if st.button(
                f"← Back to {target_back}",
                key=f"hdr_back_{current_page}",
                type="secondary",
            ):
                st.session_state["page"] = target_back
                st.rerun()

    with col_theme:
        current_theme = st.session_state.get("theme", "Lagoon")
        new_theme = "Aurora" if current_theme == "Lagoon" else "Lagoon"
        btn_label = "🌙 Aurora" if current_theme == "Lagoon" else "☀️ Lagoon"
        if st.button(
            btn_label,
            key=f"hdr_theme_{current_page}",
            help=f"Switch to {new_theme} theme",
            use_container_width=True,
        ):
            st.session_state["theme"] = new_theme
            st.rerun()

    # Main Page Title & Subtitle
    html = f"""
    <div style="margin-bottom: 20px; margin-top: 4px;">
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
        <div class="ico" style="margin: 0; width: 40px; height: 40px; font-size: 20px; border-radius: 12px;">🐾</div>
        <div>
          <h1 style="margin: 0; font-size: 26px; line-height: 1.2;">{title}</h1>
          {f'<p class="m" style="margin: 3px 0 0 0; font-size: 14px;">{subtitle}</p>' if subtitle else ''}
        </div>
      </div>
      <div style="height: 1px; background: var(--line); margin-top: 14px; margin-bottom: 18px;"></div>
    </div>
    """
    render_html(html)
