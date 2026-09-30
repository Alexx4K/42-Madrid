# Unlike light_spellbook.py, this import stays at the top of the
# file on purpose: dark_spellbook and dark_validator import each
# other at module level, which is exactly what creates the circular
# dependency curse (see ft_kaboom_1.py).
from .dark_validator import validate_ingredients


def dark_spell_allowed_ingredients() -> list[str]:
    return ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    result = validate_ingredients(ingredients)
    if "VALID" in result:
        return f"Spell recorded: {spell_name} ({result})"
    return f"Spell rejected: {spell_name} ({result})"
