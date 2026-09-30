def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    # Imported here, inside the function, instead of at the top of
    # the file: this is what breaks the circular dependency with
    # light_validator, which itself needs the allowed ingredients
    # list defined above.
    from .light_validator import validate_ingredients

    result = validate_ingredients(ingredients)
    if "VALID" in result:
        return f"Spell recorded: {spell_name} ({result})"
    return f"Spell rejected: {spell_name} ({result})"
