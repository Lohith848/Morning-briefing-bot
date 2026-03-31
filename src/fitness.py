"""
fitness.py — Daily fitness & wellness tip.
No API needed — rotates from a curated list based on day-of-year.
"""

from datetime import date


TIPS = [
    ("💧 Drink a full glass of water right now — your body is 10% dehydrated after sleep.", "Hydration"),
    ("🧘 5 minutes of deep breathing reduces cortisol. Try box breathing: 4-4-4-4.", "Mindfulness"),
    ("🚶 A 10-minute walk after breakfast improves blood sugar control by up to 30%.", "Movement"),
    ("🥗 Include a protein source in breakfast — it keeps you full 3x longer.", "Nutrition"),
    ("📵 First 30 min after waking: no phone. Let your brain wake up naturally.", "Digital Wellness"),
    ("🦵 Do 20 squats before your first tea/coffee — activate those muscles!", "Strength"),
    ("😴 Sleep consistency (same wake time daily) matters more than sleep duration.", "Sleep"),
    ("🧠 Write 3 things you're grateful for — rewires your brain for positivity in 21 days.", "Mental Health"),
    ("🍎 Eat the rainbow — try to include 3 different coloured vegetables today.", "Nutrition"),
    ("🏋️ Progressive overload: add 1 rep or 1 kg to one exercise this week.", "Strength"),
    ("🕯️ 10 min of sunlight exposure in morning regulates your circadian rhythm.", "Wellness"),
    ("🥜 Nuts are a perfect mid-day snack — 20g keeps energy stable without a crash.", "Nutrition"),
    ("🚴 20 mins of cardio, 3x a week, is clinically proven to reduce anxiety.", "Cardio"),
    ("📖 Reading for 6 minutes reduces stress by 68% — more effective than a walk.", "Mindfulness"),
    ("🧂 Most Indians consume 2x the recommended salt. Choose flavour over sodium today.", "Nutrition"),
    ("💪 Push-up challenge: do max push-ups now. Note it. Beat it next week.", "Strength"),
    ("⏸️ Every 45 min of sitting: stand and stretch for 2 min — prevents back pain.", "Posture"),
    ("🍵 Green tea has L-theanine + caffeine — a smoother focus boost than coffee.", "Energy"),
    ("🫁 Nasal breathing during exercise improves stamina and oxygen uptake.", "Breathing"),
    ("🧴 Apply sunscreen even indoors — UV rays pass through glass windows.", "Skin Health"),
    ("🏊 Swimming engages 100% of muscle groups. Even 15 min is excellent.", "Full-Body"),
    ("🛌 Cold room (18–20°C) improves deep sleep quality significantly.", "Sleep"),
    ("🤸 Dynamic stretching before workouts, static stretching after — not before.", "Flexibility"),
    ("🥚 Eggs have all 9 essential amino acids — one of the most complete foods.", "Nutrition"),
    ("🏃 Run/walk in conversation pace — if you can't speak a sentence, slow down.", "Cardio"),
    ("📐 Good posture tip: shoulders back, chin tucked, core slightly engaged.", "Posture"),
    ("🧃 Fruit juice ≠ fruit. Whole fruit has fibre that slows sugar absorption.", "Nutrition"),
    ("💤 Power nap sweet spot: 10–20 min. Longer = sleep inertia and grogginess.", "Sleep"),
    ("🤲 Wash hands before meals — reduces illness risk by 35% per WHO data.", "Hygiene"),
    ("🎵 Upbeat music during workouts increases performance output by ~15%.", "Motivation"),
]


def get_fitness_tip() -> str:
    """Returns today's fitness tip based on day-of-year (deterministic rotation)."""
    day_index = date.today().timetuple().tm_yday % len(TIPS)
    tip, category = TIPS[day_index]
    return f"🏋️ *Wellness Tip* _{category}_\n  {tip}"
