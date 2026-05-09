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
    LIGHT_BLUE = (0, 255, 255)
    FOUNTAIN_BLUE = (102, 168, 176)
    DARK_TURQUOISE = (5, 195, 221) # AQUA BLUE

    # Retro fish palette — hand-picked to contrast against the aqua-to-navy background gradient.
    # Units: RGB 0-255.
    RETRO_CORAL = (255, 100, 80)       # warm salmon-red
    RETRO_MINT = (80, 220, 160)        # seafoam green
    RETRO_LAVENDER = (180, 130, 255)   # soft purple
    RETRO_PEACH = (255, 190, 80)       # warm amber
    RETRO_LIME = (130, 230, 60)        # chartreuse green
    RETRO_SKY = (80, 160, 255)         # cornflower blue
    FISH_PALETTE = [RETRO_CORAL, RETRO_MINT, RETRO_LAVENDER, RETRO_PEACH, RETRO_LIME, RETRO_SKY]

    # Ocean background gradient endpoints — blended top-to-bottom each frame.
    BG_COLOR_TOP = (60, 180, 210)      # sunlit aqua at the water surface
    BG_COLOR_BOTTOM = (10, 30, 70)     # deep navy at the ocean floor

    BG_COLOR = DARK_TURQUOISE

class ScreenSettings:
    """Class to hold all the settings related to the screen."""
    WIDTH = 1280
    HEIGHT = 720
    RESOLUTION = (WIDTH, HEIGHT)
    FPS = 60
    CRT_ALPHA_RANGE = (75, 90)
    CRT_SCANLINE_HEIGHT = 3
    TITLE = "Ms. Fishy"


class UiSettings:
    """UI text content and font-size settings for gameplay overlays."""

    GAME_OVER_TEXT = "GAME OVER"
    PAUSE_TEXT = "PAUSED"
    OVERLAY_FONT_SIZE = 52


class GameStateSettings:
    """Canonical state names for the game loop state machine."""

    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

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
    """Player-specific settings for movement, underwater physics, and appearance."""

    # Maximum speed the fish can reach on any single axis, in pixels per frame.
    # Increasing this makes top-end feel faster; decreasing it keeps the fish
    # feeling heavy and viscous in the water.
    MAX_SPEED = 3.0

    # Velocity added per frame (px/frame²) while a direction key is held.
    # Lower values = longer ramp-up (sluggish); higher = near-instant response.
    # At 60 FPS, 0.5 takes ~10 frames to reach MAX_SPEED from a standstill.
    ACCELERATION = 0.03

    # Velocity added per frame (px/frame²) when input directly opposes the
    # current travel direction (i.e. active braking / reversing).  Should be
    # noticeably higher than ACCELERATION so the player can fight their own
    # momentum and stop/reverse faster than passive drag alone would allow.
    COUNTER_ACCELERATION = 0.12

    # Fraction of velocity retained each frame when no input is given (0–1).
    # Models water resistance: 1.0 = frictionless coast, 0.0 = instant stop.
    # At 60 FPS, 0.88 brings a full-speed fish to near-zero in ~35 frames (~0.6 s).
    DRAG = 0.95

    # Velocity magnitude (px/frame) below which the fish snaps to a full stop.
    # Prevents imperceptible infinite drift from DRAG's geometric decay.
    STOP_THRESHOLD = 0.03

    # Velocity magnitude (px/frame) the fish must exceed before the sprite is
    # allowed to flip direction. Prevents the fish from flickering left/right
    # while coasting to a stop after the player releases a key.
    FLIP_THRESHOLD = 0.1

    SIZE = (16, 16)
    # Body gradient: bright yellow dorsal side fading to warm orange belly; units: RGB 0-255.
    COLOR_TOP = (255, 240, 60)         # bright yellow — dorsal (top of body)
    COLOR_BOTTOM = (255, 130, 0)       # warm orange — belly (bottom of body)
    # Fraction of the eaten fish's size added to the player on each eat.
    PLAYER_GROWTH_COEFFICIENT = 0.05

    # ------------------------------------------------------------------
    # MS. FISHY BOW
    # ------------------------------------------------------------------
    # The player wears a small pink bow above the body's top apex — two
    # mirrored triangles (▷◁) meeting at a central point, scaled relative
    # to fish size so the bow grows with the fish.

    # Total bow width as a fraction of fish size (sum of both triangles).
    BOW_WIDTH_RATIO = 0.55
    # Bow vertical extent as a fraction of fish size.
    BOW_HEIGHT_RATIO = 0.40
    # Vertical gap between the bow's bottom edge and the body's top apex,
    # as a fraction of fish size. Keeps the bow visually "floating" above.
    BOW_GAP_RATIO = 0.075
    # Bow color in RGB 0-255 — hot pink to read clearly against the ocean.
    BOW_COLOR = (255, 105, 180)

