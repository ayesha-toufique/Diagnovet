"""Question Engine: Dynamic, species-specific guided questioning."""
from typing import List, Dict, Any, Optional
from backend.models.question import Question

SYMPTOMS_BY_SPECIES: Dict[str, List[str]] = {
    "Dog": [
        "Vomiting", "Diarrhoea", "Itching", "Coughing", "Limping",
        "Low appetite", "Lethargy", "Fever", "Weight loss", "Loss of coordination",
    ],
    "Cat": [
        "Vomiting", "Sneezing", "Straining to urinate", "Hair loss",
        "Low appetite", "Hiding more", "Lethargy", "Fever", "Weight loss",
        "Loss of coordination",
    ],
}

FOLLOW_UP_QUESTIONS_TEXT: Dict[str, List[str]] = {
    "Vomiting": [
        "Has it happened more than twice today?",
        "Is there blood in the vomit?",
    ],
    "Diarrhoea": [
        "Is the stool watery?",
        "Is there blood or mucus in it?",
    ],
    "Itching": [
        "Is the skin red or sore?",
        "Have you seen fleas?",
    ],
    "Coughing": [
        "Is the cough worse at night?",
        "Does your pet gag after coughing?",
    ],
    "Limping": [
        "Is the leg held off the ground?",
        "Is there visible swelling or heat?",
    ],
    "Low appetite": [
        "Is your pet also drinking less?",
        "Has this lasted more than a day?",
    ],
    "Sneezing": [
        "Is there eye or nose discharge?",
        "Does sneezing happen often?",
    ],
    "Straining to urinate": [
        "Is little or no urine coming out?",
        "Is there blood in the urine?",
    ],
    "Hair loss": [
        "Are there bald patches?",
        "Is the skin flaky?",
    ],
    "Hiding more": [
        "Has the behaviour changed suddenly?",
        "Is your pet eating less?",
    ],
    "Lethargy": [
        "Is your pet unable to stand or walk normally?",
        "Has this come on suddenly within the last 24 hours?",
    ],
    "Fever": [
        "Is your pet shivering or trembling?",
        "Has your pet stopped eating?",
    ],
    "Weight loss": [
        "Has the weight loss been gradual over weeks?",
        "Is your pet still eating normally?",
    ],
    "Loss of coordination": [
        "Is your pet circling or falling over?",
        "Did this start suddenly?",
    ],
}

EMERGENCY_QUESTIONS: List[str] = [
    "Trouble breathing, or blue or pale gums?",
    "Collapse or a seizure?",
    "Possibly swallowed poison or a toxic item?",
]


def _build_question_objects(symptom: str) -> List[Question]:
    """Convert raw text follow-up strings into Question objects for a given symptom."""
    texts = FOLLOW_UP_QUESTIONS_TEXT.get(symptom, [])
    questions: List[Question] = []
    for idx, text in enumerate(texts):
        questions.append(Question(
            key=f"{symptom}|{idx}",
            text=text,
            category="follow_up",
            target_symptom=symptom,
        ))
    return questions


class QuestionEngine:
    """Manages guided clinical questioning and follow-up generation."""

    def get_symptoms_for_species(self, species: str) -> List[str]:
        """Return available primary symptom options for the chosen species."""
        return SYMPTOMS_BY_SPECIES.get(species.capitalize(), [])

    def get_follow_up_questions(self, symptom: str) -> List[Question]:
        """Return follow-up Question objects for a single symptom."""
        return _build_question_objects(symptom)

    def get_follow_ups_for_symptoms(self, symptoms: List[str]) -> Dict[str, List[Question]]:
        """Return follow-up Question objects keyed by symptom name."""
        return {s: _build_question_objects(s) for s in symptoms if s in FOLLOW_UP_QUESTIONS_TEXT}

    def get_follow_ups_as_text(self, symptoms: List[str]) -> Dict[str, List[str]]:
        """Return raw follow-up text strings keyed by symptom name."""
        return {s: FOLLOW_UP_QUESTIONS_TEXT[s] for s in symptoms if s in FOLLOW_UP_QUESTIONS_TEXT}

    def get_emergency_questions(self) -> List[str]:
        """Return standard red-flag emergency screening questions."""
        return list(EMERGENCY_QUESTIONS)

    def clean_orphaned_answers(self, symptoms: List[str], current_answers: Dict[str, str]) -> Dict[str, str]:
        """Remove follow-up answers for symptoms that were deselected by the user."""
        valid_prefixes = tuple(f"{s}|" for s in symptoms)
        return {k: v for k, v in current_answers.items() if k.startswith(valid_prefixes)}
