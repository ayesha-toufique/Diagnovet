"""Knowledge Base Loader and Integrity Validation Service."""
from typing import Dict, List, Optional
from backend.models.condition import Condition
from backend.knowledge_base.cat_conditions import CAT_CONDITIONS
from backend.knowledge_base.dog_conditions import DOG_CONDITIONS


class KnowledgeBase:
    """Singleton repository for all verified veterinary conditions."""

    _instance: Optional["KnowledgeBase"] = None

    def __init__(self):
        self._cats: Dict[str, Condition] = CAT_CONDITIONS
        self._dogs: Dict[str, Condition] = DOG_CONDITIONS
        self._all: Dict[str, Condition] = {**self._cats, **self._dogs}
        self._validate_integrity()

    @classmethod
    def get_instance(cls) -> "KnowledgeBase":
        """Get or initialize singleton instance."""
        if cls._instance is None:
            cls._instance = KnowledgeBase()
        return cls._instance

    def _validate_integrity(self) -> None:
        """Validate knowledge base completeness, taxonomy, and integrity."""
        assert len(self._cats) == 30, f"Expected 30 cat conditions, found {len(self._cats)}"
        assert len(self._dogs) == 30, f"Expected 30 dog conditions, found {len(self._dogs)}"
        assert len(self._all) == 60, f"Expected 60 total conditions, found {len(self._all)}"

        # Validate unique IDs and correct species assignment
        for cid, cond in self._cats.items():
            assert cid.startswith("CAT_"), f"Invalid cat condition ID format: {cid}"
            assert cond.species == "Cat", f"Mismatched species for {cid}: {cond.species}"
            assert len(cond.sources) >= 1, f"Missing source citations for {cid}"
            assert cond.name.strip(), f"Missing name for {cid}"

        for did, cond in self._dogs.items():
            assert did.startswith("DOG_"), f"Invalid dog condition ID format: {did}"
            assert cond.species == "Dog", f"Mismatched species for {did}: {cond.species}"
            assert len(cond.sources) >= 1, f"Missing source citations for {did}"
            assert cond.name.strip(), f"Missing name for {did}"

    def get_condition(self, condition_id: str) -> Optional[Condition]:
        """Lookup condition by its unique ID."""
        return self._all.get(condition_id)

    def get_by_species(self, species: str) -> List[Condition]:
        """Return list of conditions filtered by species."""
        norm = species.capitalize()
        if norm == "Cat":
            return list(self._cats.values())
        elif norm == "Dog":
            return list(self._dogs.values())
        return []

    def get_by_symptom(self, species: str, symptom: str) -> List[Condition]:
        """Find all conditions for a species containing a specific symptom."""
        target_conditions = self.get_by_species(species)
        matches: List[Condition] = []
        for cond in target_conditions:
            all_symptoms = [s.lower() for s in cond.common_symptoms + cond.less_specific_symptoms]
            if symptom.lower() in all_symptoms:
                matches.append(cond)
        return matches

    def get_all(self) -> List[Condition]:
        """Return all 60 conditions."""
        return list(self._all.values())

    def get_all_conditions(self) -> List[Condition]:
        """Alias for get_all()."""
        return self.get_all()

    def get_cat_conditions(self) -> List[Condition]:
        """Return all cat conditions."""
        return list(self._cats.values())

    def get_dog_conditions(self) -> List[Condition]:
        """Return all dog conditions."""
        return list(self._dogs.values())

    def get_condition_by_id(self, condition_id: str) -> Optional[Condition]:
        """Alias for get_condition()."""
        return self.get_condition(condition_id)

    def get_conditions_for_symptom(self, species: str, symptom: str) -> List[Condition]:
        """Alias for get_by_symptom()."""
        return self.get_by_symptom(species, symptom)

    def get_primary_symptoms_for_species(self, species: str) -> List[str]:
        """Return distinct primary clinical signs available for UI triage chips."""
        norm = species.capitalize()
        if norm == "Dog":
            return ["Vomiting", "Diarrhoea", "Itching", "Coughing", "Limping", "Low appetite"]
        elif norm == "Cat":
            return ["Vomiting", "Sneezing", "Straining to urinate", "Hair loss", "Low appetite", "Hiding more"]
        return []


def get_knowledge_base() -> KnowledgeBase:
    """Helper function to retrieve singleton KnowledgeBase instance."""
    return KnowledgeBase.get_instance()
