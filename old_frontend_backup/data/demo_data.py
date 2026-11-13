"""Mock and demo data for Diagnovet Phase 1 Frontend."""

# Supported Species
SUPPORTED_ANIMALS = [
    {
        "species": "Dog",
        "icon": "🐶",
        "desc": "Canine health assessments across all life stages",
    },
    {
        "species": "Cat",
        "icon": "🐱",
        "desc": "Feline specialized health evaluation & care guidance",
    },
]

# 9 Core Health Categories
HEALTH_CATEGORIES = [
    {
        "id": "digestive",
        "name": "Digestive Health",
        "icon": "🥣",
        "desc": "Vomiting, diarrhea, loss of appetite, bloating",
    },
    {
        "id": "skin_coat",
        "name": "Skin & Coat",
        "icon": "✨",
        "desc": "Itching, hair loss, redness, lumps, parasites",
    },
    {
        "id": "respiratory",
        "name": "Respiratory Health",
        "icon": "🫁",
        "desc": "Coughing, wheezing, sneezing, nasal discharge",
    },
    {
        "id": "urinary",
        "name": "Urinary Health",
        "icon": "💧",
        "desc": "Straining, blood in urine, frequent or reduced urination",
    },
    {
        "id": "eyes_ears",
        "name": "Eyes & Ears",
        "icon": "👁️",
        "desc": "Discharge, head shaking, squinting, redness",
    },
    {
        "id": "general",
        "name": "General Health",
        "icon": "🩺",
        "desc": "Lethargy, fever, sudden weight change, weakness",
    },
    {
        "id": "nutrition",
        "name": "Nutrition & Weight",
        "icon": "🥗",
        "desc": "Dietary issues, excessive thirst, rapid weight loss/gain",
    },
    {
        "id": "dental",
        "name": "Dental Health",
        "icon": "🦷",
        "desc": "Bad breath, bleeding gums, difficulty chewing",
    },
    {
        "id": "behavioural",
        "name": "Behavioural Health",
        "icon": "🐾",
        "desc": "Sudden aggression, anxiety, excessive vocalization, pacing",
    },
]

# Emergency Warning Signs for Front-End Safety Alert Demonstration
EMERGENCY_SIGNS = [
    "Severe difficulty breathing, gasping, or open-mouth breathing (especially in cats)",
    "Pale, blue, or grayish gums and tongue",
    "Repeated non-productive retching or swollen, rigid abdomen",
    "Complete inability to urinate or extreme distress in litter box",
    "Seizure lasting longer than 2 minutes or multiple cluster seizures",
    "Uncontrolled active bleeding from any orifice",
    "Sudden inability to walk or paralysis of hind limbs",
    "Suspected ingestion of toxic substances (chocolate, lilies, rodenticide, antifreeze)",
]

# Sample Pet Profiles
DEMO_PETS = [
    {
        "id": "pet-001",
        "name": "Luna",
        "species": "Cat",
        "breed": "Domestic Shorthair",
        "age": 3.0,
        "gender": "Female (Spayed)",
        "weight": 4.2,
        "conditions": "None reported",
        "allergies": "No known allergies",
        "notes": "Indoor-only cat, fully vaccinated.",
    },
    {
        "id": "pet-002",
        "name": "Max",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 5.0,
        "gender": "Male (Neutered)",
        "weight": 31.5,
        "conditions": "Mild bilateral hip dysplasia history",
        "allergies": "Sensitive to beef proteins",
        "notes": "Active family dog, up to date on heartworm preventative.",
    },
    {
        "id": "pet-003",
        "name": "Bella",
        "species": "Cat",
        "breed": "Siamese",
        "age": 2.0,
        "gender": "Female (Intact)",
        "weight": 3.4,
        "conditions": "Past episode of mild URI",
        "allergies": "No known allergies",
        "notes": "Indoor cat with patio access.",
    },
]

# Sample Questionnaire for Consultation
SAMPLE_QUESTIONNAIRE = {
    "digestive": [
        {
            "id": "q1",
            "question": "Has your pet experienced vomiting within the last 24-48 hours?",
            "subtext": "Includes vomiting bile, foam, or undigested food",
            "followup": "Did the vomiting contain blood or dark coffee-ground appearance?",
        },
        {
            "id": "q2",
            "question": "Is your pet having loose stools or diarrhea?",
            "subtext": "Noticeable change from normal solid consistency",
            "followup": "Is there mucus or visible fresh red blood in the stool?",
        },
        {
            "id": "q3",
            "question": "Has there been a noticeable reduction in appetite or food refusal?",
            "subtext": "Skipped meals or refusing favorite treats",
            "followup": "Has the pet stopped drinking water as well?",
        },
        {
            "id": "q4",
            "question": "Does your pet show signs of abdominal discomfort or tenderness when touched?",
            "subtext": "Guarding the belly, whining, or adopting a prayer posture",
            "followup": "Does the abdomen feel tight, hard, or visibly bloated?",
        },
    ],
    "skin_coat": [
        {
            "id": "q1",
            "question": "Is your pet scratching, chewing, or licking their skin excessively?",
            "subtext": "Particularly paws, belly, ears, or base of the tail",
            "followup": "Has the persistent scratching created open wounds or scabs?",
        },
        {
            "id": "q2",
            "question": "Have you noticed patches of hair loss (alopecia)?",
            "subtext": "Circular bald spots or generalized thinning coat",
            "followup": "Is the skin under the bald patches red, inflamed, or darkened?",
        },
        {
            "id": "q3",
            "question": "Is there an unpleasant odor coming from the coat or skin?",
            "subtext": "Yeasty or foul smell even after grooming",
            "followup": "Is there greasy discharge or visible flakes?",
        },
    ],
}

