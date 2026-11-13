# Diagnovet — Smart Pet Health Diagnosis & Decision Support System

> **Academic Expert System & Clinical Decision Support Portal for Cats and Dogs**  
> Developed for **IAI CCP** &bull; **Phase 1: Complete Frontend Architecture & Pixel-Accurate UI**

Diagnovet is a guided, web-based veterinary decision-support portal that assists pet guardians in assessing health concerns in cats and dogs through a structured consultation workflow, understanding possible disease concordance, and receiving clear care guidance.

The frontend is built using **Python and Streamlit**, directly matching the approved UI design reference in `design_reference/diagnovet_flow.html`.

---

## 🎨 Design System: "Lagoon" & "Aurora"

Diagnovet provides two carefully calibrated themes with instant switching:

- **Lagoon (Default Light Theme)**:
  - Background: `#E8FAF6`
  - Card & Surfaces: `#FFFFFF`
  - Text & Muted: `#0B2F3A` and `#5C8089`
  - Border & Dividers: `#CBEBE4`
  - Primary Accent: `#2E7DFF`
  - Gradient: `linear-gradient(135deg, #00C9A7, #2E7DFF 55%, #8A5CFF)`
  - Glow: `0 8px 26px rgba(46, 125, 255, 0.25)`

- **Aurora (Dark Theme)**:
  - Background: `#0F0B24`
  - Card & Surfaces: `#1A1438`
  - Text & Muted: `#F2EEFF` and `#A59CC9`
  - Border: `#2D2557`
  - Primary Accent: `#7B5CFF`
  - Gradient: `linear-gradient(135deg, #00E5C3, #7B5CFF 55%, #FF5FA2)`
  - Glow: `0 8px 30px rgba(123, 92, 255, 0.33)`

- **4 Structured Decision Outcomes**:
  - 🚨 **Get Help Now (Critical)**: `#E5484D`
  - 🏥 **Visit Vet Today (High)**: `#E69B28`
  - 📅 **Book a Vet Visit (Medium)**: `#2E7DFF` (Lagoon) / `#7B5CFF` (Aurora)
  - 🏡 **Home Care & Monitor (Low)**: `#27966F`

---

## 🧭 The 9 Required Views

All consultation data remains in Streamlit `session_state` only. No database, permanent records, or tracking are used.

1. **🏠 Home (`views/home.py`)**: Hero banner, Dog & Cat entry cards, 4-step walkthrough, emergency alert, and veterinary disclaimer.
2. **🐾 Pet Information (`views/pet_information.py`)**: Species selection, species-specific breed selection, gender, age validation (0–30 yrs), weight, and medical background.
3. **🩺 Assessment (`views/assessment.py`)**:
   - *Step 2*: Species-specific symptom chips (Dog vs Cat).
   - *Step 3*: Dynamic follow-up questions for chosen symptoms (`Yes / No / Not Sure`).
   - *Step 4*: Duration, severity (`Mild / Moderate / Severe`), and frequency.
   - *Step 5*: Quick emergency check (3 red-flag questions).
4. **📝 Review Answers (`views/review.py`)**: Review all entered data with inline `Edit` links that navigate directly back to the relevant step.
5. **🧪 Possible Conditions (`views/conditions.py`)**: Accordion list of differential possibilities with likelihood concordance bars, matching evidence, and unconfirmed signs.
6. **⚖️ Care Guidance (`views/care_guidance.py`)**: Highlights the recommended 4-tier care outcome, rationale, and bulleted next-step instructions.
7. **📊 Decision Support (`views/decision_support.py`)**: Plain-language comparison, severity/urgency badges, and supporting vs unconfirmed criteria matrix.
8. **📄 Final Summary (`views/summary.py`)**: Complete assessment report with clear options to `End assessment` or `Start new assessment`.
9. **🛡️ Safety & Disclaimer (`views/safety.py`)**: Core clinical limitations, emergency warnings, and educational boundaries.

---

## 🚀 How to Run

Execute using the virtual environment:

```powershell
D:\Diagnovet\venv\Scripts\python.exe -m streamlit run D:\Diagnovet\app.py
```

Then navigate to **http://localhost:8501** (or port 8504 if running headless).

---

## 🧪 Automated Testing

Diagnovet includes automated test coverage for startup, validation, navigation locks, dynamic follow-ups, answer preservation, and emergency triage:

```powershell
D:\Diagnovet\venv\Scripts\python.exe -m pytest -v
```

To run with coverage reporting:

```powershell
D:\Diagnovet\venv\Scripts\python.exe -m pytest --cov=components --cov=services --cov=data --cov=views
```
