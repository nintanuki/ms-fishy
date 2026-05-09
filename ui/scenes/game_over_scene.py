"""Scene for game-over state."""

from __future__ import annotations

import pygame

from core.scene import Scene
from core.score import Score
from settings import ColorSettings, InputSettings, ScreenSettings, UiSettings
from utils.text import draw_centered_text


class GameOverScene(Scene):
    """Scene displayed when the player is eaten by a larger fish."""

    def __init__(self, game, score: Score | None = None):
        """Initialize the game-over scene.
        
        Args:
            game: The GameManager instance that owns this scene.
            score: Score from the run that just ended.
        """
        super().__init__(game)
        self.score = score

    def on_enter(self) -> None:
        """Called when entering this scene from another scene."""
        pass

    def on_exit(self) -> None:
        """Called when leaving this scene."""
        pass

    def handle_event(self, event: pygame.event.EventType) -> None:
        """Handle input events for the game-over scene.
        
        Args:
            event: The pygame event to process.
        """
        # Note: global events (Esc, F11, BACK, quit-combo) are handled
        # by GameManager and never reach here.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._restart()
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == InputSettings.JOY_BUTTON_START:
                self._restart()

    def _restart(self) -> None:
        """Restart the game by transitioning to a fresh PlayScene."""
        from ui.scenes.play_scene import PlayScene
        self.game.scenes.change_to(PlayScene(self.game))

    def update(self) -> None:
        """Game-over scene does not update anything."""
        pass

    def render(self, screen: pygame.Surface) -> None:
        """Draw the game-over screen to the screen.
        
        Args:
            screen: The pygame surface to draw to.
        """
        screen.fill(ColorSettings.BLACK)
        draw_centered_text(
            surface=screen,
            text=UiSettings.GAME_OVER_TEXT,
            font=self.game.overlay_font,
            color=ColorSettings.WHITE,
            center=(ScreenSettings.WIDTH // 2, ScreenSettings.HEIGHT // 2),
        )
