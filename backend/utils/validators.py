"""Validation utilities for Diagnovet backend."""
from typing import Dict, Any, Tuple, List, Optional

VALID_SPECIES = {"Dog", "Cat"}
VALID_GENDERS = {"Male", "Female"}


def validate_pet_data(
    species: str,
    breed: str,
    gender: str,
    age_str: str,
    weight_str: Optional[str] = None
) -> Tuple[bool, Dict[str, str]]:
    """Validate pet demographic details. Returns (is_valid, error_dict)."""
    errors: Dict[str, str] = {}

    if not species or species not in VALID_SPECIES:
        errors["sp"] = "Please choose Dog or Cat."

    if not breed or breed.strip() in ("", "Choose a breed", "Choose species first"):
        errors["breed"] = "Please choose a breed."

    if not gender or gender not in VALID_GENDERS:
        errors["gen"] = "Please choose a gender."

    if age_str is None or str(age_str).strip() == "":
        errors["age"] = "Enter an age from 0 to 30."
    else:
        try:
            val_age = float(str(age_str).strip())
            if val_age < 0 or val_age > 30:
                errors["age"] = "Enter an age from 0 to 30."
        except ValueError:
            errors["age"] = "Enter an age from 0 to 30."

    if weight_str is not None and str(weight_str).strip() != "":
        try:
            val_wt = float(str(weight_str).strip())
            if val_wt < 0.5 or val_wt > 90:
                errors["wt"] = "Enter a weight from 0.5 to 90 kg."
        except ValueError:
            errors["wt"] = "Enter a weight from 0.5 to 90 kg."

    return len(errors) == 0, errors


def validate_symptoms_selection(symptoms: List[str]) -> Tuple[bool, str]:
    """Validate that at least one clinical sign was selected."""
    if not symptoms:
        return False, "Choose at least one sign to continue."
    return True, ""


def validate_duration_severity_frequency(
    duration: str, severity: str, frequency: str
) -> Tuple[bool, str]:
    """Validate step 4 parameters."""
    if not (duration and severity and frequency):
        return False, "Please choose duration, severity and frequency."
    return True, ""
