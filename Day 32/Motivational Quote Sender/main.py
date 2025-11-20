import datetime as dt
import os
import random
import smtplib
import logging

my_email = "sudheer.167@gmail.com"
my_password = os.environ['GMAIL_APP_PASSWORD']


def send_email(subject, body):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            to_addrs="sudheer.167@gmail.com",
            from_addr=my_email,
            msg=f"Subject:{subject}\n\n{body}"
        )


today = dt.date.today().isoweekday()
if today == 2:
    try:
        with open("quotes.txt", "r") as file:
            quotes = file.read().splitlines()
    except FileNotFoundError as error:
       logging.warning(f"File {error} not found.")

    else:
        quote_of_the_day = random.choice(quotes)
        send_email("Quote of the day", quote_of_the_day)
