# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- VARIABLES ------------------------------- #
reps = 0
timer = None

# ---------------------------- UI SETUP ------------------------------- #
from tkinter import *

windows = Tk()
windows.title("Pomodoro")
windows.config(padx=100, pady=50, bg=GREEN)

title_label = Label(text="Timer", fg=YELLOW, bg=GREEN, font=(FONT_NAME, 30))
title_label.grid(row=0, column=1)

canvas = Canvas(width=200, height=224, bg=GREEN, highlightthickness=0)
img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    if timer:
        windows.after_cancel(timer)
    reps = 0
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=YELLOW)
    check_marks.config(text="")
    start_button.config(state="normal")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    start_button.config(state="disabled")

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        title_label.config(text="Long Break", fg=RED)
        countdown(long_break_sec)
    elif reps % 2 == 0:
        title_label.config(text="Short Break", fg=PINK)
        countdown(short_break_sec)
    else:
        title_label.config(text="Work", fg=YELLOW)
        countdown(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    global timer
    count_min = count // 60
    count_sec = count % 60
    canvas.itemconfig(timer_text, text=f"{count_min:02d}:{count_sec:02d}")

    if count > 0:
        timer = windows.after(1000, countdown, count - 1)
    else:
        # Only start next cycle after previous fully completes
        if reps < 8:
            start_timer()

        # Update checkmarks after every work session
        marks = "✅" * (reps // 2)
        check_marks.config(text=marks)

        # Re-enable Start button after 8 sessions (full cycle)
        if reps % 8 == 0:
            start_button.config(state="normal")


# ---------------------------- BUTTONS ------------------------------- #
start_button = Button(text="Start", command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", command=reset_timer)
reset_button.grid(row=2, column=2)

check_marks = Label(fg=YELLOW, bg=GREEN)
check_marks.grid(row=3, column=1)

windows.mainloop()
