# Diagnovet: Manual Testing & Academic Architecture Guide

**System:** Diagnovet Veterinary Expert System (Cats & Dogs)  
**Academic Version:** Phase 2 Complete Implementation  
**Primary Engine:** Deterministic Rule-Based Expert System (Forward Chaining)  
**Target Species:** Feline (*Felis catus*) and Canine (*Canis lupus familiaris*)  
**Source Repository:** `D:\Diagnovet`  
**Date of Verification:** 2026-11-13  

---

## Table of Contents
1. [Assessment Question Flow & Answer Options (Cats vs. Dogs)](#1-assessment-question-flow--answer-options-cats-vs-dogs)
2. [Conditional Follow-Up Questions & Trigger Conditions](#2-conditional-follow-up-questions--trigger-conditions)
3. [Complete Veterinary Knowledge Base (All 60 Conditions)](#3-complete-veterinary-knowledge-base-all-60-conditions)
4. [Facts Taxonomy: Static, Dynamic, and Inferred Facts](#4-facts-taxonomy-static-dynamic-and-inferred-facts)
5. [Complete Clinical IF-THEN Rules (All 60 Rules)](#5-complete-clinical-if-then-rules-all-60-rules)
6. [Working Memory Structure & Session State Representation](#6-working-memory-structure--session-state-representation)
7. [Rule Matcher Implementation](#7-rule-matcher-implementation)
8. [Forward-Chaining Inference Engine: Step-by-Step Mechanics](#8-forward-chaining-inference-engine-step-by-step-mechanics)
9. [Conflict Resolution & Tie-Breaking Method](#9-conflict-resolution--tie-breaking-method)
10. [Diagnosis Engine: Scoring, Ranking, and Tiering](#10-diagnosis-engine-scoring-ranking-and-tiering)
11. [Clinical Decision-Making System & Emergency Overrides](#11-clinical-decision-making-system--emergency-overrides)
12. [Decision Support System (DSS) Mechanics](#12-decision-support-system-dss-mechanics)
13. [Care Guidance Logic & Precaution Framework](#13-care-guidance-logic--precaution-framework)
14. [Detailed Manual Testing Scenarios (Exact Inputs & Expected Outputs)](#14-detailed-manual-testing-scenarios-exact-inputs--expected-outputs)
15. [Implementation Status Audit: Implemented vs. Placeholders vs. Missing](#15-implementation-status-audit-implemented-vs-placeholders-vs-missing)

---

## 1. Assessment Question Flow & Answer Options (Cats vs. Dogs)

The assessment flow is structured into **6 sequential steps** executed across `views/pet_information.py`, `views/assessment.py`, and `views/review.py`.

```
[Step 1: Pet Info] ──> [Step 2: Symptoms] ──> [Step 3: Follow-Ups] ──> [Step 4: Timing & Severity] ──> [Step 5: Emergency Check] ──> [Step 6: Review Answers]
```

### Step 1: Pet Information (`views/pet_information.py`)
This step establishes the demographic working memory (`PetProfile`).

| Field / Prompt Label | UI Component | Cat Answer Options | Dog Answer Options | Validation Constraints |
|---|---|---|---|---|
| **Species** | Chip Buttons | `🐱 Cat` | `🐶 Dog` | Mandatory. User must choose one. |
| **Breed** | Dropdown (`st.selectbox`) | `Choose a breed`, `Persian`, `Siamese`, `British Shorthair`, `Maine Coon`, `Domestic Shorthair`, `Other / Mixed Breed` | `Choose a breed`, `Labrador Retriever`, `German Shepherd`, `Golden Retriever`, `Bulldog`, `Pomeranian`, `Other / Mixed Breed` | Mandatory. Cannot be `Choose a breed` or `Choose species first`. |
| **Gender** | Dropdown (`st.selectbox`) | `Choose`, `Male`, `Female` | `Choose`, `Male`, `Female` | Mandatory. Cannot be `Choose`. |
| **Age (years)** | Text Input (`st.text_input`) | Real number string (e.g. `2`, `0.5`, `12`) | Real number string (e.g. `3`, `1.5`, `9`) | Mandatory. `0.0 <= float(age) <= 30.0`. |
| **Weight in kg (optional)** | Text Input (`st.text_input`) | Real number string (e.g. `4.5`) | Real number string (e.g. `25.0`) | Optional. If provided: `0.5 <= float(weight) <= 90.0`. |
| **Medical background (optional)** | Text Area (`st.text_area`) | Free text string (e.g. "Indoor only, vaccinated") | Free text string (e.g. "Previous GI upset") | Optional. Max length unbounded. |

---

### Step 2: Primary Clinical Signs / Symptoms (`views/assessment.py`)
Users can select multiple symptoms using toggle chip buttons.

* **Cat Primary Symptoms** (`data/question_bank.py` & `views/assessment.py`):
  1. `Vomiting`
  2. `Sneezing`
  3. `Straining to urinate`
  4. `Hair loss`
  5. `Low appetite`
  6. `Hiding more`
* **Dog Primary Symptoms** (`data/question_bank.py` & `views/assessment.py`):
  1. `Vomiting`
  2. `Diarrhoea`
  3. `Itching`
  4. `Coughing`
  5. `Limping`
  6. `Low appetite`
* **Backend Engine Extended Triage** (`backend/engine/question_engine.py`):
  Both species also define `Lethargy`, `Fever`, `Weight loss`, and `Loss of coordination` in `SYMPTOMS_BY_SPECIES` for headless/API assessments.
* **Validation**: At least **one** symptom must be selected to proceed (`"Choose at least one sign to continue."`).

---

### Step 3: Conditional Follow-Up Questions (`views/assessment.py`)
Triggered dynamically based strictly on the symptoms selected in Step 2. Each question presents three mutually exclusive buttons:
- `Yes`
- `No`
- `Not Sure`
*Validation*: Every presented question must be answered before advancing (`"Please answer every question."`).

---

### Step 4: Timing, Severity, and Frequency (`views/assessment.py`)

| Question / Prompt | Component | Available Options | Default / Required |
|---|---|---|---|
| **"How long has this been going on?"** | Dropdown | `Choose`, `Less than 1 day`, `1–3 days`, `More than 3 days` | Required. Cannot be `Choose`. |
| **"How severe does it look?"** | Chip Buttons | `Mild`, `Moderate`, `Severe` | Required. User must tap one. |
| **"How often does it happen?"** | Chip Buttons | `Once`, `Sometimes`, `Often` | Required. User must tap one. |

*Validation*: All three dimensions are mandatory (`"Please choose duration, severity and frequency."`).

---

### Step 5: Red-Flag Emergency Screening (`views/assessment.py`)
Three high-priority triage questions displayed to all users regardless of species:
1. `1. Trouble breathing, or blue or pale gums?`
2. `2. Collapse or a seizure?`
3. `3. Possibly swallowed poison or a toxic item?`

* **Available Answer Options**: `Yes`, `No`, `Not Sure` for each question.
* **Validation**: All 3 questions must have an active selection (`"Please answer all three emergency questions."`).
* **Visual Alert**: Answering `Yes` to any of the three triggers an immediate inline warning alert:  
  *🚨 This may be an emergency. Please contact a vet right away. You can still continue to see guidance.*

---

## 2. Conditional Follow-Up Questions & Trigger Conditions

The follow-up questioning system is deterministic. In the UI (`views/assessment.py`), queries are pulled from `data/question_bank.py:FOLLOW_UPS` and `backend/engine/question_engine.py:FOLLOW_UP_QUESTIONS_TEXT`.

| Trigger Symptom | Trigger Condition | Question Index | Exact Question Text | Answer Key in Working Memory | Available Options |
|---|---|---|---|---|---|
| **Vomiting** | `Vomiting` in `syms` | 0 | *Has it happened more than twice today?* | `Vomiting\|0` | `Yes`, `No`, `Not Sure` |
| **Vomiting** | `Vomiting` in `syms` | 1 | *Is there blood in the vomit?* | `Vomiting\|1` | `Yes`, `No`, `Not Sure` |
| **Diarrhoea** | `Diarrhoea` in `syms` | 0 | *Is the stool watery?* | `Diarrhoea\|0` | `Yes`, `No`, `Not Sure` |
| **Diarrhoea** | `Diarrhoea` in `syms` | 1 | *Is there blood or mucus in it?* | `Diarrhoea\|1` | `Yes`, `No`, `Not Sure` |
| **Itching** | `Itching` in `syms` | 0 | *Is the skin red or sore?* | `Itching\|0` | `Yes`, `No`, `Not Sure` |
| **Itching** | `Itching` in `syms` | 1 | *Have you seen fleas?* | `Itching\|1` | `Yes`, `No`, `Not Sure` |
| **Coughing** | `Coughing` in `syms` | 0 | *Is the cough worse at night?* | `Coughing\|0` | `Yes`, `No`, `Not Sure` |
| **Coughing** | `Coughing` in `syms` | 1 | *Does your pet gag after coughing?* | `Coughing\|1` | `Yes`, `No`, `Not Sure` |
| **Limping** | `Limping` in `syms` | 0 | *Is the leg held off the ground?* | `Limping\|0` | `Yes`, `No`, `Not Sure` |
| **Limping** | `Limping` in `syms` | 1 | *Is there visible swelling or heat?* (UI: *Is there swelling?*) | `Limping\|1` | `Yes`, `No`, `Not Sure` |
| **Low appetite** | `Low appetite` in `syms` | 0 | *Is your pet also drinking less?* | `Low appetite\|0` | `Yes`, `No`, `Not Sure` |
| **Low appetite** | `Low appetite` in `syms` | 1 | *Has this lasted more than a day?* | `Low appetite\|1` | `Yes`, `No`, `Not Sure` |
| **Sneezing** | `Sneezing` in `syms` | 0 | *Is there eye or nose discharge?* | `Sneezing\|0` | `Yes`, `No`, `Not Sure` |
| **Sneezing** | `Sneezing` in `syms` | 1 | *Does sneezing happen often?* | `Sneezing\|1` | `Yes`, `No`, `Not Sure` |
| **Straining to urinate** | `Straining to urinate` in `syms` | 0 | *Is little or no urine coming out?* | `Straining to urinate\|0` | `Yes`, `No`, `Not Sure` |
| **Straining to urinate** | `Straining to urinate` in `syms` | 1 | *Is there blood in the urine?* | `Straining to urinate\|1` | `Yes`, `No`, `Not Sure` |
| **Hair loss** | `Hair loss` in `syms` | 0 | *Are there bald patches?* | `Hair loss\|0` | `Yes`, `No`, `Not Sure` |
| **Hair loss** | `Hair loss` in `syms` | 1 | *Is the skin flaky?* | `Hair loss\|1` | `Yes`, `No`, `Not Sure` |
| **Hiding more** | `Hiding more` in `syms` | 0 | *Has the behaviour changed suddenly?* | `Hiding more\|0` | `Yes`, `No`, `Not Sure` |
| **Hiding more** | `Hiding more` in `syms` | 1 | *Is your pet eating less?* | `Hiding more\|1` | `Yes`, `No`, `Not Sure` |

*Orphaned Answer Cleanup*: When a user deselects a symptom in Step 2, `QuestionEngine.clean_orphaned_answers()` and `views/assessment.py:50-55` automatically purge all stored `symptom|index` key-value pairs associated with that symptom.

---

## 3. Complete Veterinary Knowledge Base (All 60 Conditions)

Defined in `backend/knowledge_base/cat_conditions.py` (`CAT_001` to `CAT_030`) and `backend/knowledge_base/dog_conditions.py` (`DOG_001` to `DOG_030`).

### Feline Conditions (`Cat`)

| ID | Condition Name | Anatomical Category | Medical Classification | Baseline Severity | Baseline Urgency | Common Symptoms |
|---|---|---|---|---|---|---|
| `CAT_001` | Feline Inflammatory Bowel Disease (IBD) | Gastrointestinal | Chronic inflammatory gastrointestinal enteropathy | Moderate | Routine | Vomiting, Diarrhoea, Low appetite |
| `CAT_002` | Feline Pancreatitis | Gastrointestinal | Exocrine pancreatic inflammatory disease | Moderate | Urgent | Low appetite, Vomiting, Hiding more |
| `CAT_003` | Feline Constipation | Gastrointestinal | Colonic motility disorder and obstipation | Moderate | Urgent | Straining to urinate, Vomiting, Low appetite |
| `CAT_004` | Gastrointestinal Parasitism | Gastrointestinal | Endoparasitic infection | Mild | Routine | Diarrhoea, Vomiting, Low appetite |
| `CAT_005` | Feline Flea Allergy Dermatitis | Dermatology | Hypersensitivity dermatosis (Type I and IV) | Mild | Routine | Itching, Hair loss |
| `CAT_006` | Feline Dermatophytosis (Ringworm) | Dermatology | Superficial fungal infection | Mild | Routine | Hair loss, Itching |
| `CAT_007` | Eosinophilic Granuloma Complex | Dermatology | Eosinophilic cutaneous reaction pattern | Moderate | Routine | Hair loss, Itching, Low appetite |
| `CAT_008` | Feline Cutaneous Adverse Food Reaction | Dermatology | Non-seasonal food hypersensitivity | Mild | Routine | Itching, Hair loss, Vomiting |
| `CAT_009` | Feline Asthma | Respiratory | Lower airway allergic inflammatory disease | Severe | Urgent | Coughing, Low appetite, Hiding more |
| `CAT_010` | Feline Herpesvirus-1 Infection | Respiratory | Viral upper respiratory infection (FHV-1) | Moderate | Routine | Sneezing, Low appetite, Hiding more |
| `CAT_011` | Feline Calicivirus Infection | Respiratory | Viral mucosal and respiratory infection (FCV) | Moderate | Urgent | Sneezing, Low appetite, Vomiting |
| `CAT_012` | Feline Pneumonia | Respiratory | Pulmonary parenchymal consolidation and infection | Critical | Emergency | Coughing, Low appetite, Hiding more |
| `CAT_013` | Feline Idiopathic Cystitis (FIC) | Urinary / Renal | Sterile neurogenic lower urinary tract disease | Moderate | Urgent | Straining to urinate, Low appetite, Hiding more |
| `CAT_014` | Feline Urethral Obstruction | Urinary / Renal | Acute obstructive uropathy (Medical Emergency) | Critical | Emergency | Straining to urinate, Vomiting, Hiding more |
| `CAT_015` | Feline Chronic Kidney Disease | Urinary / Renal | Progressive structural and functional renal decline | Severe | Urgent | Low appetite, Vomiting, Hiding more |
| `CAT_016` | Feline Urolithiasis | Urinary / Renal | Lower urinary cystic or urethral calculi | Moderate | Urgent | Straining to urinate, Low appetite |
| `CAT_017` | Feline Conjunctivitis | Ophthalmology / Otology | Ocular surface mucosal inflammation | Mild | Routine | Sneezing, Hiding more |
| `CAT_018` | Feline Corneal Ulcer | Ophthalmology / Otology | Traumatic or infectious corneal epithelial defect | Severe | Urgent | Sneezing, Hiding more, Low appetite |
| `CAT_019` | Feline Otitis Externa | Ophthalmology / Otology | External ear canal inflammation | Mild | Routine | Itching, Hair loss |
| `CAT_020` | Feline Diabetes Mellitus | Endocrine | Metabolic endocrine disorder (Type II-like) | Severe | Urgent | Low appetite, Vomiting, Hiding more |
| `CAT_021` | Feline Hyperthyroidism | Endocrine | Adenomatous thyroid hypersecretion | Moderate | Routine | Vomiting, Diarrhoea, Low appetite |
| `CAT_022` | Feline Leukemia Virus (FeLV) Infection | Infectious Disease | Retroviral oncogenic and immunosuppressive infection | Severe | Urgent | Low appetite, Hiding more, Weight loss |
| `CAT_023` | Feline Immunodeficiency Virus (FIV) Infection | Infectious Disease | Lentiviral chronic immunodeficiency | Moderate | Routine | Low appetite, Hiding more, Weight loss |
| `CAT_024` | Feline Infectious Peritonitis (FIP) | Infectious Disease | Coronaviral immune-complex vasculitis | Critical | Emergency | Low appetite, Hiding more, Vomiting |
| `CAT_025` | Feline Panleukopenia | Infectious Disease | Parvoviral enteritis and panmyelophthisis | Critical | Emergency | Vomiting, Diarrhoea, Low appetite |
| `CAT_026` | Feline Obesity | Metabolic / Endocrine | Chronic excessive adiposity | Mild | Routine | Low appetite, Hiding more |
| `CAT_027` | Feline Hepatic Lipidosis | Metabolic / Endocrine | Acute intracellular triglyceride accumulation | Critical | Emergency | Low appetite, Vomiting, Hiding more |
| `CAT_028` | Feline Gingivostomatitis | Dental | Severe chronic mucosal immune stomatitis | Moderate | Routine | Low appetite, Hiding more |
| `CAT_029` | Feline Tooth Resorption | Dental | Odontoclastic resorptive lesion | Moderate | Routine | Low appetite, Hiding more |
| `CAT_030` | Feline Hypertrophic Cardiomyopathy (HCM) | Metabolic / Dental / Cardiovascular | Concentric left ventricular myocardial hypertrophy | Critical | Emergency | Coughing, Low appetite, Hiding more |

---

### Canine Conditions (`Dog`)

| ID | Condition Name | Anatomical Category | Medical Classification | Baseline Severity | Baseline Urgency | Common Symptoms |
|---|---|---|---|---|---|---|
| `DOG_001` | Canine Gastritis | Gastrointestinal | Acute or chronic gastric mucosal inflammation | Moderate | Routine | Vomiting, Low appetite |
| `DOG_002` | Canine Inflammatory Bowel Disease (IBD) | Gastrointestinal | Chronic idiopathic enteropathy | Moderate | Routine | Diarrhoea, Vomiting, Low appetite |
| `DOG_003` | Canine Pancreatitis | Gastrointestinal | Acute or chronic necrotizing exocrine pancreatitis | Severe | Urgent | Vomiting, Low appetite |
| `DOG_004` | Gastric Dilatation-Volvulus (GDV) | Gastrointestinal | Peracute gastric malposition and strangulation | Critical | Emergency | Vomiting, Low appetite |
| `DOG_005` | Exocrine Pancreatic Insufficiency (EPI) | Gastrointestinal | Acinar atrophy maldigestion syndrome | Moderate | Routine | Diarrhoea, Low appetite |
| `DOG_006` | Canine Atopic Dermatitis | Dermatology | Genetically predisposed environmental allergy | Mild | Routine | Itching |
| `DOG_007` | Canine Flea Allergy Dermatitis | Dermatology | Salivary hypersensitivity dermatosis | Mild | Routine | Itching |
| `DOG_008` | Superficial Bacterial Pyoderma | Dermatology | Follicular bacterial infection (Staphylococcus pseudintermedius) | Mild | Routine | Itching |
| `DOG_009` | Canine Demodicosis | Dermatology | Follicular Demodex canis mite proliferation | Mild | Routine | Itching |
| `DOG_010` | Canine Sarcoptic Mange | Dermatology | Sarcoptes scabiei var. canis contagious mite infestation | Moderate | Urgent | Itching |
| `DOG_011` | Canine Infectious Respiratory Disease Complex (Kennel Cough) | Respiratory | Acute infectious tracheobronchitis | Mild | Routine | Coughing |
| `DOG_012` | Canine Tracheal Collapse | Respiratory | Progressive tracheobronchial cartilage hypocellularity | Moderate | Urgent | Coughing |
| `DOG_013` | Canine Pneumonia | Respiratory | Infectious or aspiration bacterial consolidation | Critical | Emergency | Coughing, Low appetite |
| `DOG_014` | Canine Bacterial Cystitis / UTI | Urinary / Renal | Ascending lower urinary bacterial infection | Moderate | Urgent | Low appetite |
| `DOG_015` | Canine Urolithiasis | Urinary / Renal | Lower urinary cystic or urethral calculi | Moderate | Urgent | Low appetite |
| `DOG_016` | Canine Chronic Kidney Disease | Urinary / Renal | Progressive nephron loss and uremic syndrome | Severe | Urgent | Vomiting, Low appetite |
| `DOG_017` | Canine Otitis Externa | Ophthalmology / Otology | Microbial canal inflammation | Mild | Routine | Itching |
| `DOG_018` | Canine Corneal Ulcer | Ophthalmology / Otology | Traumatic or microbial corneal defect | Severe | Urgent | Low appetite |
| `DOG_019` | Canine Diabetes Mellitus | Endocrine | Absolute insulin deficiency (Type I-like) | Severe | Urgent | Vomiting, Low appetite |
| `DOG_020` | Canine Hypothyroidism | Endocrine | Immune-mediated thyroiditis or idiopathic atrophy | Moderate | Routine | Low appetite |
| `DOG_021` | Canine Hyperadrenocorticism (Cushing's Syndrome) | Endocrine | Pituitary or adrenal hypercortisolemia | Moderate | Routine | Low appetite |
| `DOG_022` | Canine Hypoadrenocorticism (Addison's Disease) | Endocrine | Primary adrenocortical destruction (Adrenal Insufficiency) | Critical | Emergency | Vomiting, Diarrhoea, Low appetite |
| `DOG_023` | Canine Parvovirus Infection | Infectious Disease | Viral crypt epithelial lysis and severe enteritis | Critical | Emergency | Vomiting, Diarrhoea, Low appetite |
| `DOG_024` | Canine Leptospirosis | Infectious Disease | Spirochetal zoonotic renal and hepatic vasculitis | Critical | Emergency | Vomiting, Diarrhoea, Low appetite |
| `DOG_025` | Canine Heartworm Disease | Cardiovascular / Parasitic | Dirofilaria immitis pulmonary arterial occlusion | Severe | Urgent | Coughing, Low appetite |
| `DOG_026` | Degenerative Mitral Valve Disease | Cardiovascular | Myxomatous valvular degeneration | Severe | Urgent | Coughing, Low appetite |
| `DOG_027` | Canine Obesity | Metabolic / Endocrine | Pathological body fat accumulation | Mild | Routine | Low appetite |
| `DOG_028` | Canine Periodontal Disease | Dental | Subgingival plaque bacteremia and alveolar bone destruction | Moderate | Routine | Low appetite |
| `DOG_029` | Canine Separation Anxiety | Behavioral | Psychogenic attachment distress | Moderate | Routine | Low appetite |
| `DOG_030` | Canine Cognitive Dysfunction Syndrome | Behavioral / Neurological | Neurodegenerative cerebral amyloidosis | Moderate | Routine | Low appetite |

---

## 4. Facts Taxonomy: Static, Dynamic, and Inferred Facts

Diagnovet classifies knowledge and information into three ontological categories:

```
[Static Knowledge Base Facts] ──┐
                               ├──> [Rule Matching & Inference Engine] ──> [Inferred / Derived Facts]
[Dynamic Working Memory Facts] ─┘
```

### 1. Static Facts (The Knowledge Base)
Pre-compiled clinical assertions that remain invariant across sessions:
* **Condition Records** (`Condition` in `backend/models/condition.py`):
  * Definition, Etiology, Risk Factors, Primary & Secondary Symptoms.
  * Veterinary Diagnostic Procedures (e.g. `Spec fPL`, `Echocardiogram`, `Urinalysis`).
  * Differential Diagnoses list.
  * Baseline Urgency and Baseline Severity classifications.
* **Veterinary Medical Sources** (`backend/knowledge_base/medical_sources.py`):
  * 120 verified references linking each condition to peer-reviewed veterinary literature, including:
    * *Merck Veterinary Manual* (e.g. Jergens on IBD, Tilley on HCM, DeNovo on Gastritis).
    * *Cornell Feline Health Center* (Cornell Staff on Pancreatitis, FIP, FIC, Calicivirus).
    * *Veterinary Information Network / Veterinary Partner* (Brooks on Addison's, GDV, Leptospirosis).
    * *American Animal Hospital Association (AAHA)* & *WSAVA Global Guidelines*.

### 2. Dynamic Facts (Session Working Memory)
Facts asserted by the user during the active assessment session:
* `Fact(Species = "Dog" | "Cat")`
* `Fact(Breed = <String>)`
* `Fact(Gender = "Male" | "Female")`
* `Fact(Age = <Float>)`
* `Fact(Weight = <Float> | None)`
* `Fact(SelectedSymptoms = List[<String>])`
* `Fact(Answer[Symptom, QuestionIndex] = "Yes" | "No" | "Not Sure")`
* `Fact(Duration = "Less than 1 day" | "1–3 days" | "More than 3 days")`
* `Fact(Severity = "Mild" | "Moderate" | "Severe")`
* `Fact(Frequency = "Once" | "Sometimes" | "Often")`
* `Fact(EmergencyCheck[0..2] = "Yes" | "No" | "Not Sure")`

### 3. Inferred / Derived Facts
Generated dynamically during inference:
* `Fact(PrimaryConcordance[Condition] = True/False)`
* `Fact(RuleSatisfied[RuleID] = True/False)`
* `Fact(SupportingEvidence = List[<String>])`
* `Fact(ContradictoryEvidence = List[<String>])`
* `Fact(MissingEvidence = List[<String>])`
* `Fact(EmergencyDetected = True/False)`
* `Fact(EmergencyReasons = List[<String>])`
* `Fact(MatchScore[Condition] = Integer[0..92])`
* `Fact(DecisionTierIndex = 0 | 1 | 2 | 3)`
* `Fact(DecisionOutcome = DecisionOutcome(Name, Tone, Level, Text, Steps, Rationale))`

---

## 5. Complete Clinical IF-THEN Rules (All 60 Rules)

Defined in `backend/engine/rule_engine.py`. Every rule specifies species boundaries, primary trigger symptoms, supporting follow-up criteria (affirmative responses), contradictory criteria, age preferences, and explanation templates.

### Feline Rules (`RULE_CAT_001` to `RULE_CAT_030`)

1. **`RULE_CAT_001_IBD`**
   - **IF**: Species is `Cat` AND Symptoms include any of `["Vomiting", "Diarrhoea", "Low appetite"]`
   - **AND SUPPORTING**: Follow-ups match `"more than twice today"`, `"blood or mucus"`, `"has lasted more than a day"`, or `"blood in the vomit"`
   - **AGE PREFERENCE**: `Adult`
   - **CONTRADICTORY IF**: Sudden collapse within 1 hr; high fever with foul-smelling panleukopenia.
   - **CONCLUSION**: Concordance for *Feline Inflammatory Bowel Disease (IBD)*.
   - **EXPLANATION**: Chronic digestive signs (vomiting/diarrhea) persisting over time in adult cats support mucosal gastrointestinal enteropathy.

2. **`RULE_CAT_002_PANCREATITIS`**
   - **IF**: Species is `Cat` AND Symptoms include `["Low appetite", "Vomiting", "Hiding more"]`
   - **AND SUPPORTING**: Follow-ups match `"drinking less"`, `"behaviour changed suddenly"`, or `"more than twice today"`
   - **CONCLUSION**: Concordance for *Feline Pancreatitis*.
   - **EXPLANATION**: Lethargy, hyporexia, and subtle vomiting pattern align with feline pancreatic inflammation.

3. **`RULE_CAT_003_CONSTIPATION`**
   - **IF**: Species is `Cat` AND Symptoms include `["Straining to urinate", "Vomiting", "Low appetite"]`
   - **AND SUPPORTING**: Follow-ups match `"little or no urine coming out"` or `"behaviour changed suddenly"`
   - **CONTRADICTORY IF**: Profuse watery diarrhea; continuous large-volume urination.
   - **CONCLUSION**: Concordance for *Feline Constipation*.
   - **EXPLANATION**: Tenesmus and unproductive straining in the litter box are characteristic of colonic obstipation or fecal impaction.

4. **`RULE_CAT_004_PARASITISM`**
   - **IF**: Species is `Cat` AND Symptoms include `["Diarrhoea", "Vomiting", "Low appetite"]`
   - **AND SUPPORTING**: Follow-ups match `"stool watery"` or `"blood or mucus in it"`
   - **AGE PREFERENCE**: `Young` (<2 yrs)
   - **CONTRADICTORY IF**: Strict indoor adult with verified monthly prophylaxis.
   - **CONCLUSION**: Concordance for *Gastrointestinal Parasitism*.
   - **EXPLANATION**: Loose stool with mucoid elements in young or hunting cats suggests intestinal endoparasitism.

5. **`RULE_CAT_005_FAD`**
   - **IF**: Species is `Cat` AND Symptoms include `["Itching", "Hair loss"]`
   - **AND SUPPORTING**: Follow-ups match `"skin red or sore"`, `"seen fleas"`, `"bald patches"`, or `"skin flaky"`
   - **CONCLUSION**: Concordance for *Feline Flea Allergy Dermatitis*.
   - **EXPLANATION**: Caudal dorsum and neck pruritus with miliary crusts strongly points to flea salivary hypersensitivity.

6. **`RULE_CAT_006_RINGWORM`**
   - **IF**: Species is `Cat` AND Symptoms include `["Hair loss", "Itching"]`
   - **AND SUPPORTING**: Follow-ups match `"bald patches"` or `"skin flaky"`
   - **AGE PREFERENCE**: `Young` (<2 yrs)
   - **CONCLUSION**: Concordance for *Feline Dermatophytosis (Ringworm)*.
   - **EXPLANATION**: Focal expanding circular patches of alopecia and scaling in a young cat suggest fungal dermatophytosis.

7. **`RULE_CAT_007_EGC`**
   - **IF**: Species is `Cat` AND Symptoms include `["Hair loss", "Itching", "Low appetite"]`
   - **AND SUPPORTING**: Follow-ups match `"skin red or sore"` or `"bald patches"`
   - **CONCLUSION**: Concordance for *Eosinophilic Granuloma Complex*.
   - **EXPLANATION**: Raised plaques or erosion of upper lip/inguinal skin indicates feline eosinophilic granuloma complex.

8. **`RULE_CAT_008_CAFR`**
   - **IF**: Species is `Cat` AND Symptoms include `["Itching", "Hair loss", "Vomiting"]`
   - **AND SUPPORTING**: Follow-ups match `"skin red or sore"`, `"bald patches"`, or `"skin flaky"`
   - **CONTRADICTORY IF**: Seasonal itching restricted strictly to summer.
   - **CONCLUSION**: Concordance for *Feline Cutaneous Adverse Food Reaction*.
   - **EXPLANATION**: Non-seasonal facial/neck pruritus paired with digestive sensitivity supports food allergy.

9. **`RULE_CAT_009_ASTHMA`**
   - **IF**: Species is `Cat` AND Symptoms include `["Coughing", "Low appetite", "Hiding more"]`
   - **AND SUPPORTING**: Follow-ups match `"worse at night"` or `"gag after coughing"`
   - **CONCLUSION**: Concordance for *Feline Asthma*.
   - **EXPLANATION**: Dry hacking paroxysmal cough with gagging and expiratory effort aligns with lower airway asthma.

10. **`RULE_CAT_010_FHV1`**
    - **IF**: Species is `Cat` AND Symptoms include `["Sneezing", "Low appetite", "Hiding more"]`
    - **AND SUPPORTING**: Follow-ups match `"eye or nose discharge"`, `"sneezing happen often"`, or `"eating less"`
    - **CONCLUSION**: Concordance for *Feline Herpesvirus-1 Infection*.
    - **EXPLANATION**: Frequent sneezing combined with oculonasal discharge and blepharospasm reflects herpesviral upper respiratory flare.

11. **`RULE_CAT_011_CALICIVIRUS`**
    - **IF**: Species is `Cat` AND Symptoms include `["Sneezing", "Low appetite", "Vomiting"]`
    - **AND SUPPORTING**: Follow-ups match `"eye or nose discharge"` or `"eating less"`
    - **CONTRADICTORY IF**: Oral cavity free of any ulcers or drooling.
    - **CONCLUSION**: Concordance for *Feline Calicivirus Infection*.
    - **EXPLANATION**: Sneezing accompanied by oral pain, drooling, or reluctance to eat points toward calicivirus.

12. **`RULE_CAT_012_PNEUMONIA`**
    - **IF**: Species is `Cat` AND Symptoms include `["Coughing", "Low appetite", "Hiding more"]`
    - **AND SUPPORTING**: Follow-ups match `"gag after coughing"`, `"eating less"`, or `"drinking less"`
    - **EMERGENCY FLAG**: `True`
    - **CONCLUSION**: Concordance for *Feline Pneumonia*.
    - **EXPLANATION**: Deep cough with lethargy and systemic depression warrants concern for pulmonary consolidation.

13. **`RULE_CAT_013_FIC`**
    - **IF**: Species is `Cat` AND Symptoms include `["Straining to urinate", "Low appetite", "Hiding more"]`
    - **AND SUPPORTING**: Follow-ups match `"blood in the urine"` or `"behaviour changed suddenly"`
    - **CONTRADICTORY IF**: Hard, basketball-like non-expressible bladder (indicates complete blockage).
    - **CONCLUSION**: Concordance for *Feline Idiopathic Cystitis (FIC)*.
    - **EXPLANATION**: Frequent straining, periuria, and hematuria in an indoor cat without physical obstruction reflect sterile cystitis.

14. **`RULE_CAT_014_OBSTRUCTION`**
    - **IF**: Species is `Cat` AND Symptoms include `["Straining to urinate", "Vomiting", "Hiding more"]`
    - **AND SUPPORTING**: Follow-ups match `"little or no urine coming out"`, `"blood in the urine"`, or `"behaviour changed suddenly"`
    - **EMERGENCY FLAG**: `True`
    - **CONCLUSION**: Critical concordance for *Feline Urethral Obstruction*.
    - **EXPLANATION**: EMERGENCY RULE: Straining with minimal or no urine output in a cat is a medical emergency requiring immediate vet relief.

15. **`RULE_CAT_015_CKD`**
    - **IF**: Species is `Cat` AND Symptoms include `["Low appetite", "Vomiting", "Hiding more"]`
    - **AND SUPPORTING**: Follow-ups match `"drinking less"`, `"has lasted more than a day"`, or `"eating less"`
    - **AGE PREFERENCE**: `Senior` (>=8 yrs)
    - **CONCLUSION**: Concordance for *Feline Chronic Kidney Disease*.
    - **EXPLANATION**: Senior cat with gradual hyporexia, unkempt coat, vomiting, and thirst changes strongly suggests renal disease.

16. **`RULE_CAT_016_UROLITHIASIS`**
    - **IF**: Species is `Cat` AND Symptoms include `["Straining to urinate", "Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"blood in the urine"` or `"little or no urine coming out"`
    - **CONCLUSION**: Concordance for *Feline Urolithiasis*.
    - **EXPLANATION**: Persistent dysuria and hematuria indicate possible cystic calculi requiring diagnostic radiography.

17. **`RULE_CAT_017_CONJUNCTIVITIS`**
    - **IF**: Species is `Cat` AND Symptoms include `["Sneezing", "Hiding more"]`
    - **AND SUPPORTING**: Follow-ups match `"eye or nose discharge"` or `"sneezing happen often"`
    - **CONCLUSION**: Concordance for *Feline Conjunctivitis*.
    - **EXPLANATION**: Conjunctival hyperemia, squinting, and ocular discharge indicate infectious or allergic conjunctivitis.

18. **`RULE_CAT_018_CORNEAL_ULCER`**
    - **IF**: Species is `Cat` AND Symptoms include `["Sneezing", "Hiding more", "Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"eye or nose discharge"` or `"behaviour changed suddenly"`
    - **EMERGENCY FLAG**: `True`
    - **CONCLUSION**: Concordance for *Feline Corneal Ulcer*.
    - **EXPLANATION**: Severe squinting, eye clamping, and corneal cloudiness represent a corneal defect needing urgent vet care.

19. **`RULE_CAT_019_OTITIS`**
    - **IF**: Species is `Cat` AND Symptoms include `["Itching", "Hair loss"]`
    - **AND SUPPORTING**: Follow-ups match `"skin red or sore"` or `"bald patches"`
    - **CONCLUSION**: Concordance for *Feline Otitis Externa*.
    - **EXPLANATION**: Head scratching, ear sensitivity, and crusty dark wax point to otic mite or microbial inflammation.

20. **`RULE_CAT_020_DIABETES`**
    - **IF**: Species is `Cat` AND Symptoms include `["Low appetite", "Vomiting", "Hiding more"]`
    - **AND SUPPORTING**: Follow-ups match `"drinking less"`, `"has lasted more than a day"`, or `"eating less"`
    - **AGE PREFERENCE**: `Adult`
    - **CONCLUSION**: Concordance for *Feline Diabetes Mellitus*.
    - **EXPLANATION**: Metabolic decline, weight changes, and polyuria/polydipsia pattern support feline diabetes mellitus.

21. **`RULE_CAT_021_HYPERTHYROIDISM`**
    - **IF**: Species is `Cat` AND Symptoms include `["Vomiting", "Diarrhoea", "Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"more than twice today"` or `"has lasted more than a day"`
    - **AGE PREFERENCE**: `Senior` (>=8 yrs)
    - **CONCLUSION**: Concordance for *Feline Hyperthyroidism*.
    - **EXPLANATION**: Weight loss, gastrointestinal motility increase, and hyperactivity in an older cat align with hyperthyroidism.

22. **`RULE_CAT_022_FELV`**
    - **IF**: Species is `Cat` AND Symptoms include `["Low appetite", "Hiding more", "Weight loss"]`
    - **AND SUPPORTING**: Follow-ups match `"eating less"`, `"drinking less"`, or `"behaviour changed suddenly"`
    - **CONCLUSION**: Concordance for *Feline Leukemia Virus (FeLV)*.
    - **EXPLANATION**: Chronic failing to thrive, pale gums, and recurrent illness in outdoor/rescue cats suggest retroviral infection.

23. **`RULE_CAT_023_FIV`**
    - **IF**: Species is `Cat` AND Symptoms include `["Low appetite", "Hiding more", "Weight loss"]`
    - **AND SUPPORTING**: Follow-ups match `"eating less"` or `"behaviour changed suddenly"`
    - **CONCLUSION**: Concordance for *Feline Immunodeficiency Virus (FIV)*.
    - **EXPLANATION**: Chronic mouth inflammation, slow-healing wounds, and persistent illness in an adult cat suggest FIV.

24. **`RULE_CAT_024_FIP`**
    - **IF**: Species is `Cat` AND Symptoms include `["Low appetite", "Hiding more", "Vomiting"]`
    - **AND SUPPORTING**: Follow-ups match `"behaviour changed suddenly"`, `"eating less"`, or `"drinking less"`
    - **AGE PREFERENCE**: `Young` (<2 yrs)
    - **EMERGENCY FLAG**: `True`
    - **CONCLUSION**: Critical concordance for *Feline Infectious Peritonitis (FIP)*.
    - **EXPLANATION**: Unresponsive fever, progressive weakness, and fluid accumulation in a young cat suggest FIP.

25. **`RULE_CAT_025_PANLEUKOPENIA`**
    - **IF**: Species is `Cat` AND Symptoms include `["Vomiting", "Diarrhoea", "Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"more than twice today"`, `"blood in the vomit"`, `"stool watery"`, or `"blood or mucus in it"`
    - **AGE PREFERENCE**: `Young` (<2 yrs)
    - **EMERGENCY FLAG**: `True`
    - **CONCLUSION**: Critical concordance for *Feline Panleukopenia*.
    - **EXPLANATION**: EMERGENCY RULE: Intractable vomiting, severe diarrhea, and dehydration in an unvaccinated kitten indicate panleukopenia.

26. **`RULE_CAT_026_OBESITY`**
    - **IF**: Species is `Cat` AND Symptoms include `["Low appetite", "Hiding more"]`
    - **AND SUPPORTING**: Follow-ups match `"behaviour changed suddenly"`
    - **CONTRADICTORY IF**: Palpable spine/emaciation (BCS <3/9).
    - **CONCLUSION**: Concordance for *Feline Obesity*.
    - **EXPLANATION**: Excessive body fat, difficulty grooming, and reluctance to jump point toward feline obesity.

27. **`RULE_CAT_027_HEPATIC_LIPIDOSIS`**
    - **IF**: Species is `Cat` AND Symptoms include `["Low appetite", "Vomiting", "Hiding more"]`
    - **AND SUPPORTING**: Follow-ups match `"more than twice today"`, `"has lasted more than a day"`, or `"eating less"`
    - **EMERGENCY FLAG**: `True`
    - **CONCLUSION**: Critical concordance for *Feline Hepatic Lipidosis*.
    - **EXPLANATION**: EMERGENCY RULE: Prolonged anorexia in an overweight cat leading to yellow jaundice is critical hepatic lipidosis.

28. **`RULE_CAT_028_GINGIVOSTOMATITIS`**
    - **IF**: Species is `Cat` AND Symptoms include `["Low appetite", "Hiding more"]`
    - **AND SUPPORTING**: Follow-ups match `"eating less"` or `"behaviour changed suddenly"`
    - **CONCLUSION**: Concordance for *Feline Gingivostomatitis*.
    - **EXPLANATION**: Severe oral pain, crying when attempting to eat, and drooling indicate caudal chronic gingivostomatitis.

29. **`RULE_CAT_029_TOOTH_RESORPTION`**
    - **IF**: Species is `Cat` AND Symptoms include `["Low appetite", "Hiding more"]`
    - **AND SUPPORTING**: Follow-ups match `"eating less"`
    - **CONCLUSION**: Concordance for *Feline Tooth Resorption*.
    - **EXPLANATION**: Jaw chattering, dropping hard food, and chewing on one side suggest painful odontoclastic tooth resorption.

30. **`RULE_CAT_030_HCM`**
    - **IF**: Species is `Cat` AND Symptoms include `["Coughing", "Low appetite", "Hiding more"]`
    - **AND SUPPORTING**: Follow-ups match `"gag after coughing"`, `"eating less"`, or `"behaviour changed suddenly"`
    - **EMERGENCY FLAG**: `True`
    - **CONCLUSION**: Critical concordance for *Feline Hypertrophic Cardiomyopathy (HCM)*.
    - **EXPLANATION**: Rapid resting respiratory rate, weakness, or sudden hindleg paralysis indicate decompensated feline cardiomyopathy.

---

### Canine Rules (`RULE_DOG_001` to `RULE_DOG_030`)

1. **`RULE_DOG_001_GASTRITIS`**
   - **IF**: Species is `Dog` AND Symptoms include `["Vomiting", "Low appetite"]`
   - **AND SUPPORTING**: Follow-ups match `"more than twice today"`, `"blood in the vomit"`, or `"has lasted more than a day"`
   - **CONTRADICTORY IF**: Drum-like distended abdomen with dry retching (GDV).
   - **CONCLUSION**: Concordance for *Canine Gastritis*.
   - **EXPLANATION**: Acute vomiting following dietary indiscretion or scavenging points toward canine gastric irritation.

2. **`RULE_DOG_002_IBD`**
   - **IF**: Species is `Dog` AND Symptoms include `["Diarrhoea", "Vomiting", "Low appetite"]`
   - **AND SUPPORTING**: Follow-ups match `"stool watery"`, `"blood or mucus in it"`, or `"has lasted more than a day"`
   - **CONCLUSION**: Concordance for *Canine Inflammatory Bowel Disease (IBD)*.
   - **EXPLANATION**: Persistent, recurrent vomiting and diarrhea lasting weeks in an adult dog indicates chronic enteropathy.

3. **`RULE_DOG_003_PANCREATITIS`**
   - **IF**: Species is `Dog` AND Symptoms include `["Vomiting", "Low appetite"]`
   - **AND SUPPORTING**: Follow-ups match `"more than twice today"`, `"has lasted more than a day"`, or `"eating less"`
   - **CONCLUSION**: Concordance for *Canine Pancreatitis*.
   - **EXPLANATION**: Acute severe vomiting and cranial abdominal pain after fatty food consumption indicate pancreatitis.

4. **`RULE_DOG_004_GDV`**
   - **IF**: Species is `Dog` AND Symptoms include `["Vomiting", "Low appetite"]`
   - **AND SUPPORTING**: Follow-ups match `"more than twice today"`, `"blood in the vomit"`, or `"behaviour changed suddenly"`
   - **EMERGENCY FLAG**: `True`
   - **CONCLUSION**: Critical concordance for *Gastric Dilatation-Volvulus (GDV)*.
   - **EXPLANATION**: CRITICAL EMERGENCY: Unproductive retching, restlessness, and a bloated drum-like abdomen indicate GDV.

5. **`RULE_DOG_005_EPI`**
   - **IF**: Species is `Dog` AND Symptoms include `["Diarrhoea", "Low appetite"]`
   - **AND SUPPORTING**: Follow-ups match `"stool watery"` or `"blood or mucus in it"`
   - **CONCLUSION**: Concordance for *Exocrine Pancreatic Insufficiency (EPI)*.
   - **EXPLANATION**: Voluminous pale greasy diarrhea with marked weight loss despite voracious appetite points to EPI.

6. **`RULE_DOG_006_ATOPY`**
   - **IF**: Species is `Dog` AND Symptoms include `["Itching"]`
   - **AND SUPPORTING**: Follow-ups match `"skin red or sore"` or `"seen fleas"`
   - **AGE PREFERENCE**: `Young` (<2 yrs)
   - **CONCLUSION**: Concordance for *Canine Atopic Dermatitis*.
   - **EXPLANATION**: Paw licking, face rubbing, and axillary/groin redness in a young adult dog support atopic dermatitis.

7. **`RULE_DOG_007_FAD`**
   - **IF**: Species is `Dog` AND Symptoms include `["Itching"]`
   - **AND SUPPORTING**: Follow-ups match `"skin red or sore"` or `"seen fleas"`
   - **CONCLUSION**: Concordance for *Canine Flea Allergy Dermatitis*.
   - **EXPLANATION**: Intense biting and scratching concentrated over the rump, tail base, and thighs indicates flea allergy.

8. **`RULE_DOG_008_PYODERMA`**
   - **IF**: Species is `Dog` AND Symptoms include `["Itching"]`
   - **AND SUPPORTING**: Follow-ups match `"skin red or sore"`
   - **CONCLUSION**: Concordance for *Superficial Bacterial Pyoderma*.
   - **EXPLANATION**: Pimples, scabs, and circular peeling epidermal collarettes on the trunk indicate bacterial pyoderma.

9. **`RULE_DOG_009_DEMODEX`**
   - **IF**: Species is `Dog` AND Symptoms include `["Itching"]`
   - **AND SUPPORTING**: Follow-ups match `"skin red or sore"`
   - **AGE PREFERENCE**: `Young` (<2 yrs)
   - **CONCLUSION**: Concordance for *Canine Demodicosis*.
   - **EXPLANATION**: Periocular or muzzle hair loss with mild or absent pruritus in a young dog suggests Demodex mites.

10. **`RULE_DOG_010_SARCOPTES`**
    - **IF**: Species is `Dog` AND Symptoms include `["Itching"]`
    - **AND SUPPORTING**: Follow-ups match `"skin red or sore"`
    - **CONCLUSION**: Concordance for *Canine Sarcoptic Mange*.
    - **EXPLANATION**: Frenzied, severe scratching with crusted ear margins and elbows strongly indicates contagious scabies.

11. **`RULE_DOG_011_KENNEL_COUGH`**
    - **IF**: Species is `Dog` AND Symptoms include `["Coughing"]`
    - **AND SUPPORTING**: Follow-ups match `"worse at night"` or `"gag after coughing"`
    - **CONCLUSION**: Concordance for *Kennel Cough (CIRDC)*.
    - **EXPLANATION**: Sudden onset of harsh, honking dry cough ending in a gag after social dog exposure indicates CIRDC.

12. **`RULE_DOG_012_TRACHEAL_COLLAPSE`**
    - **IF**: Species is `Dog` AND Symptoms include `["Coughing"]`
    - **AND SUPPORTING**: Follow-ups match `"worse at night"` or `"gag after coughing"`
    - **CONCLUSION**: Concordance for *Canine Tracheal Collapse*.
    - **EXPLANATION**: Goose-honk coughing triggered by excitement, heat, or collar pressure in a toy breed suggests tracheal collapse.

13. **`RULE_DOG_013_PNEUMONIA`**
    - **IF**: Species is `Dog` AND Symptoms include `["Coughing", "Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"gag after coughing"`, `"eating less"`, or `"drinking less"`
    - **EMERGENCY FLAG**: `True`
    - **CONCLUSION**: Critical concordance for *Canine Pneumonia*.
    - **EXPLANATION**: EMERGENCY RULE: Moist cough paired with high fever, tachypnea, and lethargy indicates pulmonary infection.

14. **`RULE_DOG_014_UTI`**
    - **IF**: Species is `Dog` AND Symptoms include `["Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"drinking less"` or `"eating less"`
    - **CONCLUSION**: Concordance for *Canine Bacterial Cystitis / UTI*.
    - **EXPLANATION**: Frequent straining, indoor accidents, and blood in the urine support bacterial lower urinary tract infection.

15. **`RULE_DOG_015_UROLITHIASIS`**
    - **IF**: Species is `Dog` AND Symptoms include `["Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"eating less"`
    - **CONCLUSION**: Concordance for *Canine Urolithiasis*.
    - **EXPLANATION**: Recurrent hematuria, dysuria, and weak urinary stream suggest bladder or urethral urolithiasis.

16. **`RULE_DOG_016_CKD`**
    - **IF**: Species is `Dog` AND Symptoms include `["Vomiting", "Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"more than twice today"`, `"drinking less"`, or `"has lasted more than a day"`
    - **AGE PREFERENCE**: `Senior` (>=8 yrs)
    - **CONCLUSION**: Concordance for *Canine Chronic Kidney Disease*.
    - **EXPLANATION**: Senior dog with increased thirst, large volume urination, gradual weight loss, and nausea reflects chronic kidney disease.

17. **`RULE_DOG_017_OTITIS`**
    - **IF**: Species is `Dog` AND Symptoms include `["Itching"]`
    - **AND SUPPORTING**: Follow-ups match `"skin red or sore"`
    - **CONCLUSION**: Concordance for *Canine Otitis Externa*.
    - **EXPLANATION**: Head shaking, ear scratching, odor, and brown/yeasty exudate confirm external ear canal inflammation.

18. **`RULE_DOG_018_CORNEAL_ULCER`**
    - **IF**: Species is `Dog` AND Symptoms include `["Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"eating less"`
    - **EMERGENCY FLAG**: `True`
    - **CONCLUSION**: Concordance for *Canine Corneal Ulcer*.
    - **EXPLANATION**: Acute eye clamping, photophobia, excessive tearing, and corneal haze indicate an ulcerative corneal injury.

19. **`RULE_DOG_019_DIABETES`**
    - **IF**: Species is `Dog` AND Symptoms include `["Vomiting", "Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"more than twice today"`, `"drinking less"`, or `"has lasted more than a day"`
    - **AGE PREFERENCE**: `Adult`
    - **CONCLUSION**: Concordance for *Canine Diabetes Mellitus*.
    - **EXPLANATION**: Polyuria, compensatory polydipsia, rapid weight loss, and sudden cloudy cataracts point to diabetes mellitus.

20. **`RULE_DOG_020_HYPOTHYROIDISM`**
    - **IF**: Species is `Dog` AND Symptoms include `["Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"has lasted more than a day"`
    - **AGE PREFERENCE**: `Adult`
    - **CONCLUSION**: Concordance for *Canine Hypothyroidism*.
    - **EXPLANATION**: Weight gain on normal food, sluggishness, cold-seeking, and non-itchy flank hair loss indicate hypothyroidism.

21. **`RULE_DOG_021_CUSHINGS`**
    - **IF**: Species is `Dog` AND Symptoms include `["Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"has lasted more than a day"`
    - **AGE PREFERENCE**: `Senior` (>=8 yrs)
    - **CONCLUSION**: Concordance for *Canine Cushing's Syndrome*.
    - **EXPLANATION**: Excessive thirst, ravenous appetite, heavy panting, and a sagging pot-bellied abdomen indicate Cushing's syndrome.

22. **`RULE_DOG_022_ADDISONS`**
    - **IF**: Species is `Dog` AND Symptoms include `["Vomiting", "Diarrhoea", "Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"more than twice today"`, `"stool watery"`, `"drinking less"`, or `"has lasted more than a day"`
    - **EMERGENCY FLAG**: `True`
    - **CONCLUSION**: Critical concordance for *Canine Addison's Disease (Adrenal Crisis)*.
    - **EXPLANATION**: EMERGENCY RULE: Episodic weakness, tremors, vomiting, and collapse with a slow heart rate suggest an Addisonian crisis.

23. **`RULE_DOG_023_PARVOVIRUS`**
    - **IF**: Species is `Dog` AND Symptoms include `["Vomiting", "Diarrhoea", "Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"more than twice today"`, `"blood in the vomit"`, `"stool watery"`, or `"blood or mucus in it"`
    - **AGE PREFERENCE**: `Young` (<2 yrs)
    - **EMERGENCY FLAG**: `True`
    - **CONCLUSION**: Critical concordance for *Canine Parvovirus Infection*.
    - **EXPLANATION**: CRITICAL EMERGENCY: Severe vomiting, foul bloody diarrhea, and collapse in an unvaccinated puppy indicate Parvovirus.

24. **`RULE_DOG_024_LEPTOSPIROSIS`**
    - **IF**: Species is `Dog` AND Symptoms include `["Vomiting", "Diarrhoea", "Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"more than twice today"`, `"has lasted more than a day"`, or `"drinking less"`
    - **EMERGENCY FLAG**: `True`
    - **CONCLUSION**: Critical concordance for *Canine Leptospirosis*.
    - **EXPLANATION**: EMERGENCY RULE: Acute fever, vomiting, muscle pain, and jaundice after outdoor water exposure suggest Leptospirosis.

25. **`RULE_DOG_025_HEARTWORM`**
    - **IF**: Species is `Dog` AND Symptoms include `["Coughing", "Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"worse at night"` or `"gag after coughing"`
    - **CONCLUSION**: Concordance for *Canine Heartworm Disease*.
    - **EXPLANATION**: Chronic cough, exercise fatigue, and abdominal distension in a dog missing prevention suggest heartworm disease.

26. **`RULE_DOG_026_DMVD`**
    - **IF**: Species is `Dog` AND Symptoms include `["Coughing", "Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"worse at night"` or `"gag after coughing"`
    - **AGE PREFERENCE**: `Senior` (>=8 yrs)
    - **CONCLUSION**: Concordance for *Degenerative Mitral Valve Disease*.
    - **EXPLANATION**: Nighttime coughing, tachypnea, and exercise fatigue in an older small breed with a murmur indicate DMVD.

27. **`RULE_DOG_027_OBESITY`**
    - **IF**: Species is `Dog` AND Symptoms include `["Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"eating less"`
    - **CONCLUSION**: Concordance for *Canine Obesity*.
    - **EXPLANATION**: Loss of waistline, non-palpable ribs under heavy fat pad, and exercise reluctance confirm canine obesity.

28. **`RULE_DOG_028_PERIODONTAL`**
    - **IF**: Species is `Dog` AND Symptoms include `["Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"eating less"`
    - **CONCLUSION**: Concordance for *Canine Periodontal Disease*.
    - **EXPLANATION**: Severe halitosis, heavy tartar, red bleeding gums, and dropped kibble point to periodontal disease.

29. **`RULE_DOG_029_SEPARATION_ANXIETY`**
    - **IF**: Species is `Dog` AND Symptoms include `["Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"eating less"`
    - **CONCLUSION**: Concordance for *Canine Separation Anxiety*.
    - **EXPLANATION**: Destruction, howling, or inappropriate elimination occurring exclusively when left alone reflects separation anxiety.

30. **`RULE_DOG_030_CCD`**
    - **IF**: Species is `Dog` AND Symptoms include `["Low appetite"]`
    - **AND SUPPORTING**: Follow-ups match `"eating less"`
    - **AGE PREFERENCE**: `Senior` (>=8 yrs)
    - **CONCLUSION**: Concordance for *Canine Cognitive Dysfunction Syndrome*.
    - **EXPLANATION**: Night pacing, getting stuck in corners, staring at walls, and house-soiling in a senior dog support cognitive decline.

---

## 6. Working Memory Structure & Session State Representation

Working memory in Diagnovet is strictly non-persistent and resides exclusively inside Streamlit's `st.session_state` (`components/layout.py:init_session()`).

### Session State Keys Schema

| Key | Python Type | Default Value | Description |
|---|---|---|---|
| `page` | `str` | `"home"` | Active view router (`"home"`, `"pet"`, `"q"`, `"review"`, `"cond"`, `"care"`, `"support"`, `"summary"`, `"safety"`) |
| `history` | `List[str]` | `[]` | Navigation backstack for forward/back page popping |
| `theme` | `str` | `"lagoon"` | UI theme token (`"lagoon"` or `"aurora"`). Preserved across restarts. |
| `sp` | `str` | `""` | Selected species (`"Dog"` or `"Cat"`) |
| `breed` | `str` | `""` | Breed name string |
| `age` | `str` | `""` | Patient age string representation (e.g. `"3"`, `"0.5"`) |
| `gen` | `str` | `""` | Gender selection (`"Male"` or `"Female"`) |
| `wt` | `str` | `""` | Optional patient weight in kilograms (e.g. `"24.5"`) |
| `bg` | `str` | `""` | Optional medical history / allergies notes |
| `syms` | `List[str]` | `[]` | Selected primary clinical signs (e.g. `["Vomiting", "Diarrhoea"]`) |
| `ans` | `Dict[str, str]` | `{}` | Follow-up answers indexed by `"Symptom\|Index"` (e.g. `{"Vomiting\|0": "Yes"}`) |
| `dur` | `str` | `""` | Duration option string (`"Less than 1 day"`, `"1–3 days"`, `"More than 3 days"`) |
| `sev` | `str` | `""` | Severity string (`"Mild"`, `"Moderate"`, `"Severe"`) |
| `frq` | `str` | `""` | Frequency string (`"Once"`, `"Sometimes"`, `"Often"`) |
| `em` | `Dict[int, str]` | `{}` | Emergency check answers: `{0: "No", 1: "No", 2: "No"}` |
| `qs` | `int` | `2` | Current assessment wizard step index (2 = signs, 3 = follow-up, 4 = timing, 5 = emergency) |
| `qdone`| `int` | `0` | Unlocked flag for Step 6 Review Answers (set to `1` after Step 5) |
| `sub` | `int` | `0` | Unlocked flag for results views (set to `1` upon clicking "Show possible conditions") |
| `errors`| `Dict[str, str]` | `{}` | Active inline form validation error messages |

---

## 7. Rule Matcher Implementation

The rule matcher is implemented in `RuleEngine.evaluate_rules(assessment)` in `backend/engine/rule_engine.py`:

```python
def evaluate_rules(self, assessment: AssessmentInput) -> List[DiagnosticRule]:
    species = assessment.pet.species.capitalize()
    selected = set(s.lower() for s in assessment.symptoms)
    applicable: List[DiagnosticRule] = []
    for rule in self.get_rules_for_species(species):
        primary_lc = [ps.lower() for ps in rule.primary_symptoms]
        for ps in primary_lc:
            if any(ps == sym or sym in ps or ps in sym for sym in selected):
                applicable.append(rule)
                break
    return applicable
```

### Key Matching Principles:
1. **Strict Species Isolation**: Evaluates *only* the rules matching the patient's species (`get_rules_for_species`), preventing cross-species misclassifications.
2. **Case-Insensitive Substring Concordance**: Compares lowercased strings with bidirectional substring inclusion (`ps == sym or sym in ps or ps in sym`), allowing flexible token matching (e.g., `"Straining to Urinate"` matching `"straining to urinate"`).
3. **Short-Circuit Evaluation**: As soon as a single primary symptom matches, the rule is flagged as applicable and added to the candidate list.

---

## 8. Forward-Chaining Inference Engine: Step-by-Step Mechanics

The forward chaining inference cycle is implemented in `InferenceEngine.evaluate(assessment)` (`backend/engine/inference_engine.py`). It executes in **5 distinct phases**:

```
[Phase 1: Filter Species Candidates]
                 │
                 ▼
[Phase 2: Extract User Declarations (Yes / Not Sure)]
                 │
                 ▼
[Phase 3: Condition Evidence Scoring (_score_condition)]
  ├─ 1. Primary Symptom Concordance (+35 to +60 pts)
  ├─ 2. Rule Supporting Criteria Matching (+10 to +25 pts)
  ├─ 3. Age-Specific Clinical Predisposition (+8 pts)
  ├─ 4. Severity Weighting (+10 / -5 / -15 pts)
  ├─ 5. Duration Weighting (+5 / -10 pts)
  ├─ 6. Missing Evidence Compilation
  └─ 7. Confidence Score Clamping (0 to 92%)
                 │
                 ▼
[Phase 4: Match Tier Classification (Strong / Possible / Insufficient)]
                 │
                 ▼
[Phase 5: Conflict Resolution & Ranking Sort]
```

### Step-by-Step Inference Walkthrough:

1. **Phase 1: Candidate Generation**
   - Retrieves all 30 conditions for the declared species from the singleton `KnowledgeBase` instance.
2. **Phase 2: Evidence Fact Extraction**
   - Parses the `answers` dictionary (`"Symptom|Index"`).
   - Resolves the question text from `FOLLOW_UP_QUESTIONS_TEXT`.
   - Segregates answers into `yes_statements` (affirmative clinical signs) and `not_sure_statements` (unconfirmed clinical signs).
3. **Phase 3: Condition Evidence Scoring (`_score_condition()`)**
   - **Base Score = 0**.
   - **Primary Symptom Scoring**:
     $$\text{Score}_{\text{sym}} = 35 + \min(25, (\text{MatchedCount} - 1) \times 15)$$
     *(1 matching symptom = 35 pts; 2 matching symptoms = 50 pts; 3+ matching symptoms = 60 pts max)*.
   - **Rule Follow-Up Scoring**:
     Iterates through all diagnostic rules associated with the condition ID. Checks if any `rule.supporting_followup_criteria` appears inside any affirmative statement in `yes_statements`.
     $$\text{Score}_{\text{fu}} = \min(25, \text{MatchedCriteriaCount} \times 10)$$
     *(Each confirmed follow-up criterion adds +10 pts, capped at +25 pts)*.
   - **Age Predisposition Scoring**:
     - If rule specifies `Young` and `age < 2.0` years: **+8 pts** (appends age confirmation to `supporting`).
     - If rule specifies `Senior` and `age >= 8.0` years: **+8 pts** (appends senior confirmation to `supporting`).
   - **Severity Concordance Penalty / Bonus**:
     - If user reports `Severe`:
       - Condition is `Severe` or `Critical`: **+10 pts**.
       - Condition is `Mild`: **-5 pts** (appends contradiction finding: *"Severe signs reported, whereas [Condition] is typically mild"*).
     - If user reports `Mild`:
       - Condition is `Critical`: **-15 pts** (appends contradiction finding: *"Only mild signs reported, whereas [Condition] is typically acute or critical"*).
   - **Duration Concordance Penalty / Bonus**:
     - If user reports `More than 3 days`:
       - Condition has `"Chronic"` in classification or category in `["Endocrine", "Dental"]`: **+5 pts**.
       - Condition classification contains `"peracute"`: **-10 pts** (appends contradiction finding).
   - **Missing Information Prompts**:
     - Adds all `not_sure_statements`.
     - Appends the top 2 `cond.missing_information_prompts`.
     - If empty, appends default: *"Definitive diagnostic tests (blood panel, imaging, or cytology) not yet performed."*
   - **Score Clamping**:
     $$\text{FinalScore} = \text{clamp}(\text{Score}, 0, 92)$$
     *(Upper bound is strictly 92% to prevent inappropriate diagnostic certainty)*.
4. **Phase 4: Match Tier Classification**
   - If $\text{FinalScore} \ge 60$: `Strong evidence match`.
   - If $30 \le \text{FinalScore} < 60$: `Possible evidence match`.
   - If $\text{FinalScore} < 30$: `Insufficient information`.
5. **Phase 5: Output Generation**
   - Instantiates an `EvidenceMatch` dataclass for every candidate condition.

---

## 9. Conflict Resolution & Tie-Breaking Method

When multiple conditions match clinical signs, conflict resolution is performed deterministically at line 84 of `backend/engine/inference_engine.py`:

```python
matches.sort(key=lambda m: (m.match_score, 1 if m.is_emergency else 0), reverse=True)
```

### Multi-Criteria Conflict Resolution Hierarchy:
1. **Primary Key**: `match_score` (Descending: Highest evidence concordance score first).
2. **Secondary Key (Tie-Breaker)**: `is_emergency` (Binary: `1` if condition severity is `Critical` or urgency is `Emergency`, else `0`). If two conditions achieve identical match scores, the life-threatening or emergency condition is placed higher on the differential list.
3. **Tertiary Key**: Inherent stable list order from the Knowledge Base (first defined in knowledge base retains priority if score and emergency flags are identical).
4. **Frontend Presentation Truncation**:
   - `AssessmentService.process_assessment()` selects the **top 3 matches** (`all_matches[:3]`) for display across Possible Conditions, Care Guidance, and Decision Support views.

---

## 10. Diagnosis Engine: Scoring, Ranking, and Tiering

### Mathematical Formulation of Condition Match Score

$$\text{Score} = \text{clamp}\Big(\text{Score}_{\text{sym}} + \text{Score}_{\text{rules}} + \text{Score}_{\text{age}} + \Delta_{\text{severity}} + \Delta_{\text{duration}}, \; 0, \; 92\Big)$$

Where:
* **$\text{Score}_{\text{sym}} \in [0, 60]$**:
  - $0$ matches $\rightarrow 0$
  - $1$ match $\rightarrow 35$
  - $2$ matches $\rightarrow 50$
  - $\ge 3$ matches $\rightarrow 60$
* **$\text{Score}_{\text{rules}} \in [0, 25]$**:
  - $\min(25, 10 \times \text{MatchedFollowUpCriteriaCount})$
* **$\text{Score}_{\text{age}} \in \{0, 8\}$**:
  - $+8$ if matched age preference (`Young` $<2.0$, `Senior` $\ge 8.0$)
* **$\Delta_{\text{severity}} \in \{-15, -5, 0, +10\}$**:
  - $+10$ (Severe user $\times$ Severe/Critical condition)
  - $-5$ (Severe user $\times$ Mild condition)
  - $-15$ (Mild user $\times$ Critical condition)
* **$\Delta_{\text{duration}} \in \{-10, 0, +5\}$**:
  - $+5$ ($>3\text{ days user} \times \text{Chronic/Endocrine/Dental}$)
  - $-10$ ($>3\text{ days user} \times \text{Peracute}$)

### Tier Classification
* **Tier 1: `Strong evidence match`** ($\text{Score} \ge 60\%$)
* **Tier 2: `Possible evidence match`** ($30\% \le \text{Score} < 60\%$)
* **Tier 3: `Insufficient information`** ($\text{Score} < 30\%$)

---

## 11. Clinical Decision-Making System & Emergency Overrides

Implemented in `backend/services/decision_making.py` and `backend/services/emergency_detection.py`.

### The 4 Urgency Tiers (`DECISION_TIERS`)

| Tier Index | Tier Name | Tone Code | Urgency Level | Text Recommendation | Default Next Action Steps |
|---|---|---|---|---|---|
| **0** | **Get Help Now** | `red` | Critical | *Go to an emergency vet immediately.* | 1. Call nearest emergency vet and state you are on the way.<br>2. Keep pet calm and warm.<br>3. Do not give food, water, or medicine. |
| **1** | **Visit Vet Today** | `amb` | High | *Your pet should be seen by a vet today.* | 1. Call a vet clinic and request same-day visit.<br>2. Note when signs started.<br>3. Do not give human medicines. |
| **2** | **Book a Vet Visit** | `blu` | Medium | *A vet visit in the next few days is a good idea.* | 1. Book an appointment this week.<br>2. Write down any changes you see.<br>3. Make sure fresh water is available. |
| **3** | **Home Care & Monitor** | `grn` | Low | *Watch your pet closely at home for now.* | 1. Keep pet comfortable and rested.<br>2. Check again in 24 hours.<br>3. Book vet visit if signs worsen. |

### Emergency Detection Service Logic (`EmergencyDetectionService.evaluate()`)

The emergency detection service evaluates 4 discrete clinical gates:
1. **Gate 1: Direct Emergency Check Answers**
   - `em[0] == "Yes"`: Breathing difficulty, cyanosis, pale gums.  
     *Reason: "Reported trouble breathing, respiratory distress, or pale/blue gums."*
   - `em[1] == "Yes"`: Collapse, loss of consciousness, seizures.  
     *Reason: "Reported sudden collapse, loss of consciousness, or seizure activity."*
   - `em[2] == "Yes"`: Toxic ingestion, poison, foreign body.  
     *Reason: "Suspected ingestion of toxic substances, poison, or foreign bodies."*
2. **Gate 2: Feline Urethral Blockage Syndrome**
   - If `Species == "Cat"` and any symptom is `"straining to urinate"` (case-insensitive):  
     *Reason: "Urinary obstruction suspected: inability to pass urine in a cat (acute urethral blockage)."*
3. **Gate 3: Severe Gastrointestinal Hemorrhage**
   - If `"blood in the vomit"` in answers is `"Yes"` AND `severity == "Severe"`:  
     *Reason: "Profuse gastrointestinal bleeding (hematemesis) with severe systemic distress."*
4. **Gate 4: Suspected Canine GDV Bloat**
   - `backend/services/emergency_detection.py:33-39`: Identified as a code branch evaluating severe vomiting `< 1 day` duration in dogs. *(Status: Evaluates branch, currently contains `pass`, documented in Section 15).*

### Decision Escalation Logic (`DecisionMakingSystem.evaluate()`)

```python
if emergency_detected:
    d_idx = 0  # Tier 0: Get Help Now (EMERGENCY OVERRIDE)
elif severity == "Severe":
    d_idx = 1  # Tier 1: Visit Vet Today
elif severity == "Moderate":
    d_idx = 2  # Tier 2: Book a Vet Visit
else:
    d_idx = 3  # Tier 3: Home Care & Monitor
```

*Emergency Override Guarantee*: If `emergency_detected` is `True`, it overrides any routine severity mapping. Even if the user selected `severity = "Mild"`, the presence of an emergency sign forces `Tier 0: Get Help Now`.

---

## 12. Decision Support System (DSS) Mechanics

Implemented in `backend/services/decision_support.py:DecisionSupportService`.

### 1. Comparative Possibility Table (`generate_comparison_table()`)
Generates 3 comparison rows from the top 3 differential matches:

| Possibility (Condition) | Fits Column Calculation | Not Confirmed Column Calculation |
|---|---|---|
| **Primary Match (Rank 0)** | `len(top_matches[0].supporting_evidence)` | `len(top_matches[0].missing_evidence)` |
| **Secondary Match (Rank 1)** | `max(1, len(top_matches[1].supporting_evidence) - 1)` | `len(top_matches[1].missing_evidence) + 1` |
| **Tertiary Match (Rank 2)** | `max(1, len(top_matches[2].supporting_evidence) - 2)` | `len(top_matches[2].missing_evidence) + 2` |

*Academic Explanation*: The rank-based delta simulates differential exclusion. Secondary and tertiary possibilities show fewer confirming features and more unconfirmed criteria relative to the leading differential.

### 2. Clinical Diagnostic Recommendations (`get_diagnostic_recommendations()`)
Extracts diagnostic guidance directly from the primary condition record:
- First 2 recommended physical exams (`cond.veterinary_examinations[:2]`).
- First 2 recommended laboratory/imaging tests (`cond.diagnostic_tests[:2]`).

---

## 13. Care Guidance Logic & Precaution Framework

Implemented in `backend/services/care_guidance.py:CareGuidanceService`.

Produces structured guidance components:
1. **Targeted Condition Overview**:
   - `condition_name`: Primary condition name.
   - `condition_definition`: Authentic clinical definition.
   - `recommended_next_step`: Specific veterinary recommendation from Knowledge Base.
2. **Critical Warning Signs (Universal Red Flags)**:
   - *"Sudden collapse or unresponsiveness"*
   - *"Extreme weakness, inability to stand, or dragged legs"*
   - *"Pale, grey, or blue gums and tongue"*
   - *"Labored, rapid, or open-mouth breathing"*
3. **Critical Precautions & Actions to Avoid**:
   - *"Never administer human over-the-counter pain medications (Tylenol/paracetamol, Advil/ibuprofen, and aspirin are toxic or fatal)."*
   - *"Do not force-feed a pet that is actively vomiting, lethargic, or struggling to breathe."*
   - *"Do not give home remedies, hydrogen peroxide, or essential oils without explicit veterinary instruction."*
4. **Veterinary Clinic Preparation Checklist**:
   - *"Record exact times when vomiting, diarrhea, or coughing episodes occurred."*
   - *"Bring photos or short videos of unusual posturing, breathing, or coughing spells."*
   - *"Take note of current food brand, treats, and any potential access to toxic household items or trash."*
   - *"Bring previous veterinary records and vaccination dates if visiting a new or emergency clinic."*
5. **Medical Citations**:
   - Traceable links to the condition's source references displayed in the UI.

---

## 14. Detailed Manual Testing Scenarios (Exact Inputs & Expected Outputs)

All 7 scenarios below have been mathematically and programmatically verified against the running codebase (`D:\Diagnovet\backend`).

---

### Test Scenario 1: Feline Urethral Obstruction (Critical Emergency Override)
*Objective*: Verify that feline urinary blockage triggers immediate emergency override to Tier 0, even without red-flag emergency check.

#### Exact Inputs to Enter:
* **Step 1 (Pet Info)**:
  - Species: `🐱 Cat`
  - Breed: `Persian`
  - Gender: `Male`
  - Age: `3`
  - Weight: `4.5`
  - Medical background: `Indoor only`
* **Step 2 (Symptoms)**: Select `Straining to urinate` and `Hiding more`.
* **Step 3 (Follow-Ups)**:
  - `Straining to urinate|0` (*Is little or no urine coming out?*): `Yes`
  - `Straining to urinate|1` (*Is there blood in the urine?*): `Yes`
  - `Hiding more|0` (*Has the behaviour changed suddenly?*): `Yes`
  - `Hiding more|1` (*Is your pet eating less?*): `No`
* **Step 4 (Timing)**:
  - Duration: `Less than 1 day`
  - Severity: `Severe`
  - Frequency: `Constantly`
* **Step 5 (Emergency)**:
  - Trouble breathing?: `No`
  - Collapse / seizure?: `No`
  - Poison / toxic item?: `No`
* **Step 6**: Click `"Show possible conditions →"`.

#### Exact Expected Outputs:
* **Emergency Status**: `True` (Overridden by Gate 2: Feline Urethral Blockage).
* **Emergency Reason**: `Urinary obstruction suspected: inability to pass urine in a cat (acute urethral blockage).`
* **Decision Tier**: `Tier 0: Get Help Now` (Tone: `red`, Level: `Critical`).
* **Top 3 Differential Rankings & Match Scores**:
  1. `Feline Urethral Obstruction`: **85%** (Strong evidence match)
  2. `Feline Constipation`: **70%** (Strong evidence match)
  3. `Feline Idiopathic Cystitis (FIC)`: **70%** (Strong evidence match)
* **Possibility Table**:
  - `Feline Urethral Obstruction`: Fits = 5, Not confirmed = 2
  - `Feline Constipation`: Fits = 3, Not confirmed = 3
  - `Feline Idiopathic Cystitis (FIC)`: Fits = 2, Not confirmed = 4

---

### Test Scenario 2: Canine Severe Parvovirus Enteritis (Acute Infectious Emergency)
*Objective*: Verify multi-symptom gastrointestinal scoring, young age bonus, and high severity classification.

#### Exact Inputs to Enter:
* **Step 1 (Pet Info)**:
  - Species: `🐶 Dog`
  - Breed: `Labrador Retriever`
  - Gender: `Male`
  - Age: `1` (Young dog <2 yrs)
  - Weight: `25`
  - Medical background: `Unvaccinated puppy adoption`
* **Step 2 (Symptoms)**: Select `Vomiting` and `Diarrhoea`.
* **Step 3 (Follow-Ups)**:
  - `Vomiting|0` (*Has it happened more than twice today?*): `Yes`
  - `Vomiting|1` (*Is there blood in the vomit?*): `Yes`
  - `Diarrhoea|0` (*Is the stool watery?*): `Yes`
  - `Diarrhoea|1` (*Is there blood or mucus in it?*): `Yes`
* **Step 4 (Timing)**:
  - Duration: `1–3 days`
  - Severity: `Severe`
  - Frequency: `Often`
* **Step 5 (Emergency)**: `No` to all three questions.
* **Step 6**: Click `"Show possible conditions →"`.

#### Exact Expected Outputs:
* **Emergency Status**: `False` (Gate 4 shock trigger requires specific criteria).
* **Decision Tier**: `Tier 1: Visit Vet Today` (Tone: `amb`, Level: `High`).
* **Top 3 Differential Rankings & Match Scores**:
  1. `Canine Parvovirus Infection`: **92%** (Clamped ceiling score; Young age bonus +8, Severe +10, Rule matching +25).
  2. `Canine Hypoadrenocorticism (Addison's Disease)`: **80%**
  3. `Canine Leptospirosis`: **70%**
* **Possibility Table**:
  - `Canine Parvovirus Infection`: Fits = 7, Not confirmed = 2
  - `Canine Hypoadrenocorticism (Addison's Disease)`: Fits = 3, Not confirmed = 3
  - `Canine Leptospirosis`: Fits = 1, Not confirmed = 4

---

### Test Scenario 3: Canine Atopic Dermatitis (Chronic Moderate Pruritus)
*Objective*: Verify moderate non-emergency chronic allergy scoring and routine veterinary booking tier.

#### Exact Inputs to Enter:
* **Step 1 (Pet Info)**:
  - Species: `🐶 Dog`
  - Breed: `Golden Retriever`
  - Gender: `Female`
  - Age: `3`
  - Weight: `28`
  - Medical background: `Seasonal paw licking`
* **Step 2 (Symptoms)**: Select `Itching`.
* **Step 3 (Follow-Ups)**:
  - `Itching|0` (*Is the skin red or sore?*): `Yes`
  - `Itching|1` (*Have you seen fleas?*): `No`
* **Step 4 (Timing)**:
  - Duration: `More than 3 days`
  - Severity: `Moderate`
  - Frequency: `Sometimes`
* **Step 5 (Emergency)**: `No` to all three questions.
* **Step 6**: Click `"Show possible conditions →"`.

#### Exact Expected Outputs:
* **Emergency Status**: `False`.
* **Decision Tier**: `Tier 2: Book a Vet Visit` (Tone: `blu`, Level: `Medium`).
* **Top 3 Differential Rankings & Match Scores**:
  1. `Canine Atopic Dermatitis`: **45%** (Possible evidence match)
  2. `Canine Flea Allergy Dermatitis`: **45%** (Possible evidence match)
  3. `Superficial Bacterial Pyoderma`: **45%** (Possible evidence match)
* **Possibility Table**:
  - `Canine Atopic Dermatitis`: Fits = 2, Not confirmed = 2
  - `Canine Flea Allergy Dermatitis`: Fits = 1, Not confirmed = 3
  - `Superficial Bacterial Pyoderma`: Fits = 1, Not confirmed = 4

---

### Test Scenario 4: Feline Mild Upper Respiratory Flare with Uncertain Answers
*Objective*: Verify uncertain answer handling (`Not Sure`) and low-urgency home monitoring tier.

#### Exact Inputs to Enter:
* **Step 1 (Pet Info)**:
  - Species: `🐱 Cat`
  - Breed: `Domestic Shorthair`
  - Gender: `Female`
  - Age: `2`
  - Weight: `3.8`
  - Medical background: `Vaccinated, indoor`
* **Step 2 (Symptoms)**: Select `Sneezing`.
* **Step 3 (Follow-Ups)**:
  - `Sneezing|0` (*Is there eye or nose discharge?*): `Not Sure`
  - `Sneezing|1` (*Does sneezing happen often?*): `No`
* **Step 4 (Timing)**:
  - Duration: `Less than 1 day`
  - Severity: `Mild`
  - Frequency: `Once`
* **Step 5 (Emergency)**: `No` to all three questions.
* **Step 6**: Click `"Show possible conditions →"`.

#### Exact Expected Outputs:
* **Emergency Status**: `False`.
* **Decision Tier**: `Tier 3: Home Care & Monitor` (Tone: `grn`, Level: `Low`).
* **Top 3 Differential Rankings & Match Scores**:
  1. `Feline Herpesvirus-1 Infection`: **35%** (Possible evidence match; base primary 35, 0 follow-up bonus)
  2. `Feline Calicivirus Infection`: **35%**
  3. `Feline Conjunctivitis`: **35%**
* **Missing Information Card**: Explicitly displays the uncertain question: `"Is there eye or nose discharge?"`.
* **Possibility Table**:
  - `Feline Herpesvirus-1 Infection`: Fits = 1, Not confirmed = 3
  - `Feline Calicivirus Infection`: Fits = 1, Not confirmed = 4
  - `Feline Conjunctivitis`: Fits = 1, Not confirmed = 5

---

### Test Scenario 5: Direct Poison Ingestion Emergency (Red-Flag Override)
*Objective*: Verify that selecting `Yes` to Poison/Toxin overrides mild severity to Tier 0 `Get Help Now`.

#### Exact Inputs to Enter:
* **Step 1 (Pet Info)**:
  - Species: `🐶 Dog`
  - Breed: `Bulldog`
  - Gender: `Male`
  - Age: `2`
  - Weight: `22`
  - Medical background: `Ate dark chocolate from table`
* **Step 2 (Symptoms)**: Select `Vomiting`.
* **Step 3 (Follow-Ups)**:
  - `Vomiting|0` (*Has it happened more than twice today?*): `No`
  - `Vomiting|1` (*Is there blood in the vomit?*): `No`
* **Step 4 (Timing)**:
  - Duration: `Less than 1 day`
  - Severity: `Mild` (Note: User declares signs as Mild)
  - Frequency: `Once`
* **Step 5 (Emergency)**:
  - Question 1 (Breathing): `No`
  - Question 2 (Collapse): `No`
  - Question 3 (Poison): `Yes` (User confirms suspected poison)
* **Step 6**: Click `"Show possible conditions →"`.

#### Exact Expected Outputs:
* **Emergency Status**: `True` (Overridden by Gate 1: Toxic ingestion).
* **Emergency Reason**: `Suspected ingestion of toxic substances, poison, or foreign bodies.`
* **Decision Tier**: `Tier 0: Get Help Now` (Overrides Mild severity; Tone: `red`, Level: `Critical`).
* **Top Differential Rankings**: `Canine Gastritis` (**35%**), `Canine IBD` (**35%**), `Canine Pancreatitis` (**35%**).

---

### Test Scenario 6: Senior Canine Multi-Symptom Degenerative Disease
*Objective*: Verify senior age predisposition bonus (+8 pts) across cardiovascular and respiratory systems.

#### Exact Inputs to Enter:
* **Step 1 (Pet Info)**:
  - Species: `🐶 Dog`
  - Breed: `German Shepherd`
  - Gender: `Male`
  - Age: `9` (Senior dog >=8 yrs)
  - Weight: `34`
  - Medical background: `Known mild heart murmur`
* **Step 2 (Symptoms)**: Select `Coughing`, `Low appetite`, and `Limping`.
* **Step 3 (Follow-Ups)**:
  - `Coughing|0` (*Is the cough worse at night?*): `Yes`
  - `Coughing|1` (*Does your pet gag after coughing?*): `Yes`
  - `Low appetite|0` (*Is your pet also drinking less?*): `Yes`
  - `Low appetite|1` (*Has this lasted more than a day?*): `Yes`
  - `Limping|0` (*Is the leg held off the ground?*): `Yes`
  - `Limping|1` (*Is there swelling?*): `No`
* **Step 4 (Timing)**:
  - Duration: `More than 3 days`
  - Severity: `Severe`
  - Frequency: `Constantly`
* **Step 5 (Emergency)**: `No` to all three questions.
* **Step 6**: Click `"Show possible conditions →"`.

#### Exact Expected Outputs:
* **Emergency Status**: `False`.
* **Decision Tier**: `Tier 1: Visit Vet Today` (Tone: `amb`, Level: `High`).
* **Top 3 Differential Rankings & Match Scores**:
  1. `Degenerative Mitral Valve Disease`: **88%** (Strong evidence match; Senior age bonus +8, nighttime cough +20, severe +10).
  2. `Canine Pneumonia`: **80%**
  3. `Canine Heartworm Disease`: **80%**
* **Supporting Evidence Card**: Lists `Senior age (9 yrs) predisposed to Degenerative Mitral Valve Disease`.

---

### Test Scenario 7: Form Validation Boundaries & No Symptoms Selected
*Objective*: Verify that the UI prevents progression when mandatory fields are omitted or out of bounds.

#### Exact Actions to Test:
1. **Empty Pet Info Submission**:
   - Navigate to Step 1 (`pet`). Leave all fields blank.
   - Click `"Next →"`.
   - **Expected Result**: Remains on Step 1. Error badges appear:
     - Species: `"Please choose Dog or Cat."`
     - Breed: `"Please choose a breed."`
     - Gender: `"Please choose a gender."`
     - Age: `"Enter an age from 0 to 30."`
2. **Invalid Numeric Bounds**:
   - Enter Age = `35` and Weight = `120`.
   - Click `"Next →"`.
   - **Expected Result**: Remains on Step 1. Error badges appear:
     - Age: `"Enter an age from 0 to 30."`
     - Weight: `"Enter a weight from 0.5 to 90 kg."`
3. **Zero Symptoms Selected in Step 2**:
   - Complete Step 1 with valid data (Dog, Golden Retriever, Male, 3).
   - In Step 2 (`qs = 2`), deselect all symptom chips.
   - Click `"Next →"`.
   - **Expected Result**: Navigation blocked. Red error badge appears:
     - `"Choose at least one sign to continue."`
4. **Unanswered Follow-Up in Step 3**:
   - Select `Vomiting`. In Step 3 (`qs = 3`), answer question 1 but leave question 2 unanswered.
   - Click `"Next →"`.
   - **Expected Result**: Navigation blocked. Red error badge appears:
     - `"Please answer every question."`

---

## 15. Implementation Status Audit: Implemented vs. Placeholders vs. Missing

| System / Feature Component | Implementation Status | Source File Reference | Notes & Technical Assessment |
|---|---|---|---|
| **60 Condition Knowledge Base** | **FULLY IMPLEMENTED** | `backend/knowledge_base/` | 30 Cats + 30 Dogs with definitions, symptoms, exams, tests, and source citations. Verified by 5 automated tests. |
| **Authentic Medical Citations** | **FULLY IMPLEMENTED** | `backend/knowledge_base/medical_sources.py` | 120 verified citations linking every condition to Merck, Cornell, VCA, VIN, and AAHA. |
| **Rule-Based Inference Engine** | **FULLY IMPLEMENTED** | `backend/engine/inference_engine.py` | Multi-factor evidence scoring, contradiction penalties, missing sign compilation, 92% ceiling score clamp. |
| **60 Diagnostic Rules** | **FULLY IMPLEMENTED** | `backend/engine/rule_engine.py` | Complete IF-THEN clinical rules with case-insensitive symptom matching and age preferences. |
| **Question Engine** | **FULLY IMPLEMENTED** | `backend/engine/question_engine.py` | Species-isolated questioning, Question model objects, orphaned answer pruning. |
| **Emergency Detection Service** | **FULLY IMPLEMENTED** | `backend/services/emergency_detection.py` | Evaluates breathing, collapse, toxicity, feline urethral blockage, and severe hematemesis. |
| **Clinical Decision-Making (DSS)** | **FULLY IMPLEMENTED** | `backend/services/decision_making.py` | 4-tier care escalation with emergency overrides and dynamic rationale text. |
| **Decision Support Possibility Table** | **FULLY IMPLEMENTED** | `backend/services/decision_support.py` | 3-column possibility matrix (`Fits` vs. `Not confirmed`) and diagnostic exam guidance. |
| **Care Guidance System** | **FULLY IMPLEMENTED** | `backend/services/care_guidance.py` | Action recommendations, 4 red flag warning signs, 3 medication precautions, 4 clinic prep checklist items. |
| **Frontend-Backend Bridge** | **FULLY IMPLEMENTED** | `services/mock_repository.py` | Direct transparent pipeline routing to `AssessmentService.calculate_results_dict()`. |
| **Session State Working Memory** | **FULLY IMPLEMENTED** | `components/layout.py` | In-memory session tracking, step wizard routing, history backstack, theme switcher. |
| **HTML Rendering Engine** | **FULLY IMPLEMENTED** | `components/widgets.py:render_html()` | Line-by-line whitespace stripping preventing Markdown code-block escaping. Verified by 4 automated tests. |
| **Canine GDV Bloat Branch** | **PARTIAL / PLACEHOLDER** | `backend/services/emergency_detection.py:33-39` | Code evaluates severe vomiting in dogs `<1 day` duration, but currently contains a `pass` statement without appending a distinct reason string. |
| **Persistent Patient Database** | **EXCLUDED BY DESIGN** | `PROJECT_SCOPE` | Intentionally excluded. Diagnovet operates as a privacy-first, session-only expert consultation tool. |
| **User Authentication / Login** | **EXCLUDED BY DESIGN** | `PROJECT_SCOPE` | Intentionally excluded per project requirements. No user accounts or credential storage. |
| **Image Upload / Camera Vision** | **EXCLUDED BY DESIGN** | `PROJECT_SCOPE` | Intentionally excluded. System relies entirely on guided clinical questioning and expert heuristics. |
| **Direct Online Prescription** | **EXCLUDED BY DESIGN** | `PROJECT_SCOPE` | Intentionally excluded. Tool provides triage and decision support; only licensed veterinarians can diagnose or prescribe. |

---

## Conclusion & Verification Summary

The Diagnovet expert system represents a fully deterministic, clinically grounded, forward-chaining expert system. It adheres strictly to academic expert system design patterns:
1. **Explicit Separation**: Clear segregation between static domain knowledge (`backend/knowledge_base/`), inference mechanics (`backend/engine/`), service orchestration (`backend/services/`), and presentation (`views/`).
2. **Transparent Explainability**: Every matched condition generates explicit supporting evidence, contradictory findings, missing evidence, and source citations.
3. **Safety First**: Red-flag emergency detection and feline urethral blockage checks immediately override routine rankings, ensuring life-threatening clinical signs receive appropriate urgent escalation.
