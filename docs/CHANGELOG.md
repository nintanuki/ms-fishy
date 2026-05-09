# Change Log

This file is an append-only record of every code change made to **Fishy**
by a human, AI assistant, or copilot tool. Read it before making changes so you know the current state of the codebase.

## Format

Each entry covers one logical change (which may touch multiple files). Use the
template below, with one `**File:** ... **Why:** ...` block per file touched.

    ## YYYY-MM-DD HH:MM — short summary

    **File:** path/to/file.py
    **Lines (at time of edit):** 38-52 (modified)
    **Before:**
        [old code]
    **After:**
        [new code]
    **Why:** explanation

## Conventions

* Line numbers reflect the file as it existed at the moment of the edit. Edits
  above shift line numbers below, so older entries will not match the current
  file. Never go back and "fix" old line numbers.
* Entries are append-only. Never delete history. If a later edit reverts an
  earlier one, write a new entry that references the original.
* For new files, write `(new file)` instead of a line range. The "Before"
  block can be omitted or marked `(file did not exist)`.
* For deletes, write `(deleted)` and put the removed code in "Before" with no
  "After" block.
* Keep "Before" / "After" blocks short. If a change is huge, summarize with a
  diff-style excerpt of the most important lines plus a sentence describing the
  rest, instead of pasting the entire file.
* New Entries should be BELOW this line, do not add new log entries to the top. These instructions must stay on top.

---

## 2026-05-07 — Generic-template cleanup pass

**File:** main.py
**Lines (at time of edit):** 12-31 (modified)
**Before:** `__init__` docstring referenced "the first dungeon level"; kept an unused `self.game_active = False`; called `set_mode((ScreenSettings.RESOLUTION), pygame.SCALED)` with redundant parens.
**After:** Generic docstring, no `game_active`, `set_mode(ScreenSettings.RESOLUTION, pygame.SCALED)`.
**Why:** Template was copy-pasted from a dungeon project; needed to be neutral so it can seed any new pygame project.
**Editor:** Bryan (Claude Opus 4.7)

**File:** main.py
**Lines (at time of edit):** 45-51 (modified)
**Before:** `reset_game` docstring was a 7-line block.
**After:** Tightened to a 4-line block with the same intent.
**Why:** Cosmetic; matches the docstring style of the rest of the file.
**Editor:** Bryan (Claude Opus 4.7)

**File:** main.py
**Lines (at time of edit):** 80-87 (modified)
**Before:** `_handle_keydown` only handled `F11`.
**After:** Added an `Esc` quit branch above the `F11` branch.
**Why:** So the template runs without a controller for development.
**Editor:** Bryan (Claude Opus 4.7)

**File:** settings.py
**Lines (at time of edit):** 22 (modified)
**Before:** `TITLE = "Mimic Dice"`
**After:** `TITLE = "Pygame Template"  # Replace with your project's name.`
**Why:** Generic placeholder for the template.
**Editor:** Bryan (Claude Opus 4.7)

**File:** settings.py
**Lines (at time of edit):** 58-66 (modified)
**Before:** `AssetPaths.TV = "assets/graphics/effects/tv.png"`; `DebugSettings.MUTE = False` duplicated `AudioSettings.MUTE`.
**After:** `AssetPaths.TV` is now `__file__`-relative via `os.path.join(os.path.dirname(__file__), ...)`; the duplicate `DebugSettings.MUTE` was removed.
**Why:** Cwd-relative paths break when launched via the arcade cabinet; duplicate mute flags caused ambiguity.
**Editor:** Bryan (Claude Opus 4.7)

**File:** crt.py
**Lines (at time of edit):** 1-3 (modified)
**Before:** `from settings import *`
**After:** `from settings import ScreenSettings, ColorSettings, AssetPaths`
**Why:** Explicit imports match `main.py` and make dependencies obvious.
**Editor:** Bryan (Claude Opus 4.7)

**File:** core/__init__.py
**Lines (at time of edit):** (new file)
**After:** `"""Core data classes and state machines for the game."""`
**Why:** Empty folders weren't tracked by git; gives the package a docstring and a stable home.
**Editor:** Bryan (Claude Opus 4.7)

**File:** systems/__init__.py
**Lines (at time of edit):** (new file)
**After:** `"""Gameplay systems (physics, AI, scoring, etc.)."""`
**Why:** Same as `core/__init__.py`.
**Editor:** Bryan (Claude Opus 4.7)

