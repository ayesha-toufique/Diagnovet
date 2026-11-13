"""Assessment Service: High-level orchestrator for inference, decision making, and DSS."""
from typing import Dict, Any, List, Optional
from backend.models.assessment import PetProfile, AssessmentInput, AssessmentResult, DecisionOutcome
from backend.models.condition import EvidenceMatch, Condition
from backend.engine.inference_engine import InferenceEngine
from backend.services.emergency_detection import EmergencyDetectionService
from backend.services.decision_making import DecisionMakingSystem, DECISION_TIERS
from backend.services.decision_support import DecisionSupportService
from backend.services.care_guidance import CareGuidanceService
from backend.knowledge_base.knowledge_base_loader import KnowledgeBase


class AssessmentService:
    """Coordinates the expert system consultation and generates comprehensive results."""

    def __init__(self):
        self._kb = KnowledgeBase.get_instance()
        self._inference_engine = InferenceEngine()
        self._emergency_service = EmergencyDetectionService()
        self._decision_system = DecisionMakingSystem()
        self._dss_service = DecisionSupportService()
        self._care_service = CareGuidanceService()

    def process_assessment(self, session_state: Dict[str, Any]) -> AssessmentResult:
        """Process session state and return strongly typed AssessmentResult."""
        # 1. Parse PetProfile
        sp = session_state.get("sp", "Dog")
        breed = session_state.get("breed", "Unknown")
        gen = session_state.get("gen", "Unknown")
        try:
            age = float(str(session_state.get("age", 1)).strip() or 1)
        except ValueError:
            age = 1.0
        try:
            wt_raw = session_state.get("wt", "")
            wt = float(str(wt_raw).strip()) if str(wt_raw).strip() else None
        except ValueError:
            wt = None
        bg = session_state.get("bg", "")

        pet = PetProfile(species=sp, breed=breed, gender=gen, age=age, weight=wt, background=bg)

        # 2. Parse AssessmentInput
        syms: List[str] = session_state.get("syms", [])
        ans: Dict[str, str] = session_state.get("ans", {})
        dur: str = session_state.get("dur", "")
        sev: str = session_state.get("sev", "")
        frq: str = session_state.get("frq", "")
        em: Dict[int, str] = session_state.get("em", {})

        assessment_input = AssessmentInput(
            pet=pet,
            symptoms=syms,
            answers=ans,
            duration=dur,
            severity=sev,
            frequency=frq,
            emergency_answers=em,
        )

        # 3. Emergency Evaluation
        emergency_detected, emergency_reasons = self._emergency_service.evaluate(assessment_input)

        # 4. Inference Engine Evaluation
        all_matches = self._inference_engine.evaluate(assessment_input)
        top_matches = all_matches[:3] if len(all_matches) >= 3 else all_matches

        # 5. Decision Making Evaluation
        d_idx, decision_outcome = self._decision_system.evaluate(
            assessment=assessment_input,
            emergency_detected=emergency_detected,
            emergency_reasons=emergency_reasons,
        )

        # 6. Decision Support Service Table Generation
        table_rows = self._dss_service.generate_comparison_table(top_matches)

        # Compile supporting and contradictory findings
        supporting_findings = list(syms)
        for m in top_matches:
            for s in m.supporting_evidence:
                if s not in supporting_findings:
                    supporting_findings.append(s)

        contradictory_findings: List[str] = []
        for m in top_matches:
            for c in m.contradictory_evidence:
                if c not in contradictory_findings:
                    contradictory_findings.append(c)

        missing_info: List[str] = []
        if top_matches:
            missing_info.extend(top_matches[0].missing_evidence)

        return AssessmentResult(
            pet=pet,
            matches=top_matches,
            emergency_detected=emergency_detected,
            emergency_reasons=emergency_reasons,
            decision_index=d_idx,
            decision=decision_outcome,
            supporting_findings=supporting_findings,
            contradictory_findings=contradictory_findings,
            missing_information=missing_info,
            table_rows=table_rows,
        )

    def calculate_results_dict(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        """Backward-compatible result calculation dictionary for existing Streamlit views."""
        res = self.process_assessment(session_state)
        top_matches = res.matches

        conditions = [m.condition.name for m in top_matches]
        scores = [m.match_score for m in top_matches]

        # Top condition details
        top_condition: Optional[Condition] = top_matches[0].condition if top_matches else None
        top_sources = top_condition.sources if top_condition else []

        guidance_dict = {}
        if top_matches:
            guidance_dict = self._care_service.generate_guidance(
                decision=res.decision,
                primary_match=top_matches[0],
                emergency_detected=res.emergency_detected,
            )

        return {
            "conditions": conditions,
            "scores": scores,
            "supporting": res.supporting_findings,
            "missing": res.missing_information,
            "contradictory": res.contradictory_findings,
            "emergency": res.emergency_detected,
            "emergency_reasons": res.emergency_reasons,
            "decision_index": res.decision_index,
            "decision": {
                "icon": res.decision.icon,
                "name": res.decision.name,
                "tone": res.decision.tone,
                "level": res.decision.level,
                "text": res.decision.text,
                "steps": res.decision.steps,
                "rationale": res.decision.rationale,
            },
            "table_rows": res.table_rows,
            "matches": top_matches,
            "top_condition": top_condition,
            "sources": top_sources,
            "guidance": guidance_dict,
            "disclaimer": res.disclaimer,
        }
