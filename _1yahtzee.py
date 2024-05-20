# ---------------------------- imports -------------------------------------------------------------------------------- #

import customtkinter as ctk
from customtkinter import *

import tkinter as tk
from tkinter import ttk
from tkinter import *

from PIL import Image, ImageTk

import random, pygame, time
pygame.init()

from _0fonts_and_colors import *
from _0lists_and_variables import *

# ---------------------------- functions -------------------------------------------------------------------------------- #

def determine_winner():
    winner_screen()

def popup_message(message):
    try:
        error_frame = ctk.CTkFrame(main_root, border_width=2, border_color='white', fg_color=main_color, corner_radius=0)
        error_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        error_label = ctk.CTkLabel(error_frame, text=message, font=standard_font, corner_radius=0)
        error_label.pack(expand=True, padx=20, pady=20)

        ok_button = ctk.CTkButton(error_frame, text="Click to dismiss", corner_radius=0, fg_color=dark_accent_color, hover_color=light_accent_color)
        ok_button.configure(command=lambda: hide_error(None))
        ok_button.pack(expand=True, pady=10)

        def hide_error(event):
            error_frame.place_forget()
    except NameError:
        print("Error frame not found. Creating new error frame.")
        
        error_root = ctk.CTk()
        error_root.title('Important Message')
        
        error_root.propagate(True)
        error_root.resizable(False, False)
        error_root.eval('tk::PlaceWindow . center')
                
        outer_error_frame = ctk.CTkFrame(error_root, corner_radius=0, fg_color='white')
        outer_error_frame.pack(fill='both', expand=True)
        
        error_frame = ctk.CTkFrame(outer_error_frame, corner_radius=0, fg_color=main_color)
        error_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        error_label = ctk.CTkLabel(error_frame, text=message, font=standard_font, corner_radius=0)
        error_label.pack(expand=True, padx=20, pady=20)

        ok_button = ctk.CTkButton(error_frame, text="Click to dismiss", corner_radius=0, fg_color=dark_accent_color, hover_color=light_accent_color)
        ok_button.configure(command=lambda: hide_error(None))
        ok_button.pack(expand=True, pady=10)

        def hide_error(event):
            error_root.quit
        
        error_root.mainloop()

def stage_2():
    global stage_2_activated
    stage_2_activated = True
    
    reset_gamefunc()
    
    for player in players:
        if player['score'] >= 63:
            player['score'] += 35
            popup_message(f"{player['name']} has scored a bonus of 35 points for having 63 or more points in the stage 1.")
    
    for i in range(len(buttons)):
        buttons[i].configure(state='disabled')
    
    for i in range(len(c2_buttons)):
        c2_buttons[i].configure(state='normal')

# rule functions

def cross_category(category):    
    global complete_sound
    
    click_sound.play()
    
    if not stage_2_activated:
        if category not in players[player_turn]['categories_stage1_used']:
            players[player_turn]['categories_stage1_used'].add(category)
            player_scorecards[player_turn][category] = '-----'

            for i, button in enumerate(buttons):
                button.configure(command=lambda c=i: check_input(categories_stage1[c][0]), fg_color=main_color)
    
                scorecard_update()
                remove_button.configure(state='disabled')
        else:
            popup_message(f"Category '{category}' has already been used.")
    else:
        if category not in players[player_turn]['categories_stage2_used']:
            players[player_turn]['categories_stage2_used'].add(category)
            c2_player_scorecards[player_turn][category] = '-----'

            for i, button in enumerate(c2_buttons):
                button.configure(command=lambda c=i: check_input(categories_stage2[c][0]), fg_color=main_color)
                
                scorecard_update()
                remove_button.configure(state='disabled')
        else:
            popup_message(f"Category '{category}' has already been used.")
    
    def next_turn():
        complete_sound.play()
        
        if not stage_2_activated:
            if all(len(player['categories_stage2_used']) == len(categories_stage2) for player in players):
                popup_message("Game has ended! All categories in stage 2 have been filled.")
                continue_button_scorecard.destroy()
                determine_winner()  
            elif all(len(player['categories_stage1_used']) == len(categories_stage1) for player in players):
                popup_message("Halftime! All of stage 1 have been filled, proceeding to stage 2.")
                continue_button_scorecard.destroy()
                stage_2()
            else:
                popup_message(f"{players[player_turn]['name']} removed the category '{category}'.\nIt is now the next players turn.")
                continue_button_scorecard.destroy()
                remove_button.configure(state='normal')
                determine_turn()
        else:
            if all(len(player['categories_stage2_used']) == len(categories_stage2) for player in players):
                popup_message("Game has ended! All categories in stage 2 have been filled.")
                continue_button_scorecard.destroy()
                determine_winner()  
            else:
                popup_message(f"{players[player_turn]['name']} removed the category '{category}'.\nIt is now the next players turn.")
                continue_button_scorecard.destroy()
                remove_button.configure(state='normal')
                determine_turn()

    continue_button_scorecard = ctk.CTkButton(master=side_bar, text="Pass Turn", font=standard_font, fg_color=dark_accent_color, corner_radius=0, hover_color=light_accent_color, command=next_turn)
    continue_button_scorecard.pack(side="top", pady=20)
    continue_button_scorecard.propagate(False)
    
    scorecard_update()

    for indv_buttons in buttons and c2_buttons:
        indv_buttons.configure(state='disabled')

