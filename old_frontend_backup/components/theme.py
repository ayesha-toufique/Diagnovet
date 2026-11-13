"""Theme tokens and styling helpers for Diagnovet.

Mirrors the CSS variables defined in assets/styles.css and diagnovet.html.
Single source of truth for all Python-level styling, Plotly colors, and theme switching.
"""

from pathlib import Path
import streamlit as st

# Color Tokens - Lagoon Theme (Default Light)
LAGOON_BG = "#E8FAF6"
LAGOON_CARD = "#FFFFFF"
LAGOON_TEXT = "#0B2F3A"
LAGOON_MUTED = "#5C8089"
LAGOON_LINE = "#CBEBE4"
LAGOON_ACCENT = "#2E7DFF"
LAGOON_GRADIENT = "linear-gradient(135deg, #00C9A7, #2E7DFF 55%, #8A5CFF)"
LAGOON_GLOW = "0 8px 26px rgba(46, 125, 255, 0.25)"

# Color Tokens - Aurora Theme (Dark Mode)
AURORA_BG = "#0F0B24"
AURORA_CARD = "#1A1438"
AURORA_TEXT = "#F2EEFF"
AURORA_MUTED = "#A59CC9"
AURORA_LINE = "#2D2557"
AURORA_ACCENT = "#7B5CFF"
AURORA_GRADIENT = "linear-gradient(135deg, #00E5C3, #7B5CFF 55%, #FF5FA2)"
AURORA_GLOW = "0 8px 30px rgba(123, 92, 255, 0.33)"

# Status & Decision Colors (Universal across both themes)
COLOR_EMERGENCY = "#E5484D"  # Critical / Get Help Now
COLOR_WARNING = "#E69B28"  # High / Visit Vet Today
COLOR_ACCENT = "#2E7DFF"  # Medium / Book a Vet Visit
COLOR_SUCCESS = "#27966F"  # Low / Home Care & Monitor

# Plotly Colorway
PLOTLY_COLORWAY = [
    "#00C9A7",  # Mint
    "#2E7DFF",  # Blue
    "#8A5CFF",  # Violet
    "#E69B28",  # Amber
    "#E5484D",  # Coral / Emergency
]

# Aurora Theme Complete Override CSS
AURORA_CSS_OVERRIDE = """
<style>
:root {
  --bg: #0F0B24;
  --card: #1A1438;
  --text: #F2EEFF;
  --muted: #A59CC9;
  --line: #2D2557;
  --accent: #7B5CFF;
  --a: #7B5CFF;
  --grad: linear-gradient(135deg, #00E5C3, #7B5CFF 55%, #FF5FA2);
  --g: linear-gradient(135deg, #00E5C3, #7B5CFF 55%, #FF5FA2);
  --glow: 0 8px 30px rgba(123, 92, 255, 0.33);
  --blu: #7B5CFF;
}

html, body, .stApp, [data-testid="stAppViewContainer"], section.main,
header[data-testid="stHeader"], [data-testid="stHeader"], [data-testid="stToolbar"] {
  background: #0F0B24 !important;
  color: #F2EEFF !important;
}

header[data-testid="stHeader"] {
  background: #0F0B24 !important;
  border-bottom: 1px solid #2D2557 !important;
}

[data-testid="stSidebar"], [data-testid="stSidebarContent"], section[data-testid="stSidebar"] {
  background: #1A1438 !important;
  border-right: 1px solid #2D2557 !important;
}

.card, .dv-card, .dv-card-static {
  background: #1A1438 !important;
  border-color: #2D2557 !important;
  color: #F2EEFF !important;
}

.chip {
  background: #1A1438 !important;
  border-color: #2D2557 !important;
  color: #F2EEFF !important;
}

.chip:hover {
  border-color: #7B5CFF !important;
}

.seg {
  border-color: #2D2557 !important;
  background: #1A1438 !important;
}

.seg button {
  color: #A59CC9 !important;
}

.steps span {
  background: #2D2557 !important;
}

div[role="radiogroup"] > label {
  background: #1A1438 !important;
  border-color: #2D2557 !important;
  color: #F2EEFF !important;
}

.stTextInput input, .stNumberInput input, .stTextArea textarea,
.stSelectbox > div > div, .stMultiSelect > div > div {
  background: #1A1438 !important;
  border-color: #2D2557 !important;
  color: #F2EEFF !important;
}

[data-testid="stExpander"] {
  background: #1A1438 !important;
  border-color: #2D2557 !important;
  color: #F2EEFF !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
  color: #F2EEFF !important;
}

table, tr, td, th {
  color: #F2EEFF !important;
  border-color: #2D2557 !important;
}

th {
  color: #A59CC9 !important;
}

.dv-footer, footer {
  border-color: #2D2557 !important;
  color: #A59CC9 !important;
}

.dv-btn-secondary > button {
  border-color: #2D2557 !important;
  color: #F2EEFF !important;
}
</style>
"""


def safe_html(html_str: str) -> str:
    """Strips all leading and trailing whitespace from every line.

    This prevents CommonMark markdown parsers from misinterpreting indented HTML
    as preformatted code blocks.
    """
    return "\n".join(line.strip() for line in html_str.strip().splitlines())


def render_html(html_str: str):
    """Renders HTML safely via st.markdown with zero risk of markdown code block bugs."""
    st.markdown(safe_html(html_str), unsafe_allow_html=True)


def get_decision_color(outcome_name: str) -> str:
    """Return the designated theme color for a 4-level decision outcome."""
    mapping = {
        "Get Help Now": COLOR_EMERGENCY,
        "Visit Vet Today": COLOR_WARNING,
        "Book a Vet Visit": COLOR_ACCENT,
        "Home Care & Monitor": COLOR_SUCCESS,
        "Critical": COLOR_EMERGENCY,
        "High": COLOR_WARNING,
        "Medium": COLOR_ACCENT,
        "Low": COLOR_SUCCESS,
    }
    return mapping.get(outcome_name, COLOR_ACCENT)


def get_decision_badge_class(outcome_name: str) -> str:
    """Return the CSS class for badge rendering matching diagnovet.html."""
    mapping = {
        "Get Help Now": "red",
        "Visit Vet Today": "amb",
        "Book a Vet Visit": "blu",
        "Home Care & Monitor": "grn",
        "Critical": "red",
        "High": "amb",
        "Medium": "blu",
        "Low": "grn",
    }
    return mapping.get(outcome_name, "blu")


def inject_custom_styles():
    """Load base CSS and apply theme overrides."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Lagoon"

    css_path = Path("D:/Diagnovet/assets/styles.css")
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            base_css = f"<style>\n{f.read()}\n</style>"
            st.markdown(base_css, unsafe_allow_html=True)

    if st.session_state["theme"] == "Aurora":
        st.markdown(AURORA_CSS_OVERRIDE, unsafe_allow_html=True)
