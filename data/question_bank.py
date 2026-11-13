"""Question bank and reference data for Diagnovet.

Exact data structures matching design_reference/diagnovet_flow.html.
"""

BREEDS = {
    "Dog": [
        "Labrador Retriever",
        "German Shepherd",
        "Golden Retriever",
        "Bulldog",
        "Pomeranian",
        "Other / Mixed Breed",
    ],
    "Cat": [
        "Persian",
        "Siamese",
        "British Shorthair",
        "Maine Coon",
        "Domestic Shorthair",
        "Other / Mixed Breed",
    ],
}

SYMPTOMS = {
    "Dog": ["Vomiting", "Diarrhoea", "Itching", "Coughing", "Limping", "Low appetite"],
    "Cat": [
        "Vomiting",
        "Sneezing",
        "Straining to urinate",
        "Hair loss",
        "Low appetite",
        "Hiding more",
    ],
}

FOLLOW_UPS = {
    "Vomiting": [
        "Has it happened more than twice today?",
        "Is there blood in the vomit?",
    ],
    "Diarrhoea": ["Is the stool watery?", "Is there blood or mucus in it?"],
    "Itching": ["Is the skin red or sore?", "Have you seen fleas?"],
    "Coughing": ["Is the cough worse at night?", "Does your pet gag after coughing?"],
    "Limping": ["Is the leg held off the ground?", "Is there swelling?"],
    "Low appetite": [
        "Is your pet also drinking less?",
        "Has this lasted more than a day?",
    ],
    "Sneezing": ["Is there eye or nose discharge?", "Does sneezing happen often?"],
    "Straining to urinate": [
        "Is little or no urine coming out?",
        "Is there blood in the urine?",
    ],
    "Hair loss": ["Are there bald patches?", "Is the skin flaky?"],
    "Hiding more": [
        "Has the behaviour changed suddenly?",
        "Is your pet eating less?",
    ],
}

EMERGENCY_QUESTIONS = [
    "Trouble breathing, or blue or pale gums?",
    "Collapse or a seizure?",
    "Possibly swallowed poison or a toxic item?",
]

CONDITIONS = {
    "Vomiting": ["Stomach upset", "Ate something unusual", "Gut infection"],
    "Diarrhoea": ["Diet-change upset", "Gut infection", "Intestinal worms"],
    "Itching": ["Skin allergy", "Fleas or mites", "Dry skin"],
    "Coughing": ["Kennel cough", "Airway irritation", "Heart-related cough"],
    "Limping": ["Muscle strain", "Joint pain", "Paw injury"],
    "Low appetite": ["Mild stomach upset", "Dental discomfort", "General illness"],
    "Sneezing": ["Cat flu", "Airway irritation", "Allergy"],
    "Straining to urinate": [
        "Urinary infection",
        "Bladder stones",
        "Urinary blockage",
    ],
    "Hair loss": ["Skin allergy", "Fleas or mites", "Stress grooming"],
    "Hiding more": ["Stress", "Pain", "General illness"],
}

DECISIONS = [
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
