"""Page 2: Pet Profile Management View for Diagnovet matching diagnovet.html."""

from typing import Dict, Any
import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.cards import render_pet_card
from components.theme import render_html
from services.mock_repository import DiagnovetRepository


def render_pet_profile_view(repo: DiagnovetRepository):
    """Renders the pet profile registration, selection, and editing screen."""
    render_header(
        title="Pet Profile",
        subtitle="Register, update, and manage companion animal health records.",
        show_back=True,
    )

    pets = repo.get_all_pets()
    active_pet_id = st.session_state.get("selected_pet", {}).get(
        "id", pets[0]["id"] if pets else None
    )

    col_form, col_list = st.columns([1, 1])

    with col_list:
        render_html(
            '<div class="sec" style="margin-top: 0;">Registered Companion Animals</div>'
        )
        render_html(
            '<p class="m" style="margin-bottom: 12px;">Click a card below to select as the active patient:</p>'
        )

        for pet in pets:
            is_active = pet["id"] == active_pet_id
            render_pet_card(pet, is_selected=is_active)
            btn_txt = "✅ Currently Active" if is_active else f"Select {pet['name']}"
            if st.button(
                btn_txt,
                key=f"sel_pet_{pet['id']}",
                use_container_width=True,
                disabled=is_active,
            ):
                st.session_state["selected_pet"] = pet
                st.rerun()

    with col_form:
        render_html('<div class="sec" style="margin-top: 0;">Profile Actions</div>')
        tab_new, tab_edit = st.tabs(["➕ Add New Pet", "✏️ Edit Active Profile"])

        with tab_new:
            with st.form("new_pet_form"):
                name = st.text_input("Pet Name *", placeholder="e.g. Milo")
                c1, c2 = st.columns(2)
                with c1:
                    species = st.selectbox("Species *", options=["Dog", "Cat"], index=0)
                    breed = st.text_input(
                        "Breed *", placeholder="e.g. Golden Retriever"
                    )
                with c2:
                    age = st.number_input(
                        "Age (years) *",
                        min_value=0.1,
                        max_value=30.0,
                        value=3.0,
                        step=0.5,
                    )
                    weight = st.number_input(
                        "Weight (kg) *",
                        min_value=0.2,
                        max_value=120.0,
                        value=12.0,
                        step=0.5,
                    )

                gender = st.selectbox(
                    "Gender & Altered Status *",
                    options=[
                        "Female (Spayed)",
                        "Female (Intact)",
                        "Male (Neutered)",
                        "Male (Intact)",
                        "Unknown",
                    ],
                )
                allergies = st.text_input(
                    "Allergies / Previous Conditions",
                    placeholder="e.g. Sensitive to beef, flea allergy",
                )
                notes = st.text_area(
                    "Additional Notes",
                    placeholder="e.g. Indoor only, up to date on vaccines",
                )

                submit_new = st.form_submit_button("Save Profile")
                if submit_new:
                    if not name.strip() or not breed.strip():
                        st.error("Pet name and breed are required.")
                    else:
                        new_data: Dict[str, Any] = {
                            "name": name.strip(),
                            "species": species,
                            "breed": breed.strip(),
                            "age": float(age),
                            "gender": gender,
                            "weight": float(weight),
                            "conditions": allergies.strip() or "None",
                            "allergies": allergies.strip() or "None",
                            "notes": notes.strip(),
                        }
                        new_id = repo.add_pet(new_data)
                        new_data["id"] = new_id
                        st.session_state["selected_pet"] = new_data
                        st.success(f"Profile for {name} saved successfully!")
                        st.rerun()

        with tab_edit:
            active_pet = st.session_state.get("selected_pet", pets[0] if pets else None)
            if not active_pet:
                st.info("No active pet selected to edit.")
            else:
                with st.form("edit_pet_form"):
                    e_name = st.text_input(
                        "Pet Name *", value=active_pet.get("name", "")
                    )
                    c1, c2 = st.columns(2)
                    with c1:
                        sp_idx = 0 if active_pet.get("species") == "Dog" else 1
                        e_species = st.selectbox(
                            "Species *", options=["Dog", "Cat"], index=sp_idx
                        )
                        e_breed = st.text_input(
                            "Breed *", value=active_pet.get("breed", "")
                        )
                    with c2:
                        e_age = st.number_input(
                            "Age (years) *",
                            min_value=0.1,
                            max_value=30.0,
                            value=float(active_pet.get("age", 3.0)),
                            step=0.5,
                        )
                        e_weight = st.number_input(
                            "Weight (kg) *",
                            min_value=0.2,
                            max_value=120.0,
                            value=float(active_pet.get("weight", 10.0)),
                            step=0.5,
                        )

                    g_opts = [
                        "Female (Spayed)",
                        "Female (Intact)",
                        "Male (Neutered)",
                        "Male (Intact)",
                        "Unknown",
                    ]
                    cur_g = active_pet.get("gender", "Female (Spayed)")
                    g_idx = g_opts.index(cur_g) if cur_g in g_opts else 0
                    e_gender = st.selectbox(
                        "Gender & Altered Status *", options=g_opts, index=g_idx
                    )

                    e_allergies = st.text_input(
                        "Allergies / Previous Conditions",
                        value=active_pet.get("conditions", ""),
                    )
                    e_notes = st.text_area(
                        "Additional Notes", value=active_pet.get("notes", "")
                    )

                    submit_edit = st.form_submit_button("Update Profile")
                    if submit_edit:
                        if not e_name.strip() or not e_breed.strip():
                            st.error("Pet name and breed cannot be empty.")
                        else:
                            up_data: Dict[str, Any] = {
                                "id": active_pet["id"],
                                "name": e_name.strip(),
                                "species": e_species,
                                "breed": e_breed.strip(),
                                "age": float(e_age),
                                "gender": e_gender,
                                "weight": float(e_weight),
                                "conditions": e_allergies.strip() or "None",
                                "allergies": e_allergies.strip() or "None",
                                "notes": e_notes.strip(),
                            }
                            repo.update_pet(active_pet["id"], up_data)
                            st.session_state["selected_pet"] = up_data
                            st.success(f"Profile for {e_name} updated successfully!")
                            st.rerun()

    render_footer()
