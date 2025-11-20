PLACEHOLDER = "[name]"

# Read all invited names
with open("./Input/Names/invited_names.txt", "r") as names_file:
    names = names_file.readlines()

# Read the letter template
with open("./Input/Letters/starting_letter.txt", "r") as letter_file:
    letter_template = letter_file.read()

# Creat and save personalized letters.
for name in names:
    name = name.replace("\n", "")
    new_letter = letter_template.replace(PLACEHOLDER, name)
    with open(f"./Output/ReadyToSend/invited_{name}.txt", "w") as output_file:
        output_file.write(new_letter)
