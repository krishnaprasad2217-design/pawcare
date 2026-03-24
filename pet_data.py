from datetime import datetime, date
from dateutil.relativedelta import relativedelta

PET_DATABASE = {
    "dog": {
        "default": {
            "vaccinations": [
                {"name": "Distemper + Parvovirus (DHPPi)", "age_weeks": 6, "repeat_years": 1},
                {"name": "Rabies", "age_weeks": 12, "repeat_years": 1},
                {"name": "Bordetella (Kennel Cough)", "age_weeks": 8, "repeat_years": 1},
                {"name": "Leptospirosis", "age_weeks": 12, "repeat_years": 1},
                {"name": "Canine Influenza", "age_weeks": 16, "repeat_years": 1},
            ],
            "lifespan_years": 12,
            "feeding": {
                "puppy": {"meals_per_day": 4, "types": ["Puppy kibble", "Soft wet food", "Rice + boiled chicken"], "avoid": ["Onions", "Grapes", "Chocolate", "Xylitol", "Avocado"]},
                "adult": {"meals_per_day": 2, "types": ["Dry kibble", "Wet food", "Raw diet (BARF)", "Cooked rice + meat"], "avoid": ["Onions", "Grapes", "Chocolate", "Caffeine", "Macadamia nuts"]},
                "senior": {"meals_per_day": 2, "types": ["Senior formula kibble", "Wet food", "Joint-support diet", "Low-sodium options"], "avoid": ["Salty snacks", "Raw meat (immune risk)", "High-fat foods"]}
            },
            "care_tips": [
                "Brush teeth 2-3 times per week",
                "Trim nails every 3-4 weeks",
                "Bathe every 4-6 weeks",
                "Daily exercise: 30-60 minutes",
                "Annual vet check-up",
                "Monthly flea & tick prevention",
                "Deworming every 3 months"
            ]
        },
        "golden retriever": {
            "vaccinations": [
                {"name": "DHPPi (Core Vaccine)", "age_weeks": 6, "repeat_years": 1},
                {"name": "Rabies", "age_weeks": 12, "repeat_years": 1},
                {"name": "Leptospirosis", "age_weeks": 9, "repeat_years": 1},
                {"name": "Bordetella", "age_weeks": 8, "repeat_years": 1},
                {"name": "Canine Influenza H3N2", "age_weeks": 16, "repeat_years": 1},
                {"name": "Lyme Disease", "age_weeks": 12, "repeat_years": 1},
            ],
            "lifespan_years": 12,
            "feeding": {
                "puppy": {"meals_per_day": 3, "types": ["Large-breed puppy food", "Fish-based kibble", "Boiled chicken + veg"], "avoid": ["Onions", "Grapes", "Chocolate", "Xylitol"]},
                "adult": {"meals_per_day": 2, "types": ["Salmon & sweet potato kibble", "Wet food", "Raw meaty bones"], "avoid": ["Onions", "Grapes", "Salty food", "Chocolate"]},
                "senior": {"meals_per_day": 2, "types": ["Senior low-calorie formula", "Joint-support diet", "Omega-3 rich food"], "avoid": ["High-fat food", "Excess treats", "Raw fish"]}
            },
            "care_tips": [
                "Brush coat daily — prone to shedding",
                "Check ears weekly for infection",
                "Hip dysplasia check annually",
                "Swim-friendly exercise recommended",
                "Regular dental care essential",
                "Cancer screening from age 6+",
                "Monthly flea/tick/heartworm prevention"
            ]
        },
        "labrador retriever": {
            "vaccinations": [
                {"name": "DHPPi", "age_weeks": 6, "repeat_years": 1},
                {"name": "Rabies", "age_weeks": 12, "repeat_years": 1},
                {"name": "Leptospirosis", "age_weeks": 9, "repeat_years": 1},
                {"name": "Bordetella", "age_weeks": 8, "repeat_years": 1},
            ],
            "lifespan_years": 12,
            "feeding": {
                "puppy": {"meals_per_day": 3, "types": ["Large-breed puppy kibble", "Measured portions (labs overeat!)"], "avoid": ["Table scraps", "Fatty foods", "Grapes", "Chocolate"]},
                "adult": {"meals_per_day": 2, "types": ["Weight-control kibble", "Lean proteins", "Vegetables as treats"], "avoid": ["High-calorie treats", "Salty snacks", "Onions"]},
                "senior": {"meals_per_day": 2, "types": ["Senior weight management food", "Joint-care formula"], "avoid": ["Excess calories", "High-sodium food"]}
            },
            "care_tips": [
                "Monitor weight closely — prone to obesity",
                "Daily vigorous exercise (60+ min)",
                "Brush weekly",
                "Check ears monthly",
                "Elbow & hip dysplasia screening",
                "Monthly heartworm prevention"
            ]
        },
        "german shepherd": {
            "vaccinations": [
                {"name": "DHPPi", "age_weeks": 6, "repeat_years": 1},
                {"name": "Rabies", "age_weeks": 12, "repeat_years": 1},
                {"name": "Leptospirosis", "age_weeks": 9, "repeat_years": 1},
                {"name": "Bordetella", "age_weeks": 8, "repeat_years": 1},
                {"name": "Canine Influenza", "age_weeks": 16, "repeat_years": 1},
            ],
            "lifespan_years": 11,
            "feeding": {
                "puppy": {"meals_per_day": 3, "types": ["High-protein puppy food", "Chicken & rice", "Omega-3 supplements"], "avoid": ["Grains (some are sensitive)", "Chocolate", "Onions"]},
                "adult": {"meals_per_day": 2, "types": ["High-protein kibble", "Raw diet", "Lean meats + veggies"], "avoid": ["Bloat-risk: no exercise after big meals", "Grapes", "Onions"]},
                "senior": {"meals_per_day": 2, "types": ["Senior formula", "Joint-support food", "Easy-digest kibble"], "avoid": ["High-fat food", "Large single meals"]}
            },
            "care_tips": [
                "Brush 3-4 times per week",
                "Mental stimulation daily (training/puzzles)",
                "Hip dysplasia screening",
                "Watch for bloat — smaller meals",
                "Exercise 2 hours per day",
                "Socialization from puppyhood"
            ]
        },
        "pomeranian": {
            "vaccinations": [
                {"name": "Distemper + Parvovirus (DHPPi)", "age_weeks": 6, "repeat_years": 1},
                {"name": "Rabies", "age_weeks": 12, "repeat_years": 1},
                {"name": "Bordetella (Kennel Cough)", "age_weeks": 8, "repeat_years": 1},
                {"name": "Leptospirosis", "age_weeks": 12, "repeat_years": 1},
                {"name": "Canine Influenza", "age_weeks": 16, "repeat_years": 1},
            ],
            "lifespan_years": 14,
            "feeding": {
                "puppy": {"meals_per_day": 4, "types": ["Small-breed puppy kibble", "Soft wet food"], "avoid": ["Onions", "Grapes", "Chocolate", "Xylitol"]},
                "adult": {"meals_per_day": 3, "types": ["Small-breed adult kibble", "Wet food", "Boiled chicken + rice"], "avoid": ["Onions", "Grapes", "Chocolate", "Salty snacks"]},
                "senior": {"meals_per_day": 3, "types": ["Senior small-breed formula", "Wet food", "Joint-support diet"], "avoid": ["High-fat food", "Excess treats"]}
            },
            "care_tips": [
                "Brush coat daily — dense double coat",
                "Trim nails every 3-4 weeks",
                "Dental care essential — prone to dental disease",
                "Exercise 20-30 min daily",
                "Annual vet check-up",
                "Monthly flea prevention",
                "Watch for tracheal collapse — use harness not collar"
            ]
        }
    },
    "cat": {
        "default": {
            "vaccinations": [
                {"name": "FVRCP (Feline 3-in-1)", "age_weeks": 6, "repeat_years": 1},
                {"name": "Rabies", "age_weeks": 12, "repeat_years": 1},
                {"name": "Feline Leukemia (FeLV)", "age_weeks": 8, "repeat_years": 1},
                {"name": "Feline Immunodeficiency (FIV)", "age_weeks": 9, "repeat_years": 1},
            ],
            "lifespan_years": 15,
            "feeding": {
                "kitten": {"meals_per_day": 4, "types": ["Kitten wet food", "Kitten kibble", "High-protein food"], "avoid": ["Cow milk", "Onions", "Garlic", "Chocolate", "Grapes"]},
                "adult": {"meals_per_day": 2, "types": ["Wet food (hydration)", "Dry kibble", "Raw diet"], "avoid": ["Onions", "Garlic", "Alcohol", "Caffeine", "Dog food"]},
                "senior": {"meals_per_day": 3, "types": ["Senior wet food", "Kidney-support diet", "Easy-digest formula"], "avoid": ["High-phosphorus food", "Excess dry food"]}
            },
            "care_tips": [
                "Annual vet visit + dental check",
                "Litter box cleaned daily",
                "Brush coat 2-3 times per week",
                "Trim nails every 2 weeks",
                "Provide scratching posts",
                "Monthly flea prevention",
                "Keep indoors for longer life"
            ]
        },
        "persian": {
            "vaccinations": [
                {"name": "FVRCP", "age_weeks": 6, "repeat_years": 1},
                {"name": "Rabies", "age_weeks": 12, "repeat_years": 1},
                {"name": "Feline Leukemia", "age_weeks": 8, "repeat_years": 1},
            ],
            "lifespan_years": 14,
            "feeding": {
                "kitten": {"meals_per_day": 4, "types": ["Flat-face friendly kibble", "Wet food", "High-protein kitten food"], "avoid": ["Cow milk", "Chocolate", "Onions"]},
                "adult": {"meals_per_day": 2, "types": ["Flat-face formula kibble", "Premium wet food", "Hairball control food"], "avoid": ["Onions", "Garlic", "Raw fish (regularly)"]},
                "senior": {"meals_per_day": 3, "types": ["Senior persian formula", "Hairball remedy food"], "avoid": ["High-phosphorus food"]}
            },
            "care_tips": [
                "Daily coat brushing — mats quickly",
                "Clean face folds daily",
                "Check eyes daily for discharge",
                "Regular dental care (prone to issues)",
                "Keep indoors only",
                "Polycystic kidney disease screening",
                "Monthly flea treatment"
            ]
        }
    },
    "rabbit": {
        "default": {
            "vaccinations": [
                {"name": "Myxomatosis", "age_weeks": 5, "repeat_years": 1},
                {"name": "RVHD1 (Rabbit Viral Haemorrhagic)", "age_weeks": 5, "repeat_years": 1},
                {"name": "RVHD2", "age_weeks": 10, "repeat_years": 1},
            ],
            "lifespan_years": 9,
            "feeding": {
                "young": {"meals_per_day": 3, "types": ["Unlimited hay (80%)", "Fresh leafy greens", "Pellets (small portion)"], "avoid": ["Iceberg lettuce", "Fruit (excess)", "Beans", "Potatoes"]},
                "adult": {"meals_per_day": 2, "types": ["Timothy hay (constant)", "Dark leafy greens", "Limited pellets"], "avoid": ["Sugary treats", "Bread", "Nuts", "Potatoes"]},
                "senior": {"meals_per_day": 2, "types": ["Soft hay", "Easy-digest greens", "Fresh water always"], "avoid": ["High-calcium greens", "Excess pellets"]}
            },
            "care_tips": [
                "Spay/neuter strongly recommended",
                "Hay must be available 24/7",
                "Daily exercise outside cage",
                "Brush 2-3 times per week",
                "Check teeth monthly",
                "GI stasis is emergency — watch eating",
                "Never pick up by ears"
            ]
        }
    }
}

