import random

# choosing a random string from a list of strings
friends = ["Alice", "Bob", "Charlie", "David", "Emanuel"]
print(random.choice(friends))

random_nuber = random.randint(0, len(friends) - 1)
print(friends[random_nuber])
