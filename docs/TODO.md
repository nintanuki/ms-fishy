# Pygame Template — Roadmap & TODO

This file is the new-project starter checklist. **When you copy the template into a real project, walk through the items below, then replace the entire file with your real game's roadmap.**

---

## First-run checklist (every new project)

- [ ] Rename the folder.
- [ ] Update `ScreenSettings.TITLE` in [settings.py](../settings.py).
- [ ] Update the header of [docs/CHANGELOG.md](CHANGELOG.md) (replace `<RENAME ME — your project name>`).
- [ ] Update the header of [.github/copilot-instructions.md](../.github/copilot-instructions.md).
- [ ] Rewrite [README.md](../README.md) for the actual game (status, requirements, controls). Delete the "How to use this template" block from the README once you're done with it.
- [ ] Decide whether you want a `requirements.txt` and add one if so (`pygame>=2.5` is a sensible baseline).
- [ ] Initialize git (`git init`) if not already done.
- [ ] Delete this `## First-run checklist` section once every item is checked.

## Suggested first features

- [ ] Add a scene/state machine (title screen → playing → game over).
- [ ] Add an audio bootstrap helper that respects `AudioSettings.MUTE` / `MUTE_MUSIC`.
- [ ] Add a high-score persistence helper (JSON file next to `main.py`).
- [ ] Add a pause overlay (Start button / `P`).

## Code-health items inherited from this template

- [x] [crt.py](../crt.py) used `from settings import *`. Now uses explicit imports.
- [x] `AudioSettings.MUTE` / `DebugSettings.MUTE` were duplicated. Kept `AudioSettings.MUTE`; removed the duplicate.
- [x] `AssetPaths.TV` was a cwd-relative path. Now `__file__`-relative, like `FontSettings.FONT`.
- [x] `GameManager.__init__` carried an unused `self.game_active`. Removed.
- [x] `GameManager.__init__` and `reset_game` docstrings referenced dungeon levels (copy-paste from a prior project). Generalized.
- [x] `pygame.display.set_mode((ScreenSettings.RESOLUTION), pygame.SCALED)` had redundant parens. Removed.
- [x] Empty `core/`, `systems/`, `ui/`, and `utils/` folders now have `__init__.py` files so git tracks them.
- [x] `Esc` is now wired in `_handle_keydown` so the template runs without a controller for testing.

---

## Documentation maintenance

Every pass that meaningfully changes a system must:

1. Update [docs/ARCHITECTURE.md](ARCHITECTURE.md).
2. Append entries to [docs/CHANGELOG.md](CHANGELOG.md).
3. Move completed items here from `[ ]` to `[x]` (do not delete).
