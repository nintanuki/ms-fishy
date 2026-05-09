# Ms. Fishy — Architecture

> **Maintenance rule:** every pass that meaningfully changes a system must update this document.

## 1. The shape of the program

```
                        +-------------------+
                        |     main.py       |
                        |   GameManager     |   (coordinator)
                        +---+-----+-----+---+
                            |     |     |
           +----------------+     |     +----------------+
           v                      v                      v
        events               world / state             render
      (keyboard,             Player, FishManager      (screen fill
       joystick)             collision loop)           + sprites
                                                       + CRT pass)
```

`GameManager` owns the screen, the clock, the cached joystick list, the fullscreen flag, the `Player` sprite, and the `FishManager`. Everything else — future UI, audio, persistence — should live in modules under `core/`, `systems/`, `ui/`, or `utils/` and be coordinated through `GameManager`.

## 2. Frame loop

`GameManager.run()` per frame:

1. `quit_combo_pressed()` — early-exit on the held quit chord.
2. `_process_events()` — drain pygame's event queue and dispatch to the typed handlers.
3. `_update_world()` — if state is `playing`, advance `all_sprites`, `enemy_sprites`, and `FishManager`.
4. `_render_frame()` — render by state:
  - `playing`: blit pre-rendered `bg_surface` (ocean gradient) + world sprites.
  - `paused`: black background + centered pause text.
  - `game_over`: black background + centered game-over text and restart prompt.
  Then CRT overlay (windowed only).
5. `pygame.display.flip()` and `clock.tick(FPS)`.

`Enter` drives state transitions:

- `playing -> paused` (pause SFX in, music paused)
- `paused -> playing` (pause SFX out, music resumed)
- `game_over -> playing` (session entities recreated, restart)

## 3. Sprites (`core/sprites.py`)

### `Player`

A `pygame.sprite.Sprite` representing the player fish.

