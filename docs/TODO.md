# Ms. Fishy — Roadmap & TODO

Move completed items from `[ ]` to `[x]`. Do not delete entries.

The roadmap is grouped into **passes**. A pass is a focused batch of work
where every item is at a similar level of architectural depth. Earlier
passes lay foundation that later passes depend on, so finish a pass before
starting the next one even if a later item looks individually easier.
Within a pass, items are ordered low-to-high difficulty.

---

## Completed

- [x] **Ms. Fishy rebrand** — renamed game from *Fishy* to *Ms. Fishy* (à la Ms. Pac-Man) to match the cute voice samples used for the gulp/scream SFX. Player fish now wears a pink bow above the body apex.
- [x] `GameManager` frame loop (events → update → render → flip).
- [x] Keyboard and controller input routing.
- [x] `F11` / `BACK` fullscreen toggle (now via shared `_toggle_fullscreen` helper).
- [x] `Esc` keyboard quit.
- [x] `START + SELECT + L1 + R1` controller quit chord.
- [x] CRT overlay (scanlines + flicker, windowed only).
- [x] `Player` sprite with arrow-key and left-stick movement, screen-boundary clamping.
- [x] `Fish` sprite spawning from left/right edges, scrolling across, self-destructing off-screen.
- [x] `FishManager` spawn timer and eat-or-be-eaten collision logic.
- [x] Player grows when eating a smaller fish (`FishSettings.PLAYER_GROWTH_COEFFICIENT`).
- [x] Session ends when a larger fish hits the player.
- [x] **Pixel-perfect (mask) collision** for fish-vs-player.
- [x] Game-over screen instead of abrupt `sys.exit()` when eaten.
- [x] Pause feature — keyboard (Enter) and controller (START); pauses world + music; plays pause-in/out SFX.
- [x] Underwater inertia movement (acceleration, drag, counter-acceleration, sub-pixel accumulators).
- [x] Retro visual pass: ocean gradient bg, fish drop shadows, gradient player, palette-randomized fish.
- [x] Player fish polygon shape (replaced the yellow square placeholder).
- [x] Player distinction (gradient + bow) so it stands out from enemies.
- [x] Fish eyes — small black square positioned half-way between body center and nose.
- [x] Audio system (`AudioManager`) with data-driven sound registry, music randomizer, mute, pause/resume.
- [x] **Player spawn centered correctly** at startup (was anchored topleft).
- [x] **Architecture rule**: keyboard/controller parity for every action.
- [x] **Architecture rule**: input handlers must not call each other; share via action methods.
- [x] **Architecture rule**: prefer updating an existing function over creating a near-duplicate name.
- [x] **Architecture rule**: never add/remove/modify in-game UI without explicit user request.
- [x] **Code-health items inherited from the template** — explicit imports in `crt.py`, deduped mute flags, `__file__`-relative asset paths, removed unused `game_active`, all `__init__.py` files present, `Esc` wired, title set, no `sys.exit()` in `FishManager`, joystick list cached.

---

## In progress

*(nothing active)*

---

## Pass 1 — Foundation (do first, unblocks everything else)

These are architectural decisions every later feature depends on. Doing
them now is cheaper than retrofitting after the title screen, score, and
HUD already exist.

The implementation notes in each item are written for an implementer LLM:
follow them literally; do not invent extra behaviour.

### 1.1 Project rule: visuals are 100% Pygame primitives

- [x] Add this rule to [docs/ARCHITECTURE.md](ARCHITECTURE.md) (in §7 Settings or a new §12 Project rules) and to [.github/copilot-instructions.md](../.github/copilot-instructions.md) (under "Code style"):

  > **No imported visual assets.** All sprites, backgrounds, particles, and
  > visual effects must be drawn at runtime with `pygame.draw`,
  > `pygame.Surface` operations, or per-pixel manipulation. Audio files
  > and font files are allowed. The CRT overlay PNG
  > (`assets/graphics/effects/tv.png`) is grandfathered as the only
  > exception; do not add new image files.

- Acceptance: rule is in both files; no other code change required.

### 1.2 `utils/text.py` — centered-text helper

