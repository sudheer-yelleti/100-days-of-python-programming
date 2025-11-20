import random

number_of_guesses = 0
is_game_over = False


def validate_guess(guess_number):
    global is_game_over
    if guess_number == answer:
        is_game_over = True
        return f"You guessed right! The number was {answer}"
    elif guess_number < answer:
        return "Too low! Guess again"
    else:
        return "Too high! Guess again"


print("Welcome to the number guessing game!\n I'm thinking of a number between 1 and 100")
answer = random.randint(1, 100)
print(answer)
difficulty_level = input("Choose the difficulty level(EASY/HARD): ")

if difficulty_level == "EASY":
    number_of_guesses = 10
else:
    number_of_guesses = 5

while number_of_guesses > 0 and not is_game_over:
    print(f" You have {number_of_guesses} guesses left to guess the number.")
    guess = int(input("Make a guess: "))

    if guess < 1 or guess > 100:
        print("Sorry, your guess should be between 1 and 100")
    else:
        print(validate_guess(guess))
        if not is_game_over:
            number_of_guesses -= 1

if number_of_guesses == 0 and not is_game_over:
    print(f"Sorry, you ran out of guesses. The correct number is : {answer}")