# Generic fallback questions for remaining categories
DEFAULT_QUESTIONS = [
    {
        "id": "q1",
        "question": "Have you observed noticeable changes in your pet's energy or normal routine?",
        "subtext": "Sleeping more than usual, reluctance to move, or decreased interest in play",
        "followup": "Has this lethargy been progressive over more than 48 hours?",
    },
    {
        "id": "q2",
        "question": "Is your pet showing signs of physical pain or discomfort?",
        "subtext": "Vocalizing, trembling, limping, or hiding in quiet areas",
        "followup": "Does the discomfort worsen when moving or eating?",
    },
    {
        "id": "q3",
        "question": "Have you noticed any abnormal discharge (eyes, nose, mouth, ears)?",
        "subtext": "Clear, cloudy, green/yellow fluid, or foul odor",
        "followup": "Is the discharge accompanied by swelling or redness?",
    },
]

# Sample Diagnosis Result (Demo)
DEMO_DIAGNOSIS_RESULT = {
    "consultation_id": "CNS-2026-0842",
    "pet_name": "Luna",
    "species": "Cat",
    "category": "Digestive Health",
    "created_at": "2026-11-12 11:30 AM",
    "overall_severity": "High",
    "top_conditions": [
        {
            "condition": "Acute Feline Gastroenteritis",
            "confidence": 78,
            "severity": "High",
            "supporting_symptoms": [
                "Vomiting > 3 times in 24 hours",
                "Acute food refusal & lethargy",
                "Mild abdominal sensitivity",
            ],
            "missing_symptoms": [
                "Blood in stool",
                "Fever > 39.5°C",
                "Severe dehydration skin tenting",
            ],
            "explanation": "Reported acute onset of vomiting combined with complete anorexia and mild lethargy strongly aligns with gastrointestinal inflammation.",
            "next_steps": "Prompt veterinary evaluation within 12-24 hours to prevent rapid feline dehydration and hepatic lipidosis.",
        },
        {
            "condition": "Dietary Indiscretion / Mild Food Reaction",
            "confidence": 42,
            "severity": "Medium",
            "supporting_symptoms": [
                "Sudden vomiting episode",
                "Temporary appetite drop",
            ],
            "missing_symptoms": [
                "Confirmed ingestion of foreign body or garbage",
                "Persistent diarrhea",
            ],
            "explanation": "Often self-limiting, but less likely given the repeated vomiting and ongoing lethargy.",
            "next_steps": "Monitor hydration; do not give over-the-counter human medications.",
        },
        {
            "condition": "Gastrointestinal Foreign Body Obstruction",
            "confidence": 28,
            "severity": "Critical",
            "supporting_symptoms": [
                "Persistent vomiting",
                "Inability to keep liquids down",
            ],
            "missing_symptoms": [
                "Palpable abdominal mass",
                "Severe vocalization on touch",
                "Absence of defecation for >48h",
            ],
            "explanation": "Cannot be ruled out without physical veterinary palpation or abdominal radiographs.",
            "next_steps": "Requires clinical examination if vomiting persists despite withholding food.",
        },
    ],
}

