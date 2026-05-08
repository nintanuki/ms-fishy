# Fishy — Architecture

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
3. `_update_world()` — advance `all_sprites`, `enemy_sprites`, and `FishManager`.
4. `_render_frame()` — `screen.fill(BG_COLOR)`, draw `all_sprites`, draw `enemy_sprites`, then the CRT overlay (windowed only).
5. `pygame.display.flip()` and `clock.tick(FPS)`.

## 3. Sprites (`core/sprites.py`)

### `Player`

A `pygame.sprite.Sprite` representing the player fish.

- **Appearance:** Yellow square, initial size `PlayerSettings.SIZE`.
- **Movement:** Arrow keys and left analog stick. Speed is `PlayerSettings.SPEED` px/frame.
- **Boundary:** `enforce_boundaries` clamps the rect to the screen edges each frame.
- **Growth:** `FishManager.grow_player` replaces `player.image` and `player.rect` with a larger yellow square when the player eats a fish. Growth amount is `FishSettings.PLAYER_GROWTH_RATE` px per eat.

### `Fish`

A `pygame.sprite.Sprite` representing an enemy fish.

- **Appearance:** Red square of a random size in `[FishSettings.MIN_SIZE, FishSettings.MAX_SIZE]`.
- **Spawn:** From off the left or right edge at a random vertical position. Direction is set to match the side it spawned from (left→right, right→left).
- **Movement:** Constant horizontal speed in `[FishSettings.MIN_SPEED, FishSettings.MAX_SPEED]`. Self-destructs (`kill()`) once it clears the opposite edge by 50 px.

## 4. Fish manager (`systems/fish_manager.py`)

`FishManager` holds the `enemy_sprites` group and drives the fish lifecycle each frame:

1. **Spawn timer:** increments each frame; fires `spawn_fish()` every `FishSettings.SPAWN_RATE` frames (≈1 s at 60 FPS) and resets.
2. **Collision:** `check_collisions` calls `pygame.sprite.spritecollide` against the player.
   - Player rect area > fish rect area → `grow_player`, fish is killed.
   - Player rect area ≤ fish rect area → `pygame.quit()` + `sys.exit()` (immediate exit; no game-over screen yet).

## 5. Input

Events are routed by type:

- `KEYDOWN` → `_handle_keydown`. `Esc` quits; `F11` toggles fullscreen.
- `JOYBUTTONDOWN` → `_handle_joybuttondown`. Quit-chord check; `BACK` toggles fullscreen.
- `JOYHATMOTION` → `_handle_joyhatmotion` (stub).
- `JOYAXISMOTION` → `_handle_joyaxismotion` (stub).

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

## 9. Extension points

- **Game-over screen:** replace the `pygame.quit()` / `sys.exit()` calls in `FishManager.check_collisions` with a transition to a game-over scene.
- **Scene/state machine:** give `GameManager` a current-scene attribute and forward `_handle_*` / `_update_world` / `_render_frame` calls to it. Scenes: title, playing, game-over, pause.
- **Score / HUD:** add a score counter to `GameManager` or a dedicated HUD class in `ui/`; draw it in `_render_frame` before the CRT pass.
- **Sprite art:** replace the `pygame.Surface` placeholders in `Player.__init__` and `Fish.__init__` with loaded images.
- **Audio:** initialize `pygame.mixer` in `GameManager.__init__` and call sound effects from `FishManager.grow_player` and the death branch.