- [x] Create [utils/text.py](../utils/text.py) with one function:

  ```python
  def draw_centered_text(
      surface: pygame.Surface,
      text: str,
      font: pygame.font.Font,
      color: tuple[int, int, int],
      center: tuple[int, int],
  ) -> pygame.Rect:
      """Render `text` with `font` and blit it centered at `center`.
      Returns the blitted rect (useful for stacking lines)."""
  ```

- Refactor `GameManager._draw_centered_overlay` in [main.py](../main.py) to call this helper instead of duplicating the render/get_rect/blit dance.
- Acceptance: pause and game-over screens look identical to before; `utils/text.py` is importable and has the docstring.

### 1.3 `Scene` base class + `SceneManager`

Replace the string-based `game_state` with first-class `Scene` objects.

- [x] Create [core/scene.py](../core/scene.py) with base `Scene` class and lifecycle hooks.
- [x] Create [systems/scene_manager.py](../systems/scene_manager.py) with `SceneManager` for transitions.
- [x] Create [ui/scenes/](../ui/scenes/) package with `__init__.py`.
- [x] Create [ui/scenes/play_scene.py](../ui/scenes/play_scene.py) wrapping current gameplay.
- [x] Create [ui/scenes/game_over_scene.py](../ui/scenes/game_over_scene.py) wrapping current game-over state.
- [x] Refactor [main.py](../main.py) to use `SceneManager`; remove gameplay attributes from `GameManager`.
- [x] Update [docs/ARCHITECTURE.md](ARCHITECTURE.md) to show new scene-based architecture.
- [x] Add changelog entry.

- Acceptance: pressing Enter still pauses/unpauses (now via `PlayScene.handle_event`), still restarts on game-over, fullscreen + quit-combo + Esc still work, and the architecture diagram in [docs/ARCHITECTURE.md](ARCHITECTURE.md) is updated to show the SceneManager in the middle.

### 1.4 `TitleScene`

- [x] Create [ui/scenes/title_scene.py](../ui/scenes/title_scene.py) (create the `ui/scenes/` package as needed with an `__init__.py`).
- Visuals:
  - Same ocean gradient background as the play scene. Reuse the `build_gradient_surface` helper — move it to `utils/graphics.py` if needed by both scenes.
  - Title text **"MS. FISHY"** centered horizontally, vertically positioned at 35% screen height, rendered with `Pixeled.ttf` at a large size (add `UiSettings.TITLE_FONT_SIZE = 96` to [settings.py](../settings.py)).
  - Prompt text **"PRESS START TO PLAY"** centered horizontally, vertically positioned at 60% screen height, at `UiSettings.OVERLAY_FONT_SIZE`.
  - Below the prompt, render the current top high-score line **"HI: NNNNN  XYZ"** (zero-padded score, then the initials) centered. If the leaderboard is empty, render **"HI: -----"**. Use `UiSettings.OVERLAY_FONT_SIZE`.
  - **Background fish swim across the screen** while the title is showing. Reuse `FishManager` exactly — instantiate it inside `TitleScene` and call its `update(player=None)`. To make `FishManager.update` accept `None`, change its signature so when `player is None` it skips the collision step and only spawns/moves fish. Returns `(False, 0)` in that case.
- Input:
  - `Enter` (keyboard) or `START` (controller) transitions to `PlayScene`. **Important:** the title scene's fish must **not** be passed to the play scene — the play scene creates its own fresh `FishManager`.
- Add the title text and prompt to [settings.py](../settings.py) `UiSettings`:
  - `TITLE_TEXT = "MS. FISHY"`
  - `START_PROMPT_TEXT = "PRESS START TO PLAY"`
  - `HIGH_SCORE_LABEL = "HI: "`
- Acceptance: launching the game shows the title screen; fish drift across; Enter/START starts a new run with no fish on-screen.

### 1.5 `PlayScene` + player drop-in animation

