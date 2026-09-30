from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed = dark_spell_allowed_ingredients()
    lowered = ingredients.lower()
    for ingredient in allowed:
        if ingredient in lowered:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
