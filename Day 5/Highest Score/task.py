student_scores = [89, 142, 185, 120, 171, 184, 149, 24, 59, 68, 150, 78, 65, 89, 86, 55, 91, 64, 199]
for i in range(1, 10):
    print(student_scores[i])

# Print maximum number in the list without using inbuilt functions.
max_score = student_scores[0]
for score in student_scores:
    if score > max_score:
        max_score = score
print(f"Max score is {max_score}")
