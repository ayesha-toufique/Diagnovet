"""Assessment view (Steps 2-5 of 6) matching design_reference/diagnovet_flow.html."""
import streamlit as st
from data.question_bank import SYMPTOMS, FOLLOW_UPS, EMERGENCY_QUESTIONS
from components.widgets import render_head, render_prog
from components.layout import navigate_to, navigate_back, show_confirm_dialog, reset_assessment


def render_assessment_view():
    """Renders Step 2-5 Assessment."""
    sp = st.session_state.get("sp", "Dog")
    qs = st.session_state.get("qs", 2)
    syms = st.session_state.get("syms", [])
    ans = st.session_state.get("ans", {})
    dur = st.session_state.get("dur", "")
    sev = st.session_state.get("sev", "")
    frq = st.session_state.get("frq", "")
    em = st.session_state.get("em", {})
    err_q = st.session_state.get("errors", {}).get("q", "")

    # Header and progress
    render_head("Health Assessment", f"Questions are chosen for your {sp.lower()}.")
    render_prog(qs)

    with st.container(border=True):
        # STEP 2: Symptoms selection
        if qs == 2:
            st.markdown(
                """
                <h3>Which signs have you noticed?</h3>
                <p class="m">You can choose more than one.</p>
                <br>
                """,
                unsafe_allow_html=True,
            )
            available_syms = SYMPTOMS.get(sp, [])
            cols = st.columns(3)
            for i, sym in enumerate(available_syms):
                col = cols[i % 3]
                is_sel = sym in syms
                with col:
                    btn_label = f"✓ {sym}" if is_sel else sym
                    if st.button(
                        btn_label,
                        key=f"sym_chip_{sym}",
                        type="primary" if is_sel else "secondary",
                        use_container_width=True,
                    ):
                        if sym in syms:
                            syms.remove(sym)
                            # Remove follow-up answers for this symptom
                            prefix = f"{sym}|"
                            keys_to_del = [k for k in ans.keys() if k.startswith(prefix)]
                            for k in keys_to_del:
                                del ans[k]
                        else:
                            syms.append(sym)
                        st.session_state["syms"] = syms
                        st.session_state["ans"] = ans
                        if "q" in st.session_state.get("errors", {}):
                            del st.session_state["errors"]["q"]
                        st.rerun()

        # STEP 3: Follow-up questions
        elif qs == 3:
            st.markdown(
                """
                <h3>A few more questions</h3>
                <p class="m">Based on what you selected.</p>
                """,
                unsafe_allow_html=True,
            )
            q_count = 0
            for s in syms:
                for j, q_text in enumerate(FOLLOW_UPS.get(s, [])):
                    q_count += 1
                    k = f"{s}|{j}"
                    cur_val = ans.get(k, "")
                    st.markdown(
                        f'<div class="q"><b>{q_count}. {q_text}</b></div>',
                        unsafe_allow_html=True,
                    )
                    c1, c2, c3, _ = st.columns([1, 1, 1, 3])
                    for opt, col in zip(["Yes", "No", "Not Sure"], [c1, c2, c3]):
                        with col:
                            is_on = cur_val == opt
                            if st.button(
                                opt,
                                key=f"fu_{k}_{opt}",
                                type="primary" if is_on else "secondary",
                                use_container_width=True,
                            ):
                                ans[k] = opt
                                st.session_state["ans"] = ans
                                if "q" in st.session_state.get("errors", {}):
                                    del st.session_state["errors"]["q"]
                                st.rerun()

        # STEP 4: Timing and severity
        elif qs == 4:
            st.markdown('<h3>Timing and severity</h3>', unsafe_allow_html=True)

            st.markdown('<label>How long has this been going on?</label>', unsafe_allow_html=True)
            dur_opts = ["Choose", "Less than 1 day", "1–3 days", "More than 3 days"]
            curr_d_idx = dur_opts.index(dur) if dur in dur_opts else 0
            sel_dur = st.selectbox(
                "Duration",
                options=dur_opts,
                index=curr_d_idx,
                label_visibility="collapsed",
                key="step4_dur_select",
            )
            if sel_dur != "Choose":
                st.session_state["dur"] = sel_dur
            else:
                st.session_state["dur"] = ""

            st.markdown('<label>How severe does it look?</label>', unsafe_allow_html=True)
            c_s1, c_s2, c_s3, _ = st.columns([1, 1, 1, 3])
            for opt, col in zip(["Mild", "Moderate", "Severe"], [c_s1, c_s2, c_s3]):
                with col:
                    is_on = sev == opt
                    if st.button(
                        opt,
                        key=f"sev_btn_{opt}",
                        type="primary" if is_on else "secondary",
                        use_container_width=True,
                    ):
                        st.session_state["sev"] = opt
                        st.rerun()

            st.markdown('<label>How often does it happen?</label>', unsafe_allow_html=True)
            c_f1, c_f2, c_f3, _ = st.columns([1, 1, 1, 3])
            for opt, col in zip(["Once", "Sometimes", "Often"], [c_f1, c_f2, c_f3]):
                with col:
                    is_on = frq == opt
                    if st.button(
                        opt,
                        key=f"frq_btn_{opt}",
                        type="primary" if is_on else "secondary",
                        use_container_width=True,
                    ):
                        st.session_state["frq"] = opt
                        st.rerun()

        # STEP 5: Emergency check
        elif qs == 5:
            st.markdown(
                """
                <h3>Quick emergency check</h3>
                <p class="m">Please answer all three.</p>
                """,
                unsafe_allow_html=True,
            )
            for i, em_text in enumerate(EMERGENCY_QUESTIONS):
                cur_val = em.get(i, "")
                st.markdown(
                    f'<div class="q"><b>{i + 1}. {em_text}</b></div>',
                    unsafe_allow_html=True,
                )
                c1, c2, c3, _ = st.columns([1, 1, 1, 3])
                for opt, col in zip(["Yes", "No", "Not Sure"], [c1, c2, c3]):
                    with col:
                        is_on = cur_val == opt
                        if st.button(
                            opt,
                            key=f"em_{i}_{opt}",
                            type="primary" if is_on else "secondary",
                            use_container_width=True,
                        ):
                            em[i] = opt
                            st.session_state["em"] = em
                            if "q" in st.session_state.get("errors", {}):
                                del st.session_state["errors"]["q"]
                            st.rerun()

            if any(v == "Yes" for v in em.values()):
                st.markdown(
                    """
                    <div class="alert">
                      🚨 <b>This may be an emergency.</b> Please contact a vet right away. You can still continue to see guidance.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Error message if present
        if err_q:
            st.markdown(f'<div class="err">{err_q}</div>', unsafe_allow_html=True)

    # Navigation buttons
    st.markdown('<div class="nav2">', unsafe_allow_html=True)
    c_prev, _, c_next = st.columns([2, 5, 3])

    with c_prev:
        if st.button("← Previous", key="q_prev_btn", type="secondary", use_container_width=True):
            st.session_state.get("errors", {})["q"] = ""
            if qs == 2:
                navigate_back()
            else:
                st.session_state["qs"] = qs - 1
                st.rerun()

    with c_next:
        btn_label = "Review answers →" if qs == 5 else "Next →"
        if st.button(btn_label, key="q_next_btn", use_container_width=True):
            m = ""
            if qs == 2 and not syms:
                m = "Choose at least one sign to continue."
            elif qs == 3:
                for s in syms:
                    for j in range(len(FOLLOW_UPS.get(s, []))):
                        if not ans.get(f"{s}|{j}"):
                            m = "Please answer every question."
                            break
                    if m:
                        break
            elif qs == 4:
                curr_dur = st.session_state.get("dur", "")
                curr_sev = st.session_state.get("sev", "")
                curr_frq = st.session_state.get("frq", "")
                if not (curr_dur and curr_sev and curr_frq):
                    m = "Please choose duration, severity and frequency."
            elif qs == 5:
                if any(em.get(i) is None for i in [0, 1, 2]):
                    m = "Please answer all three emergency questions."

            if m:
                st.session_state.setdefault("errors", {})["q"] = m
                st.rerun()
            else:
                st.session_state.setdefault("errors", {})["q"] = ""
                if qs == 5:
                    st.session_state["qdone"] = 1
                    navigate_to("review")
                else:
                    st.session_state["qs"] = qs + 1
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Cancel assessment link
    st.markdown('<div style="margin-top: 14px;">', unsafe_allow_html=True)
    if st.button("Cancel assessment", key="cancel_assessment_btn", type="secondary"):
        def do_cancel():
            reset_assessment()
            navigate_to("home")

        show_confirm_dialog(
            "Cancel this assessment? Your answers will be cleared.",
            do_cancel,
        )
    st.markdown('</div>', unsafe_allow_html=True)
