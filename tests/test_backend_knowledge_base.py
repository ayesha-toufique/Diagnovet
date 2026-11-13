"""Unit tests for Diagnovet backend Knowledge Base."""
import pytest
from backend.knowledge_base.knowledge_base_loader import get_knowledge_base
from backend.models.condition import Condition


@pytest.fixture(scope="module")
def kb():
    """Returns singleton knowledge base instance."""
    return get_knowledge_base()


def test_knowledge_base_condition_counts(kb):
    """Verify exactly 60 conditions total: 30 cats, 30 dogs."""
    assert len(kb.get_all_conditions()) == 60
    assert len(kb.get_cat_conditions()) == 30
    assert len(kb.get_dog_conditions()) == 30


def test_condition_id_format_and_species_isolation(kb):
    """Verify condition ID formatting and species isolation."""
    cat_conditions = kb.get_cat_conditions()
    dog_conditions = kb.get_dog_conditions()

    # Check cat conditions
    for i, cond in enumerate(cat_conditions, start=1):
        expected_id = f"CAT_{i:03d}"
        assert cond.id == expected_id, f"Condition {cond.name} has incorrect ID {cond.id}"
        assert cond.species.lower() == "cat", f"Condition {cond.id} has incorrect species {cond.species}"

    # Check dog conditions
    for i, cond in enumerate(dog_conditions, start=1):
        expected_id = f"DOG_{i:03d}"
        assert cond.id == expected_id, f"Condition {cond.name} has incorrect ID {cond.id}"
        assert cond.species.lower() == "dog", f"Condition {cond.id} has incorrect species {cond.species}"


def test_condition_data_integrity(kb):
    """Verify all conditions have non-empty required fields and medical sources."""
    for cond in kb.get_all_conditions():
        assert cond.name.strip(), f"Condition {cond.id} has blank name"
        assert cond.system.strip(), f"Condition {cond.id} has blank system"
        assert cond.primary_symptoms, f"Condition {cond.id} has no primary symptoms"
        assert cond.diagnostic_tests, f"Condition {cond.id} has no diagnostic tests"
        assert cond.urgency_tier in [
            "Get Help Now",
            "Visit Vet Today",
            "Book a Vet Visit",
            "Home Care & Monitor",
        ], f"Condition {cond.id} has invalid urgency tier {cond.urgency_tier}"

        # Verified authentic source citations
        assert cond.sources, f"Condition {cond.id} ({cond.name}) has no medical sources"
        for src in cond.sources:
            assert src.title.strip(), f"Source in {cond.id} has blank title"
            assert src.organization.strip(), f"Source in {cond.id} has blank organization"
            assert src.url.startswith("http"), f"Source in {cond.id} has invalid URL {src.url}"
            assert src.claims_supported, f"Source in {cond.id} has no claims supported"


def test_knowledge_base_lookups(kb):
    """Verify condition retrieval by ID and by species."""
    cat_1 = kb.get_condition_by_id("CAT_001")
    assert cat_1 is not None
    assert cat_1.id == "CAT_001"
    assert cat_1.species == "Cat"

    dog_1 = kb.get_condition_by_id("DOG_001")
    assert dog_1 is not None
    assert dog_1.id == "DOG_001"
    assert dog_1.species == "Dog"

    # Non-existent ID lookup
    assert kb.get_condition_by_id("INVALID_999") is None


def test_symptom_condition_search(kb):
    """Verify searching conditions matching specific symptoms."""
    vomiting_cats = kb.get_conditions_for_symptom("Cat", "Vomiting")
    assert len(vomiting_cats) > 0
    for c in vomiting_cats:
        assert c.species == "Cat"
        assert "Vomiting" in c.primary_symptoms or "Vomiting" in c.secondary_symptoms

    cough_dogs = kb.get_conditions_for_symptom("Dog", "Coughing")
    assert len(cough_dogs) > 0
    for c in cough_dogs:
        assert c.species == "Dog"
        assert "Coughing" in c.primary_symptoms or "Coughing" in c.secondary_symptoms
