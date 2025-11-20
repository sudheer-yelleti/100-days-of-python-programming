from tkinter import *

from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = Label(text="Score: 0", fg="white", bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(150, 125, width=300, text="Question Text",
                                                     font=("Arial", 20, "italic"),
                                                     fill=THEME_COLOR)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        true_image = PhotoImage(file="./images/true.png")
        self.true_button = Button(image=true_image, highlightthickness=0, command=self.true_pressed)
        self.true_button.grid(row=2, column=0)
        false_image = PhotoImage(file="./images/false.png")
        self.false_button = Button(image=false_image, highlightthickness=0, command=self.false_pressed)
        self.false_button.grid(row=2, column=1)

        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        question = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=question)

    def true_pressed(self):
        if self.quiz.check_answer("True"):
            self.score_label.config(text=f"Score: {self.quiz.score}")
        if self.quiz.still_has_questions():
            self.get_next_question()
        else:
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
            self.canvas.itemconfig(self.question_text,
                                   text=f"You've reached the end of the quiz.Your final score is: {self.quiz.score}")

    def false_pressed(self):
        if self.quiz.check_answer("False"):
            self.score_label.config(text=f"Score: {self.quiz.score}")
        if self.quiz.still_has_questions():
            self.get_next_question()
        else:
            self.false_button.config(state="disabled")
            self.true_button.config(state="disabled")
            self.canvas.itemconfig(self.question_text,
                                   text=f"You've reached the end of the quiz.Your final score is: {self.quiz.score}")
