# Only a small, curated part of the laboratory is exposed here.
# create_earth is left out on purpose: alchemy.create_earth() must
# raise an AttributeError (see ft_alembic_4.py). heal is a friendly
# package-level alias for healing_potion (see ft_distillation_1.py).
from .elements import create_air
from .potions import healing_potion as heal
from .potions import strength_potion
from .transmutation import lead_to_gold

__all__ = ["create_air", "heal", "strength_potion", "lead_to_gold"]
