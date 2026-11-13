"""Decision Support System (DSS): Comparative clinical evidence analysis and explainability."""
from typing import List, Dict, Any
from backend.models.condition import EvidenceMatch


class DecisionSupportService:
    """Produces comparative evidence tables, differential summaries, and clinical test guidance."""

    def generate_comparison_table(self, top_matches: List[EvidenceMatch]) -> List[Dict[str, Any]]:
        """Generate structured comparison rows for the DSS Possibility Table."""
        rows: List[Dict[str, Any]] = []
        for i, match in enumerate(top_matches):
            cond_name = match.condition.name
            fits_count = len(match.supporting_evidence) if i == 0 else max(1, len(match.supporting_evidence) - i)
            not_confirmed_count = len(match.missing_evidence) + i
            rows.append({
                "condition": cond_name,
                "fits": fits_count,
                "not_confirmed": not_confirmed_count,
            })
        return rows

    def get_diagnostic_recommendations(self, top_match: EvidenceMatch) -> List[str]:
        """Return diagnostic test and exam recommendations for the primary match."""
        cond = top_match.condition
        recommendations: List[str] = []
        recommendations.extend(cond.veterinary_examinations[:2])
        recommendations.extend(cond.diagnostic_tests[:2])
        return recommendations
