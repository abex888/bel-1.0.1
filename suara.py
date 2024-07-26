import pygame.mixer

def init_mixer():
    """Initializes the pygame mixer if not already done."""
    pygame.mixer.init()

def play_sound(sound_file):
    """Loads and plays a sound from the specified file."""
    pygame.mixer.init()
    if not pygame.mixer.music.get_busy():
        init_mixer()  # Ensure mixer is initialized
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

# Function calls for specific sounds
suara_masuk = lambda: play_sound("masuk.mp3")
suara_pulang = lambda: play_sound("pulang.mp3")
suara_istirahat = lambda: play_sound("istirahat.mp3")
suara_upacara = lambda: play_sound("upacara.mp3")
suara_kumpul = lambda: play_sound("kumpul.mp3")