def check_input(chosen_category):
    global player_turn, players, score_labels, buttons, c2_buttons, complete_sound

    click_sound.play()
    chosen_category2 = chosen_category

    category_to_number = {
        "Ones": 1,
        "Twos": 2,
        "Threes": 3,
        "Fours": 4,
        "Fives": 5,
        "Sixes": 6
    }
    
    score = 0
    
    if not stage_2_activated:
        if chosen_category in players[player_turn]['categories_stage1_used']:
            popup_message("Category already filled. Please select another category.")
            return
        if chosen_category not in [chosen_category for chosen_category, _ in categories_stage1]:
            popup_message("Invalid category. Please select a valid category.")
            return
    else:
        if chosen_category in players[player_turn]['categories_stage2_used']:
            popup_message("Category already filled. Please select another category.")
            return
        if chosen_category not in [chosen_category for chosen_category, _ in categories_stage2]:
            popup_message("Invalid category. Please select a valid category.")
            return
    
    if chosen_category in category_to_number and not any(die == category_to_number[chosen_category] for die in dice):
        popup_message(f"No {chosen_category2.lower()} found. Please select another category.")
        return

    if chosen_category in category_to_number:
        score = sum(die == category_to_number[chosen_category] for die in dice) * category_to_number[chosen_category]

    else:
        conditions = {
            "3K": lambda dice: any(dice.count(die) >= 3 for die in set(dice)),
            "4K": lambda dice: any(dice.count(die) >= 4 for die in set(dice)),
            "Full House": lambda dice: any(dice.count(die) == 3 for die in set(dice)) and any(dice.count(die) == 2 for die in set(dice)),
            "S.Straight": lambda dice: any(sorted(dice) == list(range(start, start + 4)) for start in range(1, 7) if start + 3 <= 6),
            "L.Straight": lambda dice: any(sorted(dice) == list(range(start, start + 5)) for start in range(1, 7) if start + 4 <= 6),
            "Yatzy": lambda dice: dice.count(dice[0]) == 5,
            "Chance": lambda dice: True
        }
        
        if not conditions[chosen_category](dice):
            popup_message(f"No valid {chosen_category2} found. Please select another category.")
            return

    if chosen_category in ["3K", "4K", "Chance"]:
        score = sum(dice)
    elif chosen_category == "Full House":
        score = 25  
    elif chosen_category == "S.Straight":
        score = 30  
    elif chosen_category == "L.Straight":
        score = 40  
    elif chosen_category == "Yatzy":
        score = 50  
    
    if not stage_2_activated:
        players[player_turn]['score'] += score
        player_scorecards[player_turn][chosen_category] = score
        players[player_turn]['categories_stage1_used'].add(chosen_category)
    else:
        players[player_turn]['categories_stage2_used'].add(chosen_category)
        c2_player_scorecards[player_turn][chosen_category] = score
        
    def next_turn(chosen_category2):
        print(f"Debug: chosen_category after next_turn = {chosen_category}")
        complete_sound.play()

        if not stage_2_activated:
            if all(len(player['categories_stage2_used']) == len(categories_stage2) for player in players):
                popup_message("Game has ended! All categories in stage 2 have been filled.")
                continue_button_scorecard.destroy()
                determine_winner()
            elif all(len(player['categories_stage1_used']) == len(categories_stage1) for player in players):
                popup_message("Halftime! All of stage 1 have been filled, proceeding to stage 2.")
                continue_button_scorecard.destroy()
                stage_2()
            else:
                popup_message(f"{players[player_turn]['name']} scored {score} points in the {chosen_category2} category!\nIt is now the next players turn.")
                continue_button_scorecard.destroy()
                determine_turn()
        else:
            if all(len(player['categories_stage2_used']) == len(categories_stage2) for player in players):
                popup_message("Game has ended! All categories in stage 2 have been filled.")
                continue_button_scorecard.destroy()
                determine_winner()
            else:
                popup_message(f"{players[player_turn]['name']} scored {score} points in the {chosen_category2} category!\nIt is now the next players turn.")
                continue_button_scorecard.destroy()
                determine_turn()

    continue_button_scorecard = ctk.CTkButton(master=side_bar, text="Pass Turn", font=standard_font, fg_color=dark_accent_color, corner_radius=0, hover_color=light_accent_color, command=lambda: next_turn(chosen_category2))
    continue_button_scorecard.pack(side="top", pady=20)
    scorecard_update()

    for i, (chosen_category) in enumerate(categories_stage1, start=1):
        buttons[i-1].configure(state='disabled')
    for i, (chosen_category) in enumerate(categories_stage2, start=len(categories_stage1)+2):
        c2_buttons[i-len(categories_stage1)-2].configure(state='disabled')
    
