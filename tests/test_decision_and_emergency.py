"""Test decision calculation, severity mapping, and emergency override."""
from services.mock_repository import calculate_results


def test_emergency_override_forces_get_help_now():
    """Verify that any Yes in emergency signs overrides severity to Get Help Now."""
    state = {
        "syms": ["Vomiting"],
        "ans": {"Vomiting|0": "No", "Vomiting|1": "No"},
        "em": {0: "Yes", 1: "No", 2: "No"},
        "sev": "Mild",  # Even with mild severity, emergency forces critical
    }
    r = calculate_results(state)
    assert r["emergency"] is True
    assert r["decision_index"] == 0
    assert r["decision"]["name"] == "Get Help Now"
    assert r["decision"]["level"] == "Critical"
    assert r["decision"]["tone"] == "red"


def test_severity_tier_mapping_without_emergency():
    """Verify severity maps to correct 4-tier decision when no emergency signs."""
    # 1. Severe -> Visit Vet Today
    r1 = calculate_results({"syms": ["Diarrhoea"], "ans": {}, "em": {0: "No", 1: "No", 2: "No"}, "sev": "Severe"})
    assert r1["decision_index"] == 1
    assert r1["decision"]["name"] == "Visit Vet Today"

    # 2. Moderate -> Book a Vet Visit
    r2 = calculate_results({"syms": ["Diarrhoea"], "ans": {}, "em": {0: "No", 1: "No", 2: "No"}, "sev": "Moderate"})
    assert r2["decision_index"] == 2
    assert r2["decision"]["name"] == "Book a Vet Visit"

    # 3. Mild -> Home Care & Monitor
    r3 = calculate_results({"syms": ["Diarrhoea"], "ans": {}, "em": {0: "No", 1: "No", 2: "No"}, "sev": "Mild"})
    assert r3["decision_index"] == 3
    assert r3["decision"]["name"] == "Home Care & Monitor"


def test_evidence_and_scoring():
    """Verify concordance scores, supporting and unconfirmed evidence accumulation."""
    state = {
        "sp": "Dog",
        "syms": ["Vomiting", "Itching"],
        "ans": {
            "Vomiting|0": "Yes",
            "Vomiting|1": "Not Sure",
            "Itching|0": "No",
        },
        "em": {0: "No", 1: "No", 2: "No"},
        "sev": "Moderate",
    }
    r = calculate_results(state)
    assert len(r["conditions"]) == 3
    # Top condition match score is within valid bounds (clamped at 92 max)
    assert 0 < r["scores"][0] <= 92
    assert r["scores"][0] >= r["scores"][1] >= r["scores"][2]
    # Supporting includes selected symptoms
    assert "Vomiting" in r["supporting"]
    assert "Itching" in r["supporting"]
    # Table rows check
    assert len(r["table_rows"]) == 3
