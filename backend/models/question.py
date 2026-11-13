"""Models for Guided Questioning."""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Question:
    """Clinical question structure for the guided consultation."""
    key: str
    text: str
    category: str  # "symptom", "follow_up", "timing", "severity", "frequency", "emergency"
    options: List[str] = field(default_factory=lambda: ["Yes", "No", "Not Sure"])
    condition_ids: List[str] = field(default_factory=list)
    is_emergency: bool = False
    help_text: Optional[str] = None
    target_symptom: Optional[str] = None
