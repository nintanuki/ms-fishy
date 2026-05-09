"""Gameplay HUD widget for run score and best score display."""

from __future__ import annotations

import pygame

from core.score import Score
from settings import ColorSettings, UiSettings


class Hud:
    """Draw run score indicators for the active play scene."""

    def __init__(
        self,
        score: Score,
        font: pygame.font.Font,
        leaderboard=None,
    ):
        """Initialize HUD dependencies.

        Args:
            score: The run-scoped score model for the current session.
            font: Font used for all HUD text.
            leaderboard: Optional leaderboard service exposing top().
        """
        self.score = score
        self.font = font
        self.leaderboard = leaderboard

    def _high_score_text(self) -> str:
        """Return the high-score line for the HUD center position."""
        if self.leaderboard is None:
            return f"{UiSettings.HIGH_SCORE_LABEL}-----"

        top_entries = self.leaderboard.top()
        if not top_entries:
            return f"{UiSettings.HIGH_SCORE_LABEL}-----"

        initials, score_value = top_entries[0]
        return f"{UiSettings.HIGH_SCORE_LABEL}{score_value:05d}  {initials}"

    def draw(self, screen: pygame.Surface) -> None:
        """Draw fish count, run score, and top score labels.

        Args:
            screen: The pygame surface to draw on.
        """
        padding = UiSettings.HUD_PADDING
        fish_text = f"FISH: {self.score.fish_eaten:02d}"
        score_text = f"SCORE: {self.score.total:05d}"
        high_score_text = self._high_score_text()

        fish_surface = self.font.render(fish_text, True, ColorSettings.WHITE)
        fish_rect = fish_surface.get_rect(topleft=(padding, padding))
        screen.blit(fish_surface, fish_rect)

        score_surface = self.font.render(score_text, True, ColorSettings.WHITE)
        score_rect = score_surface.get_rect(
            topright=(screen.get_width() - padding, padding)
        )
        screen.blit(score_surface, score_rect)

        high_score_surface = self.font.render(high_score_text, True, ColorSettings.WHITE)
        high_score_rect = high_score_surface.get_rect(
            midtop=(screen.get_width() // 2, padding)
        )
        screen.blit(high_score_surface, high_score_rect)