- [ ] Create [ui/scenes/play_scene.py](../ui/scenes/play_scene.py).
- Owns: `player`, `all_sprites`, `enemy_sprites`, `fish_manager`, `bg_surface`, and a small substate enum `DROPPING_IN` / `ACTIVE` / `PAUSED`.
- **Drop-in animation** (substate `DROPPING_IN`, runs once on `on_enter`):
  - Spawn the player above the screen at `(WIDTH // 2, -player.rect.height)`.
  - Each frame, move the player downward toward the screen center using the same velocity model already in `Player` — but apply a one-time downward velocity at `on_enter` (e.g. `player.velocity_y = PlayerSettings.DROP_IN_VELOCITY`, new constant, `2.0` px/frame). Let `DRAG` and `STOP_THRESHOLD` bring it to rest naturally near the center.
  - During this substate: ignore movement input (skip `Player.input`); still draw the player and the gradient background; do **not** call `FishManager.update` (no fish spawn yet).
  - Transition to `ACTIVE` when `abs(player.velocity_y) < PlayerSettings.STOP_THRESHOLD` **and** `player.rect.centery >= HEIGHT // 2 - 4` (small tolerance for rounding).
- **`ACTIVE`**: behaves exactly like the current play loop — input on, fish spawn on, collisions on. On a "fish ate player" event, transition to `GameOverScene`.
- **`PAUSED`**: same as today (Enter/START toggles, audio pause/resume, centered "PAUSED" text on black; no fish update).
- Add to [settings.py](../settings.py) `PlayerSettings`:
  - `DROP_IN_VELOCITY = 2.0  # px/frame; initial downward velocity for the title→play transition`
- Acceptance: pressing START on the title screen shows an empty ocean; the player visibly drifts in from the top and settles at the center; only after it settles do fish begin to spawn.

### 1.6 `GameOverScene` (real scene, no UI changes yet — leaderboard comes in Pass 2)

- [ ] Create [ui/scenes/game_over_scene.py](../ui/scenes/game_over_scene.py).
- Renders exactly what the current `game_over` state renders today: black background, centered "GAME OVER". No restart prompt yet (the leaderboard scene in Pass 2 replaces this).
- `Enter` or `START` transitions to a fresh `PlayScene`.
- Acceptance: behaviour is identical to today; the only structural change is that this is a real `Scene` subclass.

---

## Pass 2 — Score, leaderboard, persistence

Small but unblocks the title screen actually having something interesting
to show, and gives players a reason to keep playing.

### 2.1 Score model

- [ ] Create [core/score.py](../core/score.py) with one class:

  ```python
  class Score:
      """Tracks a single run's score. Owned by PlayScene."""
      def __init__(self):
          self.fish_eaten = 0
          self.size_eaten = 0  # cumulative integer pixels
      def add(self, fish_size: int) -> None:
          self.fish_eaten += 1
          self.size_eaten += fish_size
      @property
      def total(self) -> int:
          """The number persisted on the leaderboard. Equals size_eaten."""
          return self.size_eaten
  ```

- `PlayScene` holds a `Score` instance and calls `score.add(fish.size)` whenever `FishManager.update` reports an eat. Pass that score into `GameOverScene` when transitioning.

### 2.2 HUD widget

- [ ] Create [ui/hud.py](../ui/hud.py) with one class `Hud` that takes a `Score` and a font, and exposes a `draw(screen)` method.
- Layout:
  - Top-left: **"FISH: NN"** (zero-padded to 2 digits if you like; otherwise just integer).
  - Top-right: **"SCORE: NNNNN"** (zero-padded to 5 digits).
  - Top-center: **"HI: NNNNN  XYZ"** (current top leaderboard entry, or `"HI: -----"` when empty).
  - All HUD text uses `UiSettings.HUD_FONT_SIZE = 24` (new constant). Padded 16 px from the screen edges (new `UiSettings.HUD_PADDING = 16`).
- `PlayScene.render` calls `self.hud.draw(screen)` after the world sprites and before the game returns control (CRT pass still happens last in `GameManager`).
- Acceptance: HUD is visible during play, hidden on title and pause screens (game-over screen has its own layout).

### 2.3 Leaderboard model + persistence

- [ ] Create [systems/leaderboard.py](../systems/leaderboard.py):

  ```python
  class Leaderboard:
      """Top-10 scoreboard with initials. Persists to JSON next to main.py."""
      MAX_ENTRIES = 10
      FILE_NAME = "leaderboard.json"   # add to AssetPaths instead if cleaner

      def __init__(self): ...
      def load(self) -> None: ...      # reads JSON; missing file = empty list
      def save(self) -> None: ...      # writes JSON atomically
      def qualifies(self, score: int) -> bool: ...
      def submit(self, initials: str, score: int) -> int | None:
          """Insert or update. Returns the 0-based rank if accepted, else None."""
      def top(self) -> list[tuple[str, int]]: ...   # sorted high → low
  ```