# important game functions

def sort_dice():
    global dice, dice_labels
    dice = sorted(dice)
    
    for i, die in enumerate(dice):
        dice_labels[i].configure(image=images[die-1])
    
def roll_dice():
    global dice, dice_labels
        
    roll_button.configure(state='disabled')
    dice = [random.randint(1, 6) for _ in range(5)]
    
    for i, die in enumerate(dice):
        dice_labels[i].configure(image=images[die-1])
    
    dice_roll_sound.play()

def reroll_dice():
    global rerolled_dice, dice, images

    if input_box.get() == "":
        if rerolled_dice == 0:
            determine_turn()
            return
        return

    try:
        dice_indexes = [int(index) - 1 for index in input_box.get().split(',')]
    except ValueError:
        popup_message("Invalid Input:\nRefer to the info hover for correct valid input.")
        return
    
    for index in dice_indexes:
        if 0 <= index < len(dice):
            dice[index] = random.randint(1, 6)
        else:
            popup_message("Invalid Input:\nRefer to the info hover for correct valid input.")
            return
        
    rerolled_dice -= 1  # Decrement the counter
    
    for i, die in enumerate(dice):
        dice_labels[i].configure(image=images[die-1])
    
    dice_roll_sound.play()
    
    remaining_reroll.configure(text=f"Remaining rerolls: {rerolled_dice}")
    
    if rerolled_dice == 0:
        reroll_button.configure(state='disabled') 

def remove_category():
    if not stage_2_activated:
        for i, button in enumerate(buttons):
            if button.cget('fg_color') == REMOVE_COLOR:
                button.configure(command=lambda c=i: check_input(categories_stage1[c][0]), fg_color=main_color)
            else:
                button.configure(fg_color=REMOVE_COLOR)
                button.configure(command=lambda c=i: cross_category(categories_stage1[c][0]))
    else:
        for i, button in enumerate(c2_buttons):
            if button.cget('fg_color') == REMOVE_COLOR:
                button.configure(command=lambda c=i: check_input(categories_stage2[c][0]), fg_color=main_color)
            else:
                button.configure(fg_color=REMOVE_COLOR)
                button.configure(command=lambda c=i: cross_category(categories_stage2[c][0]))

def determine_turn():
    global player_turn, players, turn_indicator, game_started

    valid_players = [index for index, player in enumerate(players) if player is not None]

    if player_turn is None:
        player_turn = valid_players[0]    
    else:
        current_index = valid_players.index(player_turn)
        next_index = (current_index + 1) % len(valid_players)
        player_turn = valid_players[next_index]
    
    player_name = players[player_turn]['name']
    if player_name.endswith('s'):
        turn_indicator.configure(text=f"{player_name}' turn")
    else:
        turn_indicator.configure(text=f"{player_name}'s turn")
    
    if game_started:
        reset_gamefunc()
    
def reset_gamefunc():
    global players, player_turn, rerolled_dice, dice, dice_labels

    scorecard_update()

    if not stage_2_activated:
        for indv_buttons in buttons:
            indv_buttons.configure(state='normal')
    else:
        for indv_buttons in c2_buttons:
            indv_buttons.configure(state='normal')

    roll_button.configure(state='normal')
    dice.clear()

    reroll_button.configure(state='normal')
    remaining_reroll.configure(text=f"Remaining rerolls: 3")
    rerolled_dice = 3

    for i in range(5):
        dice_labels[i].configure(image='')

def scorecard_update():
    global c2_player_scorecards, player_scorecards, player_turn, score_labels

    for category, _ in categories_stage1:
        score_labels[category].configure(text=player_scorecards[player_turn][category])
    for category, _ in categories_stage2:
        score_labels[category].configure(text=c2_player_scorecards[player_turn][category])

