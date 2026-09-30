# Only the light magic spells are exposed at package level: the dark
# ones must be reached by importing dark_spellbook.py directly (see
# ft_kaboom_1.py), otherwise every import of this package would
# trigger the circular dependency explosion.
from .light_spellbook import light_spell_allowed_ingredients
from .light_spellbook import light_spell_record

__all__ = ["light_spell_allowed_ingredients", "light_spell_record"]
