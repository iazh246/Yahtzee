# ---------------------------- imports ------------------------------- #

import customtkinter as ctk
from customtkinter import *

import tkinter as tk
from tkinter import ttk
from tkinter import *

from PIL import Image, ImageTk

import random

from fonts_and_colors import *
from lists_and_variables import *

from win_screen import determine_winner


# ---------------------------- functions ------------------------------- #

def popup_message(message):
    try:
        error_frame = ctk.CTkFrame(outer_root, border_width=2, border_color='white', fg_color=main_color, corner_radius=0)
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
            error_root.destroy()
        
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
    
def cross_category(category):    
    if not stage_2_activated:
        players[player_turn]['categories_stage1_used'].add(category)
        player_scorecards[player_turn][category] = '-----'
        
        for i, button in enumerate(buttons):
            button.configure(command=lambda c=i: check_input(categories_stage1[c][0]), fg_color=main_color)
    else:
        players[player_turn]['categories_stage2_used'].add(category)
        c2_player_scorecards[player_turn][category] = '-----'
        
        for i, button in enumerate(c2_buttons):
            button.configure(command=lambda c=i: check_input(categories_stage2[c][0]), fg_color=main_color)
    
    scorecard_update()

    remove_button.configure(state='disabled')
    
    def next_turn():
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


def check_input(category):
    global player_turn, players, score_labels

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
        if category in players[player_turn]['categories_stage1_used']:
            popup_message("Category already filled. Please select another category.")
            return
        if category not in [category for category, _ in categories_stage1]:
            popup_message("Invalid category. Please select a valid category.")
            return
    else:
        if category in players[player_turn]['categories_stage2_used']:
            popup_message("Category already filled. Please select another category.")
            return
        if category not in [category for category, _ in categories_stage2]:
            popup_message("Invalid category. Please select a valid category.")
            return
    
    if category in category_to_number and not any(die == category_to_number[category] for die in dice):
        popup_message(f"No {category.lower()} found. Please select another category.")
        return

    if category in category_to_number:
        score = sum(die == category_to_number[category] for die in dice) * category_to_number[category]

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
        
        if not conditions[category](dice):
            popup_message(f"No valid {category} found. Please select another category.")
            return

    if category in ["3K", "4K", "Chance"]:
        score = sum(dice)
    elif category == "Full House":
        score = 25  
    elif category == "S.Straight":
        score = 30  
    elif category == "L.Straight":
        score = 40  
    elif category == "Yatzy":
        score = 50  
    
    if not stage_2_activated:
        players[player_turn]['score'] += score
        player_scorecards[player_turn][category] = score
        players[player_turn]['categories_stage1_used'].add(category)
    else:
        players[player_turn]['categories_stage2_used'].add(category)
        c2_player_scorecards[player_turn][category] = score

    def next_turn():
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
                popup_message(f"{players[player_turn]['name']} scored {score} points in the {category} category!\nIt is now the next players turn.")
                continue_button_scorecard.destroy()
                determine_turn()
        else:
            if all(len(player['categories_stage2_used']) == len(categories_stage2) for player in players):
                popup_message("Game has ended! All categories in stage 2 have been filled.")
                continue_button_scorecard.destroy()
                determine_winner()
            else:
                popup_message(f"{players[player_turn]['name']} scored {score} points in the {category} category!\nIt is now the next players turn.")
                continue_button_scorecard.destroy()
                determine_turn()

    continue_button_scorecard = ctk.CTkButton(master=side_bar, text="Pass Turn", font=standard_font, fg_color=dark_accent_color, corner_radius=0, hover_color=light_accent_color, command=next_turn)
    continue_button_scorecard.pack(side="top", pady=20)
    scorecard_update()

    for indv_buttons in buttons and c2_buttons:
        indv_buttons.configure(state='disabled')
    

#independent of stages

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

def register_complete():
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

    register_root.destroy()

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

# ---------------------------------------------------------------------- #











# ---------------------------- player registration ------------------------------- #

register_root = ctk.CTk()
register_root.title("Player Registration")
register_root.resizable(False, False)

register_root.geometry("250x350")
register_root.eval('tk::PlaceWindow . center')
register_root.propagate(True)


name_entry = ctk.CTkEntry(register_root, placeholder_text="Enter player name")
name_entry.pack(pady=10)

add_button = ctk.CTkButton(register_root, text="Add Player", command=add_player, corner_radius=0, fg_color=dark_accent_color, hover_color=light_accent_color)
add_button.pack(pady=5)