# registration functions

def register_complete():    
    global game_started
    
    if len(players) < 2:
        popup_message("No players or only 1 was registered. Please register at least two players.")
        return show_reg()

    for _ in range(len(players)):
        player_scorecards.append({
            'Ones': 0,
            'Twos': 0,
            'Threes': 0,
            'Fours': 0,
            'Fives': 0,
            'Sixes': 0
        })
        
    for _ in range(len(players)):
        c2_player_scorecards.append({
            '3K': 0,
            '4K': 0,
            'Full House': 0,
            'S.Straight': 0,
            'L.Straight': 0,
            'Yatzy': 0,
            'Chance': 0
        })
        
    hide_reg()
    game_started = True
    main()

def player_list_update():
    for widget in player_list.winfo_children():
        widget.destroy()

    for index, player in enumerate(players, start=1):
        player_frame = ctk.CTkFrame(player_list)
        player_frame.pack(fill='x', pady=5, padx=5)
        
        label = ctk.CTkLabel(player_frame, text=f"{index}. {player['name']}", font=standard_font)
        label.pack(side='left', padx=10)
        
        remove_button = ctk.CTkButton(player_frame, text="-", corner_radius=0, fg_color=main_color, hover_color=highlight_color, width=40,
                                      command=lambda player=player: remove_player(player))
        remove_button.pack(side='right', padx=10)

def add_player():
    player_name = name_entry.get().capitalize().strip()
    if player_name and len(players) < 4 and len(player_name) <= 8:
        players.append({'name': player_name, 'score': 0, 'categories_stage1_used': set(), 'categories_stage2_used': set()})
        name_entry.delete(0, tk.END)
        player_list_update()
        if len(players) == 4:
            add_button['state'] = 'disabled'
    else:
        popup_message("Invalid Input:\nName must be 8 characters or fewer.\nRefer to the info hover for correct valid input.")

def remove_player(player):
    if player in players:
        players.remove(player)
        player_list_update()
        if len(players) < 4:
            add_button.configure(state='normal')

# gui initialization functions

def show_main_frame():
    yahtzee_label.pack_forget()
    
    inner_root.pack(padx=0, pady=0, fill='both', expand=True)
    side_bar.pack(side="left", fill="y")
    turn_indicator.pack(side="top", fill="x")
    scorecard.pack(anchor='n', expand=True)
    
    for i, (category, max_score) in enumerate(categories_stage1, start=1):
        score_labels[category].grid(row=i, column=2, padx=10)
        buttons[i-1].grid(row=i, column=3, padx=10)
    
    for i, (category, max_score) in enumerate(categories_stage2, start=len(categories_stage1)+2):
        score_labels[category].grid(row=i, column=2, padx=10)
        c2_buttons[i-len(categories_stage1)-2].grid(row=i, column=3, padx=10)
    
    top_bar.pack(side="top", fill="x")
    roll_sort_frame.pack(side="left", padx=12)
    roll_button.pack(side='top', pady=10)
    sort_button.pack(side='bottom', pady=10)
    initialize_dices()
    under_bar.pack(side="top", fill="x")
    reroll_button.pack(side="left", expand=True)
    input_box.pack(side="left", expand=True, fill="x", padx=10)
    input_info_box.pack(side="left", expand=True)
    remaining_reroll.pack(side="right", expand=True, fill="x", padx=10)

def hide_main_frame():
    inner_root.pack_forget()
    side_bar.pack_forget()
    turn_indicator.pack_forget()
    scorecard.pack_forget()
    
    for i, (category, max_score) in enumerate(categories_stage1, start=1):
        score_labels[category].grid_forget()
        buttons[i-1].grid_forget()
    
    for i, (category, max_score) in enumerate(categories_stage2, start=len(categories_stage1)+2):
        score_labels[category].grid_forget()
        c2_buttons[i-len(categories_stage1)-2].grid_forget()
    
    top_bar.pack_forget()
    roll_sort_frame.pack_forget()
    roll_button.pack_forget()
    sort_button.pack_forget()
    for label in dice_labels:
        label.pack_forget()
    under_bar.pack_forget()
    reroll_button.pack_forget()
    input_box.pack_forget()
    input_info_box.pack_forget()
    remaining_reroll.pack_forget()

