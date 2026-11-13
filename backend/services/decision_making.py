"""Decision Making System: Evaluates urgency level and generates transparent decision rationale."""
from typing import Tuple, List, Dict, Any
from backend.models.assessment import AssessmentInput, DecisionOutcome

DECISION_TIERS: List[Dict[str, Any]] = [
    {
        "icon": "🚨",
        "name": "Get Help Now",
        "tone": "red",
        "level": "Critical",
        "text": "Go to an emergency vet immediately.",
        "steps": [
            "Call the nearest emergency vet and tell them you are on the way.",
            "Keep your pet calm and warm.",
            "Do not give food, water or any medicine.",
        ],
    },
    {
        "icon": "🏥",
        "name": "Visit Vet Today",
        "tone": "amb",
        "level": "High",
        "text": "Your pet should be seen by a vet today.",
        "steps": [
            "Call a vet clinic and ask for a same-day visit.",
            "Note when the signs started.",
            "Do not give human medicines.",
        ],
    },
    {
        "icon": "📅",
        "name": "Book a Vet Visit",
        "tone": "blu",
        "level": "Medium",
        "text": "A vet visit in the next few days is a good idea.",
        "steps": [
            "Book an appointment this week.",
            "Write down any changes you see.",
            "Make sure fresh water is available.",
        ],
    },
    {
        "icon": "🏡",
        "name": "Home Care & Monitor",
        "tone": "grn",
        "level": "Low",
        "text": "Watch your pet closely at home for now.",
        "steps": [
            "Keep your pet comfortable and rested.",
            "Check again in 24 hours.",
            "Book a vet visit if signs get worse.",
        ],
    },
]


class DecisionMakingSystem:
    """Calculates appropriate clinical care tier and rationale."""

    def evaluate(
        self,
        assessment: AssessmentInput,
        emergency_detected: bool,
        emergency_reasons: List[str]
    ) -> Tuple[int, DecisionOutcome]:
        """Determine clinical urgency tier (0-3) and create DecisionOutcome object."""
        severity = assessment.severity
        duration = assessment.duration
        frequency = assessment.frequency
        symptoms = assessment.symptoms

        if emergency_detected:
            d_idx = 0
            tier_data = DECISION_TIERS[0]
            reasons_str = "; ".join(emergency_reasons)
            rationale = f"Emergency override triggered: {reasons_str}. Immediate veterinary care is imperative."
        elif severity == "Severe":
            d_idx = 1
            tier_data = DECISION_TIERS[1]
            rationale = (
                f"You reported severe signs ({', '.join(symptoms)}) lasting {duration.lower()} "
                f"and happening {frequency.lower()}. A same-day veterinary examination is required to prevent deterioration."
            )
        elif severity == "Moderate":
            d_idx = 2
            tier_data = DECISION_TIERS[2]
            rationale = (
                f"You reported moderate signs lasting {duration.lower()} with {frequency.lower()} occurrence. "
                "Non-emergency veterinary evaluation in the coming days is recommended to prevent chronic progression."
            )
        else:
            d_idx = 3
            tier_data = DECISION_TIERS[3]
            rationale = (
                f"You reported mild signs ({', '.join(symptoms)}) occurring {frequency.lower()}. "
                "Close home observation is safe for now provided no emergency signs or worsening develops."
            )

        outcome = DecisionOutcome(
            icon=tier_data["icon"],
            name=tier_data["name"],
            tone=tier_data["tone"],
            level=tier_data["level"],
            text=tier_data["text"],
            steps=list(tier_data["steps"]),
            rationale=rationale,
        )

        return d_idx, outcome
