##################### Extra Hard Starting Project ######################
import datetime as dt
import logging
import os
import random
import smtplib

import pandas

my_email = "sudheer.167@gmail.com"
my_password = os.environ['GMAIL_APP_PASSWORD']


def send_email(to_email, subject, body):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            to_addrs=to_email,
            from_addr=my_email,
            msg=f"Subject:{subject}\n\n{body}"
        )


try:
    birthdays = pandas.read_csv("birthdays.csv")

    today_day = dt.datetime.now().day
    today_month = dt.datetime.now().month

    for (index, row) in birthdays.iterrows():

        if row.day == today_day and row.month == today_month:
            birthday_person = row["name"]
            letter_choice = random.randint(1, 3)
            with open("./letter_templates/letter_" + str(letter_choice) + ".txt") as letter:
                letter_content = letter.read()
                letter_content = letter_content.replace("[NAME]", birthday_person)
                send_email(to_email=row.email, subject="Happy Birthday!", body=letter_content)
except FileNotFoundError as error:
    logging.error(f"File {error} not found.")
except Exception as error:
    logging.error(f"An error occurred: {error}")
