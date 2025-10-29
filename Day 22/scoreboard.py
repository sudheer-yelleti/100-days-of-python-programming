from turtle import Turtle


class Scoreboard(Turtle):
    ALIGNMENT = "center"
    FONT = ("Courier", 25, "normal")
    WINNING_SCORE = 5

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        # Left player score
        self.goto(-200, 200)
        self.write(f"PLAYER 1: {self.l_score}", align=self.ALIGNMENT, font=self.FONT)
        # Right player score
        self.goto(200, 200)
        self.write(f"PLAYER 2: {self.r_score}", align=self.ALIGNMENT, font=self.FONT)

    def l_point(self):
        self.l_score += 1
        self.update_scoreboard()

    def r_point(self):
        self.r_score += 1
        self.update_scoreboard()

    def game_over(self):
        """Display Game Over and announce winner or tie."""
        self.goto(0, 0)
        if self.l_score > self.r_score:
            winner = "PLAYER 1 Wins!"
        elif self.r_score > self.l_score:
            winner = "PLAYER 2 Wins!"
        else:
            winner = "IT'S A TIE!"

        self.write("GAME OVER", align=self.ALIGNMENT, font=("Courier", 30, "bold"))
        self.goto(0, -40)
        self.write(f"{winner}", align=self.ALIGNMENT, font=self.FONT)
