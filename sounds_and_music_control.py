"""This module contains class AudioController which is responsible for all sounds and music in game"""

import pygame as pg


class AudioController:
    MUSIC_PATH: str = "assets/audio/music/"
    SOUNDS_PATH: str = "assets/audio/sounds/"

    def __init__(self) -> None:
        self.is_volume_on: int = True
        self.is_music_on: int = True

        self.sounds_dict: dict[str, pg.mixer.Sound] = {
            "change_button": pg.mixer.Sound(self.SOUNDS_PATH + "button_change.mp3"),
            "button_confirm": pg.mixer.Sound(self.SOUNDS_PATH + "button_confirm.mp3"),
            "shot": pg.mixer.Sound(self.SOUNDS_PATH + "shot_sound.mp3"),
            "explosion": pg.mixer.Sound(self.SOUNDS_PATH + "explosion.mp3"),
            "torpedo": pg.mixer.Sound(self.SOUNDS_PATH + "torpedo_launch.wav"),
            "particle": pg.mixer.Sound(self.SOUNDS_PATH + "particle_sound.wav"),
            "game_over": pg.mixer.Sound(self.SOUNDS_PATH + "game_over.wav"),
        }

        self.music_dict: dict[str, pg.mixer.Sound] = {
            "gameplay": pg.mixer.Sound(self.MUSIC_PATH + "main_theme.wav"),
            "menu": pg.mixer.Sound(self.MUSIC_PATH + "menu_theme.wav"),
        }
        self.current_music_name = None

    def flip_volume_status(self) -> None:
        self.is_volume_on = not self.is_volume_on

    def flip_music_status(self) -> None:
        self.is_music_on = not self.is_music_on
        if not self.is_music_on:
            self.music_dict[self.current_music_name].stop()
        else:
            self.music_dict[self.current_music_name].play(loops=-1)

    def play_sound(self, sound_name: str) -> None:
        if self.is_volume_on:
            self.sounds_dict[sound_name].play()

    def change_music(self, music_name: str) -> None:
        if self.current_music_name is not None:
            self.music_dict[self.current_music_name].stop()
        self.current_music_name: str = music_name
        if self.is_music_on:
            self.music_dict[self.current_music_name].play(loops=-1)
