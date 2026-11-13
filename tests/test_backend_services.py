"""Unit tests for Diagnovet backend services."""
import pytest
from backend.models.assessment import AssessmentInput, PetProfile
from backend.services.emergency_detection import EmergencyDetectionService
from backend.services.decision_making import DecisionMakingSystem
from backend.services.decision_support import DecisionSupportService
from backend.services.care_guidance import CareGuidanceService
from backend.services.assessment_service import AssessmentService
from backend.knowledge_base.knowledge_base_loader import get_knowledge_base


@pytest.fixture(scope="module")
def emergency_service():
    return EmergencyDetectionService()


@pytest.fixture(scope="module")
def decision_system():
    return DecisionMakingSystem()


@pytest.fixture(scope="module")
def dss_service():
    return DecisionSupportService()


@pytest.fixture(scope="module")
def care_service():
    return CareGuidanceService()


@pytest.fixture(scope="module")
def assessment_service():
    return AssessmentService()


def test_emergency_detection_user_checklist(emergency_service):
    """Verify emergency detected when user checks any emergency question as Yes."""
    assessment = AssessmentInput(
        pet=PetProfile(species="Dog", breed="Beagle", age=2.0, weight=10.0, gender="Female"),
        symptoms=["Vomiting"],
        answers={},
        duration="Under 24 hours",
        severity="Mild",
        frequency="Once or twice",
        emergency_answers={0: "Yes", 1: "No", 2: "No"},
    )
    detected, reasons = emergency_service.evaluate(assessment)
    assert detected is True
    assert len(reasons) > 0


def test_emergency_detection_feline_urinary_blockage(emergency_service):
    """Verify male cat straining to urinate triggers emergency red flag."""
    assessment = AssessmentInput(
        pet=PetProfile(species="Cat", breed="DSH", age=4.0, weight=4.5, gender="Male"),
        symptoms=["Straining to Urinate"],
        answers={},
        duration="Under 24 hours",
        severity="Severe",
        frequency="Constantly",
        emergency_answers={0: "No", 1: "No", 2: "No"},
    )
    detected, reasons = emergency_service.evaluate(assessment)
    assert detected is True
    assert any("urinary obstruction" in r.lower() for r in reasons)


def test_decision_making_emergency_override(decision_system):
    """Verify emergency detection overrides mild severity to Tier 0: Get Help Now."""
    assessment = AssessmentInput(
        pet=PetProfile(species="Dog", breed="Labrador", age=5.0, weight=30.0, gender="Male"),
        symptoms=["Lethargy"],
        answers={},
        duration="Under 24 hours",
        severity="Mild",
        frequency="Once or twice",
        emergency_answers={0: "Yes", 1: "No", 2: "No"},
    )
    idx, outcome = decision_system.evaluate(
        assessment=assessment,
        emergency_detected=True,
        emergency_reasons=["Severe difficulty breathing reported."],
    )
    assert idx == 0
    assert outcome.name == "Get Help Now"
    assert outcome.level == "Critical"
    assert outcome.tone == "red"
    assert "emergency" in outcome.rationale.lower()


def test_decision_making_severity_mapping(decision_system):
    """Verify severity mapping without emergency."""
    # 1. Severe
    a_severe = AssessmentInput(
        pet=PetProfile(species="Dog", breed="Pug", age=3.0, weight=8.0, gender="Male"),
        symptoms=["Vomiting"],
        answers={},
        duration="1-3 days",
        severity="Severe",
        frequency="Often",
        emergency_answers={0: "No", 1: "No", 2: "No"},
    )
    idx_s, out_s = decision_system.evaluate(a_severe, emergency_detected=False, emergency_reasons=[])
    assert idx_s == 1
    assert out_s.name == "Visit Vet Today"

    # 2. Moderate
    a_mod = AssessmentInput(
        pet=PetProfile(species="Dog", breed="Pug", age=3.0, weight=8.0, gender="Male"),
        symptoms=["Vomiting"],
        answers={},
        duration="1-3 days",
        severity="Moderate",
        frequency="Often",
        emergency_answers={0: "No", 1: "No", 2: "No"},
    )
    idx_m, out_m = decision_system.evaluate(a_mod, emergency_detected=False, emergency_reasons=[])
    assert idx_m == 2
    assert out_m.name == "Book a Vet Visit"

    # 3. Mild
    a_mild = AssessmentInput(
        pet=PetProfile(species="Dog", breed="Pug", age=3.0, weight=8.0, gender="Male"),
        symptoms=["Vomiting"],
        answers={},
        duration="Under 24 hours",
        severity="Mild",
        frequency="Once or twice",
        emergency_answers={0: "No", 1: "No", 2: "No"},
    )
    idx_l, out_l = decision_system.evaluate(a_mild, emergency_detected=False, emergency_reasons=[])
    assert idx_l == 3
    assert out_l.name == "Home Care & Monitor"


def test_care_guidance_critical_actions_and_checklist(care_service, decision_system):
    """Verify care guidance includes clinical checklist and warning against human NSAIDs."""
    kb = get_knowledge_base()
    cond = kb.get_condition_by_id("DOG_001")
    from backend.models.condition import EvidenceMatch
    match = EvidenceMatch(
        condition=cond,
        match_score=75,
        supporting_evidence=["Vomiting"],
        contradictory_evidence=[],
        missing_evidence=["Blood in vomit"],
    )

    assessment = AssessmentInput(
        pet=PetProfile(species="Dog", breed="German Shepherd", age=4.0, weight=30.0, gender="Male"),
        symptoms=["Vomiting"],
        answers={},
        duration="1-3 days",
        severity="Moderate",
        frequency="Often",
        emergency_answers={0: "No", 1: "No", 2: "No"},
    )
    _, decision = decision_system.evaluate(assessment, emergency_detected=False, emergency_reasons=[])
    guidance = care_service.generate_guidance(decision, primary_match=match, emergency_detected=False)

    assert "preparation_checklist" in guidance
    assert len(guidance["preparation_checklist"]) >= 3
    assert "unsafe_actions" in guidance
    # Must warn against human medication (ibuprofen/paracetamol/NSAIDs)
    assert any("human" in a.lower() or "ibuprofen" in a.lower() for a in guidance["unsafe_actions"])


def test_assessment_service_full_pipeline(assessment_service):
    """Verify end-to-end AssessmentService and calculate_results_dict adapter."""
    session_state = {
        "sp": "Cat",
        "breed": "Siamese",
        "age": 2.5,
        "wt": 3.8,
        "gen": "Female",
        "syms": ["Vomiting", "Lethargy"],
        "ans": {"Vomiting|0": "Yes"},
        "dur": "1-3 days",
        "sev": "Moderate",
        "frq": "Often",
        "em": {0: "No", 1: "No", 2: "No"},
    }

    results = assessment_service.calculate_results_dict(session_state)
    assert "conditions" in results
    assert len(results["conditions"]) == 3
    assert "scores" in results
    assert len(results["scores"]) == 3
    assert "decision" in results
    assert "table_rows" in results
    assert "sources" in results
    assert "guidance" in results
    assert results["emergency"] is False
    assert results["decision_index"] == 2  # Moderate -> Book a Vet Visit
