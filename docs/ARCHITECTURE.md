# Pygame Template — Architecture

> **Maintenance rule:** every pass that meaningfully changes a system must update this document.

## 1. The shape of the program

```
                   +-------------------+
                   |     main.py       |
                   |   GameManager     |   (coordinator)
                   +---+-----+-----+---+
                       |     |     |
        +--------------+     |     +-------------+
        v                    v                   v
     events             world / state           render
   (keyboard,           (your gameplay         (screen fill
    joystick)             goes here)            + CRT pass)
```

`GameManager` owns the screen, the clock, the cached joystick list, and the fullscreen flag. Everything else — gameplay, UI, animations, audio, persistence — should live in modules under `core/`, `systems/`, `ui/`, or `utils/` and be coordinated through `GameManager`.

## 2. Frame loop

`GameManager.run()` per frame:

1. `quit_combo_pressed()` — early-exit on the held quit chord.
2. `_process_events()` — drain pygame's event queue and dispatch to the typed handlers.
3. `_update_world()` — game logic (currently a no-op stub).
4. `_render_frame()` — `screen.fill(BG_COLOR)` then the CRT overlay (windowed only).
5. `pygame.display.flip()` and `clock.tick(FPS)`.

## 3. Input

Events are routed by type:

- `KEYDOWN` → `_handle_keydown`. Default: `Esc` quits, `F11` toggles fullscreen.
- `JOYBUTTONDOWN` → `_handle_joybuttondown`. Default: quit-chord check + `BACK` toggles fullscreen.
- `JOYHATMOTION` → `_handle_joyhatmotion` (stub).
- `JOYAXISMOTION` → `_handle_joyaxismotion` (stub).

The joystick list is cached once at startup via `setup_controllers()`. Hot-plug requires re-running that method or re-init.

The quit chord is defined as the tuple `InputSettings.JOY_BUTTON_QUIT_COMBO`. When **all** of those buttons are held on **any** connected controller, the game closes.

## 4. CRT overlay

[crt.py](../crt.py) loads `AssetPaths.TV`, scales it to the screen, and on each `draw()` blits a fresh copy with a randomized alpha and per-row scanlines. `GameManager._render_frame` calls it only when not in fullscreen so it does not double-up on a real CRT cabinet.

## 5. Settings

[settings.py](../settings.py) is the single source of truth for tunables.

| Class            | Purpose                                                             |
| ---------------- | ------------------------------------------------------------------- |
| `ColorSettings`  | Named colors + semantic aliases (`BG_COLOR`, `OVERLAY_BACKGROUND`). |
| `ScreenSettings` | Resolution, FPS, title, CRT alpha range and scanline height.        |
| `InputSettings`  | Controller button/axis indices + quit combo + analog threshold.     |
| `FontSettings`   | Font file paths.                                                    |
| `AudioSettings`  | Mute toggles + music volume.                                        |
| `AssetPaths`     | Asset file paths for non-font assets.                               |
| `DebugSettings`  | Debug-only toggles.                                                 |

**No magic numbers anywhere outside this file.**

## 6. Source tree

```
assets/
  font/Pixeled.ttf              Pixel font for retro UI text.
  graphics/effects/tv.png       CRT overlay texture.
core/                           (empty) Place state-machine / data classes here.
systems/                        (empty) Place gameplay systems here.
ui/                             (empty) Place screens / HUD widgets here.
utils/                          (empty) Place pure helpers here.
crt.py                          CRT post-processing overlay.
main.py                         Entry point + GameManager.
settings.py                     All tunables.
docs/                           ARCHITECTURE, TODO, TESTING, CHANGELOG.
.github/copilot-instructions.md Editor rules.
```

## 7. Extension points

When you add gameplay, the recommended seams are:

- Replace the `_update_world` stub with a call into your game-state object.
- Replace the `_render_frame` body's `screen.fill` with calls into your render pipeline (and keep the CRT pass as the *last* step before `flip`).
- Add new event-type handlers in `_process_events` if you need (e.g. `MOUSEBUTTONDOWN`).
- Add scene/state switching by giving `GameManager` a current-scene attribute and forwarding `_handle_*` / `_update_world` / `_render_frame` to it.