**File:** ui/__init__.py
**Lines (at time of edit):** (new file)
**After:** `"""User-interface widgets, screens, and HUD elements."""`
**Why:** Same as `core/__init__.py`.
**Editor:** Bryan (Claude Opus 4.7)

**File:** utils/__init__.py
**Lines (at time of edit):** (new file)
**After:** `"""Pure helper functions and small utilities."""`
**Why:** Same as `core/__init__.py`.
**Editor:** Bryan (Claude Opus 4.7)

**File:** README.md, docs/ARCHITECTURE.md, docs/TESTING.md, docs/TODO.md
**Why:** Reflected the code changes above (Esc now wired, `__init__.py` files exist) and added a "first-run setup, delete this block afterwards" section to README + a delete-this-section instruction on the first-run checklist in docs/TODO.md.
**Editor:** Bryan (Claude Opus 4.7)

## 2026-05-07 — Initial gameplay implementation

**File:** core/sprites.py
**Lines (at time of edit):** (new file)
**After:** `Player` sprite (yellow square, arrow-key + left-stick movement, boundary clamping) and `Fish` sprite (red square, random size/speed, spawns from left or right edge, self-destructs off-screen).
**Why:** First gameplay pass — player and enemy sprites for the eat-or-be-eaten mechanic.
**Editor:** Bryan

**File:** systems/fish_manager.py
**Lines (at time of edit):** (new file)
**After:** `FishManager` with `spawn_fish`, `check_collisions` (eat smaller fish → grow player; eaten by larger fish → exit), and `grow_player`.
**Why:** Centralizes all fish lifecycle logic, keeping `GameManager` thin.
**Editor:** Bryan

**File:** settings.py
**Lines (at time of edit):** 50-55 (added)
**After:** Added `PlayerSettings` (SPEED, SIZE) and `FishSettings` (SPAWN_RATE, MIN_SIZE, MAX_SIZE, MIN_SPEED, MAX_SPEED, PLAYER_GROWTH_RATE).
**Why:** New gameplay systems need tunables; all magic numbers must live in settings.py.
**Editor:** Bryan

**File:** main.py
**Lines (at time of edit):** 1-170 (modified)
**After:** `GameManager.__init__` now creates `Player`, `all_sprites`, `enemy_sprites`, and `FishManager`. `_update_world` drives all three. `_render_frame` draws both sprite groups.
**Why:** Wire the new sprites and manager into the frame loop.
**Editor:** Bryan

## 2026-05-08 — Docs rewritten for Fishy

**File:** README.md
**Lines (at time of edit):** 1-60 (replaced)
**Before:** Template scaffold description with first-run setup instructions.
**After:** Describes Fishy — the eat-or-be-eaten game, its current status, controls, and links.
**Why:** Docs reflected the template origin, not the actual game.
**Editor:** Bryan (GitHub Copilot — Claude Sonnet 4.6)

**File:** docs/ARCHITECTURE.md
**Lines (at time of edit):** 1-100 (replaced)
**Before:** Generic scaffold architecture with stub update/render descriptions.
**After:** Documents Player, Fish, FishManager, collision logic, and all current settings classes.
**Why:** Architecture had not been updated after gameplay was added.
**Editor:** Bryan (GitHub Copilot — Claude Sonnet 4.6)

**File:** docs/TODO.md
**Lines (at time of edit):** 1-60 (replaced)
**Before:** Template first-run checklist.
**After:** Real roadmap with completed items, core polish tasks, difficulty/feel, visuals, audio, and known code-health items.
**Why:** TODO reflected the template, not the game's actual state and goals.
**Editor:** Bryan (GitHub Copilot — Claude Sonnet 4.6)

**File:** docs/CHANGELOG.md
**Lines (at time of edit):** 3 (modified)
**Before:** `<RENAME ME — your project name>`
**After:** `Fishy`
**Why:** Project name was never filled in.
**Editor:** Bryan (GitHub Copilot — Claude Sonnet 4.6)

**File:** docs/TESTING.md
**Lines (at time of edit):** 1-30 (replaced)
**Before:** Template smoke checks (background color, title bar, CRT).
**After:** Added gameplay checks: player moves, fish spawn and scroll, player grows on eat, session ends on being eaten.
**Why:** No gameplay tests existed after the initial gameplay pass was added.
**Editor:** Bryan (GitHub Copilot — Claude Sonnet 4.6)