def show_reg():
    startbutton.pack_forget()
    button_frame.pack_forget()
    optionsbutton.pack_forget()
    quitbutton.pack_forget()
        
    outer_register_root.place(relx=0.5, rely=0.5, anchor="center")
    register_root.pack(fill='both', expand=True, padx=2, pady=2)
    name_entry.pack(pady=10)
    add_button.pack(pady=5)
    player_list.pack(pady=10, fill='both', expand=True)
    back_button.pack(side='left', padx=10, pady=10, fill='x')
    reg_info_box.pack(side="left", padx=10, pady=10)
    continue_button.pack(side='right', padx=10, pady=10)

def start_game():
    click_sound.play()
    show_reg()

def hide_reg():    
    outer_register_root.place_forget()
    register_root.place_forget()
    name_entry.pack_forget()
    add_button.pack_forget()
    player_list.pack_forget()
    reg_info_box.pack_forget()
    continue_button.pack_forget()
    back_button.pack_forget()
        
def back_button_activated():
    click_sound.play()
    button_frame.pack(pady=20, padx=20, anchor='nw')
    startbutton.pack(pady=20, padx=20, side='top', anchor='w', fill='x', expand=True)
    optionsbutton.pack(pady=20, padx=20,side='top', anchor='w', fill='x', expand=True)
    quitbutton.pack(pady=20, padx=20, side='top', anchor='w', fill='x', expand=True)
    hide_reg()
    
def quit_game():
    click_sound.play()
    time.sleep(0.5)
    main_root.quit()

# winnner screen

def winner_screen():    
    hide_main_frame()
    
    if len(players) < 4:
        for _ in range(4 - len(players)):
            players.append({'name': 'N/A', 'score': 0})
    
    winners = sorted(players, key=lambda x: x['score'], reverse=True)
    winners.extend([None] * (4 - len(winners)))
    
    player_1 = winners[0]
    player_2 = winners[1]
    player_3 = winners[2]
    player_4 = winners[3]

    winner_name = player_1['name']
    
    winner_frame = ctk.CTkFrame(main_root, corner_radius=0, fg_color=main_color)
    winner_frame.pack(fill="both", expand=True)

    colors = ['#404040', '#454545', '#505050', '#555555']

    podium_sizes = [(100, 180), (100, 240), (100, 300), (100, 120)]

    total_width = sum(size[0] for size in podium_sizes)
    start_x = (root_width - total_width) / 2

    bottom_align = (root_height - podium_sizes[2][1]) * 2

    ctk.CTkLabel(master=winner_frame, text=f'Congratulations, {winner_name} has won!', font=h1_cursive_font).place(x=root_width/2, y=50, anchor='n')

    for i, size in enumerate(podium_sizes):
        x_position = start_x + i*size[0]
        podium = ctk.CTkFrame(master=winner_frame, width=size[0], height=size[1], corner_radius=0, fg_color=colors[3 - i])
        podium.place(x=x_position, y=bottom_align, anchor='sw')


    player_label = [
        f"{player_3['name']}\nscore: {player_3['score']}",
        f"{player_2['name']}\nscore: {player_2['score']}",
        f"{player_1['name']}\nscore: {player_1['score']}",
        f"{player_4['name']}\nscore: {player_4['score']}"
    ]  # Player labels corresponding to their podium place
    place_labels = ['3rd', '2nd', '1st', '4th']


    for i, (size, label) in enumerate(zip(podium_sizes, place_labels)):
        x_position = start_x + i*size[0]

        podium = ctk.CTkFrame(master=winner_frame, width=size[0], height=size[1], corner_radius=0, fg_color=colors[3 - i])
        podium.place(x=x_position, y=bottom_align, anchor='sw')

        label_below = ctk.CTkLabel(master=winner_frame, text=label, font=standard_font)
        label_below.place(x=x_position + size[0]/2, y=bottom_align + 40, anchor='s')

        label_above = ctk.CTkLabel(master=winner_frame, text=player_label[i], font=standard_font)
        label_above.place(x=x_position + size[0]/2, y=bottom_align - size[1] - 20, anchor='s')
        
    def restart_game():
        click_sound.play()
        winner_frame.destroy()
        complete_reset_gamefunc()
        
        click_sound.play()
        yahtzee_label.pack(pady=20, padx=20, anchor='nw')
        button_frame.pack(pady=20, padx=20, anchor='nw')
        startbutton.pack(pady=20, padx=20, side='top', anchor='w', fill='x', expand=True)
        optionsbutton.pack(pady=20, padx=20,side='top', anchor='w', fill='x', expand=True)
        quitbutton.pack(pady=20, padx=20, side='top', anchor='w', fill='x', expand=True)
    
    restart_button = ctk.CTkButton(master=winner_frame, text="Restart Game", corner_radius=0, fg_color=dark_accent_color, hover_color=light_accent_color, command=restart_game)
    restart_button.place(anchor='se', x=root_width-20, y=root_height-20)
    restart_button.configure(state='disabled')
    
