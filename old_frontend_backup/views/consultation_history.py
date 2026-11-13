"""Page 8: Consultation History View for Diagnovet matching diagnovet.html."""

import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.theme import render_html
from services.mock_repository import DiagnovetRepository


def render_consultation_history_view(repo: DiagnovetRepository):
    """Renders the consultation records log with search and filters matching diagnovet.html."""
    render_header(
        title="Consultation History",
        subtitle="Review past clinical consultations, recorded symptoms, and recommended actions.",
        show_back=True,
    )

    pets = repo.get_all_pets()
    pet_names = ["All"] + [p["name"] for p in pets]
    categories = ["All"] + [c["name"] for c in repo.get_health_categories()]

    col_s1, col_s2, col_s3 = st.columns([3, 2, 2])
    with col_s1:
        search_query = st.text_input(
            "Search Records",
            placeholder="🔍 Search pet, category or outcome",
            label_visibility="collapsed",
        )
    with col_s2:
        selected_pet = st.selectbox("Patient Filter", options=pet_names, index=0)
    with col_s3:
        selected_cat = st.selectbox("Category Filter", options=categories, index=0)

    history_items = repo.get_consultation_history(
        filter_pet=selected_pet,
        filter_category=selected_cat,
    )

    if search_query.strip():
        q = search_query.strip().lower()
        history_items = [
            h
            for h in history_items
            if q in h["pet_name"].lower()
            or q in h["id"].lower()
            or q in h["top_condition"].lower()
            or q in h["category"].lower()
            or q in h["decision"].lower()
        ]

    render_html(f'<div class="sec">Previous Records ({len(history_items)})</div>')

    if not history_items:
        render_html("""
            <div class="card" style="text-align: center; padding: 36px;">
              <div class="ico" style="margin: 0 auto 12px auto;">🔍</div>
              <h3>No Matches Found</h3>
              <p class="m">Try searching for a different keyword or resetting filters.</p>
            </div>
            """)
    else:
        grid_cols = st.columns(2)
        for idx, h in enumerate(history_items):
            col_target = grid_cols[idx % 2]
            badge_cls = (
                "red"
                if h["decision"] == "Get Help Now"
                else (
                    "amb"
                    if h["decision"] == "Visit Vet Today"
                    else "blu" if h["decision"] == "Book a Vet Visit" else "grn"
                )
            )
            icon = "🐱" if h.get("species") == "Cat" else "🐶"

            with col_target:
                render_html(f"""
                    <div class="card h" style="margin-bottom: 12px;">
                      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                          <span style="font-size: 20px;">{icon}</span>
                          <h3 style="margin: 0;">{h['pet_name']}</h3>
                        </div>
                        <span class="m" style="font-size: 12px;">{h['date']}</span>
                      </div>
                      <p class="m" style="margin: 4px 0 10px 0;">{h['category']} &bull; {h['top_condition']}</p>
                      <span class="badge {badge_cls}">{h['decision']}</span>
                    </div>
                    """)
                if st.button(
                    "View Details →",
                    key=f"hist_view_{h['id']}",
                    use_container_width=True,
                    type="secondary",
                ):
                    st.session_state["page"] = "Decision Making"
                    st.rerun()

    render_footer()
