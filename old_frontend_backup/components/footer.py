"""Shared Footer Component for Diagnovet."""

from components.theme import render_html


def render_footer():
    """Renders the standard footer across all pages matching diagnovet.html."""
    html = """
    <footer class="dv-footer">
      <div style="display: flex; justify-content: center; align-items: center; gap: 8px; margin-bottom: 6px;">
        <span style="font-size: 15px;">🐾</span>
        <strong style="color: var(--text);">Diagnovet</strong>
        <span style="color: var(--muted);">&mdash; Smart Pet Health Diagnosis & Decision Support System</span>
      </div>
      <p style="margin: 4px 0 0 0; color: var(--muted); font-size: 12.5px;">
        &copy; Diagnovet &mdash; a decision-support tool, not a replacement for a qualified veterinarian.
      </p>
    </footer>
    """
    render_html(html)