- **Appearance:** Gradient polygon fish (yellow dorsal → orange belly, diamond body + triangle tail) with a small black square eye, a soft drop shadow, and a pink bow (two mirrored triangles meeting at a central apex) floating above the body's top point — Ms. Fishy's signature accessory. Built once at init and rebuilt only on `grow()`. Initial size `PlayerSettings.SIZE`.
- **Movement:** Arrow keys and left analog stick. Uses a velocity model: each frame of held input adds `PlayerSettings.ACCELERATION` to the velocity on that axis (capped at `PlayerSettings.MAX_SPEED`). When input is released, `PlayerSettings.DRAG` is multiplied into the velocity each frame until it falls below `PlayerSettings.STOP_THRESHOLD`, giving an underwater coast-and-stop feel. Direction flip waits until velocity exceeds `PlayerSettings.FLIP_THRESHOLD` so the sprite doesn't flicker while drifting to a stop. Sub-pixel accumulators (`_pos_x`, `_pos_y`) prevent fractional velocities from being silently discarded by `int()` truncation each frame.
- **Boundary:** `enforce_boundaries` clamps the rect to the screen edges, zeroes velocity on any clamped axis (so the player doesn't fight the wall), and resyncs the float accumulators to the clamped position.
- **Growth:** `FishManager.grow_player` calls `Player.grow(...)`, which rebuilds the fish polygon/mask at a larger size while preserving center position. `self.size` is stored as `float` so fractional growth (from `PLAYER_GROWTH_COEFFICIENT = 0.10`) accumulates across multiple fish eaten; the surface is always built from `int(self.size)`. Storing it as `int` would silently discard sub-pixel growth on every call.

### `Fish`

A `pygame.sprite.Sprite` representing an enemy fish.

- **Appearance:** Solid-color polygon fish (random color from `ColorSettings.FISH_PALETTE`, chosen at spawn) with a small black square eye of size `FishSettings.EYE_SIZE_RATIO * size` and a soft drop shadow. The palette is a curated set of retro hues chosen to contrast against the ocean gradient background.
- **Spawn:** From off the left or right edge at a random vertical position. Direction is set to match the side it spawned from (left→right, right→left).
- **Movement:** Constant horizontal speed in `[FishSettings.MIN_SPEED, FishSettings.MAX_SPEED]`. Self-destructs (`kill()`) once it clears the opposite edge by 50 px.

## 4. Fish manager (`systems/fish_manager.py`)

`FishManager` holds the `enemy_sprites` group and drives the fish lifecycle each frame:

1. **Spawn timer:** increments each frame; fires `spawn_fish()` every `FishSettings.SPAWN_RATE` frames (≈1 s at 60 FPS) and resets.
2. **Collision:** `check_collisions` calls `pygame.sprite.spritecollide` against the player.
   - Player rect area > fish rect area → `grow_player`, fish is killed.
  - Player rect area ≤ fish rect area → returns `True` to signal game-over to `GameManager`.

`GameManager._update_world` consumes that signal and switches the state to `game_over` (no abrupt process exit).

## 5. Input

**Parity rule:** every action available on the keyboard must also be reachable on the controller. Keep this invariant when adding new input actions.

**Handler design rule:** input handlers (`_handle_enter_key`, `_handle_start_button`, etc.) must never call each other. When two input sources share a behaviour, extract that behaviour into a dedicated action method (e.g. `_handle_pause_action`) and have each handler call the action method directly. This keeps every handler self-contained and prevents one input path from silently inheriting unrelated side-effects of another.

Events are routed by type:

- `KEYDOWN` → `_handle_keydown`. `Esc` quits; `F11` toggles fullscreen; `Enter` → `_handle_enter_key` (pause/resume/restart).
- `JOYBUTTONDOWN` → `_handle_joybuttondown`. Quit-chord check; `BACK` toggles fullscreen; `START` → `_handle_start_button` (pause/resume only).
- `JOYHATMOTION` → `_handle_joyhatmotion` (stub).
- `JOYAXISMOTION` → `_handle_joyaxismotion` (stub).

Both `_handle_enter_key` and `_handle_start_button` delegate to `_handle_pause_action` for the shared pause/resume logic, and both handle restart from the game-over state independently.

Player movement from the analog stick is polled directly in `Player.input()` each frame rather than being event-driven, so it is continuous.

The joystick list is cached once at startup via `setup_controllers()`. Hot-plug requires re-running that method or re-init.

The quit chord is `InputSettings.JOY_BUTTON_QUIT_COMBO` (START + SELECT + L1 + R1). When all buttons are held on any connected controller, the game closes.

## 6. CRT overlay (`crt.py`)

`CRT` loads `AssetPaths.TV`, scales it to the screen, and on each `draw()` blits a fresh copy with a randomized alpha (flicker) and per-row scanlines. `GameManager._render_frame` calls it only in windowed mode so it doesn't double-up on a real CRT cabinet.

## 7. Settings (`settings.py`)

Single source of truth for all tunables.

| Class            | Purpose                                                               |
| ---------------- | --------------------------------------------------------------------- |
| `ColorSettings`  | Named colors + semantic aliases (`BG_COLOR`, `OVERLAY_BACKGROUND`).  |
| `ScreenSettings` | Resolution, FPS, title, CRT alpha range, scanline height.             |
| `InputSettings`  | Controller button/axis indices + quit combo + analog threshold.       |
| `PlayerSettings` | Player movement speed and initial sprite size.                        |
| `FishSettings`   | Fish spawn rate, size range, speed range, player growth amount.       |
| `UiSettings`     | Overlay text and font sizes for pause/game-over screens.               |
| `GameStateSettings` | Canonical state names (`playing`, `paused`, `game_over`).           |
| `FontSettings`   | Font file path.                                                       |
| `AudioSettings`  | Mute toggles + music volume.                                          |
| `AssetPaths`     | `__file__`-relative paths for non-font assets.                        |
| `DebugSettings`  | Debug-only toggles.                                                   |

**No magic numbers anywhere outside this file.**

## 8. Source tree

```
assets/
  font/Pixeled.ttf              Pixel font for retro UI text.
  graphics/effects/tv.png       CRT overlay texture.
core/
  sprites.py                    Player and Fish sprite classes.
systems/
  fish_manager.py               Fish spawning, collision, and player growth.
ui/                             (empty) Screens and HUD widgets go here.
utils/                          (empty) Pure helpers go here.
crt.py                          CRT post-processing overlay.
main.py                         Entry point + GameManager.
settings.py                     All tunables.
docs/                           ARCHITECTURE, TODO, TESTING, CHANGELOG.
.github/copilot-instructions.md Editor rules.
```

## 9. Current state-machine scope

- Active states: `playing`, `paused`, `game_over`.
- Not yet implemented: title screen and a full scene object architecture.

## 10. Audio (`systems/audio_manager.py`)

`AudioManager` is **data-driven**: every sound effect is declared in
`AudioSettings.SOUND_EFFECTS` (logical name → file path), and every gameplay
call site triggers one through a single entry point:

```python
self.audio.play("gulp")
self.audio.play("pause_in")
self.audio.play("scream")
```

Adding a new sound is one line in `settings.py`; the manager never changes.

**Why this shape:**

- **DRY.** No bespoke `play_X_sound` wrappers. One `play(name)` method covers every cue.
- **No middlemen.** Earlier drafts mapped each sound to a reserved
  `pygame.mixer.Channel`. For casual SFX that's overkill — pygame's default
  8-channel pool, used implicitly via `Sound.play()`, is sufficient and never
  drops audible cues in practice. If a future sound *must* never be cut off,
  the template documents a one-line opt-in for a dedicated channel.
- **Portable.** The class has zero game-specific identifiers; only the
  `AudioSettings` registry differs per project.

**Music API:** `play_random_music`, `pause_music`, `resume_music`,
`stop_music`, `toggle_mute`. `play_random_music` avoids back-to-back repeats
of the same track.

**Failure mode:** a missing asset or uninitialised mixer logs a warning and is
skipped; the game keeps running silently rather than crashing.

**Template:** `systems/audio_manager_template.py` is a self-documenting copy
intended to be lifted into other pygame projects. The header docstring
describes the `AudioSettings` contract the manager expects.

## 11. Extension points

- **Scene/state machine:** evolve string-state handling into dedicated scene classes and add the missing title scene.
- **Score / HUD:** add a score counter to `GameManager` or a dedicated HUD class in `ui/`; draw it in `_render_frame` before the CRT pass.
- **Sprite art:** replace the `pygame.Surface` placeholders in `Player.__init__` and `Fish.__init__` with loaded images.