def complete_reset_gamefunc():
    global players, player_turn, rerolled_dice, dice, dice_labels, stage_2_activated, game_started, player_scorecards, c2_player_scorecards, buttons, c2_buttons, score_labels

    dice =[]
    dice_labels = []

    players = []
    player_scorecards = []
    c2_player_scorecards = []

    buttons = []
    c2_buttons = []

    score_labels = {}

    player_turn = None
    rerolled_dice = 3

    game_started = False
    stage_2_activated = False
    
    player_list_update()

# ---------------------------- start screen -------------------------------------------------------------------------------- #

main_root = ctk.CTk()
main_root.title("Yahtzee | have fun !") 
main_root.geometry(f"{root_width}x{root_height}")

yahtzee_label = ctk.CTkLabel(main_root, text="Yahtzee", font=h0_font_cursive)
yahtzee_label.pack(pady=20, padx=20, anchor='nw')

button_frame = ctk.CTkFrame(main_root, corner_radius=0, fg_color=main_color, width=50, height=100)
button_frame.pack(pady=20, padx=20, anchor='nw')

startbutton = ctk.CTkButton(button_frame, text="Start Game", corner_radius=0, fg_color=main_color, hover_color=highlight_color, font=h2_font_underlined, command=start_game)
startbutton.pack(pady=20, padx=20, side='top', anchor='w', fill='x', expand=True)

optionsbutton = ctk.CTkButton(button_frame, text="Options", corner_radius=0, fg_color=main_color, hover_color=highlight_color, font=h2_font_underlined)
optionsbutton.pack(pady=20, padx=20,side='top', anchor='w', fill='x', expand=True)

quitbutton = ctk.CTkButton(button_frame, text="Quit", corner_radius=0, fg_color=main_color, hover_color=highlight_color, font=h2_font_underlined, command=quit_game)
quitbutton.pack(pady=20, padx=20, side='top', anchor='w', fill='x', expand=True)

# ---------------------------- player registration -------------------------------------------------------------------------------- #

outer_register_root = ctk.CTkFrame(main_root, corner_radius=0, fg_color='white', bg_color='white', width=364, height=364)
outer_register_root.propagate(False)

register_root = ctk.CTkFrame(outer_register_root, corner_radius=0,)
register_root.propagate(False)

name_entry = ctk.CTkEntry(register_root, placeholder_text="Enter player name")

add_button = ctk.CTkButton(register_root, text="Add Player", command=add_player, corner_radius=0, fg_color=dark_accent_color, hover_color=light_accent_color)

player_list = ctk.CTkFrame(register_root, corner_radius=0, fg_color=secondary_color)

back_button = ctk.CTkButton(register_root, text="Back", corner_radius=0, fg_color=dark_accent_color, hover_color=highlight_color, command=back_button_activated)

