print("=== Kaboom 1 ===")
print("Access to alchemy/grimoire/dark_spellbook.py directly")
print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")

# dark_spellbook.py and dark_validator.py import each other at
# module level, so this import never completes: it is expected to
# blow up with an ImportError (partially initialized module).
from alchemy.grimoire.dark_spellbook import (  # noqa: E402,F401
    dark_spell_record,
)
