"""Unit tests for Diagnovet backend inference, rule, and question engines."""
import pytest
from backend.engine.rule_engine import RuleEngine
from backend.engine.question_engine import QuestionEngine
from backend.engine.inference_engine import InferenceEngine
from backend.models.assessment import AssessmentInput, PetProfile


@pytest.fixture(scope="module")
def rule_engine():
    return RuleEngine()


@pytest.fixture(scope="module")
def question_engine():
    return QuestionEngine()


@pytest.fixture(scope="module")
def inference_engine():
    return InferenceEngine()


def test_rule_engine_coverage(rule_engine):
    """Verify rule engine contains rules for all 60 conditions."""
    rules = rule_engine.get_all_rules()
    assert len(rules) == 60

    cat_rules = rule_engine.get_rules_for_species("Cat")
    dog_rules = rule_engine.get_rules_for_species("Dog")
    assert len(cat_rules) == 30
    assert len(dog_rules) == 30


def test_rule_evaluation(rule_engine):
    """Verify rule condition evaluation for positive and negative matches."""
    assessment = AssessmentInput(
        pet=PetProfile(species="Cat", breed="Persian", age=3.0, weight=4.0, gender="Male"),
        symptoms=["Frequent Urination", "Straining to Urinate"],
        answers={"Frequent Urination|0": "Yes"},
        duration="1-3 days",
        severity="Severe",
        frequency="Constantly",
        emergency_answers={0: "No", 1: "No", 2: "No"},
    )

    matches = rule_engine.evaluate_rules(assessment)
    assert len(matches) > 0

    # Urinary symptoms must match feline urinary tract conditions.
    # CAT_013 = Feline Idiopathic Cystitis, CAT_014 = Feline Urethral Obstruction
    matched_ids = [m.condition_id for m in matches]
    assert any(cid in matched_ids for cid in ("CAT_013", "CAT_014", "CAT_016")), (
        f"Expected a feline urinary condition (CAT_013/CAT_014/CAT_016) in matched rules, got: {matched_ids}"
    )


def test_question_engine_symptoms_and_followups(question_engine):
    """Verify question engine provides symptoms and follow-up questions."""
    cat_syms = question_engine.get_symptoms_for_species("Cat")
    dog_syms = question_engine.get_symptoms_for_species("Dog")

    assert "Vomiting" in cat_syms
    assert "Vomiting" in dog_syms
    assert len(cat_syms) >= 10
    assert len(dog_syms) >= 10

    # Follow-ups for vomiting
    vomit_questions = question_engine.get_follow_up_questions("Vomiting")
    assert len(vomit_questions) > 0
    assert any("twice" in q.text.lower() for q in vomit_questions)


def test_question_engine_clean_orphaned_answers(question_engine):
    """Verify orphaned follow-up answers are removed when symptom is deselected."""
    current_syms = ["Vomiting"]
    answers = {
        "Vomiting|0": "Yes",
        "Vomiting|1": "No",
        "Coughing|0": "Yes",
        "Diarrhoea|0": "Not Sure",
    }
    cleaned = question_engine.clean_orphaned_answers(current_syms, answers)
    assert "Vomiting|0" in cleaned
    assert "Vomiting|1" in cleaned
    assert "Coughing|0" not in cleaned
    assert "Diarrhoea|0" not in cleaned


def test_inference_engine_scoring_and_ranking(inference_engine):
    """Verify inference engine calculates differential rankings and clamps scores."""
    assessment = AssessmentInput(
        pet=PetProfile(species="Dog", breed="Labrador", age=4.0, weight=25.0, gender="Male"),
        symptoms=["Coughing", "Lethargy"],
        answers={"Coughing|0": "Yes"},
        duration="1-3 days",
        severity="Moderate",
        frequency="Often",
        emergency_answers={0: "No", 1: "No", 2: "No"},
    )

    matches = inference_engine.evaluate(assessment)
    assert len(matches) >= 3

    # Ranking must be in descending order of match_score
    for i in range(len(matches) - 1):
        assert matches[i].match_score >= matches[i + 1].match_score

    # Top score must be clamped at or below 92 to avoid false certainty
    top = matches[0]
    assert 0 <= top.match_score <= 92
    assert top.condition.species == "Dog"
    assert len(top.supporting_evidence) > 0
