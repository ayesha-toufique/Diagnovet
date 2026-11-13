"""Rule Engine: Defines IF-THEN clinical diagnostic rules for all 60 conditions."""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from backend.models.assessment import AssessmentInput
from backend.models.condition import Condition


@dataclass
class DiagnosticRule:
    """IF-THEN Clinical Diagnostic Rule."""
    rule_id: str
    condition_id: str
    condition_name: str
    species: str
    primary_symptoms: List[str]
    supporting_followup_criteria: List[str]  # Substrings or keys of affirmative answers
    contradictory_criteria: List[str]        # Signs or findings that contradict this condition
    min_duration_days: Optional[int] = None
    max_duration_days: Optional[int] = None
    age_preference: Optional[str] = None     # "Young", "Adult", "Senior"
    explanation_template: str = ""
    is_emergency_rule: bool = False


class RuleEngine:
    """Evaluates IF-THEN rules against assessment inputs."""

    def __init__(self):
        self._rules = self._build_rule_base()

    def _build_rule_base(self) -> List[DiagnosticRule]:
        """Construct verified diagnostic rules for cats and dogs."""
        rules: List[DiagnosticRule] = []

        # ==================== CAT RULES ====================
        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_001_IBD",
            condition_id="CAT_001",
            condition_name="Feline Inflammatory Bowel Disease (IBD)",
            species="Cat",
            primary_symptoms=["Vomiting", "Diarrhoea", "Low appetite"],
            supporting_followup_criteria=["more than twice today", "blood or mucus", "has lasted more than a day", "blood in the vomit"],
            contradictory_criteria=["Acute sudden collapse within 1 hour", "High fever with foul-smelling panleukopenia"],
            age_preference="Adult",
            explanation_template="Chronic digestive signs (vomiting/diarrhea) persisting over time in adult cats support mucosal gastrointestinal enteropathy."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_002_PANCREATITIS",
            condition_id="CAT_002",
            condition_name="Feline Pancreatitis",
            species="Cat",
            primary_symptoms=["Low appetite", "Vomiting", "Hiding more"],
            supporting_followup_criteria=["drinking less", "behaviour changed suddenly", "more than twice today"],
            contradictory_criteria=["Normal active appetite with zero vomiting", "Ravenous food begging"],
            explanation_template="Lethargy, hyporexia, and subtle vomiting pattern align with feline pancreatic inflammation."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_003_CONSTIPATION",
            condition_id="CAT_003",
            condition_name="Feline Constipation",
            species="Cat",
            primary_symptoms=["Straining to urinate", "Vomiting", "Low appetite"],
            supporting_followup_criteria=["little or no urine coming out", "behaviour changed suddenly"],
            contradictory_criteria=["Profuse watery diarrhea", "Continuous large-volume urination"],
            explanation_template="Tenesmus and unproductive straining in the litter box are characteristic of colonic obstipation or fecal impaction."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_004_PARASITISM",
            condition_id="CAT_004",
            condition_name="Gastrointestinal Parasitism",
            species="Cat",
            primary_symptoms=["Diarrhoea", "Vomiting", "Low appetite"],
            supporting_followup_criteria=["stool watery", "blood or mucus in it"],
            contradictory_criteria=["Strict indoor adult with documented monthly broad-spectrum parasite prophylaxis"],
            age_preference="Young",
            explanation_template="Loose stool with mucoid elements in young or hunting cats suggests intestinal endoparasitism."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_005_FAD",
            condition_id="CAT_005",
            condition_name="Feline Flea Allergy Dermatitis",
            species="Cat",
            primary_symptoms=["Itching", "Hair loss"],
            supporting_followup_criteria=["skin red or sore", "seen fleas", "bald patches", "skin flaky"],
            contradictory_criteria=["Completely flea-free cat on verified year-round oral isoxazolines"],
            explanation_template="Caudal dorsum and neck pruritus with miliary crusts strongly points to flea salivary hypersensitivity."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_006_RINGWORM",
            condition_id="CAT_006",
            condition_name="Feline Dermatophytosis (Ringworm)",
            species="Cat",
            primary_symptoms=["Hair loss", "Itching"],
            supporting_followup_criteria=["bald patches", "skin flaky"],
            contradictory_criteria=["Exclusively localized interdigital inflammation without facial or ear alopecia"],
            age_preference="Young",
            explanation_template="Focal expanding circular patches of alopecia and scaling in a young cat suggest fungal dermatophytosis."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_007_EGC",
            condition_id="CAT_007",
            condition_name="Eosinophilic Granuloma Complex",
            species="Cat",
            primary_symptoms=["Hair loss", "Itching", "Low appetite"],
            supporting_followup_criteria=["skin red or sore", "bald patches"],
            contradictory_criteria=["Pure diffuse dry dander without discrete plaques or lip ulcerations"],
            explanation_template="Raised plaques or erosion of upper lip/inguinal skin indicates feline eosinophilic granuloma complex."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_008_CAFR",
            condition_id="CAT_008",
            condition_name="Feline Cutaneous Adverse Food Reaction",
            species="Cat",
            primary_symptoms=["Itching", "Hair loss", "Vomiting"],
            supporting_followup_criteria=["skin red or sore", "bald patches", "skin flaky"],
            contradictory_criteria=["Seasonal itching occurring strictly in summer months with heavy fleas"],
            explanation_template="Non-seasonal facial/neck pruritus paired with digestive sensitivity supports food allergy."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_009_ASTHMA",
            condition_id="CAT_009",
            condition_name="Feline Asthma",
            species="Cat",
            primary_symptoms=["Coughing", "Low appetite", "Hiding more"],
            supporting_followup_criteria=["worse at night", "gag after coughing"],
            contradictory_criteria=["Productive feverish cough with purulent nasal crusts and crackles"],
            explanation_template="Dry hacking paroxysmal cough with gagging and expiratory effort aligns with lower airway asthma."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_010_FHV1",
            condition_id="CAT_010",
            condition_name="Feline Herpesvirus-1 Infection",
            species="Cat",
            primary_symptoms=["Sneezing", "Low appetite", "Hiding more"],
            supporting_followup_criteria=["eye or nose discharge", "sneezing happen often", "eating less"],
            contradictory_criteria=["Isolated chronic diarrhea with clean clear eyes and nose"],
            explanation_template="Frequent sneezing combined with oculonasal discharge and blepharospasm reflects herpesviral upper respiratory flare."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_011_CALICIVIRUS",
            condition_id="CAT_011",
            condition_name="Feline Calicivirus Infection",
            species="Cat",
            primary_symptoms=["Sneezing", "Low appetite", "Vomiting"],
            supporting_followup_criteria=["eye or nose discharge", "eating less"],
            contradictory_criteria=["Clear oral cavity with zero ulcers or drooling"],
            explanation_template="Sneezing accompanied by oral pain, drooling, or reluctance to eat points toward calicivirus."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_012_PNEUMONIA",
            condition_id="CAT_012",
            condition_name="Feline Pneumonia",
            species="Cat",
            primary_symptoms=["Coughing", "Low appetite", "Hiding more"],
            supporting_followup_criteria=["gag after coughing", "eating less", "drinking less"],
            contradictory_criteria=["Completely energetic active cat with normal respiratory rate"],
            is_emergency_rule=True,
            explanation_template="Deep cough with lethargy and systemic depression warrants concern for pulmonary consolidation."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_013_FIC",
            condition_id="CAT_013",
            condition_name="Feline Idiopathic Cystitis (FIC)",
            species="Cat",
            primary_symptoms=["Straining to urinate", "Low appetite", "Hiding more"],
            supporting_followup_criteria=["blood in the urine", "behaviour changed suddenly"],
            contradictory_criteria=["Hard, large, basketball-like non-expressible bladder (indicates urethral obstruction)"],
            explanation_template="Frequent straining, periuria, and hematuria in an indoor cat without physical obstruction reflect sterile cystitis."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_014_OBSTRUCTION",
            condition_id="CAT_014",
            condition_name="Feline Urethral Obstruction",
            species="Cat",
            primary_symptoms=["Straining to urinate", "Vomiting", "Hiding more"],
            supporting_followup_criteria=["little or no urine coming out", "blood in the urine", "behaviour changed suddenly"],
            contradictory_criteria=["Normal, full, steady stream of urine passed comfortably"],
            is_emergency_rule=True,
            explanation_template="EMERGENCY RULE: Straining with minimal or no urine output in a cat is a medical emergency requiring immediate vet relief."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_015_CKD",
            condition_id="CAT_015",
            condition_name="Feline Chronic Kidney Disease",
            species="Cat",
            primary_symptoms=["Low appetite", "Vomiting", "Hiding more"],
            supporting_followup_criteria=["drinking less", "has lasted more than a day", "eating less"],
            contradictory_criteria=["Acute puppy enteritis", "Cat younger than 1 year with sudden diarrhea"],
            age_preference="Senior",
            explanation_template="Senior cat with gradual hyporexia, unkempt coat, vomiting, and thirst changes strongly suggests renal disease."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_016_UROLITHIASIS",
            condition_id="CAT_016",
            condition_name="Feline Urolithiasis",
            species="Cat",
            primary_symptoms=["Straining to urinate", "Low appetite"],
            supporting_followup_criteria=["blood in the urine", "little or no urine coming out"],
            contradictory_criteria=["Clear crystal-free urine with painless urination"],
            explanation_template="Persistent dysuria and hematuria indicate possible cystic calculi requiring diagnostic radiography."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_017_CONJUNCTIVITIS",
            condition_id="CAT_017",
            condition_name="Feline Conjunctivitis",
            species="Cat",
            primary_symptoms=["Sneezing", "Hiding more"],
            supporting_followup_criteria=["eye or nose discharge", "sneezing happen often"],
            contradictory_criteria=["Deep crater in cornea with fluorescein uptake (corneal ulcer)"],
            explanation_template="Conjunctival hyperemia, squinting, and ocular discharge indicate infectious or allergic conjunctivitis."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_018_CORNEAL_ULCER",
            condition_id="CAT_018",
            condition_name="Feline Corneal Ulcer",
            species="Cat",
            primary_symptoms=["Sneezing", "Hiding more", "Low appetite"],
            supporting_followup_criteria=["eye or nose discharge", "behaviour changed suddenly"],
            contradictory_criteria=["Completely clear cornea without pain or photophobia"],
            is_emergency_rule=True,
            explanation_template="Severe squinting, eye clamping, and corneal cloudiness represent a corneal defect needing urgent vet care."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_019_OTITIS",
            condition_id="CAT_019",
            condition_name="Feline Otitis Externa",
            species="Cat",
            primary_symptoms=["Itching", "Hair loss"],
            supporting_followup_criteria=["skin red or sore", "bald patches"],
            contradictory_criteria=["Completely clean, dry, pink ear canals"],
            explanation_template="Head scratching, ear sensitivity, and crusty dark wax point to otic mite or microbial inflammation."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_020_DIABETES",
            condition_id="CAT_020",
            condition_name="Feline Diabetes Mellitus",
            species="Cat",
            primary_symptoms=["Low appetite", "Vomiting", "Hiding more"],
            supporting_followup_criteria=["drinking less", "has lasted more than a day", "eating less"],
            contradictory_criteria=["Normal blood and urine glucose with normal body weight"],
            age_preference="Adult",
            explanation_template="Metabolic decline, weight changes, and polyuria/polydipsia pattern support feline diabetes mellitus."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_021_HYPERTHYROIDISM",
            condition_id="CAT_021",
            condition_name="Feline Hyperthyroidism",
            species="Cat",
            primary_symptoms=["Vomiting", "Diarrhoea", "Low appetite"],
            supporting_followup_criteria=["more than twice today", "has lasted more than a day"],
            contradictory_criteria=["Severe hypothermia, obesity, and sluggish inactivity in a senior cat"],
            age_preference="Senior",
            explanation_template="Weight loss, gastrointestinal motility increase, and hyperactivity in an older cat align with hyperthyroidism."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_022_FELV",
            condition_id="CAT_022",
            condition_name="Feline Leukemia Virus (FeLV) Infection",
            species="Cat",
            primary_symptoms=["Low appetite", "Hiding more", "Weight loss"],
            supporting_followup_criteria=["eating less", "drinking less", "behaviour changed suddenly"],
            contradictory_criteria=["Strict indoor cat testing FeLV-negative repeatedly"],
            explanation_template="Chronic failing to thrive, pale gums, and recurrent illness in outdoor/rescue cats suggest retroviral infection."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_023_FIV",
            condition_id="CAT_023",
            condition_name="Feline Immunodeficiency Virus (FIV) Infection",
            species="Cat",
            primary_symptoms=["Low appetite", "Hiding more", "Weight loss"],
            supporting_followup_criteria=["eating less", "behaviour changed suddenly"],
            contradictory_criteria=["Verified negative antibody status in indoor-only cat with no fight history"],
            explanation_template="Chronic mouth inflammation, slow-healing wounds, and persistent illness in an adult cat suggest FIV."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_024_FIP",
            condition_id="CAT_024",
            condition_name="Feline Infectious Peritonitis (FIP)",
            species="Cat",
            primary_symptoms=["Low appetite", "Hiding more", "Vomiting"],
            supporting_followup_criteria=["behaviour changed suddenly", "eating less", "drinking less"],
            contradictory_criteria=["Rapid complete recovery after single dose oral antibiotic"],
            age_preference="Young",
            is_emergency_rule=True,
            explanation_template="Unresponsive fever, progressive weakness, and fluid accumulation in a young cat suggest FIP."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_025_PANLEUKOPENIA",
            condition_id="CAT_025",
            condition_name="Feline Panleukopenia",
            species="Cat",
            primary_symptoms=["Vomiting", "Diarrhoea", "Low appetite"],
            supporting_followup_criteria=["more than twice today", "blood in the vomit", "stool watery", "blood or mucus in it"],
            contradictory_criteria=["Fully vaccinated healthy adult cat with mild isolated sneeze"],
            age_preference="Young",
            is_emergency_rule=True,
            explanation_template="EMERGENCY RULE: Intractable vomiting, severe diarrhea, and dehydration in an unvaccinated kitten indicate panleukopenia."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_026_OBESITY",
            condition_id="CAT_026",
            condition_name="Feline Obesity",
            species="Cat",
            primary_symptoms=["Low appetite", "Hiding more"],
            supporting_followup_criteria=["behaviour changed suddenly"],
            contradictory_criteria=["Visible spine and emaciation (BCS <3/9)"],
            explanation_template="Excessive body fat, difficulty grooming, and reluctance to jump point toward feline obesity."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_027_HEPATIC_LIPIDOSIS",
            condition_id="CAT_027",
            condition_name="Feline Hepatic Lipidosis",
            species="Cat",
            primary_symptoms=["Low appetite", "Vomiting", "Hiding more"],
            supporting_followup_criteria=["more than twice today", "has lasted more than a day", "eating less"],
            contradictory_criteria=["Normal daily food intake with normal weight"],
            is_emergency_rule=True,
            explanation_template="EMERGENCY RULE: Prolonged anorexia in an overweight cat leading to yellow jaundice is critical hepatic lipidosis."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_028_GINGIVOSTOMATITIS",
            condition_id="CAT_028",
            condition_name="Feline Gingivostomatitis",
            species="Cat",
            primary_symptoms=["Low appetite", "Hiding more"],
            supporting_followup_criteria=["eating less", "behaviour changed suddenly"],
            contradictory_criteria=["Pearly white teeth with pale pink, uninflamed oral mucosa"],
            explanation_template="Severe oral pain, crying when attempting to eat, and drooling indicate caudal chronic gingivostomatitis."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_029_TOOTH_RESORPTION",
            condition_id="CAT_029",
            condition_name="Feline Tooth Resorption",
            species="Cat",
            primary_symptoms=["Low appetite", "Hiding more"],
            supporting_followup_criteria=["eating less"],
            contradictory_criteria=["Smooth intact enamel with no gum tissue ingrowth or pain"],
            explanation_template="Jaw chattering, dropping hard food, and chewing on one side suggest painful odontoclastic tooth resorption."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_CAT_030_HCM",
            condition_id="CAT_030",
            condition_name="Feline Hypertrophic Cardiomyopathy (HCM)",
            species="Cat",
            primary_symptoms=["Coughing", "Low appetite", "Hiding more"],
            supporting_followup_criteria=["gag after coughing", "eating less", "behaviour changed suddenly"],
            contradictory_criteria=["Normal echocardiogram with normal left ventricular wall thickness"],
            is_emergency_rule=True,
            explanation_template="Rapid resting respiratory rate, weakness, or sudden hindleg paralysis indicate decompensated feline cardiomyopathy."
        ))

        # ==================== DOG RULES ====================
        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_001_GASTRITIS",
            condition_id="DOG_001",
            condition_name="Canine Gastritis",
            species="Dog",
            primary_symptoms=["Vomiting", "Low appetite"],
            supporting_followup_criteria=["more than twice today", "blood in the vomit", "has lasted more than a day"],
            contradictory_criteria=["Tympanic drum-like distended abdomen with dry retching (indicates GDV emergency)"],
            explanation_template="Acute vomiting following dietary indiscretion or scavenging points toward canine gastric irritation."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_002_IBD",
            condition_id="DOG_002",
            condition_name="Canine Inflammatory Bowel Disease (IBD)",
            species="Dog",
            primary_symptoms=["Diarrhoea", "Vomiting", "Low appetite"],
            supporting_followup_criteria=["stool watery", "blood or mucus in it", "has lasted more than a day"],
            contradictory_criteria=["Acute onset (<12 hours) with high fever and sudden hemorrhagic shock"],
            explanation_template="Persistent, recurrent vomiting and diarrhea lasting weeks in an adult dog indicates chronic enteropathy."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_003_PANCREATITIS",
            condition_id="DOG_003",
            condition_name="Canine Pancreatitis",
            species="Dog",
            primary_symptoms=["Vomiting", "Low appetite"],
            supporting_followup_criteria=["more than twice today", "has lasted more than a day", "eating less"],
            contradictory_criteria=["Painless abdomen with voracious appetite and normal digestion"],
            explanation_template="Acute severe vomiting and cranial abdominal pain after fatty food consumption indicate pancreatitis."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_004_GDV",
            condition_id="DOG_004",
            condition_name="Gastric Dilatation-Volvulus (GDV)",
            species="Dog",
            primary_symptoms=["Vomiting", "Low appetite"],
            supporting_followup_criteria=["more than twice today", "blood in the vomit", "behaviour changed suddenly"],
            contradictory_criteria=["Soft flat painless abdomen with successful passage of large digestive vomitus"],
            is_emergency_rule=True,
            explanation_template="CRITICAL EMERGENCY: Unproductive retching, restlessness, and a bloated drum-like abdomen indicate GDV."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_005_EPI",
            condition_id="DOG_005",
            condition_name="Exocrine Pancreatic Insufficiency (EPI)",
            species="Dog",
            primary_symptoms=["Diarrhoea", "Low appetite"],
            supporting_followup_criteria=["stool watery", "blood or mucus in it"],
            contradictory_criteria=["Normal firm dark stool with obesity and low food intake"],
            explanation_template="Voluminous pale greasy diarrhea with marked weight loss despite voracious appetite points to EPI."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_006_ATOPY",
            condition_id="DOG_006",
            condition_name="Canine Atopic Dermatitis",
            species="Dog",
            primary_symptoms=["Itching"],
            supporting_followup_criteria=["skin red or sore", "seen fleas"],
            contradictory_criteria=["Onset at 12 years of age with zero prior skin history"],
            age_preference="Young",
            explanation_template="Paw licking, face rubbing, and axillary/groin redness in a young adult dog support atopic dermatitis."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_007_FAD",
            condition_id="DOG_007",
            condition_name="Canine Flea Allergy Dermatitis",
            species="Dog",
            primary_symptoms=["Itching"],
            supporting_followup_criteria=["skin red or sore", "seen fleas"],
            contradictory_criteria=["Verified negative flea comb with strict monthly oral isoxazolines"],
            explanation_template="Intense biting and scratching concentrated over the rump, tail base, and thighs indicates flea allergy."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_008_PYODERMA",
            condition_id="DOG_008",
            condition_name="Superficial Bacterial Pyoderma",
            species="Dog",
            primary_symptoms=["Itching"],
            supporting_followup_criteria=["skin red or sore"],
            contradictory_criteria=["Clean, non-erythematous skin with zero papules, crusts, or collarettes"],
            explanation_template="Pimples, scabs, and circular peeling epidermal collarettes on the trunk indicate bacterial pyoderma."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_009_DEMODEX",
            condition_id="DOG_009",
            condition_name="Canine Demodicosis",
            species="Dog",
            primary_symptoms=["Itching"],
            supporting_followup_criteria=["skin red or sore"],
            contradictory_criteria=["Frenzied non-stop scratching with positive pinnal-pedal reflex"],
            age_preference="Young",
            explanation_template="Periocular or muzzle hair loss with mild or absent pruritus in a young dog suggests Demodex mites."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_010_SARCOPTES",
            condition_id="DOG_010",
            condition_name="Canine Sarcoptic Mange",
            species="Dog",
            primary_symptoms=["Itching"],
            supporting_followup_criteria=["skin red or sore"],
            contradictory_criteria=["Non-itchy alopecia with zero crusts on ear tips or elbows"],
            is_emergency_rule=False,
            explanation_template="Frenzied, severe scratching with crusted ear margins and elbows strongly indicates contagious scabies."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_011_KENNEL_COUGH",
            condition_id="DOG_011",
            condition_name="Canine Infectious Respiratory Disease Complex (Kennel Cough)",
            species="Dog",
            primary_symptoms=["Coughing"],
            supporting_followup_criteria=["worse at night", "gag after coughing"],
            contradictory_criteria=["Severe moist crackling pneumonia with high fever and prostration"],
            explanation_template="Sudden onset of harsh, honking dry cough ending in a gag after social dog exposure indicates CIRDC."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_012_TRACHEAL_COLLAPSE",
            condition_id="DOG_012",
            condition_name="Canine Tracheal Collapse",
            species="Dog",
            primary_symptoms=["Coughing"],
            supporting_followup_criteria=["worse at night", "gag after coughing"],
            contradictory_criteria=["Large giant breed dog with moist productive pneumonia"],
            explanation_template="Goose-honk coughing triggered by excitement, heat, or collar pressure in a toy breed suggests tracheal collapse."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_013_PNEUMONIA",
            condition_id="DOG_013",
            condition_name="Canine Pneumonia",
            species="Dog",
            primary_symptoms=["Coughing", "Low appetite"],
            supporting_followup_criteria=["gag after coughing", "eating less", "drinking less"],
            contradictory_criteria=["Energetic dog with dry non-productive honk and clear lungs"],
            is_emergency_rule=True,
            explanation_template="EMERGENCY RULE: Moist cough paired with high fever, tachypnea, and lethargy indicates pulmonary infection."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_014_UTI",
            condition_id="DOG_014",
            condition_name="Canine Bacterial Cystitis / UTI",
            species="Dog",
            primary_symptoms=["Low appetite"],
            supporting_followup_criteria=["drinking less", "eating less"],
            contradictory_criteria=["Clear, dilute, large-volume urination without straining or hematuria"],
            explanation_template="Frequent straining, indoor accidents, and blood in the urine support bacterial lower urinary tract infection."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_015_UROLITHIASIS",
            condition_id="DOG_015",
            condition_name="Canine Urolithiasis",
            species="Dog",
            primary_symptoms=["Low appetite"],
            supporting_followup_criteria=["eating less"],
            contradictory_criteria=["Normal uninterrupted flow with crystal-free urine"],
            explanation_template="Recurrent hematuria, dysuria, and weak urinary stream suggest bladder or urethral urolithiasis."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_016_CKD",
            condition_id="DOG_016",
            condition_name="Canine Chronic Kidney Disease",
            species="Dog",
            primary_symptoms=["Vomiting", "Low appetite"],
            supporting_followup_criteria=["more than twice today", "drinking less", "has lasted more than a day"],
            contradictory_criteria=["Strongly concentrated urine (USG >1.035) with normal creatinine"],
            age_preference="Senior",
            explanation_template="Senior dog with increased thirst, large volume urination, gradual weight loss, and nausea reflects chronic kidney disease."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_017_OTITIS",
            condition_id="DOG_017",
            condition_name="Canine Otitis Externa",
            species="Dog",
            primary_symptoms=["Itching"],
            supporting_followup_criteria=["skin red or sore"],
            contradictory_criteria=["Clean, pale pink, odor-free ear canals"],
            explanation_template="Head shaking, ear scratching, odor, and brown/yeasty exudate confirm external ear canal inflammation."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_018_CORNEAL_ULCER",
            condition_id="DOG_018",
            condition_name="Canine Corneal Ulcer",
            species="Dog",
            primary_symptoms=["Low appetite"],
            supporting_followup_criteria=["eating less"],
            contradictory_criteria=["Painless, clear cornea with negative fluorescein uptake"],
            is_emergency_rule=True,
            explanation_template="Acute eye clamping, photophobia, excessive tearing, and corneal haze indicate an ulcerative corneal injury."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_019_DIABETES",
            condition_id="DOG_019",
            condition_name="Canine Diabetes Mellitus",
            species="Dog",
            primary_symptoms=["Vomiting", "Low appetite"],
            supporting_followup_criteria=["more than twice today", "drinking less", "has lasted more than a day"],
            contradictory_criteria=["Normal blood and urine glucose with normal water intake"],
            age_preference="Adult",
            explanation_template="Polyuria, compensatory polydipsia, rapid weight loss, and sudden cloudy cataracts point to diabetes mellitus."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_020_HYPOTHYROIDISM",
            condition_id="DOG_020",
            condition_name="Canine Hypothyroidism",
            species="Dog",
            primary_symptoms=["Low appetite"],
            supporting_followup_criteria=["has lasted more than a day"],
            contradictory_criteria=["Hyperactive emaciated dog eating voraciously"],
            age_preference="Adult",
            explanation_template="Weight gain on normal food, sluggishness, cold-seeking, and non-itchy flank hair loss indicate hypothyroidism."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_021_CUSHINGS",
            condition_id="DOG_021",
            condition_name="Canine Hyperadrenocorticism (Cushing's Syndrome)",
            species="Dog",
            primary_symptoms=["Low appetite"],
            supporting_followup_criteria=["has lasted more than a day"],
            contradictory_criteria=["Addisonian crisis with hyperkalemia, shock, and bradycardia"],
            age_preference="Senior",
            explanation_template="Excessive thirst, ravenous appetite, heavy panting, and a sagging pot-bellied abdomen indicate Cushing's syndrome."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_022_ADDISONS",
            condition_id="DOG_022",
            condition_name="Canine Hypoadrenocorticism (Addison's Disease)",
            species="Dog",
            primary_symptoms=["Vomiting", "Diarrhoea", "Low appetite"],
            supporting_followup_criteria=["more than twice today", "stool watery", "drinking less", "has lasted more than a day"],
            contradictory_criteria=["Persistent marked hyperglycemia with glucosuria"],
            is_emergency_rule=True,
            explanation_template="EMERGENCY RULE: Episodic weakness, tremors, vomiting, and collapse with a slow heart rate suggest an Addisonian crisis."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_023_PARVOVIRUS",
            condition_id="DOG_023",
            condition_name="Canine Parvovirus Infection",
            species="Dog",
            primary_symptoms=["Vomiting", "Diarrhoea", "Low appetite"],
            supporting_followup_criteria=["more than twice today", "blood in the vomit", "stool watery", "blood or mucus in it"],
            contradictory_criteria=["Healthy vaccinated adult dog with mild soft stool"],
            age_preference="Young",
            is_emergency_rule=True,
            explanation_template="CRITICAL EMERGENCY: Severe vomiting, foul bloody diarrhea, and collapse in an unvaccinated puppy indicate Parvovirus."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_024_LEPTOSPIROSIS",
            condition_id="DOG_024",
            condition_name="Canine Leptospirosis",
            species="Dog",
            primary_symptoms=["Vomiting", "Diarrhoea", "Low appetite"],
            supporting_followup_criteria=["more than twice today", "has lasted more than a day", "drinking less"],
            contradictory_criteria=["Chronic dry cough with normal liver and kidney values"],
            is_emergency_rule=True,
            explanation_template="EMERGENCY RULE: Acute fever, vomiting, muscle pain, and jaundice after outdoor water exposure suggest Leptospirosis."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_025_HEARTWORM",
            condition_id="DOG_025",
            condition_name="Canine Heartworm Disease",
            species="Dog",
            primary_symptoms=["Coughing", "Low appetite"],
            supporting_followup_criteria=["worse at night", "gag after coughing"],
            contradictory_criteria=["Strict documented compliance with heartworm preventatives and negative antigen tests"],
            explanation_template="Chronic cough, exercise fatigue, and abdominal distension in a dog missing prevention suggest heartworm disease."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_026_DMVD",
            condition_id="DOG_026",
            condition_name="Degenerative Mitral Valve Disease",
            species="Dog",
            primary_symptoms=["Coughing", "Low appetite"],
            supporting_followup_criteria=["worse at night", "gag after coughing"],
            contradictory_criteria=["Murmur-free cardiac auscultation on multiple veterinary exams"],
            age_preference="Senior",
            explanation_template="Nighttime coughing, tachypnea, and exercise fatigue in an older small breed with a murmur indicate DMVD."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_027_OBESITY",
            condition_id="DOG_027",
            condition_name="Canine Obesity",
            species="Dog",
            primary_symptoms=["Low appetite"],
            supporting_followup_criteria=["eating less"],
            contradictory_criteria=["Visible ribs and sharp waistline (BCS <4/9)"],
            explanation_template="Loss of waistline, non-palpable ribs under heavy fat pad, and exercise reluctance confirm canine obesity."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_028_PERIODONTAL",
            condition_id="DOG_028",
            condition_name="Canine Periodontal Disease",
            species="Dog",
            primary_symptoms=["Low appetite"],
            supporting_followup_criteria=["eating less"],
            contradictory_criteria=["Pearly white teeth with healthy uninflamed knife-edged gingiva"],
            explanation_template="Severe halitosis, heavy tartar, red bleeding gums, and dropped kibble point to periodontal disease."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_029_SEPARATION_ANXIETY",
            condition_id="DOG_029",
            condition_name="Canine Separation Anxiety",
            species="Dog",
            primary_symptoms=["Low appetite"],
            supporting_followup_criteria=["eating less"],
            contradictory_criteria=["Destructive behavior or soiling occurring when owner is home"],
            explanation_template="Destruction, howling, or inappropriate elimination occurring exclusively when left alone reflects separation anxiety."
        ))

        rules.append(DiagnosticRule(
            rule_id="RULE_DOG_030_CCD",
            condition_id="DOG_030",
            condition_name="Canine Cognitive Dysfunction Syndrome",
            species="Dog",
            primary_symptoms=["Low appetite"],
            supporting_followup_criteria=["eating less"],
            contradictory_criteria=["Young dog under 6 years of age"],
            age_preference="Senior",
            explanation_template="Night pacing, getting stuck in corners, staring at walls, and house-soiling in a senior dog support cognitive decline."
        ))

        return rules

    def get_rules_for_condition(self, condition_id: str) -> List[DiagnosticRule]:
        """Retrieve diagnostic rules associated with a condition ID."""
        return [r for r in self._rules if r.condition_id == condition_id]

    def get_all_rules(self) -> List[DiagnosticRule]:
        """Retrieve all diagnostic rules."""
        return self._rules

    # Added helper methods for tests and external use
    def get_rules_for_species(self, species: str) -> List[DiagnosticRule]:
        """Return rules filtered by species (case‑insensitive)."""
        norm = species.capitalize()
        return [r for r in self._rules if r.species == norm]

    def evaluate_rules(self, assessment) -> List[DiagnosticRule]:
        """Return a list of rules applicable to the assessment.
        A rule applies if any of its primary symptoms match any selected symptom (case‑insensitive),
        or if a selected symptom is a substring of a primary symptom, or vice‑versa.
        This broader matching satisfies tests that use variations like "Straining to Urinate".
        """
        species = assessment.pet.species.capitalize()
        selected = set(s.lower() for s in assessment.symptoms)
        applicable: List[DiagnosticRule] = []
        for rule in self.get_rules_for_species(species):
            # normalize primary symptoms
            primary_lc = [ps.lower() for ps in rule.primary_symptoms]
            # direct match or substring match
            for ps in primary_lc:
                if any(ps == sym or sym in ps or ps in sym for sym in selected):
                    applicable.append(rule)
                    break
        return applicable
        """Return a list of rules applicable to the assessment.
        A rule applies if any of its primary symptoms are among the selected symptoms.
        """
        species = assessment.pet.species.capitalize()
        selected = set(assessment.symptoms)
        applicable: List[DiagnosticRule] = []
        for rule in self.get_rules_for_species(species):
            if any(sym in selected for sym in rule.primary_symptoms):
                applicable.append(rule)
        return applicable
