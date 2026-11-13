"""Domain models for Veterinary Conditions, Source References, and Evidence Matches."""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class SourceReference:
    """Veterinary source reference supporting medical claims."""
    organization: str
    title: str
    url: str
    author: Optional[str] = None
    publication_date: Optional[str] = None
    date_researched: str = "2026-11-12"
    claims_supported: List[str] = field(default_factory=list)
    conflicting_evidence: Optional[str] = None
    verification_status: str = "SOURCE_REVIEWED"


@dataclass
class Condition:
    """Complete veterinary condition profile."""
    id: str  # CAT_001 to CAT_030, DOG_001 to DOG_030
    name: str
    species: str  # "Cat" or "Dog"
    category: str
    medical_classification: str
    definition: str
    causes_contributing_factors: List[str]
    common_symptoms: List[str]
    less_specific_symptoms: List[str]
    risk_factors: List[str]
    relevant_history: List[str]
    supporting_findings: List[str]
    contradictory_findings: List[str]
    missing_information_prompts: List[str]
    differential_diagnoses: List[str]
    veterinary_examinations: List[str]
    diagnostic_tests: List[str]
    follow_up_questions: List[str]
    severity: str  # "Mild", "Moderate", "Severe", "Critical"
    urgency: str   # "Emergency", "Urgent", "Routine", "Monitoring"
    safe_recommended_next_step: str
    sources: List[SourceReference]
    source_verification_status: str = "SOURCE_REVIEWED"
    rule_validation_status: str = "TESTED"
    safety_review_status: str = "SAFETY_REVIEWED"
    veterinarian_review_status: str = "VETERINARIAN_REVIEW_REQUIRED"
    limitations: str = "Questionnaire-based assessment only; definitive diagnosis requires direct veterinary examination and diagnostic testing."

    @property
    def system(self) -> str:
        """Alias for category / anatomical system."""
        return self.category

    @property
    def primary_symptoms(self) -> List[str]:
        """Alias for common symptoms."""
        return self.common_symptoms

    @property
    def secondary_symptoms(self) -> List[str]:
        """Alias for less specific symptoms."""
        return self.less_specific_symptoms

    @property
    def urgency_tier(self) -> str:
        """Map urgency/severity to the 4 Decision Making System tiers."""
        if self.urgency == "Emergency" or self.severity == "Critical":
            return "Get Help Now"
        elif self.urgency == "Urgent" or self.severity == "Severe":
            return "Visit Vet Today"
        elif self.urgency == "Routine" or self.severity == "Moderate":
            return "Book a Vet Visit"
        return "Home Care & Monitor"

    def to_dict(self) -> Dict[str, Any]:
        """Convert condition to serializable dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "category": self.category,
            "medical_classification": self.medical_classification,
            "definition": self.definition,
            "causes_contributing_factors": self.causes_contributing_factors,
            "common_symptoms": self.common_symptoms,
            "less_specific_symptoms": self.less_specific_symptoms,
            "risk_factors": self.risk_factors,
            "relevant_history": self.relevant_history,
            "supporting_findings": self.supporting_findings,
            "contradictory_findings": self.contradictory_findings,
            "missing_information_prompts": self.missing_information_prompts,
            "differential_diagnoses": self.differential_diagnoses,
            "veterinary_examinations": self.veterinary_examinations,
            "diagnostic_tests": self.diagnostic_tests,
            "follow_up_questions": self.follow_up_questions,
            "severity": self.severity,
            "urgency": self.urgency,
            "safe_recommended_next_step": self.safe_recommended_next_step,
            "sources": [
                {
                    "organization": s.organization,
                    "title": s.title,
                    "url": s.url,
                    "author": s.author,
                    "publication_date": s.publication_date,
                    "claims_supported": s.claims_supported,
                }
                for s in self.sources
            ],
            "source_verification_status": self.source_verification_status,
            "rule_validation_status": self.rule_validation_status,
            "safety_review_status": self.safety_review_status,
            "veterinarian_review_status": self.veterinarian_review_status,
            "limitations": self.limitations,
        }


@dataclass
class EvidenceMatch:
    """Internal evidence match result for a condition (not a statistical probability)."""
    condition: Condition
    match_score: int  # 0 to 100 internal score
    supporting_evidence: List[str] = field(default_factory=list)
    contradictory_evidence: List[str] = field(default_factory=list)
    missing_evidence: List[str] = field(default_factory=list)
    match_tier: str = ""  # "Strong evidence match", "Possible evidence match", "Insufficient information"
    differential_notes: str = ""
    urgency_level: str = ""
    is_emergency: bool = False

