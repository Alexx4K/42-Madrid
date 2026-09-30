# Root elements.py lives outside the alchemy package: reach it with
# a plain absolute import. alchemy/elements.py and alchemy/potions.py
# live one level up from here, so a relative import ("..") is enough.
import elements
from ..elements import create_air
from ..potions import strength_potion


def lead_to_gold() -> str:
    air = create_air()
    strength = strength_potion()
    fire = elements.create_fire()
    return (
        f"Recipe transmuting Lead to Gold: brew '{air}' and "
        f"'{strength}' mixed with '{fire}'"
    )
