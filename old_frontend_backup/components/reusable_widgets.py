"""Reusable interactive widgets and progress indicators for Diagnovet matching diagnovet.html."""

from typing import List
from components.theme import get_decision_badge_class, render_html


def render_stepper(step_names: List[str], current_index: int):
    """Renders a 5-step progress indicator matching diagnovet.html."""
    total_steps = len(step_names)
    pct = int(((current_index + 1) / total_steps) * 100)

    spans = "".join(
        [
            f'<span class="{"on" if i <= current_index else ""}"></span>'
            for i in range(total_steps)
        ]
    )

    html = f"""
    <div style="margin-bottom: 20px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <span style="font-size: 13px; font-weight: 700; color: var(--a); text-transform: uppercase;">
          Step {current_index + 1} of {total_steps} &mdash; {step_names[current_index]}
        </span>
        <span class="m" style="font-size: 12.5px; font-weight: 600;">{pct}% Completed</span>
      </div>
      <div class="steps">
        {spans}
      </div>
    </div>
    """
    render_html(html)


def render_progress_bar(percentage: int, label: str = ""):
    """Renders a themed progress bar matching diagnovet.html."""
    pct = min(100, max(0, percentage))
    html = f"""
    <div style="margin-bottom: 10px;">
      {f'<div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px;"><span>{label}</span><b>{pct}%</b></div>' if label else ''}
      <div class="bar">
        <i style="width: {pct}%;"></i>
      </div>
    </div>
    """
    render_html(html)


def render_status_badge(level: str) -> str:
    """Returns HTML for a status badge corresponding to clinical priority."""
    badge_cls = get_decision_badge_class(level)
    return f'<span class="badge {badge_cls}">{level}</span>'
