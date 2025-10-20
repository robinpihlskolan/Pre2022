import pygame

class GameSounds:
    def __init__(self):
        pygame.mixer.init()
        try:
            self.normal_jump_sound = pygame.mixer.Sound('./sounds/effect/normal_jump.mp3')
            self.spring_jump_sound = pygame.mixer.Sound('./sounds/effect/spring_jump.mp3')
            self.red_platform_sound = pygame.mixer.Sound('./sounds/effect/red_platform.mp3')
        except Exception as e:
            print(f"Error loading sounds: {e}")
            self.normal_jump_sound = pygame.mixer.Sound(buffer=pygame.sndarray.make_sound(pygame.sndarray.array([0, 0])))
            self.spring_jump_sound = pygame.mixer.Sound(buffer=pygame.sndarray.make_sound(pygame.sndarray.array([0, 0])))
            self.red_platform_sound = pygame.mixer.Sound(buffer=pygame.sndarray.make_sound(pygame.sndarray.array([0, 0])))

    def play_normal_jump(self):
        self.normal_jump_sound.play()

    def play_spring_jump(self):
        self.spring_jump_sound.play()

    def play_red_platform(self):
        self.red_platform_sound.play()