class FishSettings:
    """Settings related to the fish enemies."""

    # NOTE: MAX_SIZE must be less than ScreenSettings.HEIGHT (720).
    # If MAX_SIZE >= 720, the spawn logic in sprites.py will pass a 
    # negative range to random.randint(), causing a ValueError.

    SPAWN_RATE = ScreenSettings.FPS // 5 # Frames between spawns
    MIN_SIZE = 8
    MAX_SIZE = ScreenSettings.HEIGHT // 2
    MIN_SPEED = 0.2
    MAX_SPEED = 2

    # Fish body height as a fraction of size; values < 1 flatten the fish vertically.
    BODY_HEIGHT_RATIO = 0.5
    # Fish tail width as a fraction of size.
    TAIL_WIDTH_RATIO = 0.33
    # Fish eye side length as a fraction of fish size.
    EYE_SIZE_RATIO = 0.12
    # Eye horizontal offset from the nose toward the tail-start, as fraction of size.
    EYE_NOSE_OFFSET_RATIO = 0.25
    # Pixel offset for the drop shadow rendered behind every fish; adds perceived depth.
    SHADOW_OFFSET = 2

class FontSettings:
    """Font files, sizes, and text-color mappings for UI rendering."""

    FONT = os.path.join(
        os.path.dirname(__file__), 'assets', 'font', 'Pixeled.ttf'
    )

class AssetPaths:
    """Class to hold all the file paths for assets."""
    # __file__-relative so the project runs no matter the working directory
    # (e.g. when launched from the arcade cabinet launcher).
    BASE_DIR = os.path.dirname(__file__)
    ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
    AUDIO_DIR = os.path.join(ASSETS_DIR, 'audio')
    MUSIC_DIR = os.path.join(AUDIO_DIR, 'music')
    SOUND_DIR = os.path.join(AUDIO_DIR, 'sound')

    TV = os.path.join(
        ASSETS_DIR, 'graphics', 'effects', 'tv.png'
    )


class AudioSettings:
    """Global audio toggles, mixer-level defaults, and the sound/music registry.

    To add a new sound effect: drop the file in assets/audio/sound/ and add a
    line to SOUND_EFFECTS keyed by the logical name used at the call site
    (e.g. ``self.audio.play("gulp")``). To add a new background track: append
    its path to MUSIC_TRACKS.
    """

    MUTE = False
    MUTE_MUSIC = False  # Keep music disabled while retaining sound effects.
    MUSIC_VOLUME = 1.0  # Background music volume in the range [0.0, 1.0].
    SFX_VOLUME = 1.0    # Default playback volume for all sound effects.

    # Logical sound name -> file path. The key is what gameplay code passes
    # to AudioManager.play(). Keep names short and game-action-oriented.
    SOUND_EFFECTS = {
        "pause_in":  os.path.join(AssetPaths.SOUND_DIR, 'sfx_sounds_pause2_in.ogg'),
        "pause_out": os.path.join(AssetPaths.SOUND_DIR, 'sfx_sounds_pause2_out.ogg'),
        "gulp":      os.path.join(AssetPaths.SOUND_DIR, 'gulp.ogg'),
        "scream":    os.path.join(AssetPaths.SOUND_DIR, 'game_over.ogg'),
    }

    # Background music pool; one is chosen at random each time music starts,
    # avoiding back-to-back repeats of the same track.
    MUSIC_TRACKS = [
        os.path.join(AssetPaths.MUSIC_DIR, '8bit-aquarium.mp3'),
    ]

class DebugSettings:
    """Settings related to debugging features."""