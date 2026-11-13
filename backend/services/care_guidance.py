"""Care Guidance Service: Medically cautious home guidance and vet preparation checklists."""
from typing import Dict, List, Any
from backend.models.assessment import DecisionOutcome
from backend.models.condition import EvidenceMatch


class CareGuidanceService:
    """Generates safe next-step guidance and veterinary preparation information."""

    def generate_guidance(
        self,
        decision: DecisionOutcome,
        primary_match: EvidenceMatch,
        emergency_detected: bool,
    ) -> Dict[str, Any]:
        """Produce structured care guidance elements."""
        cond = primary_match.condition

        # Unsafe actions to avoid
        unsafe_actions = [
            "Never administer human over-the-counter pain medications (Tylenol/paracetamol, Advil/ibuprofen, and aspirin are toxic or fatal).",
            "Do not force-feed a pet that is actively vomiting, lethargic, or struggling to breathe.",
            "Do not give home remedies, hydrogen peroxide, or essential oils without explicit veterinary instruction.",
        ]

        # Preparation checklist for clinic visit
        preparation_checklist = [
            "Record exact times when vomiting, diarrhea, or coughing episodes occurred.",
            "Bring photos or short videos of unusual posturing, breathing, or coughing spells.",
            "Take note of current food brand, treats, and any potential access to toxic household items or trash.",
            "Bring previous veterinary records and vaccination dates if visiting a new or emergency clinic.",
        ]

        return {
            "condition_name": cond.name,
            "condition_definition": cond.definition,
            "recommended_next_step": cond.safe_recommended_next_step,
            "warning_signs": [
                "Sudden collapse or unresponsiveness",
                "Extreme weakness, inability to stand, or dragged legs",
                "Pale, grey, or blue gums and tongue",
                "Labored, rapid, or open-mouth breathing",
            ],
            "unsafe_actions": unsafe_actions,
            "preparation_checklist": preparation_checklist,
            "sources": cond.sources,
        }
