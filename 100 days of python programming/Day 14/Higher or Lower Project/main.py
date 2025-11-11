import random

import art
import game_data

print(art.logo)
a = random.choice(game_data.data)
b = random.choice(game_data.data)
while a == b:
    b = random.choice(game_data.data)
score = 0


def check_answer(user_guess, a_followers, b_followers):
    if a_followers > b_followers:
        return user_guess == "A"
    elif b_followers > a_followers:
        return user_guess == "B"


should_game_continue = True
while should_game_continue:
    print(f"Compare A: {a["name"]}, a {a["description"]}, from {a["country"]}")
    print(art.vs)
    print(f"Against B: {b["name"]}, a {b["description"]}, from {b["country"]}")
    guess = input("Who has more followers? Type 'A' or 'B': ").upper()

    if guess not in ["A", "B"]:
        print("Sorry!, that's an invalid input. Please type 'A' or 'B'.")
        continue
    is_guess_correct = check_answer(guess, a["follower_count"], b["follower_count"])
    if is_guess_correct:
        score += 1
        print(f"You guessed right! Current score: {score}")
        if a["follower_count"] > b["follower_count"]:
            winner = a
        else:
            winner = b
        a = winner
        b = random.choice(game_data.data)
        while a == b:
            b = random.choice(game_data.data)
    else:
        should_game_continue = False
        print(f"Sorry, that's wrong. Final score: {score}")
