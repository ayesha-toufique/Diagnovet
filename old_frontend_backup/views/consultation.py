"""Page 3: Start Consultation 5-Step Workflow for Diagnovet matching diagnovet.html."""

from typing import Dict, Any
import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.reusable_widgets import render_stepper
from components.cards import render_pet_card
from components.theme import render_html
from services.mock_repository import DiagnovetRepository

CONSULTATION_STEPS = [
    "Select Pet",
    "Health Category",
    "Symptom Questionnaire",
    "Follow-up Questions",
    "Review & Submit",
]


def render_consultation_view(repo: DiagnovetRepository):
    """Renders the 5-step guided consultation workflow matching diagnovet.html."""
    render_header(
        title="Consultation",
        subtitle="Guided 5-step clinical evaluation for companion animals.",
        show_back=True,
    )

    # Initialize consultation session state
    if "consult_step" not in st.session_state:
        st.session_state["consult_step"] = 0
    if "consult_category" not in st.session_state:
        st.session_state["consult_category"] = "digestive"
    if "consult_answers" not in st.session_state:
        st.session_state["consult_answers"] = {}
    if "consult_followups" not in st.session_state:
        st.session_state["consult_followups"] = {}

    step_idx = st.session_state["consult_step"]
    render_stepper(CONSULTATION_STEPS, step_idx)

    pets = repo.get_all_pets()
    current_pet = st.session_state.get("selected_pet", pets[0] if pets else None)
    categories = repo.get_health_categories()

    # STEP 0: SELECT PET
    if step_idx == 0:
        render_html(
            '<div class="sec" style="margin-top: 0;">Step 1 &mdash; Select your pet</div>'
        )
        render_html(
            '<p class="m" style="margin-bottom: 14px;">Choose the companion animal needing clinical assessment today:</p>'
        )

        # Interactive pet cards matching diagnovet.html
        for pet in pets:
            is_sel = current_pet and pet["id"] == current_pet["id"]
            render_pet_card(pet, is_selected=is_sel)
            btn_txt = "✅ Active Patient" if is_sel else f"Select {pet['name']}"
            if st.button(
                btn_txt,
                key=f"step0_pick_{pet['id']}",
                use_container_width=True,
                disabled=is_sel,
            ):
                st.session_state["selected_pet"] = pet
                st.rerun()

        render_html('<div style="height: 18px;"></div>')
        c_prev, c_next = st.columns([1, 1])
        with c_next:
            if st.button(
                "Next: Health Category →", key="step0_next", use_container_width=True
            ):
                st.session_state["consult_step"] = 1
                st.rerun()

    # STEP 1: SELECT HEALTH CATEGORY
    elif step_idx == 1:
        render_html(
            '<div class="sec" style="margin-top: 0;">Step 2 &mdash; Main health category</div>'
        )
        render_html(
            '<p class="m" style="margin-bottom: 14px;">Select the primary bodily system or symptoms observed:</p>'
        )

        active_cat_id = st.session_state.get("consult_category", "digestive")
        cat_cols = st.columns(3)

        for i, cat in enumerate(categories):
            col_target = cat_cols[i % 3]
            with col_target:
                is_active = active_cat_id == cat["id"]
                border_s = (
                    "border-color: var(--a) !important; box-shadow: var(--glow);"
                    if is_active
                    else ""
                )
                badge_html = (
                    '<span class="badge blu" style="margin-left: auto;">Selected</span>'
                    if is_active
                    else ""
                )

                render_html(f"""
                    <div class="card h {'sel' if is_active else ''}" style="padding: 16px; margin-bottom: 8px; {border_s}">
                      <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div class="ico" style="margin: 0; width: 40px; height: 40px; font-size: 18px;">{cat['icon']}</div>
                        {badge_html}
                      </div>
                      <h3 style="margin: 8px 0 2px 0; font-size: 16px;">{cat['name']}</h3>
                      <p class="m" style="margin: 0; font-size: 12px;">{cat['desc']}</p>
                    </div>
                    """)
                if st.button(
                    f"Choose {cat['name']}",
                    key=f"pick_cat_{cat['id']}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    st.session_state["consult_category"] = cat["id"]
                    st.rerun()

        render_html('<div style="height: 18px;"></div>')
        c_prev, c_next = st.columns([1, 1])
        with c_prev:
            if st.button(
                "← Previous",
                key="step1_prev",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state["consult_step"] = 0
                st.rerun()
        with c_next:
            if st.button(
                "Next: Questionnaire →", key="step1_next", use_container_width=True
            ):
                st.session_state["consult_step"] = 2
                st.rerun()

    # STEP 2: SYMPTOM QUESTIONNAIRE
    elif step_idx == 2:
        active_cat_id = st.session_state.get("consult_category", "digestive")
        cat_info = next(
            (c for c in categories if c["id"] == active_cat_id), categories[0]
        )
        render_html(
            f'<div class="sec" style="margin-top: 0;">Step 3 &mdash; Symptom questionnaire ({cat_info["name"]})</div>'
        )
        render_html(
            '<p class="m" style="margin-bottom: 14px;">Answer each clinical question based on recent observations:</p>'
        )

        questions = repo.get_questions_for_category(active_cat_id)

        for q_idx, q in enumerate(questions):
            q_id = q["id"]
            cur_val = st.session_state["consult_answers"].get(q_id, "Not Sure")

            render_html(f"""
                <div class="q">
                  <b>{q_idx + 1}. {q['question']}</b>
                  <p class="m" style="margin: 2px 0 6px 0; font-size: 12.5px;">{q['subtext']}</p>
                </div>
                """)

            options = ["Yes", "No", "Not Sure"]
            sel_ans = st.radio(
                f"Question {q_idx + 1}",
                options=options,
                index=options.index(cur_val) if cur_val in options else 2,
                key=f"q_radio_{q_id}",
                horizontal=True,
                label_visibility="collapsed",
            )
            st.session_state["consult_answers"][q_id] = sel_ans

        render_html('<div style="height: 18px;"></div>')
        c_prev, c_next = st.columns([1, 1])
        with c_prev:
            if st.button(
                "← Previous",
                key="step2_prev",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state["consult_step"] = 1
                st.rerun()
        with c_next:
            if st.button(
                "Next: Follow-up Questions →",
                key="step2_next",
                use_container_width=True,
            ):
                st.session_state["consult_step"] = 3
                st.rerun()

    # STEP 3: FOLLOW-UP QUESTIONS
    elif step_idx == 3:
        render_html(
            '<div class="sec" style="margin-top: 0;">Step 4 &mdash; Follow-up questions <span class="badge blu">simulated</span></div>'
        )
        render_html(
            '<p class="m" style="margin-bottom: 14px;">Targeted conditional questions based on reported symptoms:</p>'
        )

        active_cat_id = st.session_state.get("consult_category", "digestive")
        questions = repo.get_questions_for_category(active_cat_id)
        yes_questions = [
            q
            for q in questions
            if st.session_state["consult_answers"].get(q["id"]) == "Yes"
        ]

        # Emergency breathing check question matching diagnovet.html
        render_html("""
            <div class="q">
              <b>Is your pet having noticeable difficulty breathing or gasping?</b>
              <p class="m" style="margin: 2px 0 6px 0; font-size: 12.5px;">Open-mouth panting (cats) or abdominal pumping effort</p>
            </div>
            """)
        cur_breath = st.session_state["consult_followups"].get("breathing", "No")
        breath_ans = st.radio(
            "Difficulty breathing",
            options=["Yes", "No", "Not Sure"],
            index=(
                ["Yes", "No", "Not Sure"].index(cur_breath)
                if cur_breath in ["Yes", "No", "Not Sure"]
                else 1
            ),
            key="followup_breathing",
            horizontal=True,
            label_visibility="collapsed",
        )
        st.session_state["consult_followups"]["breathing"] = breath_ans

        if breath_ans == "Yes":
            render_html("""
                <div class="alert">
                  🚨 <b>Difficulty breathing is an emergency sign.</b> Please seek immediate veterinary hospital care.
                </div>
                """)

        if yes_questions:
            for q in yes_questions:
                q_id = q["id"]
                render_html(f"""
                    <div class="q">
                      <b>Follow-up: {q['followup']}</b>
                      <p class="m" style="margin: 2px 0 6px 0; font-size: 12.5px;">Triggered by: {q['question']}</p>
                    </div>
                    """)
                cur_f = st.session_state["consult_followups"].get(q_id, "Not Sure")
                ans_f = st.radio(
                    f"Follow-up for {q_id}",
                    options=["Yes", "No", "Not Sure"],
                    index=(
                        ["Yes", "No", "Not Sure"].index(cur_f)
                        if cur_f in ["Yes", "No", "Not Sure"]
                        else 2
                    ),
                    key=f"followup_radio_{q_id}",
                    horizontal=True,
                    label_visibility="collapsed",
                )
                st.session_state["consult_followups"][q_id] = ans_f
        else:
            render_html("""
                <div class="q">
                  <b>Has this condition been progressively worsening over the past 48 hours?</b>
                </div>
                """)
            cur_prog = st.session_state["consult_followups"].get("progression", "No")
            ans_prog = st.radio(
                "Progression",
                options=["Yes", "No", "Not Sure"],
                index=(
                    ["Yes", "No", "Not Sure"].index(cur_prog)
                    if cur_prog in ["Yes", "No", "Not Sure"]
                    else 1
                ),
                key="followup_progression",
                horizontal=True,
                label_visibility="collapsed",
            )
            st.session_state["consult_followups"]["progression"] = ans_prog

        render_html('<div style="height: 18px;"></div>')
        c_prev, c_next = st.columns([1, 1])
        with c_prev:
            if st.button(
                "← Previous",
                key="step3_prev",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state["consult_step"] = 2
                st.rerun()
        with c_next:
            if st.button(
                "Next: Review & Submit →", key="step3_next", use_container_width=True
            ):
                st.session_state["consult_step"] = 4
                st.rerun()

    # STEP 4: REVIEW & SUBMIT
    elif step_idx == 4:
        active_cat_id = st.session_state.get("consult_category", "digestive")
        cat_info = next(
            (c for c in categories if c["id"] == active_cat_id), categories[0]
        )
        pet_name = current_pet.get("name", "Pet") if current_pet else "Pet"

        render_html(
            '<div class="sec" style="margin-top: 0;">Step 5 &mdash; Review & submit</div>'
        )
        render_html(
            f'<p class="m" style="margin-bottom: 16px;"><b>Patient:</b> {pet_name} &bull; <b>Category:</b> {cat_info["name"]}</p>'
        )

        questions = repo.get_questions_for_category(active_cat_id)
        for idx, q in enumerate(questions):
            ans = st.session_state["consult_answers"].get(q["id"], "Not Sure")
            badge_cls = "red" if ans == "Yes" else "grn" if ans == "No" else "blu"
            render_html(f"""
                <div class="q" style="display: flex; justify-content: space-between; align-items: center;">
                  <div>
                    <span class="m" style="font-size: 13px;">{idx + 1}. {q['question']}</span>
                  </div>
                  <span class="badge {badge_cls}">{ans}</span>
                </div>
                """)

        render_html('<div style="height: 20px;"></div>')
        c_prev, c_sub = st.columns([1, 1])
        with c_prev:
            if st.button(
                "← Previous",
                key="step4_prev",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state["consult_step"] = 3
                st.rerun()
        with c_sub:
            if st.button("Submit ✓", key="step4_submit", use_container_width=True):
                # Save consultation record into mock repository history
                record: Dict[str, Any] = {
                    "pet_name": pet_name,
                    "species": (
                        current_pet.get("species", "Cat") if current_pet else "Cat"
                    ),
                    "category": cat_info["name"],
                    "date": "2026-11-12",
                    "top_condition": (
                        "Gastric Upset (demo)"
                        if cat_info["id"] == "digestive"
                        else "Clinical Condition (demo)"
                    ),
                    "confidence": "78%",
                    "decision": "Visit Vet Today",
                    "status": "Completed",
                }
                repo.add_consultation_record(record)
                st.session_state["consult_step"] = 0
                st.session_state["page"] = "Diagnosis Results"
                st.rerun()

    render_footer()
