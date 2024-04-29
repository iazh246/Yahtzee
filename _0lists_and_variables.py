import pygame

root_width = 1920 // 2
root_height = 1080 // 2

dice =[]
dice_labels = []

players = []
player_scorecards = []
c2_player_scorecards = []

buttons = []
c2_buttons = []

score_labels = {}
categories_stage1 = [
    ("Ones", 5), 
    ("Twos", 10), 
    ("Threes", 15), 
    ("Fours", 20), 
    ("Fives", 25), 
    ("Sixes", 30)
]

categories_stage2 = [
    ("3K", 30),
    ("4K", 40),
    ("Full House", 25),
    ("S.Straight", 30),
    ("L.Straight", 40),
    ("Yatzy", 50),
    ("Chance", 30)
]

debug = True

player_turn = None
rerolled_dice = 3

game_started = False
stage_2_activated = False
game_ended = False

dice_roll_sound = pygame.mixer.Sound("sound_effects/dice_roll_sound.mp3")







