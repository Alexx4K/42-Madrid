# The two root elements (fire, water) live outside the alchemy
# package, so we reach them with a plain absolute import. The two
# alchemy elements (earth, air) live right next to us, so a relative
# import is enough.
import elements as root_elements
from .elements import create_air, create_earth


def strength_potion() -> str:
    fire = root_elements.create_fire()
    water = root_elements.create_water()
    return f"Strength potion brewed with '{fire}' and '{water}'"


def healing_potion() -> str:
    earth = create_earth()
    air = create_air()
    return f"Healing potion brewed with '{earth}' and '{air}'"
