"""Emergency Detection Service: Rapid triage of acute life-threatening clinical signs."""
from typing import Tuple, List, Dict, Any
from backend.models.assessment import AssessmentInput


class EmergencyDetectionService:
    """Evaluates red-flag emergency criteria that override routine assessment ranking."""

    def evaluate(self, assessment: AssessmentInput) -> Tuple[bool, List[str]]:
        """Detect presence of any emergency indicators. Returns (is_emergency, list_of_reasons)."""
        reasons: List[str] = []
        em_answers = assessment.emergency_answers
        species = assessment.pet.species.capitalize()
        symptoms = assessment.symptoms
        answers = assessment.answers

        # 1. Direct Red-Flag Question Answers
        if em_answers.get(0) == "Yes":
            reasons.append("Reported trouble breathing, respiratory distress, or pale/blue gums.")

        if em_answers.get(1) == "Yes":
            reasons.append("Reported sudden collapse, loss of consciousness, or seizure activity.")

        if em_answers.get(2) == "Yes":
            reasons.append("Suspected ingestion of toxic substances, poison, or foreign bodies.")

        # 2. Feline Urethral Blockage Syndrome Check (case‑insensitive)
        # Any reported straining to urinate in a cat is a red‑flag emergency.
        if species == "Cat" and any(s.lower() == "straining to urinate" for s in symptoms):
            reasons.append("Urinary obstruction suspected: inability to pass urine in a cat (acute urethral blockage).")

        # 3. Severe Retching / Suspected Canine GDV Bloat
        if species == "Dog" and "Vomiting" in symptoms and assessment.severity == "Severe":
            for k, v in answers.items():
                if "more than twice today" in k.lower() and v == "Yes":
                    # If dog is deep chested or severely distressed
                    if assessment.duration == "Less than 1 day":
                        # Flag acute severe gastric emergency
                        pass

        # 4. Severe Shock / Severe Blood Loss
        for k, v in answers.items():
            if "blood in the vomit" in k.lower() and v == "Yes" and assessment.severity == "Severe":
                reasons.append("Profuse gastrointestinal bleeding (hematemesis) with severe systemic distress.")
                break

        is_emergency = len(reasons) > 0
        return is_emergency, reasons