- **Initial-deduplication rule** (implementer: read this carefully):
  - `initials` is always exactly 3 uppercase A–Z letters. `submit` validates and uppercases.
  - If an entry with the same initials already exists:
    - If the new score is **strictly greater**, update that entry's score in place and re-sort. Return its new rank.
    - If the new score is **less than or equal**, do nothing and return `None` (even if the new score would otherwise have qualified under different initials — same initials means "this player already has a better record").
  - If no entry with those initials exists and the list has fewer than 10 entries, append.
  - If no entry with those initials exists and the list is full, replace the lowest-scoring entry **only if** the new score is strictly greater than that lowest score.
  - After every accepted submission, sort high → low and truncate to 10.

- **File format** (`leaderboard.json` next to `main.py`):

  ```json
  [
    {"initials": "BRY", "score": 12345},
    {"initials": "AAA", "score": 9000}
  ]
  ```

- Add to [settings.py](../settings.py) `AssetPaths`:
  - `LEADERBOARD = os.path.join(BASE_DIR, "leaderboard.json")`

- `Leaderboard` is owned by `GameManager` (one instance for the whole process). Title scene reads it for the HI line; game-over scene reads/writes via `submit`.

### 2.4 Initials-entry scene

- [ ] Create [ui/scenes/initials_entry_scene.py](../ui/scenes/initials_entry_scene.py).
- Reached **only** from `GameOverScene` when `leaderboard.qualifies(score)` is true. If the score doesn't qualify, `GameOverScene` skips this scene and shows the regular game-over layout straight away.
- Layout (centered column on a black background):
  - Line 1 (top, large): **"NEW HIGH SCORE"** at `UiSettings.OVERLAY_FONT_SIZE`.
  - Line 2: **"SCORE: NNNNN"**.
  - Line 3: **"ENTER YOUR INITIALS"** at `UiSettings.HUD_FONT_SIZE`.
  - Line 4 (large, the editor): three letter slots **"_ _ _"** with the currently-selected slot highlighted (white box outline, 2 px). Letters fill in as the player commits each slot.
  - Line 5: **"PRESS START WHEN DONE"** at `UiSettings.HUD_FONT_SIZE`.
- Input model — three editable slots, current slot index `0..2`:
  - **Keyboard typing**: pressing any A–Z key sets that letter into the current slot and advances the cursor. After the third letter is committed, the cursor stops at slot 2 (any further A–Z keys overwrite slot 2).
  - **Backspace**: clears the current slot (or steps back to the previous slot if the current is already empty) and moves the cursor to that slot.
  - **Up arrow / D-pad up**: cycle the current slot's letter up alphabetically (`A → B → ... → Z → A`). If empty, start at `A`.
  - **Down arrow / D-pad down**: cycle down (`A → Z → Y → ...`).
  - **Left arrow / D-pad left**: move cursor to the previous slot (clamped at 0).
  - **Right arrow / D-pad right**: move cursor to the next slot (clamped at 2).
  - **Enter / START**: commit. If any slot is empty, fill it with `A`. Call `leaderboard.submit(initials, score)` and `leaderboard.save()`. Transition to `LeaderboardScene` (next item).
- Acceptance: a qualifying run is followed by an editable 3-letter prompt that accepts both keyboard typing and arrow/controller stepping, persists the result, and moves on.

### 2.5 Leaderboard display scene

- [ ] Create [ui/scenes/leaderboard_scene.py](../ui/scenes/leaderboard_scene.py).
- Reached from:
  - `InitialsEntryScene` after submit.
  - `GameOverScene` after a non-qualifying death (no initials prompt — this scene replaces the bare "GAME OVER" screen for non-qualifying runs once the leaderboard exists).
- Layout (centered column on a black background):
  - Header: **"GAME OVER"** at `UiSettings.OVERLAY_FONT_SIZE`.
  - Subheader: **"SCORE: NNNNN"** at `UiSettings.HUD_FONT_SIZE`.
  - Then the leaderboard, one row per entry, e.g.:

    ```
     1.  BRY    12345
     2.  AAA     9000
    ...
    ```

  - If the player just submitted, **highlight their row** (white background, black text, or just bold/underlined) using their initials + score as the match key.
  - Footer: **"PRESS START TO RETURN TO TITLE"**.