reg_info_box = ctk.CTkLabel(master=register_root, text="  info  ", fg_color=dark_accent_color, corner_radius=0)
reg_info_frame = ctk.CTkFrame(master=register_root, width=root_width//2, height=root_height/2, corner_radius=0, fg_color=main_color, border_width=2, border_color="white")
reg_info_frame.place(relx=0.5, rely=0.5, anchor="center")
reg_info_frame.place_forget()
reg_info_label = ctk.CTkLabel(master=reg_info_frame, text="8 characters maximum for names,\nno blank spaces.\nPlease use abbreviations or\npseudonyms for long names.\n\nMinimum players: 2\nMaximum players:4")
reg_info_label.pack(padx=10, pady=10)

def reg_show_info(event):
    reg_info_frame.place(relx=0.5, rely=0.5, anchor="center")

def reg_hide_info(event):
    reg_info_frame.place_forget()
    
reg_info_box.bind("<Enter>", reg_show_info)
reg_info_box.bind("<Leave>", reg_hide_info)

continue_button = ctk.CTkButton(register_root, text="Continue", command=register_complete, corner_radius=0, fg_color=dark_accent_color, hover_color=light_accent_color)

# ---------------------------- main frame -------------------------------------------------------------------------------- #

inner_root = ctk.CTkFrame(main_root, corner_radius=0)

side_bar = ctk.CTkFrame(master=inner_root, width=root_width//3, corner_radius=0, fg_color=main_color)
side_bar.propagate(False)

turn_indicator = ctk.CTkLabel(master=side_bar, text="DEFAULT STATE", font=standard_font, fg_color=dark_accent_color, pady=20)

scorecard = ctk.CTkFrame(master=side_bar, corner_radius=0, fg_color=main_color)

# ---------------------------- scorecard area -------------------------------------------------------------------------------- #
    
ctk.CTkLabel(master=scorecard, text="Category", font=small_font_bold).grid(row=0, column=0, padx=10, sticky="w")
ctk.CTkLabel(master=scorecard, text="Max Score", font=small_font_bold).grid(row=0, column=1, padx=10)
ctk.CTkLabel(master=scorecard, text="Your Score", font=small_font_bold).grid(row=0, column=2, padx=10)
remove_button = ctk.CTkButton(master=scorecard, text="REMOVE", width=10, fg_color=main_color, font=small_font_bold, corner_radius=0, border_width=0, hover_color=highlight_color, command=remove_category)
remove_button.grid(row=0, column=3, padx=10)

# ---------------------------- categories_stage1 -------------------------------------------------------------------------------- #

for i, (category, max_score) in enumerate(categories_stage1, start=1):
    ctk.CTkLabel(master=scorecard, text=category).grid(row=i, column=0, sticky="w", padx=10)
    ctk.CTkLabel(master=scorecard, text=max_score).grid(row=i, column=1, padx=10)

    score_label = ctk.CTkLabel(master=scorecard, text="0", font=standard_font)
    score_label.grid(row=i, column=2, padx=10)
    score_label.grid_forget()
    score_labels[category] = score_label

    button = ctk.CTkButton(master=scorecard, text="  ←  ", width=5, font=standard_font, fg_color=main_color, corner_radius=0, border_width=0, hover_color=highlight_color, command=lambda c=category: check_input(c))
    button.grid(row=i, column=3, padx=10)
    button.grid_forget()

    buttons.append(button)

# ---------------------------- spacing -------------------------------------------------------------------------------- #

ctk.CTkFrame(master=scorecard, height=5, fg_color=main_color).grid(row=len(categories_stage1)+1, columnspan=5)

# ---------------------------- categories_stage2 -------------------------------------------------------------------------------- #

for i, (category, max_score) in enumerate(categories_stage2, start=len(categories_stage1)+2):
    ctk.CTkLabel(master=scorecard, text=category).grid(row=i, column=0, sticky="w", padx=10)
    ctk.CTkLabel(master=scorecard, text=max_score).grid(row=i, column=1, padx=10)

    score_label = ctk.CTkLabel(master=scorecard, text="0", font=standard_font)
    score_label.grid(row=i, column=2, padx=10)
    score_label.grid_forget()
    score_labels[category] = score_label

    c2_button = ctk.CTkButton(master=scorecard, text="  ←  ", width=5, font=standard_font, fg_color=main_color, corner_radius=0, border_width=0, hover_color=highlight_color, command=lambda c=category: check_input(c))
    c2_button.grid(row=i, column=3, padx=10)
    c2_button.grid_forget()
    c2_button.configure(state='disabled')

    c2_buttons.append(c2_button)

# ---------------------------- main frame continuation -------------------------------------------------------------------------------- #

top_bar = ctk.CTkFrame(master=inner_root, height=root_height//5, corner_radius=0, fg_color=secondary_color)
top_bar.pack_propagate(False)

roll_sort_frame = ctk.CTkFrame(master=top_bar, corner_radius=0, fg_color=secondary_color, width=130)
roll_sort_frame.propagate(False)

roll_button = ctk.CTkButton(master=roll_sort_frame, text="Roll Dice", font=h2_font, fg_color=main_color, corner_radius=0, border_width=0, hover_color=highlight_color, command=roll_dice)
roll_button.propagate(False)

sort_button = ctk.CTkButton(master=roll_sort_frame, text="Sort Dice", font=standard_font, fg_color=main_color, corner_radius=0, border_width=0, hover_color=highlight_color, command=sort_dice)
sort_button.propagate(False)

# ---------------------------- dice images initilizing -------------------------------------------------------------------------------- #
def initialize_dices():
    global images
    
    images = [ImageTk.PhotoImage(Image.open(f"./dice_images/dice{i}.png").resize((root_height//6, root_height//6))) for i in range(1, 7)]

    for _ in range(5):
        label = Label(top_bar, bg=secondary_color, borderwidth=0)
        label.pack(side='left', fill="both", expand=True)
        dice_labels.append(label)

# ---------------------------- main frame continuation -------------------------------------------------------------------------------- #

under_bar = ctk.CTkFrame(master=inner_root, height=root_height/5, corner_radius=0, fg_color=transparent_color)
under_bar.pack_propagate(False)

reroll_button = ctk.CTkButton(master=under_bar, text="Reroll Dice", font=standard_font, fg_color=main_color, corner_radius=0, border_width=0, hover_color=highlight_color)
reroll_button.configure(command=reroll_dice)

input_box = ctk.CTkEntry(master=under_bar, font=standard_font, fg_color=main_color, corner_radius=0, border_width=0)

# ---------------------------- info box function -------------------------------------------------------------------------------- #

input_info_box = ctk.CTkLabel(master=under_bar, text=" info ", font=standard_font, fg_color=main_color, corner_radius=0)

input_info_frame = ctk.CTkFrame(master=inner_root, width=root_width//2, height=root_height/2, corner_radius=0, fg_color=main_color, border_width=2, border_color="white")
input_info_frame.place(relx=0.5, rely=0.5, anchor="center")
input_info_frame.place_forget()

input_info_label = ctk.CTkLabel(master=input_info_frame, text="The reroll functions by inputing the corresponding numbers for the list index.\nFor example, inputing 2 for the dices 4, 2, 6, 3, 6 will reroll the second number, 2.\nTo reroll multiple dices at the same time, write the numbers comma-seperated like such: 1,2,3.\nThis will reroll 4, 2, and 6 from the previous dice list.", font=standard_font)
input_info_label.pack(padx=64, pady=36)

def input_show_info(event):
    input_info_frame.place(relx=0.5, rely=0.5, anchor="center")

def input_hide_info(event):
    input_info_frame.place_forget()

input_info_box.bind("<Enter>", input_show_info)
input_info_box.bind("<Leave>", input_hide_info)

# ---------------------------- main frame continuation -------------------------------------------------------------------------------- #

remaining_reroll = ctk.CTkLabel(master=under_bar, text="Remaining Rerolls: 3", font=standard_font, fg_color=main_color, corner_radius=0)


# ---------------------------- debug -------------------------------------------------------------------------------- #

def debug_init():
    if debug:
        def fill_categories_for_stage_1():
            player = players[player_turn]
            for category, _ in categories_stage1:
                player['categories_stage1_used'].add(category)
                player_scorecards[player_turn][category] = 6
            popup_message(f"All Stage 1 categories filled for {player['name']}.")
            scorecard_update()

        def change_player_turn():
            determine_turn()


        def trigger_stage_2_transition():
            stage_2()

        def trigger_end_game():
            determine_winner()


        debug_frame = ctk.CTkFrame(master=inner_root, corner_radius=0, fg_color='grey')
        debug_frame.pack(side='bottom', fill='x')

        fill_stage1_button = ctk.CTkButton(master=debug_frame, text="Fill Stage 1", command=fill_categories_for_stage_1, corner_radius=0, fg_color=dark_accent_color, hover_color=light_accent_color)
        fill_stage1_button.pack(side='left', padx=10, pady=10)

        change_turn_button = ctk.CTkButton(master=debug_frame, text="Change Turn", command=change_player_turn, corner_radius=0, fg_color=dark_accent_color, hover_color=light_accent_color)
        change_turn_button.pack(side='left', padx=10, pady=10)

        stage_2_button = ctk.CTkButton(master=debug_frame, text="Trigger Stage 2", command=trigger_stage_2_transition, corner_radius=0, fg_color=dark_accent_color, hover_color=light_accent_color)
        stage_2_button.pack(side='left', padx=10, pady=10)

        end_game_button = ctk.CTkButton(master=debug_frame, text="Trigger End Game", command=trigger_end_game, corner_radius=0, fg_color=dark_accent_color, hover_color=light_accent_color)
        end_game_button.pack(side='left', padx=10, pady=10)
  
# ---------------------------- mainloop -------------------------------------------------------------------------------- #

def main():
    if not game_started:
        main_root.mainloop()
    else:
        show_main_frame()
        debug_init()
        determine_turn()
        
if not game_started:
    main()

# ---------------------------- TODO -------------------------------------------------------------------------------- #

# TO FIX NOW
# TODO: buggy remove function, allowing pass turn after removing a already taken category
# TODO: add sound effects and better images
# TODO: try making animations

# TO FIX LATER
# TODO: bug fixes, better error handling, and more user-friendly fixes

# FUTURE IDEAS
# TODO: add a function to play against the computer
# TODO: add a function to play online with friends (socket)
# TODO: add a function to save and load the game state

# TO MAKE AS LAST THING
# TODO: add a settings panel for theme changes and more