# Sample Decision Explanation (Academic Requirement)
DEMO_DECISION_EXPLANATION = {
    "decision": "Visit Vet Today",
    "priority": "High",
    "color_token": "COLOR_WARNING",
    "why_selected": "Luna exhibits multiple acute digestive symptoms: recurring vomiting over a 24-hour period coupled with complete food refusal. In felines, persistent anorexia beyond 24-48 hours poses significant risk of secondary hepatic lipidosis, elevating clinical urgency from routine monitoring to same-day professional assessment.",
    "symptoms_influencing": [
        "Vomiting frequency: 4 episodes within 24 hours",
        "Refusal of both dry and wet food for 24+ hours",
        "Noticeable lethargy and withdrawal behavior",
    ],
    "severity_duration": "Severity scored as HIGH due to multi-symptom cluster (vomiting + anorexia) with rapid onset (< 24 hours duration).",
    "risk_factors": [
        "Species specific: Feline vulnerability to liver stress under acute anorexia",
        "Age: 3 years (prime adult, rapid dehydration risk if unaddressed)",
    ],
    "rules_influenced": [
        "RULE_DIG_014: IF vomiting >= 3 times/day AND anorexia == True THEN set_urgency('High')",
        "RULE_CAT_008: IF species == 'Cat' AND days_without_food >= 1 THEN flag_hepatic_lipidosis_risk()",
        "RULE_EMERG_CHECK: IF NO cyanosis AND NO hypothermia THEN allow_ambulatory_same_day()",
    ],
    "emergency_override": "No immediate life-threatening emergency indicators (such as cyanotic gums, dyspnea, or shock) were triggered. Therefore, the highest-tier 'Get Help Now' protocol was overridden in favor of a same-day appointment.",
    "alternatives_considered": [
        {
            "decision": "Get Help Now",
            "why_not": "Reserved for active shock, respiratory distress, or profuse hemorrhaging. Luna remains conscious and ambulatory.",
        },
        {
            "decision": "Book a Vet Visit",
            "why_not": "Routine 3-5 day booking is unsafe due to the rapid dehydration and feline fasting risk.",
        },
        {
            "decision": "Home Care & Monitor",
            "why_not": "Repeated vomiting and refusal of water makes home rehydration ineffective without clinical antiemetics.",
        },
    ],
    "recommended_actions": [
        "Contact your primary veterinary clinic to request a same-day urgent appointment.",
        "Withhold dry food for 2-4 hours, but keep clean fresh water accessible.",
        "Transport the cat in a secure, covered carrier to minimize stress.",
        "Do not administer human anti-nausea medications or painkillers under any circumstances.",
    ],
}

# Sample DSS Comparison Report (Decision Support System)
DEMO_DSS_REPORT = {
    "report_id": "DSS-REP-2026-004",
    "consultation_id": "CNS-2026-0842",
    "generated_at": "2026-11-12 11:35 AM",
    "pet_name": "Luna",
    "recommended_action": "Visit Vet Today",
    "urgency_level": "High (Level 2 of 4)",
    "primary_rationale": "Symptom concordance strongly points to Acute Gastroenteritis (78% match) with elevated clinical vulnerability due to feline physiology.",
    "condition_comparison": [
        {
            "Condition": "Acute Gastroenteritis",
            "Concordance": 78,
            "Severity": "High",
            "Evidence For": "Repeated vomiting, total anorexia, stomach tenderness",
            "Evidence Against": "No hematemesis, no extreme hyperthermia",
            "Action Urgency": "Visit Vet Today",
        },
        {
            "Condition": "Dietary Reaction",
            "Concordance": 42,
            "Severity": "Medium",
            "Evidence For": "Vomiting episode, mild discomfort",
            "Evidence Against": "Persistent anorexia, progressive lethargy",
            "Action Urgency": "Book a Vet Visit",
        },
        {
            "Condition": "GI Obstruction",
            "Concordance": 28,
            "Severity": "Critical",
            "Evidence For": "Inability to keep liquids down",
            "Evidence Against": "No hard distension, no palpable mass",
            "Action Urgency": "Get Help Now",
        },
    ],
    "criteria_weights": [
        {"Criterion": "Symptom Match", "Weight": 35, "Score": 82},
        {"Criterion": "Clinical Severity", "Weight": 25, "Score": 75},
        {"Criterion": "Feline Physiological Risk", "Weight": 20, "Score": 85},
        {"Criterion": "Time Duration Factor", "Weight": 20, "Score": 70},
    ],
}

# Sample Consultation History
DEMO_HISTORY = [
    {
        "id": "CNS-2026-0842",
        "date": "2026-11-12",
        "pet_name": "Luna",
        "species": "Cat",
        "category": "Digestive Health",
        "top_condition": "Acute Feline Gastroenteritis",
        "confidence": "78%",
        "decision": "Visit Vet Today",
        "status": "Completed",
    },
    {
        "id": "CNS-2026-0791",
        "date": "2026-11-04",
        "pet_name": "Max",
        "species": "Dog",
        "category": "Skin & Coat",
        "top_condition": "Canine Atopic Dermatitis",
        "confidence": "65%",
        "decision": "Book a Vet Visit",
        "status": "Completed",
    },
    {
        "id": "CNS-2026-0612",
        "date": "2026-10-22",
        "pet_name": "Bella",
        "species": "Cat",
        "category": "Eyes & Ears",
        "top_condition": "Mild Conjunctivitis",
        "confidence": "82%",
        "decision": "Home Care & Monitor",
        "status": "Resolved",
    },
    {
        "id": "CNS-2026-0503",
        "date": "2026-10-09",
        "pet_name": "Max",
        "species": "Dog",
        "category": "Urinary Health",
        "top_condition": "Urinary Tract Infection",
        "confidence": "72%",
        "decision": "Visit Vet Today",
        "status": "Resolved",
    },
]
