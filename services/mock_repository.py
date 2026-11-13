"""Inference service adapter forwarding to the Phase 2 Rule-Based Expert System."""
from typing import Dict, Any
from backend.services.assessment_service import AssessmentService

_service = AssessmentService()


def calculate_results(session_state: Dict[str, Any]) -> Dict[str, Any]:
    """Execute Phase 2 inference engine, emergency detection, and DSS service."""
    return _service.calculate_results_dict(session_state)
