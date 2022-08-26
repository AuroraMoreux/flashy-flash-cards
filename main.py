import random
from tkinter import *

import pandas

BACKGROUND_COLOR = "#B1DDC6"

to_learn = []
current_card = {}


def load_words():
    data = pandas.DataFrame()
    try:
        data = pandas.read_csv("./data/words_to_learn.csv")
    except FileNotFoundError:
        data = pandas.read_csv("./data/french_words.csv")
    finally:
        global to_learn
        to_learn = data.to_dict(orient="records")  # or {row[1].French: row[1].English for row in data.iterrows()}


def next_card(button):
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, flip_card)
    if button == "yes":
        remove_known_word()


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def remove_known_word():
    to_learn.remove(current_card)
    pandas.DataFrame(to_learn).to_csv("./data/words_to_learn.csv", index=False)


window = Tk()
window.title("Flashy")
window.config(background=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)

card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

yes_button_image = PhotoImage(file="./images/right.png")
yes_button = Button(image=yes_button_image, highlightthickness=0, command=lambda: next_card("yes"))
yes_button.grid(row=1, column=1)

no_button_image = PhotoImage(file="./images/wrong.png")
no_button = Button(image=no_button_image, highlightthickness=0, command=lambda: next_card("no"))
no_button.grid(row=1, column=0)

load_words()
next_card("no")

window.mainloop()
