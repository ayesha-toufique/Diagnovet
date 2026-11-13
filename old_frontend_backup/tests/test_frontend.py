"""Automated Consistency & Quality Audit Tests for Diagnovet Frontend."""

import re
from pathlib import Path
from services.mock_repository import DiagnovetRepository
from components.theme import (
    COLOR_EMERGENCY,
    COLOR_WARNING,
    COLOR_ACCENT,
    COLOR_SUCCESS,
    get_decision_color,
    get_decision_badge_class,
    safe_html,
)

VIEWS_DIR = Path("D:/Diagnovet/views")
COMPONENTS_DIR = Path("D:/Diagnovet/components")


def test_repository_initialization():
    """Verify mock repository loads all required demo entities."""
    repo = DiagnovetRepository()
    pets = repo.get_all_pets()
    assert len(pets) >= 3, "Should have at least 3 initial demo pets"
    categories = repo.get_health_categories()
    assert len(categories) == 9, "Should support all 9 health categories"
    history = repo.get_consultation_history()
    assert len(history) >= 4, "Should have initial consultation history records"


def test_diagnosis_and_decision_mock_data():
    """Verify mock diagnosis and decision interfaces produce valid schemas."""
    repo = DiagnovetRepository()
    diag = repo.get_diagnosis()
    assert "top_conditions" in diag
    assert len(diag["top_conditions"]) >= 2
    assert "supporting_symptoms" in diag["top_conditions"][0]
    assert "missing_symptoms" in diag["top_conditions"][0]

    dec = repo.get_decision()
    assert "decision" in dec
    assert "why_selected" in dec
    assert "alternatives_considered" in dec
    assert "rules_influenced" in dec

    dss = repo.get_dss_report()
    assert "condition_comparison" in dss
    assert "criteria_weights" in dss


def test_decision_colors_and_badges():
    """Verify that all 4 decision outcomes map to their exact theme tokens and classes."""
    assert get_decision_color("Get Help Now") == COLOR_EMERGENCY
    assert get_decision_color("Visit Vet Today") == COLOR_WARNING
    assert get_decision_color("Book a Vet Visit") == COLOR_ACCENT
    assert get_decision_color("Home Care & Monitor") == COLOR_SUCCESS

    assert get_decision_badge_class("Get Help Now") == "red"
    assert get_decision_badge_class("Visit Vet Today") == "amb"
    assert get_decision_badge_class("Book a Vet Visit") == "blu"
    assert get_decision_badge_class("Home Care & Monitor") == "grn"


def test_all_10_views_call_header_and_footer():
    """Consistency Audit: Ensure all 10 view modules call render_header and render_footer."""
    view_files = list(VIEWS_DIR.glob("*.py"))
    assert (
        len(view_files) == 10
    ), f"Expected 10 view modules in {VIEWS_DIR}, found {len(view_files)}"

    for vf in view_files:
        content = vf.read_text(encoding="utf-8")
        assert (
            "render_header(" in content
        ), f"{vf.name} is missing call to render_header"
        assert (
            "render_footer(" in content
        ), f"{vf.name} is missing call to render_footer"


def test_no_hardcoded_hex_colors_in_views():
    """Consistency Audit: Strict design system check ensuring no raw hex colors are in views/*.py."""
    hex_pattern = re.compile(r"#[0-9a-fA-F]{3,6}\b")
    violations = []

    for vf in VIEWS_DIR.glob("*.py"):
        content = vf.read_text(encoding="utf-8")
        matches = hex_pattern.findall(content)
        if matches:
            violations.append(f"{vf.name}: {matches}")

    assert (
        not violations
    ), f"Raw hex color violation in view files (must use CSS classes/theme tokens): {violations}"


def test_mandatory_demo_labels_present():
    """Audit: Ensure mandatory demo labels exist in results, decision making, and DSS views matching diagnovet.html."""
    diag_file = (VIEWS_DIR / "diagnosis_results.py").read_text(encoding="utf-8")
    dec_file = (VIEWS_DIR / "decision_making.py").read_text(encoding="utf-8")
    dss_file = (VIEWS_DIR / "decision_support.py").read_text(encoding="utf-8")

    assert "DEMO RESULT — NOT A REAL VETERINARY DIAGNOSIS" in diag_file
    assert "DEMO DECISION — BACKEND DECISION ENGINE NOT CONNECTED" in dec_file
    assert "DEMONSTRATION DATA ONLY" in dss_file


def test_no_unwanted_phase_1_prototyping_text():
    """Audit: Ensure no unwanted 'Phase 1 Prototyping' text appears in views or components."""
    prohibited = ["Phase 1 Prototyping", "Phase 1 Prototype"]
    violations = []

    for path in list(VIEWS_DIR.glob("*.py")) + list(COMPONENTS_DIR.glob("*.py")):
        content = path.read_text(encoding="utf-8")
        for p in prohibited:
            if p in content:
                violations.append(f"{path.name} contains '{p}'")

    assert not violations, f"Found unwanted prototype labels: {violations}"


def test_safe_html_strips_indentation():
    """Verify safe_html removes all leading indentation so markdown never generates code blocks."""
    test_input = """
        <div class="card">
            <p>Some text</p>
        </div>
    """
    cleaned = safe_html(test_input)
    for line in cleaned.splitlines():
        assert not line.startswith(
            "    "
        ), f"Line still has 4+ spaces indentation: {line}"