- Input: `Enter` / `START` returns to `TitleScene` (which now reads the updated high score for its HI line).
- Acceptance: every game-over now ends here; a qualifying run highlights the player's row; pressing start returns to the title.

### 2.6 Wire it all together

- [ ] `GameOverScene.on_enter` should:
  1. Stop music; play scream SFX (already done today).
  2. If `game.leaderboard.qualifies(score)`, change to `InitialsEntryScene(score)`.
  3. Else, change to `LeaderboardScene(score, highlight=None)`.
- [ ] `TitleScene.render` reads `game.leaderboard.top()[0]` (or the empty case) for the HI line.
- [ ] `Hud.draw` reads the same.

---

## Pass 3 — Levels and level design *(placeholder — design TBD)*

Difficulty in Ms. Fishy will come from **level design**, not from a global
difficulty ramp or fish-stat scaling. The base loop where the player
eventually grows into an unstoppable juggernaut is intentional and is the
reward — do not nerf it.

Concrete level-design plans will be added here once the foundation passes
land. Likely directions to revisit later:

- [ ] Hand-authored arenas with static obstacle layouts (coral walls,
  rocks, narrow tunnels) drawn from polygons.
- [ ] Per-level fish-pool overrides (specific size mixes, specific
  spawn-side weights) without changing the global `FishSettings`.
- [ ] Hazards that don't scale with the player: jellyfish (always lethal,
  drift vertically), shark (always lethal, chases). These remain
  threatening even when the player is huge — the only thing that does.

---

## Pass 4 — Visual polish (Pygame-primitive only)

Last pass. These items make the game prettier without affecting gameplay.
Everything here must be drawable with Pygame's draw API — no imported art.

- [ ] **Black outline** on all fish (player and enemy) for legibility.
- [ ] **Polygon-tier player shape** — once the player fish exceeds some
  fraction of screen size, rebuild the body from more polygons (ellipse
  approximation, segmented diamond, or curved spine) so a giant fish
  doesn't look blocky. Diamond+triangle stays for small/medium sizes.
  This is a **visual** tier, not a difficulty tier — stats don't change.
- [ ] **Particle system** (`systems/particles.py`) — splash/bubbles when
  the player eats a fish.
- [ ] **Parallax background** — multiple gradient/silhouette layers (kelp
  silhouettes, distant fish dots) drawn from primitives.
- [ ] **Kelp / seaweed** drawn as wavy line strips, swayed by a low-freq
  sine so the world breathes.
- [ ] **Underwater waviness** — per-frame horizontal offset along scanlines
  for a shimmer effect.

---

## Pass 5 — Audio polish

Most of the audio system already exists; only thin gaps remain.

- [ ] **In-game audio toggle** — a controller button + keyboard key that
  calls `AudioManager.toggle_mute`. Surface the current mute state in the
  pause overlay.
- [ ] **Distinct SFX** for: title-screen confirm, leaderboard-entry
  qualify celebration, leaderboard scroll/select.

---

## Pass 6 — Settings menu

Now that there are scenes and persistence, give the player real knobs.

- [ ] **Options scene** reachable from the title — toggle CRT overlay,
  music volume, SFX volume.
- [ ] **Persist options** alongside the leaderboard (separate JSON file
  next to `main.py`, e.g. `options.json`).

---

## Ideas / parking lot

Things to consider but not yet planned into a pass.

- [ ] **Combo system** — eating fish quickly in succession multiplies score.
- [ ] **Cosmetic ecosystem events** — occasionally a non-player big fish
  eats a non-player small fish nearby (purely visual, but sells the
  ecosystem).
- [ ] **Screen-wrap movement option** as an alternative to boundary
  clamping (player exits left → enters right). Toggleable in the options
  scene from Pass 6 if revisited.
- [ ] **Imported sprite art** — explicitly *off the table* per the
  Pygame-primitive rule from Pass 1.

---

## Documentation maintenance

Every pass that meaningfully changes a system must:

1. Update [docs/ARCHITECTURE.md](ARCHITECTURE.md).
2. Append entries to [docs/CHANGELOG.md](CHANGELOG.md).
3. Move completed items here from `[ ]` to `[x]` (do not delete).
