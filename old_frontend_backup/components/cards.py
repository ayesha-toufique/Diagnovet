"""Reusable Card and Presentation Components for Diagnovet matching diagnovet.html."""

from typing import Dict, Any
from components.theme import get_decision_badge_class, render_html


def render_demo_badge(
    label_text: str = "DEMO RESULT — NOT A REAL VETERINARY DIAGNOSIS",
):
    """Renders the required high-visibility diagonal red-striped demo badge."""
    html = f"""
    <div style="display: flex; justify-content: flex-start; margin-bottom: 16px;">
      <span class="demo">⚠️ {label_text}</span>
    </div>
    """
    render_html(html)


def render_emergency_alert(message: str, title: str = "Emergency?"):
    """Renders high-visibility safety alert for urgent clinical situations matching diagnovet.html."""
    html = f"""
    <div class="alert">
      🚨 <b>{title}</b> {message}
    </div>
    """
    render_html(html)


def render_hero(
    title: str,
    subtitle: str,
    badge_text: str = "✨ Veterinary Decision Support",
):
    """Renders the top gradient hero section with watermark matching diagnovet.html."""
    html = f"""
    <div class="hero">
      <span class="badge" style="background: rgba(255,255,255,0.22); margin-bottom: 14px;">{badge_text}</span>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </div>
    """
    render_html(html)


def render_feature_card(icon: str, title: str, description: str):
    """Renders a feature card with icon tile matching diagnovet.html."""
    html = f"""
    <div class="card h" style="height: 100%;">
      <div class="ico">{icon}</div>
      <h3>{title}</h3>
      <p class="m">{description}</p>
    </div>
    """
    render_html(html)


def render_pet_card(pet: Dict[str, Any], is_selected: bool = False):
    """Renders a clean, responsive pet profile card with zero raw HTML leaks matching diagnovet.html."""
    icon = "🐱" if pet.get("species") == "Cat" else "🐶"
    selected_cls = "sel" if is_selected else ""
    badge_html = (
        '<span class="badge grn" style="margin-left: auto;">Selected</span>'
        if is_selected
        else ""
    )
    gender_short = pet.get("gender", "—").split()[0]

    html = f"""
    <div class="card h {selected_cls}" style="margin-bottom: 12px; width: 100%;">
      <div style="display: flex; gap: 14px; align-items: center; justify-content: space-between;">
        <div style="display: flex; gap: 14px; align-items: center;">
          <div class="ico" style="margin: 0; flex-shrink: 0;">{icon}</div>
          <div>
            <h3 style="margin: 0 0 2px 0;">{pet.get('name', 'Pet')}</h3>
            <p class="m" style="margin: 0;">
              {pet.get('breed', '—')} &bull; {pet.get('species', 'Pet')} &bull; {gender_short}
            </p>
            <p class="m" style="margin: 2px 0 0 0; font-size: 12px;">
              <b>{pet.get('age', '?')}</b> yrs &bull; <b>{pet.get('weight', '?')}</b> kg
            </p>
          </div>
        </div>
        {badge_html}
      </div>
    </div>
    """
    render_html(html)


def render_decision_card(
    outcome_title: str,
    priority_level: str,
    description: str,
    is_active: bool = False,
):
    """Renders an outcome card for the 4 core decisions matching diagnovet.html."""
    badge_cls = get_decision_badge_class(outcome_title)
    selected_cls = "sel" if is_active else ""
    icon_map = {
        "Get Help Now": "🚨",
        "Visit Vet Today": "🏥",
        "Book a Vet Visit": "📅",
        "Home Care & Monitor": "🏡",
    }
    ico = icon_map.get(outcome_title, "🩺")

    html = f"""
    <div class="card h {selected_cls}" style="height: 100%;">
      <div class="ico">{ico}</div>
      <h3>{outcome_title}</h3>
      <span class="badge {badge_cls}" style="margin-bottom: 8px;">{priority_level}</span>
      <p class="m" style="margin-top: 6px;">{description}</p>
    </div>
    """
    render_html(html)
