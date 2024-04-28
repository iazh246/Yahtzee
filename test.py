import customtkinter as ctk
from customtkinter import *

import tkinter as tk
from tkinter import ttk
from tkinter import *

from PIL import Image, ImageTk

import random

from fonts_and_colors import *
from lists_and_variables import *
 
winners = sorted(players, key=lambda x: x['score'], reverse=True)
winners.extend([None] * (4 - len(winners)))
winner = winners[0] if winners[0] else None


player_1 = winners[0]
player_2 = winners[1]
player_3 = winners[2]
player_4 = winners[3]

winner = winners[0]['name']

root_width = 1920 // 2
root_height = 1080 // 2

winner_root = ctk.CTk()
winner_root.title('~~ Yatzy | Winner ~~')
winner_root.geometry(f"{root_width}x{root_height}")
winner_root.resizable(False, False)

winner_frame = ctk.CTkFrame(winner_root, corner_radius=0, fg_color=main_color)
winner_frame.pack(fill="both", expand=True)

colors = ['#404040', '#454545', '#505050', '#555555']

podium_sizes = [(100, 180), (100, 240), (100, 300), (100, 120)]

total_width = sum(size[0] for size in podium_sizes)
start_x = (root_width - total_width) / 2

bottom_align = (root_height - podium_sizes[2][1]) * 2

ctk.CTkLabel(master=winner_frame, text=f'Congratulations, {winner} has won!', font=h1_cursive_font).place(x=root_width/2, y=50, anchor='n')

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

winner_continue = ctk.CTkButton(master=winner_frame, text='Play Again', font=standard_font, corner_radius=0, fg_color=light_accent_color, hover_color=dark_accent_color)
winner_continue.place(x=root_width-10, y=root_height-10, anchor='se')

winner_root.mainloop()