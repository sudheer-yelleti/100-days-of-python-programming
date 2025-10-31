from turtle import Turtle, Screen

import pandas

screen = Screen()
turtle = Turtle()
turtle.hideturtle()
turtle.penup()
screen.title("U.S. States Game")
screen.setup(width=600, height=600)
screen.bgpic("blank_states_img.gif")

states = pandas.read_csv("50_states.csv")
states_list = states["state"].to_list()
correct_guesses = []
while len(correct_guesses) < 50:
    user_input = screen.textinput(prompt="What's another state's name?",
                                  title=f"U.S. States Game({len(correct_guesses)})/50 Correct").title()
    if user_input in states_list and user_input not in correct_guesses:
        correct_guesses.append(user_input)
        state_data = states[states["state"] == user_input]
        turtle.goto(int(state_data.x), int(state_data.y))
        turtle.write(user_input)
    elif user_input == "Exit":
        missed_states = [state for state in states_list if state not in correct_guesses]
        data_frame = {
            "states": missed_states
        }
        data_missed_states = pandas.DataFrame(data_frame)
        data_missed_states.to_csv("missed_states.csv")
        break

screen.exitonclick()