def calculate_age(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        today = date.today()
        delta = relativedelta(today, dob)
        years = delta.years
        months = delta.months
        if years == 0:
            return f"{months} month{'s' if months != 1 else ''}", months / 12, dob
        return f"{years} year{'s' if years != 1 else ''} {months} month{'s' if months != 1 else ''}", years + months/12, dob
    except:
        return "Unknown", 0, None

def get_life_stage(pet_type, age_years):
    if pet_type == "dog":
        if age_years < 1: return "puppy"
        if age_years < 7: return "adult"
        return "senior"
    elif pet_type == "cat":
        if age_years < 1: return "kitten"
        if age_years < 10: return "adult"
        return "senior"
    elif pet_type == "rabbit":
        if age_years < 1: return "young"
        if age_years < 5: return "adult"
        return "senior"
    return "adult"

def get_full_vaccination_schedule(vaccinations, dob, lifespan_years=12):
    """
    Generate the COMPLETE vaccination schedule from birth to lifespan,
    one entry per year per vaccine.
    Each entry has: id (unique), name, year_label, due_date, status
    status: 'past' (before today), 'current' (this year), 'upcoming' (future)
    """
    if not dob:
        return []

    today = date.today()
    current_year = today.year
    schedule = []

    for v in vaccinations:
        first_due = dob + relativedelta(weeks=v["age_weeks"])
        repeat = v.get("repeat_years", 1)

        # Generate all doses from first_due until lifespan ends
        dose_num = 0
        due = first_due
        while True:
            pet_age_at_dose_years = (due - dob).days / 365.25
            if pet_age_at_dose_years > lifespan_years + 1:
                break

            if dose_num == 0:
                year_label = "Puppy / First Dose"
            else:
                year_label = f"Year {dose_num}"

            if due > today:
                status = "upcoming"
            elif due.year == current_year:
                status = "current"
            else:
                status = "past"

            # Days until/since due
            days_diff = (due - today).days

            schedule.append({
                "id": f"{v['name']}__dose{dose_num}",
                "name": v["name"],
                "dose_num": dose_num,
                "year_label": year_label,
                "due_date": due.strftime("%d %b %Y"),
                "due_date_iso": due.strftime("%Y-%m-%d"),
                "status": status,
                "days_diff": days_diff,
                "pet_age_at_dose": f"{int(pet_age_at_dose_years)} yr" if pet_age_at_dose_years >= 1 else f"{int(pet_age_at_dose_years*52)} wk"
            })

            dose_num += 1
            due = first_due + relativedelta(years=dose_num * repeat)

    # Sort by due date
    schedule.sort(key=lambda x: x["due_date_iso"])

    # Keep: all past/current doses + next 2 upcoming years only
    today = date.today()
    current_year = today.year
    result = []
    upcoming_years_seen = set()
    for item in schedule:
        if item["status"] in ("past", "current"):
            result.append(item)
        else:
            yr = int(item["due_date_iso"][:4])
            upcoming_years_seen.add(yr)
            if len(upcoming_years_seen) <= 2:
                result.append(item)
    return result

def get_pet_info(breed, pet_type, dob_str):
    pt = pet_type.lower() if pet_type else "dog"
    br = breed.lower() if breed else ""
    db = PET_DATABASE.get(pt, PET_DATABASE["dog"])
    pet_data = db.get(br, db.get("default", {}))
    if not pet_data:
        pet_data = db.get("default", {})

    age_str, age_years, dob = calculate_age(dob_str)
    stage = get_life_stage(pt, age_years)
    feeding = pet_data.get("feeding", {}).get(stage, {})
    lifespan = pet_data.get("lifespan_years", 12)
    full_schedule = get_full_vaccination_schedule(
        pet_data.get("vaccinations", []), dob, lifespan
    )

    return {
        "age_display": age_str,
        "age_years": round(age_years, 1),
        "life_stage": stage,
        "lifespan_years": lifespan,
        "vaccinations": full_schedule,
        "feeding": feeding,
        "care_tips": pet_data.get("care_tips", []),
        "pet_type": pt,
        "breed": breed
    }
