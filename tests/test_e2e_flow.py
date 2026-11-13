"""End-to-end integration test of the complete 9-page Diagnovet assessment flow."""
from streamlit.testing.v1 import AppTest


def test_complete_end_to_end_assessment_flow():
    """Verify user can walk through all 9 views from Home to Final Summary and Safety."""
    at = AppTest.from_file("D:/Diagnovet/app.py").run()
    assert at.session_state["page"] == "home"

    # 1. Start from hero
    for b in at.button:
        if b.key == "hero_start_btn":
            b.click().run()
            break
    assert at.session_state["page"] == "pet"

    # 2. Complete Pet Information
    for b in at.button:
        if b.key == "chip_dog":
            b.click().run()
            break

    for s in at.selectbox:
        if s.key == "pet_breed_select":
            s.select("Golden Retriever").run()
            break

    for s in at.selectbox:
        if s.key == "pet_gender_select":
            s.select("Female").run()
            break

    for t in at.text_input:
        if t.key == "pet_age_input":
            t.input("4").run()
            break

    for b in at.button:
        if b.key == "pet_next_btn":
            b.click().run()
            break
    assert at.session_state["page"] == "q"
    assert at.session_state["qs"] == 2

    # 3. Assessment Step 2 (Symptoms)
    for b in at.button:
        if b.key == "sym_chip_Vomiting":
            b.click().run()
            break
    for b in at.button:
        if b.key == "q_next_btn":
            b.click().run()
            break
    assert at.session_state["qs"] == 3

    # 4. Assessment Step 3 (Follow-ups)
    for b in at.button:
        if b.key == "fu_Vomiting|0_Yes":
            b.click().run()
            break
    for b in at.button:
        if b.key == "fu_Vomiting|1_No":
            b.click().run()
            break
    for b in at.button:
        if b.key == "q_next_btn":
            b.click().run()
            break
    assert at.session_state["qs"] == 4

    # 5. Assessment Step 4 (Timing)
    for s in at.selectbox:
        if s.key == "step4_dur_select":
            s.select("1–3 days").run()
            break
    for b in at.button:
        if b.key == "sev_btn_Severe":
            b.click().run()
            break
    for b in at.button:
        if b.key == "frq_btn_Often":
            b.click().run()
            break
    for b in at.button:
        if b.key == "q_next_btn":
            b.click().run()
            break
    assert at.session_state["qs"] == 5

    # 6. Assessment Step 5 (Emergency check)
    for b in at.button:
        if b.key == "em_0_No":
            b.click().run()
            break
    for b in at.button:
        if b.key == "em_1_No":
            b.click().run()
            break
    for b in at.button:
        if b.key == "em_2_No":
            b.click().run()
            break
    for b in at.button:
        if b.key == "q_next_btn":
            b.click().run()
            break
    assert at.session_state["page"] == "review"
    assert at.session_state["qdone"] == 1

    # 7. Review answers -> Edit button test (jump to Step 4)
    for b in at.button:
        if b.key == "rev_edit_timing":
            b.click().run()
            break
    assert at.session_state["page"] == "q"
    assert at.session_state["qs"] == 4

    # Jump back to Review
    at.session_state["page"] = "review"
    at.run()

    # 8. Review -> Possible Conditions
    for b in at.button:
        if b.key == "rev_show_cond_btn":
            b.click().run()
            break
    assert at.session_state["page"] == "cond"
    assert at.session_state["sub"] == 1

    # 9. Conditions -> Care Guidance
    for b in at.button:
        if b.key == "cond_next_btn":
            b.click().run()
            break
    assert at.session_state["page"] == "care"

    # 10. Care Guidance -> Decision Support
    for b in at.button:
        if b.key == "care_next_btn":
            b.click().run()
            break
    assert at.session_state["page"] == "support"

    # 11. Decision Support -> Final Summary
    for b in at.button:
        if b.key == "supp_next_btn":
            b.click().run()
            break
    assert at.session_state["page"] == "summary"

    # 12. Safety page navigation
    for b in at.button:
        if b.key == "sb_nav_safety":
            b.click().run()
            break
    assert at.session_state["page"] == "safety"
