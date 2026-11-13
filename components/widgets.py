"""Reusable UI widgets for Diagnovet matching design_reference/diagnovet_flow.html."""
import textwrap
import streamlit as st


def render_html(content: str):
    """Safely renders multiline HTML by stripping any leading indentation.
    Strips common leading indentation and line-by-line whitespace to ensure
    Markdown never misinterprets indented lines as <pre><code> blocks.
    """
    clean_html = textwrap.dedent(content).strip()
    clean_html = "\n".join(line.strip() for line in clean_html.splitlines() if line.strip())
    st.markdown(clean_html, unsafe_allow_html=True)


def render_head(title: str, subtitle: str = ""):
    """Renders page header with pt title and m subtitle."""
    sub_html = f'<p class="m">{subtitle}</p>' if subtitle else ""
    render_html(
        f"""
        <div class="pt">{title}</div>
        {sub_html}
        """
    )


def render_prog(step_num: int):
    """Renders Step n of 6 with 6 bar segments."""
    spans = "".join(
        [
            f'<span class="{"on" if i <= step_num else ""}"></span>'
            for i in range(1, 7)
        ]
    )
    render_html(
        f"""
        <div class="m" style="margin-top: 14px;"><b>Step {step_num} of 6</b></div>
        <div class="steps">
          {spans}
        </div>
        """
    )


def render_demo_badge():
    """Renders the exact demo badge from the reference."""
    render_html('<span class="demo">SAMPLE PREVIEW — DESIGN DEMO ONLY</span>')


def render_alert(html_content: str):
    """Renders alert block."""
    render_html(f'<div class="alert">{html_content}</div>')


def render_bar(percentage: int):
    """Renders progress bar matching reference."""
    pct = min(100, max(0, percentage))
    render_html(f'<div class="bar"><i style="width:{pct}%;"></i></div>')


def render_badge(text: str, tone: str = "blu") -> str:
    """Returns HTML for badge: red, amb, grn, blu."""
    return f'<span class="badge {tone}">{text}</span>'


def render_kv(label: str, value: str) -> str:
    """Returns HTML for key-value row."""
    return f'<div class="kv"><span>{label}</span><b>{value}</b></div>'

