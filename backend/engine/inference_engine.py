"""Inference Engine: Deterministic rule-based reasoning and evidence evaluation."""
from typing import List, Dict, Any, Tuple
from backend.models.assessment import AssessmentInput
from backend.models.condition import Condition, EvidenceMatch
from backend.knowledge_base.knowledge_base_loader import KnowledgeBase
from backend.engine.rule_engine import RuleEngine, DiagnosticRule
from backend.engine.question_engine import FOLLOW_UP_QUESTIONS_TEXT as FOLLOW_UP_QUESTIONS
from backend.utils.helpers import clamp_score


class InferenceEngine:
    """Evaluates clinical rules to compute condition concordance and explainability."""

    def __init__(self):
        self._kb = KnowledgeBase.get_instance()
        self._rule_engine = RuleEngine()

    def evaluate(self, assessment: AssessmentInput) -> List[EvidenceMatch]:
        """Execute rule-based inferencing on the user assessment input."""
        species = assessment.pet.species.capitalize()
        symptoms = assessment.symptoms
        answers = assessment.answers
        severity = assessment.severity
        duration = assessment.duration
        age = assessment.pet.age

        # Retrieve candidate conditions for species
        candidate_conditions = self._kb.get_by_species(species)
        matches: List[EvidenceMatch] = []

        # Extract affirmative and uncertain answer texts
        yes_statements: List[str] = []
        not_sure_statements: List[str] = []
        for k, v in answers.items():
            if "|" in k:
                s_name, idx_str = k.split("|", 1)
                try:
                    idx = int(idx_str)
                    q_list = FOLLOW_UP_QUESTIONS.get(s_name, [])
                    if idx < len(q_list):
                        q_text = q_list[idx]
                        if v == "Yes":
                            yes_statements.append(q_text)
                        elif v == "Not Sure":
                            not_sure_statements.append(q_text)
                except ValueError:
                    pass

        # Evaluate every candidate condition against its diagnostic rules
        for cond in candidate_conditions:
            score, supporting, contradictory, missing, diff_notes = self._score_condition(
                cond=cond,
                symptoms=symptoms,
                yes_statements=yes_statements,
                not_sure_statements=not_sure_statements,
                severity=severity,
                duration=duration,
                age=age,
            )

            # Determine tier
            if score >= 60:
                tier = "Strong evidence match"
            elif score >= 30:
                tier = "Possible evidence match"
            else:
                tier = "Insufficient information"

            is_emergency = cond.severity == "Critical" or cond.urgency == "Emergency"

            matches.append(EvidenceMatch(
                condition=cond,
                match_score=score,
                match_tier=tier,
                supporting_evidence=supporting,
                contradictory_evidence=contradictory,
                missing_evidence=missing,
                differential_notes=diff_notes,
                urgency_level=cond.urgency,
                is_emergency=is_emergency,
            ))

        # Rank matches: highest score first; for equal scores, prioritize higher severity
        matches.sort(key=lambda m: (m.match_score, 1 if m.is_emergency else 0), reverse=True)
        return matches

    def _score_condition(
        self,
        cond: Condition,
        symptoms: List[str],
        yes_statements: List[str],
        not_sure_statements: List[str],
        severity: str,
        duration: str,
        age: float,
    ) -> Tuple[int, List[str], List[str], List[str], str]:
        """Compute condition evidence match score and findings breakdown."""
        score = 0
        supporting: List[str] = []
        contradictory: List[str] = []
        missing: List[str] = []

        # 1. Primary symptom concordance
        cond_syms_lower = [s.lower() for s in cond.common_symptoms + cond.less_specific_symptoms]
        matched_primary = [s for s in symptoms if s.lower() in cond_syms_lower]
        if matched_primary:
            score += 35 + min(25, (len(matched_primary) - 1) * 15)
            supporting.extend(matched_primary)

        # 2. Rule evaluation
        rules = self._rule_engine.get_rules_for_condition(cond.id)
        for rule in rules:
            # Check affirmative follow-ups
            matched_fu = 0
            for crit in rule.supporting_followup_criteria:
                for stmt in yes_statements:
                    if crit.lower() in stmt.lower():
                        matched_fu += 1
                        if stmt not in supporting:
                            supporting.append(stmt)

            score += min(25, matched_fu * 10)

            # Check age preference
            if rule.age_preference == "Young" and age < 2.0:
                score += 8
                supporting.append(f"Young age ({age:g} yrs) predisposed to {cond.name}")
            elif rule.age_preference == "Senior" and age >= 8.0:
                score += 8
                supporting.append(f"Senior age ({age:g} yrs) predisposed to {cond.name}")

        # 3. Severity weighting
        if severity == "Severe":
            if cond.severity in ["Severe", "Critical"]:
                score += 10
            elif cond.severity == "Mild":
                score -= 5
                contradictory.append(f"Severe signs reported, whereas {cond.name} is typically mild")
        elif severity == "Mild":
            if cond.severity == "Critical":
                score -= 15
                contradictory.append(f"Only mild signs reported, whereas {cond.name} is typically acute or critical")

        # 4. Duration weighting
        if duration == "More than 3 days":
            if "Chronic" in cond.medical_classification or cond.category in ["Endocrine", "Dental"]:
                score += 5
            elif "peracute" in cond.medical_classification.lower():
                score -= 10
                contradictory.append(f"Duration >3 days is inconsistent with peracute nature of {cond.name}")

        # 5. Missing evidence collection
        for stmt in not_sure_statements:
            missing.append(stmt)

        for prompt in cond.missing_information_prompts[:2]:
            if prompt not in missing:
                missing.append(prompt)

        # Ensure minimal missing note if user answered everything
        if not missing:
            missing.append("Definitive diagnostic tests (blood panel, imaging, or cytology) not yet performed.")

        # Differential note
        diffs = cond.differential_diagnoses[:3]
        diff_notes = f"Differential considerations: {', '.join(diffs)}." if diffs else ""

        clamped = clamp_score(score, 0, 92)
        return clamped, supporting, contradictory, missing, diff_notes
