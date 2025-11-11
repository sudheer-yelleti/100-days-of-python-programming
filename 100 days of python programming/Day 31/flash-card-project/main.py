import random
from tkinter import *
from tkinter import messagebox

import pandas

BACKGROUND_COLOR = "#B1DDC6"
french_words = []
word_to_learn_dict = {}
try:

    french_words = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:

    french_words = pandas.read_csv("./data/french_words.csv")
finally:
    word_to_learn_dict = {row.French: row.English for (index, row) in french_words.iterrows()}
    new_word = ""


def next_card():
    global new_word, flip_timer
    window.after_cancel(flip_timer)
    if word_to_learn_dict == {}:
        messagebox.showinfo(title="All done", message="You've completed all the words!")
        return
    new_word = random.choice(list(word_to_learn_dict.keys()))
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=new_word, fill="black")

    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    global new_word
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=word_to_learn_dict[new_word], fill="white")


def is_known():
    word_to_learn_dict.pop(new_word)
    next_card()
    data = pandas.DataFrame(list(word_to_learn_dict.items()), columns=["French", "English"])
    data.to_csv("./data/words_to_learn.csv", index=False)


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file="./images/wrong.png")
button_unknown = Button(image=wrong_img, highlightthickness=0, command=next_card)
button_unknown.grid(row=1, column=0)

right_img = PhotoImage(file="./images/right.png")
button_known = Button(image=right_img, highlightthickness=0, command=is_known)
button_known.grid(row=1, column=1)

next_card()

window.mainloop()