## 2026-05-08 — Pixel-perfect mask collision

**File:** core/sprites.py
**Lines (at time of edit):** 12 (Player.__init__), 82 (Fish.__init__) (modified)
**Before:** Neither sprite built a mask; collision relied on bounding-box rect overlap.
**After:** Both `Player.__init__` and `Fish.__init__` call `pygame.mask.from_surface(self.image)` after the surface is ready, storing it as `self.mask`.
**Why:** Fish are now polygon shapes on transparent surfaces; the bounding box contains large empty corners that triggered false collisions.
**Editor:** Bryan (GitHub Copilot — Claude Sonnet 4.6)

**File:** systems/fish_manager.py
**Lines (at time of edit):** 45, 64 (modified)
**Before:** `spritecollide(player, self.sprite_group, False)` used default rect collision. `grow_player` did not rebuild the mask after resizing.
**After:** `spritecollide(..., pygame.sprite.collide_mask)` for pixel-accurate hits. `grow_player` calls `pygame.mask.from_surface(player.image)` after resizing so the mask stays in sync.
**Why:** Required to make the new mask-based collision actually work end-to-end.
**Editor:** Bryan (GitHub Copilot — Claude Sonnet 4.6)

## 2026-05-08 — Fix fish tail direction; rename cryptic variables; improve comments

**File:** core/sprites.py
**Lines (at time of edit):** 54-91 (modified Fish.__init__)
**Before:** `tail = [(0, cy), (tail_w, 0), (tail_w, body_h)]` — triangle point was on the left, so the tail looked like a backwards arrowhead for a right-facing fish. Single-letter/abbreviated locals (`body_h`, `tail_w`, `total_w`, `cy`). Minimal comments.
**After:** `tail_points = [(0, 0), (0, body_height), (tail_width, center_y)]` — wide fan on the left, tip pointing right into the diamond. All locals renamed to full words (`body_height`, `tail_width`, `total_width`, `center_y`). Block comment explains the layout and what each point represents.
**Why:** Tail geometry was mirrored; variable names violated the project's readability rules; comments were not sufficient for a non-coder to follow the math.
**Editor:** Bryan (GitHub Copilot — Claude Sonnet 4.6)

## 2026-05-08 — Draw fish as polygon shape (diamond body + triangle tail)

**File:** settings.py
**Lines (at time of edit):** 65-66 (added to FishSettings)
**After:** Added `BODY_HEIGHT_RATIO = 0.5` and `TAIL_WIDTH_RATIO = 0.33`.
**Why:** Fish shape proportions belong in settings.py as named constants, not as inline magic numbers.
**Editor:** Bryan (GitHub Copilot — Claude Sonnet 4.6)

**File:** core/sprites.py
**Lines (at time of edit):** 41-66 (replaced Fish.__init__)
**Before:** `pygame.Surface((size, size))` filled solid red.
**After:** Transparent surface drawn with two `pygame.draw.polygon` calls — a flat left-pointing triangle (tail) and a flat diamond (body). `pygame.transform.flip` mirrors the surface for left-facing fish. `self.size` stored for accurate area comparisons.
**Why:** Visual representation of fish as a recognizable shape instead of a square.
**Editor:** Bryan (GitHub Copilot — Claude Sonnet 4.6)

**File:** systems/fish_manager.py
**Lines (at time of edit):** 47, 62 (modified)
**Before:** `fish_area = fish.rect.width * fish.rect.height`; `growth_amount = fish.rect.width * ...`
**After:** `fish_area = fish.size * fish.size`; `growth_amount = fish.size * ...`
**Why:** The polygon bounding box no longer equals the conceptual fish size, so the stored `fish.size` attribute is used instead for consistent area comparisons and growth calculation.
**Editor:** Bryan (GitHub Copilot — Claude Sonnet 4.6)

## 2026-05-08T17:35:08.8120954-04:00 — Stop restarting music every frame

**File:** main.py
**Lines (at time of edit):** 149 (removed)
**Before:** `self.audio.play_random_bgm() # move to functions later` was called every loop iteration in `GameManager.run()`.
**After:** Removed the per-frame call so background music is started by `AudioManager` initialization instead of being continuously reloaded.
**Why:** Reloading and replaying music each frame effectively prevented audible playback even after the path issue was fixed.
**Editor:** Bryan (GitHub Copilot — GPT-5.3-Codex)
