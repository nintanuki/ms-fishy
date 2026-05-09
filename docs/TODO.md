# Ms. Fishy — Roadmap & TODO

Move completed items from `[ ]` to `[x]`. Do not delete entries.

---

## Completed

- [x] **Ms. Fishy rebrand** — renamed game from *Fishy* to *Ms. Fishy* (à la Ms. Pac-Man) to match the cute voice samples used for the gulp/scream SFX. Player fish now wears a pink bow above the body apex.
- [x] `GameManager` frame loop (events → update → render → flip).
- [x] Keyboard and controller input routing.
- [x] `F11` / `BACK` fullscreen toggle.
- [x] `Esc` keyboard quit.
- [x] `START + SELECT + L1 + R1` controller quit chord.
- [x] CRT overlay (scanlines + flicker, windowed only).
- [x] `Player` sprite with arrow-key and left-stick movement, screen-boundary clamping.
- [x] `Fish` sprite spawning from left/right edges, scrolling across, self-destructing off-screen.
- [x] `FishManager` spawn timer and eat-or-be-eaten collision logic.
- [x] Player grows when eating a smaller fish (`FishSettings.PLAYER_GROWTH_RATE`).
- [x] Session ends when a larger fish hits the player.

---

## In progress

*(nothing active)*

---

## Core gameplay polish

- [x] **Pixel-perfect (mask) collision** — swap `spritecollide` for `collide_mask` now that fish are polygon shapes; bounding-box overlap fires in empty transparent corners.
- [x] Game-over screen instead of abrupt `sys.exit()` when eaten — black screen, large centered `Pixeled.ttf` white text ("GAME OVER" / restart prompt). No abrupt exit.
- [ ] Title / start screen before gameplay begins.
- [ ] Scene/state machine: `title → playing → game_over → (restart or quit)`.
- [x] Pause feature — `Enter` key freezes world, stops music, shows centered pause text on black; resume restores music. Play `sfx_sounds_pause2_in.ogg` on pause and `sfx_sounds_pause2_out.ogg` on unpause.
- [ ] Score counter: track fish eaten or total pixels consumed; display in the HUD.
- [ ] High-score persistence: save the session's top score to a JSON file next to `main.py`.
- [ ] Statistics in hud (# of fish eaten, total weight eaten, time elapsed, etc)
- [ ] Game should end when player width exceeds screen width. Display message about having destroyed the ecosystem.
- [ ] Add enemies that can't be eaten, such as jellyfish (pure obstacle) or a shark that chases you (maybe at higher levels)
- [ ] Different levels and maps with obstacles such as coral, etc.
- [x] Controller needs to be able to pause too, currently can only pause with enter button

---

## Feel and difficulty

- [ ] Difficulty ramp: gradually decrease `FishSettings.SPAWN_RATE` and increase fish speed as the session goes on.
- [ ] Fish variety: multiple size tiers with distinct colors so the player can read threat level at a glance. Loop randomly through a list of set colors
- [ ] Player growth cap or diminishing-returns curve so the endgame stays interesting.
- [ ] Screen-wrapping option (player exits left edge → re-enters right edge) as an alternative to boundary clamping.

---

## Visuals

- [x] **Player fish shape** — give the player the same diamond-body + triangle-tail polygon treatment as enemy fish; remove the yellow square placeholder.
- [ ] **Enemy fish color variety** — randomize or tier fish colors so threat level is readable at a glance.
- [x] **Fish eyes** — small black square centered vertically, positioned one-quarter of the way from the nose toward the start of the tail.
- [ ] **Fish outlines / shadow** — add a black outline or drop-shadow to all fish (player and enemy) for legibility against the background.
- [x] **Player distinction** — give the player a unique color, gradient, or other visual marker so it stands out from enemy fish.
- [ ] Replace fish polygon shapes with imported sprites once art is ready (multiple frames for swim cycle).
- [ ] Scrolling ocean background or parallax layers.
- [ ] Particle effect when the player eats a fish (splash, bubbles).
- [ ] More polygons as fish get bigger? The diamond + triangle shape has it's charm and I like it, but when the player is half the screen it looks bad. Maybe the player could be a different shape such as an ellipse? Or get more polygons as they get bigger?
- [ ] Kelp or seaweed in the background?
- [ ] Underwater visual effect (waviness)?
- [ ] Make a note in the documentation, as a rule this game will only use Pygame's tools for drawing to create images and visual effects. No imported visual assets or image files (audio and font assets are fine). I want to use this project to see how much I can do with Pygame alone.

---

## Audio

- [ ] Initialize `pygame.mixer` in `GameManager.__init__`.
- [ ] Eat sound effect triggered in `FishManager.grow_player`.
- [ ] Death sound triggered on game-over.
- [ ] Looping background music that respects `AudioSettings.MUTE_MUSIC`.
- [ ] All audio toggle via `AudioSettings.MUTE`.

---

## Code-health items inherited from the template

- [x] `crt.py` used `from settings import *`. Now uses explicit imports.
- [x] `AudioSettings.MUTE` / `DebugSettings.MUTE` were duplicated. Kept `AudioSettings.MUTE`; removed the duplicate.
- [x] `AssetPaths.TV` was a cwd-relative path. Now `__file__`-relative, like `FontSettings.FONT`.
- [x] `GameManager.__init__` carried an unused `self.game_active`. Removed.
- [x] `pygame.display.set_mode((ScreenSettings.RESOLUTION), pygame.SCALED)` had redundant parens. Removed.
- [x] Empty `core/`, `systems/`, `ui/`, and `utils/` folders now have `__init__.py` files so git tracks them.
- [x] `Esc` is wired in `_handle_keydown` so the game runs without a controller.
- [x] `ScreenSettings.TITLE` is still `"Pygame Template"` — update to `"Fishy"`.
- [ ] `FishManager.check_collisions` calls `pygame.quit()` / `sys.exit()` directly — should route through `GameManager.close_game()` or a scene transition instead.
- [ ] `Player.input()` re-queries `pygame.joystick.Joystick(i)` every frame — should use the cached list from `GameManager`.

---

## Rules

- [x] **Keyboard/controller parity** — anything doable on the keyboard must also be reachable on the controller. Documented in ARCHITECTURE.md § 5.

---

## Ideas

- [x] Add more realistic/challenging movement to mimic being underwater, there should be some initial inertia when first moving, and when the player lets go of the arrow key or analog stick the player should still keep moving a little before slowing down.

---

## Documentation maintenance

Every pass that meaningfully changes a system must:

1. Update [docs/ARCHITECTURE.md](ARCHITECTURE.md).
2. Append entries to [docs/CHANGELOG.md](CHANGELOG.md).
3. Move completed items here from `[ ]` to `[x]` (do not delete).
