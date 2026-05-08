# Fishy

A minimal, opinionated scaffolding for starting a new Pygame project. Drop this folder somewhere, rename it, and start writing gameplay — the boring boot, input, fullscreen, and CRT post-processing plumbing is already wired up.

## Status

Scaffolding only. There is no gameplay yet. Running `python main.py` opens a window with a dark background and a CRT overlay; that is the entire experience until you add code.

## What you get out of the box

- A `GameManager` coordinator with the canonical frame loop (`_process_events` → `_update_world` → `_render_frame` → flip).
- Keyboard + controller event routing stubs (`_handle_keydown`, `_handle_joybuttondown`, `_handle_joyhatmotion`, `_handle_joyaxismotion`).
- Cached joystick list and a `START + SELECT + L1 + R1` quit chord.
- `F11` and the controller `BACK` button toggle fullscreen.
- A reusable `CRT` overlay (scanlines + flicker) loaded from `assets/graphics/effects/tv.png`.
- A `settings.py` skeleton with `ScreenSettings`, `ColorSettings`, `InputSettings`, `FontSettings`, `AudioSettings`, `AssetPaths`, and `DebugSettings`.
- The retro `Pixeled.ttf` font in `assets/font/`.
- Empty `core/`, `systems/`, `ui/`, and `utils/` folders ready for your modules.
- A docs scaffold under [docs/](docs/) plus [.github/copilot-instructions.md](.github/copilot-instructions.md).

## Requirements

- Python 3.10+
- `pygame` 2.5+

A `requirements.txt` is intentionally not included — pin your own once you know what you actually depend on.

## Run

```powershell
cd pygame-template-files
python main.py
```

## Controls (defaults)

| Action            | Keyboard | Controller            |
| ----------------- | -------- | --------------------- |
| Toggle fullscreen | `F11`    | `BACK`                |
| Quit              | `Esc`    | `START+SELECT+L1+R1`  |

## How to use this template

```
>>>>>>>>>>  FIRST-RUN SETUP — DELETE THIS BLOCK AFTERWARDS  <<<<<<<<<<
```

When you copy this folder into a new project, do this once and then **delete this entire "How to use this template" section** so the README describes only the real game:

1. Rename the folder to your project name.
2. Update the project name in:
   - The top heading of this `README.md` (and rewrite the body to describe the real game).
   - `ScreenSettings.TITLE` in [settings.py](settings.py).
   - The header in [docs/CHANGELOG.md](docs/CHANGELOG.md) (replace `<RENAME ME — your project name>`).
   - The header in [.github/copilot-instructions.md](.github/copilot-instructions.md).
3. Walk through the ["First-run checklist"](docs/TODO.md) in `docs/TODO.md` and check the items off as you go. Delete that checklist once it's all done.
4. Decide whether you want a `requirements.txt` and add one if so (`pygame>=2.5` is a sensible baseline).
5. `git init` if not already done.
6. Start adding modules under `core/`, `systems/`, `ui/`, `utils/`. Wire them through `GameManager`. Append a CHANGELOG entry for every meaningful change from day one.

```
>>>>>>>>>>  END OF FIRST-RUN SETUP BLOCK  <<<<<<<<<<
```

## Documentation

- [README.md](README.md) — this file.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — how the scaffold fits together.
- [docs/TODO.md](docs/TODO.md) — first-run checklist + suggested first features.
- [docs/TESTING.md](docs/TESTING.md) — manual smoke checks.
- [docs/CHANGELOG.md](docs/CHANGELOG.md) — append-only history.
- [.github/copilot-instructions.md](.github/copilot-instructions.md) — rules for human or AI editors.

## Asset credits

- `assets/font/Pixeled.ttf` — *Pixeled* by OmegaPC777 (free for personal & commercial use).
- `assets/graphics/effects/tv.png` — CRT overlay reused from the arcade cabinet asset set.
