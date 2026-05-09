"""Scene for game-over state."""

from __future__ import annotations

import pygame

from core.scene import Scene
from core.score import Score
from settings import InputSettings


class GameOverScene(Scene):
    """Routing scene that dispatches to InitialsEntryScene or LeaderboardScene.

    Music stop and scream SFX are handled by PlayScene before transitioning
    here. This scene's only job is to check whether the run qualifies for
    the leaderboard and immediately change to the appropriate next scene.
    """

    def __init__(self, game, score: Score | None = None):
        """Initialize the game-over routing scene.

        Args:
            game: The GameManager instance that owns this scene.
            score: Score from the run that just ended.
        """
        super().__init__(game)
        self.score = score

    def on_enter(self) -> None:
        """Route immediately to InitialsEntryScene or LeaderboardScene."""
        if self.score is not None and self.game.leaderboard.qualifies(self.score.total):
            from ui.scenes.initials_entry_scene import InitialsEntryScene
            self.game.scenes.change_to(InitialsEntryScene(self.game, self.score))
        else:
            from ui.scenes.leaderboard_scene import LeaderboardScene
            self.game.scenes.change_to(LeaderboardScene(self.game, self.score))

    def on_exit(self) -> None:
        """Called when leaving this scene."""
        pass

    def handle_event(self, event: pygame.event.EventType) -> None:
        """No events are processed here; the scene transitions in on_enter.

        Args:
            event: The pygame event to process.
        """
        pass

    def update(self) -> None:
        """Game-over routing scene does not update anything."""
        pass

    def render(self, screen: pygame.Surface) -> None:
        """Game-over routing scene renders nothing; it exits in on_enter.

        Args:
            screen: The pygame surface to draw to.
        """
        pass

