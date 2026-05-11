"""Gameplay HUD widget showing run stats and hunger timer."""

from __future__ import annotations

import math

import pygame

from core.score import Score
from core.sprites import Player
from settings import ColorSettings, TimerSettings, UiSettings


class Hud:
    """Draw stacked run stats and a colour-coded hunger countdown in the top-left corner.

    Layout (top to bottom, all left-aligned):
        TOTAL FISH EATEN: NN
        WEIGHT EATEN: NNNNN
        CURRENT WEIGHT: NNNNN
        HUNGER TIMER: MM:SS   (red when <= HUNGER_WARNING_SECONDS)
        [hunger bar]
    """

    def __init__(
        self,
        score: Score,
        font: pygame.font.Font,
        player: Player,
    ):
        """Initialize HUD dependencies.

        Args:
            score: The run-scoped score model for the current session.
            font: Font used for all HUD text.
            player: The player sprite; provides current weight for display.
        """
        self.score = score
        self.font = font
        self.player = player

    def draw(self, screen: pygame.Surface, remaining_seconds: float = 0.0) -> None:
        """Draw stacked run stats and hunger timer in the top-left corner.

        Args:
            screen: The pygame surface to draw on.
            remaining_seconds: Countdown time left in seconds.
        """
        padding = UiSettings.HUD_PADDING
        line_h = UiSettings.HUD_LINE_SPACING
        x = padding

        # ------------------------------------------------------------------
        # STAT ROWS
        # ------------------------------------------------------------------
        stat_rows = [
            f"TOTAL FISH EATEN: {self.score.fish_eaten}",
            f"WEIGHT EATEN: {self.score.size_eaten}",
            f"CURRENT WEIGHT: {int(self.player.size)}",
        ]
        for i, text in enumerate(stat_rows):
            surf = self.font.render(text, True, ColorSettings.IN_GAME_HUD_TEXT)
            screen.blit(surf, (x, padding + i * line_h))

        # ------------------------------------------------------------------
        # HUNGER TIMER
        # ------------------------------------------------------------------
        timer_y = padding + 3 * line_h
        display_seconds = max(0, math.ceil(remaining_seconds))
        minutes, secs = divmod(display_seconds, 60)
        timer_text = f"HUNGER TIMER: {minutes:02d}:{secs:02d}"
        # Timer text turns red at the warning threshold.
        # TODO: add a warning audio cue here when sound system supports it.
        timer_color = (
            ColorSettings.RED
            if remaining_seconds <= UiSettings.HUNGER_WARNING_SECONDS
            else ColorSettings.IN_GAME_HUD_TEXT
        )
        timer_surf = self.font.render(timer_text, True, timer_color)
        screen.blit(timer_surf, (x, timer_y))

        # ------------------------------------------------------------------
        # HUNGER BAR
        # ------------------------------------------------------------------
        # Position bar below the actual rendered timer text, not a fixed line_h,
        # so it never overlaps the label regardless of font size.
        bar_y = timer_y + timer_surf.get_height() + UiSettings.HUD_BAR_TOP_GAP
        bar_w = UiSettings.HUD_BAR_WIDTH
        bar_h = UiSettings.HUD_BAR_HEIGHT
        fraction = max(0.0, min(1.0, remaining_seconds / TimerSettings.STARTING_SECONDS))

        # Background track (always full width, dark).
        pygame.draw.rect(screen, ColorSettings.NERO, (x, bar_y, bar_w, bar_h))
        # Filled portion: green when full, red when empty, smooth lerp.
        fill_w = int(bar_w * fraction)
        if fill_w > 0:
            r = int(255 * (1.0 - fraction))
            g = int(255 * fraction)
            pygame.draw.rect(screen, (r, g, 0), (x, bar_y, fill_w, bar_h))
