"""Pet Information view (Step 1 of 6) matching design_reference/diagnovet_flow.html."""
import streamlit as st
from data.question_bank import BREEDS
from components.widgets import render_head, render_prog
from components.layout import navigate_to


def render_pet_information_view():
    """Renders Step 1: Pet Information."""
    render_head("Pet Information", "Basic details for this assessment only. Nothing is saved.")
    render_prog(1)

    errors = st.session_state.get("errors", {})
    sp = st.session_state.get("sp", "")
    breed = st.session_state.get("breed", "")
    gen = st.session_state.get("gen", "")
    age = st.session_state.get("age", "")
    wt = st.session_state.get("wt", "")
    bg = st.session_state.get("bg", "")

    with st.container(border=True):
        # 1. Species chips
        st.markdown('<label>Species</label>', unsafe_allow_html=True)
        c_sp1, c_sp2, _ = st.columns([1, 1, 3])
        with c_sp1:
            is_dog = sp == "Dog"
            if st.button("🐶 Dog", key="chip_dog", type="primary" if is_dog else "secondary", use_container_width=True):
                st.session_state["sp"] = "Dog"
                st.session_state["breed"] = ""
                if "sp" in errors:
                    del errors["sp"]
                st.rerun()

        with c_sp2:
            is_cat = sp == "Cat"
            if st.button("🐱 Cat", key="chip_cat", type="primary" if is_cat else "secondary", use_container_width=True):
                st.session_state["sp"] = "Cat"
                st.session_state["breed"] = ""
                if "sp" in errors:
                    del errors["sp"]
                st.rerun()

        if "sp" in errors:
            st.markdown(f'<div class="err">{errors["sp"]}</div>', unsafe_allow_html=True)

        # 2. Breed and Gender
        c_br, c_gn = st.columns(2)
        with c_br:
            st.markdown('<label>Breed</label>', unsafe_allow_html=True)
            if sp:
                options = ["Choose a breed"] + BREEDS.get(sp, [])
                curr_idx = options.index(breed) if breed in options else 0
                selected_breed = st.selectbox(
                    "Breed",
                    options=options,
                    index=curr_idx,
                    label_visibility="collapsed",
                    key="pet_breed_select",
                )
                if selected_breed != "Choose a breed":
                    st.session_state["breed"] = selected_breed
                else:
                    st.session_state["breed"] = ""
            else:
                st.selectbox(
                    "Breed",
                    options=["Choose species first"],
                    disabled=True,
                    label_visibility="collapsed",
                    key="pet_breed_disabled",
                )
                st.session_state["breed"] = ""

            if "breed" in errors:
                st.markdown(f'<div class="err">{errors["breed"]}</div>', unsafe_allow_html=True)

        with c_gn:
            st.markdown('<label>Gender</label>', unsafe_allow_html=True)
            gender_options = ["Choose", "Male", "Female"]
            curr_g_idx = gender_options.index(gen) if gen in gender_options else 0
            selected_gender = st.selectbox(
                "Gender",
                options=gender_options,
                index=curr_g_idx,
                label_visibility="collapsed",
                key="pet_gender_select",
            )
            if selected_gender != "Choose":
                st.session_state["gen"] = selected_gender
            else:
                st.session_state["gen"] = ""

            if "gen" in errors:
                st.markdown(f'<div class="err">{errors["gen"]}</div>', unsafe_allow_html=True)

        # 3. Age and Weight
        c_ag, c_wt = st.columns(2)
        with c_ag:
            st.markdown('<label>Age (years)</label>', unsafe_allow_html=True)
            val_age = st.text_input(
                "Age (years)",
                value=str(age) if age != "" else "",
                placeholder="",
                label_visibility="collapsed",
                key="pet_age_input",
            )
            st.session_state["age"] = val_age.strip()
            if "age" in errors:
                st.markdown(f'<div class="err">{errors["age"]}</div>', unsafe_allow_html=True)

        with c_wt:
            st.markdown('<label>Weight in kg (optional)</label>', unsafe_allow_html=True)
            val_wt = st.text_input(
                "Weight in kg (optional)",
                value=str(wt) if wt != "" else "",
                placeholder="",
                label_visibility="collapsed",
                key="pet_wt_input",
            )
            st.session_state["wt"] = val_wt.strip()
            if "wt" in errors:
                st.markdown(f'<div class="err">{errors["wt"]}</div>', unsafe_allow_html=True)

        # 4. Medical background
        st.markdown('<label>Medical background or allergies (optional)</label>', unsafe_allow_html=True)
        val_bg = st.text_area(
            "Medical background or allergies (optional)",
            value=bg,
            height=85,
            label_visibility="collapsed",
            key="pet_bg_input",
        )
        st.session_state["bg"] = val_bg

    # 5. Nav buttons
    st.markdown('<div class="nav2">', unsafe_allow_html=True)
    c_n1, c_n2 = st.columns([5, 1])
    with c_n2:
        if st.button("Next →", key="pet_next_btn", use_container_width=True):
            # Validation
            e = {}
            current_sp = st.session_state.get("sp", "")
            current_breed = st.session_state.get("breed", "")
            current_gen = st.session_state.get("gen", "")
            current_age = st.session_state.get("age", "")
            current_wt = st.session_state.get("wt", "")

            if not current_sp:
                e["sp"] = "Please choose Dog or Cat."
            if not current_breed:
                e["breed"] = "Please choose a breed."
            if not current_gen:
                e["gen"] = "Please choose a gender."

            if current_age == "":
                e["age"] = "Enter an age from 0 to 30."
            else:
                try:
                    num_age = float(current_age)
                    if num_age < 0 or num_age > 30:
                        e["age"] = "Enter an age from 0 to 30."
                except ValueError:
                    e["age"] = "Enter an age from 0 to 30."

            if current_wt != "":
                try:
                    num_wt = float(current_wt)
                    if num_wt < 0.5 or num_wt > 90:
                        e["wt"] = "Enter a weight from 0.5 to 90 kg."
                except ValueError:
                    e["wt"] = "Enter a weight from 0.5 to 90 kg."

            st.session_state["errors"] = e
            if not e:
                st.session_state["qs"] = 2
                navigate_to("q")
            else:
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
