# Diagnovet — Smart Pet Health Diagnosis & Decision Support System

> **Academic Expert System & Clinical Decision Support Portal**  
> Developed for **IAI CCP** &bull; **Complete Frontend Architecture & UI Refinement**

Diagnovet is an intelligent, web-based veterinary decision-support application designed to assist dog and cat guardians in evaluating clinical symptoms early, understanding possible disease concordance, and receiving structured next-step veterinary recommendations.

---

## 🎨 Design System: "Lagoon" & "Aurora" Themes

Directly aligned with `diagnovet.html`:
- **Lagoon (Default Light Theme)**:
  - Background: `#E8FAF6` (Refreshing Mint)
  - Card & Surfaces: `#FFFFFF`
  - Text & Muted: `#0B2F3A` and `#5C8089`
  - Border & Dividers: `#CBEBE4`
  - Primary Accent: `#2E7DFF`
  - Primary Gradient: `linear-gradient(135deg, #00C9A7, #2E7DFF 55%, #8A5CFF)`
  - Glow: `0 8px 26px rgba(46, 125, 255, 0.25)`
- **Aurora (Optional Dark Theme)**:
  - Background: `#0F0B24` (Deep Night Purple)
  - Card & Surfaces: `#1A1438`
  - Text & Muted: `#F2EEFF` and `#A59CC9`
  - Border: `#2D2557`
  - Accent: `#7B5CFF`
  - Gradient: `linear-gradient(135deg, #00E5C3, #7B5CFF 55%, #FF5FA2)`
  - Glow: `0 8px 30px rgba(123, 92, 255, 0.33)`
- **4 Decision Outcomes**:
  - 🚨 **Get Help Now (Critical)**: `#E5484D`
  - 🏥 **Visit Vet Today (High)**: `#E69B28`
  - 📅 **Book a Vet Visit (Medium)**: `#2E7DFF` (Lagoon) / `#7B5CFF` (Aurora)
  - 🏡 **Home Care & Monitor (Low)**: `#27966F`

---

## 🧭 Multi-View Application Structure

Diagnovet provides 10 interconnected pages with persistent navigation, back navigation, and session state:

1. **🏠 Home Dashboard (`views/home.py`)**: Landing portal matching `diagnovet.html` with hero banner, species triage cards, 4-step workflow, 9 health categories grid, feature cards, and emergency warnings.
2. **🐶 Pet Profile (`views/pet_profile.py`)**: Pet registration and profile cards for Luna, Max, and Bella with zero HTML leaking and instant active patient switching.
3. **🩺 Start Consultation (`views/consultation.py`)**: 5-step guided consultation workflow with 5-segment stepper, interactive `Yes / No / Not Sure` segmented controls, conditional follow-ups, and review summary.
4. **📋 Symptom Assessment (`views/symptom_assessment.py`)**: Clinical duration, severity sliders, risk factors, and interactive emergency triage screening.
5. **🧪 Diagnosis Results (`views/diagnosis_results.py`)**: Differential condition concordance matching with Plotly likelihood charts, progress bars, and supporting/missing evidence breakdown.
6. **⚖️ Decision Making (`views/decision_making.py`)**: Academic explanation facility detailing why an action was chosen, fired rules, risk factors, and excluded alternative outcomes.
7. **📊 Decision Support System (`views/decision_support.py`)**: Comparative evidence matrix table, MCDA Plotly chart, and synthesis methodology.
8. **🕘 Consultation History (`views/consultation_history.py`)**: Searchable and filterable consultation log by pet and health category.
9. **ℹ️ About Diagnovet (`views/about.py`)**: Academic project objectives, system architecture, methodology, and ethical boundaries.
10. **🛡️ Safety & Disclaimer (`views/safety.py`)**: Clinical boundaries, red-flag emergency symptoms, and user agreement terms.

---

## 🚀 How to Run

Launch the application using the D-drive Python virtual environment:

```powershell
$env:TEMP='D:\Diagnovet\temp'; $env:TMP='D:\Diagnovet\temp'; $env:PIP_CACHE_DIR='D:\Diagnovet\pip-cache'
D:\Diagnovet\venv\Scripts\python.exe -m streamlit run D:\Diagnovet\app.py
```

Open your browser at **http://localhost:8501**.

---

## 🧪 Testing and Quality Assurance

Run the automated consistency audit and unit test suite:

```powershell
D:\Diagnovet\venv\Scripts\python.exe -m pytest tests/test_frontend.py -v
```

This verifies:
- All 10 views call the shared header and footer.
- Zero hardcoded hex colors exist in `views/*.py`.
- All 4 decision outcomes correctly map to theme tokens and CSS classes.
- Required demo labels are present on Results, Decision Making, and DSS pages.
- Zero unwanted prototype labels exist.
- Safe HTML rendering prevents markdown `<pre><code>` block leakage.