player_list = ctk.CTkFrame(register_root, corner_radius=0, fg_color=secondary_color)
player_list.pack(pady=10, fill='both', expand=True)

reg_info_box = ctk.CTkLabel(master=register_root, text="  info  ", fg_color=dark_accent_color, corner_radius=0)
reg_info_box.pack(side="left", padx=10, pady=10)

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
continue_button.pack(side='right', padx=10, pady=10)

register_root.mainloop()

if len(players) < 2:
    popup_message("No players or only 1 was registered. Please register at least two players.")
    register_root.mainloop()

# -------------------------------------------------------------------------------- #










# ---------------------------- main frame ------------------------------- #

outer_root = ctk.CTk()
outer_root.title('~~ Yatzy ~~')
outer_root.geometry(f"{root_width}x{root_height}")
outer_root.resizable(False, False)

inner_root = ctk.CTkFrame(master=outer_root, corner_radius=0)
inner_root.pack(padx=0, pady=0, fill='both', expand=True)

side_bar = ctk.CTkFrame(master=inner_root, width=root_width//3, corner_radius=0, fg_color=main_color)
side_bar.pack(side="left", fill="y")
side_bar.propagate(False)

turn_indicator = ctk.CTkLabel(master=side_bar, text="DEFAULT STATE", font=standard_font, fg_color=dark_accent_color, pady=20)
turn_indicator.pack(side="top", fill="x")

scorecard = ctk.CTkFrame(master=side_bar, corner_radius=0, fg_color=main_color)
scorecard.pack(anchor='n', expand=True)

ctk.CTkLabel(master=scorecard, text="Category", font=small_font_bold).grid(row=0, column=0, padx=10, sticky="w")
ctk.CTkLabel(master=scorecard, text="Max Score", font=small_font_bold).grid(row=0, column=1, padx=10)
ctk.CTkLabel(master=scorecard, text="Your Score", font=small_font_bold).grid(row=0, column=2, padx=10)
remove_button = ctk.CTkButton(master=scorecard, text="REMOVE", width=10, fg_color=main_color, font=small_font_bold, corner_radius=0, border_width=0, hover_color=highlight_color, command=remove_category)
remove_button.grid(row=0, column=3, padx=10)

# ---------------------------- categories_stage1 ------------------------------- #

for i, (category, max_score) in enumerate(categories_stage1, start=1):
    ctk.CTkLabel(master=scorecard, text=category).grid(row=i, column=0, sticky="w", padx=10)
    ctk.CTkLabel(master=scorecard, text=max_score).grid(row=i, column=1, padx=10)
    
    score_label = ctk.CTkLabel(master=scorecard, text="0", font=standard_font)
    score_label.grid(row=i, column=2, padx=10)
    score_labels[category] = score_label

    button = ctk.CTkButton(master=scorecard, text="  ←  ", width=5, font=standard_font, fg_color=main_color, corner_radius=0, border_width=0, hover_color=highlight_color, command=lambda c=category: check_input(c))
    button.grid(row=i, column=3, padx=10)

    buttons.append(button)

# ---------------------------- spacing ------------------------------- #

ctk.CTkFrame(master=scorecard, height=5, fg_color=main_color).grid(row=len(categories_stage1)+1, columnspan=5)

# ---------------------------- categories_stage2 ------------------------------- #

for i, (category, max_score) in enumerate(categories_stage2, start=len(categories_stage1)+2):
    ctk.CTkLabel(master=scorecard, text=category).grid(row=i, column=0, sticky="w", padx=10)
    ctk.CTkLabel(master=scorecard, text=max_score).grid(row=i, column=1, padx=10)
    
    score_label = ctk.CTkLabel(master=scorecard, text="0", font=standard_font)
    score_label.grid(row=i, column=2, padx=10)
    score_labels[category] = score_label

    c2_button = ctk.CTkButton(master=scorecard, text="  ←  ", width=5, font=standard_font, fg_color=main_color, corner_radius=0, border_width=0, hover_color=highlight_color, command=lambda c=category: check_input(c))
    c2_button.grid(row=i, column=3, padx=10)
    c2_button.configure(state='disabled')
    
    c2_buttons.append(c2_button)
    
top_bar = ctk.CTkFrame(master=inner_root, height=root_height//5, corner_radius=0, fg_color=secondary_color)
top_bar.pack_propagate(False)
top_bar.pack(side="top", fill="x")

roll_sort_frame = ctk.CTkFrame(master=top_bar, corner_radius=0, fg_color=secondary_color, width=130)
roll_sort_frame.pack(side="left", padx=12)
roll_sort_frame.propagate(False)

roll_button = ctk.CTkButton(master=roll_sort_frame, text="Roll Dice", font=h2_font, fg_color=main_color, corner_radius=0, border_width=0, hover_color=highlight_color, command=roll_dice)
roll_button.pack(side='top', pady=10)
roll_button.propagate(False)

sort_button = ctk.CTkButton(master=roll_sort_frame, text="Sort Dice", font=standard_font, fg_color=main_color, corner_radius=0, border_width=0, hover_color=highlight_color, command=sort_dice)
sort_button.pack(side='bottom', pady=10)
sort_button.propagate(False)

images = [ImageTk.PhotoImage(Image.open(f"./dice_images/dice{i}.png").resize((root_height//6, root_height//6))) for i in range(1, 7)]

for _ in range(5):
    label = Label(top_bar, bg=secondary_color, borderwidth=0)
    label.pack(side='left', fill="both", expand=True)
    dice_labels.append(label)

under_bar = ctk.CTkFrame(master=inner_root, height=root_height/5, corner_radius=0, fg_color=transparent_color)
under_bar.pack_propagate(False)
under_bar.pack(side="top", fill="x")

reroll_button = ctk.CTkButton(master=under_bar, text="Reroll Dice", font=standard_font, fg_color=main_color, corner_radius=0, border_width=0, hover_color=highlight_color)
reroll_button.pack(side="left", expand=True)
reroll_button.configure(command=reroll_dice)

input_box = ctk.CTkEntry(master=under_bar, font=standard_font, fg_color=main_color, corner_radius=0, border_width=0)
input_box.pack(side="left", expand=True, fill="x", padx=10)

input_info_box = ctk.CTkLabel(master=under_bar, text=" info ", font=standard_font, fg_color=main_color, corner_radius=0)
input_info_box.pack(side="left", expand=True)

input_info_frame = ctk.CTkFrame(master=outer_root, width=root_width//2, height=root_height/2, corner_radius=0, fg_color=main_color, border_width=2, border_color="white")
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

remaining_reroll = ctk.CTkLabel(master=under_bar, text="Remaining Rerolls: 3", font=standard_font, fg_color=main_color, corner_radius=0)
remaining_reroll.pack(side="right", expand=True, fill="x", padx=10)

if debug:
    def fill_categories_for_stage_1():
        player = players[player_turn]
        for category, _ in categories_stage1:
            player['categories_stage1_used'].add(category)
            player_scorecards[player_turn][category] = 6  # Assigning max points for simplification
        popup_message(f"All Stage 1 categories filled for {player['name']}.")
        scorecard_update()
    
    def change_player_turn():
        determine_turn()

    def trigger_stage_2_transition():
        stage_2()

    def trigger_end_game():
        determine_winner()  # Assuming this function handles the end game screen

    
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
  


determine_turn()
game_started = True
outer_root.mainloop()















# TO FIX NOW

# TODO: fix the category filled popup
# TODO: fix the play again button in the win screen
# TODO: finish the code for fundamental game functionality

# TO FIX LATER

# TODO: bug fixes, better error handling, and more user-friendly fixes

# FUTURE IDEAS

# TODO: add sound effects and better images
# TODO: try making animations
# TODO: add a function to play against the computer
# TODO: add a function to play online with friends (socket)
# TODO: add a function to save and load the game state

# TO MAKE AS LAST THING

# TODO: add a settings panel for theme changes and more


[{'3K': 0, '4K': 0, 'Full House': 0, 'S.Straight': 0, 'L.Straight': 0, 'Yatzy': 0, 'Chance': 0}, 
 {'3K': 0, '4K': 0, 'Full House': 0, 'S.Straight': 0, 'L.Straight': 0, 'Yatzy': 0, 'Chance': 0}, 
 {'3K': 0, '4K': 0, 'Full House': 0, 'S.Straight': 0, 'L.Straight': 0, 'Yatzy': 0, 'Chance': 0}, 
 {'3K': 0, '4K': 0, 'Full House': 0, 'S.Straight': 0, 'L.Straight': 0, 'Yatzy': 0, 'Chance': 0}]

{'Threes', 'Twos', 'Sixes', 'Fours', 'Fives', 'Ones'}
set()