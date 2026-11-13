"""Layout components for Diagnovet matching design_reference/diagnovet_flow.html.

Includes sidebar, top bar, back button, theme switcher, footer, and confirmation dialogs.
"""
from typing import Callable
from pathlib import Path
import streamlit as st

NAV_ITEMS = [
    ("home", "🏠", "Home"),
    ("pet", "🐾", "Pet Information"),
    ("q", "🩺", "Assessment"),
    ("review", "📝", "Review Answers"),
    ("cond", "🧪", "Possible Conditions"),
    ("care", "⚖️", "Care Guidance"),
    ("support", "📊", "Decision Support"),
    ("summary", "📄", "Final Summary"),
    ("safety", "🛡️", "Safety"),
]


def init_session():
    """Initializes session state keys matching Section 8."""
    defaults = {
        "page": "home",
        "history": [],
        "theme": "lagoon",
        "sp": "",
        "breed": "",
        "age": "",
        "gen": "",
        "wt": "",
        "bg": "",
        "syms": [],
        "ans": {},
        "dur": "",
        "sev": "",
        "frq": "",
        "em": {},
        "qs": 2,
        "qdone": 0,
        "sub": 0,
        "errors": {},
        "confirm_action": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_assessment():
    """Restores all assessment-specific keys while preserving selected theme."""
    current_theme = st.session_state.get("theme", "lagoon")
    st.session_state["page"] = "home"
    st.session_state["history"] = []
    st.session_state["sp"] = ""
    st.session_state["breed"] = ""
    st.session_state["age"] = ""
    st.session_state["gen"] = ""
    st.session_state["wt"] = ""
    st.session_state["bg"] = ""
    st.session_state["syms"] = []
    st.session_state["ans"] = {}
    st.session_state["dur"] = ""
    st.session_state["sev"] = ""
    st.session_state["frq"] = ""
    st.session_state["em"] = {}
    st.session_state["qs"] = 2
    st.session_state["qdone"] = 0
    st.session_state["sub"] = 0
    st.session_state["errors"] = {}
    st.session_state["theme"] = current_theme


def is_pet_valid() -> bool:
    """Pet Information is valid when Species, Breed, Gender, and valid Age (0-30) are chosen."""
    sp = st.session_state.get("sp", "")
    breed = st.session_state.get("breed", "")
    gen = st.session_state.get("gen", "")
    age = str(st.session_state.get("age", "")).strip()

    if not sp or not breed or not gen or age == "":
        return False
    try:
        val = float(age)
        return 0 <= val <= 30
    except ValueError:
        return False


def is_unlocked(page_id: str) -> bool:
    """Determines if a page is unlocked per Section 4 unlock rules."""
    if page_id in ["home", "pet", "safety"]:
        return True
    if page_id == "q":
        return is_pet_valid()
    if page_id == "review":
        return bool(st.session_state.get("qdone", 0))
    if page_id in ["cond", "care", "support", "summary"]:
        return bool(st.session_state.get("sub", 0))
    return False


def navigate_to(page_id: str, is_back: bool = False):
    """Navigates to the given page if unlocked; otherwise shows toast."""
    if not is_unlocked(page_id):
        st.toast("Please finish the earlier steps first")
        return

    cur = st.session_state.get("page", "home")
    if not is_back and page_id != cur:
        st.session_state["history"].append(cur)

    st.session_state["page"] = page_id
    st.rerun()


def navigate_back():
    """Pops the history stack and navigates to the previous page."""
    hist = st.session_state.get("history", [])
    if hist:
        prev_page = hist.pop()
        st.session_state["page"] = prev_page
        st.rerun()
    else:
        st.session_state["page"] = "home"
        st.rerun()


@st.dialog("Are you sure?")
def show_confirm_dialog(message: str, on_confirm: Callable[[], None]):
    """Shared confirmation dialog matching Section 6.10."""
    st.markdown(f'<p class="m">{message}</p>', unsafe_allow_html=True)
    st.markdown('<div class="nav2">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Cancel", key="dlg_btn_cancel", type="secondary", use_container_width=True):
            st.rerun()
    with c2:
        if st.button("Yes, continue", key="dlg_btn_yes", use_container_width=True):
            on_confirm()
    st.markdown('</div>', unsafe_allow_html=True)


def inject_custom_styles():
    """Injects assets/styles.css and dynamic CSS variables matching the active theme."""
    theme = st.session_state.get("theme", "lagoon")
    css_path = Path(__file__).resolve().parent.parent / "assets" / "styles.css"
    css_content = ""
    if css_path.exists():
        css_content = css_path.read_text(encoding="utf-8")

    if theme == "aurora":
        theme_vars = """
:root {
  --bg: #0F0B24;
  --card: #1A1438;
  --text: #F2EEFF;
  --muted: #A59CC9;
  --line: #2D2557;
  --g: linear-gradient(135deg, #00E5C3, #7B5CFF 55%, #FF5FA2);
  --a: #7B5CFF;
  --glow: 0 8px 30px #7b5cff55;
}
.st-key-theme_dot_aurora button { outline: 2px solid var(--a) !important; }
.st-key-theme_dot_lagoon button { outline: 2px solid var(--line) !important; }
header[data-testid="stHeader"] { background: var(--bg) !important; }
"""
    else:
        theme_vars = """
:root {
  --bg: #E8FAF6;
  --card: #FFFFFF;
  --text: #0B2F3A;
  --muted: #5C8089;
  --line: #CBEBE4;
  --g: linear-gradient(135deg, #00C9A7, #2E7DFF 55%, #8A5CFF);
  --a: #2E7DFF;
  --glow: 0 8px 26px #2e7dff40;
}
.st-key-theme_dot_lagoon button { outline: 2px solid var(--a) !important; }
.st-key-theme_dot_aurora button { outline: 2px solid var(--line) !important; }
header[data-testid="stHeader"] { background: var(--bg) !important; }
"""

    st.markdown(f"<style>\n{css_content}\n{theme_vars}\n</style>", unsafe_allow_html=True)


def render_top_bar():
    """Renders top bar with back button or Diagnovet label on left, and theme dots on right."""
    inject_custom_styles()
    cur_page = st.session_state.get("page", "home")

    c_left, c_right = st.columns([4, 2])

    with c_left:
        if cur_page == "home":
            st.markdown('<div style="padding-top: 6px;"><b class="m" style="font-size: 16px;">Diagnovet</b></div>', unsafe_allow_html=True)
        else:
            if st.button("←", key="top_back_btn", type="secondary", help="Back"):
                navigate_back()

    with c_right:
        # Theme switcher dots matching diagnovet.html
        col_t_label, col_t_aurora, col_t_lagoon = st.columns([2, 1, 1])
        with col_t_label:
            st.markdown('<div style="text-align: right; font-size: 12px; color: var(--muted); padding-top: 10px;">Theme</div>', unsafe_allow_html=True)
        with col_t_aurora:
            if st.button("●", key="theme_dot_aurora", help="Aurora theme", use_container_width=True):
                st.session_state["theme"] = "aurora"
                st.rerun()
        with col_t_lagoon:
            if st.button("●", key="theme_dot_lagoon", help="Lagoon theme", use_container_width=True):
                st.session_state["theme"] = "lagoon"
                st.rerun()


def render_sidebar():
    """Renders the 240px sidebar with logo, navigation items, and restart button."""
    with st.sidebar:
        # Logo tile + wordmark Diagnovet
        st.markdown(
            """
            <div class="logo">
              <i>🐾</i><b>Diagnovet</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

        cur_page = st.session_state.get("page", "home")

        # 9 Nav items in exact order
        for p_id, icon, label in NAV_ITEMS:
            unlocked = is_unlocked(p_id)
            is_active = cur_page == p_id
            lock_suffix = "" if unlocked else " 🔒"
            btn_label = f"{icon}  {label}{lock_suffix}"

            if st.button(
                btn_label,
                key=f"sb_nav_{p_id}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                disabled=False,
            ):
                if unlocked:
                    navigate_to(p_id)
                else:
                    st.toast("Please finish the earlier steps first")

        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

        # Restart button at bottom of sidebar
        if st.button("↺ Restart assessment", key="sb_restart_btn", type="secondary", use_container_width=True):
            def do_restart():
                reset_assessment()
                st.session_state["page"] = "pet"
                st.rerun()

            show_confirm_dialog(
                "Restart this assessment? Your current answers will be cleared.",
                do_restart,
            )


def render_footer():
    """Renders exact footer text matching Section 5 & reference."""
    st.markdown(
        """
        <footer>
          © Diagnovet — a decision-support tool, not a replacement for a qualified veterinarian. Nothing is saved after you close the assessment.
        </footer>
        """,
        unsafe_allow_html=True,
    )
