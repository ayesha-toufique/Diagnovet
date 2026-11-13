"""Mock Repository and Service Interface Layer for Diagnovet.

Provides a clean abstraction between frontend views and data sources.
In Phase 2, this layer will interface with SQLite and the Inference/Diagnosis Engine.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import copy
from data.demo_data import (
    DEMO_PETS,
    DEMO_DIAGNOSIS_RESULT,
    DEMO_DECISION_EXPLANATION,
    DEMO_DSS_REPORT,
    DEMO_HISTORY,
    SAMPLE_QUESTIONNAIRE,
    DEFAULT_QUESTIONS,
    HEALTH_CATEGORIES,
    SUPPORTED_ANIMALS,
    EMERGENCY_SIGNS,
)


@dataclass
class PetProfile:
    id: str
    name: str
    species: str
    breed: str
    age: float
    gender: str
    weight: float
    conditions: str = "None"
    allergies: str = "None"
    notes: str = ""


class DiagnovetRepository:
    """Manages session-level data storage and retrieval for pets, consultations, and mock engines."""

    def __init__(self):
        self._pets: List[Dict[str, Any]] = copy.deepcopy(DEMO_PETS)
        self._history: List[Dict[str, Any]] = copy.deepcopy(DEMO_HISTORY)

    # Pet Profile Methods
    def get_all_pets(self) -> List[Dict[str, Any]]:
        return self._pets

    def get_pet_by_id(self, pet_id: str) -> Optional[Dict[str, Any]]:
        for pet in self._pets:
            if pet["id"] == pet_id:
                return pet
        return None

    def add_pet(self, pet_data: Dict[str, Any]) -> str:
        new_id = f"pet-{len(self._pets) + 1:03d}"
        pet_data["id"] = new_id
        self._pets.append(pet_data)
        return new_id

    def update_pet(self, pet_id: str, updated_data: Dict[str, Any]) -> bool:
        for idx, pet in enumerate(self._pets):
            if pet["id"] == pet_id:
                self._pets[idx].update(updated_data)
                return True
        return False

    # Consultation Data & Questions
    def get_health_categories(self) -> List[Dict[str, Any]]:
        return HEALTH_CATEGORIES

    def get_supported_animals(self) -> List[Dict[str, Any]]:
        return SUPPORTED_ANIMALS

    def get_emergency_signs(self) -> List[str]:
        return EMERGENCY_SIGNS

    def get_questions_for_category(self, category_id: str) -> List[Dict[str, Any]]:
        return SAMPLE_QUESTIONNAIRE.get(category_id, DEFAULT_QUESTIONS)

    # Phase 2 Compatibility Interfaces
    def get_diagnosis(
        self, consultation_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Returns mock diagnosis result.

        In Phase 2, this will trigger the Expert System Forward Chaining Inference Engine.
        """
        result = copy.deepcopy(DEMO_DIAGNOSIS_RESULT)
        if consultation_context and "pet_name" in consultation_context:
            result["pet_name"] = consultation_context["pet_name"]
            result["species"] = consultation_context.get("species", "Cat")
            result["category"] = consultation_context.get(
                "category", "Digestive Health"
            )
        return result

    def get_decision(
        self, consultation_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Returns mock decision explanation.

        In Phase 2, this will invoke the Decision Making Engine & Explanation Facility.
        """
        decision = copy.deepcopy(DEMO_DECISION_EXPLANATION)
        if consultation_context and "pet_name" in consultation_context:
            decision["pet_name"] = consultation_context["pet_name"]
        return decision

    def get_dss_report(
        self, consultation_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Returns mock Decision Support System comparison report.

        In Phase 2, this will synthesize multi-attribute criteria and evidence weighting.
        """
        dss = copy.deepcopy(DEMO_DSS_REPORT)
        if consultation_context and "pet_name" in consultation_context:
            dss["pet_name"] = consultation_context["pet_name"]
        return dss

    # Consultation History Methods
    def get_consultation_history(
        self, filter_pet: Optional[str] = None, filter_category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        items = self._history
        if filter_pet and filter_pet != "All":
            items = [c for c in items if c["pet_name"].lower() == filter_pet.lower()]
        if filter_category and filter_category != "All":
            items = [c for c in items if c["category"] == filter_category]
        return items

    def add_consultation_record(self, record: Dict[str, Any]) -> str:
        record_id = f"CNS-2026-{len(self._history) + 845:04d}"
        record["id"] = record_id
        self._history.insert(0, record)
        return record_id
