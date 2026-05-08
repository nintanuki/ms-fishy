import os

class ColorSettings:
    """Class to hold all the color settings for the game."""
    BLACK = (0, 0, 0)
    NERO = (30, 30, 30)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)

    BG_COLOR = BLUE
    OVERLAY_BACKGROUND = WHITE

class ScreenSettings:
    """Class to hold all the settings related to the screen."""
    WIDTH = 1280
    HEIGHT = 720
    RESOLUTION = (WIDTH, HEIGHT)
    FPS = 60
    CRT_ALPHA_RANGE = (75, 90)
    CRT_SCANLINE_HEIGHT = 3
    TITLE = "Pygame Template"  # Replace with your project's name.

class InputSettings:
    """Controller button and axis mappings used by gameplay and menus.

    Constants are named after the physical button on the controller, not the
    action it performs. The only exception is JOY_BUTTON_QUIT_COMBO, which is
    a special multi-button chord rather than a single button.
    """

    JOY_BUTTON_A = 0
    JOY_BUTTON_B = 1
    JOY_BUTTON_X = 2
    JOY_BUTTON_Y = 3
    JOY_BUTTON_L1 = 4
    JOY_BUTTON_R1 = 5
    JOY_BUTTON_BACK = 6
    JOY_BUTTON_START = 7
    JOY_BUTTON_QUIT_COMBO = (7, 6, 4, 5)

    JOY_AXIS_LEFT_X = 0
    JOY_AXIS_LEFT_Y = 1
    JOY_AXIS_L2 = 4
    JOY_AXIS_R2 = 5
    JOY_TRIGGER_THRESHOLD = 0.5

class PlayerSettings:
    """Player-specific settings like movement speed."""
    SPEED = 5
    SIZE = (50, 50)

# Add this to settings.py

class FishSettings:
    SPAWN_RATE = 60  # Frames between spawns (approx 1 sec at 60 FPS)
    MIN_SIZE = 10
    MAX_SIZE = 100
    MIN_SPEED = 2
    MAX_SPEED = 5
    PLAYER_GROWTH_RATE = 2 # Pixels added to width/height per "eat"

class FontSettings:
    """Font files, sizes, and text-color mappings for UI rendering."""

    FONT = os.path.join(
        os.path.dirname(__file__), 'assets', 'font', 'Pixeled.ttf'
    )

class AudioSettings:
    """Global audio toggles and mixer-level defaults."""

    MUTE = False
    MUTE_MUSIC = False  # Keep music disabled while retaining sound effects.
    MUSIC_VOLUME = 1  # Background music volume in the range [0.0, 1.0].

class AssetPaths:
    """Class to hold all the file paths for assets."""
    # __file__-relative so the project runs no matter the working directory
    # (e.g. when launched from the arcade cabinet launcher).
    BASE_DIR = os.path.dirname(__file__)
    ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
    AUDIO_DIR = os.path.join(ASSETS_DIR, 'audio')
    MUSIC_DIR = os.path.join(AUDIO_DIR, 'music')

    TV = os.path.join(
        ASSETS_DIR, 'graphics', 'effects', 'tv.png'
    )

    # # Music
    # BACKGROUND_MUSIC = os.path.join(
    #     MUSIC_DIR, 'aquarium.mp3'
    # )

    # Music
    NORMAL_MUSIC_TRACKS = [
        os.path.join(MUSIC_DIR, 'aquarium.mp3'),
    ]
    MUSIC_TRACKS = NORMAL_MUSIC_TRACKS

class DebugSettings:
    """Settings related to debugging features."""