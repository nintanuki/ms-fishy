# Pygame Template — Manual Testing Checklist

Run after a non-trivial change.

```powershell
cd pygame-template-files
python main.py
```

## Smoke

1. Boot: window opens at the resolution defined by `ScreenSettings.RESOLUTION`, no console errors.
2. The title bar shows `ScreenSettings.TITLE`.
3. The background is `ColorSettings.BG_COLOR`.
4. The CRT overlay is visible (scanlines + slight flicker).

## Globals

5. `F11` toggles fullscreen. CRT overlay disappears in fullscreen, reappears in windowed.
6. `Esc` exits cleanly.
7. With a controller connected: `BACK` toggles fullscreen.
8. With a controller connected: holding `START + SELECT + L1 + R1` exits cleanly.
9. Closing the OS window via the title-bar `X` exits cleanly.

## Sign-off

- [ ] Smoke + globals all passed.
- [ ] [docs/CHANGELOG.md](CHANGELOG.md) updated.
- [ ] [docs/ARCHITECTURE.md](ARCHITECTURE.md) updated if structure changed.
- [ ] [docs/TODO.md](TODO.md) updated if a roadmap item was completed.
